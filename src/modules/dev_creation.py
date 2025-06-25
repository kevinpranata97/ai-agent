"""
Development and Creation Module
Handles website creation, application development, and code generation.
"""

import os
import json
import logging
import subprocess
import shutil
from typing import Dict, Any, List, Optional
from datetime import datetime

class DevelopmentCreationModule:
    """
    Module responsible for creating websites, applications, and generating code.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.project_templates = {
            'react_website': self._create_react_website,
            'static_website': self._create_static_website,
            'flask_api': self._create_flask_api,
            'full_stack_app': self._create_full_stack_app
        }
        self.logger.info("Development and Creation module initialized")
    
    def create_project(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a project based on task requirements.
        
        Args:
            task: Task dictionary containing requirements and plan
            
        Returns:
            Dictionary containing project creation results
        """
        self.logger.info(f"Creating project for task: {task['id']}")
        
        # Determine project type from task analysis
        project_type = self._determine_project_type(task)
        
        # Create project directory
        project_path = self._create_project_directory(task['id'])
        
        # Generate project based on type
        if project_type in self.project_templates:
            result = self.project_templates[project_type](task, project_path)
        else:
            result = self._create_generic_project(task, project_path)
        
        # Add common project files
        self._add_common_files(project_path, task)
        
        result.update({
            'project_path': project_path,
            'project_type': project_type,
            'created_at': datetime.now().isoformat()
        })
        
        self.logger.info(f"Project created at: {project_path}")
        
        return result
    
    def _determine_project_type(self, task: Dict[str, Any]) -> str:
        """Determine the type of project to create based on task requirements."""
        description = task['description'].lower()
        task_type = task.get('type', 'general')
        
        # Check for specific frameworks mentioned
        if 'react' in description:
            return 'react_website'
        elif 'api' in description or 'backend' in description:
            return 'flask_api'
        elif task_type == 'website_creation':
            if 'dynamic' in description or 'interactive' in description:
                return 'react_website'
            else:
                return 'static_website'
        elif task_type == 'app_development':
            if 'full' in description or 'stack' in description:
                return 'full_stack_app'
            else:
                return 'flask_api'
        
        return 'static_website'  # Default
    
    def _create_project_directory(self, task_id: str) -> str:
        """Create a project directory for the task."""
        base_path = os.path.join(os.getcwd(), 'tasks', task_id)
        project_path = os.path.join(base_path, 'project')
        
        os.makedirs(project_path, exist_ok=True)
        os.makedirs(os.path.join(base_path, 'logs'), exist_ok=True)
        
        return project_path
    
    def _create_react_website(self, task: Dict[str, Any], project_path: str) -> Dict[str, Any]:
        """Create a React website project."""
        self.logger.info("Creating React website")
        
        try:
            # Use the manus utility to create React app
            app_name = f"react-app-{task['id'][:8]}"
            
            # Run the manus-create-react-app utility
            result = subprocess.run(
                ['manus-create-react-app', app_name],
                cwd=os.path.dirname(project_path),
                capture_output=True,
                text=True,
                timeout=300
            )
            
            if result.returncode == 0:
                # Move the created app to our project path
                created_app_path = os.path.join(os.path.dirname(project_path), app_name)
                if os.path.exists(created_app_path):
                    # Move contents to project_path
                    for item in os.listdir(created_app_path):
                        shutil.move(
                            os.path.join(created_app_path, item),
                            os.path.join(project_path, item)
                        )
                    os.rmdir(created_app_path)
                
                # Customize the React app based on task requirements
                self._customize_react_app(task, project_path)
                
                return {
                    'status': 'success',
                    'framework': 'React',
                    'features': ['Responsive Design', 'Modern UI', 'Component-based'],
                    'entry_point': 'src/App.js',
                    'build_command': 'npm run build',
                    'dev_command': 'npm start'
                }
            else:
                self.logger.error(f"Failed to create React app: {result.stderr}")
                return self._create_static_website(task, project_path)
                
        except Exception as e:
            self.logger.error(f"Error creating React website: {str(e)}")
            return self._create_static_website(task, project_path)
    
    def _create_static_website(self, task: Dict[str, Any], project_path: str) -> Dict[str, Any]:
        """Create a static HTML/CSS/JS website."""
        self.logger.info("Creating static website")
        
        # Create basic HTML structure
        html_content = self._generate_html_template(task)
        css_content = self._generate_css_template(task)
        js_content = self._generate_js_template(task)
        
        # Write files
        with open(os.path.join(project_path, 'index.html'), 'w') as f:
            f.write(html_content)
        
        with open(os.path.join(project_path, 'style.css'), 'w') as f:
            f.write(css_content)
        
        with open(os.path.join(project_path, 'script.js'), 'w') as f:
            f.write(js_content)
        
        return {
            'status': 'success',
            'framework': 'Static HTML/CSS/JS',
            'features': ['Responsive Design', 'Cross-browser Compatible'],
            'entry_point': 'index.html',
            'files': ['index.html', 'style.css', 'script.js']
        }
    
    def _create_flask_api(self, task: Dict[str, Any], project_path: str) -> Dict[str, Any]:
        """Create a Flask API project."""
        self.logger.info("Creating Flask API")
        
        try:
            # Use the manus utility to create Flask app
            app_name = f"flask-api-{task['id'][:8]}"
            
            # Run the manus-create-flask-app utility
            result = subprocess.run(
                ['manus-create-flask-app', app_name],
                cwd=os.path.dirname(project_path),
                capture_output=True,
                text=True,
                timeout=300
            )
            
            if result.returncode == 0:
                # Move the created app to our project path
                created_app_path = os.path.join(os.path.dirname(project_path), app_name)
                if os.path.exists(created_app_path):
                    # Move contents to project_path
                    for item in os.listdir(created_app_path):
                        shutil.move(
                            os.path.join(created_app_path, item),
                            os.path.join(project_path, item)
                        )
                    os.rmdir(created_app_path)
                
                # Customize the Flask app based on task requirements
                self._customize_flask_app(task, project_path)
                
                return {
                    'status': 'success',
                    'framework': 'Flask',
                    'features': ['REST API', 'CORS Enabled', 'JSON Responses'],
                    'entry_point': 'app.py',
                    'run_command': 'python app.py',
                    'api_endpoints': self._get_flask_endpoints(project_path)
                }
            else:
                self.logger.error(f"Failed to create Flask app: {result.stderr}")
                return self._create_basic_flask_app(task, project_path)
                
        except Exception as e:
            self.logger.error(f"Error creating Flask API: {str(e)}")
            return self._create_basic_flask_app(task, project_path)
    
    def _create_full_stack_app(self, task: Dict[str, Any], project_path: str) -> Dict[str, Any]:
        """Create a full-stack application with React frontend and Flask backend."""
        self.logger.info("Creating full-stack application")
        
        # Create backend
        backend_path = os.path.join(project_path, 'backend')
        os.makedirs(backend_path, exist_ok=True)
        backend_result = self._create_flask_api(task, backend_path)
        
        # Create frontend
        frontend_path = os.path.join(project_path, 'frontend')
        os.makedirs(frontend_path, exist_ok=True)
        frontend_result = self._create_react_website(task, frontend_path)
        
        # Create docker-compose for easy deployment
        self._create_docker_compose(project_path)
        
        return {
            'status': 'success',
            'framework': 'Full Stack (React + Flask)',
            'features': ['React Frontend', 'Flask Backend', 'API Integration', 'Docker Support'],
            'backend': backend_result,
            'frontend': frontend_result,
            'structure': {
                'backend': 'backend/',
                'frontend': 'frontend/',
                'docker': 'docker-compose.yml'
            }
        }
    
    def _create_generic_project(self, task: Dict[str, Any], project_path: str) -> Dict[str, Any]:
        """Create a generic project structure."""
        self.logger.info("Creating generic project")
        
        # Create basic project structure
        os.makedirs(os.path.join(project_path, 'src'), exist_ok=True)
        os.makedirs(os.path.join(project_path, 'docs'), exist_ok=True)
        os.makedirs(os.path.join(project_path, 'tests'), exist_ok=True)
        
        # Create README
        readme_content = f"""# {task['description']}

## Project Description
{task['description']}

## Created
{datetime.now().isoformat()}

## Task ID
{task['id']}
"""
        
        with open(os.path.join(project_path, 'README.md'), 'w') as f:
            f.write(readme_content)
        
        return {
            'status': 'success',
            'framework': 'Generic Project',
            'features': ['Basic Structure', 'Documentation'],
            'structure': ['src/', 'docs/', 'tests/', 'README.md']
        }
    
    def _customize_react_app(self, task: Dict[str, Any], project_path: str):
        """Customize React app based on task requirements."""
        # This would contain logic to modify the React app
        # based on specific requirements in the task
        pass
    
    def _customize_flask_app(self, task: Dict[str, Any], project_path: str):
        """Customize Flask app based on task requirements."""
        # This would contain logic to modify the Flask app
        # based on specific requirements in the task
        pass
    
    def _create_basic_flask_app(self, task: Dict[str, Any], project_path: str) -> Dict[str, Any]:
        """Create a basic Flask app manually if utility fails."""
        app_content = '''from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({
        'message': 'AI Agent Flask API',
        'status': 'running',
        'endpoints': ['/api/health', '/api/data']
    })

@app.route('/api/health')
def health():
    return jsonify({'status': 'healthy'})

@app.route('/api/data', methods=['GET', 'POST'])
def data():
    if request.method == 'POST':
        return jsonify({'message': 'Data received', 'data': request.json})
    return jsonify({'message': 'Data endpoint', 'method': 'GET'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
'''
        
        with open(os.path.join(project_path, 'app.py'), 'w') as f:
            f.write(app_content)
        
        # Create requirements.txt
        requirements = '''Flask==2.3.3
Flask-CORS==4.0.0
'''
        
        with open(os.path.join(project_path, 'requirements.txt'), 'w') as f:
            f.write(requirements)
        
        return {
            'status': 'success',
            'framework': 'Flask (Basic)',
            'features': ['REST API', 'CORS Enabled'],
            'entry_point': 'app.py'
        }
    
    def _generate_html_template(self, task: Dict[str, Any]) -> str:
        """Generate HTML template based on task requirements."""
        title = task.get('metadata', {}).get('title', 'AI Agent Project')
        
        return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header>
        <nav>
            <h1>{title}</h1>
        </nav>
    </header>
    
    <main>
        <section class="hero">
            <h2>Welcome to {title}</h2>
            <p>{task['description']}</p>
        </section>
        
        <section class="content">
            <div class="container">
                <h3>Features</h3>
                <div class="features">
                    <div class="feature">
                        <h4>Responsive Design</h4>
                        <p>Works on all devices</p>
                    </div>
                    <div class="feature">
                        <h4>Modern UI</h4>
                        <p>Clean and professional design</p>
                    </div>
                    <div class="feature">
                        <h4>Fast Loading</h4>
                        <p>Optimized for performance</p>
                    </div>
                </div>
            </div>
        </section>
    </main>
    
    <footer>
        <p>&copy; 2024 AI Agent. Created on {datetime.now().strftime('%Y-%m-%d')}</p>
    </footer>
    
    <script src="script.js"></script>
