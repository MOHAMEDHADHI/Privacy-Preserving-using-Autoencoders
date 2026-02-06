#!/usr/bin/env python3
"""
Test Render Logging - Verify latent vectors are shown in logs
"""

import requests
import torch
import numpy as np
from datetime import datetime

def test_render_logging():
    """Test that Render logs show latent vectors"""
    
    print("="*70)
    print("  TESTING RENDER LOGGING - LATENT VECTORS VISIBILITY")
    print("="*70)
    print()
    
    # Configuration
    render_endpoint = "https://privacy-preserving-using-autoencoders-1.onrender.com"
    api_key = "rnd_GY3hBI68fZ1nhHsPLIaMLCrFxHwC"
    
    print(f"🎯 Target: {render_endpoint}")
    print(f"🔑 API Key: {api_key[:20]}...")
    print()
    
    # Create test latent vectors
    print("📦 Creating test latent vectors...")
    latent_vectors = torch.randn(100, 128)  # 100 samples, 128 dimensions
    labels = torch.randint(0, 3, (100,))
    
    print(f"   Shape: {latent_vectors.shape}")
    print(f"   Sample values (first 10 dims of first sample):")
    print(f"   {latent_vectors[0][:10].numpy()}")
    print()
    
    # Prepare payload
    payload = {
        'latent_vectors': latent_vectors.numpy().tolist(),
        'labels': labels.numpy().tolist(),
        'metadata': {
            'shape': list(latent_vectors.shape),
            'timestamp': datetime.now().isoformat(),
            'privacy_preserved': True,
            'original_data_included': False,
            'test_run': True
        }
    }
    
    print("📤 Sending to Render...")
    print(f"   Payload size: {len(str(payload))} characters")
    print()
    
    try:
        headers = {
            'Content-Type': 'application/json',
            'X-API-Key': api_key
        }
        
        response = requests.post(
            f"{render_endpoint}/train",
            json=payload,
            headers=headers,
            timeout=120
        )
        
        if response.status_code == 200:
            result = response.json()
            
            print("✅ REQUEST SUCCESSFUL!")
            print("="*70)
            print(f"   Status: {result['status']}")
            print(f"   Best Model: {result['summary']['best_model']}")
            print(f"   Best Accuracy: {result['summary']['best_accuracy']:.3f}")
            print(f"   Training Time: {result['summary']['total_training_time']:.2f}s")
            print()
            
            print("📋 WHAT TO CHECK IN RENDER LOGS:")
            print("="*70)
            print("   1. Look for: '📦 RECEIVED LATENT VECTORS FROM CLIENT'")
            print("   2. Should show: Latent vectors shape: (100, 128)")
            print("   3. Should show: Number of samples: 100")
            print("   4. Should show: Latent dimensions: 128")
            print("   5. Should show: Sample latent vectors (first 3 samples)")
            print("   6. Should show: '✅ CONFIRMED: Training on LATENT VECTORS only'")
            print()
            
            print("🔍 EXPECTED LOG OUTPUT:")
            print("-"*70)
            print("📦 RECEIVED LATENT VECTORS FROM CLIENT:")
            print("   Latent vectors shape: (100, 128)")
            print("   Number of samples: 100")
            print("   Latent dimensions: 128")
            print("   Labels shape: (100,)")
            print("   Unique classes: 3")
            print("   Privacy preserved: True")
            print("   Raw data included: False")
            print()
            print("🔍 SAMPLE LATENT VECTORS (first 3 samples, first 10 dims):")
            print("   Sample 1: [0.123, -0.456, 0.789, ...]")
            print("   Sample 2: [-0.234, 0.567, -0.890, ...]")
            print("   Sample 3: [0.345, -0.678, 0.901, ...]")
            print("-"*70)
            print()
            
            print("✅ Test completed successfully!")
            print("   Check your Render dashboard logs to see the detailed output.")
            
        else:
            print(f"❌ Request failed: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except requests.exceptions.Timeout:
        print("❌ Request timeout")
    except requests.exceptions.ConnectionError:
        print("❌ Connection error")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == '__main__':
    test_render_logging()
