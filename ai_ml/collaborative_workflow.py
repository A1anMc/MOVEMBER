#!/usr/bin/env python3
"""
Collaborative Workflow System
Manages team collaboration, task distribution, and real-time coordination
"""

import asyncio
import logging
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, asdict
from enum import Enum
import secrets
import threading
import queue
import time
import numpy as np

logger = logging.getLogger(__name__)

class TaskStatus(Enum):
    """Task status enumeration."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    REVIEW = "review"
    COMPLETED = "completed"
    BLOCKED = "blocked"
    CANCELLED = "cancelled"

class TaskPriority(Enum):
    """Task priority levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class WorkflowType(Enum):
    """Types of collaborative workflows."""
    DATA_PREPARATION = "data_preparation"
    MODEL_TRAINING = "model_training"
    FEATURE_ENGINEERING = "feature_engineering"
    MODEL_EVALUATION = "model_evaluation"
    DEPLOYMENT = "deployment"
    MAINTENANCE = "maintenance"

@dataclass
class CollaborativeTask:
    """Task in collaborative workflow."""
    task_id: str
    title: str
    description: str
    workflow_type: WorkflowType
    status: TaskStatus
    priority: TaskPriority
    assigned_to: List[str]
    dependencies: List[str]
    created_by: str
    created_at: datetime
    due_date: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    progress: float = 0.0
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}

@dataclass
class WorkflowSession:
    """Active workflow session."""
    session_id: str
    name: str
    workflow_type: WorkflowType
    participants: List[str]
    tasks: List[str]
    start_time: datetime
    end_time: Optional[datetime] = None
    status: str = "active"
    progress: float = 0.0
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}

@dataclass
class CollaborationEvent:
    """Event in collaborative workflow."""
    event_id: str
    session_id: str
    event_type: str
    participant: str
    timestamp: datetime
    data: Dict[str, Any]
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}

