#!/usr/bin/env python3
"""
AI Agent - Main Entry Point
A comprehensive AI agent capable of handling website creation, application development,
analysis, planning, and management tasks across platforms.
"""

import os
import sys
import json
import logging
from datetime import datetime
from typing import Dict, Any, Optional
from flask import Flask, request, jsonify
from flask_cors import CORS

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from modules.orchestration import OrchestrationLayer
from modules.task_management import TaskManager
from modules.planning_analysis import PlanningAnalysisModule
from modules.dev_creation import DevelopmentCreationModule
from modules.deploy_management import DeploymentManagementModule
from modules.version_control import VersionControlModule
from utils.logging import setup_logging

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Global variables
orchestrator = None
logger = None

def initialize_agent():
    """Initialize the AI agent with all its components."""
    global orchestrator, logger
    
    # Setup logging
    logger = setup_logging()
    logger.info("Initializing AI Agent...")
    
    # Initialize modules
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
    
    logger.info("AI Agent initialized successfully!")

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'agent_status': 'running' if orchestrator else 'not_initialized'
    })

@app.route('/api/tasks', methods=['POST'])
def create_task():
    """Create a new task for the AI agent to execute."""
    try:
        data = request.get_json()
        
        if not data or 'description' not in data:
            return jsonify({'error': 'Task description is required'}), 400
        
        task_id = orchestrator.create_task(
            description=data['description'],
            task_type=data.get('type', 'general'),
            priority=data.get('priority', 'medium'),
            metadata=data.get('metadata', {})
        )
        
        logger.info(f"Created new task: {task_id}")
        
        return jsonify({
            'task_id': task_id,
            'status': 'created',
            'message': 'Task created successfully'
        }), 201
        
    except Exception as e:
        logger.error(f"Error creating task: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/tasks/<task_id>', methods=['GET'])
def get_task_status(task_id):
    """Get the status of a specific task."""
    try:
        task_info = orchestrator.get_task_status(task_id)
        
        if not task_info:
            return jsonify({'error': 'Task not found'}), 404
        
        return jsonify(task_info)
        
    except Exception as e:
        logger.error(f"Error getting task status: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/tasks', methods=['GET'])
def list_tasks():
    """List all tasks with their current status."""
    try:
        tasks = orchestrator.list_tasks()
        return jsonify({'tasks': tasks})
        
    except Exception as e:
        logger.error(f"Error listing tasks: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/tasks/<task_id>/execute', methods=['POST'])
def execute_task(task_id):
    """Execute a specific task."""
    try:
        result = orchestrator.execute_task(task_id)
        
        return jsonify({
            'task_id': task_id,
            'status': 'executed',
            'result': result
        })
        
    except Exception as e:
        logger.error(f"Error executing task {task_id}: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/tasks/<task_id>/logs', methods=['GET'])
def get_task_logs(task_id):
    """Get logs for a specific task."""
    try:
        logs = orchestrator.get_task_logs(task_id)
        
        if logs is None:
            return jsonify({'error': 'Task not found'}), 404
        
        return jsonify({'logs': logs})
        
    except Exception as e:
        logger.error(f"Error getting task logs: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/capabilities', methods=['GET'])
def get_capabilities():
    """Get the list of available capabilities."""
    capabilities = {
        'website_creation': {
            'description': 'Create responsive websites using modern frameworks',
            'frameworks': ['React', 'HTML/CSS/JS', 'Static Sites']
        },
        'application_development': {
            'description': 'Develop web applications and APIs',
            'frameworks': ['Flask', 'FastAPI', 'Node.js']
        },
        'data_analysis': {
            'description': 'Analyze data and generate insights',
            'tools': ['Python', 'Pandas', 'Matplotlib', 'Plotly']
        },
        'planning_management': {
            'description': 'Project planning and task management',
            'features': ['Task breakdown', 'Timeline planning', 'Resource allocation']
        },
        'deployment': {
            'description': 'Deploy applications to various platforms',
            'platforms': ['Cloud platforms', 'Static hosting', 'Container deployment']
        }
    }
    
    return jsonify({'capabilities': capabilities})

if __name__ == '__main__':
    # Initialize the agent
    initialize_agent()
    
    # Start the Flask server
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

