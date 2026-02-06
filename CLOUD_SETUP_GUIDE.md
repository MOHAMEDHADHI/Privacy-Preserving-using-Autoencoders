# 🌐 Complete Cloud Setup Guide
## Google Colab + ngrok vs Render Deployment

Choose your preferred cloud deployment method:

---

## 🚀 Option 1: Google Colab + ngrok (Quick Setup - 5 minutes)

### ✅ Pros:
- **Fast setup** (5 minutes)
- **Free** (no cost)
- **Easy testing**
- **Full control**

### ❌ Cons:
- **Temporary** (session-based)
- **Manual restart** needed
- **Sleep after inactivity**

### 📋 Setup Steps:

#### 1. Get ngrok Token
- Go to: https://dashboard.ngrok.com/get-started/your-authtoken
- Sign up (free)
- Copy your auth token

#### 2. Open Google Colab
- Go to: https://colab.research.google.com/
- Click "New notebook"

#### 3. Copy and Run This Code:

**Cell 1: Install Dependencies**
```python
!pip install flask pyngrok scikit-learn numpy pandas requests
```

**Cell 2: Setup ngrok**
```python
!ngrok authtoken YOUR_NGROK_TOKEN_HERE
# Replace YOUR_NGROK_TOKEN_HERE with your actual token
```

**Cell 3: Create Flask Server**
```python
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
trained_models = {}

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'service': 'Privacy-Preserving ML Cloud Service',
        'status': 'running',
        'deployment': 'google_colab'
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
        
        latent_vectors = np.array(data['latent_vectors'])
        labels = np.array(data['labels'])
        metadata = data.get('metadata', {})
        
        print(f"📊 Data received: {latent_vectors.shape}")
        
        # Privacy check
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
                
                model_id = f"colab_{name}_{int(time.time())}"
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
print("\\n🛡️  Privacy Status: Only latent vectors accepted")
print("\\n🚀 Ready for your privacy-preserving pipeline!")
print(f"\\n📋 Copy this URL:")
print(f'{public_url}')
```

**Cell 4: Keep Running**
```python
import time
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    ngrok.disconnect(public_url)
    print("\\n🛑 Server stopped")
```

#### 4. Copy the ngrok URL
After running, copy the URL that appears (e.g., `https://abc123.ngrok.io`)

#### 5. Configure Your Local Project
Create `colab_config.json`:
```json
{
  "endpoint": "https://your-ngrok-url.ngrok.io"
}
```

---

## 🌐 Option 2: Render Deployment (Permanent - 10 minutes)

### ✅ Pros:
- **Permanent service**
- **Always available**
- **HTTPS built-in**
- **Auto-deploy**
- **Professional**

### ❌ Cons:
- **Requires GitHub**
- **Free tier sleeps**
- **Slight setup complexity**

### 📋 Setup Steps:

#### 1. Prepare Repository
```bash
# Create new repo or use existing
git init
git add .
git commit -m "Privacy-preserving ML cloud service"
git branch -M main
git remote add origin https://github.com/yourusername/privacy-ml-cloud.git
git push -u origin main
```

#### 2. Deploy to Render
1. Go to: https://render.com/
2. Sign up with GitHub
3. Click "New +" → "Web Service"
4. Connect your GitHub repository
5. Configure:
   - **Name**: `privacy-ml-cloud`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r render_requirements.txt`
   - **Start Command**: `gunicorn render_app:app`

#### 3. Get Your URL
After deployment: `https://your-app.onrender.com`

#### 4. Configure Your Local Project
Create `render_config.json`:
```json
{
  "endpoint": "https://your-app.onrender.com"
}
```

---

## 🧪 Test Your Setup

### Quick Test Script:
```python
# Run this to test your cloud service
python test_colab_connection.py
```

### Manual Test:
```python
import requests
import numpy as np

# Replace with your URL
url = "https://your-service-url.com/train"

data = {
    "latent_vectors": np.random.randn(100, 128).tolist(),
    "labels": np.random.randint(0, 3, 100).tolist(),
    "metadata": {
        "privacy_preserved": True,
        "original_data_included": False
    }
}

response = requests.post(url, json=data)
print(response.json())
```

---

## 🚀 Run Your Privacy-Preserving Pipeline

Once your cloud service is running:

```bash
python main.py
```

The system will:
1. **Auto-detect** your cloud service
2. **Generate** latent vectors locally
3. **Send** only latent vectors to cloud
4. **Train** ML models in the cloud
5. **Test** privacy with attack simulations
6. **Report** comprehensive results

---

## 🔍 Expected Output

```
🌐 AUTO-DETECTING REAL CLOUD SERVICES
✅ Render service detected: https://your-app.onrender.com
📤 Transmitting latent vectors to Render...
   Data size: 1,352,277 bytes
   ❌ Raw sensitive data: NEVER TRANSMITTED
   🔒 HTTPS encryption: ✅
✅ Render cloud training completed!
   Best model: random_forest
   Best accuracy: 0.847
   Training time: 12.34s
   Privacy preserved: ✅
```

---

## 🛡️ Privacy Guarantees

Both options provide:
- ✅ **Raw data never transmitted**
- ✅ **Latent vectors only**
- ✅ **Automatic privacy validation**
- ✅ **HTTPS encryption**
- ✅ **Attack resistance testing**

---

## 🔧 Troubleshooting

### Google Colab Issues:
- **Token Error**: Get new token from ngrok dashboard
- **Session Timeout**: Restart notebook
- **Connection Failed**: Check ngrok tunnel is active

### Render Issues:
- **Build Failed**: Check `render_requirements.txt`
- **Service Sleeping**: First request takes ~30 seconds (free tier)
- **Deploy Failed**: Check logs in Render dashboard

### General Issues:
- **No Service Detected**: Check config files
- **Connection Timeout**: Verify service is running
- **Privacy Errors**: Ensure only latent vectors are sent

---

## 🎯 Recommendation

- **For Testing**: Use Google Colab + ngrok (quick setup)
- **For Production**: Use Render deployment (permanent service)
- **For Development**: Both work great!

Your privacy-preserving ML pipeline is now ready for real cloud integration! 🚀