class CollaborativeWorkflow:
    """Collaborative workflow management system."""
    
    def __init__(self):
        self.tasks: Dict[str, CollaborativeTask] = {}
        self.sessions: Dict[str, WorkflowSession] = {}
        self.events: List[CollaborationEvent] = []
        
        # Real-time coordination
        self.task_queue = queue.Queue()
        self.event_queue = queue.Queue()
        self.notification_queue = queue.Queue()
        
        # Performance tracking
        self.total_tasks = 0
        self.completed_tasks = 0
        self.average_completion_time = 0.0
        
        # Start background workers
        self._start_background_workers()
        
        logger.info("Collaborative Workflow System initialized")
    
    def _start_background_workers(self):
        """Start background workers for real-time coordination."""
        
        # Task processing worker
        self.task_worker = threading.Thread(target=self._task_processing_worker, daemon=True)
        self.task_worker.start()
        
        # Event processing worker
        self.event_worker = threading.Thread(target=self._event_processing_worker, daemon=True)
        self.event_worker.start()
        
        # Notification worker
        self.notification_worker = threading.Thread(target=self._notification_worker, daemon=True)
        self.notification_worker.start()
        
        logger.info("Background workers started")
    
    def _task_processing_worker(self):
        """Background worker for task processing."""
        while True:
            try:
                if not self.task_queue.empty():
                    task_data = self.task_queue.get()
                    self._process_task_update(task_data)
                time.sleep(0.1)
            except Exception as e:
                logger.error(f"Task processing worker error: {e}")
    
    def _event_processing_worker(self):
        """Background worker for event processing."""
        while True:
            try:
                if not self.event_queue.empty():
                    event_data = self.event_queue.get()
                    self._process_collaboration_event(event_data)
                time.sleep(0.1)
            except Exception as e:
                logger.error(f"Event processing worker error: {e}")
    
    def _notification_worker(self):
        """Background worker for notifications."""
        while True:
            try:
                if not self.notification_queue.empty():
                    notification = self.notification_queue.get()
                    self._send_notification(notification)
                time.sleep(0.2)
            except Exception as e:
                logger.error(f"Notification worker error: {e}")
    
    async def create_workflow_session(self, name: str, workflow_type: WorkflowType, 
                                    participants: List[str], description: str = "") -> str:
        """Create a new collaborative workflow session."""
        
        session_id = f"workflow_{secrets.token_urlsafe(8)}"
        
        session = WorkflowSession(
            session_id=session_id,
            name=name,
            workflow_type=workflow_type,
            participants=participants,
            tasks=[],
            start_time=datetime.now(),
            metadata={"description": description}
        )
        
        self.sessions[session_id] = session
        
        # Log event
        await self._log_event(session_id, "session_created", participants[0], {
            "session_name": name,
            "workflow_type": workflow_type.value,
            "participants": participants
        })
        
        logger.info(f"Workflow session created: {session_id} with {len(participants)} participants")
        return session_id
    
    async def create_task(self, session_id: str, title: str, description: str, 
                         assigned_to: List[str], priority: TaskPriority = TaskPriority.MEDIUM,
                         dependencies: List[str] = None, due_date: Optional[datetime] = None) -> str:
        """Create a new task in a workflow session."""
        
        if session_id not in self.sessions:
            raise ValueError(f"Session {session_id} not found")
        
        if dependencies is None:
            dependencies = []
        
        task_id = f"task_{secrets.token_urlsafe(8)}"
        
        task = CollaborativeTask(
            task_id=task_id,
            title=title,
            description=description,
            workflow_type=self.sessions[session_id].workflow_type,
            status=TaskStatus.PENDING,
            priority=priority,
            assigned_to=assigned_to,
            dependencies=dependencies,
            created_by=assigned_to[0] if assigned_to else "system",
            created_at=datetime.now(),
            due_date=due_date
        )
        
        self.tasks[task_id] = task
        self.sessions[session_id].tasks.append(task_id)
        
        # Queue for processing
        self.task_queue.put({
            "action": "task_created",
            "task_id": task_id,
            "session_id": session_id
        })
        
        # Log event
        await self._log_event(session_id, "task_created", task.created_by, {
            "task_id": task_id,
            "title": title,
            "assigned_to": assigned_to,
            "priority": priority.value
        })
        
        logger.info(f"Task created: {task_id} in session {session_id}")
        return task_id
    
    async def update_task_status(self, task_id: str, new_status: TaskStatus, 
                                updated_by: str, progress: Optional[float] = None,
                                notes: str = "") -> bool:
        """Update task status and progress."""
        
        if task_id not in self.tasks:
            logger.error(f"Task {task_id} not found")
            return False
        
        task = self.tasks[task_id]
        old_status = task.status
        
        # Update task
        task.status = new_status
        if progress is not None:
            task.progress = max(0.0, min(1.0, progress))
        
        if new_status == TaskStatus.COMPLETED:
            task.completed_at = datetime.now()
            self.completed_tasks += 1
        
        # Update metadata
        if "notes" not in task.metadata:
            task.metadata["notes"] = []
        task.metadata["notes"].append({
            "timestamp": datetime.now().isoformat(),
            "user": updated_by,
            "status_change": f"{old_status.value} -> {new_status.value}",
            "notes": notes
        })
        
        # Queue for processing
        self.task_queue.put({
            "action": "task_updated",
            "task_id": task_id,
            "old_status": old_status.value,
            "new_status": new_status.value,
            "updated_by": updated_by
        })
        
        # Log event
        session_id = self._get_session_for_task(task_id)
        if session_id:
            await self._log_event(session_id, "task_status_updated", updated_by, {
                "task_id": task_id,
                "old_status": old_status.value,
                "new_status": new_status.value,
                "progress": task.progress
            })
        
        logger.info(f"Task {task_id} status updated to {new_status.value} by {updated_by}")
        return True
    
    async def assign_task(self, task_id: str, assigned_to: List[str], 
                         assigned_by: str) -> bool:
        """Reassign task to different participants."""
        
        if task_id not in self.tasks:
            logger.error(f"Task {task_id} not found")
            return False
        
        task = self.tasks[task_id]
        old_assignees = task.assigned_to.copy()
        
        task.assigned_to = assigned_to
        
        # Log event
        session_id = self._get_session_for_task(task_id)
        if session_id:
            await self._log_event(session_id, "task_reassigned", assigned_by, {
                "task_id": task_id,
                "old_assignees": old_assignees,
                "new_assignees": assigned_to
            })
        
        logger.info(f"Task {task_id} reassigned from {old_assignees} to {assigned_to}")
        return True
    
    async def add_task_dependency(self, task_id: str, dependency_id: str, 
                                 added_by: str) -> bool:
        """Add dependency between tasks."""
        
        if task_id not in self.tasks or dependency_id not in self.tasks:
            logger.error(f"Task or dependency not found")
            return False
        
        task = self.tasks[task_id]
        
        if dependency_id not in task.dependencies:
            task.dependencies.append(dependency_id)
            
            # Log event
            session_id = self._get_session_for_task(task_id)
            if session_id:
                await self._log_event(session_id, "dependency_added", added_by, {
                    "task_id": task_id,
                    "dependency_id": dependency_id
                })
            
            logger.info(f"Dependency added: {task_id} depends on {dependency_id}")
            return True
        
        return False
    
    async def get_workflow_progress(self, session_id: str) -> Dict[str, Any]:
        """Get workflow progress and statistics."""
        
        if session_id not in self.sessions:
            raise ValueError(f"Session {session_id} not found")
        
        session = self.sessions[session_id]
        session_tasks = [self.tasks[task_id] for task_id in session.tasks if task_id in self.tasks]
        
        total_tasks = len(session_tasks)
        completed_tasks = len([t for t in session_tasks if t.status == TaskStatus.COMPLETED])
        in_progress_tasks = len([t for t in session_tasks if t.status == TaskStatus.IN_PROGRESS])
        blocked_tasks = len([t for t in session_tasks if t.status == TaskStatus.BLOCKED])
        
        # Calculate progress
        if total_tasks > 0:
            progress = (completed_tasks / total_tasks) * 100
        else:
            progress = 0.0
        
        # Calculate average completion time
        completion_times = []
        for task in session_tasks:
            if task.status == TaskStatus.COMPLETED and task.completed_at:
                duration = (task.completed_at - task.created_at).total_seconds()
                completion_times.append(duration)
        
        avg_completion_time = np.mean(completion_times) if completion_times else 0
        
        return {
            "session_id": session_id,
            "session_name": session.name,
            "workflow_type": session.workflow_type.value,
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "in_progress_tasks": in_progress_tasks,
            "blocked_tasks": blocked_tasks,
            "progress_percentage": progress,
            "average_completion_time": avg_completion_time,
            "participants": session.participants,
            "start_time": session.start_time.isoformat(),
            "status": session.status
        }
    
    async def get_participant_tasks(self, session_id: str, participant: str) -> List[Dict[str, Any]]:
        """Get all tasks assigned to a specific participant."""
        
        if session_id not in self.sessions:
            raise ValueError(f"Session {session_id} not found")
        
        session = self.sessions[session_id]
        participant_tasks = []
        
        for task_id in session.tasks:
            if task_id in self.tasks:
                task = self.tasks[task_id]
                if participant in task.assigned_to:
                    participant_tasks.append({
                        "task_id": task.task_id,
                        "title": task.title,
                        "description": task.description,
                        "status": task.status.value,
                        "priority": task.priority.value,
                        "progress": task.progress,
                        "due_date": task.due_date.isoformat() if task.due_date else None,
                        "dependencies": task.dependencies,
                        "created_at": task.created_at.isoformat()
                    })
        
        return participant_tasks
    
    async def get_task_dependencies(self, task_id: str) -> Dict[str, Any]:
        """Get task dependencies and dependency graph."""
        
        if task_id not in self.tasks:
            raise ValueError(f"Task {task_id} not found")
        
        task = self.tasks[task_id]
        
        # Get direct dependencies
        direct_dependencies = []
        for dep_id in task.dependencies:
            if dep_id in self.tasks:
                dep_task = self.tasks[dep_id]
                direct_dependencies.append({
                    "task_id": dep_id,
                    "title": dep_task.title,
                    "status": dep_task.status.value,
                    "progress": dep_task.progress
                })
        
        # Get tasks that depend on this task
        dependent_tasks = []
        for other_task_id, other_task in self.tasks.items():
            if task_id in other_task.dependencies:
                dependent_tasks.append({
                    "task_id": other_task_id,
                    "title": other_task.title,
                    "status": other_task.status.value,
                    "progress": other_task.progress
                })
        
        return {
            "task_id": task_id,
            "title": task.title,
            "direct_dependencies": direct_dependencies,
            "dependent_tasks": dependent_tasks,
            "dependency_count": len(direct_dependencies),
            "dependent_count": len(dependent_tasks)
        }
    
    def _get_session_for_task(self, task_id: str) -> Optional[str]:
        """Get session ID for a given task."""
        for session_id, session in self.sessions.items():
            if task_id in session.tasks:
                return session_id
        return None
    
    async def _log_event(self, session_id: str, event_type: str, participant: str, 
                        data: Dict[str, Any]):
        """Log collaboration event."""
        
        event = CollaborationEvent(
            event_id=f"event_{secrets.token_urlsafe(8)}",
            session_id=session_id,
            event_type=event_type,
            participant=participant,
            timestamp=datetime.now(),
            data=data
        )
        
        self.events.append(event)
        
        # Queue for processing
        self.event_queue.put({
            "event": event,
            "session_id": session_id
        })
    
    def _process_task_update(self, task_data: Dict[str, Any]):
        """Process task update in background."""
        action = task_data.get("action")
        task_id = task_data.get("task_id")
        
        if action == "task_created":
            self.total_tasks += 1
            logger.info(f"Task {task_id} created and queued for processing")
        
        elif action == "task_updated":
            new_status = task_data.get("new_status")
            if new_status == "completed":
                # Update completion time statistics
                if self.completed_tasks > 0:
                    self.average_completion_time = (
                        (self.average_completion_time * (self.completed_tasks - 1) + 0) 
                        / self.completed_tasks
                    )
    
    def _process_collaboration_event(self, event_data: Dict[str, Any]):
        """Process collaboration event in background."""
        event = event_data.get("event")
        session_id = event_data.get("session_id")
        
        # Update session progress if needed
        if session_id in self.sessions:
            session = self.sessions[session_id]
            if event.event_type in ["task_completed", "task_status_updated"]:
                # Recalculate session progress
                session_tasks = [self.tasks[task_id] for task_id in session.tasks if task_id in self.tasks]
                completed_count = len([t for t in session_tasks if t.status == TaskStatus.COMPLETED])
                session.progress = completed_count / max(len(session_tasks), 1)
    
    def _send_notification(self, notification: Dict[str, Any]):
        """Send notification to participants."""
        # This would integrate with the notification system
        logger.info(f"Notification sent: {notification.get('type')} to {notification.get('recipients')}")
    
    def get_workflow_status(self) -> Dict[str, Any]:
        """Get overall workflow system status."""
        return {
            "total_sessions": len(self.sessions),
            "active_sessions": len([s for s in self.sessions.values() if s.status == "active"]),
            "total_tasks": self.total_tasks,
            "completed_tasks": self.completed_tasks,
            "completion_rate": self.completed_tasks / max(self.total_tasks, 1),
            "average_completion_time": self.average_completion_time,
            "total_events": len(self.events),
            "recent_events": len([e for e in self.events if e.timestamp > datetime.now() - timedelta(hours=1)])
        }
    
    def get_collaboration_history(self, session_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Get collaboration history for a session."""
        session_events = [e for e in self.events if e.session_id == session_id]
        return [asdict(event) for event in session_events[-limit:]]

# Global instance
collaborative_workflow = CollaborativeWorkflow()

# Convenience functions
async def create_workflow_session(name: str, workflow_type: WorkflowType, 
                                participants: List[str], description: str = "") -> str:
    """Create a new collaborative workflow session."""
    return await collaborative_workflow.create_workflow_session(name, workflow_type, participants, description)

async def create_task(session_id: str, title: str, description: str, 
                     assigned_to: List[str], priority: TaskPriority = TaskPriority.MEDIUM,
                     dependencies: List[str] = None, due_date: Optional[datetime] = None) -> str:
    """Create a new task in a workflow session."""
    return await collaborative_workflow.create_task(session_id, title, description, assigned_to, priority, dependencies, due_date)

async def update_task_status(task_id: str, new_status: TaskStatus, 
                            updated_by: str, progress: Optional[float] = None,
                            notes: str = "") -> bool:
    """Update task status and progress."""
    return await collaborative_workflow.update_task_status(task_id, new_status, updated_by, progress, notes)

async def get_workflow_progress(session_id: str) -> Dict[str, Any]:
    """Get workflow progress and statistics."""
    return await collaborative_workflow.get_workflow_progress(session_id)

def get_workflow_status() -> Dict[str, Any]:
    """Get overall workflow system status."""
    return collaborative_workflow.get_workflow_status()

if __name__ == "__main__":
    # Test the collaborative workflow system
    async def test_collaborative_workflow():
        print("Testing Collaborative Workflow System...")
        
        # Create workflow session
        participants = ["team_member_1", "team_member_2", "team_member_3"]
        session_id = await create_workflow_session(
            "ML Model Development", 
            WorkflowType.MODEL_TRAINING, 
            participants,
            "Collaborative ML model development workflow"
        )
        print(f"Created workflow session: {session_id}")
        
        # Create tasks
        task1_id = await create_task(
            session_id, 
            "Data Preprocessing", 
            "Clean and prepare training data",
            ["team_member_1"],
            TaskPriority.HIGH
        )
        
        task2_id = await create_task(
            session_id,
            "Feature Engineering",
            "Create and select features",
            ["team_member_2"],
            TaskPriority.HIGH,
            [task1_id]
        )
        
        task3_id = await create_task(
            session_id,
            "Model Training",
            "Train the ML model",
            ["team_member_3"],
            TaskPriority.CRITICAL,
            [task1_id, task2_id]
        )
        
        print(f"Created tasks: {task1_id}, {task2_id}, {task3_id}")
        
        # Update task status
        await update_task_status(task1_id, TaskStatus.IN_PROGRESS, "team_member_1", 0.3)
        await update_task_status(task1_id, TaskStatus.COMPLETED, "team_member_1", 1.0)
        await update_task_status(task2_id, TaskStatus.IN_PROGRESS, "team_member_2", 0.5)
        
        # Get progress
        progress = await get_workflow_progress(session_id)
        print(f"Workflow progress: {progress['progress_percentage']:.1f}%")
        
        # Get status
        status = get_workflow_status()
        print(f"Workflow status: {status['completion_rate']:.2%} completion rate")
        
        print("Collaborative Workflow System test completed!")
    
    asyncio.run(test_collaborative_workflow())
