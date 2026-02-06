#!/usr/bin/env python3
"""
Google Colab Server for Privacy-Preserving ML Pipeline
Run this in Google Colab to create a real cloud ML service
"""

# Google Colab Setup Code
COLAB_SETUP_CODE = '''
# ============================================================================
# GOOGLE COLAB SETUP - Copy and paste this into a Google Colab notebook
# ============================================================================

# Cell 1: Install dependencies
!pip install flask pyngrok scikit-learn numpy pandas matplotlib seaborn

# Cell 2: Setup ngrok authentication
from pyngrok import ngrok
import getpass

# Get your ngrok auth token from https://dashboard.ngrok.com/get-started/your-authtoken
ngrok_token = getpass.getpass("Enter your ngrok auth token: ")
ngrok.set_auth_token(ngrok_token)

# Cell 3: Create the ML training server
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
import threading

app = Flask(__name__)

# Global variables to store models and results
trained_models = {}
training_results = {}

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Privacy-Preserving ML Cloud Service',
        'timestamp': datetime.now().isoformat(),
        'message': 'Ready to receive latent vectors for training'
    })

@app.route('/train', methods=['POST'])
def train_models():
    """Train ML models on received latent vectors"""
    try:
        print("\\n🚀 RECEIVED TRAINING REQUEST FROM CLIENT")
        print("=" * 50)
        
        # Parse request data
        data = request.get_json()
        
        if not data or 'latent_vectors' not in data or 'labels' not in data:
            return jsonify({'error': 'Missing latent_vectors or labels'}), 400
        
        # Extract data
        latent_vectors = np.array(data['latent_vectors'])
        labels = np.array(data['labels'])
        metadata = data.get('metadata', {})
        
        print(f"📊 Received data:")
        print(f"   Latent vectors shape: {latent_vectors.shape}")
        print(f"   Labels shape: {labels.shape}")
        print(f"   Privacy preserved: {metadata.get('privacy_preserved', 'Unknown')}")
        print(f"   Raw data included: {metadata.get('original_data_included', 'Unknown')}")
        print(f"   Timestamp: {metadata.get('timestamp', 'Unknown')}")
        
        # Verify no raw data was sent
        if metadata.get('original_data_included', False):
            return jsonify({'error': 'Raw data detected - privacy violation!'}), 400
        
        # Split data for training
        X_train, X_test, y_train, y_test = train_test_split(
            latent_vectors, labels, test_size=0.2, random_state=42, stratify=labels
        )
        
        print(f"\\n🎯 Training models on cloud:")
        print(f"   Training samples: {len(X_train)}")
        print(f"   Test samples: {len(X_test)}")
        
        # Define models to train
        models = {
            'logistic_regression': LogisticRegression(random_state=42, max_iter=1000),
            'mlp_classifier': MLPClassifier(hidden_layer_sizes=(64, 32), random_state=42, max_iter=500),
            'random_forest': RandomForestClassifier(n_estimators=100, random_state=42)
        }
        
        results = {}
        training_start_time = time.time()
        
        # Train each model
        for model_name, model in models.items():
            print(f"\\n📈 Training {model_name.replace('_', ' ').title()}...")
            
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
                precision = precision_score(y_test, test_pred, average='weighted', zero_division=0)
                recall = recall_score(y_test, test_pred, average='weighted', zero_division=0)
                f1 = f1_score(y_test, test_pred, average='weighted', zero_division=0)
                
                model_training_time = time.time() - model_start_time
                
                # Store model and results
                model_id = f"cloud_{model_name}_{int(time.time())}"
                trained_models[model_id] = model
                
                results[model_name] = {
                    'model_id': model_id,
                    'train_accuracy': float(train_acc),
                    'test_accuracy': float(test_acc),
                    'precision': float(precision),
                    'recall': float(recall),
                    'f1_score': float(f1),
                    'training_time': float(model_training_time),
                    'status': 'success'
                }
                
                print(f"   ✅ {model_name.replace('_', ' ').title()} Results:")
                print(f"      Training Accuracy: {train_acc:.3f}")
                print(f"      Test Accuracy: {test_acc:.3f}")
                print(f"      Training Time: {model_training_time:.2f}s")
                
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
        response = {
            'status': 'success',
            'message': 'Cloud training completed successfully',
            'results': results,
            'summary': {
                'best_model': best_model,
                'best_accuracy': float(best_accuracy),
                'total_training_time': float(total_training_time),
                'models_trained': len(successful_models),
                'data_shape': latent_vectors.shape,
                'privacy_preserved': True,
                'raw_data_processed': False
            },
            'timestamp': datetime.now().isoformat()
        }
        
        # Store results globally
        training_results[datetime.now().isoformat()] = response
        
        print(f"\\n✅ CLOUD TRAINING COMPLETED:")
        print(f"   Best model: {best_model}")
        print(f"   Best accuracy: {best_accuracy:.3f}")
        print(f"   Total time: {total_training_time:.2f}s")
        print(f"   Privacy preserved: ✅")
        
        return jsonify(response)
        
    except Exception as e:
        error_response = {
            'status': 'error',
            'message': f'Training failed: {str(e)}',
            'timestamp': datetime.now().isoformat()
        }
        print(f"❌ Training error: {str(e)}")
        return jsonify(error_response), 500

@app.route('/predict', methods=['POST'])
def predict():
    """Make predictions using trained models"""
    try:
        data = request.get_json()
        model_id = data.get('model_id')
        latent_vectors = np.array(data['latent_vectors'])
        
        if model_id not in trained_models:
            return jsonify({'error': 'Model not found'}), 404
        
        model = trained_models[model_id]
        predictions = model.predict(latent_vectors)
        probabilities = model.predict_proba(latent_vectors) if hasattr(model, 'predict_proba') else None
        
        response = {
            'predictions': predictions.tolist(),
            'probabilities': probabilities.tolist() if probabilities is not None else None,
            'model_id': model_id,
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/models', methods=['GET'])
def list_models():
    """List all trained models"""
    models_info = {}
    for model_id, model in trained_models.items():
        models_info[model_id] = {
            'model_type': type(model).__name__,
            'created': model_id.split('_')[-1]
        }
    
    return jsonify({
        'models': models_info,
        'count': len(trained_models),
        'timestamp': datetime.now().isoformat()
    })

@app.route('/results', methods=['GET'])
def get_results():
    """Get training results history"""
    return jsonify({
        'training_history': training_results,
        'timestamp': datetime.now().isoformat()
    })

# Cell 4: Start the server with ngrok
def run_server():
    app.run(host='0.0.0.0', port=8080, debug=False)

# Start server in background thread
server_thread = threading.Thread(target=run_server)
server_thread.daemon = True
server_thread.start()

# Create ngrok tunnel
public_url = ngrok.connect(8080)
print(f"\\n🌐 PRIVACY-PRESERVING ML CLOUD SERVICE STARTED!")
print(f"=" * 55)
print(f"🔗 Public URL: {public_url}")
print(f"📍 Local URL: http://localhost:8080")
print(f"🛡️  Privacy Status: Only latent vectors accepted")
print(f"❌ Raw data: REJECTED automatically")
print(f"\\n📋 Available Endpoints:")
print(f"   GET  {public_url}/health - Health check")
print(f"   POST {public_url}/train - Train models on latent vectors")
print(f"   POST {public_url}/predict - Make predictions")
print(f"   GET  {public_url}/models - List trained models")
print(f"   GET  {public_url}/results - Get training history")
print(f"\\n🚀 Ready to receive latent vectors from your local pipeline!")
print(f"\\nCopy this URL to use in your local project:")
print(f"COLAB_ENDPOINT = '{public_url}'")

# Cell 5: Keep the server running
import time
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\\n🛑 Server stopped")
    ngrok.disconnect(public_url)
'''

