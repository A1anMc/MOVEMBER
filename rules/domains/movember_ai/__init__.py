"""
Movember AI Rules System

Comprehensive rules system for the Movember Impact Intelligence Agent.
Integrates AI behaviour, impact reporting, grant lifecycle, and context validation rules.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime

from rules.core import RuleEngine, RuleEngineConfig
from rules.types import Rule, ContextType, ExecutionContext

# Import all rule modules
from .behaviours import get_ai_behaviour_rules, AI_RULES
from .reporting import get_impact_report_rules, IMPACT_REPORT_RULES
from .grant_rules import get_grant_rules, GRANT_RULES
from .context import get_project_rules, PROJECT_RULES, validate_movember_context
from .refactor import get_refactor_rules, REFACTOR_RULES, run_weekly_refactor


class MovemberAIRulesEngine:
    """Integrated rules engine for Movember AI operations."""
    
    def __init__(self, config: Optional[RuleEngineConfig] = None):
        self.engine = RuleEngine(config or RuleEngineConfig())
        self._load_all_rules()
    
    def _load_all_rules(self):
        """Load all Movember AI rules into the engine."""
        # Load all rule sets
        all_rules = (
            PROJECT_RULES +      # Context validation (highest priority)
            AI_RULES +           # AI behaviour rules
            GRANT_RULES +        # Grant lifecycle rules
            IMPACT_REPORT_RULES + # Impact reporting rules
            REFACTOR_RULES       # Weekly refactoring rules
        )
        
        self.engine.add_rules(all_rules)
        print(f"✅ Loaded {len(all_rules)} Movember AI rules")
    
    def evaluate_context(self, context: ExecutionContext, mode: str = "default") -> List[Any]:
        """Evaluate rules for a given context and mode."""
        # Validate Movember context first
        if not validate_movember_context(context.data.get('project_id', ''), context.context_type.value):
            raise ValueError("Context must be Movember-related")
        
        # Add mode-specific data
        context.data['evaluation_mode'] = mode
        context.data['evaluation_timestamp'] = datetime.now().isoformat()
        
        # Evaluate rules
        results = self.engine.evaluate(context)
        
        return results
    
    def evaluate_async(self, context: ExecutionContext, mode: str = "default") -> List[Any]:
        """Evaluate rules asynchronously."""
        # Validate Movember context first
        if not validate_movember_context(context.data.get('project_id', ''), context.context_type.value):
            raise ValueError("Context must be Movember-related")
        
        # Add mode-specific data
        context.data['evaluation_mode'] = mode
        context.data['evaluation_timestamp'] = datetime.now().isoformat()
        
        # Evaluate rules asynchronously
        import asyncio
        return asyncio.run(self.engine.evaluate_async(context))
    
    def get_rules_by_category(self, category: str) -> List[Rule]:
        """Get rules by category."""
        category_mapping = {
            'behaviour': AI_RULES,
            'reporting': IMPACT_REPORT_RULES,
            'grant': GRANT_RULES,
            'context': PROJECT_RULES,
            'refactor': REFACTOR_RULES
        }
        return category_mapping.get(category, [])
    
    def get_rules_by_priority(self, priority: str) -> List[Rule]:
        """Get rules by priority level."""
        from rules.types import RulePriority
        
        priority_mapping = {
            'critical': RulePriority.CRITICAL,
            'high': RulePriority.HIGH,
            'medium': RulePriority.MEDIUM,
            'low': RulePriority.LOW,
            'minimal': RulePriority.MINIMAL
        }
        
        target_priority = priority_mapping.get(priority.lower())
        if not target_priority:
            return []
        
        all_rules = self.engine.list_rules()
        return [rule for rule in all_rules if rule.priority == target_priority]
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get system metrics."""
        return self.engine.get_metrics()
    
    def get_execution_history(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get recent execution history."""
        return self.engine.get_execution_history(limit)
    
    def run_weekly_maintenance(self):
        """Run weekly maintenance and refactoring."""
        return run_weekly_refactor()
    
    def validate_mission_alignment(self, operation_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate if an operation aligns with Movember's mission."""
        mission_areas = ['men_health', 'mental_health', 'prostate_cancer', 'testicular_cancer']
        strategy_pillars = ['awareness', 'prevention', 'support', 'research']
        
        alignment_score = 0.0
        alignment_factors = []
        
        # Check if operation addresses mission areas
        for area in mission_areas:
            if area in str(operation_data).lower():
                alignment_score += 0.25
                alignment_factors.append(f"Addresses {area}")
        
        # Check if operation supports strategy pillars
        for pillar in strategy_pillars:
            if pillar in str(operation_data).lower():
                alignment_score += 0.25
                alignment_factors.append(f"Supports {pillar}")
        
        return {
            'alignment_score': min(alignment_score, 1.0),
            'alignment_factors': alignment_factors,
            'mission_areas': mission_areas,
            'strategy_pillars': strategy_pillars,
            'is_aligned': alignment_score >= 0.5
        }
    
    def get_system_summary(self) -> Dict[str, Any]:
        """Get a comprehensive system summary."""
        return {
            'total_rules': len(self.engine.list_rules()),
            'rule_categories': {
                'behaviour': len(AI_RULES),
                'reporting': len(IMPACT_REPORT_RULES),
                'grant': len(GRANT_RULES),
                'context': len(PROJECT_RULES),
                'refactor': len(REFACTOR_RULES)
            },
            'priority_distribution': {
                'critical': len([r for r in self.engine.rules.values() if r.priority.value == 100]),
                'high': len([r for r in self.engine.rules.values() if r.priority.value == 75]),
                'medium': len([r for r in self.engine.rules.values() if r.priority.value == 50]),
                'low': len([r for r in self.engine.rules.values() if r.priority.value == 25]),
                'minimal': len([r for r in self.engine.rules.values() if r.priority.value == 1])
            },
            'context_types': [ct.value for ct in ContextType],
            'system_status': 'operational',
            'last_maintenance': datetime.now().isoformat()
        }


# Convenience functions for easy access
def create_movember_engine(config: Optional[RuleEngineConfig] = None) -> MovemberAIRulesEngine:
    """Create a Movember AI rules engine instance."""
    return MovemberAIRulesEngine(config)


def get_all_movember_rules() -> List[Rule]:
    """Get all Movember AI rules."""
    return (
        PROJECT_RULES +
        AI_RULES +
        GRANT_RULES +
        IMPACT_REPORT_RULES +
        REFACTOR_RULES
    )


def validate_movember_operation(operation_data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate if an operation is appropriate for Movember context."""
    engine = MovemberAIRulesEngine()
    
    # Create context for validation
    context = ExecutionContext(
        context_type=ContextType.BUSINESS_PROCESS,
        context_id=f"validation_{datetime.now().timestamp()}",
        data=operation_data
    )
    
    # Run validation
    results = engine.evaluate_context(context, mode="validation")
    
    # Check mission alignment
    mission_alignment = engine.validate_mission_alignment(operation_data)
    
    return {
        'is_valid': len(results) > 0 and all(r.success for r in results),
        'validation_results': results,
        'mission_alignment': mission_alignment,
        'recommendations': [
            'Ensure operation aligns with Movember mission',
            'Include appropriate impact metrics',
            'Follow data integrity guidelines',
            'Maintain professional standards'
        ]
    }


def run_movember_impact_analysis(impact_data: Dict[str, Any]) -> Dict[str, Any]:
    """Run impact analysis using Movember rules."""
    engine = MovemberAIRulesEngine()
    
    # Create context for impact analysis
    context = ExecutionContext(
        context_type=ContextType.BUSINESS_PROCESS,
        context_id=f"impact_{datetime.now().timestamp()}",
        data={
            **impact_data,
            'analysis_type': 'impact',
            'framework_required': True
        }
    )
    
    # Run analysis
    results = engine.evaluate_context(context, mode="impact_analysis")
    
    return {
        'analysis_results': results,
        'framework_compliance': any('framework' in str(r) for r in results),
        'outcome_mapping': any('outcome' in str(r) for r in results),
        'data_visualization': any('visualization' in str(r) for r in results),
        'recommendations': [
            'Ensure ToC, CEMP, or SDG framework is used',
            'Map all outputs to measurable outcomes',
            'Include appropriate data visualizations',
            'Maintain clear attribution vs contribution distinction'
        ]
    }


def evaluate_grant_application(grant_data: Dict[str, Any]) -> Dict[str, Any]:
    """Evaluate a grant application using Movember rules."""
    engine = MovemberAIRulesEngine()
    
    # Create context for grant evaluation
    context = ExecutionContext(
        context_type=ContextType.BUSINESS_PROCESS,
        context_id=f"grant_{datetime.now().timestamp()}",
        data={
            **grant_data,
            'evaluation_type': 'grant',
            'completeness_check': True
        }
    )
    
    # Run evaluation
    results = engine.evaluate_context(context, mode="grant_evaluation")
    
    return {
        'evaluation_results': results,
        'completeness_score': len([r for r in results if 'completeness' in str(r)]) / len(results) if results else 0,
        'impact_metrics_present': any('impact' in str(r) for r in results),
        'budget_appropriate': any('budget' in str(r) for r in results),
        'timeline_realistic': any('timeline' in str(r) for r in results),
        'recommendations': [
            'Ensure all required fields are completed',
            'Include measurable impact metrics',
            'Provide realistic budget and timeline',
            'Align with relevant SDGs'
        ]
    }


# Export main components
__all__ = [
    'MovemberAIRulesEngine',
    'create_movember_engine',
    'get_all_movember_rules',
    'validate_movember_operation',
    'run_movember_impact_analysis',
    'evaluate_grant_application',
    'run_weekly_refactor',
    'AI_RULES',
    'IMPACT_REPORT_RULES',
    'GRANT_RULES',
    'PROJECT_RULES',
    'REFACTOR_RULES'
] 