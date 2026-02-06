#!/usr/bin/env python3
"""
STEP 3: Prepare Latent Data for Cloud
Convert to JSON-safe format for cloud transmission
"""

import torch
import torch.nn as nn
import numpy as np
import json
from datetime import datetime

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

def step3_prepare_latent_data_for_cloud():
    """STEP 3: Prepare Latent Data for Cloud"""
    
    print("☁️ STEP 3: Prepare Latent Data for Cloud")
    print("=" * 42)
    print("Convert to JSON-safe format:")
    print()
    
    # Create sample input data and label
    input_data = torch.randn(1, 20)  # Single sample
    label = torch.tensor([2])  # Sample label
    
    print(f"📊 Input data shape: {input_data.shape}")
    print(f"📊 Label: {label.item()}")
    
    # Initialize encoder and generate latent vector
    encoder = LocalEncoder(input_dim=20, latent_dim=128)
    
    with torch.no_grad():
        latent = encoder(input_data)
        latent = latent.detach().cpu().numpy()
    
    print(f"\n🔐 Latent vector generated:")
    print(f"   Shape: {latent.shape}")
    print(f"   Type: {type(latent)}")
    
    # Convert to JSON-safe format (exactly as specified)
    print(f"\n📦 Converting to JSON-safe format...")
    print("Code execution:")
    print('payload = {')
    print('    "client_id": "client_001",')
    print('    "latent_vector": latent.tolist(),')
    print('    "label": int(label)   # only if training')
    print('}')
    
    # Execute the exact code format
    payload = {
        "client_id": "client_001",
        "latent_vector": latent.tolist(),
        "label": int(label)   # only if training
    }
    
    print(f"\n✅ Payload created:")
    print(f"   Client ID: {payload['client_id']}")
    print(f"   Latent vector type: {type(payload['latent_vector'])}")
    print(f"   Latent vector length: {len(payload['latent_vector'][0])}")
    print(f"   Label: {payload['label']}")
    print(f"   Label type: {type(payload['label'])}")
    
    # Show payload structure
    print(f"\n📋 PAYLOAD STRUCTURE:")
    print("=" * 25)
    print(f"{{")
    print(f'  "client_id": "{payload["client_id"]}",')
    print(f'  "latent_vector": [')
    print(f'    [{payload["latent_vector"][0][:5]}...] # 128 dimensions')
    print(f'  ],')
    print(f'  "label": {payload["label"]}')
    print(f"}}")
    
    # Verify JSON serialization
    print(f"\n🔍 JSON SERIALIZATION TEST:")
    print("=" * 30)
    
    try:
        json_string = json.dumps(payload)
        json_size = len(json_string)
        print(f"✅ JSON serialization successful")
        print(f"   JSON size: {json_size:,} bytes")
        print(f"   Ready for HTTP transmission: ✅")
        
        # Show first part of JSON
        print(f"\n📄 JSON Preview (first 200 chars):")
        print(f'   {json_string[:200]}...')
        
    except Exception as e:
        print(f"❌ JSON serialization failed: {str(e)}")
        return None
    
    return payload, json_string

def demonstrate_batch_payload():
    """Demonstrate batch payload preparation"""
    
    print(f"\n" + "=" * 50)
    print("🔄 BATCH PAYLOAD DEMONSTRATION")
    print("=" * 50)
    
    # Create batch data
    batch_size = 3
    input_batch = torch.randn(batch_size, 20)
    labels_batch = torch.tensor([0, 1, 2])
    
    encoder = LocalEncoder(input_dim=20, latent_dim=128)
    
    with torch.no_grad():
        latent_batch = encoder(input_batch)
        latent_batch = latent_batch.detach().cpu().numpy()
    
    print(f"📊 Batch input shape: {input_batch.shape}")
    print(f"📊 Batch latent shape: {latent_batch.shape}")
    print(f"📊 Batch labels: {labels_batch.tolist()}")
    
    # Create batch payload
    batch_payload = {
        "client_id": "client_001",
        "latent_vectors": latent_batch.tolist(),  # Note: plural for batch
        "labels": labels_batch.tolist()  # Note: plural for batch
    }
    
    print(f"\n📦 Batch payload structure:")
    print(f"   Client ID: {batch_payload['client_id']}")
    print(f"   Latent vectors: {len(batch_payload['latent_vectors'])} samples")
    print(f"   Each vector: {len(batch_payload['latent_vectors'][0])} dimensions")
    print(f"   Labels: {batch_payload['labels']}")
    
    # Test JSON serialization
    try:
        batch_json = json.dumps(batch_payload)
        print(f"✅ Batch JSON serialization successful")
        print(f"   Batch JSON size: {len(batch_json):,} bytes")
    except Exception as e:
        print(f"❌ Batch JSON serialization failed: {str(e)}")
    
    return batch_payload

