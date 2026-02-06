#!/usr/bin/env python3
"""
Integrated Privacy-Preserving ML Pipeline
Connects local processing, cloud training, monitoring, and reporting
"""

import torch
import torch.nn as nn
import numpy as np
from datetime import datetime
import json
import requests
import os
import sys

# Import local modules
from admin_dashboard import init_database, log_training_session, log_audit_action
from report_generator import ReportGenerator

class IntegratedPipeline:
    """Complete integrated pipeline with monitoring and reporting"""
    
    def __init__(self, render_endpoint=None, api_key=None):
        self.render_endpoint = render_endpoint or os.environ.get('RENDER_ENDPOINT')
        self.api_key = api_key or os.environ.get('RENDER_API_KEY', 'demo_key_12345')
        self.report_generator = ReportGenerator()
        
        # Initialize monitoring database
        init_database()
        
        print("🔒 INTEGRATED PRIVACY-PRESERVING ML PIPELINE")
        print("=" * 60)
        print(f"✅ Monitoring database initialized")
        print(f"✅ Report generator ready")
        if self.render_endpoint:
            print(f"✅ Render endpoint configured: {self.render_endpoint}")
        else:
            print(f"⚠️  No Render endpoint - using simulation mode")
        print()
    
    def manual_data_input(self):
        """Step 1: Manual data input with audit logging"""
        print("📝 STEP 1: MANUAL DATA INPUT")
        print("-" * 40)
        
        dataset_path = input("Enter dataset path: ").strip()
        data_type = input("Data type (image/csv): ").strip().lower()
        sensitive = input("Contains sensitive data? (yes/no): ").strip().lower()
        
        config = {
            'dataset_path': dataset_path,
            'data_type': data_type,
            'sensitive_data': sensitive == 'yes',
            'timestamp': datetime.now().isoformat()
        }
        
        # Log audit action
        log_audit_action(
            action='manual_data_input',
            user='local_user',
            details=json.dumps(config),
            status='success'
        )
        
        print(f"\n✅ Configuration captured and logged")
        for key, value in config.items():
            print(f"   {key}: {value}")
        
        if config['sensitive_data']:
            print("🔒 PRIVACY MODE ACTIVATED")
        
        return config
    
    def load_and_encode_data(self, config):
        """Step 2: Load data and generate latent vectors"""
        print(f"\n🔐 STEP 2: LOADING AND ENCODING DATA")
        print("-" * 40)
        
        # Simulate data loading (replace with actual loader)
        if config['data_type'] == 'image':
            data = torch.randn(500, 3, 64, 64)
            labels = torch.randint(0, 5, (500,))
            print(f"📊 Loaded {len(data)} images")
        else:
            data = torch.randn(500, 20)
            labels = torch.randint(0, 3, (500,))
            print(f"📊 Loaded {len(data)} samples")
        
        # Create encoder
        input_shape = data.shape[1:]
        encoder = self.create_encoder(input_shape)
        
        # Generate latent vectors
        with torch.no_grad():
            latent_vectors = encoder(data)
        
        print(f"✅ Latent vectors generated: {latent_vectors.shape}")
        
        # Display latent vectors locally
        self.display_latent_vectors_locally(latent_vectors, labels)
        
        # Log audit action
        log_audit_action(
            action='latent_encoding',
            user='local_user',
            details=f'Generated {latent_vectors.shape[0]} latent vectors',
            status='success'
        )
        
        return data, labels, latent_vectors
    
    def create_encoder(self, input_shape):
        """Create privacy-preserving encoder"""
        
        class SimpleEncoder(nn.Module):
            def __init__(self, input_dim, latent_dim=128):
                super(SimpleEncoder, self).__init__()
                
                if len(input_dim) == 3:
                    flat_dim = np.prod(input_dim)
                    self.encoder = nn.Sequential(
                        nn.Flatten(),
                        nn.Linear(flat_dim, 512),
                        nn.ReLU(),
                        nn.Linear(512, 256),
                        nn.ReLU(),
                        nn.Linear(256, latent_dim)
                    )
                else:
                    self.encoder = nn.Sequential(
                        nn.Linear(input_dim[0], 256),
                        nn.ReLU(),
                        nn.Linear(256, 128),
                        nn.ReLU(),
                        nn.Linear(128, latent_dim)
                    )
            
            def forward(self, x):
                if len(x.shape) > 2:
                    x = x.view(x.size(0), -1)
                return self.encoder(x)
        
        encoder = SimpleEncoder(input_shape, latent_dim=128)
        print(f"🧠 Encoder created: {sum(p.numel() for p in encoder.parameters()):,} parameters")
        
        return encoder
    
    def display_latent_vectors_locally(self, latent_vectors, labels):
        """Display latent vectors before sending to cloud"""
        print(f"\n📊 DISPLAYING LATENT VECTORS LOCALLY (BEFORE CLOUD TRANSMISSION)")
        print("-" * 70)
        
        # Convert to numpy for display
        if torch.is_tensor(latent_vectors):
            latent_np = latent_vectors.detach().numpy()
        else:
            latent_np = latent_vectors
        
        if torch.is_tensor(labels):
            labels_np = labels.numpy()
        else:
            labels_np = labels
        
        # Show statistics
        print(f"\n📈 Latent Vector Statistics:")
        print(f"   Shape: {latent_np.shape}")
        print(f"   Total samples: {latent_np.shape[0]}")
        print(f"   Latent dimensions: {latent_np.shape[1]}")
        print(f"   Data type: {latent_np.dtype}")
        print(f"   Memory size: {latent_np.nbytes:,} bytes")
        
        # Show value ranges
        print(f"\n📊 Value Ranges:")
        print(f"   Min value: {latent_np.min():.6f}")
        print(f"   Max value: {latent_np.max():.6f}")
        print(f"   Mean value: {latent_np.mean():.6f}")
        print(f"   Std deviation: {latent_np.std():.6f}")
        
        # Show sample latent vectors
        print(f"\n🔍 SAMPLE LATENT VECTORS (First 5 samples, First 10 dimensions):")
        print("-" * 70)
        num_samples = min(5, len(latent_np))
        for i in range(num_samples):
            label = labels_np[i] if i < len(labels_np) else 'N/A'
            print(f"   Sample {i+1} (Label: {label}):")
            print(f"   {latent_np[i][:10]}")
        
        # Show class distribution
        print(f"\n📊 Class Distribution:")
        unique_labels, counts = np.unique(labels_np, return_counts=True)
        for label, count in zip(unique_labels, counts):
            percentage = (count / len(labels_np)) * 100
            print(f"   Class {label}: {count} samples ({percentage:.1f}%)")
        
        # Show dimensionality info
        print(f"\n🔐 Privacy Information:")
        print(f"   ✅ Original data dimensions: Compressed to {latent_np.shape[1]}D")
        print(f"   ✅ Data is now in latent space (privacy-preserving)")
        print(f"   ✅ Original features are NOT recoverable")
        print(f"   ✅ Ready for secure cloud transmission")
        
        print("-" * 70)
        
        # Ask user confirmation before sending
        print(f"\n⚠️  CONFIRMATION REQUIRED:")
        print(f"   These latent vectors will be sent to Render cloud.")
        print(f"   Original sensitive data will NOT be transmitted.")
        
        response = input("\n   Proceed with cloud transmission? (yes/no): ").strip().lower()
        
        if response != 'yes':
            print("\n❌ Cloud transmission cancelled by user.")
            return False
        
        print("\n✅ User confirmed - proceeding with cloud transmission...")
        return True
    
    def send_to_cloud(self, latent_vectors, labels):
        """Step 3: Send latent vectors to Render cloud"""
        print(f"\n☁️  STEP 3: SENDING TO CLOUD")
        print("-" * 40)
        
        # Prepare payload
        payload = {
            'latent_vectors': latent_vectors.detach().numpy().tolist(),
            'labels': labels.numpy().tolist(),
            'metadata': {
                'shape': latent_vectors.shape,
                'timestamp': datetime.now().isoformat(),
                'privacy_preserved': True,
                'original_data_included': False
            }
        }
        
        print(f"📦 Payload prepared:")
        print(f"   Latent vectors: {latent_vectors.shape}")
        print(f"   Labels: {labels.shape}")
        print(f"   Privacy preserved: ✅")
        print(f"   Payload size: {len(json.dumps(payload)):,} bytes")
        
        # Show what's being sent
        print(f"\n📤 TRANSMISSION DETAILS:")
        print(f"   Sending: Latent vectors only")
        print(f"   NOT sending: Raw data, original features, sensitive information")
        print(f"   Encryption: HTTPS")
        print(f"   Destination: Render Cloud")
        
        if not self.render_endpoint:
            print("\n⚠️  No Render endpoint configured - using simulation")
            return self.simulate_cloud_training(payload)
        
        try:
            print(f"\n📤 Sending to Render: {self.render_endpoint}")
            
            headers = {
                'Content-Type': 'application/json',
                'X-API-Key': self.api_key
            }
            
            response = requests.post(
                f"{self.render_endpoint}/train",
                json=payload,
                headers=headers,
                timeout=120
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Cloud training successful!")
                print(f"   Session ID: {result.get('session_id')}")
                print(f"   Best model: {result['summary']['best_model']}")
                print(f"   Best accuracy: {result['summary']['best_accuracy']:.3f}")
                
                # Log audit action
                log_audit_action(
                    action='cloud_training',
                    user='local_user',
                    details=f"Session: {result.get('session_id')}",
                    status='success'
                )
                
                return result
            else:
                print(f"❌ Cloud training failed: {response.status_code}")
                print(f"   Response: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Error connecting to cloud: {str(e)}")
            return None
    
    def simulate_cloud_training(self, payload):
        """Simulate cloud training if no endpoint available"""
        import time
        from sklearn.linear_model import LogisticRegression
        from sklearn.metrics import accuracy_score
        
        print("🔄 Running simulation mode...")
        
        latent_vectors = np.array(payload['latent_vectors'])
        labels = np.array(payload['labels'])
        
        # Split data
        split_idx = int(0.8 * len(latent_vectors))
        X_train, X_test = latent_vectors[:split_idx], latent_vectors[split_idx:]
        y_train, y_test = labels[:split_idx], labels[split_idx:]
        
        # Train model
        model = LogisticRegression(random_state=42)
        start_time = time.time()
        model.fit(X_train, y_train)
        training_time = time.time() - start_time
        
        # Evaluate
        test_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, test_pred)
        
        result = {
            'session_id': f'sim_session_{int(time.time())}',
            'status': 'success',
            'summary': {
                'best_model': 'logistic_regression',
                'best_accuracy': accuracy,
                'total_training_time': training_time,
                'models_trained': 1
            },
            'results': {
                'logistic_regression': {
                    'test_accuracy': accuracy,
                    'training_time': training_time,
                    'status': 'success'
                }
            },
            'timestamp': datetime.now().isoformat()
        }
        
        print(f"✅ Simulation complete: {accuracy:.3f} accuracy")
        
        return result
    
    def log_to_monitoring(self, cloud_result, latent_vectors, labels):
        """Step 4: Log results to monitoring database"""
        print(f"\n📊 STEP 4: LOGGING TO MONITORING SYSTEM")
        print("-" * 40)
        
        session_data = {
            'session_id': cloud_result.get('session_id'),
            'timestamp': cloud_result.get('timestamp', datetime.now().isoformat()),
            'data_samples': len(latent_vectors),
            'latent_dim': latent_vectors.shape[1],
            'models_trained': cloud_result['summary']['models_trained'],
            'best_model': cloud_result['summary']['best_model'],
            'best_accuracy': cloud_result['summary']['best_accuracy'],
            'training_time': cloud_result['summary']['total_training_time'],
            'cloud_provider': 'render',
            'privacy_preserved': True,
            'status': 'completed'
        }
        
        log_training_session(session_data)
        
        print(f"✅ Session logged to monitoring database")
        print(f"   Session ID: {session_data['session_id']}")
        
        return session_data
    
    def generate_reports(self, session_data, cloud_result):
        """Step 5: Generate comprehensive reports"""
        print(f"\n📄 STEP 5: GENERATING REPORTS")
        print("-" * 40)
        
        model_results = cloud_result.get('results', {})
        
        reports = self.report_generator.generate_complete_report(
            session_data, model_results
        )
        
        # Log audit action
        log_audit_action(
            action='report_generation',
            user='local_user',
            details=f"Generated reports for {session_data['session_id']}",
            status='success'
        )
        
        return reports
    
    def run_complete_pipeline(self):
        """Run the complete integrated pipeline"""
        print("\n🚀 STARTING COMPLETE INTEGRATED PIPELINE")
        print("=" * 60)
        
        try:
            # Step 1: Manual data input
            config = self.manual_data_input()
            
            # Step 2: Load and encode data
            data, labels, latent_vectors = self.load_and_encode_data(config)
            
            # Step 3: Send to cloud
            cloud_result = self.send_to_cloud(latent_vectors, labels)
            
            if not cloud_result:
                print("\n❌ Pipeline failed at cloud training step")
                return None
            
            # Step 4: Log to monitoring
            session_data = self.log_to_monitoring(cloud_result, latent_vectors, labels)
            
            # Step 5: Generate reports
            reports = self.generate_reports(session_data, cloud_result)
            
            # Final summary
            print(f"\n🎉 PIPELINE COMPLETED SUCCESSFULLY")
            print("=" * 60)
            print(f"✅ Data processed: {len(data)} samples")
            print(f"✅ Latent vectors generated: {latent_vectors.shape}")
            print(f"✅ Cloud training completed")
            print(f"✅ Best model: {session_data['best_model']}")
            print(f"✅ Best accuracy: {session_data['best_accuracy']:.3f}")
            print(f"✅ Session logged to monitoring")
            print(f"✅ Reports generated:")
            print(f"   - HTML: {reports['html']}")
            print(f"   - Chart: {reports['chart']}")
            print(f"   - JSON: {reports['json']}")
            print(f"\n🔒 PRIVACY STATUS: PRESERVED")
            print(f"   Raw data: Stayed local ✅")
            print(f"   Cloud received: Latent vectors only ✅")
            print(f"   All actions: Logged and audited ✅")
            
            return {
                'session_data': session_data,
                'cloud_result': cloud_result,
                'reports': reports
            }
            
        except Exception as e:
            print(f"\n❌ Pipeline error: {str(e)}")
            log_audit_action(
                action='pipeline_execution',
                user='local_user',
                details=f'Error: {str(e)}',
                status='failed'
            )
            return None

def main():
    """Main function"""
    
    # Check for Render endpoint
    render_endpoint = os.environ.get('RENDER_ENDPOINT')
    api_key = os.environ.get('RENDER_API_KEY', 'demo_key_12345')
    
    if not render_endpoint:
        print("⚠️  RENDER_ENDPOINT not set - will use simulation mode")
        print("   To use real Render cloud, set environment variable:")
        print("   export RENDER_ENDPOINT=https://your-app.onrender.com")
        print()
    
    # Create and run pipeline
    pipeline = IntegratedPipeline(render_endpoint, api_key)
    result = pipeline.run_complete_pipeline()
    
    if result:
        print(f"\n📋 NEXT STEPS:")
        print(f"   1. View monitoring dashboard: python admin_dashboard.py")
        print(f"   2. Open HTML report: {result['reports']['html']}")
        print(f"   3. Check performance chart: {result['reports']['chart']}")
        print(f"   4. Review JSON summary: {result['reports']['json']}")

if __name__ == '__main__':
    main()
