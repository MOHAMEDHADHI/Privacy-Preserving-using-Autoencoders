#!/usr/bin/env python3
"""
Quick Start Script
Automated setup and demo of the complete privacy-preserving ML pipeline
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def print_header(text):
    """Print formatted header"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70 + "\n")

def print_step(step_num, text):
    """Print step number"""
    print(f"\n{'='*70}")
    print(f"  STEP {step_num}: {text}")
    print(f"{'='*70}\n")

def check_dependencies():
    """Check if required packages are installed"""
    print_step(1, "CHECKING DEPENDENCIES")
    
    required = ['torch', 'numpy', 'sklearn', 'flask', 'matplotlib', 'pandas']
    missing = []
    
    for package in required:
        try:
            __import__(package)
            print(f"✅ {package} installed")
        except ImportError:
            print(f"❌ {package} missing")
            missing.append(package)
    
    if missing:
        print(f"\n⚠️  Missing packages: {', '.join(missing)}")
        print("Run: pip install -r requirements.txt")
        return False
    
    print("\n✅ All dependencies installed!")
    return True

def initialize_database():
    """Initialize monitoring database"""
    print_step(2, "INITIALIZING MONITORING DATABASE")
    
    try:
        from admin_dashboard import init_database
        init_database()
        print("✅ Monitoring database initialized: monitoring.db")
        return True
    except Exception as e:
        print(f"❌ Database initialization failed: {str(e)}")
        return False

def check_render_config():
    """Check Render configuration"""
    print_step(3, "CHECKING RENDER CONFIGURATION")
    
    render_endpoint = os.environ.get('RENDER_ENDPOINT')
    api_key = os.environ.get('RENDER_API_KEY')
    
    if render_endpoint:
        print(f"✅ Render endpoint configured: {render_endpoint}")
    else:
        print("⚠️  RENDER_ENDPOINT not set")
        print("   Will use simulation mode")
        print("   To use real Render cloud:")
        print("   export RENDER_ENDPOINT=https://your-app.onrender.com")
    
    if api_key:
        print(f"✅ API key configured: {api_key[:10]}...")
    else:
        print("⚠️  RENDER_API_KEY not set")
        print("   Using default: demo_key_12345")
        print("   To set your key:")
        print("   export RENDER_API_KEY=your_api_key_here")
    
    return True

def create_directories():
    """Create necessary directories"""
    print_step(4, "CREATING DIRECTORIES")
    
    dirs = ['reports', 'static', 'dashboard_templates']
    
    for dir_name in dirs:
        Path(dir_name).mkdir(exist_ok=True)
        print(f"✅ {dir_name}/ directory ready")
    
    return True

def show_menu():
    """Show main menu"""
    print_header("PRIVACY-PRESERVING ML PIPELINE - QUICK START")
    
    print("Choose an option:")
    print()
    print("1. 🚀 Run Complete Integrated Pipeline")
    print("   (Data input → Encoding → Cloud training → Reports)")
    print()
    print("2. 📊 Start Admin Dashboard Only")
    print("   (Monitoring web interface on port 5001)")
    print()
    print("3. 📄 Generate Sample Report")
    print("   (Create demo HTML/JSON reports)")
    print()
    print("4. 🧪 Test Render Connection")
    print("   (Verify cloud endpoint is working)")
    print()
    print("5. 📚 View Documentation")
    print("   (Open setup guide)")
    print()
    print("6. ✅ Run System Check")
    print("   (Verify all components)")
    print()
    print("0. ❌ Exit")
    print()
    
    choice = input("Enter your choice (0-6): ").strip()
    return choice

