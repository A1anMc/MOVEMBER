#!/usr/bin/env python3
"""
Movember AI Rules System - AI Behaviour Rules
Ensures professional standards, data integrity, and mission alignment.
All text uses UK spelling and currency in AUD.
"""

from rules.types import Rule, Condition, Action, RulePriority
from rules.core import RuleEngine


# AI Behaviour Rules with UK spelling and AUD currency
AI_RULES = [
    Rule(
        name="ensure_expert_tone",
        conditions=[
            Condition("agent.role == 'impact_intelligence'"),
            Condition("agent.audience in ['executive', 'funder', 'researcher']")
        ],
        actions=[
            Action("use_professional_tone"),
            Action("require_evidence_for_claims"),
            Action("define_jargon"),
            Action("use_uk_spelling"),
            Action("display_currency_in_aud")
        ],
        priority=RulePriority.HIGH,
        description="Ensure professional tone with UK spelling and AUD currency for executive audiences"
    ),
    
    Rule(
        name="fail_gracefully_on_uncertainty",
        conditions=[Condition("agent.confidence < 0.6")],
        actions=[
            Action("defer_with_message", parameters={"message":"I need to verify this information before continuing."}),
            Action("request_additional_context"),
            Action("suggest_alternative_sources")
        ],
        priority=RulePriority.CRITICAL,
        description="Handle uncertainty professionally with UK spelling"
    ),
    
    Rule(
        name="maintain_data_integrity",
        conditions=[
            Condition("data.source_validation == False"),
            Condition("data.confidence_score < 0.8")
        ],
        actions=[
            Action("flag_data_for_review"),
            Action("request_source_verification"),
            Action("use_placeholder_if_missing"),
            Action("tag_data_sources_clearly")
        ],
        priority=RulePriority.CRITICAL,
        description="Ensure data integrity with proper source validation"
    ),
    
    Rule(
        name="align_with_movember_mission",
        conditions=[
            Condition("operation.mission_alignment_score < 0.7"),
            Condition("operation.focus not in ['men_health', 'mental_health', 'prostate_cancer', 'testicular_cancer']")
        ],
        actions=[
            Action("redirect_to_mission_scope"),
            Action("explain_mission_alignment"),
            Action("suggest_relevant_alternatives")
        ],
        priority=RulePriority.HIGH,
        description="Ensure all operations align with Movember's mission"
    ),
    
    Rule(
        name="explain_reasoning_when_asked",
        conditions=[
            Condition("user.request_type == 'explanation'"),
            Condition("agent.reasoning_required == True")
        ],
        actions=[
            Action("provide_detailed_reasoning"),
            Action("cite_evidence_sources"),
            Action("explain_trade_offs"),
            Action("use_uk_spelling_in_explanation")
        ],
        priority=RulePriority.MEDIUM,
        description="Provide clear reasoning with UK spelling when requested"
    ),
    
    Rule(
        name="adapt_to_stakeholder_role",
        conditions=[
            Condition("stakeholder.role in ['analyst', 'executive', 'funder', 'community']"),
            Condition("communication.tone_appropriate == False")
        ],
        actions=[
            Action("adjust_communication_style"),
            Action("use_role_appropriate_terminology"),
            Action("provide_relevant_context"),
            Action("ensure_uk_spelling_consistency")
        ],
        priority=RulePriority.MEDIUM,
        description="Adapt communication style to stakeholder role with UK spelling"
    ),
    
    Rule(
        name="enforce_professional_standards",
        conditions=[
            Condition("communication.formality_level < 0.8"),
            Condition("audience.includes_executive == True")
        ],
        actions=[
            Action("use_formal_language"),
            Action("maintain_professional_tone"),
            Action("ensure_uk_spelling"),
            Action("display_currency_in_aud"),
            Action("use_proper_citations")
        ],
        priority=RulePriority.HIGH,
        description="Maintain professional standards with UK spelling and AUD currency"
    ),
    
    Rule(
        name="validate_currency_display",
        conditions=[
            Condition("data.contains_currency == True"),
            Condition("currency.format != 'AUD'")
        ],
        actions=[
            Action("convert_to_aud"),
            Action("display_aud_format"),
            Action("include_currency_symbol"),
            Action("use_uk_number_format")
        ],
        priority=RulePriority.MEDIUM,
        description="Ensure all currency displays are in AUD with UK formatting"
    ),
    
    Rule(
        name="ensure_uk_spelling_consistency",
        conditions=[
            Condition("text.contains_american_spelling == True"),
            Condition("audience.includes_uk_users == True")
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
        name="handle_uncertainty_professionally",
        conditions=[
            Condition("agent.confidence < 0.5"),
            Condition("stakeholder.requires_certainty == True")
        ],
        actions=[
            Action("acknowledge_uncertainty"),
            Action("provide_confidence_level"),
            Action("suggest_verification_steps"),
            Action("use_uk_spelling_in_response")
        ],
        priority=RulePriority.HIGH,
        description="Handle uncertainty professionally with UK spelling"
    ),
    
    Rule(
        name="ensure_mission_alignment",
        conditions=[
            Condition("operation.mission_alignment_score < 0.6"),
            Condition("operation.type not in ['impact_analysis', 'grant_evaluation', 'health_research']")
        ],
        actions=[
            Action("redirect_to_mission_scope"),
            Action("explain_mission_requirements"),
            Action("suggest_appropriate_alternatives"),
            Action("use_uk_spelling_in_explanation")
        ],
        priority=RulePriority.CRITICAL,
        description="Ensure all operations align with Movember's mission using UK spelling"
    )
]


def get_ai_behaviour_rules() -> list:
    """Get all AI behaviour rules with UK spelling and AUD currency standards."""
    return AI_RULES


def validate_uk_spelling(text: str) -> bool:
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


def validate_aud_currency(amount: float, currency: str) -> bool:
    """
    Validate that currency is displayed in AUD.
    
    Args:
        amount: Amount to validate
        currency: Currency code
        
    Returns:
        True if currency is AUD, False otherwise
    """
    return currency.upper() == 'AUD'


def format_aud_currency(amount: float) -> str:
    """
    Format amount in AUD with UK number formatting.
    
    Args:
        amount: Amount to format
        
    Returns:
        Formatted AUD string
    """
    return f"A${amount:,.2f}"


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


def ensure_uk_spelling_and_aud_currency(data: dict) -> dict:
    """
    Ensure all text uses UK spelling and currency is in AUD.
    
    Args:
        data: Data to process
        
    Returns:
        Processed data with UK spelling and AUD currency
    """
    processed_data = data.copy()
    
    # Process text fields for UK spelling
    text_fields = ['title', 'description', 'summary', 'notes', 'comments']
    for field in text_fields:
        if field in processed_data and isinstance(processed_data[field], str):
            processed_data[field] = convert_to_uk_spelling(processed_data[field])
    
    # Process currency fields for AUD
    currency_fields = ['budget', 'amount', 'cost', 'funding', 'expense']
    for field in currency_fields:
        if field in processed_data and isinstance(processed_data[field], (int, float)):
            processed_data[f'{field}_currency'] = 'AUD'
            processed_data[f'{field}_formatted'] = format_aud_currency(processed_data[field])
    
    return processed_data


# Export functions for use in other modules
__all__ = [
    'AI_RULES',
    'get_ai_behaviour_rules',
    'validate_uk_spelling',
    'validate_aud_currency',
    'format_aud_currency',
    'convert_to_uk_spelling',
    'ensure_uk_spelling_and_aud_currency'
] 