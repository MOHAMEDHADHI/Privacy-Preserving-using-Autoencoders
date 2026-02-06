#!/usr/bin/env python3
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
        print("ERROR: colab_config.json not found")
        return False
    
    if "your-ngrok-url" in endpoint:
        print("ERROR: Please update colab_config.json with your actual ngrok URL")
        return False
    
    print(f"Testing: {endpoint}")
    
    # Test health
    try:
        response = requests.get(f"{endpoint}/health", timeout=10)
        if response.status_code == 200:
            print("SUCCESS: Health check passed")
            health_data = response.json()
            print(f"   Service: {health_data.get('service', 'Unknown')}")
            print(f"   Deployment: {health_data.get('deployment', 'Unknown')}")
        else:
            print(f"ERROR: Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"ERROR: Connection failed: {str(e)}")
        return False
    
    # Test training
    try:
        print("\nTesting training endpoint...")
        
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
            print("SUCCESS: Training test passed")
            print(f"   Best model: {result['summary']['best_model']}")
            print(f"   Best accuracy: {result['summary']['best_accuracy']:.3f}")
            print(f"   Privacy preserved: {result['summary']['privacy_preserved']}")
        else:
            print(f"ERROR: Training test failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"ERROR: Training test error: {str(e)}")
        return False
    
    print("\nSUCCESS: All tests passed! Your Colab service is ready!")
    print("\nRun the full pipeline:")
    print("   python main.py")
    
    return True

if __name__ == "__main__":
    quick_test()