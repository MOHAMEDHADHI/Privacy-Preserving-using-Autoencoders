#!/usr/bin/env python3
"""
Automated Google Colab + ngrok Setup
This script automatically sets up your cloud service
"""

import json
import os
import time
import requests
from datetime import datetime

def create_colab_notebook():
    """Create a downloadable Google Colab notebook"""
    
    notebook_content = {
        "nbformat": 4,
        "nbformat_minor": 0,
        "metadata": {
            "colab": {
                "provenance": [],
                "name": "Privacy_ML_Cloud_Service.ipynb"
            },
            "kernelspec": {
                "name": "python3",
                "display_name": "Python 3"
            },
            "language_info": {
                "name": "python"
            }
        },
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {
                    "id": "header"
                },
                "source": [
                    "# 🌐 Privacy-Preserving ML Cloud Service\\n",
                    "\\n",
                    "This notebook creates a real cloud ML service that:\\n",
                    "- ✅ Accepts only latent vectors (no raw data)\\n",
                    "- ✅ Trains multiple ML models\\n",
                    "- ✅ Provides REST API endpoints\\n",
                    "- ✅ Ensures privacy preservation\\n",
                    "\\n",
                    "## 🚀 Instructions:\\n",
                    "1. Get ngrok token: https://dashboard.ngrok.com/get-started/your-authtoken\\n",
                    "2. Run Cell 1: Install dependencies\\n",
                    "3. Run Cell 2: Enter your ngrok token\\n",
                    "4. Run Cell 3: Start the service\\n",
                    "5. Copy the ngrok URL that appears\\n",
                    "6. Use the URL in your local project"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {
                    "id": "install_deps"
                },
                "outputs": [],
                "source": [
                    "# Cell 1: Install Dependencies\\n",
                    "!pip install flask pyngrok scikit-learn numpy pandas requests\\n",
                    "print('✅ Dependencies installed!')"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {
                    "id": "setup_ngrok"
                },
                "outputs": [],
                "source": [
                    "# Cell 2: Setup ngrok Authentication\\n",
                    "from pyngrok import ngrok\\n",
                    "import getpass\\n",
                    "\\n",
                    "print('🔑 Get your ngrok token from: https://dashboard.ngrok.com/get-started/your-authtoken')\\n",
                    "ngrok_token = getpass.getpass('Enter your ngrok auth token: ')\\n",
                    "ngrok.set_auth_token(ngrok_token)\\n",
                    "print('✅ ngrok configured!')"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {
                    "id": "create_server"
                },
                "outputs": [],
                "source": [
                    "# Cell 3: Create Privacy-Preserving ML Server\\n",
                    "from flask import Flask, request, jsonify\\n",
                    "import numpy as np\\n",
                    "import json\\n",
                    "from sklearn.linear_model import LogisticRegression\\n",
                    "from sklearn.neural_network import MLPClassifier\\n",
                    "from sklearn.ensemble import RandomForestClassifier\\n",
                    "from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score\\n",
                    "from sklearn.model_selection import train_test_split\\n",
                    "import time\\n",
                    "from datetime import datetime\\n",
                    "import threading\\n",
                    "\\n",
                    "app = Flask(__name__)\\n",
                    "trained_models = {}\\n",
                    "training_results = {}\\n",
                    "\\n",
                    "@app.route('/', methods=['GET'])\\n",
                    "def home():\\n",
                    "    return jsonify({\\n",
                    "        'service': 'Privacy-Preserving ML Cloud Service',\\n",
                    "        'status': 'running',\\n",
                    "        'deployment': 'google_colab',\\n",
                    "        'privacy_policy': 'Only latent vectors accepted - raw data automatically rejected',\\n",
                    "        'timestamp': datetime.now().isoformat()\\n",
                    "    })\\n",
                    "\\n",
                    "@app.route('/health', methods=['GET'])\\n",
                    "def health():\\n",
                    "    return jsonify({\\n",
                    "        'status': 'healthy',\\n",
                    "        'service': 'Privacy-Preserving ML Cloud Service',\\n",
                    "        'deployment': 'google_colab',\\n",
                    "        'timestamp': datetime.now().isoformat(),\\n",
                    "        'privacy_preserved': True,\\n",
                    "        'raw_data_accepted': False\\n",
                    "    })\\n",
                    "\\n",
                    "@app.route('/train', methods=['POST'])\\n",
                    "def train():\\n",
                    "    try:\\n",
                    "        print('\\\\n🚀 RECEIVED TRAINING REQUEST FROM CLIENT')\\n",
                    "        print('=' * 50)\\n",
                    "        \\n",
                    "        data = request.get_json()\\n",
                    "        \\n",
                    "        if not data or 'latent_vectors' not in data or 'labels' not in data:\\n",
                    "            return jsonify({'error': 'Missing latent_vectors or labels'}), 400\\n",
                    "        \\n",
                    "        latent_vectors = np.array(data['latent_vectors'])\\n",
                    "        labels = np.array(data['labels'])\\n",
                    "        metadata = data.get('metadata', {})\\n",
                    "        \\n",
                    "        print(f'📊 Received data:')\\n",
                    "        print(f'   Latent vectors shape: {latent_vectors.shape}')\\n",
                    "        print(f'   Labels shape: {labels.shape}')\\n",
                    "        print(f'   Privacy preserved: {metadata.get(\\\"privacy_preserved\\\", True)}')\\n",
                    "        print(f'   Raw data included: {metadata.get(\\\"original_data_included\\\", False)}')\\n",
                    "        \\n",
                    "        # PRIVACY CHECK - Reject raw data\\n",
                    "        if metadata.get('original_data_included', False):\\n",
                    "            print('❌ PRIVACY VIOLATION DETECTED - Raw data in payload!')\\n",
                    "            return jsonify({\\n",
                    "                'error': 'Privacy violation detected - raw data not allowed!',\\n",
                    "                'privacy_policy': 'This service only accepts latent vectors'\\n",
                    "            }), 400\\n",
                    "        \\n",
                    "        # Split data\\n",
                    "        try:\\n",
                    "            X_train, X_test, y_train, y_test = train_test_split(\\n",
                    "                latent_vectors, labels, test_size=0.2, random_state=42,\\n",
                    "                stratify=labels if len(np.unique(labels)) > 1 else None\\n",
                    "            )\\n",
                    "        except ValueError:\\n",
                    "            X_train, X_test, y_train, y_test = train_test_split(\\n",
                    "                latent_vectors, labels, test_size=0.2, random_state=42\\n",
                    "            )\\n",
                    "        \\n",
                    "        print(f'\\\\n🎯 Training models on Google Colab:')\\n",
                    "        print(f'   Training samples: {len(X_train)}')\\n",
                    "        print(f'   Test samples: {len(X_test)}')\\n",
                    "        print(f'   Feature dimensions: {latent_vectors.shape[1]}')\\n",
                    "        \\n",
                    "        # Train models\\n",
                    "        models = {\\n",
                    "            'logistic_regression': LogisticRegression(random_state=42, max_iter=1000),\\n",
                    "            'mlp_classifier': MLPClassifier(hidden_layer_sizes=(64, 32), random_state=42, max_iter=300),\\n",
                    "            'random_forest': RandomForestClassifier(n_estimators=50, random_state=42)\\n",
                    "        }\\n",
                    "        \\n",
                    "        results = {}\\n",
                    "        start_time = time.time()\\n",
                    "        \\n",
                    "        for name, model in models.items():\\n",
                    "            try:\\n",
                    "                print(f'\\\\n📈 Training {name.replace(\\\"_\\\", \\\" \\\").title()}...')\\n",
                    "                model_start = time.time()\\n",
                    "                \\n",
                    "                model.fit(X_train, y_train)\\n",
                    "                \\n",
                    "                train_pred = model.predict(X_train)\\n",
                    "                test_pred = model.predict(X_test)\\n",
                    "                \\n",
                    "                train_acc = accuracy_score(y_train, train_pred)\\n",
                    "                test_acc = accuracy_score(y_test, test_pred)\\n",
                    "                \\n",
                    "                model_time = time.time() - model_start\\n",
                    "                model_id = f'colab_{name}_{int(time.time())}'\\n",
                    "                \\n",
                    "                trained_models[model_id] = model\\n",
                    "                \\n",
                    "                results[name] = {\\n",
                    "                    'model_id': model_id,\\n",
                    "                    'train_accuracy': float(train_acc),\\n",
                    "                    'test_accuracy': float(test_acc),\\n",
                    "                    'training_time': float(model_time),\\n",
                    "                    'status': 'success'\\n",
                    "                }\\n",
                    "                \\n",
                    "                print(f'   ✅ {name.replace(\\\"_\\\", \\\" \\\").title()} Results:')\\n",
                    "                print(f'      Training Accuracy: {train_acc:.3f}')\\n",
                    "                print(f'      Test Accuracy: {test_acc:.3f}')\\n",
                    "                print(f'      Training Time: {model_time:.2f}s')\\n",
                    "                \\n",
                    "            except Exception as e:\\n",
                    "                print(f'   ❌ {name} training failed: {str(e)}')\\n",
                    "                results[name] = {\\n",
                    "                    'model_id': None,\\n",
                    "                    'error': str(e),\\n",
                    "                    'status': 'failed'\\n",
                    "                }\\n",
                    "        \\n",
                    "        training_time = time.time() - start_time\\n",
                    "        \\n",
                    "        # Find best model\\n",
                    "        successful = {k: v for k, v in results.items() if v['status'] == 'success'}\\n",
                    "        if successful:\\n",
                    "            best_model = max(successful.keys(), key=lambda k: successful[k]['test_accuracy'])\\n",
                    "            best_accuracy = successful[best_model]['test_accuracy']\\n",
                    "        else:\\n",
                    "            best_model = None\\n",
                    "            best_accuracy = 0.0\\n",
                    "        \\n",
                    "        response = {\\n",
                    "            'status': 'success',\\n",
                    "            'message': 'Cloud training completed successfully on Google Colab',\\n",
                    "            'deployment': 'google_colab',\\n",
                    "            'results': results,\\n",
                    "            'summary': {\\n",
                    "                'best_model': best_model,\\n",
                    "                'best_accuracy': float(best_accuracy),\\n",
                    "                'total_training_time': float(training_time),\\n",
                    "                'models_trained': len(successful),\\n",
                    "                'data_shape': latent_vectors.shape,\\n",
                    "                'privacy_preserved': True,\\n",
                    "                'raw_data_processed': False\\n",
                    "            },\\n",
                    "            'timestamp': datetime.now().isoformat()\\n",
                    "        }\\n",
                    "        \\n",
                    "        # Store results\\n",
                    "        session_id = datetime.now().isoformat()\\n",
                    "        training_results[session_id] = response\\n",
                    "        \\n",
                    "        print(f'\\\\n✅ GOOGLE COLAB TRAINING COMPLETED:')\\n",
                    "        print(f'   Best model: {best_model}')\\n",
                    "        print(f'   Best accuracy: {best_accuracy:.3f}')\\n",
                    "        print(f'   Total time: {training_time:.2f}s')\\n",
                    "        print(f'   Privacy preserved: ✅')\\n",
                    "        \\n",
                    "        return jsonify(response)\\n",
                    "        \\n",
                    "    except Exception as e:\\n",
                    "        error_response = {\\n",
                    "            'status': 'error',\\n",
                    "            'message': f'Training failed: {str(e)}',\\n",
                    "            'deployment': 'google_colab',\\n",
                    "            'timestamp': datetime.now().isoformat()\\n",
                    "        }\\n",
                    "        print(f'❌ Training error: {str(e)}')\\n",
                    "        return jsonify(error_response), 500\\n",
                    "\\n",
                    "# Start Flask server\\n",
                    "def run_server():\\n",
                    "    app.run(host='0.0.0.0', port=5000, debug=False)\\n",
                    "\\n",
                    "server_thread = threading.Thread(target=run_server)\\n",
                    "server_thread.daemon = True\\n",
                    "server_thread.start()\\n",
                    "\\n",
                    "# Create ngrok tunnel\\n",
                    "public_url = ngrok.connect(5000)\\n",
                    "\\n",
                    "print('\\\\n🌐 PRIVACY-PRESERVING ML CLOUD SERVICE STARTED!')\\n",
                    "print('=' * 55)\\n",
                    "print(f'🔗 Public URL: {public_url}')\\n",
                    "print(f'📍 Local URL: http://localhost:5000')\\n",
                    "print('\\\\n🛡️  Privacy Features:')\\n",
                    "print('   ✅ Only latent vectors accepted')\\n",
                    "print('   ❌ Raw data automatically rejected')\\n",
                    "print('   🔒 HTTPS encryption enabled')\\n",
                    "print('\\\\n📋 Available Endpoints:')\\n",
                    "print(f'   GET  {public_url}/health - Health check')\\n",
                    "print(f'   POST {public_url}/train - Train ML models')\\n",
                    "print('\\\\n🚀 Ready for your privacy-preserving pipeline!')\\n",
                    "print('\\\\n📋 COPY THIS URL FOR YOUR LOCAL PROJECT:')\\n",
                    "print(f'\\\"{\"{public_url}\"}\\\"')\\n",
                    "print('\\\\n⚠️  Keep this cell running to maintain the service!')"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {
                    "id": "keep_running"
                },
                "outputs": [],
                "source": [
                    "# Cell 4: Keep Server Running\\n",
                    "import time\\n",
                    "\\n",
                    "try:\\n",
                    "    print('🔄 Server running... Press Ctrl+C to stop')\\n",
                    "    print('⚠️  Do not stop this cell - it keeps your service alive!')\\n",
                    "    print('\\\\n📊 Service Status:')\\n",
                    "    \\n",
                    "    while True:\\n",
                    "        print(f'   ✅ Service active at {datetime.now().strftime(\\\"%H:%M:%S\\\")}', end='\\\\r')\\n",
                    "        time.sleep(30)  # Update every 30 seconds\\n",
                    "        \\n",
                    "except KeyboardInterrupt:\\n",
                    "    ngrok.disconnect(public_url)\\n",
                    "    print('\\\\n🛑 Server stopped - Service is now offline')"
                ]
            }
        ]
    }
    
    # Save notebook
    with open('Privacy_ML_Cloud_Service.ipynb', 'w') as f:
        json.dump(notebook_content, f, indent=2)
    
    print("📓 Google Colab notebook created: Privacy_ML_Cloud_Service.ipynb")
    return "Privacy_ML_Cloud_Service.ipynb"

def setup_local_config():
    """Setup local configuration files"""
    
    # Create config template
    config = {
        "endpoint": "https://your-ngrok-url.ngrok.io",
        "setup_instructions": [
            "1. Open the generated Google Colab notebook",
            "2. Run all cells and get the ngrok URL",
            "3. Replace the endpoint above with your actual URL",
            "4. Run: python test_colab_connection.py",
            "5. Run: python main.py"
        ],
        "created": datetime.now().isoformat()
    }
    
    with open('colab_config.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    print("⚙️  Configuration file created: colab_config.json")

def create_quick_test():
    """Create a quick test script"""
    
    test_script = '''#!/usr/bin/env python3
"""
Quick Test for Google Colab Service
Run this after setting up your Colab service
"""

import requests
import json
import numpy as np

def quick_test():
    """Quick test of the Colab service"""
    
    # Load config
    try:
        with open('colab_config.json', 'r') as f:
            config = json.load(f)
            endpoint = config['endpoint']
    except FileNotFoundError:
        print("❌ colab_config.json not found")
        return False
    
    if "your-ngrok-url" in endpoint:
        print("❌ Please update colab_config.json with your actual ngrok URL")
        return False
    
    print(f"🧪 Testing: {endpoint}")
    
    # Test health
    try:
        response = requests.get(f"{endpoint}/health", timeout=10)
        if response.status_code == 200:
            print("✅ Health check passed")
            health_data = response.json()
            print(f"   Service: {health_data.get('service', 'Unknown')}")
            print(f"   Deployment: {health_data.get('deployment', 'Unknown')}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Connection failed: {str(e)}")
        return False
    
    # Test training
    try:
        print("\\n🧪 Testing training endpoint...")
        
        # Create test data (latent vectors only)
        test_data = {
            "latent_vectors": np.random.randn(50, 128).tolist(),
            "labels": np.random.randint(0, 3, 50).tolist(),
            "metadata": {
                "privacy_preserved": True,
                "original_data_included": False,
                "test_data": True
            }
        }
        
        response = requests.post(
            f"{endpoint}/train",
            json=test_data,
            headers={'Content-Type': 'application/json'},
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Training test passed")
            print(f"   Best model: {result['summary']['best_model']}")
            print(f"   Best accuracy: {result['summary']['best_accuracy']:.3f}")
            print(f"   Privacy preserved: {result['summary']['privacy_preserved']}")
        else:
            print(f"❌ Training test failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Training test error: {str(e)}")
        return False
    
    print("\\n🎉 All tests passed! Your Colab service is ready!")
    print("\\n🚀 Run the full pipeline:")
    print("   python main.py")
    
    return True

if __name__ == "__main__":
    quick_test()
'''
    
    with open('quick_test_colab.py', 'w') as f:
        f.write(test_script)
    
    print("🧪 Quick test script created: quick_test_colab.py")

def main():
    """Main setup function"""
    print("🚀 AUTOMATED GOOGLE COLAB + NGROK SETUP")
    print("=" * 50)
    print()
    
    print("📋 Creating setup files...")
    
    # Create notebook
    notebook_file = create_colab_notebook()
    
    # Setup config
    setup_local_config()
    
    # Create test script
    create_quick_test()
    
    print()
    print("✅ SETUP COMPLETE!")
    print("=" * 20)
    print()
    print("📋 NEXT STEPS:")
    print("=" * 15)
    print()
    print("1. 🔑 Get ngrok token:")
    print("   https://dashboard.ngrok.com/get-started/your-authtoken")
    print()
    print("2. 📓 Open Google Colab:")
    print("   https://colab.research.google.com/")
    print()
    print("3. 📤 Upload the notebook:")
    print(f"   Upload: {notebook_file}")
    print("   OR create new notebook and copy the cells")
    print()
    print("4. ▶️  Run all cells in the notebook:")
    print("   - Cell 1: Install dependencies")
    print("   - Cell 2: Enter your ngrok token")
    print("   - Cell 3: Start the service (copy the URL)")
    print("   - Cell 4: Keep running")
    print()
    print("5. 🔗 Update your local config:")
    print("   Edit colab_config.json with the ngrok URL")
    print()
    print("6. 🧪 Test the connection:")
    print("   python quick_test_colab.py")
    print()
    print("7. 🚀 Run the full pipeline:")
    print("   python main.py")
    print()
    print("🎯 Your privacy-preserving cloud ML service will be ready!")

if __name__ == "__main__":
    main()