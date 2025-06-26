"""
LLM Fine-Tuning Module
Handles OpenAI LLM fine-tuning operations for the AI agent.
"""

import os
import json
import time
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
from openai import OpenAI
from utils.logging import setup_logging

logger = setup_logging(__name__)

class LLMFineTuningModule:
    """
    Module for managing OpenAI LLM fine-tuning operations.
    
    This module provides functionality to:
    - Prepare training data for fine-tuning
    - Upload training data to OpenAI
    - Create and monitor fine-tuning jobs
    - Manage fine-tuned models
    - Validate and test fine-tuned models
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the LLM Fine-Tuning Module.
        
        Args:
            api_key: OpenAI API key. If not provided, will try to get from environment.
        """
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable or pass api_key parameter.")
        
        self.client = OpenAI(api_key=self.api_key)
        self.fine_tuning_jobs = {}
        self.fine_tuned_models = {}
        
        logger.info("LLM Fine-Tuning Module initialized")
    
    def prepare_training_data(self, data: List[Dict[str, Any]], output_file: str, format_type: str = "chat") -> str:
        """
        Prepare training data in the correct format for OpenAI fine-tuning.
        
        Args:
            data: List of training examples
            output_file: Path to save the formatted training data
            format_type: Format type ('chat' for chat models, 'completion' for completion models)
        
        Returns:
            Path to the prepared training data file
        """
        logger.info(f"Preparing training data with {len(data)} examples")
        
        formatted_data = []
        
        for example in data:
            if format_type == "chat":
                # Format for chat models (gpt-3.5-turbo, gpt-4)
                if "messages" in example:
                    formatted_example = {"messages": example["messages"]}
                else:
                    # Convert prompt/completion to chat format
                    messages = []
                    if "system" in example:
                        messages.append({"role": "system", "content": example["system"]})
                    if "prompt" in example:
                        messages.append({"role": "user", "content": example["prompt"]})
                    if "completion" in example:
                        messages.append({"role": "assistant", "content": example["completion"]})
                    formatted_example = {"messages": messages}
            else:
                # Format for completion models (davinci, curie, etc.)
                formatted_example = {
                    "prompt": example.get("prompt", ""),
                    "completion": example.get("completion", "")
                }
            
            formatted_data.append(formatted_example)
        
        # Save to JSONL format
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            for example in formatted_data:
                f.write(json.dumps(example, ensure_ascii=False) + '\n')
        
        logger.info(f"Training data prepared and saved to {output_file}")
        return output_file
    
    def validate_training_data(self, file_path: str) -> Dict[str, Any]:
        """
        Validate training data format and quality.
        
        Args:
            file_path: Path to the training data file
        
        Returns:
            Validation results with statistics and potential issues
        """
        logger.info(f"Validating training data: {file_path}")
        
        validation_results = {
            "valid": True,
            "total_examples": 0,
            "issues": [],
            "statistics": {}
        }
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                examples = []
                for line_num, line in enumerate(f, 1):
                    try:
                        example = json.loads(line.strip())
                        examples.append(example)
                    except json.JSONDecodeError as e:
                        validation_results["issues"].append(f"Line {line_num}: Invalid JSON - {str(e)}")
                        validation_results["valid"] = False
                
                validation_results["total_examples"] = len(examples)
                
                # Check format consistency
                if examples:
                    first_example = examples[0]
                    if "messages" in first_example:
                        # Chat format validation
                        for i, example in enumerate(examples):
                            if "messages" not in example:
                                validation_results["issues"].append(f"Example {i+1}: Missing 'messages' field")
                                validation_results["valid"] = False
                            elif not isinstance(example["messages"], list):
                                validation_results["issues"].append(f"Example {i+1}: 'messages' must be a list")
                                validation_results["valid"] = False
                    else:
                        # Completion format validation
                        for i, example in enumerate(examples):
                            if "prompt" not in example or "completion" not in example:
                                validation_results["issues"].append(f"Example {i+1}: Missing 'prompt' or 'completion' field")
                                validation_results["valid"] = False
                
                # Calculate statistics
                validation_results["statistics"] = {
                    "total_examples": len(examples),
                    "avg_prompt_length": 0,
                    "avg_completion_length": 0,
                    "min_examples_recommended": 50,
                    "sufficient_data": len(examples) >= 50
                }
                
                if examples and "messages" in examples[0]:
                    # Chat format statistics
                    prompt_lengths = []
                    completion_lengths = []
                    for example in examples:
                        for message in example.get("messages", []):
                            if message.get("role") == "user":
                                prompt_lengths.append(len(message.get("content", "")))
                            elif message.get("role") == "assistant":
                                completion_lengths.append(len(message.get("content", "")))
                    
                    if prompt_lengths:
                        validation_results["statistics"]["avg_prompt_length"] = sum(prompt_lengths) / len(prompt_lengths)
                    if completion_lengths:
                        validation_results["statistics"]["avg_completion_length"] = sum(completion_lengths) / len(completion_lengths)
                
        except Exception as e:
            validation_results["valid"] = False
            validation_results["issues"].append(f"File reading error: {str(e)}")
        
        logger.info(f"Validation completed. Valid: {validation_results['valid']}, Issues: {len(validation_results['issues'])}")
        return validation_results
    
    def upload_training_file(self, file_path: str) -> str:
        """
        Upload training data file to OpenAI.
        
        Args:
            file_path: Path to the training data file
        
        Returns:
            File ID from OpenAI
        """
        logger.info(f"Uploading training file: {file_path}")
        
        try:
            with open(file_path, 'rb') as f:
                response = self.client.files.create(
                    file=f,
                    purpose="fine-tune"
                )
            
            file_id = response.id
            logger.info(f"Training file uploaded successfully. File ID: {file_id}")
            return file_id
            
        except Exception as e:
            logger.error(f"Failed to upload training file: {str(e)}")
            raise
    
    def create_fine_tuning_job(self, training_file_id: str, model: str = "gpt-3.5-turbo", 
                              hyperparameters: Optional[Dict[str, Any]] = None,
                              suffix: Optional[str] = None) -> str:
        """
        Create a fine-tuning job.
        
        Args:
            training_file_id: ID of the uploaded training file
            model: Base model to fine-tune
            hyperparameters: Optional hyperparameters for fine-tuning
            suffix: Optional suffix for the fine-tuned model name
        
        Returns:
            Fine-tuning job ID
        """
        logger.info(f"Creating fine-tuning job for model: {model}")
        
        job_params = {
            "training_file": training_file_id,
            "model": model
        }
        
        if hyperparameters:
            job_params["hyperparameters"] = hyperparameters
        
        if suffix:
            job_params["suffix"] = suffix
        
        try:
            response = self.client.fine_tuning.jobs.create(**job_params)
            job_id = response.id
            
            # Store job information
            self.fine_tuning_jobs[job_id] = {
                "id": job_id,
                "model": model,
                "training_file": training_file_id,
                "status": response.status,
                "created_at": datetime.now().isoformat(),
                "hyperparameters": hyperparameters,
                "suffix": suffix
            }
            
            logger.info(f"Fine-tuning job created successfully. Job ID: {job_id}")
            return job_id
            
        except Exception as e:
            logger.error(f"Failed to create fine-tuning job: {str(e)}")
            raise
    
    def get_job_status(self, job_id: str) -> Dict[str, Any]:
        """
        Get the status of a fine-tuning job.
        
        Args:
            job_id: Fine-tuning job ID
        
        Returns:
            Job status information
        """
        try:
            response = self.client.fine_tuning.jobs.retrieve(job_id)
            
            status_info = {
                "id": response.id,
                "status": response.status,
                "model": response.model,
                "created_at": response.created_at,
                "finished_at": response.finished_at,
                "fine_tuned_model": response.fine_tuned_model,
                "training_file": response.training_file,
                "validation_file": response.validation_file,
                "result_files": response.result_files,
                "trained_tokens": response.trained_tokens
            }
            
            # Update local storage
            if job_id in self.fine_tuning_jobs:
                self.fine_tuning_jobs[job_id].update(status_info)
            
            return status_info
            
        except Exception as e:
            logger.error(f"Failed to get job status for {job_id}: {str(e)}")
            raise
    
    def monitor_job(self, job_id: str, check_interval: int = 60) -> Dict[str, Any]:
        """
        Monitor a fine-tuning job until completion.
        
        Args:
            job_id: Fine-tuning job ID
            check_interval: Interval in seconds between status checks
        
        Returns:
            Final job status
        """
        logger.info(f"Monitoring fine-tuning job: {job_id}")
        
        while True:
            status_info = self.get_job_status(job_id)
            status = status_info["status"]
            
            logger.info(f"Job {job_id} status: {status}")
            
            if status in ["succeeded", "failed", "cancelled"]:
                if status == "succeeded":
                    fine_tuned_model = status_info["fine_tuned_model"]
                    self.fine_tuned_models[fine_tuned_model] = status_info
                    logger.info(f"Fine-tuning completed successfully. Model: {fine_tuned_model}")
                else:
                    logger.error(f"Fine-tuning job failed with status: {status}")
                
                return status_info
            
            time.sleep(check_interval)
    
    def list_fine_tuned_models(self) -> List[Dict[str, Any]]:
        """
        List all fine-tuned models.
        
        Returns:
            List of fine-tuned model information
        """
        try:
            response = self.client.models.list()
            fine_tuned_models = []
            
            for model in response.data:
                if model.id.startswith("ft:"):
                    fine_tuned_models.append({
                        "id": model.id,
                        "created": model.created,
                        "owned_by": model.owned_by,
                        "object": model.object
                    })
            
            logger.info(f"Found {len(fine_tuned_models)} fine-tuned models")
            return fine_tuned_models
            
        except Exception as e:
            logger.error(f"Failed to list fine-tuned models: {str(e)}")
            raise
    
    def test_fine_tuned_model(self, model_id: str, test_prompts: List[str]) -> List[Dict[str, Any]]:
        """
        Test a fine-tuned model with sample prompts.
        
        Args:
            model_id: Fine-tuned model ID
            test_prompts: List of test prompts
        
        Returns:
            List of test results
        """
        logger.info(f"Testing fine-tuned model: {model_id}")
        
        test_results = []
        
        for i, prompt in enumerate(test_prompts):
            try:
                response = self.client.chat.completions.create(
                    model=model_id,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=150,
                    temperature=0.7
                )
                
                result = {
                    "test_id": i + 1,
                    "prompt": prompt,
                    "response": response.choices[0].message.content,
                    "usage": {
                        "prompt_tokens": response.usage.prompt_tokens,
                        "completion_tokens": response.usage.completion_tokens,
                        "total_tokens": response.usage.total_tokens
                    },
                    "success": True
                }
                
            except Exception as e:
                result = {
                    "test_id": i + 1,
                    "prompt": prompt,
                    "response": None,
                    "error": str(e),
                    "success": False
                }
            
            test_results.append(result)
        
        logger.info(f"Model testing completed. {len(test_results)} tests run")
        return test_results
    
    def delete_fine_tuned_model(self, model_id: str) -> bool:
        """
        Delete a fine-tuned model.
        
        Args:
            model_id: Fine-tuned model ID
        
        Returns:
            True if successful, False otherwise
        """
        try:
            response = self.client.models.delete(model_id)
            
            if model_id in self.fine_tuned_models:
                del self.fine_tuned_models[model_id]
            
            logger.info(f"Fine-tuned model deleted: {model_id}")
            return response.deleted
            
        except Exception as e:
            logger.error(f"Failed to delete model {model_id}: {str(e)}")
            return False
    
    def get_job_events(self, job_id: str) -> List[Dict[str, Any]]:
        """
        Get events for a fine-tuning job.
        
        Args:
            job_id: Fine-tuning job ID
        
        Returns:
            List of job events
        """
        try:
            response = self.client.fine_tuning.jobs.list_events(fine_tuning_job_id=job_id)
            
            events = []
            for event in response.data:
                events.append({
                    "id": event.id,
                    "created_at": event.created_at,
                    "level": event.level,
                    "message": event.message,
                    "object": event.object
                })
            
            return events
            
        except Exception as e:
            logger.error(f"Failed to get job events for {job_id}: {str(e)}")
            raise
    
    def cancel_job(self, job_id: str) -> bool:
        """
        Cancel a running fine-tuning job.
        
        Args:
            job_id: Fine-tuning job ID
        
        Returns:
            True if successful, False otherwise
        """
        try:
            response = self.client.fine_tuning.jobs.cancel(job_id)
            
            if job_id in self.fine_tuning_jobs:
                self.fine_tuning_jobs[job_id]["status"] = "cancelled"
            
            logger.info(f"Fine-tuning job cancelled: {job_id}")
            return response.status == "cancelled"
            
        except Exception as e:
            logger.error(f"Failed to cancel job {job_id}: {str(e)}")
            return False
    
    def export_model_info(self, output_file: str) -> str:
        """
        Export information about fine-tuned models to a file.
        
        Args:
            output_file: Path to save the model information
        
        Returns:
            Path to the exported file
        """
        model_info = {
            "fine_tuning_jobs": self.fine_tuning_jobs,
            "fine_tuned_models": self.fine_tuned_models,
            "exported_at": datetime.now().isoformat()
        }
        
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(model_info, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Model information exported to {output_file}")
        return output_file
    
    def get_usage_statistics(self) -> Dict[str, Any]:
        """
        Get usage statistics for fine-tuning operations.
        
        Returns:
            Usage statistics
        """
        stats = {
            "total_jobs": len(self.fine_tuning_jobs),
            "successful_jobs": 0,
            "failed_jobs": 0,
            "active_jobs": 0,
            "total_models": len(self.fine_tuned_models),
            "total_tokens_trained": 0
        }
        
        for job_info in self.fine_tuning_jobs.values():
            status = job_info.get("status", "unknown")
            if status == "succeeded":
                stats["successful_jobs"] += 1
            elif status == "failed":
                stats["failed_jobs"] += 1
            elif status in ["running", "pending"]:
                stats["active_jobs"] += 1
            
            trained_tokens = job_info.get("trained_tokens", 0)
            if trained_tokens:
                stats["total_tokens_trained"] += trained_tokens
        
        return stats

