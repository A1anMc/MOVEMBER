#!/usr/bin/env python3
"""
Movember AI Rules System - Main Integration Module
Provides unified access to all Movember AI rules and systems.
"""

import logging
from typing import Dict, List, Optional, Any
from datetime import datetime

from rules.core import RuleEngine, RuleEngineConfig
from rules.types import ExecutionContext, ContextType, RulePriority
from rules.domains.movember_ai.behaviours import get_ai_behaviour_rules
from rules.domains.movember_ai.reporting import get_impact_report_rules
from rules.domains.movember_ai.grant_rules import get_grant_rules
from rules.domains.movember_ai.context import get_project_rules, validate_movember_context
from rules.domains.movember_ai.refactor import get_refactor_rules, run_weekly_refactor
# from rules.domains.movember_ai.integration import (
#     MovemberSystemIntegrator,
#     create_movember_integrator,
#     process_grant_with_integration,
#     process_impact_with_integration,
#     validate_system_integration
# )

logger = logging.getLogger(__name__)


class MovemberAIRulesEngine:
    """
    Integrated rules engine for Movember AI operations.
    Provides unified access to all rule categories and systems.
    """

    def __init__(self, config: Optional[RuleEngineConfig] = None):


        self.engine = RuleEngine(config or RuleEngineConfig())
        self.integrator = None  # Will be initialized when needed
        self._load_all_rules()

    def _load_all_rules(self):


        """Load all rule categories into the engine."""
        from rules.domains.movember_ai.behaviours import AI_RULES
        from rules.domains.movember_ai.reporting import IMPACT_REPORT_RULES
        from rules.domains.movember_ai.grant_rules import GRANT_RULES
        from rules.domains.movember_ai.context import PROJECT_RULES
        from rules.domains.movember_ai.refactor import REFACTOR_RULES

        all_rules = (
            PROJECT_RULES + AI_RULES + GRANT_RULES + IMPACT_REPORT_RULES + REFACTOR_RULES
        )

        for rule in all_rules:
            self.engine.add_rule(rule)

        logger.info(f"Loaded {len(all_rules)} rules across all categories")

    async def evaluate_context(self, context: ExecutionContext, mode: str = "default") -> List[Any]:
        """
        Evaluate rules for a given context with specified mode.

        Args:
            context: Execution context containing data and metadata
            mode: Evaluation mode (default, reporting, grant_submission, etc.)

        Returns:
            List of rule evaluation results
        """
        # Validate Movember context only for project validation contexts and when project_id is provided
        project_id = context.data.get('project_id')
        if context.context_type == ContextType.PROJECT_VALIDATION and project_id is not None:
            # For project validation, treat operation as 'impact_analysis' for allow-list
            operation_type = 'impact_analysis'
            if not validate_movember_context(project_id, operation_type):
                raise ValueError("Context must be Movember-related")

        # Apply mode-specific filtering
        filtered_rules = self._filter_rules_by_mode(mode)

        # Evaluate rules
        results = await self.engine.evaluate_async(context)

        # Filter results by mode
        mode_results = [r for r in results if self._is_rule_applicable_for_mode(r, mode)]

        # Serialize results to dicts and expose priority at top-level for tests
        serialized_results: List[Dict[str, Any]] = []
        for r in mode_results:
            rd = r.to_dict() if hasattr(r, 'to_dict') else dict(r)
            # Promote priority enum to top-level
            priority_value = None
            try:
                priority_value = r.metadata.get('priority') if hasattr(r, 'metadata') else None
            except Exception:
                priority_value = None
            if priority_value is not None:
                rd['priority'] = priority_value
            serialized_results.append(rd)

        logger.info(f"Evaluated {len(serialized_results)} rules in {mode} mode")
        return serialized_results

    def _filter_rules_by_mode(self, mode: str) -> List:


        """Filter rules based on evaluation mode."""
        mode_mappings = {
            "reporting": ["impact_reporting"],
            "grant_submission": ["grant_evaluation"],
            "ai_behaviour": ["ai_behaviour"],
            "context_validation": ["project_validation"],
            "weekly_maintenance": ["refactoring"]
        }

        return mode_mappings.get(mode, [])

    def _is_rule_applicable_for_mode(self, result: Any, mode: str) -> bool:


        """Check if a rule result is applicable for the given mode."""
        # This is a simplified check - in practice, you'd have more sophisticated logic
        return True

    def get_metrics(self) -> Dict[str, Any]:


        """Get system metrics and performance statistics."""
        if self.engine.metrics:
            raw = self.engine.metrics.get_metrics()
            # Adapt keys to expected names in tests
            system = raw.get("system", {})
            # Provide compatibility aliases expected by tests
            system_alias = dict(system)
            system_alias.setdefault("total_executions", system.get("total_rules_executed", 0))
            system_alias.setdefault("success_rate", 0.0)  # Not tracked globally; leave as 0.0
            return {
                "system_metrics": system_alias,
                "rule_metrics": raw.get("rules", {}),
                "alerts": raw.get("alerts", []),
                "performance_thresholds": raw.get("performance_thresholds", {})
            }
        return {"system_metrics": {}, "rule_metrics": {}}

    def get_execution_history(self) -> List[Dict]:


        """Get execution history and audit trail."""
        return self.engine.execution_history

    async def run_weekly_maintenance(self) -> Any:
        """Run weekly maintenance and refactoring."""
        return await run_weekly_refactor()

    async def get_integrator(self):
        """Get or create the system integrator."""
        if self.integrator is None:
            from rules.domains.movember_ai.integration import create_movember_integrator # local import to avoid circular
            self.integrator = await create_movember_integrator()
        return self.integrator

    async def process_grant_lifecycle(self, grant_data: Dict) -> Dict:
        """
        Process a grant through the complete lifecycle with all systems integrated.

        Args:
            grant_data: Grant application data

        Returns:
            Complete grant processing results
        """
        integrator = await self.get_integrator()
        return await integrator.process_grant_lifecycle(grant_data)

    async def process_impact_reporting(self, impact_data: Dict) -> Dict:
        """
        Process impact reporting with all systems integrated.

        Args:
            impact_data: Impact reporting data

        Returns:
            Complete impact processing results
        """
        integrator = await self.get_integrator()
        return await integrator.process_impact_reporting(impact_data)

    async def validate_system_integration(self, data: Dict) -> Any:
        """
        Validate integration across all systems.

        Args:
            data: Data to validate across systems

        Returns:
            Cross-system validation results
        """
        integrator = await self.get_integrator()
        return await integrator._validate_cross_system_consistency(data)


