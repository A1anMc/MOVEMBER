#!/usr/bin/env python3
"""
Movember AI Rules System - Context Validation Rules
Validates operational context with UK spelling and AUD currency standards.
"""

from rules.types import Rule, Condition, Action, RulePriority


# Context Validation Rules with UK spelling and AUD currency
PROJECT_RULES = [
    Rule(
        name="validate_movember_context",
        conditions=[Condition("project.id != 'movember'")],
        actions=[
            Action("abort", parameters={"message":"This agent only operates in Movember project context."}),
            Action("log_context_violation"),
            Action("redirect_to_movember_scope")
        ],
        priority=RulePriority.CRITICAL,
        description="Ensure operations are within Movember project context"
    ),

    Rule(
        name="validate_mission_alignment",
        conditions=[
            Condition("operation.mission_alignment_score < 0.7"),
            Condition("operation.focus not in ['men_health', 'mental_health', 'prostate_cancer', 'testicular_cancer']")
        ],
        actions=[
            Action("redirect_to_mission_scope"),
            Action("explain_mission_alignment"),
            Action("suggest_relevant_alternatives"),
            Action("use_uk_spelling_in_explanation")
        ],
        priority=RulePriority.HIGH,
        description="Ensure operations align with Movember's mission using UK spelling"
    ),

    Rule(
        name="validate_data_source_authority",
        conditions=[
            Condition("data.source not in ['movember_database', 'verified_external']"),
            Condition("data.confidence < 0.8")
        ],
        actions=[
            Action("flag_unverified_data"),
            Action("request_source_verification"),
            Action("use_placeholder_if_missing"),
            Action("tag_data_sources_clearly")
        ],
        priority=RulePriority.CRITICAL,
        description="Validate data source authority and reliability"
    ),

    Rule(
        name="validate_currency_standards",
        conditions=[
            Condition("data.contains_currency == True"),
            Condition("data.currency_format != 'AUD'")
        ],
        actions=[
            Action("convert_to_aud"),
            Action("display_aud_format"),
            Action("update_currency_references"),
            Action("validate_exchange_rates")
        ],
        priority=RulePriority.MEDIUM,
        description="Ensure all currency is displayed in AUD"
    ),

    Rule(
        name="validate_uk_spelling_consistency",
        conditions=[
            Condition("text.contains_american_spelling == True"),
            Condition("operation.requires_uk_spelling == True")
        ],
        actions=[
            Action("convert_to_uk_spelling"),
            Action("use_uk_terminology"),
            Action("maintain_consistency"),
            Action("update_spelling_preferences")
        ],
        priority=RulePriority.MEDIUM,
        description="Convert American spelling to UK spelling throughout"
    ),

    Rule(
        name="validate_stakeholder_authority",
        conditions=[
            Condition("stakeholder.role not in ['executive', 'funder', 'researcher', 'analyst', 'community']"),
            Condition("operation.requires_authorisation == True")
        ],
        actions=[
            Action("request_authorisation"),
            Action("validate_stakeholder_permissions"),
            Action("log_authorisation_attempt")
        ],
        priority=RulePriority.HIGH,
        description="Validate stakeholder authority for sensitive operations"
    ),

    Rule(
        name="validate_geographic_scope",
        conditions=[
            Condition("operation.geographic_scope not in ['australia', 'global', 'regional']"),
            Condition("operation.requires_geographic_validation == True")
        ],
        actions=[
            Action("validate_geographic_permissions"),
            Action("request_geographic_clarification"),
            Action("suggest_appropriate_scope")
        ],
        priority=RulePriority.MEDIUM,
        description="Validate geographic scope of operations"
    ),

    Rule(
        name="validate_temporal_context",
        conditions=[
            Condition("operation.timeline_months > 60"),
            Condition("operation.requires_temporal_validation == True")
        ],
        actions=[
            Action("validate_long_term_permissions"),
            Action("request_temporal_justification"),
            Action("suggest_timeline_adjustment")
        ],
        priority=RulePriority.MEDIUM,
        description="Validate temporal context for long-term operations"
    ),

    Rule(
        name="validate_budget_authority",
        conditions=[
            Condition("operation.budget > 1000000"),
            Condition("operation.requires_budget_authorisation == True")
        ],
        actions=[
            Action("request_budget_authorisation"),
            Action("validate_budget_permissions"),
            Action("ensure_aud_currency_format")
        ],
        priority=RulePriority.HIGH,
        description="Validate budget authority for high-cost operations"
    ),

    Rule(
        name="validate_data_privacy_compliance",
        conditions=[
            Condition("data.contains_personal_information == True"),
            Condition("data.privacy_compliance == 'unverified'")
        ],
        actions=[
            Action("require_privacy_compliance"),
            Action("validate_data_protection"),
            Action("request_privacy_authorisation")
        ],
        priority=RulePriority.CRITICAL,
        description="Validate data privacy compliance"
    ),

    Rule(
        name="validate_ethical_approval",
        conditions=[
            Condition("operation.involves_human_subjects == True"),
            Condition("operation.ethical_approval == 'pending'")
        ],
        actions=[
            Action("require_ethical_approval"),
            Action("validate_ethical_compliance"),
            Action("request_ethical_authorisation")
        ],
        priority=RulePriority.CRITICAL,
        description="Validate ethical approval for human subjects research"
    ),

    Rule(
        name="validate_partnership_authority",
        conditions=[
            Condition("operation.involves_partnerships == True"),
            Condition("operation.partnership_authorisation == 'missing'")
        ],
        actions=[
            Action("require_partnership_authorisation"),
            Action("validate_partnership_permissions"),
            Action("request_partnership_approval")
        ],
        priority=RulePriority.MEDIUM,
        description="Validate partnership authority for collaborative operations"
    ),

    Rule(
        name="validate_technology_compliance",
        conditions=[
            Condition("operation.uses_advanced_technology == True"),
            Condition("operation.technology_compliance == 'unverified'")
        ],
        actions=[
            Action("require_technology_compliance"),
            Action("validate_technology_permissions"),
            Action("request_technology_authorisation")
        ],
        priority=RulePriority.MEDIUM,
        description="Validate technology compliance for advanced operations"
    ),

    Rule(
        name="validate_communication_standards",
        conditions=[
            Condition("communication.requires_formal_tone == True"),
            Condition("communication.formality_level < 0.8")
        ],
        actions=[
            Action("enforce_formal_communication"),
            Action("ensure_uk_spelling"),
            Action("maintain_professional_standards"),
            Action("display_currency_in_aud")
        ],
        priority=RulePriority.MEDIUM,
        description="Validate communication standards with UK spelling and AUD currency"
    ),

    Rule(
        name="validate_operational_scope",
        conditions=[
            Condition("operation.scope not in ['impact_analysis', 'grant_evaluation', 'reporting', 'research']"),
            Condition("operation.requires_scope_validation == True")
        ],
        actions=[
            Action("validate_operational_permissions"),
            Action("request_scope_clarification"),
            Action("suggest_appropriate_scope")
        ],
        priority=RulePriority.MEDIUM,
        description="Validate operational scope alignment"
    )
]


