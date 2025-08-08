#!/usr/bin/env python3
"""
Movember AI Rules System - Grant Lifecycle Rules
Manages grant application, evaluation, and lifecycle with UK spelling and AUD currency.
"""

from rules.types import Rule, Condition, Action, RulePriority
from rules.core import RuleEngine


# Grant Lifecycle Rules with UK spelling and AUD currency
GRANT_RULES = [
    Rule(
        name="grant_application_completeness",
        conditions=[
            Condition("grant.status == 'submitted'"),
            Condition("grant.application_fields.missing == []")
        ],
        actions=[
            Action("approve_grant_for_review"),
            Action("validate_uk_spelling"),
            Action("ensure_aud_currency_format")
        ],
        priority=RulePriority.CRITICAL,
        description="Validate grant application completeness with UK spelling and AUD currency"
    ),
    
    Rule(
        name="grant_to_impact_linkage",
        conditions=[Condition("grant.impact_metrics.length < 1")],
        actions=[
            Action("block_submission", parameters={"message":"Grants must include measurable impact metrics."}),
            Action("require_impact_metrics"),
            Action("suggest_impact_frameworks")
        ],
        priority=RulePriority.HIGH,
        description="Ensure grants include measurable impact metrics"
    ),
    
    Rule(
        name="budget_realism_validation",
        conditions=[
            Condition("grant.budget > 1000000"),
            Condition("grant.timeline_months < 12")
        ],
        actions=[
            Action("flag_for_review", parameters={"reason":"High budget for short timeline"}),
            Action("request_budget_justification"),
            Action("validate_aud_currency"),
            Action("suggest_timeline_adjustment")
        ],
        priority=RulePriority.MEDIUM,
        description="Validate budget realism with AUD currency"
    ),
    
    Rule(
        name="sdg_alignment_requirement",
        conditions=[Condition("grant.sdg_alignment.length == 0")],
        actions=[
            Action("require_sdg_alignment"),
            Action("suggest_relevant_sdgs"),
            Action("explain_sdg_importance")
        ],
        priority=RulePriority.MEDIUM,
        description="Require SDG alignment for all grants"
    ),
    
    Rule(
        name="sustainability_plan_validation",
        conditions=[
            Condition("grant.sustainability_plan == 'missing'"),
            Condition("grant.budget > 500000")
        ],
        actions=[
            Action("require_sustainability_plan"),
            Action("provide_sustainability_template"),
            Action("explain_sustainability_importance")
        ],
        priority=RulePriority.MEDIUM,
        description="Require sustainability plan for large grants"
    ),
    
    Rule(
        name="risk_mitigation_requirement",
        conditions=[
            Condition("grant.risk_mitigation == 'inadequate'"),
            Condition("grant.complexity_score > 0.7")
        ],
        actions=[
            Action("require_risk_mitigation_plan"),
            Action("suggest_risk_mitigation_strategies"),
            Action("request_risk_assessment")
        ],
        priority=RulePriority.MEDIUM,
        description="Require risk mitigation for complex grants"
    ),
    
    Rule(
        name="partnership_validation",
        conditions=[
            Condition("grant.partnerships.length < 1"),
            Condition("grant.scope == 'regional'")
        ],
        actions=[
            Action("suggest_partnership_opportunities"),
            Action("explain_partnership_benefits"),
            Action("provide_partnership_examples")
        ],
        priority=RulePriority.LOW,
        description="Suggest partnerships for regional grants"
    ),
    
    Rule(
        name="innovation_scoring",
        conditions=[
            Condition("grant.innovation_score < 6.0"),
            Condition("grant.funding_type == 'research'")
        ],
        actions=[
            Action("flag_low_innovation_score"),
            Action("suggest_innovation_enhancements"),
            Action("request_innovation_justification")
        ],
        priority=RulePriority.MEDIUM,
        description="Evaluate innovation score for research grants"
    ),
    
    Rule(
        name="aud_currency_validation",
        conditions=[
            Condition("grant.currency != 'AUD'"),
            Condition("grant.budget > 0")
        ],
        actions=[
            Action("convert_to_aud"),
            Action("display_aud_format"),
            Action("update_currency_references"),
            Action("validate_exchange_rates")
        ],
        priority=RulePriority.HIGH,
        description="Ensure all grant amounts are in AUD"
    ),
    
    Rule(
        name="uk_spelling_validation",
        conditions=[
            Condition("grant.description.contains_american_spelling == True"),
            Condition("grant.status in ['draft', 'submitted']")
        ],
        actions=[
            Action("convert_to_uk_spelling"),
            Action("validate_spelling_consistency"),
            Action("update_documentation"),
            Action("maintain_uk_terminology")
        ],
        priority=RulePriority.MEDIUM,
        description="Ensure all grant documentation uses UK spelling"
    ),
    
    Rule(
        name="grant_evaluation_completeness",
        conditions=[
            Condition("grant.evaluation_criteria.length < 3"),
            Condition("grant.budget > 250000")
        ],
        actions=[
            Action("require_evaluation_criteria"),
            Action("suggest_evaluation_frameworks"),
            Action("provide_evaluation_templates")
        ],
        priority=RulePriority.MEDIUM,
        description="Require comprehensive evaluation criteria for large grants"
    ),
    
    Rule(
        name="timeline_realism_check",
        conditions=[
            Condition("grant.timeline_months < 6"),
            Condition("grant.complexity_score > 0.8")
        ],
        actions=[
            Action("flag_unrealistic_timeline"),
            Action("suggest_timeline_extension"),
            Action("request_timeline_justification"),
            Action("provide_timeline_guidance")
        ],
        priority=RulePriority.MEDIUM,
        description="Validate timeline realism for complex grants"
    ),
    
    Rule(
        name="stakeholder_engagement_requirement",
        conditions=[
            Condition("grant.stakeholder_engagement == 'minimal'"),
            Condition("grant.community_impact == 'high'")
        ],
        actions=[
            Action("require_stakeholder_engagement_plan"),
            Action("suggest_engagement_strategies"),
            Action("provide_engagement_examples")
        ],
        priority=RulePriority.LOW,
        description="Require stakeholder engagement for high-impact grants"
    ),
    
    Rule(
        name="data_management_plan_requirement",
        conditions=[
            Condition("grant.data_management_plan == 'missing'"),
            Condition("grant.data_intensive == True")
        ],
        actions=[
            Action("require_data_management_plan"),
            Action("provide_dmp_template"),
            Action("explain_dmp_importance")
        ],
        priority=RulePriority.MEDIUM,
        description="Require data management plan for data-intensive grants"
    ),
    
    Rule(
        name="ethical_approval_validation",
        conditions=[
            Condition("grant.ethical_approval == 'pending'"),
            Condition("grant.human_subjects == True")
        ],
        actions=[
            Action("require_ethical_approval"),
            Action("suggest_ethical_guidelines"),
            Action("provide_approval_process")
        ],
        priority=RulePriority.HIGH,
        description="Require ethical approval for human subjects research"
    ),
    
    Rule(
        name="budget_breakdown_validation",
        conditions=[
            Condition("grant.budget_breakdown.detail_level < 0.7"),
            Condition("grant.budget > 100000")
        ],
        actions=[
            Action("require_detailed_budget_breakdown"),
            Action("provide_budget_template"),
            Action("suggest_budget_categories")
        ],
        priority=RulePriority.MEDIUM,
        description="Require detailed budget breakdown for significant grants"
    ),
    
    Rule(
        name="impact_measurement_framework",
        conditions=[
            Condition("grant.impact_measurement_framework == 'missing'"),
            Condition("grant.impact_focus == 'high'")
        ],
        actions=[
            Action("require_impact_measurement_framework"),
            Action("suggest_measurement_approaches"),
            Action("provide_framework_examples")
        ],
        priority=RulePriority.MEDIUM,
        description="Require impact measurement framework for high-impact grants"
    )
]