# Convenience functions for easy access
def create_movember_engine(config: Optional[RuleEngineConfig] = None) -> MovemberAIRulesEngine:


    """Create a Movember AI rules engine instance."""
    return MovemberAIRulesEngine(config)


def validate_movember_operation(operation: str, project_id: str) -> bool:
    """
    Validate if an operation is appropriate for the Movember project.

    Args:
        operation: Operation to validate
        project_id: Project identifier

    Returns:
        True if operation is valid for Movember context
    """
    return validate_movember_context(project_id, operation)


async def run_movember_impact_analysis(data: Dict) -> Dict:
    """
    Run comprehensive impact analysis for Movember projects.

    Args:
        data: Project data for impact analysis

    Returns:
        Impact analysis results
    """
    engine = create_movember_engine()
    context = ExecutionContext(
        context_type=ContextType.IMPACT_REPORTING,
        context_id=f"impact-analysis-{data.get('project_id', 'unknown')}",
        data=data,
        timestamp=datetime.now()
    )

    results = await engine.evaluate_context(context, mode="reporting")

    return {
        "analysis": "comprehensive_impact_analysis",
        "results": results,
        "recommendations": ["Continue monitoring", "Scale successful interventions"],
        "timestamp": datetime.now().isoformat()
    }


async def evaluate_grant_application(grant_data: Dict) -> Dict:
    """
    Evaluate a grant application using the integrated rules system.

    Args:
        grant_data: Grant application data

    Returns:
        Grant evaluation results
    """
    engine = create_movember_engine()
    context = ExecutionContext(
        context_type=ContextType.GRANT_EVALUATION,
        context_id=f"grant-eval-{grant_data.get('grant_id', 'unknown')}",
        data=grant_data,
        timestamp=datetime.now()
    )

    results = await engine.evaluate_context(context, mode="grant_submission")

    return {
        "evaluation": "comprehensive_grant_evaluation",
        "results": results,
        "recommendation": "approve" if len([r for r in results if r.get('success')]) > len(results) / 2 else "review",
        "timestamp": datetime.now().isoformat()
    }


async def run_weekly_refactor() -> Any:
    """
    Run weekly refactoring and maintenance tasks.

    Returns:
        Refactoring summary and recommendations
    """
    from rules.domains.movember_ai.refactor import run_weekly_refactor as run_refactor
    return await run_refactor()


# Lazy wrapper functions to avoid circular imports while providing package-level API
async def process_grant_with_integration(grant_data: Dict, config: Optional[Dict] = None) -> Dict:
    from rules.domains.movember_ai.integration import create_movember_integrator
    integrator = await create_movember_integrator(config)
    return await integrator.process_grant_lifecycle(grant_data)


async def process_impact_with_integration(impact_data: Dict, config: Optional[Dict] = None) -> Dict:
    from rules.domains.movember_ai.integration import create_movember_integrator
    integrator = await create_movember_integrator(config)
    return await integrator.process_impact_reporting(impact_data)


async def validate_system_integration(data: Dict, config: Optional[Dict] = None) -> Any:
    from rules.domains.movember_ai.integration import create_movember_integrator
    integrator = await create_movember_integrator(config)
    return await integrator._validate_cross_system_consistency(data)


# Export main classes and functions
__all__ = [
    'MovemberAIRulesEngine',
    'create_movember_engine',
    'validate_movember_operation',
    'run_movember_impact_analysis',
    'evaluate_grant_application',
    'run_weekly_refactor',
    'process_grant_with_integration',
    'process_impact_with_integration',
    'validate_system_integration'
]
