"""
Task Management Module
Handles task queuing, scheduling, prioritization, and lifecycle management.
"""

import json
import logging
import threading
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from queue import PriorityQueue
from dataclasses import dataclass, asdict
from enum import Enum

class Priority(Enum):
    LOW = 3
    MEDIUM = 2
    HIGH = 1

@dataclass
class Task:
    id: str
    description: str
    type: str
    priority: int
    created_at: str
    scheduled_at: Optional[str] = None
    metadata: Dict[str, Any] = None
    
    def __lt__(self, other):
        return self.priority < other.priority

class TaskManager:
    """
    Manages task lifecycle, queuing, and scheduling.
    """
    
    def __init__(self):
        self.task_queue = PriorityQueue()
        self.scheduled_tasks = {}
        self.active_tasks = {}
        self.completed_tasks = {}
        self.failed_tasks = {}
        self.logger = logging.getLogger(__name__)
        
        # Start scheduler thread
        self.scheduler_running = True
        self.scheduler_thread = threading.Thread(target=self._scheduler_loop, daemon=True)
        self.scheduler_thread.start()
        
        self.logger.info("Task Manager initialized")
    
    def add_task(self, task_data: Dict[str, Any]) -> str:
        """
        Add a new task to the queue.
        
        Args:
            task_data: Dictionary containing task information
            
        Returns:
            str: Task ID
        """
        # Convert priority string to enum value
        priority_map = {
            'low': Priority.LOW.value,
            'medium': Priority.MEDIUM.value,
            'high': Priority.HIGH.value
        }
        
        priority = priority_map.get(task_data.get('priority', 'medium'), Priority.MEDIUM.value)
        
        task = Task(
            id=task_data['id'],
            description=task_data['description'],
            type=task_data['type'],
            priority=priority,
            created_at=task_data['created_at'],
            scheduled_at=task_data.get('scheduled_at'),
            metadata=task_data.get('metadata', {})
        )
        
        if task.scheduled_at:
            # Schedule for later execution
            self.scheduled_tasks[task.id] = task
            self.logger.info(f"Scheduled task {task.id} for {task.scheduled_at}")
        else:
            # Add to immediate execution queue
            self.task_queue.put(task)
            self.logger.info(f"Added task {task.id} to queue with priority {priority}")
        
        return task.id
    
    def get_next_task(self) -> Optional[Task]:
        """
        Get the next task from the queue.
        
        Returns:
            Task object or None if queue is empty
        """
        if not self.task_queue.empty():
            task = self.task_queue.get()
            self.active_tasks[task.id] = task
            self.logger.info(f"Retrieved task {task.id} from queue")
            return task
        return None
    
    def complete_task(self, task_id: str, result: Dict[str, Any] = None):
        """
        Mark a task as completed.
        
        Args:
            task_id: Task identifier
            result: Task execution result
        """
        if task_id in self.active_tasks:
            task = self.active_tasks.pop(task_id)
            task.metadata['result'] = result
            task.metadata['completed_at'] = datetime.now().isoformat()
            self.completed_tasks[task_id] = task
            self.logger.info(f"Task {task_id} completed")
    
    def fail_task(self, task_id: str, error: str):
        """
        Mark a task as failed.
        
        Args:
            task_id: Task identifier
            error: Error message
        """
        if task_id in self.active_tasks:
            task = self.active_tasks.pop(task_id)
            task.metadata['error'] = error
            task.metadata['failed_at'] = datetime.now().isoformat()
            self.failed_tasks[task_id] = task
            self.logger.error(f"Task {task_id} failed: {error}")
    
    def schedule_task(self, task_data: Dict[str, Any], scheduled_time: datetime) -> str:
        """
        Schedule a task for future execution.
        
        Args:
            task_data: Task information
            scheduled_time: When to execute the task
            
        Returns:
            str: Task ID
        """
        task_data['scheduled_at'] = scheduled_time.isoformat()
        return self.add_task(task_data)
    
    def cancel_task(self, task_id: str) -> bool:
        """
        Cancel a scheduled or queued task.
        
        Args:
            task_id: Task identifier
            
        Returns:
            bool: True if task was cancelled, False if not found
        """
        # Check scheduled tasks
        if task_id in self.scheduled_tasks:
            del self.scheduled_tasks[task_id]
            self.logger.info(f"Cancelled scheduled task {task_id}")
            return True
        
        # Check active tasks (cannot cancel)
        if task_id in self.active_tasks:
            self.logger.warning(f"Cannot cancel active task {task_id}")
            return False
        
        # Check queue (more complex, would need to rebuild queue)
        self.logger.warning(f"Task {task_id} not found for cancellation")
        return False
    
    def get_task_statistics(self) -> Dict[str, int]:
        """
        Get statistics about tasks.
        
        Returns:
            Dictionary with task counts
        """
        return {
            'queued': self.task_queue.qsize(),
            'scheduled': len(self.scheduled_tasks),
            'active': len(self.active_tasks),
            'completed': len(self.completed_tasks),
            'failed': len(self.failed_tasks)
        }
    
    def get_queue_status(self) -> List[Dict[str, Any]]:
        """
        Get current queue status.
        
        Returns:
            List of queued tasks
        """
        # Note: This is a simplified view as PriorityQueue doesn't allow peeking
        return [
            {
                'queue_size': self.task_queue.qsize(),
                'scheduled_count': len(self.scheduled_tasks),
                'active_count': len(self.active_tasks)
            }
        ]
    
    def _scheduler_loop(self):
        """
        Background scheduler loop to move scheduled tasks to the queue.
        """
        while self.scheduler_running:
            try:
                current_time = datetime.now()
                tasks_to_queue = []
                
                # Check scheduled tasks
                for task_id, task in self.scheduled_tasks.items():
                    scheduled_time = datetime.fromisoformat(task.scheduled_at)
                    if current_time >= scheduled_time:
                        tasks_to_queue.append(task_id)
                
                # Move ready tasks to queue
                for task_id in tasks_to_queue:
                    task = self.scheduled_tasks.pop(task_id)
                    task.scheduled_at = None  # Clear scheduled time
                    self.task_queue.put(task)
                    self.logger.info(f"Moved scheduled task {task_id} to queue")
                
                # Sleep for a short interval
                threading.Event().wait(10)  # Check every 10 seconds
                
            except Exception as e:
                self.logger.error(f"Scheduler error: {str(e)}")
                threading.Event().wait(60)  # Wait longer on error
    
    def shutdown(self):
        """
        Shutdown the task manager.
        """
        self.scheduler_running = False
        if self.scheduler_thread.is_alive():
            self.scheduler_thread.join(timeout=5)
        self.logger.info("Task Manager shutdown")
    
    def export_tasks(self, file_path: str):
        """
        Export all tasks to a JSON file.
        
        Args:
            file_path: Path to save the export file
        """
        export_data = {
            'scheduled_tasks': {k: asdict(v) for k, v in self.scheduled_tasks.items()},
            'active_tasks': {k: asdict(v) for k, v in self.active_tasks.items()},
            'completed_tasks': {k: asdict(v) for k, v in self.completed_tasks.items()},
            'failed_tasks': {k: asdict(v) for k, v in self.failed_tasks.items()},
            'export_timestamp': datetime.now().isoformat()
        }
        
        with open(file_path, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        self.logger.info(f"Tasks exported to {file_path}")
    
    def import_tasks(self, file_path: str):
        """
        Import tasks from a JSON file.
        
        Args:
            file_path: Path to the import file
        """
        with open(file_path, 'r') as f:
            import_data = json.load(f)
        
        # Restore scheduled tasks
        for task_id, task_data in import_data.get('scheduled_tasks', {}).items():
            self.scheduled_tasks[task_id] = Task(**task_data)
        
        # Restore completed tasks
        for task_id, task_data in import_data.get('completed_tasks', {}).items():
            self.completed_tasks[task_id] = Task(**task_data)
        
        # Restore failed tasks
        for task_id, task_data in import_data.get('failed_tasks', {}).items():
            self.failed_tasks[task_id] = Task(**task_data)
        
        self.logger.info(f"Tasks imported from {file_path}")

