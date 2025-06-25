"""
Logging Utility
Centralized logging configuration for the AI Agent.
"""

import os
import logging
import logging.handlers
from datetime import datetime

def setup_logging(log_level=logging.INFO, log_dir="logs"):
    """
    Setup centralized logging for the AI Agent.
    
    Args:
        log_level: Logging level (default: INFO)
        log_dir: Directory to store log files
        
    Returns:
        Logger instance
    """
    # Create logs directory if it doesn't exist
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Create logger
    logger = logging.getLogger('ai_agent')
    logger.setLevel(log_level)
    
    # Clear any existing handlers
    logger.handlers.clear()
    
    # Create formatters
    detailed_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
    )
    
    simple_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(simple_formatter)
    logger.addHandler(console_handler)
    
    # File handler for general logs
    log_file = os.path.join(log_dir, f"ai_agent_{datetime.now().strftime('%Y%m%d')}.log")
    file_handler = logging.handlers.RotatingFileHandler(
        log_file, maxBytes=10*1024*1024, backupCount=5  # 10MB files, keep 5 backups
    )
    file_handler.setLevel(log_level)
    file_handler.setFormatter(detailed_formatter)
    logger.addHandler(file_handler)
    
    # Error file handler
    error_log_file = os.path.join(log_dir, f"ai_agent_errors_{datetime.now().strftime('%Y%m%d')}.log")
    error_handler = logging.handlers.RotatingFileHandler(
        error_log_file, maxBytes=10*1024*1024, backupCount=5
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(detailed_formatter)
    logger.addHandler(error_handler)
    
    # Task-specific handler
    task_log_file = os.path.join(log_dir, f"ai_agent_tasks_{datetime.now().strftime('%Y%m%d')}.log")
    task_handler = logging.handlers.RotatingFileHandler(
        task_log_file, maxBytes=10*1024*1024, backupCount=5
    )
    task_handler.setLevel(logging.INFO)
    task_handler.setFormatter(detailed_formatter)
    
    # Create a filter for task-related logs
    class TaskFilter(logging.Filter):
        def filter(self, record):
            return 'task' in record.getMessage().lower() or 'Task' in record.getMessage()
    
    task_handler.addFilter(TaskFilter())
    logger.addHandler(task_handler)
    
    logger.info("Logging system initialized")
    
    return logger

def get_task_logger(task_id: str, log_dir="logs"):
    """
    Get a logger specific to a task.
    
    Args:
        task_id: Unique task identifier
        log_dir: Directory to store log files
        
    Returns:
        Logger instance for the specific task
    """
    # Create task-specific logs directory
    task_log_dir = os.path.join(log_dir, "tasks", task_id)
    if not os.path.exists(task_log_dir):
        os.makedirs(task_log_dir)
    
    # Create task-specific logger
    logger_name = f'ai_agent.task.{task_id}'
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)
    
    # Clear any existing handlers
    logger.handlers.clear()
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # Task-specific file handler
    task_log_file = os.path.join(task_log_dir, f"task_{task_id}.log")
    task_handler = logging.FileHandler(task_log_file)
    task_handler.setLevel(logging.INFO)
    task_handler.setFormatter(formatter)
    logger.addHandler(task_handler)
    
    # Also add to main logger
    main_logger = logging.getLogger('ai_agent')
    logger.addHandler(main_logger.handlers[0])  # Console handler
    
    return logger

class TaskLogContext:
    """
    Context manager for task-specific logging.
    """
    
    def __init__(self, task_id: str, log_dir="logs"):
        self.task_id = task_id
        self.log_dir = log_dir
        self.logger = None
    
    def __enter__(self):
        self.logger = get_task_logger(self.task_id, self.log_dir)
        self.logger.info(f"Starting task {self.task_id}")
        return self.logger
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.logger.error(f"Task {self.task_id} failed: {exc_val}")
        else:
            self.logger.info(f"Task {self.task_id} completed successfully")
        
        # Clean up handlers
        for handler in self.logger.handlers[:]:
            handler.close()
            self.logger.removeHandler(handler)

def log_function_call(func):
    """
    Decorator to log function calls.
    
    Args:
        func: Function to decorate
        
    Returns:
        Decorated function
    """
    def wrapper(*args, **kwargs):
        logger = logging.getLogger('ai_agent')
        logger.debug(f"Calling {func.__name__} with args={args}, kwargs={kwargs}")
        
        try:
            result = func(*args, **kwargs)
            logger.debug(f"{func.__name__} completed successfully")
            return result
        except Exception as e:
            logger.error(f"{func.__name__} failed: {str(e)}")
            raise
    
    return wrapper

def log_performance(func):
    """
    Decorator to log function performance.
    
    Args:
        func: Function to decorate
        
    Returns:
        Decorated function
    """
    import time
    
    def wrapper(*args, **kwargs):
        logger = logging.getLogger('ai_agent')
        start_time = time.time()
        
        try:
            result = func(*args, **kwargs)
            end_time = time.time()
            execution_time = end_time - start_time
            logger.info(f"{func.__name__} executed in {execution_time:.2f} seconds")
            return result
        except Exception as e:
            end_time = time.time()
            execution_time = end_time - start_time
            logger.error(f"{func.__name__} failed after {execution_time:.2f} seconds: {str(e)}")
            raise
    
    return wrapper

