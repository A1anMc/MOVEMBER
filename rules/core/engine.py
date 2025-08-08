"""
Rule Engine

The main orchestrator for rule evaluation and execution.
"""

from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
import logging
import time
from datetime import datetime
import asyncio
from concurrent.futures import ThreadPoolExecutor

from .evaluator import RuleEvaluator
from .executor import ActionExecutor
from .metrics import MetricsCollector
from ..types import Rule, RuleResult, ExecutionContext

logger = logging.getLogger(__name__)


@dataclass
class RuleEngineConfig:
    """Configuration for the rule engine."""
    max_concurrent_rules: int = 10
    enable_metrics: bool = True
    enable_audit_trail: bool = True
    timeout_seconds: int = 30
    retry_attempts: int = 3


class RuleEngine:
    """
    The main rule engine that orchestrates rule evaluation and execution.
    
    Features:
    - Parallel rule execution
    - Rule chaining and dependencies
    - Comprehensive metrics and monitoring
    - Audit trail for all rule executions
    - Error handling and retry logic
    """
    
    def __init__(self, config: Optional[RuleEngineConfig] = None):
        self.config = config or RuleEngineConfig()
        self.rules: Dict[str, Rule] = {}
        self.evaluator = RuleEvaluator()
        self.executor = ActionExecutor()
        self.metrics = MetricsCollector() if self.config.enable_metrics else None
        self.execution_history: List[Dict] = []
        
        # Thread pool for concurrent execution
        self.thread_pool = ThreadPoolExecutor(
            max_workers=self.config.max_concurrent_rules
        )
    
    def add_rule(self, rule: Rule) -> None:
        """Add a rule to the engine."""
        if rule.name in self.rules:
            logger.warning(f"Rule '{rule.name}' already exists, overwriting")
        
        self.rules[rule.name] = rule
        logger.info(f"Added rule: {rule.name}")
    
    def add_rules(self, rules: List[Rule]) -> None:
        """Add multiple rules to the engine."""
        for rule in rules:
            self.add_rule(rule)
    
    def remove_rule(self, rule_name: str) -> bool:
        """Remove a rule from the engine."""
        if rule_name in self.rules:
            del self.rules[rule_name]
            logger.info(f"Removed rule: {rule_name}")
            return True
        return False
    
    def get_rule(self, rule_name: str) -> Optional[Rule]:
        """Get a rule by name."""
        return self.rules.get(rule_name)
    
    def list_rules(self) -> List[str]:
        """List all rule names."""
        return list(self.rules.keys())
    
    async def evaluate_async(self, context: ExecutionContext) -> List[RuleResult]:
        """Evaluate all applicable rules asynchronously."""
        start_time = time.time()
        
        # Find applicable rules
        applicable_rules = self._find_applicable_rules(context)
        
        if not applicable_rules:
            logger.info("No applicable rules found")
            return []
        
        # Execute rules concurrently
        tasks = []
        for rule in applicable_rules:
            task = self._execute_rule_async(rule, context)
            tasks.append(task)
        
        # Wait for all rules to complete
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results
        rule_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"Rule execution failed: {applicable_rules[i].name}", exc_info=result)
                rule_results.append(RuleResult(
                    rule_name=applicable_rules[i].name,
                    success=False,
                    error=str(result),
                    execution_time=0
                ))
            else:
                rule_results.append(result)
        
        # Record metrics
        execution_time = time.time() - start_time
        if self.metrics:
            self.metrics.record_batch_execution(len(applicable_rules), execution_time)
        
        # Record audit trail
        if self.config.enable_audit_trail:
            self._record_audit_trail(context, rule_results, execution_time)
        
        return rule_results
    
    def evaluate(self, context: ExecutionContext) -> List[RuleResult]:
        """Evaluate all applicable rules synchronously."""
        return asyncio.run(self.evaluate_async(context))
    
    def _find_applicable_rules(self, context: ExecutionContext) -> List[Rule]:
        """Find rules that are applicable to the current context."""
        applicable_rules = []
        
        for rule in self.rules.values():
            if self._is_rule_applicable(rule, context):
                applicable_rules.append(rule)
        
        # Sort by priority (higher priority first)
        applicable_rules.sort(key=lambda r: r.priority.value, reverse=True)
        
        return applicable_rules
    
    def _is_rule_applicable(self, rule: Rule, context: ExecutionContext) -> bool:
        """Check if a rule is applicable to the current context."""
        # Check if rule is enabled
        if not rule.enabled:
            return False
        
        # Check context type matching
        if rule.context_types and context.context_type not in rule.context_types:
            return False
        
        # Check custom applicability function
        if rule.applicability_check and not rule.applicability_check(context):
            return False
        
        return True
    
    async def _execute_rule_async(self, rule: Rule, context: ExecutionContext) -> RuleResult:
        """Execute a single rule asynchronously."""
        start_time = time.time()
        
        try:
            # Evaluate conditions
            conditions_met = await self.evaluator.evaluate_conditions_async(
                rule.conditions, context
            )
            
            if not conditions_met:
                return RuleResult(
                    rule_name=rule.name,
                    success=True,
                    conditions_met=False,
                    execution_time=time.time() - start_time,
                    metadata={"priority": rule.priority}
                )
            
            # Execute actions
            action_results = await self.executor.execute_actions_async(
                rule.actions, context
            )
            
            execution_time = time.time() - start_time
            
            # Record metrics
            if self.metrics:
                self.metrics.record_rule_execution(rule.name, execution_time, True)
            
            return RuleResult(
                rule_name=rule.name,
                success=True,
                conditions_met=True,
                action_results=action_results,
                execution_time=execution_time,
                metadata={"priority": rule.priority}
            )
            
        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(f"Rule execution failed: {rule.name}", exc_info=e)
            
            # Record metrics
            if self.metrics:
                self.metrics.record_rule_execution(rule.name, execution_time, False)
            
            return RuleResult(
                rule_name=rule.name,
                success=False,
                error=str(e),
                execution_time=execution_time,
                metadata={"priority": rule.priority}
            )
    
    def _record_audit_trail(self, context: ExecutionContext, results: List[RuleResult], total_time: float) -> None:
        """Record execution details for audit trail."""
        audit_entry = {
            'timestamp': datetime.now().isoformat(),
            'context_type': context.context_type,
            'context_id': context.context_id,
            'total_rules': len(results),
            'successful_rules': len([r for r in results if r.success]),
            'total_execution_time': total_time,
            'results': [r.to_dict() for r in results]
        }
        
        self.execution_history.append(audit_entry)
        
        # Keep only last 1000 entries to prevent memory issues
        if len(self.execution_history) > 1000:
            self.execution_history = self.execution_history[-1000:]
    
    def get_execution_history(self, limit: int = 100) -> List[Dict]:
        """Get recent execution history."""
        return self.execution_history[-limit:]
    
    def get_metrics(self) -> Optional[Dict]:
        """Get current metrics if enabled."""
        if self.metrics:
            return self.metrics.get_metrics()
        return None
    
    def clear_history(self) -> None:
        """Clear execution history."""
        self.execution_history.clear()
        if self.metrics:
            self.metrics.reset()
    
    def shutdown(self) -> None:
        """Shutdown the rule engine and cleanup resources."""
        self.thread_pool.shutdown(wait=True)
        logger.info("Rule engine shutdown complete") 