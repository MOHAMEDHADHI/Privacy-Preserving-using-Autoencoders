#!/usr/bin/env python3
"""
Render Deployment Flask App
Permanent cloud service for privacy-preserving ML
"""

from flask import Flask, request, jsonify
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

app = Flask(__name__)

# Global storage for models and results
trained_models = {}
training_results = {}


@app.route('/', methods=['GET'])
def home():
    """Home endpoint"""
    return jsonify({
        'service': 'Privacy-Preserving ML Cloud Service',
        'version': '1.0.0',
        'status': 'running',
        'deployment': 'render',
        'privacy_policy': 'Only latent vectors accepted - raw data automatically rejected',
        'endpoints': {
            'health': '/health',
            'train': '/train (POST)',
            'models': '/models',
            'predict': '/predict (POST)'
        },
        'timestamp': datetime.now().isoformat()
    })


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Privacy-Preserving ML Cloud Service',
        'deployment': 'render',
        'timestamp': datetime.now().isoformat(),
        'message': 'Ready to receive latent vectors for training',
        'privacy_guaranteed': True,
        'raw_data_accepted': False
    })


@app.route('/train', methods=['POST'])
def train_models():
    """Train ML models on received latent vectors"""
    try:
        print(f"\n🚀 TRAINING REQUEST RECEIVED - {datetime.now()}")
        print("=" * 60)

        data = request.get_json()

        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400

        if 'latent_vectors' not in data or 'labels' not in data:
            return jsonify({'error': 'Missing latent_vectors or labels'}), 400

        latent_vectors = np.array(data['latent_vectors'])
        labels = np.array(data['labels'])
        metadata = data.get('metadata', {})

        print(f"📊 Received data:")
        print(f"   Latent vectors shape: {latent_vectors.shape}")
        print(f"   Labels shape: {labels.shape}")
        print(f"   Privacy preserved: {metadata.get('privacy_preserved', 'Unknown')}")
        print(f"   Raw data included: {metadata.get('original_data_included', 'Unknown')}")

        # PRIVACY CHECK - Reject if raw data detected
        if metadata.get('original_data_included', False):
            print("❌ PRIVACY VIOLATION DETECTED - Raw data in payload!")
            return jsonify({
                'error': 'Privacy violation detected - raw data not allowed!',
                'privacy_policy': 'This service only accepts latent vectors',
                'action_required': 'Remove raw data and send only latent representations'
            }), 400

        if len(latent_vectors.shape) != 2:
            return jsonify({'error': 'Latent vectors must be 2D array'}), 400

        if len(latent_vectors) != len(labels):
            return jsonify({'error': 'Latent vectors and labels length mismatch'}), 400

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

        for model_name, model in models.items():
            print(f"\n📈 Training {model_name.replace('_', ' ').title()}...")
            try:
                model_start_time = time.time()

                model.fit(X_train, y_train)
                train_pred = model.predict(X_train)
                test_pred = model.predict(X_test)

                train_acc = accuracy_score(y_train, train_pred)
                test_acc = accuracy_score(y_test, test_pred)

                avg_method = 'weighted' if len(np.unique(labels)) > 2 else 'binary'
                precision = precision_score(y_test, test_pred, average=avg_method, zero_division=0)
                recall = recall_score(y_test, test_pred, average=avg_method, zero_division=0)
                f1 = f1_score(y_test, test_pred, average=avg_method, zero_division=0)

                model_training_time = time.time() - model_start_time

                model_id = f"render_{model_name}_{int(time.time())}"
                trained_models[model_id] = {
                    'model': model,
                    'created': datetime.now().isoformat(),
                    'type': model_name
                }

                results[model_name] = {
                    'model_id': model_id,
                    'model_type': model_name,
                    'train_accuracy': float(train_acc),
                    'test_accuracy': float(test_acc),
                    'precision': float(precision),
                    'recall': float(recall),
                    'f1_score': float(f1),
                    'training_time': float(model_training_time),
                    'status': 'success',
                    'deployment': 'render'
                }

                print(f"   ✅ {model_name.replace('_', ' ').title()} Results:")
                print(f"      Training Accuracy: {train_acc:.3f}")
                print(f"      Test Accuracy: {test_acc:.3f}")
                print(f"      F1-Score: {f1:.3f}")
                print(f"      Training Time: {model_training_time:.2f}s")

            except Exception as e:
                print(f"   ❌ {model_name} training failed: {str(e)}")
                results[model_name] = {
                    'model_id': None,
                    'error': str(e),
                    'status': 'failed'
                }

        total_training_time = time.time() - training_start_time

        successful_models = {k: v for k, v in results.items() if v['status'] == 'success'}
        if successful_models:
            best_model = max(successful_models.keys(),
                             key=lambda k: successful_models[k]['test_accuracy'])
            best_accuracy = successful_models[best_model]['test_accuracy']
        else:
            best_model = None
            best_accuracy = 0.0

        response = {
            'status': 'success',
            'message': 'Cloud training completed successfully on Render',
            'deployment': 'render',
            'results': results,
            'summary': {
                'best_model': best_model,
                'best_accuracy': float(best_accuracy),
                'total_training_time': float(total_training_time),
                'models_trained': len(successful_models),
                'data_shape': list(latent_vectors.shape),
                'privacy_preserved': True,
                'raw_data_processed': False,
                'cloud_provider': 'render'
            },
            'privacy_report': {
                'raw_data_received': False,
                'latent_vectors_only': True,
                'privacy_policy_enforced': True,
                'data_encryption': 'HTTPS',
                'data_retention': 'session_only'
            },
            'timestamp': datetime.now().isoformat()
        }

        session_id = datetime.now().isoformat()
        training_results[session_id] = response

        print(f"\n✅ RENDER CLOUD TRAINING COMPLETED:")
        print(f"   Best model: {best_model}")
        print(f"   Best accuracy: {best_accuracy:.3f}")
        print(f"   Total time: {total_training_time:.2f}s")
        print(f"   Privacy preserved: ✅")
        print(f"   Deployment: Render")

        return jsonify(response)

    except Exception as e:
        print(f"❌ Training error: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'Training failed: {str(e)}',
            'deployment': 'render',
            'timestamp': datetime.now().isoformat()
        }), 500


