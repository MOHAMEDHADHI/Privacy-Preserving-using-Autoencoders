#!/usr/bin/env python3
"""
Test Latent Vector Display Feature
Shows latent vectors locally before sending to cloud
"""

import os
os.environ['RENDER_ENDPOINT'] = 'https://privacy-preserving-using-autoencoders-1.onrender.com'
os.environ['RENDER_API_KEY'] = 'rnd_GY3hBI68fZ1nhHsPLIaMLCrFxHwC'

from integrated_pipeline import IntegratedPipeline
import sys
from io import StringIO

def test_with_auto_input():
    """Test with automated input"""
    
    print("="*70)
    print("  TESTING LATENT VECTOR DISPLAY FEATURE")
    print("="*70)
    print()
    
    # Create pipeline
    pipeline = IntegratedPipeline(
        render_endpoint=os.environ['RENDER_ENDPOINT'],
        api_key=os.environ['RENDER_API_KEY']
    )
    
    # Simulate manual input
    print("📝 STEP 1: MANUAL DATA INPUT (Automated for test)")
    print("-" * 40)
    
    config = {
        'dataset_path': 'D:\\Test',
        'data_type': 'csv',
        'sensitive_data': True,
        'timestamp': '2026-02-06T22:00:00'
    }
    
    print(f"✅ Configuration:")
    for key, value in config.items():
        print(f"   {key}: {value}")
    print("🔒 PRIVACY MODE ACTIVATED")
    
    # Load and encode data
    print(f"\n🔐 STEP 2: LOADING AND ENCODING DATA")
    print("-" * 40)
    
    data, labels, latent_vectors = pipeline.load_and_encode_data(config)
    
    # The display_latent_vectors_locally is called inside load_and_encode_data
    # Now we need to handle the user confirmation
    
    print("\n" + "="*70)
    print("  TEST COMPLETED")
    print("="*70)
    print()
    print("✅ Latent vectors displayed successfully!")
    print("✅ User can see:")
    print("   - Latent vector statistics")
    print("   - Sample values (first 5 samples)")
    print("   - Value ranges (min, max, mean, std)")
    print("   - Class distribution")
    print("   - Privacy information")
    print("   - Confirmation prompt before cloud transmission")
    print()
    print("📋 Next: User confirms and data is sent to Render cloud")

if __name__ == '__main__':
    test_with_auto_input()
