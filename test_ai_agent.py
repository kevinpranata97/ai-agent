#!/usr/bin/env python3
"""
AI Agent Test Suite
Tests the core functionality of the AI agent modules.
"""

import sys
import os
import json
from datetime import datetime

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Test that all modules can be imported successfully."""
    print("Testing module imports...")
    
    try:
        from modules.task_management import TaskManager
        from modules.planning_analysis import PlanningAnalysisModule
        from modules.dev_creation import DevelopmentCreationModule
        from modules.deploy_management import DeploymentManagementModule
        from modules.version_control import VersionControlModule
        from modules.orchestration import OrchestrationLayer
        from utils.logging import setup_logging
        print("✓ All modules imported successfully")
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def test_task_manager():
    """Test the TaskManager functionality."""
    print("\nTesting TaskManager...")
    
    try:
        from modules.task_management import TaskManager
        
        # Initialize task manager
        task_manager = TaskManager()
        
        # Create a test task
        task_data = {
            'id': 'test-001',
            'description': 'Test task for validation',
            'type': 'general',
            'priority': 'medium',
            'created_at': datetime.now().isoformat(),
            'metadata': {'test': True}
        }
        
        # Add task
        task_id = task_manager.add_task(task_data)
        
        # Get statistics
        stats = task_manager.get_task_statistics()
        
        print(f"✓ Task created with ID: {task_id}")
        print(f"✓ Task statistics: {stats}")
        
        # Cleanup
        task_manager.shutdown()
        
        return True
    except Exception as e:
        print(f"✗ TaskManager test failed: {e}")
        return False

def test_planning_module():
    """Test the PlanningAnalysisModule functionality."""
    print("\nTesting PlanningAnalysisModule...")
    
    try:
        from modules.planning_analysis import PlanningAnalysisModule
        
        # Initialize planning module
        planning_module = PlanningAnalysisModule()
        
        # Create a test task
        test_task = {
            'id': 'test-002',
            'description': 'Create a simple website with contact form',
            'type': 'website_creation',
            'priority': 'medium'
        }
        
        # Analyze and plan
        plan = planning_module.analyze_and_plan(test_task)
        
        print(f"✓ Plan created with {len(plan['execution_plan']['steps'])} steps")
        print(f"✓ Technology stack: {plan['technology_stack']}")
        print(f"✓ Estimated time: {plan['resource_estimate']['estimated_time_minutes']} minutes")
        
        return True
    except Exception as e:
        print(f"✗ PlanningAnalysisModule test failed: {e}")
        return False

def test_development_module():
    """Test the DevelopmentCreationModule functionality."""
    print("\nTesting DevelopmentCreationModule...")
    
    try:
        from modules.dev_creation import DevelopmentCreationModule
        
        # Initialize development module
        dev_module = DevelopmentCreationModule()
        
        # Create a test task
        test_task = {
            'id': 'test-003',
            'description': 'Create a static website',
            'type': 'website_creation',
            'metadata': {'title': 'Test Website'}
        }
        
        # Determine project type
        project_type = dev_module._determine_project_type(test_task)
        
        print(f"✓ Project type determined: {project_type}")
        
        return True
    except Exception as e:
        print(f"✗ DevelopmentCreationModule test failed: {e}")
        return False

def test_deployment_module():
    """Test the DeploymentManagementModule functionality."""
    print("\nTesting DeploymentManagementModule...")
    
    try:
        from modules.deploy_management import DeploymentManagementModule
        
        # Initialize deployment module
        deploy_module = DeploymentManagementModule()
        
        # Test project type detection
        test_path = "/tmp/test_project"
        os.makedirs(test_path, exist_ok=True)
        
        # Create a test HTML file
        with open(os.path.join(test_path, "index.html"), "w") as f:
            f.write("<html><body>Test</body></html>")
        
        project_type = deploy_module._detect_project_type(test_path)
        
        print(f"✓ Project type detected: {project_type}")
        
        # Cleanup
        os.remove(os.path.join(test_path, "index.html"))
        os.rmdir(test_path)
        
        return True
    except Exception as e:
        print(f"✗ DeploymentManagementModule test failed: {e}")
        return False

def test_version_control_module():
    """Test the VersionControlModule functionality."""
    print("\nTesting VersionControlModule...")
    
    try:
        from modules.version_control import VersionControlModule
        
        # Initialize version control module
        vc_module = VersionControlModule()
        
        # Get repository status
        status = vc_module.get_repository_status()
        
        print(f"✓ Repository status: {status['status']}")
        if status['status'] == 'initialized':
            print(f"✓ Current branch: {status['current_branch']}")
        
        return True
    except Exception as e:
        print(f"✗ VersionControlModule test failed: {e}")
        return False

def test_orchestration():
    """Test the OrchestrationLayer functionality."""
    print("\nTesting OrchestrationLayer...")
    
    try:
        from modules.orchestration import OrchestrationLayer
        from modules.task_management import TaskManager
        from modules.planning_analysis import PlanningAnalysisModule
        from modules.dev_creation import DevelopmentCreationModule
        from modules.deploy_management import DeploymentManagementModule
        from modules.version_control import VersionControlModule
        
        # Initialize all modules
        task_manager = TaskManager()
        planning_module = PlanningAnalysisModule()
        dev_module = DevelopmentCreationModule()
        deploy_module = DeploymentManagementModule()
        version_control = VersionControlModule()
        
        # Initialize orchestration layer
        orchestrator = OrchestrationLayer(
            task_manager=task_manager,
            planning_module=planning_module,
            dev_module=dev_module,
            deploy_module=deploy_module,
            version_control=version_control
        )
        
        # Create a test task
        task_id = orchestrator.create_task(
            description="Test orchestration functionality",
            task_type="general",
            priority="low"
        )
        
        # Get task status
        task_status = orchestrator.get_task_status(task_id)
        
        print(f"✓ Task created with orchestrator: {task_id}")
        print(f"✓ Task status: {task_status['status']}")
        
        # Cleanup
        task_manager.shutdown()
        
        return True
    except Exception as e:
        print(f"✗ OrchestrationLayer test failed: {e}")
        return False

def run_all_tests():
    """Run all tests and return overall result."""
    print("=" * 50)
    print("AI AGENT VALIDATION TEST SUITE")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_task_manager,
        test_planning_module,
        test_development_module,
        test_deployment_module,
        test_version_control_module,
        test_orchestration
    ]
    
    results = []
    
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"✗ Test {test.__name__} failed with exception: {e}")
            results.append(False)
    
    print("\n" + "=" * 50)
    print("TEST RESULTS SUMMARY")
    print("=" * 50)
    
    passed = sum(results)
    total = len(results)
    
    print(f"Tests passed: {passed}/{total}")
    print(f"Success rate: {(passed/total)*100:.1f}%")
    
    if passed == total:
        print("🎉 All tests passed! AI Agent is ready for use.")
        return True
    else:
        print("⚠️  Some tests failed. Please review the issues above.")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)