def get_grant_rules() -> list:
    """Get all grant lifecycle rules with UK spelling and AUD currency standards."""
    return GRANT_RULES


def validate_grant_currency(grant_data: dict) -> bool:
    """
    Validate that grant currency is in AUD.
    
    Args:
        grant_data: Grant data to validate
        
    Returns:
        True if currency is AUD, False otherwise
    """
    if 'currency' in grant_data:
        return grant_data['currency'].upper() == 'AUD'
    return True  # Default to AUD if not specified


def format_grant_budget(budget: float) -> str:
    """
    Format grant budget in AUD with UK number formatting.
    
    Args:
        budget: Budget amount
        
    Returns:
        Formatted AUD budget string
    """
    return f"A${budget:,.2f}"


def convert_grant_to_uk_spelling(grant_data: dict) -> dict:
    """
    Convert grant data to use UK spelling.
    
    Args:
        grant_data: Grant data to convert
        
    Returns:
        Grant data with UK spelling
    """
    uk_conversions = {
        'color': 'colour',
        'behavior': 'behaviour',
        'organization': 'organisation',
        'realize': 'realise',
        'analyze': 'analyse',
        'center': 'centre',
        'meter': 'metre',
        'program': 'programme',
        'license': 'licence',
        'defense': 'defence',
        'offense': 'offence',
        'specialize': 'specialise',
        'standardize': 'standardise',
        'optimize': 'optimise',
        'customize': 'customise',
        'summarize': 'summarise',
        'categorize': 'categorise',
        'prioritize': 'prioritise'
    }
    
    converted_data = grant_data.copy()
    
    # Convert text fields
    text_fields = ['title', 'description', 'summary', 'objectives', 'methodology']
    for field in text_fields:
        if field in converted_data and isinstance(converted_data[field], str):
            for us_spelling, uk_spelling in uk_conversions.items():
                converted_data[field] = converted_data[field].replace(us_spelling, uk_spelling)
    
    return converted_data


