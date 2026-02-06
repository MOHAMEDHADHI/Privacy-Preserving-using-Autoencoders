#!/usr/bin/env python3
"""
Test Google Colab + ngrok Connection
Quick test to verify your cloud integration is working
"""

import requests
import json
import numpy as np
import time

def test_colab_connection():
    """Test connection to Google Colab service"""
    print("🧪 TESTING GOOGLE COLAB CONNECTION")
    print("=" * 40)
    
    # Get endpoint
    endpoint = get_endpoint()
    if not endpoint:
        print("❌ No endpoint configured")
        return False
    
    print(f"🔗 Testing endpoint: {endpoint}")
    
    # Test 1: Health check
    print("\n1️⃣ Testing health check...")
    try:
        response = requests.get(f"{endpoint}/health", timeout=10)
        if response.status_code == 200:
            health_data = response.json()
            print(f"   ✅ Health check passed")
            print(f"   Service: {health_data.get('service', 'Unknown')}")
            print(f"   Status: {health_data.get('status', 'Unknown')}")
        else:
            print(f"   ❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Health check error: {str(e)}")
        return False
    
    # Test 2: Training endpoint with dummy data
    print("\n2️⃣ Testing training endpoint...")
    try:
        # Create dummy latent vectors (privacy-preserving)
        dummy_latent = np.random.randn(100, 128).tolist()
        dummy_labels = np.random.randint(0, 3, 100).tolist()
        
        payload = {
            "latent_vectors": dummy_latent,
            "labels": dummy_labels,
            "metadata": {
                "privacy_preserved": True,
                "original_data_included": False,
                "test_data": True
            }
        }
        
        print(f"   📤 Sending test latent vectors...")
        print(f"   Shape: (100, 128)")
        print(f"   Privacy preserved: ✅")
        
        response = requests.post(
            f"{endpoint}/train",
            json=payload,
            headers={'Content-Type': 'application/json'},
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Training test passed")
            print(f"   Status: {result.get('status', 'Unknown')}")
            print(f"   Best model: {result.get('summary', {}).get('best_model', 'Unknown')}")
            print(f"   Best accuracy: {result.get('summary', {}).get('best_accuracy', 0):.3f}")
            print(f"   Training time: {result.get('summary', {}).get('total_training_time', 0):.2f}s")
        else:
            print(f"   ❌ Training test failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"   ❌ Training test error: {str(e)}")
        return False
    
    # Test 3: Models endpoint
    print("\n3️⃣ Testing models endpoint...")
    try:
        response = requests.get(f"{endpoint}/models", timeout=10)
        if response.status_code == 200:
            models_data = response.json()
            print(f"   ✅ Models endpoint working")
            print(f"   Models available: {models_data.get('count', 0)}")
        else:
            print(f"   ❌ Models endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Models endpoint error: {str(e)}")
    
    print("\n🎉 CONNECTION TEST COMPLETED SUCCESSFULLY!")
    print("✅ Your Google Colab + ngrok integration is working")
    print("🚀 Ready to run the full privacy-preserving pipeline")
    
    return True

def get_endpoint():
    """Get the Google Colab endpoint"""
    import os
    
    # Method 1: Environment variable
    endpoint = os.environ.get('COLAB_ENDPOINT')
    if endpoint:
        return endpoint
    
    # Method 2: Config file
    try:
        with open('colab_config.json', 'r') as f:
            config = json.load(f)
            return config.get('endpoint')
    except FileNotFoundError:
        pass
    
    # Method 3: Interactive input
    print("🔗 COLAB ENDPOINT CONFIGURATION:")
    print("Please enter your Google Colab ngrok URL")
    print("Example: https://abc123.ngrok.io")
    
    endpoint = input("Enter URL: ").strip()
    if endpoint:
        # Save for future use
        config = {'endpoint': endpoint}
        with open('colab_config.json', 'w') as f:
            json.dump(config, f, indent=2)
        return endpoint
    
    return None

def setup_instructions():
    """Display setup instructions"""
    print("📋 GOOGLE COLAB + NGROK SETUP INSTRUCTIONS")
    print("=" * 50)
    print()
    print("If the connection test fails, follow these steps:")
    print()
    print("1. 📓 Open Google Colab:")
    print("   https://colab.research.google.com/")
    print()
    print("2. 🔑 Get ngrok token:")
    print("   https://dashboard.ngrok.com/get-started/your-authtoken")
    print()
    print("3. 📝 Create new notebook and run the setup code")
    print("   (See setup_colab_integration.md for complete code)")
    print()
    print("4. 🔗 Copy the ngrok public URL from Colab output")
    print()
    print("5. 🔄 Run this test again with the URL")
    print()

if __name__ == "__main__":
    success = test_colab_connection()
    
    if not success:
        print("\n" + "=" * 50)
        setup_instructions()