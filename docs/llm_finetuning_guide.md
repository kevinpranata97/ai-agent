# LLM Fine-tuning Guide

## Overview

The AI Agent platform now includes comprehensive LLM (Large Language Model) fine-tuning capabilities, allowing you to create custom models tailored to your specific use cases. This feature integrates directly with OpenAI's fine-tuning API to provide a seamless experience for training, managing, and deploying custom language models.

## Prerequisites

Before using the LLM fine-tuning features, ensure you have:

1. **OpenAI API Key**: A valid OpenAI API key with fine-tuning permissions
2. **API Credits**: Sufficient OpenAI credits for training (costs vary by model and data size)
3. **Training Data**: Properly formatted training data in JSONL format
4. **System Requirements**: At least 4GB RAM and stable internet connection

## Setting Up

### 1. Configure API Key

Set your OpenAI API key as an environment variable:

```bash
export OPENAI_API_KEY="your-openai-api-key-here"
```

Alternatively, you can set it in a `.env` file in the project root:

```
OPENAI_API_KEY=your-openai-api-key-here
```

### 2. Verify Configuration

Check that the LLM fine-tuning module is properly configured by visiting the dashboard health endpoint or checking the capabilities endpoint:

```bash
curl http://localhost:5000/api/capabilities
```

Look for the `llm_finetuning` section in the response.

## Training Data Format

### JSONL Format Requirements

Training data must be in JSONL (JSON Lines) format, where each line contains a complete conversation example:

```json
{"messages": [{"role": "user", "content": "What is machine learning?"}, {"role": "assistant", "content": "Machine learning is a subset of artificial intelligence that enables computers to learn and improve from experience without being explicitly programmed."}]}
{"messages": [{"role": "user", "content": "Explain neural networks"}, {"role": "assistant", "content": "Neural networks are computing systems inspired by biological neural networks. They consist of interconnected nodes (neurons) that process information through weighted connections."}]}
```

### Data Quality Guidelines

1. **Consistency**: Maintain consistent formatting and style across all examples
2. **Relevance**: Include only examples relevant to your target use case
3. **Diversity**: Provide diverse examples to improve model generalization
4. **Quality**: Ensure high-quality, accurate responses in your training data
5. **Volume**: Include at least 10-50 examples for basic fine-tuning (more for complex tasks)

### Example Use Cases

#### Customer Support Bot
```json
{"messages": [{"role": "user", "content": "How do I reset my password?"}, {"role": "assistant", "content": "To reset your password, click on 'Forgot Password' on the login page, enter your email address, and follow the instructions sent to your email."}]}
{"messages": [{"role": "user", "content": "What are your business hours?"}, {"role": "assistant", "content": "Our customer support is available Monday through Friday, 9 AM to 6 PM EST. For urgent issues, please use our emergency contact form."}]}
```

#### Technical Documentation Assistant
```json
{"messages": [{"role": "user", "content": "How do I install the package?"}, {"role": "assistant", "content": "You can install the package using pip: `pip install package-name`. Make sure you have Python 3.7 or higher installed."}]}
{"messages": [{"role": "user", "content": "What are the configuration options?"}, {"role": "assistant", "content": "The main configuration options include: database_url, api_key, debug_mode, and log_level. These can be set in the config.yaml file or as environment variables."}]}
```

## Creating a Fine-tuning Job

### Using the Dashboard

1. **Navigate to Fine-tuning Tab**: Open the AI Agent dashboard and click on the "Fine-tuning" tab
2. **Select Base Model**: Choose from available base models (GPT-3.5 Turbo, GPT-4)
3. **Prepare Training Data**: Paste your JSONL formatted training data in the text area
4. **Set Model Suffix**: (Optional) Add a custom suffix to identify your model
5. **Start Training**: Click "Start Fine-tuning" to begin the process

### Using the API

You can also create fine-tuning jobs programmatically:

```python
import requests

# Prepare the training data
training_data = [
    {
        "messages": [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi! How can I help you today?"}
        ]
    }
]

# Create fine-tuning job
response = requests.post(
    'http://localhost:5000/api/llm/fine-tuning/jobs',
    json={
        'training_data': training_data,
        'model': 'gpt-3.5-turbo',
        'suffix': 'my-custom-model'
    }
)

job_id = response.json()['job_id']
print(f"Fine-tuning job created: {job_id}")
```

## Monitoring Training Progress

### Dashboard Monitoring

The dashboard provides real-time monitoring of your fine-tuning jobs:

1. **Job Status**: View current status (queued, running, completed, failed)
2. **Progress Tracking**: Monitor training progress and estimated completion time
3. **Metrics**: View training metrics and performance indicators
4. **Logs**: Access detailed training logs and error messages

### API Monitoring

Check job status programmatically:

```python
import requests

job_id = "your-job-id"
response = requests.get(f'http://localhost:5000/api/llm/fine-tuning/jobs/{job_id}')
status = response.json()

print(f"Status: {status['status']}")
print(f"Progress: {status['progress']}%")
```

## Managing Fine-tuned Models

### Model Listing

View all your fine-tuned models:

```python
import requests

response = requests.get('http://localhost:5000/api/llm/models')
models = response.json()

for model in models:
    print(f"Model: {model['id']}")
    print(f"Created: {model['created_at']}")
    print(f"Status: {model['status']}")
```

### Model Testing

Test your fine-tuned models before deployment:

```python
import requests

model_id = "ft:gpt-3.5-turbo:your-org:custom-model:abc123"
test_prompt = "Hello, how are you?"

response = requests.post(
    f'http://localhost:5000/api/llm/models/{model_id}/test',
    json={'prompt': test_prompt}
)

result = response.json()
print(f"Response: {result['response']}")
```

