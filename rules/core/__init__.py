"""
Core Rule Engine

The heart of the rules system - a powerful, flexible rule engine
that can handle complex business logic and workflows.
"""

from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass
import logging
import time
from datetime import datetime

from .engine import RuleEngine
from .evaluator import RuleEvaluator
from .executor import ActionExecutor
from .metrics import MetricsCollector

__all__ = [
    'RuleEngine',
    'RuleEvaluator', 
    'ActionExecutor',
    'MetricsCollector'
]

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__) 