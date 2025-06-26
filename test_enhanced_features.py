#!/usr/bin/env python3
"""
Comprehensive Test Validation Script for Enhanced AI Agent
Tests the new LLM fine-tuning and application testing features.
"""

import os
import sys
import json
import time
import requests
import subprocess
from datetime import datetime

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_backend_health():
    """Test if the backend is running and healthy."""
    print("🔍 Testing backend health...")
    try:
        response = requests.get('http://localhost:5001/health', timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Backend is healthy (version {data.get('version', 'unknown')})")
            print(f"   Modules: {data.get('modules', {})}")
            return True
        else:
            print(f"❌ Backend health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Backend health check failed: {e}")
        return False

def test_capabilities_endpoint():
    """Test the capabilities endpoint."""
    print("\n🔍 Testing capabilities endpoint...")
    try:
        response = requests.get('http://localhost:5001/api/capabilities', timeout=5)
        if response.status_code == 200:
            data = response.json()
            
            # Check for new capabilities
            required_capabilities = ['llm_finetuning', 'app_testing']
            for capability in required_capabilities:
                if capability in data:
                    print(f"✅ {capability} capability found")
                else:
                    print(f"❌ {capability} capability missing")
                    return False
            
            # Check LLM fine-tuning features
            llm_features = data.get('llm_finetuning', {}).get('features', [])
            if 'Custom Training' in llm_features:
                print("✅ LLM fine-tuning features properly configured")
            else:
                print("❌ LLM fine-tuning features missing")
                return False
            
            # Check app testing features
            testing_types = data.get('app_testing', {}).get('types', [])
            if 'Unit Tests' in testing_types and 'Integration Tests' in testing_types:
                print("✅ Application testing features properly configured")
            else:
                print("❌ Application testing features missing")
                return False
            
            return True
        else:
            print(f"❌ Capabilities endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Capabilities endpoint failed: {e}")
        return False

def test_application_testing_module():
    """Test the application testing module."""
    print("\n🔍 Testing application testing module...")
    try:
        # Import the module
        from modules.app_testing import ApplicationTestingModule
        
        # Initialize the module
        testing_module = ApplicationTestingModule()
        print("✅ Application testing module imported and initialized")
        
        # Test project analysis
        current_dir = os.path.dirname(os.path.abspath(__file__))
        analysis = testing_module.analyze_project_structure(current_dir)
        
        if analysis and 'project_type' in analysis:
            print(f"✅ Project analysis successful: {analysis['project_type']}")
            print(f"   Languages: {analysis.get('languages', [])}")
            print(f"   Frameworks: {analysis.get('frameworks', [])}")
            print(f"   Has tests: {analysis.get('has_tests', False)}")
        else:
            print("❌ Project analysis failed")
            return False
        
        return True
    except Exception as e:
        print(f"❌ Application testing module test failed: {e}")
        return False

def test_llm_finetuning_module():
    """Test the LLM fine-tuning module (without API key)."""
    print("\n🔍 Testing LLM fine-tuning module...")
    try:
        # Test module import
        from modules.llm_finetuning import LLMFineTuningModule
        print("✅ LLM fine-tuning module imported successfully")
        
        # Test initialization without API key (should fail gracefully)
        try:
            finetuning_module = LLMFineTuningModule()
            print("❌ LLM fine-tuning module should fail without API key")
            return False
        except ValueError as e:
            if "API key is required" in str(e):
                print("✅ LLM fine-tuning module properly validates API key requirement")
            else:
                print(f"❌ Unexpected error: {e}")
                return False
        
        # Test data preparation functionality
        sample_data = [
            {
                "messages": [
                    {"role": "user", "content": "Hello"},
                    {"role": "assistant", "content": "Hi there!"}
                ]
            }
        ]
        
        # Create a temporary file for testing
        temp_file = "/tmp/test_training_data.jsonl"
        
        # Test with a mock API key
        os.environ['OPENAI_API_KEY'] = 'test-key-for-validation'
        try:
            finetuning_module = LLMFineTuningModule()
            prepared_file = finetuning_module.prepare_training_data(sample_data, temp_file)
            
            if os.path.exists(prepared_file):
                print("✅ Training data preparation successful")
                
                # Test validation
                validation = finetuning_module.validate_training_data(prepared_file)
                if validation and 'valid' in validation:
                    print(f"✅ Training data validation successful: {validation['valid']}")
                else:
                    print("❌ Training data validation failed")
                    return False
                
                # Clean up
                os.remove(prepared_file)
            else:
                print("❌ Training data preparation failed")
                return False
        finally:
            # Remove the test API key
            if 'OPENAI_API_KEY' in os.environ:
                del os.environ['OPENAI_API_KEY']
        
        return True
    except Exception as e:
        print(f"❌ LLM fine-tuning module test failed: {e}")
        return False

def test_api_endpoints():
    """Test the new API endpoints."""
    print("\n🔍 Testing new API endpoints...")
    
    # Test application testing analyze endpoint
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        payload = {"project_path": current_dir}
        response = requests.post(
            'http://localhost:5001/api/testing/analyze',
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            if 'project_type' in data:
                print("✅ Application testing analyze endpoint working")
            else:
                print("❌ Application testing analyze endpoint returned invalid data")
                return False
        else:
            print(f"❌ Application testing analyze endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Application testing analyze endpoint failed: {e}")
        return False
    
    # Test LLM fine-tuning jobs endpoint (should work even without API key)
    try:
        response = requests.get('http://localhost:5001/api/llm/fine-tuning/jobs', timeout=5)
        if response.status_code in [200, 503]:  # 503 expected without API key
            print("✅ LLM fine-tuning jobs endpoint accessible")
        else:
            print(f"❌ LLM fine-tuning jobs endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ LLM fine-tuning jobs endpoint failed: {e}")
        return False
    
    return True

def test_dashboard_accessibility():
    """Test if the React dashboard is accessible."""
    print("\n🔍 Testing React dashboard accessibility...")
    try:
        response = requests.get('http://localhost:5173', timeout=5)
        if response.status_code == 200:
            print("✅ React dashboard is accessible")
            return True
        else:
            print(f"❌ React dashboard failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ React dashboard failed: {e}")
        return False

def test_git_integration():
    """Test Git integration and repository status."""
    print("\n🔍 Testing Git integration...")
    try:
        # Check if we're in a Git repository
        result = subprocess.run(['git', 'status'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Git repository status accessible")
            
            # Check for recent commits
            result = subprocess.run(['git', 'log', '--oneline', '-5'], capture_output=True, text=True)
            if result.returncode == 0 and result.stdout:
                commits = result.stdout.strip().split('\n')
                print(f"✅ Recent commits found: {len(commits)}")
                
                # Check for our new features in recent commits
                recent_commit = commits[0] if commits else ""
                if any(keyword in recent_commit.lower() for keyword in ['fine-tuning', 'testing', 'llm']):
                    print("✅ Recent commits include new features")
                else:
                    print("⚠️  Recent commits may not include new features")
            else:
                print("❌ Could not retrieve Git log")
                return False
        else:
            print("❌ Not in a Git repository or Git not accessible")
            return False
        
        return True
    except Exception as e:
        print(f"❌ Git integration test failed: {e}")
        return False

def run_comprehensive_validation():
    """Run all validation tests."""
    print("🚀 Starting Comprehensive Validation of Enhanced AI Agent")
    print("=" * 60)
    
    tests = [
        ("Backend Health", test_backend_health),
        ("Capabilities Endpoint", test_capabilities_endpoint),
        ("Application Testing Module", test_application_testing_module),
        ("LLM Fine-tuning Module", test_llm_finetuning_module),
        ("API Endpoints", test_api_endpoints),
        ("Dashboard Accessibility", test_dashboard_accessibility),
        ("Git Integration", test_git_integration)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results[test_name] = False
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 VALIDATION SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:<30} {status}")
    
    print("-" * 60)
    print(f"Total Tests: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {total - passed}")
    print(f"Success Rate: {(passed/total)*100:.1f}%")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! Enhanced AI Agent is fully functional.")
        return True
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please review the issues above.")
        return False

if __name__ == "__main__":
    success = run_comprehensive_validation()
    sys.exit(0 if success else 1)