def validate_grant_completeness(grant_data: dict) -> dict:
    """
    Validate grant application completeness.
    
    Args:
        grant_data: Grant data to validate
        
    Returns:
        Validation results
    """
    required_fields = [
        'grant_id', 'title', 'budget', 'timeline_months', 
        'impact_metrics', 'sdg_alignment', 'sustainability_plan'
    ]
    
    missing_fields = []
    for field in required_fields:
        if field not in grant_data or not grant_data[field]:
            missing_fields.append(field)
    
    return {
        'complete': len(missing_fields) == 0,
        'missing_fields': missing_fields,
        'completeness_score': (len(required_fields) - len(missing_fields)) / len(required_fields)
    }


def calculate_grant_score(grant_data: dict) -> float:
    """
    Calculate overall grant score based on various criteria.
    
    Args:
        grant_data: Grant data to score
        
    Returns:
        Overall grant score (0-10)
    """
    score = 0.0
    
    # Completeness score (30%)
    completeness = validate_grant_completeness(grant_data)
    score += completeness['completeness_score'] * 3.0
    
    # Impact metrics score (25%)
    if 'impact_metrics' in grant_data and len(grant_data.get('impact_metrics', [])) > 0:
        score += 2.5
    
    # SDG alignment score (20%)
    if 'sdg_alignment' in grant_data and len(grant_data.get('sdg_alignment', [])) > 0:
        score += 2.0
    
    # Innovation score (15%)
    if 'innovation_score' in grant_data:
        score += min(grant_data['innovation_score'] / 10.0, 1.0) * 1.5
    
    # Budget realism score (10%)
    if 'budget' in grant_data and 'timeline_months' in grant_data:
        monthly_budget = grant_data['budget'] / grant_data['timeline_months']
        if monthly_budget < 100000:  # Realistic monthly budget
            score += 1.0
    
    return min(score, 10.0)


def generate_grant_recommendations(grant_data: dict) -> list:
    """
    Generate recommendations for grant improvement.
    
    Args:
        grant_data: Grant data to analyse
        
    Returns:
        List of recommendations
    """
    recommendations = []
    
    # Check for missing impact metrics
    if 'impact_metrics' not in grant_data or len(grant_data.get('impact_metrics', [])) == 0:
        recommendations.append("Include measurable impact metrics aligned with Movember's mission")
    
    # Check for missing SDG alignment
    if 'sdg_alignment' not in grant_data or len(grant_data.get('sdg_alignment', [])) == 0:
        recommendations.append("Specify alignment with Sustainable Development Goals (SDGs)")
    
    # Check for budget realism
    if 'budget' in grant_data and 'timeline_months' in grant_data:
        monthly_budget = grant_data['budget'] / grant_data['timeline_months']
        if monthly_budget > 200000:
            recommendations.append("Consider extending timeline or reducing budget for more realistic implementation")
    
    # Check for sustainability plan
    if 'sustainability_plan' not in grant_data or grant_data['sustainability_plan'] == 'missing':
        recommendations.append("Develop a comprehensive sustainability plan for long-term impact")
    
    # Check for stakeholder engagement
    if 'stakeholder_engagement' not in grant_data or grant_data['stakeholder_engagement'] == 'minimal':
        recommendations.append("Include stakeholder engagement strategies for community involvement")
    
    return recommendations


# Export functions for use in other modules
__all__ = [
    'GRANT_RULES',
    'get_grant_rules',
    'validate_grant_currency',
    'format_grant_budget',
    'convert_grant_to_uk_spelling',
    'validate_grant_completeness',
    'calculate_grant_score',
    'generate_grant_recommendations'
] 