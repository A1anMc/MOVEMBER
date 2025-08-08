"""
Rule Types

Core data structures and types for the rules system.
"""

from typing import List, Dict, Any, Optional, Callable, Union
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

__all__ = [
    'Rule',
    'Condition',
    'Action',
    'RuleResult',
    'ExecutionContext',
    'ActionResult',
    'RulePriority',
    'ContextType'
]


class RulePriority(Enum):
    """Priority levels for rules."""
    CRITICAL = 100
    HIGH = 75
    MEDIUM = 50
    LOW = 25
    MINIMAL = 1


class ContextType(Enum):
    """Types of execution contexts."""
    USER_REGISTRATION = "user_registration"
    USER_LOGIN = "user_login"
    DATA_VALIDATION = "data_validation"
    BUSINESS_PROCESS = "business_process"
    SECURITY_CHECK = "security_check"
    NOTIFICATION = "notification"
    CUSTOM = "custom"
    IMPACT_REPORTING = "impact_reporting"
    GRANT_EVALUATION = "grant_evaluation"
    AI_BEHAVIOUR = "ai_behaviour"
    PROJECT_VALIDATION = "project_validation"


@dataclass
class Condition:
    """A condition that must be met for a rule to execute."""
    expression: str
    description: Optional[str] = None
    parameters: Dict[str, Any] = field(default_factory=dict)
    custom_evaluator: Optional[Callable] = None

    def __post_init__(self):
        if not self.description:
            self.description = f"Condition: {self.expression}"


@dataclass
class Action:
    """An action to be executed when a rule's conditions are met."""
    name: str
    parameters: Dict[str, Any] = field(default_factory=dict)
    description: Optional[str] = None
    custom_executor: Optional[Callable] = None
    retry_on_failure: bool = False
    max_retries: int = 3

    def __post_init__(self):
        if not self.description:
            self.description = f"Action: {self.name}"


@dataclass
class ActionResult:
    """Result of an action execution."""
    action_name: str
    success: bool
    result: Optional[Any] = None
    error: Optional[str] = None
    execution_time: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            'action_name': self.action_name,
            'success': self.success,
            'result': self.result,
            'error': self.error,
            'execution_time': self.execution_time,
            'metadata': self.metadata
        }


@dataclass
class RuleResult:
    """Result of a rule execution."""
    rule_name: str
    success: bool
    conditions_met: bool = False
    action_results: Optional[List[ActionResult]] = None
    error: Optional[str] = None
    execution_time: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            'rule_name': self.rule_name,
            'success': self.success,
            'conditions_met': self.conditions_met,
            'action_results': [ar.to_dict() for ar in (self.action_results or [])],
            'error': self.error,
            'execution_time': self.execution_time,
            'metadata': self.metadata
        }


@dataclass
class ExecutionContext:
    """Context for rule execution."""
    context_type: ContextType
    context_id: str
    data: Dict[str, Any] = field(default_factory=dict)
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            'context_type': self.context_type.value,
            'context_id': self.context_id,
            'data': self.data,
            'user_id': self.user_id,
            'session_id': self.session_id,
            'timestamp': self.timestamp.isoformat(),
            'metadata': self.metadata
        }


@dataclass
class Rule:
    """A rule definition."""
    name: str
    conditions: List[Condition] = field(default_factory=list)
    actions: List[Action] = field(default_factory=list)
    priority: RulePriority = RulePriority.MEDIUM
    enabled: bool = True
    description: Optional[str] = None
    context_types: Optional[List[ContextType]] = None
    applicability_check: Optional[Callable[[ExecutionContext], bool]] = None
    tags: List[str] = field(default_factory=list)
    version: str = "1.0.0"
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        if not self.description:
            self.description = f"Rule: {self.name}"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            'name': self.name,
            'conditions': [
                {
                    'expression': c.expression,
                    'description': c.description,
                    'parameters': c.parameters
                }
                for c in self.conditions
            ],
            'actions': [
                {
                    'name': a.name,
                    'parameters': a.parameters,
                    'description': a.description,
                    'retry_on_failure': a.retry_on_failure,
                    'max_retries': a.max_retries
                }
                for a in self.actions
            ],
            'priority': self.priority.value,
            'enabled': self.enabled,
            'description': self.description,
            'context_types': [ct.value for ct in (self.context_types or [])],
            'tags': self.tags,
            'version': self.version,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Rule':
        """Create a rule from dictionary."""
        return cls(
            name=data['name'],
            conditions=[
                Condition(
                    expression=c['expression'],
                    description=c.get('description'),
                    parameters=c.get('parameters', {})
                )
                for c in data.get('conditions', [])
            ],
            actions=[
                Action(
                    name=a['name'],
                    parameters=a.get('parameters', {}),
                    description=a.get('description'),
                    retry_on_failure=a.get('retry_on_failure', False),
                    max_retries=a.get('max_retries', 3)
                )
                for a in data.get('actions', [])
            ],
            priority=RulePriority(data.get('priority', RulePriority.MEDIUM.value)),
            enabled=data.get('enabled', True),
            description=data.get('description'),
            context_types=[
                ContextType(ct) for ct in data.get('context_types', [])
            ] if data.get('context_types') else None,
            tags=data.get('tags', []),
            version=data.get('version', '1.0.0')
        )
