"""
Movember Impact Reporting Rules

Defines rules for impact reporting to ensure proper framework alignment,
outcome mapping, and stakeholder-appropriate content.
"""

from rules.types import Rule, Condition, Action, RulePriority, ContextType


# Impact Reporting Rules for Movember
IMPACT_REPORT_RULES = [
    Rule(
        name="require_framework_alignment",
        description="Ensure all impact reports use appropriate theoretical frameworks",
        priority=RulePriority.CRITICAL,
        context_types=[ContextType.BUSINESS_PROCESS],
        conditions=[
            Condition("report.type == 'impact'", description="Report is impact-focused"),
            Condition("report.framework not in ['ToC', 'CEMP', 'SDG']", description="Missing required framework")
        ],
        actions=[
            Action("validate_frameworks", parameters={
                'allowed_frameworks': ['ToC', 'CEMP', 'SDG'],
                'require_at_least_one': True,
                'framework_description': True
            }),
            Action("enforce_framework_usage", parameters={
                'ToC': {'theory_of_change': True, 'causal_pathways': True},
                'CEMP': {'common_evaluation': True, 'measurement_protocols': True},
                'SDG': {'sustainable_development_goals': True, 'target_mapping': True}
            }),
            Action("flag_missing_framework", parameters={
                'message': 'Impact reports must use at least one framework: ToC, CEMP, or SDG',
                'suggest_framework': True
            })
        ],
        tags=['reporting', 'framework', 'impact']
    ),
    
    Rule(
        name="block_if_outputs_without_outcomes",
        description="Prevent reports that show outputs without linking to outcomes",
        priority=RulePriority.CRITICAL,
        context_types=[ContextType.BUSINESS_PROCESS],
        conditions=[
            Condition("report.outputs.count > 0", description="Report contains outputs"),
            Condition("report.outcomes.count == 0", description="No outcomes mapped"),
            Condition("report.type in ['impact', 'grant', 'evaluation']", description="Critical report type")
        ],
        actions=[
            Action("raise_error", parameters={
                'message': 'Every output must map to an outcome. Please link outputs to measurable outcomes.',
                'block_submission': True
            }),
            Action("suggest_outcome_mapping", parameters={
                'output_outcome_pairs': True,
                'measurement_guidance': True,
                'examples': True
            }),
            Action("log_mapping_issue", parameters={
                'issue_type': 'missing_outcome_mapping',
                'report_id': 'report.id',
                'timestamp': 'now'
            })
        ],
        tags=['reporting', 'outcomes', 'mapping']
    ),
    
    Rule(
        name="require_data_visualization",
        description="Ensure impact reports include appropriate data visualization",
        priority=RulePriority.HIGH,
        context_types=[ContextType.BUSINESS_PROCESS],
        conditions=[
            Condition("report.type == 'impact'", description="Impact report"),
            Condition("report.visualizations.count == 0", description="No visualizations included"),
            Condition("report.data_points.count > 5", description="Sufficient data for visualization")
        ],
        actions=[
            Action("require_visualization", parameters={
                'min_visualizations': 1,
                'suggested_types': ['trend_charts', 'impact_metrics', 'outcome_mapping'],
                'data_requirements': True
            }),
            Action("suggest_visualization_types", parameters={
                'impact_metrics': ['bar_charts', 'line_graphs', 'dashboards'],
                'outcome_mapping': ['flow_diagrams', 'causal_pathways'],
                'stakeholder_focus': ['executive_summaries', 'key_insights']
            }),
            Action("validate_visualization_accessibility", parameters={
                'color_blind_friendly': True,
                'alt_text': True,
                'clear_labels': True
            })
        ],
        tags=['reporting', 'visualization', 'data']
    ),
    
    Rule(
        name="enforce_attribution_vs_contribution",
        description="Ensure clear distinction between attribution and contribution claims",
        priority=RulePriority.HIGH,
        context_types=[ContextType.BUSINESS_PROCESS],
        conditions=[
            Condition("report.impact_claims.length > 0", description="Report contains impact claims"),
            Condition("report.attribution_clarity == 'unclear'", description="Attribution not clearly stated")
        ],
        actions=[
            Action("clarify_attribution", parameters={
                'require_attribution_statement': True,
                'distinguish_contribution': True,
                'evidence_requirements': True
            }),
            Action("add_attribution_disclaimer", parameters={
                'standard_text': 'This report shows contribution to outcomes, not direct attribution.',
                'methodology_notes': True,
                'limitations_section': True
            }),
            Action("validate_claim_evidence", parameters={
                'require_evidence': True,
                'confidence_levels': True,
                'data_sources': True
            })
        ],
        tags=['reporting', 'attribution', 'evidence']
    ),
    
    Rule(
        name="flag_data_gaps",
        description="Identify and flag gaps in impact data",
        priority=RulePriority.MEDIUM,
        context_types=[ContextType.BUSINESS_PROCESS],
        conditions=[
            Condition("report.data_coverage < 0.8", description="Data coverage below threshold"),
            Condition("report.type == 'impact'", description="Impact report")
        ],
        actions=[
            Action("identify_data_gaps", parameters={
                'missing_metrics': True,
                'incomplete_timeframes': True,
                'geographic_gaps': True
            }),
            Action("suggest_data_collection", parameters={
                'priority_gaps': True,
                'collection_methods': True,
                'timeline': True
            }),
            Action("add_gap_disclaimer", parameters={
                'gap_description': True,
                'impact_on_analysis': True,
                'recommendations': True
            })
        ],
        tags=['reporting', 'data_gaps', 'quality']
    ),
    
    Rule(
        name="require_narrative_summary",
        description="Ensure impact reports include narrative summary of key findings",
        priority=RulePriority.MEDIUM,
        context_types=[ContextType.BUSINESS_PROCESS],
        conditions=[
            Condition("report.type == 'impact'", description="Impact report"),
            Condition("report.narrative_summary.length < 200", description="Narrative summary too brief"),
            Condition("report.audience in ['executive', 'funder', 'stakeholder']", description="Stakeholder audience")
        ],
        actions=[
            Action("require_narrative", parameters={
                'min_length': 200,
                'key_sections': ['executive_summary', 'key_findings', 'implications'],
                'stakeholder_focus': True
            }),
            Action("suggest_narrative_structure", parameters={
                'executive': ['overview', 'key_insights', 'strategic_implications'],
                'funder': ['impact_metrics', 'outcome_achievement', 'sustainability'],
                'stakeholder': ['community_impact', 'health_outcomes', 'future_directions']
            }),
            Action("validate_narrative_clarity", parameters={
                'accessible_language': True,
                'clear_structure': True,
                'actionable_insights': True
            })
        ],
        tags=['reporting', 'narrative', 'stakeholder']
    ),
    
    Rule(
        name="enforce_sdg_alignment",
        description="Ensure impact reports align with Sustainable Development Goals",
        priority=RulePriority.HIGH,
        context_types=[ContextType.BUSINESS_PROCESS],
        conditions=[
            Condition("report.type == 'impact'", description="Impact report"),
            Condition("report.sdg_mapping.count == 0", description="No SDG alignment"),
            Condition("report.global_impact == True", description="Report has global implications")
        ],
        actions=[
            Action("require_sdg_mapping", parameters={
                'relevant_sdgs': ['SDG3', 'SDG4', 'SDG5', 'SDG10', 'SDG17'],
                'mapping_methodology': True,
                'target_alignment': True
            }),
            Action("suggest_sdg_metrics", parameters={
                'SDG3': ['health_outcomes', 'wellbeing_indicators'],
                'SDG4': ['education_impact', 'awareness_raising'],
                'SDG5': ['gender_equity', 'inclusive_approaches'],
                'SDG10': ['reduced_inequalities', 'access_improvement'],
                'SDG17': ['partnerships', 'capacity_building']
            }),
            Action("validate_sdg_contribution", parameters={
                'contribution_evidence': True,
                'target_progress': True,
                'partnership_impact': True
            })
        ],
        tags=['reporting', 'sdg', 'global_impact']
    ),
    
    Rule(
        name="validate_stakeholder_appropriateness",
        description="Ensure report content is appropriate for target stakeholders",
        priority=RulePriority.MEDIUM,
        context_types=[ContextType.BUSINESS_PROCESS],
        conditions=[
            Condition("report.audience in ['executive', 'funder', 'researcher', 'community']", 
                     description="Stakeholder audience identified"),
            Condition("report.content_appropriateness_score < 0.8", description="Content not sufficiently appropriate")
        ],
        actions=[
            Action("adjust_content_for_audience", parameters={
                'executive': {'strategic_focus': True, 'key_insights': True, 'actionable_recommendations': True},
                'funder': {'impact_metrics': True, 'roi_analysis': True, 'sustainability': True},
                'researcher': {'methodology': True, 'data_quality': True, 'statistical_significance': True},
                'community': {'accessible_language': True, 'practical_impact': True, 'local_relevance': True}
            }),
            Action("validate_technical_level", parameters={
                'executive': 'high_level_summary',
                'funder': 'impact_focused',
                'researcher': 'technical_detail',
                'community': 'accessible_summary'
            }),
            Action("ensure_cultural_sensitivity", parameters={
                'language_appropriateness': True,
                'cultural_context': True,
                'local_relevance': True
            })
        ],
        tags=['reporting', 'stakeholder', 'appropriateness']
    )
]


def get_impact_report_rules():
    """Get all impact reporting rules."""
    return IMPACT_REPORT_RULES


def get_rules_by_framework(framework: str):
    """Get impact reporting rules by framework."""
    if framework == 'ToC':
        return [rule for rule in IMPACT_REPORT_RULES if 'ToC' in rule.description or 'theory_of_change' in str(rule.actions)]
    elif framework == 'CEMP':
        return [rule for rule in IMPACT_REPORT_RULES if 'CEMP' in rule.description or 'common_evaluation' in str(rule.actions)]
    elif framework == 'SDG':
        return [rule for rule in IMPACT_REPORT_RULES if 'SDG' in rule.description or 'sustainable_development' in str(rule.actions)]
    return []


def get_rules_by_priority(priority: RulePriority):
    """Get impact reporting rules by priority level."""
    return [rule for rule in IMPACT_REPORT_RULES if rule.priority == priority] 