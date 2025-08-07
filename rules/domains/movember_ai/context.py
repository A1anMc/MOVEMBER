"""
Movember Context Validation Rules

Defines rules for validating project context and ensuring the agent
only operates within the Movember project scope.
"""

from rules.types import Rule, Condition, Action, RulePriority, ContextType


# Project Context Validation Rules
PROJECT_RULES = [
    Rule(
        name="validate_movember_context",
        description="Ensure agent only operates in Movember project context",
        priority=RulePriority.CRITICAL,
        context_types=[ContextType.BUSINESS_PROCESS],
        conditions=[
            Condition("project.id != 'movember'", description="Project is not Movember"),
            Condition("project.context_type not in ['movember_impact', 'men_health', 'grant_evaluation']", 
                     description="Context not Movember-related")
        ],
        actions=[
            Action("abort", parameters={
                'message': 'This agent only operates in Movember project context.',
                'redirect_to_movember': True,
                'log_violation': True
            }),
            Action("log_context_violation", parameters={
                'project_id': 'project.id',
                'context_type': 'project.context_type',
                'timestamp': 'now',
                'violation_type': 'non_movember_context'
            })
        ],
        tags=['context', 'validation', 'movember']
    ),
    
    Rule(
        name="validate_mission_alignment",
        description="Ensure all operations align with Movember's mission",
        priority=RulePriority.CRITICAL,
        context_types=[ContextType.BUSINESS_PROCESS],
        conditions=[
            Condition("operation.mission_alignment_score < 0.7", description="Operation not sufficiently mission-aligned"),
            Condition("operation.context_type in ['analysis', 'reporting', 'recommendation']", 
                     description="Critical operation type")
        ],
        actions=[
            Action("block_operation", parameters={
                'message': 'Operation does not align with Movember mission.',
                'suggest_mission_alignment': True
            }),
            Action("review_mission_alignment", parameters={
                'mission_areas': ['men_health', 'mental_health', 'prostate_cancer', 'testicular_cancer'],
                'strategy_pillars': ['awareness', 'prevention', 'support', 'research']
            }),
            Action("log_mission_violation", parameters={
                'operation_id': 'operation.id',
                'alignment_score': 'operation.mission_alignment_score',
                'timestamp': 'now'
            })
        ],
        tags=['context', 'mission', 'alignment']
    ),
    
    Rule(
        name="validate_data_source_authority",
        description="Ensure data sources are authorized for Movember context",
        priority=RulePriority.HIGH,
        context_types=[ContextType.DATA_VALIDATION],
        conditions=[
            Condition("data.source not in ['movember_database', 'authorized_partner', 'public_health_data']", 
                     description="Data source not authorized"),
            Condition("data.confidence > 0.5", description="Data has significant confidence")
        ],
        actions=[
            Action("flag_unauthorized_source", parameters={
                'source': 'data.source',
                'confidence': 'data.confidence',
                'suggest_authorized_alternative': True
            }),
            Action("require_authorization", parameters={
                'authorization_process': True,
                'data_governance_review': True,
                'privacy_compliance': True
            }),
            Action("log_unauthorized_access", parameters={
                'data_source': 'data.source',
                'access_attempt': 'now',
                'user_id': 'user.id'
            })
        ],
        tags=['context', 'data', 'authorization']
    ),
    
    Rule(
        name="validate_stakeholder_permissions",
        description="Ensure stakeholder access permissions are appropriate",
        priority=RulePriority.HIGH,
        context_types=[ContextType.BUSINESS_PROCESS],
        conditions=[
            Condition("user.role not in ['analyst', 'executive', 'funder', 'researcher', 'admin']", 
                     description="User role not authorized"),
            Condition("operation.sensitivity_level in ['high', 'critical']", description="Sensitive operation")
        ],
        actions=[
            Action("block_access", parameters={
                'message': 'Insufficient permissions for this operation.',
                'required_role': 'operation.required_role',
                'contact_admin': True
            }),
            Action("log_access_denied", parameters={
                'user_id': 'user.id',
                'user_role': 'user.role',
                'operation': 'operation.type',
                'timestamp': 'now'
            }),
            Action("suggest_alternative_access", parameters={
                'read_only_access': True,
                'summary_access': True,
                'contact_authorized_user': True
            })
        ],
        tags=['context', 'permissions', 'access']
    ),
    
    Rule(
        name="validate_geographic_scope",
        description="Ensure operations are within Movember's geographic scope",
        priority=RulePriority.MEDIUM,
        context_types=[ContextType.BUSINESS_PROCESS],
        conditions=[
            Condition("operation.geographic_scope not in ['global', 'national', 'regional']", 
                     description="Geographic scope not supported"),
            Condition("operation.country not in ['authorized_countries']", description="Country not authorized")
        ],
        actions=[
            Action("flag_geographic_issue", parameters={
                'scope': 'operation.geographic_scope',
                'country': 'operation.country',
                'suggest_authorized_scope': True
            }),
            Action("validate_regional_permissions", parameters={
                'regional_authorization': True,
                'local_partnerships': True,
                'cultural_sensitivity': True
            }),
            Action("log_geographic_violation", parameters={
                'scope': 'operation.geographic_scope',
                'country': 'operation.country',
                'timestamp': 'now'
            })
        ],
        tags=['context', 'geographic', 'scope']
    ),
    
    Rule(
        name="validate_temporal_context",
        description="Ensure operations are within appropriate temporal context",
        priority=RulePriority.MEDIUM,
        context_types=[ContextType.BUSINESS_PROCESS],
        conditions=[
            Condition("operation.temporal_scope not in ['current', 'historical', 'projected']", 
                     description="Temporal scope not supported"),
            Condition("operation.time_period not in ['authorized_periods']", description="Time period not authorized")
        ],
        actions=[
            Action("flag_temporal_issue", parameters={
                'scope': 'operation.temporal_scope',
                'period': 'operation.time_period',
                'suggest_authorized_period': True
            }),
            Action("validate_data_availability", parameters={
                'data_coverage': True,
                'historical_data': True,
                'projection_methods': True
            }),
            Action("log_temporal_violation", parameters={
                'scope': 'operation.temporal_scope',
                'period': 'operation.time_period',
                'timestamp': 'now'
            })
        ],
        tags=['context', 'temporal', 'scope']
    ),
    
    Rule(
        name="validate_operational_scope",
        description="Ensure operations are within Movember's operational scope",
        priority=RulePriority.HIGH,
        context_types=[ContextType.BUSINESS_PROCESS],
        conditions=[
            Condition("operation.type not in ['impact_analysis', 'grant_evaluation', 'reporting', 'research']", 
                     description="Operation type not supported"),
            Condition("operation.sensitivity_level == 'high'", description="High sensitivity operation")
        ],
        actions=[
            Action("validate_operational_permissions", parameters={
                'operation_type': 'operation.type',
                'sensitivity_level': 'operation.sensitivity_level',
                'user_permissions': True
            }),
            Action("require_approval", parameters={
                'approval_workflow': True,
                'stakeholder_consultation': True,
                'risk_assessment': True
            }),
            Action("log_operational_access", parameters={
                'operation_type': 'operation.type',
                'user_id': 'user.id',
                'timestamp': 'now'
            })
        ],
        tags=['context', 'operational', 'scope']
    ),
    
    Rule(
        name="validate_partnership_context",
        description="Ensure operations respect partnership agreements and boundaries",
        priority=RulePriority.MEDIUM,
        context_types=[ContextType.BUSINESS_PROCESS],
        conditions=[
            Condition("operation.partnership_id is not None", description="Operation involves partnership"),
            Condition("operation.partnership_permissions == 'restricted'", description="Partnership has restrictions")
        ],
        actions=[
            Action("validate_partnership_permissions", parameters={
                'partnership_id': 'operation.partnership_id',
                'permission_level': 'operation.partnership_permissions',
                'data_sharing_agreement': True
            }),
            Action("enforce_partnership_boundaries", parameters={
                'data_usage_restrictions': True,
                'communication_protocols': True,
                'attribution_requirements': True
            }),
            Action("log_partnership_access", parameters={
                'partnership_id': 'operation.partnership_id',
                'operation_type': 'operation.type',
                'timestamp': 'now'
            })
        ],
        tags=['context', 'partnership', 'boundaries']
    ),
    
    Rule(
        name="validate_compliance_context",
        description="Ensure operations comply with relevant regulations and policies",
        priority=RulePriority.HIGH,
        context_types=[ContextType.BUSINESS_PROCESS],
        conditions=[
            Condition("operation.compliance_score < 0.8", description="Compliance score below threshold"),
            Condition("operation.regulatory_requirements.length > 0", description="Regulatory requirements exist")
        ],
        actions=[
            Action("flag_compliance_issues", parameters={
                'compliance_score': 'operation.compliance_score',
                'regulatory_requirements': 'operation.regulatory_requirements',
                'suggest_compliance_actions': True
            }),
            Action("require_compliance_review", parameters={
                'legal_review': True,
                'policy_alignment': True,
                'risk_assessment': True
            }),
            Action("log_compliance_violation", parameters={
                'operation_id': 'operation.id',
                'compliance_score': 'operation.compliance_score',
                'timestamp': 'now'
            })
        ],
        tags=['context', 'compliance', 'regulations']
    )
]


