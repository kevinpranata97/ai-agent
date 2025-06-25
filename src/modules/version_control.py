"""
Version Control Module
Handles Git operations and GitHub integration for tracking all changes.
"""

import os
import json
import logging
import subprocess
from typing import Dict, Any, List, Optional
from datetime import datetime
import git
from git import Repo, InvalidGitRepositoryError

class VersionControlModule:
    """
    Module responsible for version control operations and GitHub integration.
    """
    
    def __init__(self, repo_url: str = None, local_path: str = None):
        self.logger = logging.getLogger(__name__)
        self.repo_url = repo_url or "https://github.com/kevinpranata97/ai-agent.git"
        self.local_path = local_path or os.getcwd()
        self.repo = None
        
        # Initialize or connect to repository
        self._initialize_repository()
        
        self.logger.info("Version Control module initialized")
    
    def _initialize_repository(self):
        """Initialize or connect to the Git repository."""
        try:
            # Try to open existing repository
            self.repo = Repo(self.local_path)
            self.logger.info(f"Connected to existing repository at {self.local_path}")
        except InvalidGitRepositoryError:
            try:
                # Clone repository if it doesn't exist locally
                self.repo = Repo.clone_from(self.repo_url, self.local_path)
                self.logger.info(f"Cloned repository from {self.repo_url}")
            except Exception as e:
                # Initialize new repository
                self.repo = Repo.init(self.local_path)
                self.logger.info(f"Initialized new repository at {self.local_path}")
        except Exception as e:
            self.logger.error(f"Failed to initialize repository: {str(e)}")
            self.repo = None
    
    def commit_task_changes(self, task_id: str, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Commit changes related to a specific task.
        
        Args:
            task_id: Unique task identifier
            task: Task dictionary containing task information
            
        Returns:
            Dictionary containing commit information
        """
        if not self.repo:
            return {
                'status': 'failed',
                'error': 'Repository not initialized'
            }
        
        try:
            # Create a branch for the task if it doesn't exist
            branch_name = f"task-{task_id[:8]}"
            
            # Check if branch exists
            if branch_name not in [ref.name for ref in self.repo.refs]:
                # Create new branch
                self.repo.create_head(branch_name)
                self.logger.info(f"Created branch: {branch_name}")
            
            # Switch to task branch
            self.repo.heads[branch_name].checkout()
            
            # Add all changes
            self.repo.git.add('.')
            
            # Create commit message
            commit_message = self._create_commit_message(task_id, task)
            
            # Commit changes
            commit = self.repo.index.commit(commit_message)
            
            # Switch back to main branch
            self.repo.heads.main.checkout()
            
            # Merge task branch into main
            self.repo.git.merge(branch_name)
            
            commit_info = {
                'status': 'success',
                'commit_hash': commit.hexsha,
                'commit_message': commit_message,
                'branch': branch_name,
                'timestamp': datetime.now().isoformat(),
                'files_changed': len(commit.stats.files)
            }
            
            self.logger.info(f"Committed task {task_id} changes: {commit.hexsha}")
            
            return commit_info
            
        except Exception as e:
            self.logger.error(f"Failed to commit task changes: {str(e)}")
            return {
                'status': 'failed',
                'error': str(e)
            }
    
    def push_changes(self, branch: str = 'main') -> Dict[str, Any]:
        """
        Push changes to remote repository.
        
        Args:
            branch: Branch name to push
            
        Returns:
            Dictionary containing push information
        """
        if not self.repo:
            return {
                'status': 'failed',
                'error': 'Repository not initialized'
            }
        
        try:
            # Get remote origin
            origin = self.repo.remote('origin')
            
            # Push changes
            push_info = origin.push(branch)
            
            result = {
                'status': 'success',
                'branch': branch,
                'pushed_at': datetime.now().isoformat(),
                'remote_url': str(origin.url)
            }
            
            self.logger.info(f"Pushed changes to {branch}")
            
            return result
            
        except Exception as e:
            self.logger.error(f"Failed to push changes: {str(e)}")
            return {
                'status': 'failed',
                'error': str(e)
            }
    
    def create_pull_request(self, task_id: str, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a pull request for task changes.
        
        Args:
            task_id: Unique task identifier
            task: Task dictionary
            
        Returns:
            Dictionary containing pull request information
        """
        # This would integrate with GitHub API to create pull requests
        # For now, return a placeholder response
        
        branch_name = f"task-{task_id[:8]}"
        
        pr_info = {
            'status': 'created',
            'branch': branch_name,
            'title': f"Task {task_id[:8]}: {task['description'][:50]}...",
            'description': self._create_pr_description(task_id, task),
            'created_at': datetime.now().isoformat(),
            'url': f"https://github.com/kevinpranata97/ai-agent/pull/placeholder"
        }
        
        self.logger.info(f"Pull request created for task {task_id}")
        
        return pr_info
    
    def get_commit_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get commit history.
        
        Args:
            limit: Maximum number of commits to return
            
        Returns:
            List of commit information dictionaries
        """
        if not self.repo:
            return []
        
        try:
            commits = []
            
            for commit in self.repo.iter_commits(max_count=limit):
                commit_info = {
                    'hash': commit.hexsha,
                    'message': commit.message.strip(),
                    'author': str(commit.author),
                    'date': commit.committed_datetime.isoformat(),
                    'files_changed': len(commit.stats.files)
                }
                commits.append(commit_info)
            
            return commits
            
        except Exception as e:
            self.logger.error(f"Failed to get commit history: {str(e)}")
            return []
    
    def get_repository_status(self) -> Dict[str, Any]:
        """
        Get current repository status.
        
        Returns:
            Dictionary containing repository status information
        """
        if not self.repo:
            return {
                'status': 'not_initialized',
                'error': 'Repository not initialized'
            }
        
        try:
            # Get current branch
            current_branch = self.repo.active_branch.name
            
            # Get untracked files
            untracked_files = self.repo.untracked_files
            
            # Get modified files
            modified_files = [item.a_path for item in self.repo.index.diff(None)]
            
            # Get staged files
            staged_files = [item.a_path for item in self.repo.index.diff("HEAD")]
            
            # Get remote info
            remotes = [{'name': remote.name, 'url': str(remote.url)} for remote in self.repo.remotes]
            
            status = {
                'status': 'initialized',
                'current_branch': current_branch,
                'untracked_files': len(untracked_files),
                'modified_files': len(modified_files),
                'staged_files': len(staged_files),
                'remotes': remotes,
                'last_commit': {
                    'hash': self.repo.head.commit.hexsha,
                    'message': self.repo.head.commit.message.strip(),
                    'date': self.repo.head.commit.committed_datetime.isoformat()
                }
            }
            
            return status
            
        except Exception as e:
            self.logger.error(f"Failed to get repository status: {str(e)}")
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def create_tag(self, tag_name: str, message: str = None) -> Dict[str, Any]:
        """
        Create a Git tag.
        
        Args:
            tag_name: Name of the tag
            message: Optional tag message
            
        Returns:
            Dictionary containing tag information
        """
        if not self.repo:
            return {
                'status': 'failed',
                'error': 'Repository not initialized'
            }
        
        try:
            # Create tag
            tag = self.repo.create_tag(tag_name, message=message or f"Tag {tag_name}")
            
            tag_info = {
                'status': 'success',
                'tag_name': tag_name,
                'message': message,
                'commit_hash': tag.commit.hexsha,
                'created_at': datetime.now().isoformat()
            }
            
            self.logger.info(f"Created tag: {tag_name}")
            
            return tag_info
            
        except Exception as e:
            self.logger.error(f"Failed to create tag: {str(e)}")
            return {
                'status': 'failed',
                'error': str(e)
            }
    
    def backup_repository(self, backup_path: str) -> Dict[str, Any]:
        """
        Create a backup of the repository.
        
        Args:
            backup_path: Path where to create the backup
            
        Returns:
            Dictionary containing backup information
        """
        if not self.repo:
            return {
                'status': 'failed',
                'error': 'Repository not initialized'
            }
        
        try:
            # Create backup directory
            os.makedirs(backup_path, exist_ok=True)
            
            # Clone repository to backup location
            backup_repo = Repo.clone_from(self.local_path, backup_path)
            
            backup_info = {
                'status': 'success',
                'backup_path': backup_path,
                'created_at': datetime.now().isoformat(),
                'size': self._get_directory_size(backup_path)
            }
            
            self.logger.info(f"Repository backed up to: {backup_path}")
            
            return backup_info
            
        except Exception as e:
            self.logger.error(f"Failed to backup repository: {str(e)}")
            return {
                'status': 'failed',
                'error': str(e)
            }
    
    def sync_with_remote(self) -> Dict[str, Any]:
        """
        Sync local repository with remote.
        
        Returns:
            Dictionary containing sync information
        """
        if not self.repo:
            return {
                'status': 'failed',
                'error': 'Repository not initialized'
            }
        
        try:
            # Fetch from remote
            origin = self.repo.remote('origin')
            fetch_info = origin.fetch()
            
            # Pull changes
            pull_info = origin.pull()
            
            sync_info = {
                'status': 'success',
                'fetched_refs': len(fetch_info),
                'pulled_changes': len(pull_info),
                'synced_at': datetime.now().isoformat()
            }
            
            self.logger.info("Repository synced with remote")
            
            return sync_info
            
        except Exception as e:
            self.logger.error(f"Failed to sync with remote: {str(e)}")
            return {
                'status': 'failed',
                'error': str(e)
            }
    
    def _create_commit_message(self, task_id: str, task: Dict[str, Any]) -> str:
        """Create a descriptive commit message for a task."""
        task_type = task.get('type', 'general')
        description = task['description'][:50]
        
        commit_message = f"[{task_type.upper()}] {description}...\n\n"
        commit_message += f"Task ID: {task_id}\n"
        commit_message += f"Description: {task['description']}\n"
        commit_message += f"Created: {task.get('created_at', 'Unknown')}\n"
        commit_message += f"Status: {task.get('status', 'Unknown')}\n"
        
        if 'plan' in task:
            plan = task['plan']
            commit_message += f"Steps: {plan.get('execution_plan', {}).get('total_steps', 'Unknown')}\n"
        
        commit_message += f"\nCommitted by AI Agent at {datetime.now().isoformat()}"
        
        return commit_message
    
    def _create_pr_description(self, task_id: str, task: Dict[str, Any]) -> str:
        """Create a pull request description for a task."""
        description = f"## Task: {task['description']}\n\n"
        description += f"**Task ID:** {task_id}\n"
        description += f"**Type:** {task.get('type', 'general')}\n"
        description += f"**Priority:** {task.get('priority', 'medium')}\n"
        description += f"**Created:** {task.get('created_at', 'Unknown')}\n\n"
        
        if 'plan' in task:
            plan = task['plan']
            description += "## Execution Plan\n\n"
            
            if 'execution_plan' in plan:
                steps = plan['execution_plan'].get('steps', [])
                for step in steps:
                    description += f"- **{step.get('title', 'Unknown')}**: {step.get('description', 'No description')}\n"
            
            description += f"\n**Estimated Time:** {plan.get('resource_estimate', {}).get('estimated_time_minutes', 'Unknown')} minutes\n"
        
        description += "\n## Changes\n\n"
        description += "This pull request contains all changes made by the AI Agent for this task.\n"
        
        description += f"\n---\n*Generated by AI Agent on {datetime.now().isoformat()}*"
        
        return description
    
    def _get_directory_size(self, path: str) -> str:
        """Get the size of a directory in human-readable format."""
        total_size = 0
        
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                try:
                    total_size += os.path.getsize(filepath)
                except OSError:
                    pass
        
        # Convert to human-readable format
        for unit in ['B', 'KB', 'MB', 'GB']:
            if total_size < 1024.0:
                return f"{total_size:.1f} {unit}"
            total_size /= 1024.0
        
        return f"{total_size:.1f} TB"
    
    def get_file_history(self, file_path: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get commit history for a specific file.
        
        Args:
            file_path: Path to the file
            limit: Maximum number of commits to return
            
        Returns:
            List of commit information for the file
        """
        if not self.repo:
            return []
        
        try:
            commits = []
            
            for commit in self.repo.iter_commits(paths=file_path, max_count=limit):
                commit_info = {
                    'hash': commit.hexsha,
                    'message': commit.message.strip(),
                    'author': str(commit.author),
                    'date': commit.committed_datetime.isoformat()
                }
                commits.append(commit_info)
            
            return commits
            
        except Exception as e:
            self.logger.error(f"Failed to get file history: {str(e)}")
            return []

