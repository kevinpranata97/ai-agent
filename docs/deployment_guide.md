# AI Agent Deployment Guide

## Overview

This guide provides comprehensive instructions for deploying the AI Agent system in various environments, from local development to production cloud deployments.

## Deployment Options

### Local Development Deployment

The simplest deployment option is running the AI Agent locally for development and testing purposes.

**Prerequisites:**
- Python 3.11+
- Node.js 20.18+
- Git 2.34+
- 4GB RAM minimum

**Steps:**
1. Clone the repository
2. Install dependencies
3. Configure environment variables
4. Start the services

**Detailed Instructions:**

```bash
# Clone repository
git clone https://github.com/kevinpranata97/ai-agent.git
cd ai-agent

# Install Python dependencies
pip3 install -r requirements.txt

# Install Node.js dependencies
cd ai-agent-dashboard
npm install
cd ..

# Create environment configuration
cat > .env << EOF
FLASK_ENV=development
FLASK_DEBUG=true
PORT=5000
GITHUB_TOKEN=your_token_here
GITHUB_REPO=kevinpranata97/ai-agent
EOF

# Start backend (Terminal 1)
cd src && python3 main.py

# Start frontend (Terminal 2)
cd ai-agent-dashboard && npm run dev
```

### Docker Deployment

For consistent deployment across different environments, use Docker containers.

**Create Dockerfile for Backend:**

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ ./src/
COPY docs/ ./docs/

# Expose port
EXPOSE 5000

# Start application
CMD ["python", "src/main.py"]
```

**Create Dockerfile for Frontend:**

```dockerfile
FROM node:20.18-alpine

WORKDIR /app

# Copy package files
COPY ai-agent-dashboard/package*.json ./
RUN npm install

# Copy source code
COPY ai-agent-dashboard/ .

# Build application
RUN npm run build

# Serve with nginx
FROM nginx:alpine
COPY --from=0 /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

**Docker Compose Configuration:**

```yaml
version: '3.8'

services:
  backend:
    build:
      context: .
      dockerfile: Dockerfile.backend
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
      - GITHUB_TOKEN=${GITHUB_TOKEN}
    volumes:
      - ./tasks:/app/tasks
      - ./logs:/app/logs

  frontend:
    build:
      context: .
      dockerfile: Dockerfile.frontend
    ports:
      - "80:80"
    depends_on:
      - backend

  redis:
    image: redis:alpine
    ports:
      - "6379:6379"

volumes:
  task_data:
  log_data:
```

### Cloud Platform Deployment

#### AWS Deployment

**Using AWS ECS (Elastic Container Service):**

1. **Create ECR Repositories:**
```bash
aws ecr create-repository --repository-name ai-agent-backend
aws ecr create-repository --repository-name ai-agent-frontend
```

2. **Build and Push Images:**
```bash
# Get login token
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com

# Build and tag images
docker build -f Dockerfile.backend -t ai-agent-backend .
docker tag ai-agent-backend:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/ai-agent-backend:latest

# Push images
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/ai-agent-backend:latest
```

3. **Create ECS Task Definition:**
```json
{
  "family": "ai-agent-task",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "1024",
  "memory": "2048",
  "executionRoleArn": "arn:aws:iam::<account-id>:role/ecsTaskExecutionRole",
  "containerDefinitions": [
    {
      "name": "ai-agent-backend",
      "image": "<account-id>.dkr.ecr.us-east-1.amazonaws.com/ai-agent-backend:latest",
      "portMappings": [
        {
          "containerPort": 5000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "FLASK_ENV",
          "value": "production"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/ai-agent",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

#### Google Cloud Platform Deployment

**Using Google Cloud Run:**

1. **Build and Deploy Backend:**
```bash
# Build image
gcloud builds submit --tag gcr.io/PROJECT-ID/ai-agent-backend

# Deploy to Cloud Run
gcloud run deploy ai-agent-backend \
  --image gcr.io/PROJECT-ID/ai-agent-backend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 5000
```

2. **Deploy Frontend to Firebase Hosting:**
```bash
# Install Firebase CLI
npm install -g firebase-tools

# Initialize Firebase
firebase init hosting

# Build and deploy
cd ai-agent-dashboard
npm run build
firebase deploy
```

#### Azure Deployment

**Using Azure Container Instances:**

1. **Create Resource Group:**
```bash
az group create --name ai-agent-rg --location eastus
```

2. **Deploy Container:**
```bash
az container create \
  --resource-group ai-agent-rg \
  --name ai-agent-backend \
  --image your-registry/ai-agent-backend:latest \
  --cpu 1 \
  --memory 2 \
  --ports 5000 \
  --environment-variables FLASK_ENV=production
