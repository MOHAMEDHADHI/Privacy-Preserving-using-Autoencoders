#!/usr/bin/env python3
"""
Admin & Monitoring Dashboard
Web interface for monitoring privacy-preserving ML pipeline
"""

from flask import Flask, render_template, jsonify, request, send_file
import json
import os
from datetime import datetime, timedelta
import sqlite3
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

app = Flask(__name__, template_folder='dashboard_templates')

# Database setup
DB_PATH = 'monitoring.db'

def init_database():
    """Initialize SQLite database for monitoring"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Training sessions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS training_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT UNIQUE,
            timestamp TEXT,
            data_samples INTEGER,
            latent_dim INTEGER,
            models_trained INTEGER,
            best_model TEXT,
            best_accuracy REAL,
            training_time REAL,
            cloud_provider TEXT,
            privacy_preserved BOOLEAN,
            status TEXT
        )
    ''')
    
    # Model results table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS model_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            model_name TEXT,
            train_accuracy REAL,
            test_accuracy REAL,
            precision_score REAL,
            recall_score REAL,
            f1_score REAL,
            training_time REAL,
            timestamp TEXT,
            FOREIGN KEY (session_id) REFERENCES training_sessions(session_id)
        )
    ''')
    
    # System metrics table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS system_metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            cpu_usage REAL,
            memory_usage REAL,
            active_sessions INTEGER,
            total_requests INTEGER
        )
    ''')
    
    # Audit log table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS audit_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            action TEXT,
            user TEXT,
            details TEXT,
            status TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

def log_training_session(session_data):
    """Log training session to database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO training_sessions 
        (session_id, timestamp, data_samples, latent_dim, models_trained, 
         best_model, best_accuracy, training_time, cloud_provider, 
         privacy_preserved, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        session_data.get('session_id'),
        session_data.get('timestamp'),
        session_data.get('data_samples'),
        session_data.get('latent_dim'),
        session_data.get('models_trained'),
        session_data.get('best_model'),
        session_data.get('best_accuracy'),
        session_data.get('training_time'),
        session_data.get('cloud_provider', 'render'),
        session_data.get('privacy_preserved', True),
        session_data.get('status', 'completed')
    ))
    
    conn.commit()
    conn.close()

def log_audit_action(action, user, details, status='success'):
    """Log audit action"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO audit_log (timestamp, action, user, details, status)
        VALUES (?, ?, ?, ?, ?)
    ''', (datetime.now().isoformat(), action, user, details, status))
    
    conn.commit()
    conn.close()

@app.route('/')
def dashboard_home():
    """Main dashboard page"""
    return render_template('dashboard.html')

@app.route('/api/stats/overview')
def get_overview_stats():
    """Get overview statistics"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Total sessions
    cursor.execute('SELECT COUNT(*) FROM training_sessions')
    total_sessions = cursor.fetchone()[0]
    
    # Total models trained
    cursor.execute('SELECT SUM(models_trained) FROM training_sessions')
    total_models = cursor.fetchone()[0] or 0
    
    # Average accuracy
    cursor.execute('SELECT AVG(best_accuracy) FROM training_sessions WHERE best_accuracy IS NOT NULL')
    avg_accuracy = cursor.fetchone()[0] or 0
    
    # Privacy preserved rate
    cursor.execute('SELECT COUNT(*) FROM training_sessions WHERE privacy_preserved = 1')
    privacy_preserved = cursor.fetchone()[0]
    privacy_rate = (privacy_preserved / total_sessions * 100) if total_sessions > 0 else 100
    
    # Recent sessions (last 24 hours)
    yesterday = (datetime.now() - timedelta(days=1)).isoformat()
    cursor.execute('SELECT COUNT(*) FROM training_sessions WHERE timestamp > ?', (yesterday,))
    recent_sessions = cursor.fetchone()[0]
    
    conn.close()
    
    return jsonify({
        'total_sessions': total_sessions,
        'total_models': int(total_models),
        'avg_accuracy': round(avg_accuracy, 3),
        'privacy_rate': round(privacy_rate, 1),
        'recent_sessions': recent_sessions,
        'status': 'healthy'
    })