def get_project_rules():
    """Get all project context validation rules."""
    return PROJECT_RULES


def get_rules_by_context_type(context_type: str):
    """Get project rules by context type."""
    return [rule for rule in PROJECT_RULES if context_type in str(rule.conditions)]


def get_rules_by_priority(priority: RulePriority):
    """Get project rules by priority level."""
    return [rule for rule in PROJECT_RULES if rule.priority == priority]


def validate_movember_context(project_id: str, context_type: str) -> bool:
    """Validate if the context is appropriate for Movember operations."""
    if project_id != 'movember':
        return False
    
    valid_contexts = [
        'movember_impact', 'men_health', 'grant_evaluation', 
        'impact_analysis', 'reporting', 'research'
    ]
    
    return context_type in valid_contexts


def get_context_validation_summary():
    """Get a summary of context validation rules."""
    return {
        'total_rules': len(PROJECT_RULES),
        'critical_rules': len([r for r in PROJECT_RULES if r.priority == RulePriority.CRITICAL]),
        'high_priority_rules': len([r for r in PROJECT_RULES if r.priority == RulePriority.HIGH]),
        'context_types': ['business_process', 'data_validation'],
        'validation_areas': ['project', 'mission', 'data', 'permissions', 'geographic', 'temporal', 'operational', 'partnership', 'compliance']
    } 