def get_project_rules() -> list:
    """Get all project context validation rules with UK spelling and AUD currency standards."""
    return PROJECT_RULES


def validate_movember_context(project_id: str, operation_type: str) -> bool:
    """
    Validate that operation is within Movember project context.

    Args:
        project_id: Project identifier
        operation_type: Type of operation

    Returns:
        True if operation is valid for Movember context, False otherwise
    """
    valid_project_ids = ['movember', 'movember_ai', 'movember_impact']
    valid_operation_types = [
        'impact_analysis', 'grant_evaluation', 'reporting', 'research',
        'data_analysis', 'stakeholder_communication', 'health_research'
    ]

    return (project_id.lower() in valid_project_ids and
            operation_type.lower() in valid_operation_types)


def validate_currency_standards(data: dict) -> bool:
    """
    Validate that all currency in data is in AUD.

    Args:
        data: Data to validate

    Returns:
        True if all currency is AUD, False otherwise
    """
    currency_fields = ['budget', 'amount', 'cost', 'funding', 'expense']

    for field in currency_fields:
        if field in data:
            if isinstance(data[field], dict) and 'currency' in data[field]:
                if data[field]['currency'].upper() != 'AUD':
                    return False
            elif isinstance(data[field], (int, float)) and 'currency' in data:
                if data['currency'].upper() != 'AUD':
                    return False

    return True


