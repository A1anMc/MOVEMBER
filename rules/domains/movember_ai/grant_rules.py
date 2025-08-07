"""
Movember Grant Lifecycle Rules

Defines rules for grant application, evaluation, and lifecycle management
to ensure proper impact linkage and evaluation standards.
"""

from rules.types import Rule, Condition, Action, RulePriority, ContextType


# Grant Lifecycle Rules for Movember
GRANT_RULES = [
    Rule(
        name="grant_application_completeness",
        description="Ensure grant applications are complete before review",
        priority=RulePriority.CRITICAL,
        context_types=[ContextType.BUSINESS_PROCESS],
        conditions=[
            Condition("grant.status == 'submitted'", description="Grant has been submitted"),
            Condition("grant.application_fields.missing == []", description="All required fields completed"),
            Condition("grant.budget.total > 0", description="Budget information provided"),
            Condition("grant.timeline.start_date is not None", description="Timeline specified")
        ],
        actions=[
            Action("approve_grant_for_review", parameters={
                'review_priority': 'normal',
                'assign_reviewer': True,
                'notify_applicant': True
            }),
            Action("log_completeness_check", parameters={
                'grant_id': 'grant.id',
                'completeness_score': 1.0,
                'timestamp': 'now'
            })
        ],
        tags=['grant', 'completeness', 'submission']
    ),
    
    Rule(
        name="grant_to_impact_linkage",
        description="Ensure grants include proper impact metrics and outcomes",
        priority=RulePriority.CRITICAL,
        context_types=[ContextType.BUSINESS_PROCESS],
        conditions=[
            Condition("grant.impact_metrics.length < 1", description="No impact metrics specified"),
            Condition("grant.type in ['research', 'program', 'capacity_building']", description="Impact-focused grant type")
        ],
        actions=[
            Action("block_submission", parameters={
                'message': 'Grants must include measurable impact metrics linked to outcomes.',
                'require_impact_metrics': True
            }),
            Action("suggest_impact_metrics", parameters={
                'research': ['publications', 'knowledge_advancement', 'policy_influence'],
                'program': ['participant_outcomes', 'behavior_change', 'health_improvements'],
                'capacity_building': ['skill_development', 'organizational_growth', 'sustainability']
            }),
            Action("require_outcome_mapping", parameters={
                'short_term': True,
                'medium_term': True,
                'long_term': True
            })
        ],
        tags=['grant', 'impact', 'metrics']
    ),
    
    Rule(
        name="validate_grant_budget",
        description="Ensure grant budgets are realistic and properly justified",
        priority=RulePriority.HIGH,
        context_types=[ContextType.BUSINESS_PROCESS],
        conditions=[
            Condition("grant.budget.total > grant.category.max_amount", description="Budget exceeds category limit"),
            Condition("grant.budget.justification.length < 100", description="Insufficient budget justification")
        ],
        actions=[
            Action("flag_budget_issues", parameters={
                'issue_type': 'budget_exceeds_limit',
                'suggest_reduction': True,
                'require_justification': True
            }),
            Action("require_detailed_justification", parameters={
                'min_length': 200,
                'require_breakdown': True,
                'cost_effectiveness': True
            }),
            Action("suggest_budget_optimization", parameters={
                'cost_efficiency': True,
                'alternative_approaches': True,
                'partnership_opportunities': True
            })
        ],
        tags=['grant', 'budget', 'validation']
    ),
    
    Rule(
        name="enforce_sdg_alignment_for_grants",
        description="Ensure grants align with relevant Sustainable Development Goals",
        priority=RulePriority.HIGH,
        context_types=[ContextType.BUSINESS_PROCESS],
        conditions=[
            Condition("grant.type in ['research', 'program', 'global']", description="Grant with global implications"),
            Condition("grant.sdg_mapping.count == 0", description="No SDG alignment specified")
        ],
        actions=[
            Action("require_sdg_mapping", parameters={
                'relevant_sdgs': ['SDG3', 'SDG4', 'SDG5', 'SDG10', 'SDG17'],
                'mapping_justification': True,
                'target_contribution': True
            }),
            Action("suggest_sdg_metrics", parameters={
                'SDG3_health': ['health_outcomes', 'wellbeing_indicators', 'access_improvement'],
                'SDG4_education': ['awareness_raising', 'knowledge_dissemination', 'capacity_building'],
                'SDG5_gender': ['gender_equity', 'inclusive_approaches', 'women_empowerment'],
                'SDG10_inequality': ['reduced_inequalities', 'access_improvement', 'inclusive_growth'],
                'SDG17_partnerships': ['partnerships', 'capacity_building', 'knowledge_sharing']
            }),
            Action("validate_sdg_contribution", parameters={
                'contribution_evidence': True,
                'target_progress': True,
                'measurement_plan': True
            })
        ],
        tags=['grant', 'sdg', 'global_impact']
    ),
    
    Rule(
        name="validate_grant_timeline",
        description="Ensure grant timelines are realistic and achievable",
        priority=RulePriority.MEDIUM,
        context_types=[ContextType.BUSINESS_PROCESS],
        conditions=[
            Condition("grant.timeline.duration < grant.category.min_duration", description="Timeline too short"),
            Condition("grant.timeline.milestones.count < 3", description="Insufficient milestone detail")
        ],
        actions=[
            Action("flag_timeline_issues", parameters={
                'issue_type': 'unrealistic_timeline',
                'suggest_extension': True,
                'require_milestones': True
            }),
            Action("require_detailed_milestones", parameters={
                'min_milestones': 3,
                'quarterly_reviews': True,
                'progress_indicators': True
            }),
            Action("suggest_timeline_optimization", parameters={
                'realistic_duration': True,
                'milestone_planning': True,
                'risk_mitigation': True
            })
        ],
        tags=['grant', 'timeline', 'planning']
    ),
    
    Rule(
        name="validate_grant_evaluation_plan",
        description="Ensure grants include proper evaluation and monitoring plans",
        priority=RulePriority.HIGH,
        context_types=[ContextType.BUSINESS_PROCESS],
        conditions=[
            Condition("grant.evaluation_plan.length < 100", description="Insufficient evaluation plan"),
            Condition("grant.monitoring_indicators.count < 2", description="Insufficient monitoring indicators")
        ],
        actions=[
            Action("require_evaluation_plan", parameters={
                'min_length': 300,
                'methodology': True,
                'data_collection': True,
                'analysis_plan': True
            }),
            Action("require_monitoring_indicators", parameters={
                'min_indicators': 3,
                'baseline_measurement': True,
                'progress_tracking': True,
                'outcome_measurement': True
            }),
            Action("suggest_evaluation_framework", parameters={
                'ToC': 'theory_of_change',
                'CEMP': 'common_evaluation',
                'SDG': 'sustainable_development_goals'
            })
        ],
        tags=['grant', 'evaluation', 'monitoring']
    ),
    
    Rule(
        name="validate_grant_sustainability",
        description="Ensure grants include sustainability and long-term impact considerations",
        priority=RulePriority.MEDIUM,
        context_types=[ContextType.BUSINESS_PROCESS],
        conditions=[
            Condition("grant.sustainability_plan.length < 100", description="Insufficient sustainability plan"),
            Condition("grant.long_term_impact.length < 50", description="Insufficient long-term impact consideration")
        ],
        actions=[
            Action("require_sustainability_plan", parameters={
                'min_length': 200,
                'sustainability_factors': ['financial', 'institutional', 'community'],
                'long_term_vision': True
            }),
            Action("require_long_term_impact", parameters={
                'min_length': 150,
                'sustainability_indicators': True,
                'scaling_potential': True,
                'partnership_continuation': True
            }),
            Action("suggest_sustainability_metrics", parameters={
                'financial_sustainability': ['revenue_generation', 'cost_recovery', 'funding_diversification'],
                'institutional_sustainability': ['capacity_building', 'organizational_growth', 'policy_influence'],
                'community_sustainability': ['community_ownership', 'behavior_change', 'knowledge_retention']
            })
        ],
        tags=['grant', 'sustainability', 'long_term']
    ),
    
    Rule(
        name="validate_grant_risk_management",
        description="Ensure grants include proper risk assessment and mitigation strategies",
        priority=RulePriority.MEDIUM,
        context_types=[ContextType.BUSINESS_PROCESS],
        conditions=[
            Condition("grant.risk_assessment.length < 100", description="Insufficient risk assessment"),
            Condition("grant.risk_mitigation.count < 2", description="Insufficient risk mitigation strategies")
        ],
        actions=[
            Action("require_risk_assessment", parameters={
                'min_length': 200,
                'risk_categories': ['operational', 'financial', 'reputational', 'external'],
                'probability_impact': True
            }),
            Action("require_risk_mitigation", parameters={
                'min_strategies': 3,
                'contingency_plans': True,
                'monitoring_mechanisms': True
            }),
            Action("suggest_risk_mitigation", parameters={
                'operational_risks': ['backup_plans', 'resource_diversification', 'capacity_building'],
                'financial_risks': ['budget_reserves', 'funding_diversification', 'cost_controls'],
                'reputational_risks': ['stakeholder_engagement', 'transparency', 'quality_assurance'],
                'external_risks': ['partnership_backups', 'geographic_diversification', 'policy_advocacy']
            })
        ],
        tags=['grant', 'risk', 'mitigation']
    ),
    
    Rule(
        name="validate_grant_partnerships",
        description="Ensure grants include appropriate partnership and collaboration strategies",
        priority=RulePriority.MEDIUM,
        context_types=[ContextType.BUSINESS_PROCESS],
        conditions=[
            Condition("grant.partnerships.count < 1", description="No partnerships specified"),
            Condition("grant.type in ['global', 'capacity_building', 'research']", description="Partnership-focused grant type")
        ],
        actions=[
            Action("require_partnership_strategy", parameters={
                'min_partnerships': 1,
                'partnership_justification': True,
                'roles_responsibilities': True
            }),
            Action("suggest_partnership_types", parameters={
                'research': ['academic_institutions', 'research_organizations', 'policy_partners'],
                'capacity_building': ['local_organizations', 'training_partners', 'mentorship_programs'],
                'global': ['international_organizations', 'local_implementers', 'knowledge_partners']
            }),
            Action("validate_partnership_viability", parameters={
                'partner_capacity': True,
                'alignment_of_interests': True,
                'sustainability': True
            })
        ],
        tags=['grant', 'partnerships', 'collaboration']
    ),
    
    Rule(
        name="validate_grant_innovation",
        description="Ensure grants demonstrate innovation and novel approaches",
        priority=RulePriority.LOW,
        context_types=[ContextType.BUSINESS_PROCESS],
        conditions=[
            Condition("grant.innovation_score < 0.6", description="Insufficient innovation demonstrated"),
            Condition("grant.type in ['research', 'pilot', 'innovation']", description="Innovation-focused grant type")
        ],
        actions=[
            Action("require_innovation_justification", parameters={
                'min_length': 150,
                'novel_approaches': True,
                'methodology_innovation': True,
                'technology_innovation': True
            }),
            Action("suggest_innovation_areas", parameters={
                'methodology': ['novel_research_methods', 'innovative_evaluation_approaches'],
                'technology': ['digital_solutions', 'data_analytics', 'remote_delivery'],
                'partnerships': ['cross_sector_collaboration', 'unusual_partnerships'],
                'delivery': ['innovative_delivery_models', 'community_driven_approaches']
            }),
            Action("validate_innovation_impact", parameters={
                'scaling_potential': True,
                'knowledge_contribution': True,
                'replicability': True
            })
        ],
        tags=['grant', 'innovation', 'novelty']
    )
]


def get_grant_rules():
    """Get all grant lifecycle rules."""
    return GRANT_RULES


def get_rules_by_grant_type(grant_type: str):
    """Get grant rules by grant type."""
    return [rule for rule in GRANT_RULES if grant_type in rule.description or grant_type in str(rule.conditions)]


def get_rules_by_priority(priority: RulePriority):
    """Get grant rules by priority level."""
    return [rule for rule in GRANT_RULES if rule.priority == priority]


def get_rules_by_phase(phase: str):
    """Get grant rules by lifecycle phase."""
    phase_mapping = {
        'submission': ['completeness', 'budget', 'timeline'],
        'evaluation': ['impact', 'sdg', 'evaluation'],
        'implementation': ['monitoring', 'risk', 'partnerships'],
        'sustainability': ['sustainability', 'long_term', 'innovation']
    }
    
    relevant_tags = phase_mapping.get(phase, [])
    return [rule for rule in GRANT_RULES if any(tag in rule.tags for tag in relevant_tags)] 