def run_integrated_pipeline():
    """Run the complete integrated pipeline"""
    print_header("RUNNING INTEGRATED PIPELINE")
    
    try:
        from integrated_pipeline import IntegratedPipeline
        
        render_endpoint = os.environ.get('RENDER_ENDPOINT')
        api_key = os.environ.get('RENDER_API_KEY', 'demo_key_12345')
        
        pipeline = IntegratedPipeline(render_endpoint, api_key)
        result = pipeline.run_complete_pipeline()
        
        if result:
            print("\n" + "="*70)
            print("  ✅ PIPELINE COMPLETED SUCCESSFULLY!")
            print("="*70)
            print(f"\n📊 Results:")
            print(f"   Session ID: {result['session_data']['session_id']}")
            print(f"   Best Model: {result['session_data']['best_model']}")
            print(f"   Accuracy: {result['session_data']['best_accuracy']:.3f}")
            print(f"\n📄 Reports Generated:")
            print(f"   HTML: {result['reports']['html']}")
            print(f"   Chart: {result['reports']['chart']}")
            print(f"   JSON: {result['reports']['json']}")
            print(f"\n💡 Next: View admin dashboard (Option 2)")
        else:
            print("\n❌ Pipeline failed. Check error messages above.")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("Make sure all dependencies are installed.")

def start_dashboard():
    """Start admin dashboard"""
    print_header("STARTING ADMIN DASHBOARD")
    
    print("Starting dashboard server on http://localhost:5001")
    print("Press Ctrl+C to stop")
    print()
    
    try:
        subprocess.run([sys.executable, 'admin_dashboard.py'])
    except KeyboardInterrupt:
        print("\n\n✅ Dashboard stopped")

def generate_sample_report():
    """Generate sample report"""
    print_header("GENERATING SAMPLE REPORT")
    
    try:
        from report_generator import ReportGenerator
        from datetime import datetime
        
        generator = ReportGenerator()
        
        sample_session = {
            'session_id': f'demo_session_{int(time.time())}',
            'timestamp': datetime.now().isoformat(),
            'data_samples': 500,
            'latent_dim': 128,
            'models_trained': 3,
            'best_model': 'logistic_regression',
            'best_accuracy': 0.856,
            'training_time': 12.5,
            'cloud_provider': 'render'
        }
        
        sample_results = {
            'logistic_regression': {
                'status': 'success',
                'train_accuracy': 0.875,
                'test_accuracy': 0.856,
                'precision': 0.862,
                'recall': 0.851,
                'f1_score': 0.856,
                'training_time': 3.2
            },
            'mlp_classifier': {
                'status': 'success',
                'train_accuracy': 0.892,
                'test_accuracy': 0.841,
                'precision': 0.848,
                'recall': 0.839,
                'f1_score': 0.843,
                'training_time': 8.1
            },
            'random_forest': {
                'status': 'success',
                'train_accuracy': 0.910,
                'test_accuracy': 0.833,
                'precision': 0.840,
                'recall': 0.828,
                'f1_score': 0.834,
                'training_time': 1.2
            }
        }
        
        reports = generator.generate_complete_report(sample_session, sample_results)
        
        print("\n✅ Sample reports generated successfully!")
        print(f"   HTML: {reports['html']}")
        print(f"   Chart: {reports['chart']}")
        print(f"   JSON: {reports['json']}")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")

