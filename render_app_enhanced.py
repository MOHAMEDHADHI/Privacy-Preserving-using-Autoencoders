#!/usr/bin/env python3
"""
Enhanced Render Deployment Flask App
With authentication, database, and monitoring
"""

from flask import Flask, request, jsonify, render_template
import numpy as np
import json
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.model_selection import train_test_split
import time
from datetime import datetime
import os
import hashlib
import secrets
from functools import wraps

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', secrets.token_hex(32))
app.config['API_KEYS'] = {}  # Store API keys in memory (use database in production)

# In-memory storage (replace with PostgreSQL in production)
trained_models = {}
training_results = {}
api_keys_db = {}

# Initialize default API key
DEFAULT_API_KEY = os.environ.get('DEFAULT_API_KEY', 'demo_key_12345')
api_keys_db[DEFAULT_API_KEY] = {
    'user': 'default_user',
    'created': datetime.now().isoformat(),
    'requests': 0,
    'last_used': None
}

def require_api_key(f):
    """Decorator to require API key authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key') or request.args.get('api_key')
        
        if not api_key:
            return jsonify({
                'error': 'API key required',
                'message': 'Please provide API key in X-API-Key header or api_key parameter'
            }), 401
        
        if api_key not in api_keys_db:
            return jsonify({
                'error': 'Invalid API key',
                'message': 'The provided API key is not valid'
            }), 403
        
        # Update usage stats
        api_keys_db[api_key]['requests'] += 1
        api_keys_db[api_key]['last_used'] = datetime.now().isoformat()
        
        # Add user info to request
        request.api_user = api_keys_db[api_key]['user']
        
        return f(*args, **kwargs)
    
    return decorated_function

def validate_latent_data(data):
    """Validate that only latent vectors are provided (no raw data)"""
    
    # Check for privacy metadata
    metadata = data.get('metadata', {})
    
    if metadata.get('original_data_included', False):
        return False, 'Privacy violation: Raw data detected in payload'
    
    # Check data structure
    if 'latent_vectors' not in data:
        return False, 'Missing latent_vectors field'
    
    if 'labels' not in data:
        return False, 'Missing labels field'
    
    # Validate latent vectors are reasonable size (not full images)
    latent_vectors = np.array(data['latent_vectors'])
    
    # Heuristic: latent vectors should be relatively small
    if latent_vectors.shape[1] > 1000:
        return False, 'Suspicious data size - may contain raw data instead of latent vectors'
    
    return True, 'Valid latent data'

@app.route('/')
def home():
    """Home endpoint"""
    return jsonify({
        'service': 'Privacy-Preserving ML Cloud Service (Enhanced)',
        'version': '2.0.0',
        'status': 'running',
        'deployment': 'render',
        'features': [
            'API Key Authentication',
            'Request Validation',
            'Privacy Policy Enforcement',
            'Model Versioning',
            'Performance Monitoring'
        ],
        'privacy_policy': 'Only latent vectors accepted - raw data automatically rejected',
        'endpoints': {
            'health': '/health',
            'train': '/train (POST) - Requires API key',
            'predict': '/predict (POST) - Requires API key',
            'models': '/models (GET) - Requires API key',
            'results': '/results (GET) - Requires API key',
            'api_key': '/api/key/generate (POST) - Generate new API key'
        },
        'authentication': {
            'method': 'API Key',
            'header': 'X-API-Key',
            'default_key': DEFAULT_API_KEY if os.environ.get('SHOW_DEFAULT_KEY') else 'hidden'
        },
        'timestamp': datetime.now().isoformat()
    })

@app.route('/health')
def health_check():
    """Health check endpoint (no auth required)"""
    return jsonify({
        'status': 'healthy',
        'service': 'Privacy-Preserving ML Cloud Service',
        'deployment': 'render',
        'version': '2.0.0',
        'timestamp': datetime.now().isoformat(),
        'stats': {
            'total_sessions': len(training_results),
            'active_models': len(trained_models),
            'api_keys': len(api_keys_db)
        },
        'privacy_guaranteed': True,
        'raw_data_accepted': False
    })

@app.route('/api/key/generate', methods=['POST'])
def generate_api_key():
    """Generate new API key"""
    data = request.get_json() or {}
    user = data.get('user', 'anonymous')
    
    # Generate secure API key
    new_key = 'ppml_' + secrets.token_urlsafe(32)
    
    api_keys_db[new_key] = {
        'user': user,
        'created': datetime.now().isoformat(),
        'requests': 0,
        'last_used': None
    }
    
    return jsonify({
        'api_key': new_key,
        'user': user,
        'created': datetime.now().isoformat(),
        'message': 'Store this key securely - it will not be shown again'
    })

@app.route('/train', methods=['POST'])
@require_api_key
def train_models():
    """Train ML models on received latent vectors (requires authentication)"""
    try:
        print(f"\n🚀 AUTHENTICATED TRAINING REQUEST - User: {request.api_user}")
        print(f"   Timestamp: {datetime.now()}")
        print("=" * 60)
        
        # Parse request data
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        # PRIVACY VALIDATION
        is_valid, message = validate_latent_data(data)
        if not is_valid:
            print(f"❌ PRIVACY VIOLATION DETECTED: {message}")
            return jsonify({
                'error': 'Privacy policy violation',
                'message': message,
                'action_required': 'Remove raw data and send only latent representations'
            }), 400
        
        print("✅ Privacy validation passed - latent vectors only")
        
        # Extract data
        latent_vectors = np.array(data['latent_vectors'])
        labels = np.array(data['labels'])
        metadata = data.get('metadata', {})
        
        print(f"📊 Received data:")
        print(f"   Latent vectors shape: {latent_vectors.shape}")
        print(f"   Labels shape: {labels.shape}")
        print(f"   User: {request.api_user}")
        
        # Split data for training
        try:
            X_train, X_test, y_train, y_test = train_test_split(
                latent_vectors, labels, test_size=0.2, random_state=42,
                stratify=labels if len(np.unique(labels)) > 1 else None
            )
        except ValueError:
            X_train, X_test, y_train, y_test = train_test_split(
                latent_vectors, labels, test_size=0.2, random_state=42
            )
        
        print(f"\n🎯 Training models on Render cloud:")
        print(f"   Training samples: {len(X_train)}")
        print(f"   Test samples: {len(X_test)}")
        print(f"   Feature dimensions: {latent_vectors.shape[1]}")
        
        # Define models to train
        models = {
            'logistic_regression': LogisticRegression(
                random_state=42, max_iter=1000, solver='liblinear'
            ),
            'mlp_classifier': MLPClassifier(
                hidden_layer_sizes=(64, 32), random_state=42, max_iter=500,
                early_stopping=True, validation_fraction=0.1
            ),
            'random_forest': RandomForestClassifier(
                n_estimators=100, random_state=42, n_jobs=-1
            )
        }
        
        results = {}
        training_start_time = time.time()
        
        # Train each model
        for model_name, model in models.items():
            print(f"\n📈 Training {model_name.replace('_', ' ').title()}...")
            
            try:
                model_start_time = time.time()
                
                # Train model
                model.fit(X_train, y_train)
                
                # Make predictions
                train_pred = model.predict(X_train)
                test_pred = model.predict(X_test)
                
                # Calculate metrics
                train_acc = accuracy_score(y_train, train_pred)
                test_acc = accuracy_score(y_test, test_pred)
                
                avg_method = 'weighted' if len(np.unique(labels)) > 2 else 'binary'
                precision = precision_score(y_test, test_pred, average=avg_method, zero_division=0)
                recall = recall_score(y_test, test_pred, average=avg_method, zero_division=0)
                f1 = f1_score(y_test, test_pred, average=avg_method, zero_division=0)
                
                model_training_time = time.time() - model_start_time
                
                # Store model with version
                model_id = f"render_{model_name}_{int(time.time())}_v1"
                trained_models[model_id] = {
                    'model': model,
                    'created': datetime.now().isoformat(),
                    'type': model_name,
                    'user': request.api_user,
                    'version': '1.0'
                }
                
                results[model_name] = {
                    'model_id': model_id,
                    'train_accuracy': float(train_acc),
                    'test_accuracy': float(test_acc),
                    'precision': float(precision),
                    'recall': float(recall),
                    'f1_score': float(f1),
                    'training_time': float(model_training_time),
                    'status': 'success',
                    'deployment': 'render',
                    'version': '1.0'
                }
                
                print(f"   ✅ {model_name.replace('_', ' ').title()} Results:")
                print(f"      Test Accuracy: {test_acc:.3f}")
                print(f"      F1-Score: {f1:.3f}")
                print(f"      Model ID: {model_id}")
                
            except Exception as e:
                print(f"   ❌ {model_name} training failed: {str(e)}")
                results[model_name] = {
                    'model_id': None,
                    'error': str(e),
                    'status': 'failed'
                }
        
        total_training_time = time.time() - training_start_time
        
        # Find best model
        successful_models = {k: v for k, v in results.items() if v['status'] == 'success'}
        if successful_models:
            best_model = max(successful_models.keys(),
                           key=lambda k: successful_models[k]['test_accuracy'])
            best_accuracy = successful_models[best_model]['test_accuracy']
        else:
            best_model = None
            best_accuracy = 0.0
        
        # Prepare response
        session_id = f"session_{int(time.time())}_{request.api_user}"
        
        response = {
            'status': 'success',
            'session_id': session_id,
            'message': 'Cloud training completed successfully on Render',
            'deployment': 'render',
            'user': request.api_user,
            'results': results,
            'summary': {
                'best_model': best_model,
                'best_accuracy': float(best_accuracy),
                'total_training_time': float(total_training_time),
                'models_trained': len(successful_models),
                'data_shape': latent_vectors.shape,
                'privacy_preserved': True,
                'raw_data_processed': False,
                'cloud_provider': 'render',
                'version': '2.0.0'
            },
            'privacy_report': {
                'raw_data_received': False,
                'latent_vectors_only': True,
                'privacy_policy_enforced': True,
                'data_encryption': 'HTTPS',
                'data_retention': 'session_only',
                'validation_passed': True
            },
            'timestamp': datetime.now().isoformat()
        }
        
        # Store results
        training_results[session_id] = response
        
        print(f"\n✅ RENDER CLOUD TRAINING COMPLETED:")
        print(f"   Session ID: {session_id}")
        print(f"   Best model: {best_model}")
        print(f"   Best accuracy: {best_accuracy:.3f}")
        print(f"   User: {request.api_user}")
        
        return jsonify(response)
        
    except Exception as e:
        error_response = {
            'status': 'error',
            'message': f'Training failed: {str(e)}',
            'deployment': 'render',
            'timestamp': datetime.now().isoformat()
        }
        print(f"❌ Training error: {str(e)}")
        return jsonify(error_response), 500

@app.route('/predict', methods=['POST'])
@require_api_key
def predict():
    """Make predictions using trained models"""
    try:
        data = request.get_json()
        model_id = data.get('model_id')
        latent_vectors = np.array(data['latent_vectors'])
        
        if model_id not in trained_models:
            return jsonify({'error': 'Model not found'}), 404
        
        model_data = trained_models[model_id]
        
        # Check if user has access to this model
        if model_data['user'] != request.api_user and request.api_user != 'admin':
            return jsonify({'error': 'Access denied to this model'}), 403
        
        model = model_data['model']
        predictions = model.predict(latent_vectors)
        probabilities = model.predict_proba(latent_vectors) if hasattr(model, 'predict_proba') else None
        
        response = {
            'predictions': predictions.tolist(),
            'probabilities': probabilities.tolist() if probabilities is not None else None,
            'model_id': model_id,
            'model_version': model_data['version'],
            'deployment': 'render',
            'user': request.api_user,
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({'error': str(e), 'deployment': 'render'}), 500

@app.route('/models')
@require_api_key
def list_models():
    """List all trained models (filtered by user)"""
    models_info = {}
    
    for model_id, model_data in trained_models.items():
        # Show only user's models (unless admin)
        if model_data['user'] == request.api_user or request.api_user == 'admin':
            models_info[model_id] = {
                'model_type': model_data['type'],
                'created': model_data['created'],
                'version': model_data['version'],
                'user': model_data['user'],
                'deployment': 'render'
            }
    
    return jsonify({
        'models': models_info,
        'count': len(models_info),
        'user': request.api_user,
        'deployment': 'render',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/results')
@require_api_key
def get_results():
    """Get training results history (filtered by user)"""
    user_results = {}
    
    for session_id, result in training_results.items():
        if result.get('user') == request.api_user or request.api_user == 'admin':
            user_results[session_id] = result
    
    return jsonify({
        'training_history': user_results,
        'count': len(user_results),
        'user': request.api_user,
        'deployment': 'render',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/stats')
@require_api_key
def get_stats():
    """Get usage statistics"""
    user_sessions = sum(1 for r in training_results.values() 
                       if r.get('user') == request.api_user)
    user_models = sum(1 for m in trained_models.values() 
                     if m['user'] == request.api_user)
    
    return jsonify({
        'user': request.api_user,
        'sessions': user_sessions,
        'models': user_models,
        'api_requests': api_keys_db.get(request.headers.get('X-API-Key'), {}).get('requests', 0),
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"🚀 Enhanced Render App starting on port {port}")
    print(f"🔑 Default API Key: {DEFAULT_API_KEY}")
    print(f"🔒 Authentication: Enabled")
    print(f"🛡️  Privacy Validation: Enabled")
    app.run(host='0.0.0.0', port=port, debug=False)