def demonstrate_inference_payload():
    """Demonstrate inference-only payload (no labels)"""
    
    print(f"\n" + "=" * 50)
    print("🔮 INFERENCE PAYLOAD DEMONSTRATION")
    print("=" * 50)
    
    # Create inference data (no labels)
    input_data = torch.randn(1, 20)
    encoder = LocalEncoder(input_dim=20, latent_dim=128)
    
    with torch.no_grad():
        latent = encoder(input_data)
        latent = latent.detach().cpu().numpy()
    
    # Create inference payload (no label)
    inference_payload = {
        "client_id": "client_001",
        "latent_vector": latent.tolist()
        # No label for inference
    }
    
    print(f"📦 Inference payload (no training labels):")
    print(f"   Client ID: {inference_payload['client_id']}")
    print(f"   Latent vector: {len(inference_payload['latent_vector'][0])} dimensions")
    print(f"   Labels: Not included (inference only)")
    
    return inference_payload

def save_payload_examples():
    """Save payload examples to files"""
    
    print(f"\n💾 SAVING PAYLOAD EXAMPLES:")
    print("=" * 30)
    
    # Single sample payload
    encoder = LocalEncoder(input_dim=20, latent_dim=128)
    input_data = torch.randn(1, 20)
    label = torch.tensor([1])
    
    with torch.no_grad():
        latent = encoder(input_data)
        latent = latent.detach().cpu().numpy()
    
    # Training payload
    training_payload = {
        "client_id": "client_001",
        "latent_vector": latent.tolist(),
        "label": int(label)
    }
    
    # Save to file
    with open('training_payload.json', 'w') as f:
        json.dump(training_payload, f, indent=2)
    
    # Inference payload
    inference_payload = {
        "client_id": "client_001",
        "latent_vector": latent.tolist()
    }
    
    with open('inference_payload.json', 'w') as f:
        json.dump(inference_payload, f, indent=2)
    
    print(f"✅ Saved training_payload.json")
    print(f"✅ Saved inference_payload.json")
    
    # Show file sizes
    import os
    training_size = os.path.getsize('training_payload.json')
    inference_size = os.path.getsize('inference_payload.json')
    
    print(f"   Training payload size: {training_size:,} bytes")
    print(f"   Inference payload size: {inference_size:,} bytes")

def main():
    """Main function for Step 3"""
    
    # Single sample payload
    payload, json_string = step3_prepare_latent_data_for_cloud()
    
    # Batch payload demonstration
    batch_payload = demonstrate_batch_payload()
    
    # Inference payload demonstration
    inference_payload = demonstrate_inference_payload()
    
    # Save examples
    save_payload_examples()
    
    print(f"\n🎉 STEP 3 COMPLETE")
    print("=" * 20)
    print("✅ Single sample payload created")
    print("✅ Batch payload demonstrated")
    print("✅ Inference payload demonstrated")
    print("✅ JSON serialization verified")
    print("✅ Payload examples saved")
    print("✅ Ready for cloud transmission")
    
    print(f"\n📋 PAYLOAD FORMATS READY:")
    print(f"   Training: client_id + latent_vector + label")
    print(f"   Inference: client_id + latent_vector")
    print(f"   Batch: client_id + latent_vectors + labels")

if __name__ == "__main__":
    main()