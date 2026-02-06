#!/usr/bin/env python3
"""
Test script for deployed Render service
Tests the live cloud deployment with actual latent vectors
"""

import requests
import torch
import numpy as np
import json
from datetime import datetime
import time

# Your deployed Render URL
RENDER_URL = "https://privacy-preserving-using-autoencoders-1.onrender.com"

def test_render_deployment():
    """Test the deployed Render service"""
    
    print("\n" + "=" * 70)
    print("🌐 TESTING DEPLOYED RENDER SERVICE")
    print("=" * 70)
    print(f"URL: {RENDER_URL}")
    print()
    
    # Step 1: Test Health Endpoint
    print("1️⃣ Testing Health Endpoint...")
    try:
        response = requests.get(f"{RENDER_URL}/health", timeout=30)
        if response.status_code == 200:
            health_data = response.json()
            print(f"   ✅ Service is healthy!")
            print(f"   Status: {health_data.get('status')}")
            print(f"   Deployment: {health_data.get('deployment')}")
            print(f"   Privacy guaranteed: {health_data.get('privacy_guaranteed')}")
        else:
            print(f"   ❌ Health check failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except requests.exceptions.Timeout:
        print(f"   ⏱️  Request timeout - Render free tier may be sleeping")
        print(f"   Waiting 30 seconds for service to wake up...")
        time.sleep(30)
        try:
            response = requests.get(f"{RENDER_URL}/health", timeout=60)
            if response.status_code == 200:
                print(f"   ✅ Service woke up successfully!")
            else:
                print(f"   ❌ Service still not responding")
                return False
        except Exception as e:
            print(f"   ❌ Cannot connect: {e}")
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    # Step 2: Test Home Endpoint
    print("\n2️⃣ Testing Home Endpoint...")
    try:
        response = requests.get(f"{RENDER_URL}/", timeout=30)
        if response.status_code == 200:
            print(f"   ✅ Home endpoint working")
            print(f"   Visit in browser: {RENDER_URL}/")
        else:
            print(f"   ⚠️  Home endpoint returned: {response.status_code}")
    except Exception as e:
        print(f"   ⚠️  Error: {e}")
    
    # Step 3: Load Latent Vectors
    print("\n3️⃣ Loading Latent Vectors...")
    try:
        data = torch.load('latent_vectors.pt')
        
        if isinstance(data, dict):
            latent_vectors = data['latent_vectors']
            labels = data.get('labels', None)
            print(f"   ✅ Loaded from dictionary format")
        else:
            latent_vectors = data
            labels = None
        
        if torch.is_tensor(latent_vectors):
            latent_vectors = latent_vectors.numpy()
        
        if labels is None:
            num_samples = latent_vectors.shape[0]
            labels = np.random.randint(0, 5, size=num_samples)
            print(f"   ⚠️  Generated random labels")
        else:
            if torch.is_tensor(labels):
                labels = labels.numpy()
        
        print(f"   ✅ Latent vectors: {latent_vectors.shape}")
        print(f"   ✅ Labels: {labels.shape}")
        
    except FileNotFoundError:
        print(f"   ❌ latent_vectors.pt not found!")
        print(f"   Run: python part1_local_latent_generation.py")
        return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    # Step 4: Prepare Payload
    print("\n4️⃣ Preparing Training Payload...")
    payload = {
        "latent_vectors": latent_vectors.tolist(),
        "labels": labels.tolist(),
        "metadata": {
            "privacy_preserved": True,
            "original_data_included": False,
            "data_type": "image_latent_vectors",
            "timestamp": datetime.now().isoformat(),
            "source": "local_privacy_preserving_encoder",
            "deployment_test": True
        }
    }
    
    payload_size = len(json.dumps(payload))
    print(f"   ✅ Payload prepared")
    print(f"   Size: {payload_size:,} bytes ({payload_size/1024:.1f} KB)")
    print(f"   Samples: {latent_vectors.shape[0]}")
    print(f"   Features: {latent_vectors.shape[1]}")
    print(f"   Classes: {len(np.unique(labels))}")
    
    # Step 5: Send Training Request to Deployed Service
    print("\n5️⃣ Sending Training Request to Render Cloud...")
    print(f"   🌐 Endpoint: {RENDER_URL}/train")
    print(f"   🔒 Privacy: Raw data NOT included")
    print(f"   📤 Transmitting latent vectors only...")
    print(f"   ⏱️  This may take 30-60 seconds on free tier...")
    
    try:
        start_time = time.time()
        response = requests.post(
            f"{RENDER_URL}/train",
            json=payload,
            timeout=120,  # 2 minutes timeout for Render free tier
            headers={'Content-Type': 'application/json'}
        )
        request_time = time.time() - start_time
        
        if response.status_code == 200:
            result = response.json()
            
            print(f"\n✅ RENDER CLOUD TRAINING SUCCESSFUL!")
            print("=" * 70)
            print(f"⏱️  Total request time: {request_time:.2f}s")
            
            # Display Summary
            summary = result.get('summary', {})
            print(f"\n📊 TRAINING SUMMARY:")
            print(f"   Best Model: {summary.get('best_model', 'N/A')}")
            print(f"   Best Accuracy: {summary.get('best_accuracy', 0):.3f}")
            print(f"   Training Time: {summary.get('total_training_time', 0):.2f}s")
            print(f"   Models Trained: {summary.get('models_trained', 0)}")
            print(f"   Cloud Provider: {summary.get('cloud_provider', 'N/A')}")
            
            # Display Individual Results
            print(f"\n📈 MODEL RESULTS:")
            results = result.get('results', {})
            for model_name, model_result in results.items():
                if model_result.get('status') == 'success':
                    print(f"\n   {model_name.replace('_', ' ').title()}:")
                    print(f"      Test Accuracy: {model_result.get('test_accuracy', 0):.3f}")
                    print(f"      Precision:     {model_result.get('precision', 0):.3f}")
                    print(f"      Recall:        {model_result.get('recall', 0):.3f}")
                    print(f"      F1-Score:      {model_result.get('f1_score', 0):.3f}")
            
            # Privacy Report
            print(f"\n🔒 PRIVACY REPORT:")
            privacy = result.get('privacy_report', {})
            print(f"   Raw Data Received: {privacy.get('raw_data_received', 'Unknown')}")
            print(f"   Latent Vectors Only: {privacy.get('latent_vectors_only', 'Unknown')}")
            print(f"   Privacy Policy Enforced: {privacy.get('privacy_policy_enforced', 'Unknown')}")
            print(f"   Data Encryption: {privacy.get('data_encryption', 'Unknown')}")
            
            # Save results
            with open('render_deployment_results.json', 'w') as f:
                json.dump(result, f, indent=2)
            print(f"\n💾 Results saved to: render_deployment_results.json")
            
            print(f"\n🎉 DEPLOYMENT TEST SUCCESSFUL!")
            print("=" * 70)
            return True
            
        elif response.status_code == 404:
            print(f"\n❌ Endpoint not found (404)")
            print(f"   Make sure your Render service is deployed with render_app.py")
            print(f"   Check that the /train endpoint exists")
            return False
        elif response.status_code == 500:
            print(f"\n❌ Server error (500)")
            print(f"   Check Render logs for errors")
            print(f"   Response: {response.text[:500]}")
            return False
        else:
            print(f"\n❌ Request failed: {response.status_code}")
            print(f"   Response: {response.text[:500]}")
            return False
            
    except requests.exceptions.Timeout:
        print(f"\n⏱️  Request timeout after 120 seconds")
        print(f"   Render free tier can be slow on first request")
        print(f"   Try again - service should be warmed up now")
        return False
    except requests.exceptions.ConnectionError:
        print(f"\n❌ Connection error")
        print(f"   Check if Render service is deployed and running")
        print(f"   Visit: {RENDER_URL}/health in browser")
        return False
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_other_endpoints():
    """Test other endpoints"""
    print("\n\n6️⃣ Testing Other Endpoints...")
    
    # Test models endpoint
    try:
        response = requests.get(f"{RENDER_URL}/models", timeout=30)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ /models endpoint: {data.get('count', 0)} models")
    except Exception as e:
        print(f"   ⚠️  /models endpoint: {e}")
    
    # Test results endpoint
    try:
        response = requests.get(f"{RENDER_URL}/results", timeout=30)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ /results endpoint: {len(data.get('training_history', {}))} sessions")
    except Exception as e:
        print(f"   ⚠️  /results endpoint: {e}")

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("🚀 RENDER DEPLOYMENT TEST")
    print("=" * 70)
    print(f"Testing: {RENDER_URL}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    success = test_render_deployment()
    
    if success:
        test_other_endpoints()
        
        print("\n" + "=" * 70)
        print("✅ ALL TESTS PASSED!")
        print("=" * 70)
        print("\n🎉 Your Privacy-Preserving ML Service is live on Render!")
        print(f"\n🌐 Access your service:")
        print(f"   Home: {RENDER_URL}/")
        print(f"   Health: {RENDER_URL}/health")
        print(f"   API Docs: {RENDER_URL}/")
        print("\n📝 Integration code:")
        print(f'''
import requests

response = requests.post(
    "{RENDER_URL}/train",
    json=payload
)
result = response.json()
print(result)
''')
    else:
        print("\n" + "=" * 70)
        print("❌ TESTS FAILED")
        print("=" * 70)
        print("\n🔧 Troubleshooting:")
        print("   1. Check Render dashboard for deployment status")
        print("   2. View Render logs for errors")
        print("   3. Verify Start Command: gunicorn render_app:app")
        print("   4. Check render_requirements.txt is present")
        print(f"   5. Test health endpoint: {RENDER_URL}/health")