```

### Production Configuration

#### Environment Variables

For production deployments, configure these environment variables:

```env
# Application Configuration
FLASK_ENV=production
FLASK_DEBUG=false
PORT=5000

# Database Configuration
DATABASE_URL=postgresql://user:password@host:port/database

# Redis Configuration
REDIS_URL=redis://host:port/0

# GitHub Integration
GITHUB_TOKEN=your_production_token
GITHUB_REPO=your-org/ai-agent

# Security
SECRET_KEY=your-secret-key
JWT_SECRET=your-jwt-secret

# Monitoring
SENTRY_DSN=your-sentry-dsn
LOG_LEVEL=INFO

# Deployment
DEPLOY_PLATFORM=aws
AUTO_DEPLOY=true
```

#### Database Setup

For production, use PostgreSQL instead of SQLite:

```python
# In your Flask configuration
import os

class ProductionConfig:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    REDIS_URL = os.environ.get('REDIS_URL')
```

#### Security Considerations

1. **HTTPS Configuration:**
   - Use SSL/TLS certificates
   - Configure secure headers
   - Enable HSTS

2. **Authentication:**
   - Implement user authentication
   - Use JWT tokens for API access
   - Configure role-based access control

3. **Network Security:**
   - Use VPC/private networks
   - Configure security groups/firewalls
   - Implement rate limiting

#### Monitoring and Logging

1. **Application Monitoring:**
```python
# Add to your Flask app
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    dsn=os.environ.get('SENTRY_DSN'),
    integrations=[FlaskIntegration()],
    traces_sample_rate=1.0
)
```

2. **Log Aggregation:**
   - Use centralized logging (ELK stack, Splunk)
   - Configure structured logging
   - Set up log rotation

3. **Health Checks:**
```python
@app.route('/health')
def health_check():
    return {
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'version': app.config.get('VERSION', '1.0.0')
    }
```

### Scaling Considerations

#### Horizontal Scaling

1. **Load Balancing:**
   - Use application load balancers
   - Configure health checks
   - Implement session affinity if needed

2. **Auto Scaling:**
   - Configure CPU/memory-based scaling
   - Set minimum and maximum instance counts
   - Use predictive scaling for known patterns

#### Performance Optimization

1. **Caching:**
   - Implement Redis for session storage
   - Cache frequently accessed data
   - Use CDN for static assets

2. **Database Optimization:**
   - Use connection pooling
   - Implement read replicas
   - Optimize queries and indexes

### Backup and Recovery

#### Data Backup

1. **Database Backups:**
```bash
# PostgreSQL backup
pg_dump -h hostname -U username -d database_name > backup.sql

# Automated backup script
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
pg_dump -h $DB_HOST -U $DB_USER -d $DB_NAME > backup_$DATE.sql
aws s3 cp backup_$DATE.sql s3://your-backup-bucket/
```

2. **File System Backups:**
```bash
# Backup task files and logs
tar -czf ai-agent-data-$(date +%Y%m%d).tar.gz tasks/ logs/
aws s3 cp ai-agent-data-$(date +%Y%m%d).tar.gz s3://your-backup-bucket/
```

#### Disaster Recovery

1. **Recovery Procedures:**
   - Document recovery steps
   - Test recovery procedures regularly
   - Maintain recovery time objectives (RTO)

2. **High Availability:**
   - Deploy across multiple availability zones
   - Use managed database services
   - Implement circuit breakers

### Maintenance and Updates

#### Rolling Updates

1. **Blue-Green Deployment:**
```bash
# Deploy new version to green environment
kubectl apply -f deployment-green.yaml

# Switch traffic to green
kubectl patch service ai-agent-service -p '{"spec":{"selector":{"version":"green"}}}'

# Remove blue environment
kubectl delete deployment ai-agent-blue
```

2. **Canary Deployment:**
```yaml
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: ai-agent-rollout
spec:
  strategy:
    canary:
      steps:
      - setWeight: 10
      - pause: {duration: 10m}
      - setWeight: 50
      - pause: {duration: 10m}
```

#### Monitoring Deployment Health

1. **Health Checks:**
   - Monitor application metrics
   - Set up alerting for failures
   - Track deployment success rates

2. **Rollback Procedures:**
   - Automate rollback triggers
   - Maintain previous version images
   - Test rollback procedures

This deployment guide provides comprehensive instructions for deploying the AI Agent system in various environments. Choose the deployment option that best fits your requirements and infrastructure constraints.

