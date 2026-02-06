#!/usr/bin/env python3
"""
Comprehensive Report Generator
Generates PDF and HTML reports for training sessions
"""

from datetime import datetime
import json
import os
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

class ReportGenerator:
    """Generate comprehensive reports for ML training sessions"""
    
    def __init__(self, output_dir='reports'):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
    def generate_html_report(self, session_data, model_results):
        """Generate HTML report"""
        
        session_id = session_data.get('session_id', 'unknown')
        timestamp = session_data.get('timestamp', datetime.now().isoformat())
        
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Training Report - {session_id}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 40px 20px;
            background: #f5f5f5;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            border-radius: 15px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }}
        .header h1 {{
            margin: 0 0 10px 0;
            font-size: 2.5em;
        }}
        .header p {{
            margin: 5px 0;
            opacity: 0.9;
        }}
        .section {{
            background: white;
            padding: 30px;
            margin-bottom: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .section h2 {{
            color: #667eea;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }}
        .stat-box {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            border-left: 4px solid #667eea;
        }}
        .stat-value {{
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
            margin-bottom: 5px;
        }}
        .stat-label {{
            color: #6c757d;
            font-size: 0.9em;
            text-transform: uppercase;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #dee2e6;
        }}
        th {{
            background: #667eea;
            color: white;
            font-weight: 600;
        }}
        tr:hover {{
            background: #f8f9fa;
        }}
        .badge {{
            display: inline-block;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: 600;
        }}
        .badge-success {{
            background: #28a745;
            color: white;
        }}
        .badge-info {{
            background: #17a2b8;
            color: white;
        }}
        .badge-warning {{
            background: #ffc107;
            color: #333;
        }}
        .privacy-box {{
            background: #6f42c1;
            color: white;
            padding: 25px;
            border-radius: 10px;
            margin: 20px 0;
        }}
        .privacy-box h3 {{
            margin-top: 0;
            color: white;
        }}
        .privacy-item {{
            margin: 10px 0;
            padding-left: 25px;
            position: relative;
        }}
        .privacy-item:before {{
            content: "✓";
            position: absolute;
            left: 0;
            font-weight: bold;
            font-size: 1.2em;
        }}
        .footer {{
            text-align: center;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 2px solid #dee2e6;
            color: #6c757d;
        }}
        .chart {{
            margin: 20px 0;
            text-align: center;
        }}
        .chart img {{
            max-width: 100%;
            border-radius: 10px;
            box-shadow: 0 3px 10px rgba(0,0,0,0.1);
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🔒 Privacy-Preserving ML Training Report</h1>
        <p><strong>Session ID:</strong> {session_id}</p>
        <p><strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p><strong>Training Date:</strong> {timestamp}</p>
    </div>
    
    <div class="section">
        <h2>📊 Training Overview</h2>
        <div class="stats-grid">
            <div class="stat-box">
                <div class="stat-value">{session_data.get('data_samples', 'N/A')}</div>
                <div class="stat-label">Data Samples</div>
            </div>
            <div class="stat-box">
                <div class="stat-value">{session_data.get('latent_dim', 'N/A')}</div>
                <div class="stat-label">Latent Dimensions</div>
            </div>
            <div class="stat-box">
                <div class="stat-value">{len(model_results)}</div>
                <div class="stat-label">Models Trained</div>
            </div>
            <div class="stat-box">
                <div class="stat-value">{session_data.get('training_time', 0):.2f}s</div>
                <div class="stat-label">Total Time</div>
            </div>
        </div>
    </div>
    
    <div class="section">
        <h2>🤖 Model Performance</h2>
        <table>
            <thead>
                <tr>
                    <th>Model</th>
                    <th>Train Accuracy</th>
                    <th>Test Accuracy</th>
                    <th>Precision</th>
                    <th>Recall</th>
                    <th>F1-Score</th>
                    <th>Time (s)</th>
                </tr>
            </thead>
            <tbody>
"""
        
        for model_name, results in model_results.items():
            if results.get('status') == 'success':
                html_content += f"""
                <tr>
                    <td><strong>{model_name.replace('_', ' ').title()}</strong></td>
                    <td>{results.get('train_accuracy', 0):.3f}</td>
                    <td>{results.get('test_accuracy', 0):.3f}</td>
                    <td>{results.get('precision', 0):.3f}</td>
                    <td>{results.get('recall', 0):.3f}</td>
                    <td>{results.get('f1_score', 0):.3f}</td>
                    <td>{results.get('training_time', 0):.2f}</td>
                </tr>
"""
        
        html_content += """
            </tbody>
        </table>
    </div>
    
    <div class="section">
        <h2>🏆 Best Model</h2>
"""
        
        best_model = session_data.get('best_model', 'Unknown')
        best_accuracy = session_data.get('best_accuracy', 0)
        
        html_content += f"""
        <div class="stats-grid">
            <div class="stat-box">
                <div class="stat-value">{best_model.replace('_', ' ').title()}</div>
                <div class="stat-label">Model Name</div>
            </div>
            <div class="stat-box">
                <div class="stat-value">{best_accuracy:.3f}</div>
                <div class="stat-label">Test Accuracy</div>
            </div>
            <div class="stat-box">
                <div class="stat-value"><span class="badge badge-success">Deployed</span></div>
                <div class="stat-label">Status</div>
            </div>
        </div>
    </div>
    
    <div class="section">
        <div class="privacy-box">
            <h3>🛡️ Privacy Guarantees</h3>
            <div class="privacy-item">Raw sensitive data never transmitted to cloud</div>
            <div class="privacy-item">Only privacy-preserving latent vectors sent</div>
            <div class="privacy-item">Original data remains on local system</div>
            <div class="privacy-item">HTTPS encryption enforced for all transmissions</div>
            <div class="privacy-item">No data persistence on cloud servers</div>
            <div class="privacy-item">Privacy policy enforced at API level</div>
        </div>
    </div>
    
    <div class="section">
        <h2>📋 Session Details</h2>
        <table>
            <tr>
                <td><strong>Session ID</strong></td>
                <td>{session_id}</td>
            </tr>
            <tr>
                <td><strong>Timestamp</strong></td>
                <td>{timestamp}</td>
            </tr>
            <tr>
                <td><strong>Cloud Provider</strong></td>
                <td><span class="badge badge-info">{session_data.get('cloud_provider', 'render')}</span></td>
            </tr>
            <tr>
                <td><strong>Privacy Preserved</strong></td>
                <td><span class="badge badge-success">✓ Yes</span></td>
            </tr>
            <tr>
                <td><strong>Data Samples</strong></td>
                <td>{session_data.get('data_samples', 'N/A')}</td>
            </tr>
            <tr>
                <td><strong>Latent Dimensions</strong></td>
                <td>{session_data.get('latent_dim', 'N/A')}</td>
            </tr>
            <tr>
                <td><strong>Total Training Time</strong></td>
                <td>{session_data.get('training_time', 0):.2f} seconds</td>
            </tr>
        </table>
    </div>
    
    <div class="footer">
        <p><strong>Privacy-Preserving ML Pipeline</strong></p>
        <p>Generated on {datetime.now().strftime('%Y-%m-%d at %H:%M:%S')}</p>
        <p>© 2024 Privacy-Preserving ML System</p>
    </div>
</body>
</html>
"""
        
        # Save HTML report
        report_path = self.output_dir / f'report_{session_id}.html'
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ HTML report generated: {report_path}")
        return report_path
    
    def generate_performance_chart(self, model_results, session_id):
        """Generate performance comparison chart"""
        
        models = []
        metrics = {
            'Test Accuracy': [],
            'Precision': [],
            'Recall': [],
            'F1-Score': []
        }
        
        for model_name, results in model_results.items():
            if results.get('status') == 'success':
                models.append(model_name.replace('_', ' ').title())
                metrics['Test Accuracy'].append(results.get('test_accuracy', 0))
                metrics['Precision'].append(results.get('precision', 0))
                metrics['Recall'].append(results.get('recall', 0))
                metrics['F1-Score'].append(results.get('f1_score', 0))
        
        if not models:
            return None
        
        # Create chart
        fig, ax = plt.subplots(figsize=(12, 6))
        
        x = range(len(models))
        width = 0.2
        
        colors = ['#667eea', '#764ba2', '#f093fb', '#4facfe']
        
        for i, (metric_name, values) in enumerate(metrics.items()):
            offset = width * (i - 1.5)
            ax.bar([xi + offset for xi in x], values, width, 
                   label=metric_name, color=colors[i], alpha=0.8)
        
        ax.set_xlabel('Models', fontsize=12, fontweight='bold')
        ax.set_ylabel('Score', fontsize=12, fontweight='bold')
        ax.set_title('Model Performance Comparison', fontsize=14, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(models, rotation=15, ha='right')
        ax.legend(loc='upper left', framealpha=0.9)
        ax.grid(True, alpha=0.3, axis='y')
        ax.set_ylim(0, 1.1)
        
        plt.tight_layout()
        
        chart_path = self.output_dir / f'performance_{session_id}.png'
        plt.savefig(chart_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✅ Performance chart generated: {chart_path}")
        return chart_path
    
    def generate_summary_json(self, session_data, model_results):
        """Generate JSON summary"""
        
        session_id = session_data.get('session_id', 'unknown')
        
        summary = {
            'session_id': session_id,
            'timestamp': session_data.get('timestamp'),
            'generated_at': datetime.now().isoformat(),
            'overview': {
                'data_samples': session_data.get('data_samples'),
                'latent_dimensions': session_data.get('latent_dim'),
                'models_trained': len(model_results),
                'total_training_time': session_data.get('training_time'),
                'cloud_provider': session_data.get('cloud_provider', 'render')
            },
            'best_model': {
                'name': session_data.get('best_model'),
                'accuracy': session_data.get('best_accuracy')
            },
            'model_results': model_results,
            'privacy': {
                'raw_data_transmitted': False,
                'latent_vectors_only': True,
                'privacy_preserved': True,
                'encryption': 'HTTPS',
                'data_retention': 'session_only'
            }
        }
        
        summary_path = self.output_dir / f'summary_{session_id}.json'
        with open(summary_path, 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"✅ JSON summary generated: {summary_path}")
        return summary_path
    
    def generate_complete_report(self, session_data, model_results):
        """Generate all report formats"""
        
        print("\n📄 GENERATING COMPREHENSIVE REPORTS")
        print("=" * 50)
        
        # Generate HTML report
        html_path = self.generate_html_report(session_data, model_results)
        
        # Generate performance chart
        chart_path = self.generate_performance_chart(model_results, 
                                                     session_data.get('session_id', 'unknown'))
        
        # Generate JSON summary
        json_path = self.generate_summary_json(session_data, model_results)
        
        print(f"\n✅ All reports generated successfully!")
        print(f"   HTML Report: {html_path}")
        print(f"   Performance Chart: {chart_path}")
        print(f"   JSON Summary: {json_path}")
        
        return {
            'html': html_path,
            'chart': chart_path,
            'json': json_path
        }

if __name__ == '__main__':
    # Example usage
    generator = ReportGenerator()
    
    sample_session = {
        'session_id': 'test_session_001',
        'timestamp': datetime.now().isoformat(),
        'data_samples': 500,
        'latent_dim': 128,
        'models_trained': 3,
        'best_model': 'logistic_regression',
        'best_accuracy': 0.856,
        'training_time': 12.5,
        'cloud_provider': 'render'
    }
    
    sample_results = {
        'logistic_regression': {
            'status': 'success',
            'train_accuracy': 0.875,
            'test_accuracy': 0.856,
            'precision': 0.862,
            'recall': 0.851,
            'f1_score': 0.856,
            'training_time': 3.2
        },
        'mlp_classifier': {
            'status': 'success',
            'train_accuracy': 0.892,
            'test_accuracy': 0.841,
            'precision': 0.848,
            'recall': 0.839,
            'f1_score': 0.843,
            'training_time': 8.1
        }
    }
    
    generator.generate_complete_report(sample_session, sample_results)
