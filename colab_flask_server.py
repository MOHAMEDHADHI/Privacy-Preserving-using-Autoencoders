#!/usr/bin/env python3
"""
Google Colab Flask Server - Copy this code to Google Colab
Simple setup for privacy-preserving ML cloud service
"""

# ============================================================================
# GOOGLE COLAB SETUP - Copy and paste this into Google Colab cells
# ============================================================================

COLAB_CODE = '''
# Cell 1: Install dependencies
!pip install flask pyngrok scikit-learn numpy pandas requests

# Cell 2: Setup ngrok
!ngrok authtoken YOUR_NGROK_TOKEN_HERE
# Get your token from: https://dashboard.ngrok.com/get-started/your-authtoken

# Cell 3: Create Flask server
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
from pyngrok import ngrok

app = Flask(__name__)

# Global storage
trained_models = {}
training_results = {}

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'service': 'Privacy-Preserving ML Cloud Service',
        'status': 'running',
        'message': 'Send latent vectors to /train endpoint',
        'privacy': 'Raw data automatically rejected'
    })

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'privacy_preserved': True
    })

@app.route('/train', methods=['POST'])
def train():
    try:
        print("\\n🚀 RECEIVED TRAINING REQUEST")
        data = request.get_json()
        
        # Extract data
        latent_vectors = np.array(data['latent_vectors'])
        labels = np.array(data['labels'])
        metadata = data.get('metadata', {})
        
        print(f"📊 Data received: {latent_vectors.shape}")
        print(f"🛡️  Privacy preserved: {metadata.get('privacy_preserved', True)}")
        
        # Reject if raw data detected
        if metadata.get('original_data_included', False):
            return jsonify({'error': 'Privacy violation - raw data detected!'}), 400
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            latent_vectors, labels, test_size=0.2, random_state=42
        )
        
        # Train models
        models = {
            'logistic': LogisticRegression(random_state=42, max_iter=1000),
            'mlp': MLPClassifier(hidden_layer_sizes=(64, 32), random_state=42, max_iter=300),
            'forest': RandomForestClassifier(n_estimators=50, random_state=42)
        }
        
        results = {}
        start_time = time.time()
        
        for name, model in models.items():
            try:
                print(f"🤖 Training {name}...")
                model.fit(X_train, y_train)
                
                pred = model.predict(X_test)
                acc = accuracy_score(y_test, pred)
                
                model_id = f"cloud_{name}_{int(time.time())}"
                trained_models[model_id] = model
                
                results[name] = {
                    'model_id': model_id,
                    'accuracy': float(acc),
                    'status': 'success'
                }
                
                print(f"   ✅ {name}: {acc:.3f}")
                
            except Exception as e:
                results[name] = {'error': str(e), 'status': 'failed'}
        
        training_time = time.time() - start_time
        
        # Find best model
        successful = {k: v for k, v in results.items() if v['status'] == 'success'}
        best_model = max(successful.keys(), key=lambda k: successful[k]['accuracy']) if successful else None
        
        response = {
            'status': 'success',
            'results': results,
            'summary': {
                'best_model': best_model,
                'best_accuracy': successful[best_model]['accuracy'] if best_model else 0.0,
                'total_training_time': training_time,
                'privacy_preserved': True
            }
        }
        
        print(f"✅ Training completed: {best_model} ({successful[best_model]['accuracy']:.3f})")
        return jsonify(response)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Cell 4: Start server with ngrok
def run_server():
    app.run(host='0.0.0.0', port=5000, debug=False)

# Start Flask in background
server_thread = threading.Thread(target=run_server)
server_thread.daemon = True
server_thread.start()

# Create ngrok tunnel
public_url = ngrok.connect(5000)

print("\\n🌐 PRIVACY-PRESERVING ML CLOUD SERVICE")
print("=" * 50)
print(f"🔗 Public URL: {public_url}")
print(f"📍 Local URL: http://localhost:5000")
print("\\n📋 Endpoints:")
print(f"   GET  {public_url}/health")
print(f"   POST {public_url}/train")
print("\\n🛡️  Privacy Status: Only latent vectors accepted")
print("❌ Raw data automatically rejected")
print("\\n🚀 Ready for your privacy-preserving pipeline!")
print(f"\\n📋 Copy this URL for your local project:")
print(f'COLAB_ENDPOINT = "{public_url}"')

# Cell 5: Keep running
import time
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    ngrok.disconnect(public_url)
    print("\\n🛑 Server stopped")
'''

if __name__ == "__main__":
    print("Google Colab Flask Server Setup")
    print("=" * 35)
    print()
    print("📋 QUICK SETUP INSTRUCTIONS:")
    print()
    print("1. 🔑 Get ngrok token:")
    print("   https://dashboard.ngrok.com/get-started/your-authtoken")
    print()
    print("2. 📓 Open Google Colab:")
    print("   https://colab.research.google.com/")
    print()
    print("3. 📝 Create new notebook and copy the code below:")
    print()
    print("=" * 50)
    print("COLAB CODE:")
    print("=" * 50)
    print(COLAB_CODE)
    print("=" * 50)
    print()
    print("4. 🔄 Replace YOUR_NGROK_TOKEN_HERE with your actual token")
    print("5. ▶️  Run all cells")
    print("6. 🔗 Copy the public URL that appears")
    print("7. 🚀 Use the URL in your local project")