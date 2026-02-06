#!/usr/bin/env python3
"""
Automated Setup with Your ngrok Token
Everything configured and ready to go!
"""

import json
import os

def setup_everything():
    """Setup everything with your ngrok token"""
    
    print("🚀 SETTING UP PRIVACY-PRESERVING ML CLOUD SERVICE")
    print("=" * 55)
    print("✅ Your ngrok token is already configured!")
    print()
    
    # Update colab config to be ready for URL
    config = {
        "endpoint": "REPLACE_WITH_NGROK_URL_FROM_COLAB",
        "token_configured": True,
        "ready_to_use": True,
        "instructions": [
            "1. Upload Privacy_ML_Cloud_Service_Ready.ipynb to Google Colab",
            "2. Run all 4 cells in the notebook",
            "3. Copy the ngrok URL that appears",
            "4. Replace REPLACE_WITH_NGROK_URL_FROM_COLAB in this file",
            "5. Run: python main.py"
        ]
    }
    
    with open('colab_config.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    print("📋 WHAT I'VE PREPARED FOR YOU:")
    print("=" * 35)
    print()
    print("✅ Privacy_ML_Cloud_Service_Ready.ipynb - Ready-to-use Colab notebook")
    print("✅ colab_config.json - Configuration file")
    print("✅ Your ngrok token: 35iBqxHoSoRf6KNoTW35eFZp6oX_UVfyXEVXsKh4uyAVq6Zth")
    print()
    print("🎯 NEXT STEPS (Just 3 steps!):")
    print("=" * 30)
    print()
    print("1. 📓 Go to Google Colab:")
    print("   https://colab.research.google.com/")
    print()
    print("2. 📤 Upload the notebook:")
    print("   Upload: Privacy_ML_Cloud_Service_Ready.ipynb")
    print("   (Your ngrok token is already in the notebook!)")
    print()
    print("3. ▶️  Run all 4 cells:")
    print("   - Cell 1: Install dependencies")
    print("   - Cell 2: Setup ngrok (token already configured)")
    print("   - Cell 3: Start service (COPY THE URL THAT APPEARS)")
    print("   - Cell 4: Keep running")
    print()
    print("4. 🔗 Update config:")
    print("   Edit colab_config.json and replace:")
    print("   'REPLACE_WITH_NGROK_URL_FROM_COLAB'")
    print("   with your actual ngrok URL")
    print()
    print("5. 🚀 Run your pipeline:")
    print("   python main.py")
    print()
    print("🎉 Your privacy-preserving cloud ML service will be ready!")
    print()
    print("💡 TIP: The ngrok URL will look like:")
    print("   https://abc123.ngrok.io")

if __name__ == "__main__":
    setup_everything()