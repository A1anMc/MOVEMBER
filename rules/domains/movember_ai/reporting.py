#!/usr/bin/env python3
"""
Movember AI Rules System - Impact Reporting Rules
Ensures quality impact reporting with UK spelling and AUD currency standards.
"""

from rules.types import Rule, Condition, Action, RulePriority
from rules.core import RuleEngine


# Impact Reporting Rules with UK spelling and AUD currency
IMPACT_REPORT_RULES = [
    Rule(
        name="require_framework_alignment",
        conditions=[Condition("report.type == 'impact'")],
        actions=[
            Action("validate_frameworks", parameters={"allowed":["ToC", "CEMP", "SDG"]}),
            Action("ensure_uk_spelling"),
            Action("display_currency_in_aud")
        ],
        priority=RulePriority.CRITICAL,
        description="Require framework alignment with UK spelling and AUD currency"
    ),
    
    Rule(
        name="block_if_outputs_without_outcomes",
        conditions=[
            Condition("report.outputs.count > 0"),
            Condition("report.outcomes.count == 0")
        ],
        actions=[
            Action("raise_error", parameters={"message":"Every output must map to a measurable outcome."}),
            Action("require_outcome_mapping"),
            Action("suggest_outcome_metrics")
        ],
        priority=RulePriority.CRITICAL,
        description="Ensure outputs are linked to measurable outcomes"
    ),
    
    Rule(
        name="require_data_visualisation",
        conditions=[
            Condition("report.type == 'impact'"),
            Condition("report.visualisations.count == 0")
        ],
        actions=[
            Action("require_visualisation", parameters={"type":"charts_or_graphs"}),
            Action("suggest_visualisation_types"),
            Action("provide_visualisation_templates")
        ],
        priority=RulePriority.MEDIUM,
        description="Require data visualisation for impact reports"
    ),
    
    Rule(
        name="clarify_attribution_vs_contribution",
        conditions=[Condition("report.attribution == 'unclear'")],
        actions=[
            Action("require_clarification", parameters={"field":"attribution_methodology"}),
            Action("explain_attribution_vs_contribution"),
            Action("provide_attribution_examples")
        ],
        priority=RulePriority.HIGH,
        description="Clarify attribution vs contribution distinction"
    ),
    
    Rule(
        name="flag_data_gaps",
        conditions=[
            Condition("report.data_gaps.count > 0"),
            Condition("report.confidence_level < 0.8")
        ],
        actions=[
            Action("flag_data_gaps"),
            Action("suggest_data_collection_methods"),
            Action("provide_gap_mitigation_strategies")
        ],
        priority=RulePriority.MEDIUM,
        description="Flag and address data gaps in impact reports"
    ),
    
    Rule(
        name="validate_stakeholder_appropriateness",
        conditions=[
            Condition("report.audience not in ['executive', 'funder', 'researcher', 'community']"),
            Condition("report.complexity_level > 0.7")
        ],
        actions=[
            Action("adjust_complexity_for_audience"),
            Action("provide_audience_appropriate_summary"),
            Action("ensure_uk_spelling_consistency")
        ],
        priority=RulePriority.MEDIUM,
        description="Ensure reports are appropriate for target audience"
    ),
    
    Rule(
        name="require_baseline_comparison",
        conditions=[
            Condition("report.baseline_data == 'missing'"),
            Condition("report.impact_measurement == 'required'")
        ],
        actions=[
            Action("require_baseline_data"),
            Action("suggest_baseline_collection_methods"),
            Action("provide_baseline_examples")
        ],
        priority=RulePriority.HIGH,
        description="Require baseline data for impact measurement"
    ),
    
    Rule(
        name="validate_impact_metrics",
        conditions=[
            Condition("report.impact_metrics.count < 3"),
            Condition("report.type == 'comprehensive_impact'")
        ],
        actions=[
            Action("require_minimum_impact_metrics"),
            Action("suggest_additional_metrics"),
            Action("provide_metric_frameworks")
        ],
        priority=RulePriority.MEDIUM,
        description="Validate sufficient impact metrics"
    ),
    
    Rule(
        name="ensure_uk_spelling_in_reports",
        conditions=[
            Condition("report.text.contains_american_spelling == True"),
            Condition("report.status in ['draft', 'final']")
        ],
        actions=[
            Action("convert_to_uk_spelling"),
            Action("validate_spelling_consistency"),
            Action("update_report_documentation"),
            Action("maintain_uk_terminology")
        ],
        priority=RulePriority.MEDIUM,
        description="Ensure all impact reports use UK spelling"
    ),
    
    Rule(
        name="validate_aud_currency_in_reports",
        conditions=[
            Condition("report.contains_currency == True"),
            Condition("report.currency_format != 'AUD'")
        ],
        actions=[
            Action("convert_currency_to_aud"),
            Action("display_aud_format"),
            Action("include_currency_symbol"),
            Action("use_uk_number_format")
        ],
        priority=RulePriority.HIGH,
        description="Ensure all currency in reports is displayed in AUD"
    ),
    
    Rule(
        name="require_methodology_description",
        conditions=[
            Condition("report.methodology.length < 200"),
            Condition("report.type == 'research_impact'")
        ],
        actions=[
            Action("require_detailed_methodology"),
            Action("suggest_methodology_sections"),
            Action("provide_methodology_templates")
        ],
        priority=RulePriority.MEDIUM,
        description="Require detailed methodology for research impact reports"
    ),
    
    Rule(
        name="validate_statistical_significance",
        conditions=[
            Condition("report.statistical_tests == 'missing'"),
            Condition("report.sample_size > 100")
        ],
        actions=[
            Action("require_statistical_analysis"),
            Action("suggest_statistical_tests"),
            Action("provide_statistical_guidance")
        ],
        priority=RulePriority.MEDIUM,
        description="Validate statistical significance for large datasets"
    ),
    
    Rule(
        name="ensure_ethical_reporting",
        conditions=[
            Condition("report.ethical_considerations == 'missing'"),
            Condition("report.human_subjects == True")
        ],
        actions=[
            Action("require_ethical_considerations"),
            Action("suggest_ethical_guidelines"),
            Action("provide_ethical_frameworks")
        ],
        priority=RulePriority.HIGH,
        description="Ensure ethical considerations in impact reports"
    ),
    
    Rule(
        name="validate_longitudinal_tracking",
        conditions=[
            Condition("report.timeline_months > 12"),
            Condition("report.longitudinal_data == 'missing'")
        ],
        actions=[
            Action("require_longitudinal_analysis"),
            Action("suggest_tracking_methods"),
            Action("provide_longitudinal_frameworks")
        ],
        priority=RulePriority.MEDIUM,
        description="Validate longitudinal tracking for long-term projects"
    ),
    
    Rule(
        name="ensure_stakeholder_engagement",
        conditions=[
            Condition("report.stakeholder_engagement == 'minimal'"),
            Condition("report.community_impact == 'high'")
        ],
        actions=[
            Action("require_stakeholder_engagement_section"),
            Action("suggest_engagement_methods"),
            Action("provide_engagement_examples")
        ],
        priority=RulePriority.LOW,
        description="Ensure stakeholder engagement in community impact reports"
    ),
    
    Rule(
        name="validate_cost_effectiveness",
        conditions=[
            Condition("report.cost_effectiveness_analysis == 'missing'"),
            Condition("report.total_cost > 100000")
        ],
        actions=[
            Action("require_cost_effectiveness_analysis"),
            Action("suggest_cost_effectiveness_metrics"),
            Action("provide_cost_effectiveness_frameworks")
        ],
        priority=RulePriority.MEDIUM,
        description="Validate cost effectiveness analysis for high-cost projects"
    ),
    
    Rule(
        name="ensure_sustainability_indicators",
        conditions=[
            Condition("report.sustainability_indicators == 'missing'"),
            Condition("report.project_duration > 24")
        ],
        actions=[
            Action("require_sustainability_indicators"),
            Action("suggest_sustainability_metrics"),
            Action("provide_sustainability_frameworks")
        ],
        priority=RulePriority.MEDIUM,
        description="Ensure sustainability indicators for long-term projects"
    )
]