@app.route('/api/sessions/recent')
def get_recent_sessions():
    """Get recent training sessions"""
    limit = request.args.get('limit', 10, type=int)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT session_id, timestamp, data_samples, best_model, 
               best_accuracy, training_time, cloud_provider, status
        FROM training_sessions
        ORDER BY timestamp DESC
        LIMIT ?
    ''', (limit,))
    
    sessions = []
    for row in cursor.fetchall():
        sessions.append({
            'session_id': row[0],
            'timestamp': row[1],
            'data_samples': row[2],
            'best_model': row[3],
            'best_accuracy': row[4],
            'training_time': row[5],
            'cloud_provider': row[6],
            'status': row[7]
        })
    
    conn.close()
    
    return jsonify({'sessions': sessions})

@app.route('/api/sessions/<session_id>')
def get_session_details(session_id):
    """Get detailed session information"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Get session info
    cursor.execute('''
        SELECT * FROM training_sessions WHERE session_id = ?
    ''', (session_id,))
    
    session = cursor.fetchone()
    if not session:
        conn.close()
        return jsonify({'error': 'Session not found'}), 404
    
    # Get model results
    cursor.execute('''
        SELECT model_name, train_accuracy, test_accuracy, 
               precision_score, recall_score, f1_score, training_time
        FROM model_results
        WHERE session_id = ?
    ''', (session_id,))
    
    models = []
    for row in cursor.fetchall():
        models.append({
            'model_name': row[0],
            'train_accuracy': row[1],
            'test_accuracy': row[2],
            'precision': row[3],
            'recall': row[4],
            'f1_score': row[5],
            'training_time': row[6]
        })
    
    conn.close()
    
    return jsonify({
        'session_id': session[1],
        'timestamp': session[2],
        'data_samples': session[3],
        'latent_dim': session[4],
        'models': models,
        'best_model': session[6],
        'best_accuracy': session[7],
        'total_training_time': session[8],
        'cloud_provider': session[9],
        'privacy_preserved': bool(session[10]),
        'status': session[11]
    })

@app.route('/api/performance/trends')
def get_performance_trends():
    """Get performance trends over time"""
    days = request.args.get('days', 7, type=int)
    start_date = (datetime.now() - timedelta(days=days)).isoformat()
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT timestamp, best_accuracy, training_time
        FROM training_sessions
        WHERE timestamp > ? AND best_accuracy IS NOT NULL
        ORDER BY timestamp ASC
    ''', (start_date,))
    
    trends = []
    for row in cursor.fetchall():
        trends.append({
            'timestamp': row[0],
            'accuracy': row[1],
            'training_time': row[2]
        })
    
    conn.close()
    
    return jsonify({'trends': trends})

@app.route('/api/models/comparison')
def get_model_comparison():
    """Compare model performance across all sessions"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT model_name, 
               AVG(test_accuracy) as avg_accuracy,
               AVG(f1_score) as avg_f1,
               COUNT(*) as usage_count
        FROM model_results
        GROUP BY model_name
        ORDER BY avg_accuracy DESC
    ''', ())
    
    comparison = []
    for row in cursor.fetchall():
        comparison.append({
            'model_name': row[0],
            'avg_accuracy': round(row[1], 3),
            'avg_f1': round(row[2], 3),
            'usage_count': row[3]
        })
    
    conn.close()
    
    return jsonify({'comparison': comparison})

@app.route('/api/audit/log')
def get_audit_log():
    """Get audit log entries"""
    limit = request.args.get('limit', 50, type=int)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT timestamp, action, user, details, status
        FROM audit_log
        ORDER BY timestamp DESC
        LIMIT ?
    ''', (limit,))
    
    logs = []
    for row in cursor.fetchall():
        logs.append({
            'timestamp': row[0],
            'action': row[1],
            'user': row[2],
            'details': row[3],
            'status': row[4]
        })
    
    conn.close()
    
    return jsonify({'logs': logs})

@app.route('/api/export/session/<session_id>')
def export_session(session_id):
    """Export session data as JSON"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Get all session data
    cursor.execute('SELECT * FROM training_sessions WHERE session_id = ?', (session_id,))
    session = cursor.fetchone()
    
    if not session:
        conn.close()
        return jsonify({'error': 'Session not found'}), 404
    
    cursor.execute('SELECT * FROM model_results WHERE session_id = ?', (session_id,))
    models = cursor.fetchall()
    
    conn.close()
    
    export_data = {
        'session_id': session[1],
        'timestamp': session[2],
        'data_samples': session[3],
        'latent_dim': session[4],
        'models_trained': session[5],
        'best_model': session[6],
        'best_accuracy': session[7],
        'training_time': session[8],
        'cloud_provider': session[9],
        'privacy_preserved': bool(session[10]),
        'status': session[11],
        'models': [
            {
                'model_name': m[2],
                'train_accuracy': m[3],
                'test_accuracy': m[4],
                'precision': m[5],
                'recall': m[6],
                'f1_score': m[7],
                'training_time': m[8]
            } for m in models
        ]
    }
    
    # Save to file
    filename = f'session_{session_id}_export.json'
    with open(filename, 'w') as f:
        json.dump(export_data, f, indent=2)
    
    return send_file(filename, as_attachment=True)

@app.route('/api/charts/accuracy_trend')
def generate_accuracy_chart():
    """Generate accuracy trend chart"""
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query('''
        SELECT timestamp, best_accuracy 
        FROM training_sessions 
        WHERE best_accuracy IS NOT NULL
        ORDER BY timestamp ASC
    ''', conn)
    conn.close()
    
    if df.empty:
        return jsonify({'error': 'No data available'}), 404
    
    plt.figure(figsize=(10, 6))
    plt.plot(range(len(df)), df['best_accuracy'], marker='o', linewidth=2)
    plt.title('Model Accuracy Trend Over Time', fontsize=14, fontweight='bold')
    plt.xlabel('Training Session')
    plt.ylabel('Best Accuracy')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    chart_path = 'static/accuracy_trend.png'
    os.makedirs('static', exist_ok=True)
    plt.savefig(chart_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    return send_file(chart_path, mimetype='image/png')

if __name__ == '__main__':
    init_database()
    port = int(os.environ.get('DASHBOARD_PORT', 5001))
    print(f"🎯 Admin Dashboard starting on http://localhost:{port}")
    print(f"📊 Monitoring database: {DB_PATH}")
    app.run(host='0.0.0.0', port=port, debug=True)
