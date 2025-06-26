#!/usr/bin/env python3
"""
AI Agent Main Application
Enhanced with LLM fine-tuning and application testing capabilities.
"""

import os
import sys
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import modules
from modules.orchestration import OrchestrationLayer
from modules.task_management import TaskManager
from modules.planning_analysis import PlanningAnalysisModule
from modules.dev_creation import DevelopmentCreationModule
from modules.deploy_management import DeploymentManagementModule
from modules.version_control import VersionControlModule
from modules.llm_finetuning import LLMFineTuningModule
from modules.app_testing import ApplicationTestingModule
from utils.logging import setup_logging

# Initialize logging
logger = setup_logging(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize modules
logger.info("Initializing AI Agent...")

task_manager = TaskManager()
planning_module = PlanningAnalysisModule()
dev_module = DevelopmentCreationModule()
deploy_module = DeploymentManagementModule()
version_control = VersionControlModule()

# Initialize new modules
try:
    llm_finetuning = LLMFineTuningModule()
    logger.info("LLM Fine-tuning module initialized")
except Exception as e:
    logger.warning(f"LLM Fine-tuning module initialization failed: {e}")
    llm_finetuning = None

app_testing = ApplicationTestingModule()

# Initialize orchestration layer
orchestrator = OrchestrationLayer(
    task_manager=task_manager,
    planning_module=planning_module,
    dev_module=dev_module,
    deploy_module=deploy_module,
    version_control=version_control
)

logger.info("AI Agent initialized successfully!")

# Health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '2.0.0',
        'modules': {
            'task_management': True,
            'planning_analysis': True,
            'dev_creation': True,
            'deploy_management': True,
            'version_control': True,
            'llm_finetuning': llm_finetuning is not None,
            'app_testing': True
        }
    })