def get_impact_report_rules() -> list:
    """Get all impact reporting rules with UK spelling and AUD currency standards."""
    return IMPACT_REPORT_RULES


def validate_report_currency(report_data: dict) -> bool:
    """
    Validate that report currency is in AUD.
    
    Args:
        report_data: Report data to validate
        
    Returns:
        True if currency is AUD, False otherwise
    """
    if 'currency' in report_data:
        return report_data['currency'].upper() == 'AUD'
    return True  # Default to AUD if not specified


def format_report_currency(amount: float) -> str:
    """
    Format currency amount in AUD with UK number formatting.
    
    Args:
        amount: Amount to format
        
    Returns:
        Formatted AUD string
    """
    return f"A${amount:,.2f}"


def convert_report_to_uk_spelling(report_data: dict) -> dict:
    """
    Convert report data to use UK spelling.
    
    Args:
        report_data: Report data to convert
        
    Returns:
        Report data with UK spelling
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
    
    converted_data = report_data.copy()
    
    # Convert text fields
    text_fields = ['title', 'summary', 'methodology', 'conclusions', 'recommendations']
    for field in text_fields:
        if field in converted_data and isinstance(converted_data[field], str):
            for us_spelling, uk_spelling in uk_conversions.items():
                converted_data[field] = converted_data[field].replace(us_spelling, uk_spelling)
    
    return converted_data


def validate_report_completeness(report_data: dict) -> dict:
    """
    Validate impact report completeness.
    
    Args:
        report_data: Report data to validate
        
    Returns:
        Validation results
    """
    required_fields = [
        'report_id', 'title', 'type', 'frameworks', 'outputs', 'outcomes',
        'stakeholders', 'data_sources', 'visualisations'
    ]
    
    missing_fields = []
    for field in required_fields:
        if field not in report_data or not report_data[field]:
            missing_fields.append(field)
    
    return {
        'complete': len(missing_fields) == 0,
        'missing_fields': missing_fields,
        'completeness_score': (len(required_fields) - len(missing_fields)) / len(required_fields)
    }


def calculate_report_quality_score(report_data: dict) -> float:
    """
    Calculate impact report quality score.
    
    Args:
        report_data: Report data to score
        
    Returns:
        Quality score (0-10)
    """
    score = 0.0
    
    # Completeness score (30%)
    completeness = validate_report_completeness(report_data)
    score += completeness['completeness_score'] * 3.0
    
    # Framework alignment score (25%)
    if 'frameworks' in report_data and len(report_data.get('frameworks', [])) > 0:
        score += 2.5
    
    # Output-outcome mapping score (20%)
    if 'outputs' in report_data and 'outcomes' in report_data:
        if len(report_data['outputs']) > 0 and len(report_data['outcomes']) > 0:
            score += 2.0
    
    # Visualisation score (15%)
    if 'visualisations' in report_data and len(report_data.get('visualisations', [])) > 0:
        score += 1.5
    
    # Data quality score (10%)
    if 'data_sources' in report_data and len(report_data.get('data_sources', [])) > 0:
        score += 1.0
    
    return min(score, 10.0)


def generate_report_recommendations(report_data: dict) -> list:
    """
    Generate recommendations for impact report improvement.
    
    Args:
        report_data: Report data to analyse
        
    Returns:
        List of recommendations
    """
    recommendations = []
    
    # Check for framework alignment
    if 'frameworks' not in report_data or len(report_data.get('frameworks', [])) == 0:
        recommendations.append("Include alignment with ToC, CEMP, or SDG frameworks")
    
    # Check for output-outcome mapping
    if 'outputs' in report_data and 'outcomes' in report_data:
        if len(report_data['outputs']) > 0 and len(report_data['outcomes']) == 0:
            recommendations.append("Map all outputs to measurable outcomes")
    
    # Check for data visualisation
    if 'visualisations' not in report_data or len(report_data.get('visualisations', [])) == 0:
        recommendations.append("Include data visualisations to enhance impact communication")
    
    # Check for attribution clarity
    if 'attribution' in report_data and report_data['attribution'] == 'unclear':
        recommendations.append("Clarify attribution vs contribution methodology")
    
    # Check for data gaps
    if 'data_gaps' in report_data and len(report_data['data_gaps']) > 0:
        recommendations.append("Address identified data gaps with additional data collection")
    
    # Check for stakeholder appropriateness
    if 'audience' in report_data and report_data['audience'] not in ['executive', 'funder', 'researcher', 'community']:
        recommendations.append("Ensure report complexity is appropriate for target audience")
    
    return recommendations


def validate_framework_compliance(report_data: dict) -> dict:
    """
    Validate framework compliance for impact reports.
    
    Args:
        report_data: Report data to validate
        
    Returns:
        Framework compliance results
    """
    frameworks = report_data.get('frameworks', [])
    compliance = {
        'toc_compliant': 'ToC' in frameworks,
        'cemp_compliant': 'CEMP' in frameworks,
        'sdg_compliant': 'SDG' in frameworks,
        'has_framework': len(frameworks) > 0
    }
    
    compliance['overall_compliant'] = compliance['has_framework']
    
    return compliance


# Export functions for use in other modules
__all__ = [
    'IMPACT_REPORT_RULES',
    'get_impact_report_rules',
    'validate_report_currency',
    'format_report_currency',
    'convert_report_to_uk_spelling',
    'validate_report_completeness',
    'calculate_report_quality_score',
    'generate_report_recommendations',
    'validate_framework_compliance'
] 