def validate_uk_spelling_standards(text: str) -> bool:
    """
    Validate that text uses UK spelling.

    Args:
        text: Text to validate

    Returns:
        True if text uses UK spelling, False otherwise
    """
    uk_spellings = {
        'colour': 'color',
        'behaviour': 'behavior',
        'organisation': 'organization',
        'realise': 'realize',
        'analyse': 'analyze',
        'centre': 'center',
        'metre': 'meter',
        'programme': 'program',
        'licence': 'license',
        'defence': 'defense',
        'offence': 'offense',
        'practice': 'practise',
        'advice': 'advise',
        'specialise': 'specialize',
        'standardise': 'standardize',
        'optimise': 'optimize',
        'customise': 'customize',
        'summarise': 'summarize',
        'categorise': 'categorize',
        'prioritise': 'prioritize'
    }

    text_lower = text.lower()
    for uk_spelling, us_spelling in uk_spellings.items():
        if us_spelling in text_lower and uk_spelling not in text_lower:
            return False

    return True


def convert_to_uk_spelling(text: str) -> str:
    """
    Convert American spelling to UK spelling.

    Args:
        text: Text to convert

    Returns:
        Text with UK spelling
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

    converted_text = text
    for us_spelling, uk_spelling in uk_conversions.items():
        converted_text = converted_text.replace(us_spelling, uk_spelling)

    return converted_text


def format_aud_currency(amount: float) -> str:
    """
    Format amount in AUD with UK number formatting.

    Args:
        amount: Amount to format

    Returns:
        Formatted AUD string
    """
    return f"A${amount:,.2f}"


def validate_context_completeness(context_data: dict) -> dict:
    """
    Validate context data completeness.

    Args:
        context_data: Context data to validate

    Returns:
        Validation results
    """
    required_fields = [
        'project_id', 'operation_type', 'stakeholder_role', 'data_sources'
    ]

    missing_fields = []
    for field in required_fields:
        if field not in context_data or not context_data[field]:
            missing_fields.append(field)

    return {
        'complete': len(missing_fields) == 0,
        'missing_fields': missing_fields,
        'completeness_score': (len(required_fields) - len(missing_fields)) / len(required_fields)
    }


def validate_authority_level(operation_type: str, stakeholder_role: str) -> bool:
    """
    Validate that stakeholder has appropriate authority for operation.

    Args:
        operation_type: Type of operation
        stakeholder_role: Role of stakeholder

    Returns:
        True if stakeholder has appropriate authority, False otherwise
    """
    authority_mapping = {
        'impact_analysis': ['executive', 'analyst', 'researcher'],
        'grant_evaluation': ['executive', 'funder', 'analyst'],
        'reporting': ['executive', 'analyst', 'researcher'],
        'research': ['researcher', 'analyst'],
        'data_analysis': ['analyst', 'researcher'],
        'stakeholder_communication': ['executive', 'analyst'],
        'health_research': ['researcher', 'analyst']
    }

    required_roles = authority_mapping.get(operation_type, [])
    return stakeholder_role in required_roles


def generate_context_recommendations(context_data: dict) -> list:
    """
    Generate recommendations for context improvement.

    Args:
        context_data: Context data to analyse

    Returns:
        List of recommendations
    """
    recommendations = []

    # Check for project context
    if 'project_id' not in context_data or not validate_movember_context(
        context_data['project_id'], context_data.get('operation_type', '')
    ):
        recommendations.append("Ensure operation is within Movember project context")

    # Check for stakeholder authority
    if 'operation_type' in context_data and 'stakeholder_role' in context_data:
        if not validate_authority_level(context_data['operation_type'], context_data['stakeholder_role']):
            recommendations.append("Verify stakeholder has appropriate authority for this operation")

    # Check for currency standards
    if not validate_currency_standards(context_data):
        recommendations.append("Ensure all currency is displayed in AUD format")

    # Check for UK spelling
    text_fields = ['description', 'notes', 'comments']
    for field in text_fields:
        if field in context_data and isinstance(context_data[field], str):
            if not validate_uk_spelling_standards(context_data[field]):
                recommendations.append(f"Convert {field} to use UK spelling")

    # Check for data source validation
    if 'data_sources' in context_data:
        if not all(source in ['movember_database', 'verified_external'] for source in context_data['data_sources']):
            recommendations.append("Verify all data sources are authorised and reliable")

    return recommendations


# Export functions for use in other modules
__all__ = [
    'PROJECT_RULES',
    'get_project_rules',
    'validate_movember_context',
    'validate_currency_standards',
    'validate_uk_spelling_standards',
    'convert_to_uk_spelling',
    'format_aud_currency',
    'validate_context_completeness',
    'validate_authority_level',
    'generate_context_recommendations'
]
