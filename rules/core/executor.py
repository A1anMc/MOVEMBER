"""
Action Executor

Handles execution of rule actions with support for built-in actions
and custom executors.
"""

from typing import List, Dict, Any, Optional, Callable
import logging
import time
import asyncio
from datetime import datetime
import json
import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import re

from ..types import Action, ActionResult, ExecutionContext

logger = logging.getLogger(__name__)


class ActionExecutor:
    """Executes rule actions."""
    
    def __init__(self):
        self.built_in_actions = {
            'log_message': self._log_message,
            'send_email': self._send_email,
            'send_webhook': self._send_webhook,
            'update_data': self._update_data,
            'validate_data': self._validate_data,
            'notify_user': self._notify_user,
            'trigger_workflow': self._trigger_workflow,
            'store_result': self._store_result,
            'raise_alert': self._raise_alert,
            'approve_request': self._approve_request,
            'reject_request': self._reject_request,
            'schedule_task': self._schedule_task,
            'update_status': self._update_status
        }
        
        # Custom action registry
        self.custom_actions: Dict[str, Callable] = {}
    
    def register_custom_action(self, name: str, executor: Callable) -> None:
        """Register a custom action executor."""
        self.custom_actions[name] = executor
        logger.info(f"Registered custom action: {name}")
    
    def execute_action(self, action: Action, context: ExecutionContext) -> ActionResult:
        """Execute a single action."""
        start_time = time.time()
        
        try:
            # Find the executor
            executor = self._get_executor(action)
            
            if executor is None:
                raise ValueError(f"No executor found for action: {action.name}")
            
            # Execute the action
            if asyncio.iscoroutinefunction(executor):
                # For async executors, we need to run in event loop
                loop = asyncio.get_event_loop()
                result = loop.run_until_complete(executor(action, context))
            else:
                result = executor(action, context)
            
            execution_time = time.time() - start_time
            
            return ActionResult(
                action_name=action.name,
                success=True,
                result=result,
                execution_time=execution_time
            )
            
        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(f"Action execution failed: {action.name}", exc_info=e)
            
            return ActionResult(
                action_name=action.name,
                success=False,
                error=str(e),
                execution_time=execution_time
            )
    
    async def execute_action_async(self, action: Action, context: ExecutionContext) -> ActionResult:
        """Execute a single action asynchronously."""
        start_time = time.time()
        
        try:
            # Find the executor
            executor = self._get_executor(action)
            
            if executor is None:
                raise ValueError(f"No executor found for action: {action.name}")
            
            # Execute the action
            if asyncio.iscoroutinefunction(executor):
                result = await executor(action, context)
            else:
                # For sync executors, run in thread pool
                loop = asyncio.get_event_loop()
                result = await loop.run_in_executor(None, executor, action, context)
            
            execution_time = time.time() - start_time
            
            return ActionResult(
                action_name=action.name,
                success=True,
                result=result,
                execution_time=execution_time
            )
            
        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(f"Action execution failed: {action.name}", exc_info=e)
            
            return ActionResult(
                action_name=action.name,
                success=False,
                error=str(e),
                execution_time=execution_time
            )
    
    def execute_actions(self, actions: List[Action], context: ExecutionContext) -> List[ActionResult]:
        """Execute multiple actions."""
        results = []
        
        for action in actions:
            result = self.execute_action(action, context)
            results.append(result)
            
            # If action failed and retry is enabled, attempt retries
            if not result.success and action.retry_on_failure:
                for attempt in range(action.max_retries):
                    logger.info(f"Retrying action {action.name}, attempt {attempt + 1}")
                    time.sleep(1)  # Brief delay before retry
                    
                    retry_result = self.execute_action(action, context)
                    results.append(retry_result)
                    
                    if retry_result.success:
                        break
        
        return results
    
    async def execute_actions_async(self, actions: List[Action], context: ExecutionContext) -> List[ActionResult]:
        """Execute multiple actions asynchronously."""
        tasks = []
        
        for action in actions:
            task = self.execute_action_async(action, context)
            tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results and handle retries
        final_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                # Handle exception
                action = actions[i]
                final_results.append(ActionResult(
                    action_name=action.name,
                    success=False,
                    error=str(result),
                    execution_time=0
                ))
            else:
                final_results.append(result)
                
                # Handle retries for failed actions
                if not result.success and actions[i].retry_on_failure:
                    for attempt in range(actions[i].max_retries):
                        logger.info(f"Retrying action {actions[i].name}, attempt {attempt + 1}")
                        await asyncio.sleep(1)  # Brief delay before retry
                        
                        retry_result = await self.execute_action_async(actions[i], context)
                        final_results.append(retry_result)
                        
                        if retry_result.success:
                            break
        
        return final_results
    
    def _get_executor(self, action: Action) -> Optional[Callable]:
        """Get the executor for an action."""
        # Check custom executor first
        if action.custom_executor:
            return action.custom_executor
        
        # Check custom actions registry
        if action.name in self.custom_actions:
            return self.custom_actions[action.name]
        
        # Check built-in actions
        if action.name in self.built_in_actions:
            return self.built_in_actions[action.name]
        
        return None
    
    # Built-in action executors
    
    def _log_message(self, action: Action, context: ExecutionContext) -> str:
        """Log a message."""
        message = action.parameters.get('message', 'No message provided')
        level = action.parameters.get('level', 'INFO')
        
        log_message = f"[{context.context_type.value}] {message}"
        
        if level.upper() == 'ERROR':
            logger.error(log_message)
        elif level.upper() == 'WARNING':
            logger.warning(log_message)
        elif level.upper() == 'DEBUG':
            logger.debug(log_message)
        else:
            logger.info(log_message)
        
        return f"Logged message: {message}"
    
    def _send_email(self, action: Action, context: ExecutionContext) -> str:
        """Send an email."""
        to_email = action.parameters.get('to_email')
        subject = action.parameters.get('subject', 'Rule Engine Notification')
        body = action.parameters.get('body', '')
        
        if not to_email:
            raise ValueError("Email address is required")
        
        # This is a simplified email sender
        # In production, you'd use a proper email service
        logger.info(f"Would send email to {to_email}: {subject}")
        
        return f"Email sent to {to_email}"
    
    def _send_webhook(self, action: Action, context: ExecutionContext) -> str:
        """Send a webhook."""
        url = action.parameters.get('url')
        method = action.parameters.get('method', 'POST')
        data = action.parameters.get('data', {})
        headers = action.parameters.get('headers', {})
        
        if not url:
            raise ValueError("Webhook URL is required")
        
        try:
            response = requests.request(
                method=method,
                url=url,
                json=data,
                headers=headers,
                timeout=30
            )
            response.raise_for_status()
            
            return f"Webhook sent to {url}, status: {response.status_code}"
            
        except requests.RequestException as e:
            raise Exception(f"Webhook request failed: {e}")
    
    def _update_data(self, action: Action, context: ExecutionContext) -> str:
        """Update data in the context."""
        updates = action.parameters.get('updates', {})
        
        for key, value in updates.items():
            context.data[key] = value
        
        return f"Updated {len(updates)} data fields"
    
    def _validate_data(self, action: Action, context: ExecutionContext) -> str:
        """Validate data in the context."""
        validations = action.parameters.get('validations', {})
        errors = []
        
        for field, rules in validations.items():
            value = context.data.get(field)
            
            for rule in rules:
                if rule['type'] == 'required' and not value:
                    errors.append(f"{field} is required")
                elif rule['type'] == 'min_length' and len(str(value)) < rule['value']:
                    errors.append(f"{field} must be at least {rule['value']} characters")
                elif rule['type'] == 'max_length' and len(str(value)) > rule['value']:
                    errors.append(f"{field} must be at most {rule['value']} characters")
                elif rule['type'] == 'pattern' and not re.match(rule['value'], str(value)):
                    errors.append(f"{field} does not match pattern {rule['value']}")
        
        if errors:
            raise ValueError(f"Validation failed: {'; '.join(errors)}")
        
        return "Data validation passed"
    
    def _notify_user(self, action: Action, context: ExecutionContext) -> str:
        """Notify a user."""
        user_id = action.parameters.get('user_id') or context.user_id
        message = action.parameters.get('message', 'Notification from rule engine')
        notification_type = action.parameters.get('type', 'info')
        
        if not user_id:
            raise ValueError("User ID is required for notification")
        
        # This is a simplified notification
        # In production, you'd integrate with a notification service
        logger.info(f"Would notify user {user_id}: {message}")
        
        return f"Notification sent to user {user_id}"
    
    def _trigger_workflow(self, action: Action, context: ExecutionContext) -> str:
        """Trigger a workflow."""
        workflow_name = action.parameters.get('workflow_name')
        workflow_data = action.parameters.get('workflow_data', {})
        
        if not workflow_name:
            raise ValueError("Workflow name is required")
        
        # This is a simplified workflow trigger
        # In production, you'd integrate with a workflow engine
        logger.info(f"Would trigger workflow {workflow_name} with data {workflow_data}")
        
        return f"Workflow {workflow_name} triggered"
    
    def _store_result(self, action: Action, context: ExecutionContext) -> str:
        """Store a result."""
        key = action.parameters.get('key')
        value = action.parameters.get('value')
        
        if not key:
            raise ValueError("Storage key is required")
        
        # This is a simplified storage
        # In production, you'd use a proper storage service
        logger.info(f"Would store {key}: {value}")
        
        return f"Result stored with key {key}"
    
    def _raise_alert(self, action: Action, context: ExecutionContext) -> str:
        """Raise an alert."""
        alert_type = action.parameters.get('type', 'warning')
        message = action.parameters.get('message', 'Alert from rule engine')
        severity = action.parameters.get('severity', 'medium')
        
        # This is a simplified alert
        # In production, you'd integrate with an alerting service
        logger.warning(f"ALERT [{severity.upper()}]: {message}")
        
        return f"Alert raised: {message}"
    
    def _approve_request(self, action: Action, context: ExecutionContext) -> str:
        """Approve a request."""
        request_id = action.parameters.get('request_id')
        reason = action.parameters.get('reason', 'Approved by rule engine')
        
        if not request_id:
            raise ValueError("Request ID is required")
        
        # This is a simplified approval
        # In production, you'd update the request status in your system
        logger.info(f"Would approve request {request_id}: {reason}")
        
        return f"Request {request_id} approved"
    
    def _reject_request(self, action: Action, context: ExecutionContext) -> str:
        """Reject a request."""
        request_id = action.parameters.get('request_id')
        reason = action.parameters.get('reason', 'Rejected by rule engine')
        
        if not request_id:
            raise ValueError("Request ID is required")
        
        # This is a simplified rejection
        # In production, you'd update the request status in your system
        logger.info(f"Would reject request {request_id}: {reason}")
        
        return f"Request {request_id} rejected"
    
    def _schedule_task(self, action: Action, context: ExecutionContext) -> str:
        """Schedule a task."""
        task_name = action.parameters.get('task_name')
        delay_seconds = action.parameters.get('delay_seconds', 0)
        
        if not task_name:
            raise ValueError("Task name is required")
        
        # This is a simplified task scheduling
        # In production, you'd use a proper task scheduler
        logger.info(f"Would schedule task {task_name} with {delay_seconds}s delay")
        
        return f"Task {task_name} scheduled"
    
    def _update_status(self, action: Action, context: ExecutionContext) -> str:
        """Update a status."""
        status = action.parameters.get('status')
        entity_id = action.parameters.get('entity_id')
        
        if not status or not entity_id:
            raise ValueError("Status and entity_id are required")
        
        # This is a simplified status update
        # In production, you'd update the status in your system
        logger.info(f"Would update status of {entity_id} to {status}")
        
        return f"Status updated to {status}" 