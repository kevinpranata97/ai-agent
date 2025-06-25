"""
Orchestration Layer - Central coordination for the AI Agent
Manages task flow, module coordination, and overall workflow execution.
"""

import uuid
import json
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional
from enum import Enum

class TaskStatus(Enum):
    CREATED = "created"
    PLANNING = "planning"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class TaskType(Enum):
    WEBSITE_CREATION = "website_creation"
    APP_DEVELOPMENT = "app_development"
    DATA_ANALYSIS = "data_analysis"
    PLANNING = "planning"
    DEPLOYMENT = "deployment"
    GENERAL = "general"

class OrchestrationLayer:
    """
    Central orchestration layer that coordinates all AI agent modules.
    """
    
    def __init__(self, task_manager, planning_module, dev_module, deploy_module, version_control):
        self.task_manager = task_manager
        self.planning_module = planning_module
        self.dev_module = dev_module
        self.deploy_module = deploy_module
        self.version_control = version_control
        self.logger = logging.getLogger(__name__)
        
        # Task registry
        self.tasks = {}
        
        self.logger.info("Orchestration layer initialized")
    
    def create_task(self, description: str, task_type: str = "general", 
                   priority: str = "medium", metadata: Dict[str, Any] = None) -> str:
        """
        Create a new task and add it to the task queue.
        
        Args:
            description: Natural language description of the task
            task_type: Type of task (website_creation, app_development, etc.)
            priority: Task priority (low, medium, high)
            metadata: Additional task metadata
            
        Returns:
            str: Unique task ID
        """
        task_id = str(uuid.uuid4())
        
        task_data = {
            'id': task_id,
            'description': description,
            'type': task_type,
            'priority': priority,
            'status': TaskStatus.CREATED.value,
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat(),
            'metadata': metadata or {},
            'logs': [],
            'progress': 0,
            'result': None,
            'error': None
        }
        
        # Store task
        self.tasks[task_id] = task_data
        
        # Add to task manager queue
        self.task_manager.add_task(task_data)
        
        self.logger.info(f"Created task {task_id}: {description}")
        
        return task_id
    
    def execute_task(self, task_id: str) -> Dict[str, Any]:
        """
        Execute a specific task through the orchestration workflow.
        
        Args:
            task_id: Unique task identifier
            
        Returns:
            Dict containing execution result
        """
        if task_id not in self.tasks:
            raise ValueError(f"Task {task_id} not found")
        
        task = self.tasks[task_id]
        
        try:
            self._update_task_status(task_id, TaskStatus.PLANNING)
            
            # Step 1: Planning and Analysis
            self._log_task(task_id, "Starting planning and analysis phase")
            plan = self.planning_module.analyze_and_plan(task)
            task['plan'] = plan
            
            # Step 2: Determine execution path based on task type
            task_type = TaskType(task['type'])
            
            if task_type in [TaskType.WEBSITE_CREATION, TaskType.APP_DEVELOPMENT]:
                result = self._execute_development_task(task_id, task)
            elif task_type == TaskType.DATA_ANALYSIS:
                result = self._execute_analysis_task(task_id, task)
            elif task_type == TaskType.DEPLOYMENT:
                result = self._execute_deployment_task(task_id, task)
            else:
                result = self._execute_general_task(task_id, task)
            
            # Step 3: Version control integration
            self._log_task(task_id, "Committing changes to version control")
            self.version_control.commit_task_changes(task_id, task)
            
            self._update_task_status(task_id, TaskStatus.COMPLETED)
            task['result'] = result
            
            self.logger.info(f"Task {task_id} completed successfully")
            
            return result
            
        except Exception as e:
            self._update_task_status(task_id, TaskStatus.FAILED)
            task['error'] = str(e)
            self._log_task(task_id, f"Task failed: {str(e)}")
            self.logger.error(f"Task {task_id} failed: {str(e)}")
            raise
    
    def _execute_development_task(self, task_id: str, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute website creation or application development task."""
        self._update_task_status(task_id, TaskStatus.IN_PROGRESS)
        self._log_task(task_id, "Starting development phase")
        
        # Create the website/application
        dev_result = self.dev_module.create_project(task)
        
        # Update progress
        self._update_task_progress(task_id, 80)
        
        # Deploy if requested
        if task.get('metadata', {}).get('deploy', False):
            self._log_task(task_id, "Deploying project")
            deploy_result = self.deploy_module.deploy_project(dev_result['project_path'])
            dev_result['deployment'] = deploy_result
        
        self._update_task_progress(task_id, 100)
        
        return dev_result
    
    def _execute_analysis_task(self, task_id: str, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute data analysis task."""
        self._update_task_status(task_id, TaskStatus.IN_PROGRESS)
        self._log_task(task_id, "Starting analysis phase")
        
        # Perform analysis
        analysis_result = self.planning_module.perform_analysis(task)
        
        self._update_task_progress(task_id, 100)
        
        return analysis_result
    
    def _execute_deployment_task(self, task_id: str, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute deployment task."""
        self._update_task_status(task_id, TaskStatus.IN_PROGRESS)
        self._log_task(task_id, "Starting deployment phase")
        
        project_path = task.get('metadata', {}).get('project_path')
        if not project_path:
            raise ValueError("Project path required for deployment task")
        
        deploy_result = self.deploy_module.deploy_project(project_path)
        
        self._update_task_progress(task_id, 100)
        
        return deploy_result
    
    def _execute_general_task(self, task_id: str, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute general task."""
        self._update_task_status(task_id, TaskStatus.IN_PROGRESS)
        self._log_task(task_id, "Processing general task")
        
        # For general tasks, use planning module to determine best approach
        result = self.planning_module.execute_general_task(task)
        
        self._update_task_progress(task_id, 100)
        
        return result
    
    def get_task_status(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get current status of a task."""
        return self.tasks.get(task_id)
    
    def list_tasks(self) -> List[Dict[str, Any]]:
        """List all tasks."""
        return list(self.tasks.values())
    
    def get_task_logs(self, task_id: str) -> Optional[List[str]]:
        """Get logs for a specific task."""
        task = self.tasks.get(task_id)
        return task['logs'] if task else None
    
    def _update_task_status(self, task_id: str, status: TaskStatus):
        """Update task status."""
        if task_id in self.tasks:
            self.tasks[task_id]['status'] = status.value
            self.tasks[task_id]['updated_at'] = datetime.now().isoformat()
    
    def _update_task_progress(self, task_id: str, progress: int):
        """Update task progress percentage."""
        if task_id in self.tasks:
            self.tasks[task_id]['progress'] = progress
            self.tasks[task_id]['updated_at'] = datetime.now().isoformat()
    
    def _log_task(self, task_id: str, message: str):
        """Add a log entry to a task."""
        if task_id in self.tasks:
            log_entry = f"[{datetime.now().isoformat()}] {message}"
            self.tasks[task_id]['logs'].append(log_entry)
            self.logger.info(f"Task {task_id}: {message}")

