# AI Agent - Comprehensive Task Automation System

A sophisticated AI agent capable of handling website creation, application development, analysis, planning, and management tasks across multiple platforms. All development progress is tracked and managed through integrated version control.

## 🚀 Features

### Core Capabilities
- **Website Creation**: Build responsive websites using React, HTML/CSS/JS, or static site generators
- **Application Development**: Create full-stack applications with Flask backends and React frontends
- **Data Analysis**: Perform comprehensive data analysis and generate insights
- **Project Planning**: Intelligent task breakdown and resource estimation
- **Deployment Management**: Automated deployment to various cloud platforms
- **Version Control Integration**: Seamless Git/GitHub integration for progress tracking

### Management Interface
- **React Dashboard**: Modern, responsive web interface for monitoring and control
- **Real-time Monitoring**: Live system health and task progress tracking
- **Task Management**: Create, monitor, and manage tasks through an intuitive UI
- **System Analytics**: Comprehensive statistics and performance metrics

## 📋 Requirements

### System Requirements
- Python 3.11+
- Node.js 20.18+
- Git 2.34+
- 4GB RAM minimum
- 10GB free disk space

### Python Dependencies
```
Flask==2.3.3
Flask-CORS==4.0.0
requests==2.31.0
GitPython==3.1.37
python-dotenv==1.0.0
```

## 🛠 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/kevinpranata97/ai-agent.git
cd ai-agent
```

### 2. Install Python Dependencies
```bash
pip3 install -r requirements.txt
```

### 3. Install Dashboard Dependencies
```bash
cd ai-agent-dashboard
npm install
```

## 🚀 Quick Start

### 1. Start the AI Agent Backend
```bash
cd src
python3 main.py
```

The backend will start on `http://localhost:5000`

### 2. Start the Management Dashboard
```bash
cd ai-agent-dashboard
npm run dev
```

The dashboard will be available at `http://localhost:5173`

### 3. Access the Dashboard
Open your browser and navigate to `http://localhost:5173` to access the AI Agent Dashboard.

## 📖 Usage Guide

### Creating Tasks

#### Via Dashboard
1. Navigate to the "Create" tab in the dashboard
2. Enter a task description
3. Select the task type (Website Creation, App Development, Data Analysis, etc.)
4. Set the priority level
5. Click "Create Task"

#### Via API
```bash
curl -X POST http://localhost:5000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Create a responsive landing page for a tech startup",
    "type": "website_creation",
    "priority": "high"
  }'
```

### Monitoring Tasks

#### Dashboard Monitoring
- **Tasks Tab**: View all tasks with real-time status updates
- **Monitor Tab**: System health, resource usage, and version control status
- **System Tab**: Detailed system information and environment details

#### API Monitoring
```bash
# Get all tasks
curl http://localhost:5000/api/tasks

# Get specific task status
curl http://localhost:5000/api/tasks/{task_id}

# Get task logs
curl http://localhost:5000/api/tasks/{task_id}/logs
```

## 🏗 Architecture

### Core Components

#### Orchestration Layer
Central coordination system that manages task flow and module interaction.

#### Task Management Module
- Task queuing and prioritization
- Scheduling and lifecycle management
- Progress tracking and status updates

#### Planning & Analysis Module
- Natural language requirement parsing
- Technology stack selection
- Step-by-step execution planning
- Resource estimation

#### Development & Creation Module
- Project scaffolding and generation
- Code creation and modification
- Framework integration (React, Flask, etc.)
- Asset management

#### Deployment & Management Module
- Multi-platform deployment support
- Health monitoring and maintenance
- Rollback and version management

#### Version Control Module
- Git repository management
- Automated commit and push operations
- Branch management and merging
- Change tracking and history

### Technology Stack

#### Backend
- **Framework**: Flask 2.3.3
- **Language**: Python 3.11
- **Database**: SQLite (development), PostgreSQL (production)
- **Version Control**: GitPython

#### Frontend
- **Framework**: React 18
- **Build Tool**: Vite
- **UI Library**: shadcn/ui
- **Styling**: Tailwind CSS
- **Icons**: Lucide React

#### Development Tools
- **Package Manager**: npm/pnpm
- **Code Quality**: ESLint
- **Testing**: Custom test suite

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the root directory:

```env
# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=true
PORT=5000

# GitHub Configuration
GITHUB_TOKEN=your_github_token_here
GITHUB_REPO=kevinpranata97/ai-agent

# Deployment Configuration
DEPLOY_PLATFORM=auto
AUTO_DEPLOY=false
```

