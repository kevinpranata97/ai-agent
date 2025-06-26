# Application Testing Guide

## Overview

The AI Agent platform includes a comprehensive application testing framework that automatically analyzes, tests, and validates generated applications across multiple programming languages and frameworks. This feature ensures that all created applications meet quality standards and function correctly before deployment.

## Key Features

### 🔍 **Intelligent Project Analysis**
- Automatic detection of project type and structure
- Multi-language support (Python, JavaScript, Java, C#, etc.)
- Framework identification (Flask, React, Express, Django, etc.)
- Dependency analysis and validation

### 🧪 **Comprehensive Testing Suite**
- **Unit Testing**: Individual component validation
- **Integration Testing**: Component interaction verification
- **Performance Testing**: Load and stress testing
- **Security Testing**: Vulnerability scanning and validation
- **Code Quality**: Static analysis and best practices validation

### 📊 **Advanced Reporting**
- Detailed test results and coverage analysis
- Performance metrics and benchmarks
- Security vulnerability reports
- Code quality assessments
- Actionable recommendations

### 🚀 **Automated Test Generation**
- AI-powered test case creation
- Edge case identification
- Mock data generation
- Test scenario optimization

## Supported Technologies

### Programming Languages
- **Python**: Full support with pytest, unittest
- **JavaScript/TypeScript**: Jest, Mocha, Jasmine
- **Java**: JUnit, TestNG
- **C#**: NUnit, MSTest
- **Go**: Built-in testing framework
- **Ruby**: RSpec, Minitest

### Frameworks
- **Web Frameworks**: Flask, Django, Express, React, Vue, Angular
- **API Frameworks**: FastAPI, Spring Boot, ASP.NET Core
- **Mobile**: React Native, Flutter (basic support)
- **Desktop**: Electron, PyQt (basic support)

### Testing Tools
- **Unit Testing**: pytest, Jest, JUnit, NUnit
- **Integration Testing**: Selenium, Cypress, Postman
- **Performance Testing**: Locust, Artillery, JMeter
- **Security Testing**: Bandit, ESLint Security, OWASP ZAP

## Getting Started

### 1. Project Analysis

Before running tests, the system analyzes your project structure:

```python
import requests

# Analyze project structure
response = requests.post(
    'http://localhost:5000/api/testing/analyze',
    json={'project_path': '/path/to/your/project'}
)

analysis = response.json()
print(f"Project Type: {analysis['project_type']}")
print(f"Languages: {analysis['languages']}")
print(f"Frameworks: {analysis['frameworks']}")
print(f"Has Tests: {analysis['has_tests']}")
```

### 2. Running Tests via Dashboard

1. **Navigate to Testing Tab**: Open the AI Agent dashboard and click "Testing"
2. **Enter Project Path**: Specify the path to your project
3. **Run Tests**: Click "Run Comprehensive Tests"
4. **Monitor Progress**: Watch real-time test execution
5. **Review Results**: Access detailed reports and recommendations

### 3. Running Tests via API

```python
import requests

# Start comprehensive testing
response = requests.post(
    'http://localhost:5000/api/testing/run',
    json={
        'project_path': '/path/to/your/project',
        'test_types': ['unit', 'integration', 'performance'],
        'coverage_threshold': 80
    }
)

session_id = response.json()['session_id']
print(f"Test session started: {session_id}")

# Monitor progress
status_response = requests.get(
    f'http://localhost:5000/api/testing/sessions/{session_id}'
)
print(f"Status: {status_response.json()['status']}")
```

## Test Types

### Unit Testing

Tests individual components in isolation:

```python
# Example: Python Flask application
def test_user_creation():
    """Test user creation functionality"""
    user_data = {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'securepassword'
    }
    
    response = client.post('/api/users', json=user_data)
    assert response.status_code == 201
    assert response.json()['username'] == 'testuser'

# Example: JavaScript React component
describe('UserProfile Component', () => {
    test('renders user information correctly', () => {
        const user = { name: 'John Doe', email: 'john@example.com' };
        render(<UserProfile user={user} />);
        
        expect(screen.getByText('John Doe')).toBeInTheDocument();
        expect(screen.getByText('john@example.com')).toBeInTheDocument();
    });
});
```

### Integration Testing

Tests component interactions and API endpoints:

```python
# Example: API integration test
def test_user_workflow():
    """Test complete user registration and login workflow"""
    # Register user
    register_response = client.post('/api/register', json={
        'username': 'integrationuser',
        'email': 'integration@example.com',
        'password': 'password123'
    })
    assert register_response.status_code == 201
    
    # Login user
    login_response = client.post('/api/login', json={
        'username': 'integrationuser',
        'password': 'password123'
    })
    assert login_response.status_code == 200
    assert 'access_token' in login_response.json()
    
    # Access protected resource
    token = login_response.json()['access_token']
    profile_response = client.get(
        '/api/profile',
        headers={'Authorization': f'Bearer {token}'}
    )
    assert profile_response.status_code == 200
```

### Performance Testing

Evaluates application performance under load:

```python
# Example: Load testing configuration
performance_config = {
    'test_duration': 300,  # 5 minutes
    'concurrent_users': 100,
    'ramp_up_time': 60,    # 1 minute
    'endpoints': [
        {'url': '/api/users', 'method': 'GET', 'weight': 70},
        {'url': '/api/users', 'method': 'POST', 'weight': 20},
        {'url': '/api/login', 'method': 'POST', 'weight': 10}
    ],
    'success_criteria': {
        'max_response_time': 2000,  # 2 seconds
        'error_rate_threshold': 1   # 1%
    }
}
```

### Security Testing

Identifies security vulnerabilities:

```python
# Example: Security test scenarios
security_tests = [
    'sql_injection',
    'xss_vulnerability',
    'csrf_protection',
    'authentication_bypass',
    'authorization_flaws',
    'sensitive_data_exposure',
    'security_headers',
    'https_enforcement'
]
```

## Configuration

### Test Configuration File

Create a `test_config.yaml` file in your project root:

```yaml
testing:
  # Test execution settings
  parallel_execution: true
  max_workers: 4
  timeout: 300
  
  # Coverage settings
  coverage:
    enabled: true
    threshold: 80
    exclude_patterns:
      - "*/tests/*"
      - "*/migrations/*"
      - "*/venv/*"
  
  # Unit testing
  unit_tests:
    enabled: true
    framework: "auto"  # auto-detect or specify: pytest, jest, junit
    test_patterns:
      - "**/test_*.py"
      - "**/*_test.js"
      - "**/Test*.java"
  
  # Integration testing
  integration_tests:
    enabled: true
    database_setup: true
    external_services: false
    test_data_cleanup: true
  
  # Performance testing
  performance_tests:
    enabled: true
    duration: 60
    concurrent_users: 10
    endpoints:
      - path: "/api/health"
        method: "GET"
        expected_response_time: 100
  
  # Security testing
  security_tests:
    enabled: true
    scan_dependencies: true
    check_headers: true
    test_authentication: true
    
  # Reporting
  reporting:
    formats: ["html", "json", "junit"]
    output_directory: "test_reports"
    include_coverage: true
    include_performance: true
```

### Environment-Specific Configuration

```yaml
environments:
  development:
    database_url: "sqlite:///test.db"
    api_base_url: "http://localhost:5000"
    debug: true
    
  staging:
    database_url: "postgresql://user:pass@staging-db:5432/testdb"
    api_base_url: "https://staging-api.example.com"
    debug: false
    
  production:
    # Production testing with limited scope
    performance_tests:
      enabled: true
      duration: 30
      concurrent_users: 5
    security_tests:
      enabled: true
    unit_tests:
      enabled: false  # Skip in production
```

## Advanced Features

### Custom Test Generation

The AI Agent can automatically generate tests based on your code:

```python
# Request AI-generated tests
response = requests.post(
    'http://localhost:5000/api/testing/generate',
    json={
        'project_path': '/path/to/project',
        'target_files': ['app.py', 'models.py'],
        'test_types': ['unit', 'integration'],
        'coverage_target': 90
    }
)

generated_tests = response.json()['tests']
for test_file, test_content in generated_tests.items():
    print(f"Generated test file: {test_file}")
    print(test_content)
```

### Continuous Testing Integration

Integrate with CI/CD pipelines:

```yaml
# .github/workflows/test.yml
name: Automated Testing
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Setup AI Agent Testing
        run: |
          pip install -r requirements.txt
          npm install
          
      - name: Run Comprehensive Tests
        run: |
          curl -X POST http://localhost:5000/api/testing/run \
            -H "Content-Type: application/json" \
            -d '{"project_path": ".", "test_types": ["unit", "integration", "security"]}'
          
      - name: Upload Test Reports
        uses: actions/upload-artifact@v2
        with:
          name: test-reports
          path: test_reports/
```

### Custom Test Hooks

Implement custom test hooks for specific requirements:

```python
# custom_test_hooks.py
class CustomTestHooks:
    def before_test_suite(self, context):
        """Execute before running the entire test suite"""
        print("Setting up test environment...")
        # Setup test database, mock services, etc.
        
    def after_test_suite(self, context):
        """Execute after running the entire test suite"""
        print("Cleaning up test environment...")
        # Cleanup resources, send notifications, etc.
        
    def before_test_case(self, test_case):
        """Execute before each test case"""
        # Setup test-specific data
        pass
        
    def after_test_case(self, test_case, result):
        """Execute after each test case"""
        if result.failed:
            # Log failure details, take screenshots, etc.
            pass
```

## Test Reports and Analytics

### HTML Reports

Generate comprehensive HTML reports:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Test Report - MyApp</title>
</head>
<body>
    <h1>Test Execution Summary</h1>
    <div class="summary">
        <div class="metric">
            <h3>Total Tests</h3>
            <span class="value">156</span>
        </div>
        <div class="metric">
            <h3>Passed</h3>
            <span class="value success">142</span>
        </div>
        <div class="metric">
            <h3>Failed</h3>
            <span class="value error">14</span>
        </div>
        <div class="metric">
            <h3>Coverage</h3>
            <span class="value">87.3%</span>
        </div>
    </div>
    
    <h2>Performance Metrics</h2>
    <table>
        <tr>
            <th>Endpoint</th>
            <th>Avg Response Time</th>
            <th>95th Percentile</th>
            <th>Error Rate</th>
        </tr>
        <tr>
            <td>/api/users</td>
            <td>145ms</td>
            <td>320ms</td>
            <td>0.2%</td>
        </tr>
    </table>
</body>
</html>
```

### JSON Reports

Machine-readable reports for integration:

```json
{
    "test_session": {
        "id": "test_1703505600",
        "project": "/path/to/project",
        "start_time": "2024-12-25T10:00:00Z",
        "end_time": "2024-12-25T10:15:30Z",
        "duration": 930
    },
    "summary": {
        "total_tests": 156,
        "passed": 142,
        "failed": 14,
        "skipped": 0,
        "success_rate": 91.0,
        "coverage": 87.3
    },
    "test_types": {
        "unit": {
            "total": 120,
            "passed": 115,
            "failed": 5,
            "coverage": 89.2
        },
        "integration": {
            "total": 25,
            "passed": 20,
            "failed": 5,
            "coverage": 78.5
        },
        "performance": {
            "total": 8,
            "passed": 7,
            "failed": 1,
            "avg_response_time": 145,
            "max_response_time": 2100
        },
        "security": {
            "total": 3,
            "passed": 0,
            "failed": 3,
            "vulnerabilities": [
                {
                    "type": "XSS",
                    "severity": "medium",
                    "location": "/api/search",
                    "description": "Potential XSS vulnerability in search parameter"
                }
            ]
        }
    }
}
```

## Best Practices

### Test Organization

1. **Structure Tests Logically**: Organize tests by feature or module
2. **Use Descriptive Names**: Test names should clearly describe what they test
3. **Keep Tests Independent**: Each test should be able to run in isolation
4. **Use Setup and Teardown**: Properly initialize and clean up test data
5. **Mock External Dependencies**: Use mocks for external services and APIs

### Test Data Management

```python
# Example: Test data factory
class TestDataFactory:
    @staticmethod
    def create_user(username=None, email=None):
        return {
            'username': username or f'user_{random.randint(1000, 9999)}',
            'email': email or f'test_{random.randint(1000, 9999)}@example.com',
            'password': 'testpassword123',
            'created_at': datetime.utcnow().isoformat()
        }
    
    @staticmethod
    def create_product(name=None, price=None):
        return {
            'name': name or f'Product {random.randint(1, 100)}',
            'price': price or round(random.uniform(10, 1000), 2),
            'description': 'Test product description',
            'category': 'test'
        }
```

### Performance Testing Guidelines

1. **Start Small**: Begin with low load and gradually increase
2. **Monitor Resources**: Track CPU, memory, and database performance
3. **Test Realistic Scenarios**: Use production-like data and user patterns
4. **Set Clear Criteria**: Define acceptable response times and error rates
5. **Test Different Load Patterns**: Steady load, spike testing, stress testing

### Security Testing Best Practices

1. **Regular Scans**: Run security tests on every deployment
2. **Update Dependencies**: Keep all dependencies up to date
3. **Test Authentication**: Verify all authentication mechanisms
4. **Check Authorization**: Ensure proper access controls
5. **Validate Input**: Test input validation and sanitization

## Troubleshooting

### Common Issues

#### Test Discovery Problems
```bash
# Issue: Tests not being discovered
# Solution: Check test file naming conventions
# Python: test_*.py or *_test.py
# JavaScript: *.test.js or *.spec.js
# Java: *Test.java or Test*.java
```

#### Database Connection Issues
```python
# Issue: Database connection failures in tests
# Solution: Use test-specific database configuration
DATABASE_CONFIG = {
    'test': {
        'url': 'sqlite:///test.db',
        'echo': False
    },
    'development': {
        'url': 'postgresql://localhost/myapp_dev',
        'echo': True
    }
}
```

#### Performance Test Failures
```yaml
# Issue: Performance tests failing unexpectedly
# Solution: Adjust thresholds and warm-up periods
performance:
  warm_up_duration: 30  # Allow system to warm up
  response_time_threshold: 2000  # Increase if needed
  error_rate_threshold: 5  # Allow some errors during load
```

### Debugging Failed Tests

1. **Check Logs**: Review detailed test execution logs
2. **Isolate Issues**: Run individual test cases to identify problems
3. **Verify Environment**: Ensure test environment matches expectations
4. **Check Dependencies**: Verify all required services are running
5. **Review Test Data**: Ensure test data is valid and accessible

## Integration Examples

### Flask Application Testing

```python
# test_app.py
import pytest
from app import create_app, db
from app.models import User

@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_user_registration(client):
    response = client.post('/api/register', json={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password123'
    })
    assert response.status_code == 201
    assert 'user_id' in response.json
```

### React Application Testing

```javascript
// UserComponent.test.js
import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import UserComponent from './UserComponent';

describe('UserComponent', () => {
    test('displays user information', async () => {
        const mockUser = {
            id: 1,
            name: 'John Doe',
            email: 'john@example.com'
        };
        
        render(<UserComponent user={mockUser} />);
        
        expect(screen.getByText('John Doe')).toBeInTheDocument();
        expect(screen.getByText('john@example.com')).toBeInTheDocument();
    });
    
    test('handles user update', async () => {
        const mockOnUpdate = jest.fn();
        const mockUser = { id: 1, name: 'John Doe', email: 'john@example.com' };
        
        render(<UserComponent user={mockUser} onUpdate={mockOnUpdate} />);
        
        fireEvent.click(screen.getByText('Edit'));
        fireEvent.change(screen.getByLabelText('Name'), {
            target: { value: 'Jane Doe' }
        });
        fireEvent.click(screen.getByText('Save'));
        
        await waitFor(() => {
            expect(mockOnUpdate).toHaveBeenCalledWith({
                ...mockUser,
                name: 'Jane Doe'
            });
        });
    });
});
```

## Conclusion

The Application Testing feature in the AI Agent platform provides comprehensive testing capabilities that ensure your applications are reliable, performant, and secure. By following the guidelines and best practices outlined in this guide, you can implement robust testing strategies that catch issues early and maintain high code quality throughout your development lifecycle.

For additional support or advanced testing scenarios, please refer to the main documentation or contact our support team.