</body>
</html>'''
    
    def _generate_css_template(self, task: Dict[str, Any]) -> str:
        """Generate CSS template with responsive design."""
        return '''* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Arial', sans-serif;
    line-height: 1.6;
    color: #333;
}

header {
    background: #2c3e50;
    color: white;
    padding: 1rem 0;
    position: fixed;
    width: 100%;
    top: 0;
    z-index: 1000;
}

nav h1 {
    text-align: center;
    padding: 0 2rem;
}

main {
    margin-top: 80px;
}

.hero {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    text-align: center;
    padding: 4rem 2rem;
}

.hero h2 {
    font-size: 2.5rem;
    margin-bottom: 1rem;
}

.hero p {
    font-size: 1.2rem;
    max-width: 600px;
    margin: 0 auto;
}

.content {
    padding: 4rem 2rem;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
}

.features {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
    margin-top: 2rem;
}

.feature {
    background: #f8f9fa;
    padding: 2rem;
    border-radius: 8px;
    text-align: center;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.feature h4 {
    color: #2c3e50;
    margin-bottom: 1rem;
}

footer {
    background: #2c3e50;
    color: white;
    text-align: center;
    padding: 2rem;
}

@media (max-width: 768px) {
    .hero h2 {
        font-size: 2rem;
    }
    
    .hero p {
        font-size: 1rem;
    }
    
    .features {
        grid-template-columns: 1fr;
    }
}'''
    
    def _generate_js_template(self, task: Dict[str, Any]) -> str:
        """Generate JavaScript template with basic functionality."""
        return '''// AI Agent Project JavaScript

document.addEventListener('DOMContentLoaded', function() {
    console.log('AI Agent Project loaded successfully');
    
    // Add smooth scrolling
    const links = document.querySelectorAll('a[href^="#"]');
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // Add animation to features
    const features = document.querySelectorAll('.feature');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    });
    
    features.forEach(feature => {
        feature.style.opacity = '0';
        feature.style.transform = 'translateY(20px)';
        feature.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(feature);
    });
});