### GitHub Integration
1. Generate a Personal Access Token with `repo` scope
2. Add the token to your environment variables
3. The agent will automatically commit and push changes

## 📊 API Reference

### Health Check
```
GET /health
```
Returns system health status and basic information.

### Task Management
```
POST /api/tasks          # Create new task
GET /api/tasks           # List all tasks
GET /api/tasks/{id}      # Get task details
POST /api/tasks/{id}/execute  # Execute task
GET /api/tasks/{id}/logs # Get task logs
```

### System Information
```
GET /api/capabilities    # Get available capabilities
```

## 🧪 Testing

### Run Test Suite
```bash
python3 test_ai_agent.py
```

The test suite validates:
- Module imports and initialization
- Task management functionality
- Planning and analysis capabilities
- Development and creation features
- Deployment management
- Version control integration
- Orchestration layer coordination

### Expected Output
```
==================================================
AI AGENT VALIDATION TEST SUITE
==================================================
Testing module imports...
✓ All modules imported successfully
Testing TaskManager...
✓ Task created with ID: test-001
✓ Task statistics: {'queued': 1, 'scheduled': 0, 'active': 0, 'completed': 0, 'failed': 0}
...
Tests passed: 7/7
Success rate: 100.0%
🎉 All tests passed! AI Agent is ready for use.
```

## 📁 Project Structure

```
ai-agent/
├── README.md                    # This file
├── requirements.txt             # Python dependencies
├── test_ai_agent.py            # Test suite
├── .gitignore                  # Git ignore rules
├── docs/
│   └── design_document.md      # Architecture documentation
├── src/                        # Backend source code
│   ├── main.py                 # Flask application entry point
│   ├── modules/                # Core AI agent modules
│   │   ├── orchestration.py    # Central orchestration
│   │   ├── task_management.py  # Task lifecycle management
│   │   ├── planning_analysis.py # Planning and analysis
│   │   ├── dev_creation.py     # Development and creation
│   │   ├── deploy_management.py # Deployment management
│   │   └── version_control.py  # Git integration
│   └── utils/
│       └── logging.py          # Logging utilities
├── ai-agent-dashboard/         # Frontend dashboard
│   ├── src/
│   │   ├── App.jsx             # Main dashboard component
│   │   ├── components/         # UI components
│   │   └── assets/             # Static assets
│   ├── public/                 # Public assets
│   ├── package.json            # Node.js dependencies
│   └── vite.config.js          # Build configuration
└── tasks/                      # Task execution workspace
    └── {task_id}/              # Individual task directories
        ├── project/            # Generated project files
        └── logs/               # Task execution logs
```

## 🚀 Deployment

### Local Development
The AI agent is designed to run locally for development and testing. Follow the Quick Start guide above.

### Production Deployment
For production deployment, consider:

1. **Backend Deployment**
   - Use a production WSGI server (Gunicorn, uWSGI)
   - Configure environment variables
   - Set up database (PostgreSQL recommended)
   - Enable HTTPS

2. **Frontend Deployment**
   - Build the React application: `npm run build`
   - Serve static files through a web server (Nginx, Apache)
   - Configure reverse proxy for API calls

3. **Infrastructure**
   - Use containerization (Docker) for consistent deployment
   - Set up monitoring and logging
   - Configure backup and recovery procedures

## 🤝 Contributing

### Development Workflow
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run the test suite
5. Submit a pull request

### Code Standards
- Follow PEP 8 for Python code
- Use ESLint configuration for JavaScript/React
- Write comprehensive tests for new features
- Update documentation for API changes

## 📝 License

This project is licensed under the MIT License. See the LICENSE file for details.

## 🆘 Support

### Common Issues

#### Module Import Errors
Ensure all dependencies are installed:
```bash
pip3 install -r requirements.txt
```

#### Port Already in Use
Change the port in the configuration or kill existing processes:
```bash
pkill -f "python3 main.py"
```

#### Dashboard Not Loading
Ensure Node.js dependencies are installed:
```bash
cd ai-agent-dashboard
npm install
```

### Getting Help
- Check the test suite output for diagnostic information
- Review the logs in the `logs/` directory
- Consult the design document in `docs/design_document.md`

## 🔮 Future Enhancements

- Integration with cloud platforms (AWS, GCP, Azure)
- Support for additional programming languages
- Advanced AI model integration
- Real-time collaboration features
- Mobile application support
- Enterprise authentication and authorization

---

**Created by**: AI Agent Development Team  
**Last Updated**: December 25, 2024  
**Version**: 1.0.0