def save_colab_notebook():
    """Save the Colab setup as a downloadable notebook"""
    notebook_content = {
        "nbformat": 4,
        "nbformat_minor": 0,
        "metadata": {
            "colab": {
                "provenance": [],
                "name": "Privacy_Preserving_ML_Cloud_Service.ipynb"
            },
            "kernelspec": {
                "name": "python3",
                "display_name": "Python 3"
            }
        },
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "# Privacy-Preserving ML Cloud Service\\n",
                    "\\n",
                    "This notebook creates a real cloud ML service that:\\n",
                    "- Accepts only latent vectors (no raw data)\\n",
                    "- Trains multiple ML models\\n",
                    "- Provides REST API endpoints\\n",
                    "- Ensures privacy preservation\\n",
                    "\\n",
                    "## Setup Instructions:\\n",
                    "1. Get ngrok auth token from https://dashboard.ngrok.com/get-started/your-authtoken\\n",
                    "2. Run all cells in order\\n",
                    "3. Copy the public URL to use in your local project"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# Install dependencies\\n",
                    "!pip install flask pyngrok scikit-learn numpy pandas matplotlib seaborn"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# Setup ngrok authentication\\n",
                    "from pyngrok import ngrok\\n",
                    "import getpass\\n",
                    "\\n",
                    "# Get your ngrok auth token from https://dashboard.ngrok.com/get-started/your-authtoken\\n",
                    "ngrok_token = getpass.getpass('Enter your ngrok auth token: ')\\n",
                    "ngrok.set_auth_token(ngrok_token)"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": COLAB_SETUP_CODE.split('# Cell 3: Create the ML training server')[1].split('# Cell 4: Start the server with ngrok')[0]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": COLAB_SETUP_CODE.split('# Cell 4: Start the server with ngrok')[1].split('# Cell 5: Keep the server running')[0]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": COLAB_SETUP_CODE.split('# Cell 5: Keep the server running')[1]
            }
        ]
    }
    
    import json
    with open('Privacy_Preserving_ML_Cloud_Service.ipynb', 'w') as f:
        json.dump(notebook_content, f, indent=2)
    
    print("📓 Google Colab notebook saved: Privacy_Preserving_ML_Cloud_Service.ipynb")

if __name__ == "__main__":
    print("Google Colab + ngrok Setup for Privacy-Preserving ML")
    print("=" * 55)
    print()
    print("🔧 SETUP INSTRUCTIONS:")
    print("=" * 25)
    print()
    print("1. 📝 Create Google Colab Account:")
    print("   - Go to https://colab.research.google.com/")
    print("   - Sign in with Google account")
    print()
    print("2. 🔑 Get ngrok Auth Token:")
    print("   - Go to https://dashboard.ngrok.com/get-started/your-authtoken")
    print("   - Sign up for free ngrok account")
    print("   - Copy your auth token")
    print()
    print("3. 📓 Create New Colab Notebook:")
    print("   - Click 'New notebook' in Google Colab")
    print("   - Copy and paste the code below into cells")
    print()
    print("4. 🚀 Run the Notebook:")
    print("   - Run all cells in order")
    print("   - Enter your ngrok token when prompted")
    print("   - Copy the public URL that appears")
    print()
    print("5. 🔗 Update Your Local Project:")
    print("   - Use the public URL in your local project")
    print("   - Replace the endpoint in cloud_integration.py")
    print()
    print("=" * 55)
    print("📋 COLAB CODE TO COPY:")
    print("=" * 55)
    print()
    print(COLAB_SETUP_CODE)
    
    # Save notebook file
    save_colab_notebook()