// Utility functions
function showMessage(message, type = 'info') {
    console.log(`[${type.toUpperCase()}] ${message}`);
}

function apiCall(endpoint, method = 'GET', data = null) {
    const options = {
        method: method,
        headers: {
            'Content-Type': 'application/json',
        }
    };
    
    if (data) {
        options.body = JSON.stringify(data);
    }
    
    return fetch(endpoint, options)
        .then(response => response.json())
        .catch(error => {
            console.error('API call failed:', error);
            throw error;
        });
}'''
    
    def _get_flask_endpoints(self, project_path: str) -> List[str]:
        """Extract Flask endpoints from the app file."""
        # This would parse the Flask app file to extract endpoints
        # For now, return default endpoints
        return ['/api/health', '/api/data']
    
    def _create_docker_compose(self, project_path: str):
        """Create docker-compose.yml for full-stack deployment."""
        docker_compose_content = '''version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
    volumes:
      - ./backend:/app
    
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend
    volumes:
      - ./frontend:/app
      - /app/node_modules

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - frontend
      - backend
'''
        
        with open(os.path.join(project_path, 'docker-compose.yml'), 'w') as f:
            f.write(docker_compose_content)
    
    def _add_common_files(self, project_path: str, task: Dict[str, Any]):
        """Add common files to all projects."""
        # Create .gitignore
        gitignore_content = '''# Dependencies
node_modules/
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.venv/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Environment variables
.env
.env.local
.env.production

# Build outputs
build/
dist/
*.egg-info/
'''
        
        with open(os.path.join(project_path, '.gitignore'), 'w') as f:
            f.write(gitignore_content)
        
        # Create project metadata
        metadata = {
            'task_id': task['id'],
            'description': task['description'],
            'created_at': datetime.now().isoformat(),
            'ai_agent_version': '1.0.0'
        }
        
        with open(os.path.join(project_path, 'project_metadata.json'), 'w') as f:
            json.dump(metadata, f, indent=2)