# Task management endpoints
@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    """Get all tasks."""
    try:
        tasks = task_manager.get_all_tasks()
        return jsonify({'tasks': tasks})
    except Exception as e:
        logger.error(f"Failed to get tasks: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/tasks', methods=['POST'])
def create_task():
    """Create a new task."""
    try:
        data = request.get_json()
        task_id = orchestrator.create_task(
            description=data.get('description'),
            task_type=data.get('type', 'general'),
            priority=data.get('priority', 'medium')
        )
        return jsonify({'task_id': task_id, 'status': 'created'})
    except Exception as e:
        logger.error(f"Failed to create task: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/tasks/<task_id>', methods=['GET'])
def get_task(task_id):
    """Get task details."""
    try:
        task_status = orchestrator.get_task_status(task_id)
        return jsonify(task_status)
    except Exception as e:
        logger.error(f"Failed to get task {task_id}: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/tasks/<task_id>/execute', methods=['POST'])
def execute_task(task_id):
    """Execute a task."""
    try:
        result = orchestrator.execute_task(task_id)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Failed to execute task {task_id}: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/tasks/<task_id>/logs', methods=['GET'])
def get_task_logs(task_id):
    """Get task execution logs."""
    try:
        logs = task_manager.get_task_logs(task_id)
        return jsonify({'logs': logs})
    except Exception as e:
        logger.error(f"Failed to get logs for task {task_id}: {e}")
        return jsonify({'error': str(e)}), 500

# System information endpoints
@app.route('/api/capabilities', methods=['GET'])
def get_capabilities():
    """Get system capabilities."""
    capabilities = {
        'website_creation': {
            'frameworks': ['React', 'HTML/CSS/JS', 'Static Sites'],
            'features': ['Responsive Design', 'Modern UI', 'SEO Optimization']
        },
        'app_development': {
            'frameworks': ['Flask', 'FastAPI', 'Node.js'],
            'features': ['REST APIs', 'Database Integration', 'Authentication']
        },
        'data_analysis': {
            'tools': ['Python', 'Pandas', 'Plotly'],
            'features': ['Data Processing', 'Visualization', 'Reporting']
        },
        'llm_finetuning': {
            'available': llm_finetuning is not None,
            'models': ['gpt-3.5-turbo', 'gpt-4'] if llm_finetuning else [],
            'features': ['Custom Training', 'Model Testing', 'Performance Monitoring']
        },
        'app_testing': {
            'types': ['Unit Tests', 'Integration Tests', 'Performance Tests'],
            'frameworks': ['pytest', 'Jest', 'Custom Testing'],
            'features': ['Automated Testing', 'Test Reports', 'Coverage Analysis']
        }
    }
    return jsonify(capabilities)

# LLM Fine-tuning endpoints
@app.route('/api/llm/fine-tuning/jobs', methods=['GET'])
def get_finetuning_jobs():
    """Get all fine-tuning jobs."""
    if not llm_finetuning:
        return jsonify({'error': 'LLM fine-tuning not available'}), 503
    
    try:
        jobs = llm_finetuning.fine_tuning_jobs
        return jsonify({'jobs': jobs})
    except Exception as e:
        logger.error(f"Failed to get fine-tuning jobs: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/llm/fine-tuning/jobs', methods=['POST'])
def create_finetuning_job():
    """Create a new fine-tuning job."""
    if not llm_finetuning:
        return jsonify({'error': 'LLM fine-tuning not available'}), 503
    
    try:
        data = request.get_json()
        
        # Prepare training data
        training_data = data.get('training_data', [])
        output_file = f"tasks/finetuning_{int(datetime.now().timestamp())}.jsonl"
        
        prepared_file = llm_finetuning.prepare_training_data(
            training_data, 
            output_file,
            data.get('format_type', 'chat')
        )
        
        # Validate data
        validation = llm_finetuning.validate_training_data(prepared_file)
        if not validation['valid']:
            return jsonify({'error': 'Invalid training data', 'issues': validation['issues']}), 400
        
        # Upload file
        file_id = llm_finetuning.upload_training_file(prepared_file)
        
        # Create job
        job_id = llm_finetuning.create_fine_tuning_job(
            file_id,
            data.get('model', 'gpt-3.5-turbo'),
            data.get('hyperparameters'),
            data.get('suffix')
        )
        
        return jsonify({'job_id': job_id, 'file_id': file_id, 'status': 'created'})
        
    except Exception as e:
        logger.error(f"Failed to create fine-tuning job: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/llm/fine-tuning/jobs/<job_id>', methods=['GET'])
def get_finetuning_job_status(job_id):
    """Get fine-tuning job status."""
    if not llm_finetuning:
        return jsonify({'error': 'LLM fine-tuning not available'}), 503
    
    try:
        status = llm_finetuning.get_job_status(job_id)
        return jsonify(status)
    except Exception as e:
        logger.error(f"Failed to get job status: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/llm/fine-tuning/jobs/<job_id>/cancel', methods=['POST'])
def cancel_finetuning_job(job_id):
    """Cancel a fine-tuning job."""
    if not llm_finetuning:
        return jsonify({'error': 'LLM fine-tuning not available'}), 503
    
    try:
        success = llm_finetuning.cancel_job(job_id)
        return jsonify({'success': success})
    except Exception as e:
        logger.error(f"Failed to cancel job: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/llm/models', methods=['GET'])
def get_finetuned_models():
    """Get all fine-tuned models."""
    if not llm_finetuning:
        return jsonify({'error': 'LLM fine-tuning not available'}), 503
    
    try:
        models = llm_finetuning.list_fine_tuned_models()
        return jsonify({'models': models})
    except Exception as e:
        logger.error(f"Failed to get models: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/llm/models/<model_id>/test', methods=['POST'])
def test_finetuned_model(model_id):
    """Test a fine-tuned model."""
    if not llm_finetuning:
        return jsonify({'error': 'LLM fine-tuning not available'}), 503
    
    try:
        data = request.get_json()
        test_prompts = data.get('prompts', [])
        
        results = llm_finetuning.test_fine_tuned_model(model_id, test_prompts)
        return jsonify({'test_results': results})
    except Exception as e:
        logger.error(f"Failed to test model: {e}")
        return jsonify({'error': str(e)}), 500

# Application testing endpoints
@app.route('/api/testing/analyze', methods=['POST'])
def analyze_project():
    """Analyze a project for testing."""
    try:
        data = request.get_json()
        project_path = data.get('project_path')
        
        if not project_path or not os.path.exists(project_path):
            return jsonify({'error': 'Invalid project path'}), 400
        
        analysis = app_testing.analyze_project_structure(project_path)
        return jsonify(analysis)
    except Exception as e:
        logger.error(f"Failed to analyze project: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/testing/run', methods=['POST'])
def run_tests():
    """Run comprehensive tests on a project."""
    try:
        data = request.get_json()
        project_path = data.get('project_path')
        
        if not project_path or not os.path.exists(project_path):
            return jsonify({'error': 'Invalid project path'}), 400
        
        test_session_id = app_testing.run_comprehensive_test_suite(project_path)
        return jsonify({'test_session_id': test_session_id})
    except Exception as e:
        logger.error(f"Failed to run tests: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/testing/sessions/<session_id>', methods=['GET'])
def get_test_session(session_id):
    """Get test session results."""
    try:
        if session_id not in app_testing.test_sessions:
            return jsonify({'error': 'Test session not found'}), 404
        
        session_data = app_testing.test_sessions[session_id]
        return jsonify(session_data)
    except Exception as e:
        logger.error(f"Failed to get test session: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/testing/sessions/<session_id>/report', methods=['GET'])
def generate_test_report(session_id):
    """Generate a test report."""
    try:
        report_path = app_testing.generate_test_report(session_id)
        return jsonify({'report_path': report_path})
    except Exception as e:
        logger.error(f"Failed to generate test report: {e}")
        return jsonify({'error': str(e)}), 500

# Statistics endpoint
@app.route('/api/stats', methods=['GET'])
def get_statistics():
    """Get system statistics."""
    try:
        stats = {
            'tasks': task_manager.get_task_statistics(),
            'version_control': version_control.get_repository_status(),
            'timestamp': datetime.now().isoformat()
        }
        
        if llm_finetuning:
            stats['llm_finetuning'] = llm_finetuning.get_usage_statistics()
        
        return jsonify(stats)
    except Exception as e:
        logger.error(f"Failed to get statistics: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Ensure required directories exist
    os.makedirs('tasks', exist_ok=True)
    os.makedirs('logs', exist_ok=True)
    
    # Start the Flask application
    app.run(host='0.0.0.0', port=5000, debug=True)