def test_render_connection():
    """Test Render endpoint connection"""
    print_header("TESTING RENDER CONNECTION")
    
    render_endpoint = os.environ.get('RENDER_ENDPOINT')
    
    if not render_endpoint:
        print("❌ RENDER_ENDPOINT not configured")
        print("Set it with: export RENDER_ENDPOINT=https://your-app.onrender.com")
        return
    
    try:
        import requests
        
        print(f"Testing endpoint: {render_endpoint}")
        print("Sending health check request...")
        
        response = requests.get(f"{render_endpoint}/health", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print("\n✅ Connection successful!")
            print(f"   Service: {data.get('service')}")
            print(f"   Status: {data.get('status')}")
            print(f"   Version: {data.get('version')}")
            print(f"   Deployment: {data.get('deployment')}")
        else:
            print(f"\n❌ Connection failed: {response.status_code}")
            print(f"   Response: {response.text}")
    
    except requests.exceptions.Timeout:
        print("\n❌ Connection timeout - endpoint not responding")
    except requests.exceptions.ConnectionError:
        print("\n❌ Connection error - cannot reach endpoint")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")

def view_documentation():
    """View documentation"""
    print_header("DOCUMENTATION")
    
    docs = [
        ("COMPLETE_SETUP_GUIDE.md", "Complete setup and usage guide"),
        ("ARCHITECTURE_COMPLETION_SUMMARY.md", "Architecture completion summary"),
        ("README.md", "Project overview"),
        ("DEPLOYMENT_READY.md", "Render deployment guide")
    ]
    
    print("Available documentation:\n")
    
    for i, (filename, description) in enumerate(docs, 1):
        if Path(filename).exists():
            print(f"{i}. {filename}")
            print(f"   {description}")
            print()
    
    print("Open these files in your text editor or browser.")

def run_system_check():
    """Run complete system check"""
    print_header("SYSTEM CHECK")
    
    checks = []
    
    # Check dependencies
    print("Checking dependencies...")
    deps_ok = check_dependencies()
    checks.append(("Dependencies", deps_ok))
    
    # Check database
    print("\nChecking database...")
    db_exists = Path('monitoring.db').exists()
    if db_exists:
        print("✅ monitoring.db exists")
    else:
        print("⚠️  monitoring.db not found (will be created on first run)")
    checks.append(("Database", db_exists or True))
    
    # Check directories
    print("\nChecking directories...")
    dirs_ok = all(Path(d).exists() for d in ['reports', 'dashboard_templates'])
    if dirs_ok:
        print("✅ All directories exist")
    else:
        print("⚠️  Some directories missing (will be created)")
    checks.append(("Directories", dirs_ok or True))
    
    # Check Render config
    print("\nChecking Render configuration...")
    render_ok = os.environ.get('RENDER_ENDPOINT') is not None
    if render_ok:
        print(f"✅ Render endpoint: {os.environ.get('RENDER_ENDPOINT')}")
    else:
        print("⚠️  Render endpoint not configured (will use simulation)")
    checks.append(("Render Config", True))  # Not critical
    
    # Check files
    print("\nChecking key files...")
    key_files = [
        'admin_dashboard.py',
        'report_generator.py',
        'integrated_pipeline.py',
        'render_app_enhanced.py'
    ]
    files_ok = all(Path(f).exists() for f in key_files)
    if files_ok:
        print("✅ All key files present")
    else:
        print("❌ Some key files missing")
    checks.append(("Key Files", files_ok))
    
    # Summary
    print("\n" + "="*70)
    print("  SYSTEM CHECK SUMMARY")
    print("="*70 + "\n")
    
    for check_name, status in checks:
        status_icon = "✅" if status else "❌"
        print(f"{status_icon} {check_name}")
    
    all_ok = all(status for _, status in checks)
    
    if all_ok:
        print("\n✅ System ready to use!")
    else:
        print("\n⚠️  Some issues detected - see details above")

def main():
    """Main function"""
    
    # Initial setup
    if not check_dependencies():
        print("\n❌ Please install dependencies first:")
        print("   pip install -r requirements.txt")
        return
    
    initialize_database()
    check_render_config()
    create_directories()
    
    # Main loop
    while True:
        choice = show_menu()
        
        if choice == '1':
            run_integrated_pipeline()
        elif choice == '2':
            start_dashboard()
        elif choice == '3':
            generate_sample_report()
        elif choice == '4':
            test_render_connection()
        elif choice == '5':
            view_documentation()
        elif choice == '6':
            run_system_check()
        elif choice == '0':
            print("\n👋 Goodbye!")
            break
        else:
            print("\n❌ Invalid choice. Please try again.")
        
        if choice != '0':
            input("\nPress Enter to continue...")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted by user. Goodbye!")
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()