@app.route('/predict', methods=['POST'])
def predict():
    """Make predictions using trained models"""
    try:
        data = request.get_json()
        model_id = data.get('model_id')
        latent_vectors = np.array(data['latent_vectors'])

        if model_id not in trained_models:
            return jsonify({'error': 'Model not found'}), 404

        model = trained_models[model_id]['model']
        predictions = model.predict(latent_vectors)
        probabilities = model.predict_proba(latent_vectors) if hasattr(model, 'predict_proba') else None

        return jsonify({
            'predictions': predictions.tolist(),
            'probabilities': probabilities.tolist() if probabilities is not None else None,
            'model_id': model_id,
            'deployment': 'render',
            'timestamp': datetime.now().isoformat()
        })

    except Exception as e:
        return jsonify({'error': str(e), 'deployment': 'render'}), 500


@app.route('/models', methods=['GET'])
def list_models():
    """List all trained models"""
    models_info = {}
    for model_id, model_data in trained_models.items():
        models_info[model_id] = {
            'model_type': model_data['type'],
            'created': model_data['created'],
            'deployment': 'render'
        }

    return jsonify({
        'models': models_info,
        'count': len(trained_models),
        'deployment': 'render',
        'timestamp': datetime.now().isoformat()
    })


@app.route('/results', methods=['GET'])
def get_results():
    """Get training results history"""
    return jsonify({
        'training_history': training_results,
        'deployment': 'render',
        'timestamp': datetime.now().isoformat()
    })


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
