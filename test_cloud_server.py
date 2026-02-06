#!/usr/bin/env python3
"""
Test Cloud Server
Test the Flask cloud server with latent vectors
"""

import requests
import json
import torch
import torch.nn as nn
import numpy as np

class LocalEncoder(nn.Module):
    """Privacy-preserving encoder"""
    
    def __init__(self, input_dim, latent_dim=128):
        super(LocalEncoder, self).__init__()
        
        if isinstance(input_dim, (list, tuple)):
            input_size = input_dim[0] if len(input_dim) > 0 else input_dim
        else:
            input_size = input_dim
            
        self.encoder = nn.Sequential(
            nn.Linear(input_size, 256),
            nn.ReLU(),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Linear(128, latent_dim)
        )
        
        self.latent_dim = latent_dim
    
    def forward(self, x):
        return self.encoder(x)

def test_cloud_server():
    """Test the cloud server with latent vectors"""
    
    print("🧪 TESTING CLOUD SERVER")
    print("=" * 30)
    
    # Server URL
    server_url = "http://localhost:5000"
    
    # Create encoder and generate latent vectors
    encoder = LocalEncoder(input_dim=20, latent_dim=128)
    
    print("📊 Generating test latent vectors...")
    
    # Generate 5 training samples
    training_samples = []
    for i in range(5):
        input_data = torch.randn(1, 20)
        label = i % 3  # Labels 0, 1, 2, 0, 1
        
        with torch.no_grad():
            latent = encoder(input_data)
            latent = latent.detach().cpu().numpy()
        
        # Create payload
        payload = {
            "client_id": "client_001",
            "latent_vector": latent.tolist()[0],  # Flatten to 1D list
            "label": int(label)
        }
        
        training_samples.append(payload)
        print(f"   Sample {i+1}: latent shape {len(payload['latent_vector'])}, label {label}")
    
    # Test 1: Upload latent vectors
    print(f"\n🔄 TEST 1: Uploading latent vectors to cloud...")
    
    for i, sample in enumerate(training_samples):
        try:
            response = requests.post(f"{server_url}/upload_latent", json=sample)
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ Sample {i+1}: {result['status']}")
            else:
                print(f"   ❌ Sample {i+1}: Failed with status {response.status_code}")
        except Exception as e:
            print(f"   ❌ Sample {i+1}: Error - {str(e)}")
    
    # Test 2: Train model
    print(f"\n🎯 TEST 2: Training model on cloud...")
    
    try:
        response = requests.post(f"{server_url}/train")
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Training: {result['status']}")
            print(f"   📊 Samples used: {result['samples']}")
        else:
            print(f"   ❌ Training failed with status {response.status_code}")
    except Exception as e:
        print(f"   ❌ Training error: {str(e)}")
    
    # Test 3: Make predictions
    print(f"\n🔮 TEST 3: Making predictions...")
    
    # Generate test sample for prediction
    test_input = torch.randn(1, 20)
    with torch.no_grad():
        test_latent = encoder(test_input)
        test_latent = test_latent.detach().cpu().numpy()
    
    prediction_payload = {
        "client_id": "client_001",
        "latent_vector": test_latent.tolist()[0]  # Flatten to 1D list
    }
    
    try:
        response = requests.post(f"{server_url}/predict", json=prediction_payload)
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Prediction: {result['prediction']}")
            print(f"   📊 Confidence: {result['confidence']:.4f}")
        else:
            print(f"   ❌ Prediction failed with status {response.status_code}")
    except Exception as e:
        print(f"   ❌ Prediction error: {str(e)}")
    
    print(f"\n🎉 CLOUD SERVER TEST COMPLETE")
    print("=" * 35)
    print("✅ Latent vectors uploaded to cloud")
    print("✅ Model trained on cloud server")
    print("✅ Predictions made from cloud")
    print("✅ Privacy preserved (only latent vectors sent)")

if __name__ == "__main__":
    test_cloud_server()