## Best Practices

### Data Preparation

1. **Clean Data**: Remove any sensitive or inappropriate content
2. **Consistent Format**: Maintain consistent conversation structure
3. **Balanced Examples**: Include diverse scenarios and edge cases
4. **Quality Control**: Review all training examples for accuracy
5. **Incremental Training**: Start with smaller datasets and expand gradually

### Training Optimization

1. **Model Selection**: Choose the appropriate base model for your use case
2. **Hyperparameter Tuning**: Experiment with different training parameters
3. **Validation**: Always validate model performance before deployment
4. **Monitoring**: Continuously monitor model performance in production
5. **Iteration**: Regularly update and retrain models with new data

### Cost Management

1. **Data Efficiency**: Use high-quality, relevant training data to minimize training time
2. **Model Reuse**: Leverage existing fine-tuned models when possible
3. **Batch Processing**: Group multiple training jobs to optimize costs
4. **Monitoring Usage**: Track API usage and costs regularly

## Troubleshooting

### Common Issues

#### Training Data Validation Errors
- **Issue**: "Invalid JSONL format"
- **Solution**: Ensure each line is valid JSON with proper message structure
- **Example**: Check for missing quotes, commas, or brackets

#### API Key Issues
- **Issue**: "Authentication failed"
- **Solution**: Verify your OpenAI API key is correct and has fine-tuning permissions
- **Check**: Ensure the API key is properly set in environment variables

#### Insufficient Credits
- **Issue**: "Insufficient credits for fine-tuning"
- **Solution**: Add credits to your OpenAI account or reduce training data size
- **Estimate**: Check OpenAI's pricing page for cost estimates

#### Training Failures
- **Issue**: Job fails during training
- **Solution**: Check training data quality and format
- **Debug**: Review error logs in the dashboard or API response

### Performance Issues

#### Slow Training
- **Cause**: Large dataset or complex model
- **Solution**: Consider reducing data size or using a smaller base model
- **Alternative**: Split large datasets into smaller batches

#### Poor Model Performance
- **Cause**: Insufficient or low-quality training data
- **Solution**: Increase data quality and quantity
- **Improvement**: Add more diverse examples and edge cases

## Advanced Features

### Custom Training Parameters

For advanced users, you can specify custom training parameters:

```python
response = requests.post(
    'http://localhost:5000/api/llm/fine-tuning/jobs',
    json={
        'training_data': training_data,
        'model': 'gpt-3.5-turbo',
        'suffix': 'advanced-model',
        'hyperparameters': {
            'n_epochs': 3,
            'batch_size': 1,
            'learning_rate_multiplier': 0.1
        }
    }
)
```

### Model Versioning

Implement model versioning for better management:

```python
# Create versioned model
response = requests.post(
    'http://localhost:5000/api/llm/fine-tuning/jobs',
    json={
        'training_data': training_data,
        'model': 'gpt-3.5-turbo',
        'suffix': 'customer-support-v2',
        'metadata': {
            'version': '2.0',
            'description': 'Improved customer support model',
            'training_date': '2024-12-25'
        }
    }
)
```

### Automated Retraining

Set up automated retraining workflows:

```python
import schedule
import time

def retrain_model():
    # Fetch new training data
    new_data = fetch_latest_training_data()
    
    # Create new fine-tuning job
    response = requests.post(
        'http://localhost:5000/api/llm/fine-tuning/jobs',
        json={
            'training_data': new_data,
            'model': 'gpt-3.5-turbo',
            'suffix': f'auto-retrain-{int(time.time())}'
        }
    )
    
    print(f"Automated retraining started: {response.json()['job_id']}")

# Schedule retraining every week
schedule.every().week.do(retrain_model)
```

## Integration Examples

### Chatbot Integration

```python
class CustomChatbot:
    def __init__(self, model_id):
        self.model_id = model_id
        self.api_base = 'http://localhost:5000/api/llm'
    
    def chat(self, message):
        response = requests.post(
            f'{self.api_base}/models/{self.model_id}/test',
            json={'prompt': message}
        )
        return response.json()['response']

# Use your fine-tuned model
bot = CustomChatbot('ft:gpt-3.5-turbo:your-org:custom:abc123')
response = bot.chat("How can I help you today?")
print(response)
```

### API Service Integration

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/chat', methods=['POST'])
def chat_endpoint():
    user_message = request.json['message']
    model_id = request.json.get('model_id', 'default-model')
    
    # Use fine-tuned model
    response = requests.post(
        f'http://localhost:5000/api/llm/models/{model_id}/test',
        json={'prompt': user_message}
    )
    
    return jsonify({
        'response': response.json()['response'],
        'model': model_id
    })

if __name__ == '__main__':
    app.run(port=8080)
```

## Security Considerations

### API Key Security
- Never commit API keys to version control
- Use environment variables or secure key management systems
- Rotate API keys regularly
- Monitor API key usage for unusual activity

### Data Privacy
- Ensure training data doesn't contain sensitive information
- Implement data anonymization when necessary
- Follow data protection regulations (GDPR, CCPA, etc.)
- Secure data transmission and storage

### Model Access Control
- Implement proper authentication for model access
- Use role-based access control for different user types
- Monitor model usage and access patterns
- Implement rate limiting to prevent abuse

## Conclusion

The LLM fine-tuning feature in the AI Agent platform provides a powerful way to create custom language models tailored to your specific needs. By following the guidelines and best practices outlined in this guide, you can successfully train, deploy, and manage custom models that enhance your applications and workflows.

For additional support or advanced use cases, please refer to the main documentation or contact our support team.

