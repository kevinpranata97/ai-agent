"""
Planning and Analysis Module
Handles requirement analysis, project planning, and data analysis tasks.
"""

import os
import json
import logging
import subprocess
from typing import Dict, Any, List, Optional
from datetime import datetime
import requests

class PlanningAnalysisModule:
    """
    Module responsible for analyzing requirements and creating execution plans.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.analysis_tools = {
            'web_research': self._web_research,
            'data_analysis': self._data_analysis,
            'requirement_parsing': self._parse_requirements,
            'technology_selection': self._select_technologies,
            'project_planning': self._create_project_plan
        }
        self.logger.info("Planning and Analysis module initialized")
    
    def analyze_and_plan(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze a task and create an execution plan.
        
        Args:
            task: Task dictionary containing description and metadata
            
        Returns:
            Dictionary containing the execution plan
        """
        self.logger.info(f"Analyzing task: {task['description']}")
        
        # Parse requirements from task description
        requirements = self._parse_requirements(task['description'])
        
        # Determine task complexity and type
        task_analysis = self._analyze_task_complexity(task)
        
        # Select appropriate technologies and tools
        tech_stack = self._select_technologies(requirements, task['type'])
        
        # Create step-by-step execution plan
        execution_plan = self._create_project_plan(requirements, tech_stack, task_analysis)
        
        # Estimate resources and timeline
        resource_estimate = self._estimate_resources(execution_plan)
        
        plan = {
            'requirements': requirements,
            'task_analysis': task_analysis,
            'technology_stack': tech_stack,
            'execution_plan': execution_plan,
            'resource_estimate': resource_estimate,
            'created_at': datetime.now().isoformat()
        }
        
        self.logger.info(f"Plan created with {len(execution_plan['steps'])} steps")
        
        return plan
    
    def perform_analysis(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform data analysis based on task requirements.
        
        Args:
            task: Task dictionary
            
        Returns:
            Analysis results
        """
        self.logger.info("Performing data analysis")
        
        analysis_type = task.get('metadata', {}).get('analysis_type', 'general')
        data_source = task.get('metadata', {}).get('data_source')
        
        if analysis_type == 'web_research':
            return self._web_research(task['description'])
        elif analysis_type == 'data_processing':
            return self._data_analysis(data_source)
        else:
            return self._general_analysis(task)
    
    def execute_general_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a general task that doesn't fit specific categories.
        
        Args:
            task: Task dictionary
            
        Returns:
            Execution result
        """
        self.logger.info("Executing general task")
        
        # Analyze what the task is asking for
        requirements = self._parse_requirements(task['description'])
        
        # Determine the best approach
        if any(keyword in task['description'].lower() for keyword in ['analyze', 'research', 'study']):
            return self._web_research(task['description'])
        elif any(keyword in task['description'].lower() for keyword in ['plan', 'organize', 'schedule']):
            return self._create_planning_document(task)
        else:
            return self._create_general_response(task)
    
    def _parse_requirements(self, description: str) -> Dict[str, Any]:
        """Parse requirements from natural language description."""
        requirements = {
            'functional': [],
            'technical': [],
            'constraints': [],
            'keywords': []
        }
        
        # Extract keywords
        keywords = description.lower().split()
        requirements['keywords'] = keywords
        
        # Identify functional requirements
        if any(word in description.lower() for word in ['website', 'web', 'site']):
            requirements['functional'].append('web_interface')
        
        if any(word in description.lower() for word in ['api', 'backend', 'server']):
            requirements['functional'].append('backend_api')
        
        if any(word in description.lower() for word in ['database', 'data', 'storage']):
            requirements['functional'].append('data_storage')
        
        if any(word in description.lower() for word in ['responsive', 'mobile']):
            requirements['functional'].append('responsive_design')
        
        # Identify technical requirements
        if any(word in description.lower() for word in ['react', 'vue', 'angular']):
            requirements['technical'].append('frontend_framework')
        
        if any(word in description.lower() for word in ['python', 'flask', 'django']):
            requirements['technical'].append('python_backend')
        
        if any(word in description.lower() for word in ['deploy', 'hosting', 'cloud']):
            requirements['technical'].append('deployment')
        
        # Identify constraints
        if any(word in description.lower() for word in ['fast', 'quick', 'urgent']):
            requirements['constraints'].append('time_sensitive')
        
        if any(word in description.lower() for word in ['simple', 'basic', 'minimal']):
            requirements['constraints'].append('minimal_complexity')
        
        return requirements
    
    def _analyze_task_complexity(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze task complexity and characteristics."""
        description = task['description'].lower()
        
        complexity_indicators = {
            'simple': ['basic', 'simple', 'minimal', 'quick'],
            'medium': ['standard', 'typical', 'normal'],
            'complex': ['advanced', 'complex', 'comprehensive', 'full-featured']
        }
        
        complexity = 'medium'  # default
        
        for level, indicators in complexity_indicators.items():
            if any(indicator in description for indicator in indicators):
                complexity = level
                break
        
        # Estimate based on features mentioned
        feature_count = 0
        features = ['authentication', 'database', 'api', 'responsive', 'admin', 'payment']
        for feature in features:
            if feature in description:
                feature_count += 1
        
        if feature_count > 3:
            complexity = 'complex'
        elif feature_count > 1:
            complexity = 'medium'
        
        return {
            'complexity': complexity,
            'estimated_features': feature_count,
            'task_type': task['type'],
            'priority': task.get('priority', 'medium')
        }
    
    def _select_technologies(self, requirements: Dict[str, Any], task_type: str) -> Dict[str, Any]:
        """Select appropriate technologies based on requirements."""
        tech_stack = {
            'frontend': [],
            'backend': [],
            'database': [],
            'deployment': [],
            'tools': []
        }
        
        # Frontend selection
        if 'web_interface' in requirements['functional']:
            if 'frontend_framework' in requirements['technical']:
                tech_stack['frontend'].append('React')
                tech_stack['tools'].extend(['npm', 'webpack'])
            else:
                tech_stack['frontend'].extend(['HTML', 'CSS', 'JavaScript'])
        
        # Backend selection
        if 'backend_api' in requirements['functional'] or task_type == 'app_development':
            if 'python_backend' in requirements['technical']:
                tech_stack['backend'].append('Flask')
                tech_stack['tools'].append('Python')
            else:
                tech_stack['backend'].append('Flask')  # Default to Flask
                tech_stack['tools'].append('Python')
        
        # Database selection
        if 'data_storage' in requirements['functional']:
            if 'minimal_complexity' in requirements['constraints']:
                tech_stack['database'].append('SQLite')
            else:
                tech_stack['database'].append('PostgreSQL')
        
        # Deployment selection
        if 'deployment' in requirements['technical']:
            tech_stack['deployment'].extend(['Cloud Platform', 'Docker'])
        
        return tech_stack
    
    def _create_project_plan(self, requirements: Dict[str, Any], tech_stack: Dict[str, Any], 
                           task_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Create a detailed project execution plan."""
        steps = []
        
        # Planning phase
        steps.append({
            'phase': 'planning',
            'step': 1,
            'title': 'Project Setup',
            'description': 'Initialize project structure and dependencies',
            'estimated_time': '15 minutes',
            'dependencies': []
        })
        
        # Development phases based on tech stack
        step_num = 2
        
        if tech_stack['backend']:
            steps.append({
                'phase': 'development',
                'step': step_num,
                'title': 'Backend Development',
                'description': f"Implement backend using {', '.join(tech_stack['backend'])}",
                'estimated_time': '30-60 minutes',
                'dependencies': [1]
            })
            step_num += 1
        
        if tech_stack['frontend']:
            steps.append({
                'phase': 'development',
                'step': step_num,
                'title': 'Frontend Development',
                'description': f"Create frontend using {', '.join(tech_stack['frontend'])}",
                'estimated_time': '30-45 minutes',
                'dependencies': [1]
            })
            step_num += 1
        
        if tech_stack['database']:
            steps.append({
                'phase': 'development',
                'step': step_num,
                'title': 'Database Integration',
                'description': f"Set up database using {', '.join(tech_stack['database'])}",
                'estimated_time': '15-30 minutes',
                'dependencies': [2] if tech_stack['backend'] else [1]
            })
            step_num += 1
        
        # Testing phase
        steps.append({
            'phase': 'testing',
            'step': step_num,
            'title': 'Testing and Validation',
            'description': 'Test functionality and fix issues',
            'estimated_time': '15-30 minutes',
            'dependencies': list(range(1, step_num))
        })
        step_num += 1
        
        # Deployment phase
        if tech_stack['deployment']:
            steps.append({
                'phase': 'deployment',
                'step': step_num,
                'title': 'Deployment',
                'description': f"Deploy using {', '.join(tech_stack['deployment'])}",
                'estimated_time': '10-20 minutes',
                'dependencies': [step_num - 1]
            })
        
        return {
            'steps': steps,
            'total_steps': len(steps),
            'estimated_total_time': self._calculate_total_time(steps),
            'complexity': task_analysis['complexity']
        }
    
    def _estimate_resources(self, execution_plan: Dict[str, Any]) -> Dict[str, Any]:
        """Estimate resources needed for the project."""
        complexity = execution_plan['complexity']
        
        resource_multipliers = {
            'simple': 1.0,
            'medium': 1.5,
            'complex': 2.5
        }
        
        base_time = 60  # minutes
        multiplier = resource_multipliers.get(complexity, 1.5)
        
        return {
            'estimated_time_minutes': int(base_time * multiplier),
            'complexity_level': complexity,
            'required_skills': ['Python', 'Web Development', 'Git'],
            'tools_needed': ['Code Editor', 'Browser', 'Git', 'Python Environment']
        }
    
    def _calculate_total_time(self, steps: List[Dict[str, Any]]) -> str:
        """Calculate total estimated time from steps."""
        total_minutes = 0
        
        for step in steps:
            time_str = step['estimated_time']
            # Extract minutes from time string (e.g., "30-60 minutes" -> 45)
            if '-' in time_str:
                times = time_str.split('-')
                min_time = int(times[0])
                max_time = int(times[1].split()[0])
                avg_time = (min_time + max_time) // 2
            else:
                avg_time = int(time_str.split()[0])
            
            total_minutes += avg_time
        
        hours = total_minutes // 60
        minutes = total_minutes % 60
        
        if hours > 0:
            return f"{hours}h {minutes}m"
        else:
            return f"{minutes}m"
    
    def _web_research(self, query: str) -> Dict[str, Any]:
        """Perform web research on a topic."""
        self.logger.info(f"Performing web research for: {query}")
        
        # This is a placeholder for web research functionality
        # In a real implementation, this would use web scraping or search APIs
        
        return {
            'query': query,
            'research_type': 'web_research',
            'findings': [
                'Research functionality would be implemented here',
                'This would include web scraping and data collection',
                'Results would be analyzed and summarized'
            ],
            'sources': [],
            'summary': f"Research completed for query: {query}",
            'timestamp': datetime.now().isoformat()
        }
    
    def _data_analysis(self, data_source: str) -> Dict[str, Any]:
        """Perform data analysis on provided data."""
        self.logger.info(f"Performing data analysis on: {data_source}")
        
        return {
            'data_source': data_source,
            'analysis_type': 'data_analysis',
            'results': {
                'summary': 'Data analysis functionality would be implemented here',
                'insights': [],
                'visualizations': []
            },
            'timestamp': datetime.now().isoformat()
        }
    
    def _create_planning_document(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Create a planning document for the task."""
        return {
            'document_type': 'planning',
            'task_id': task['id'],
            'content': {
                'objectives': [task['description']],
                'timeline': 'To be determined based on requirements',
                'resources': 'Standard development resources',
                'milestones': []
            },
            'timestamp': datetime.now().isoformat()
        }
    
    def _general_analysis(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Perform general analysis for unspecified analysis tasks."""
        return {
            'analysis_type': 'general',
            'task_description': task['description'],
            'approach': 'General analysis approach based on task requirements',
            'recommendations': [
                'Task has been analyzed',
                'Appropriate approach determined',
                'Ready for execution'
            ],
            'timestamp': datetime.now().isoformat()
        }
    
    def _create_general_response(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Create a general response for tasks that don't fit other categories."""
        return {
            'response_type': 'general',
            'task_description': task['description'],
            'status': 'processed',
            'message': f"Task '{task['description']}' has been processed",
            'timestamp': datetime.now().isoformat()
        }

