#!/usr/bin/env python3
"""
Test script to train models on Render Flask server
Uses latent vectors from part1_local_latent_generation.py
"""

import requests
import torch
import numpy as np
import json
from datetime import datetime

def test_render_server():
    """Test the Render Flask server with actual training"""
    
    print("🧪 TESTING RENDER FLASK SERVER")
    print("=" * 60)
    
    # Server URL
    server_url = "http://127.0.0.1:5000"
    
    # Step 1: Health Check
    print("\n1️⃣ Testing Health Endpoint...")
    try:
        response = requests.get(f"{server_url}/health", timeout=5)
        if response.status_code == 200:
            health_data = response.json()
            print(f"   ✅ Server is healthy!")
            print(f"   Status: {health_data['status']}")
            print(f"   Privacy guaranteed: {health_data['privacy_guaranteed']}")
        else:
            print(f"   ❌ Health check failed: {response.status_code}")
            return
    except Exception as e:
        print(f"   ❌ Cannot connect to server: {e}")
        print(f"   Make sure server is running: python render_app.py")
        return
    
    # Step 2: Load Latent Vectors
    print("\n2️⃣ Loading Latent Vectors...")
    try:
        data = torch.load('latent_vectors.pt')
        
        # Extract latent vectors and labels from the saved dictionary
        if isinstance(data, dict):
            latent_vectors = data['latent_vectors']
            labels = data.get('labels', None)
            print(f"   ✅ Loaded from dictionary format")
            print(f"   Privacy preserved: {data.get('privacy_preserved', 'Unknown')}")
        else:
            latent_vectors = data
            labels = None
        
        # Convert to numpy if it's a tensor
        if torch.is_tensor(latent_vectors):
            latent_vectors = latent_vectors.numpy()
        
        print(f"   ✅ Loaded latent vectors: {latent_vectors.shape}")
        
        # Use saved labels or generate sample labels
        if labels is None:
            num_samples = latent_vectors.shape[0]
            labels = np.random.randint(0, 5, size=num_samples)  # 5 classes
            print(f"   ⚠️  Generated random labels: {labels.shape}")
        else:
            if torch.is_tensor(labels):
                labels = labels.numpy()
            print(f"   ✅ Using saved labels: {labels.shape}")
        
    except FileNotFoundError:
        print(f"   ❌ latent_vectors.pt not found!")
        print(f"   Run part1_local_latent_generation.py first to generate latent vectors")
        return
    except Exception as e:
        print(f"   ❌ Error loading latent vectors: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Step 3: Prepare Training Payload
    print("\n3️⃣ Preparing Training Payload...")
    
    num_samples = latent_vectors.shape[0]
    num_features = latent_vectors.shape[1]
    num_classes = len(np.unique(labels))
    
    payload = {
        "latent_vectors": latent_vectors.tolist(),
        "labels": labels.tolist(),
        "metadata": {
            "privacy_preserved": True,
            "original_data_included": False,
            "data_type": "image_latent_vectors",
            "timestamp": datetime.now().isoformat(),
            "source": "local_privacy_preserving_encoder"
        }
    }
    
    payload_size = len(json.dumps(payload))
    print(f"   ✅ Payload prepared")
    print(f"   Payload size: {payload_size:,} bytes ({payload_size/1024:.1f} KB)")
    print(f"   Samples: {num_samples}")
    print(f"   Features: {num_features}")
    print(f"   Classes: {num_classes}")
    
    # Step 4: Send Training Request
    print("\n4️⃣ Sending Training Request to Cloud...")
    print(f"   Endpoint: {server_url}/train")
    print(f"   🔒 Privacy: Raw data NOT included")
    print(f"   📤 Transmitting latent vectors only...")
    
    try:
        response = requests.post(
            f"{server_url}/train",
            json=payload,
            timeout=60,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            result = response.json()
            
            print(f"\n✅ CLOUD TRAINING SUCCESSFUL!")
            print("=" * 60)
            
            # Display Summary
            summary = result.get('summary', {})
            print(f"\n📊 TRAINING SUMMARY:")
            print(f"   Best Model: {summary.get('best_model', 'N/A')}")
            print(f"   Best Accuracy: {summary.get('best_accuracy', 0):.3f}")
            print(f"   Total Training Time: {summary.get('total_training_time', 0):.2f}s")
            print(f"   Models Trained: {summary.get('models_trained', 0)}")
            print(f"   Cloud Provider: {summary.get('cloud_provider', 'N/A')}")
            
            # Display Individual Model Results
            print(f"\n📈 INDIVIDUAL MODEL RESULTS:")
            results = result.get('results', {})
            for model_name, model_result in results.items():
                if model_result.get('status') == 'success':
                    print(f"\n   {model_name.replace('_', ' ').title()}:")
                    print(f"      Train Accuracy: {model_result.get('train_accuracy', 0):.3f}")
                    print(f"      Test Accuracy:  {model_result.get('test_accuracy', 0):.3f}")
                    print(f"      Precision:      {model_result.get('precision', 0):.3f}")
                    print(f"      Recall:         {model_result.get('recall', 0):.3f}")
                    print(f"      F1-Score:       {model_result.get('f1_score', 0):.3f}")
                    print(f"      Training Time:  {model_result.get('training_time', 0):.2f}s")
                    print(f"      Model ID:       {model_result.get('model_id', 'N/A')}")
            
            # Display Privacy Report
            print(f"\n🔒 PRIVACY REPORT:")
            privacy = result.get('privacy_report', {})
            print(f"   Raw Data Received: {privacy.get('raw_data_received', 'Unknown')}")
            print(f"   Latent Vectors Only: {privacy.get('latent_vectors_only', 'Unknown')}")
            print(f"   Privacy Policy Enforced: {privacy.get('privacy_policy_enforced', 'Unknown')}")
            print(f"   Data Encryption: {privacy.get('data_encryption', 'Unknown')}")
            print(f"   Data Retention: {privacy.get('data_retention', 'Unknown')}")
            
            print(f"\n🎉 TEST COMPLETED SUCCESSFULLY!")
            print("=" * 60)
            
            # Save results
            with open('render_training_results.json', 'w') as f:
                json.dump(result, f, indent=2)
            print(f"\n💾 Results saved to: render_training_results.json")
            
            return result
            
        else:
            print(f"\n❌ Training failed with status code: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except requests.exceptions.Timeout:
        print(f"\n❌ Request timeout - training took too long")
        return None
    except Exception as e:
        print(f"\n❌ Training error: {e}")
        return None

def test_models_endpoint():
    """Test the models listing endpoint"""
    print("\n\n5️⃣ Testing Models Endpoint...")
    try:
        response = requests.get("http://127.0.0.1:5000/models", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Models endpoint working")
            print(f"   Total models: {data.get('count', 0)}")
            if data.get('models'):
                print(f"   Available models:")
                for model_id, info in data['models'].items():
                    print(f"      - {info['model_type']} (created: {info['created']})")
        else:
            print(f"   ❌ Models endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

def test_results_endpoint():
    """Test the results endpoint"""
    print("\n6️⃣ Testing Results Endpoint...")
    try:
        response = requests.get("http://127.0.0.1:5000/results", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Results endpoint working")
            print(f"   Training sessions: {len(data.get('training_history', {}))}")
        else:
            print(f"   ❌ Results endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("🔒 PRIVACY-PRESERVING ML CLOUD SERVICE TEST")
    print("=" * 60)
    
    # Run main training test
    result = test_render_server()
    
    if result:
        # Test other endpoints
        test_models_endpoint()
        test_results_endpoint()
        
        print("\n" + "=" * 60)
        print("✅ ALL TESTS COMPLETED!")
        print("=" * 60)
        print("\n📝 Next Steps:")
        print("   1. Check render_training_results.json for detailed results")
        print("   2. Visit http://127.0.0.1:5000/ in browser for nice UI")
        print("   3. Deploy to Render with: gunicorn render_app:app")
        print("   4. Your privacy-preserving ML pipeline is working! 🎉")
    else:
        print("\n" + "=" * 60)
        print("❌ TESTS FAILED")
        print("=" * 60)
        print("\nTroubleshooting:")
        print("   1. Make sure server is running: python render_app.py")
        print("   2. Make sure latent_vectors.pt exists")
        print("   3. Check server logs for errors")
