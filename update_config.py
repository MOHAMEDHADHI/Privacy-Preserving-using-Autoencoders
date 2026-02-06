#!/usr/bin/env python3
"""
Quick Config Updater
Run this after you get your ngrok URL from Colab
"""

import json

def update_config():
    """Update config with ngrok URL"""
    
    print("🔗 UPDATE COLAB CONFIG")
    print("=" * 25)
    print()
    
    # Get URL from user
    print("After running your Google Colab notebook, you'll see a URL like:")
    print("🔗 Public URL: https://abc123.ngrok.io")
    print()
    
    url = input("Enter your ngrok URL: ").strip()
    
    if not url:
        print("❌ No URL provided")
        return
    
    if not url.startswith('http'):
        url = 'https://' + url
    
    # Update config
    config = {
        "endpoint": url,
        "token_configured": True,
        "ready_to_use": True,
        "updated": True
    }
    
    with open('colab_config.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"✅ Config updated with: {url}")
    print()
    print("🧪 Test your connection:")
    print("   python quick_test_colab.py")
    print()
    print("🚀 Run your full pipeline:")
    print("   python main.py")

if __name__ == "__main__":
    update_config()