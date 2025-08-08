#!/usr/bin/env python3
"""
Movember AI Rules System - Weekly Refactoring Rules
Manages weekly rule auditing and refactoring with UK spelling and AUD currency standards.
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional

from rules.types import Rule, Condition, Action, RulePriority


# Weekly Refactoring Rules with UK spelling and AUD currency
REFACTOR_RULES = [
    Rule(
        name="auto_flag_unused_rules",
        conditions=[Condition("rule.last_used > 30 days ago")],
        actions=[
            Action("flag_for_review", parameters={"reason":"Stale rule – evaluate relevance"}),
            Action("suggest_removal_or_update"),
            Action("log_refactoring_action")
        ],
        priority=RulePriority.MEDIUM,
        description="Flag unused rules for review with UK spelling standards"
    ),

    Rule(
        name="check_duplicate_logic",
        conditions=[Condition("rule.similarity_score >= 0.9")],
        actions=[
            Action("suggest_merge", parameters={"target_rule":"most_recent"}),
            Action("identify_duplicate_patterns"),
            Action("propose_consolidation")
        ],
        priority=RulePriority.MEDIUM,
        description="Identify and merge duplicate rule logic"
    ),

    Rule(
        name="enforce_weekly_review",
        conditions=[Condition("day_of_week == 'Friday'")],
        actions=[
            Action("trigger_audit_log"),
            Action("send_refactor_summary_to_admin"),
            Action("schedule_next_review")
        ],
        priority=RulePriority.HIGH,
        description="Enforce weekly refactoring schedule"
    ),

    Rule(
        name="validate_rule_uk_spelling_consistency",
        conditions=[
            Condition("rule.description.contains_american_spelling == True"),
            Condition("rule.status == 'active'")
        ],
        actions=[
            Action("convert_to_uk_spelling"),
            Action("update_rule_documentation"),
            Action("maintain_spelling_consistency")
        ],
        priority=RulePriority.MEDIUM,
        description="Ensure all rules use UK spelling consistently"
    ),

    Rule(
        name="validate_rule_aud_currency_standards",
        conditions=[
            Condition("rule.contains_currency_references == True"),
            Condition("rule.currency_format != 'AUD'")
        ],
        actions=[
            Action("convert_currency_to_aud"),
            Action("update_currency_references"),
            Action("validate_exchange_rates")
        ],
        priority=RulePriority.MEDIUM,
        description="Ensure all currency references are in AUD"
    ),

    Rule(
        name="optimise_rule_performance",
        conditions=[
            Condition("rule.execution_time > 1000"),
            Condition("rule.success_rate < 0.8")
        ],
        actions=[
            Action("optimise_rule_logic"),
            Action("suggest_performance_improvements"),
            Action("update_rule_efficiency")
        ],
        priority=RulePriority.HIGH,
        description="Optimise underperforming rules"
    ),

    Rule(
        name="validate_rule_dependencies",
        conditions=[
            Condition("rule.dependencies.count > 5"),
            Condition("rule.complexity_score > 0.8")
        ],
        actions=[
            Action("simplify_rule_dependencies"),
            Action("suggest_dependency_reduction"),
            Action("optimise_rule_structure")
        ],
        priority=RulePriority.MEDIUM,
        description="Simplify complex rule dependencies"
    ),

    Rule(
        name="check_rule_coverage",
        conditions=[
            Condition("rule.coverage_score < 0.6"),
            Condition("rule.importance_score > 0.7")
        ],
        actions=[
            Action("improve_rule_coverage"),
            Action("suggest_coverage_enhancements"),
            Action("update_rule_conditions")
        ],
        priority=RulePriority.MEDIUM,
        description="Improve rule coverage for important rules"
    ),

    Rule(
        name="validate_rule_consistency",
        conditions=[
            Condition("rule.consistency_score < 0.8"),
            Condition("rule.category in ['critical', 'high_priority']")
        ],
        actions=[
            Action("standardise_rule_format"),
            Action("ensure_consistency_across_rules"),
            Action("update_rule_standards")
        ],
        priority=RulePriority.HIGH,
        description="Ensure consistency across critical rules"
    ),

    Rule(
        name="cleanup_obsolete_rules",
        conditions=[
            Condition("rule.last_used > 90 days ago"),
            Condition("rule.success_rate < 0.3")
        ],
        actions=[
            Action("mark_for_removal"),
            Action("archive_obsolete_rule"),
            Action("update_rule_registry")
        ],
        priority=RulePriority.LOW,
        description="Remove obsolete and underperforming rules"
    ),

    Rule(
        name="validate_rule_documentation",
        conditions=[
            Condition("rule.documentation.length < 100"),
            Condition("rule.complexity_score > 0.6")
        ],
        actions=[
            Action("improve_rule_documentation"),
            Action("add_usage_examples"),
            Action("update_documentation_standards")
        ],
        priority=RulePriority.MEDIUM,
        description="Improve documentation for complex rules"
    ),

    Rule(
        name="optimise_rule_priorities",
        conditions=[
            Condition("rule.priority_mismatch == True"),
            Condition("rule.importance_score > 0.8")
        ],
        actions=[
            Action("adjust_rule_priority"),
            Action("validate_priority_assignment"),
            Action("update_priority_standards")
        ],
        priority=RulePriority.MEDIUM,
        description="Optimise rule priority assignments"
    ),

    Rule(
        name="validate_rule_security",
        conditions=[
            Condition("rule.security_score < 0.7"),
            Condition("rule.access_level == 'sensitive'")
        ],
        actions=[
            Action("enhance_rule_security"),
            Action("validate_access_controls"),
            Action("update_security_standards")
        ],
        priority=RulePriority.HIGH,
        description="Enhance security for sensitive rules"
    ),

    Rule(
        name="check_rule_scalability",
        conditions=[
            Condition("rule.scalability_score < 0.6"),
            Condition("rule.usage_frequency > 100")
        ],
        actions=[
            Action("improve_rule_scalability"),
            Action("optimise_for_high_usage"),
            Action("update_scalability_standards")
        ],
        priority=RulePriority.MEDIUM,
        description="Improve scalability for frequently used rules"
    ),

    Rule(
        name="validate_rule_maintainability",
        conditions=[
            Condition("rule.maintainability_score < 0.7"),
            Condition("rule.last_modified > 30 days ago")
        ],
        actions=[
            Action("improve_rule_maintainability"),
            Action("simplify_rule_structure"),
            Action("update_maintainability_standards")
        ],
        priority=RulePriority.MEDIUM,
        description="Improve maintainability of complex rules"
    )
]


@dataclass
class RefactorSummary:


    """Summary of refactoring results."""
    issues_found: int
    rules_optimised: int
    rules_removed: int
    performance_improvements: List[str]
    recommendations: List[str]
    audit_timestamp: datetime
    uk_spelling_fixes: int
    aud_currency_fixes: int


class RuleRefactorEngine:
    """Engine for managing rule refactoring and optimisation."""

    def __init__(self):


        self.logger = logging.getLogger(__name__)
        self.refactor_history = []

    async def run_weekly_refactor(self) -> RefactorSummary:
        """
        Run weekly refactoring process.

        Returns:
            Summary of refactoring results
        """
        self.logger.info("Starting weekly refactoring process")

        issues_found = 0
        rules_optimised = 0
        rules_removed = 0
        performance_improvements = []
        recommendations = []
        uk_spelling_fixes = 0
        aud_currency_fixes = 0

        # Check for unused rules
        unused_rules = await self._identify_unused_rules()
        if unused_rules:
            issues_found += len(unused_rules)
            recommendations.append(f"Consider removing {len(unused_rules)} unused rules")

        # Check for duplicate logic
        duplicate_rules = await self._identify_duplicate_logic()
        if duplicate_rules:
            issues_found += len(duplicate_rules)
            recommendations.append(f"Merge {len(duplicate_rules)} duplicate rule sets")

        # Validate UK spelling consistency
        spelling_issues = await self._validate_uk_spelling()
        uk_spelling_fixes = len(spelling_issues)
        if spelling_issues:
            issues_found += uk_spelling_fixes
            recommendations.append("Convert American spelling to UK spelling throughout")

        # Validate AUD currency standards
        currency_issues = await self._validate_aud_currency()
        aud_currency_fixes = len(currency_issues)
        if currency_issues:
            issues_found += aud_currency_fixes
            recommendations.append("Ensure all currency references are in AUD")

        # Optimise performance
        performance_issues = await self._optimise_rule_performance()
        if performance_issues:
            rules_optimised += len(performance_issues)
            performance_improvements.extend(performance_issues)

        # Clean up obsolete rules
        obsolete_rules = await self._identify_obsolete_rules()
        if obsolete_rules:
            rules_removed += len(obsolete_rules)
            recommendations.append(f"Remove {len(obsolete_rules)} obsolete rules")

        summary = RefactorSummary(
            issues_found=issues_found,
            rules_optimised=rules_optimised,
            rules_removed=rules_removed,
            performance_improvements=performance_improvements,
            recommendations=recommendations,
            audit_timestamp=datetime.now(),
            uk_spelling_fixes=uk_spelling_fixes,
            aud_currency_fixes=aud_currency_fixes
        )

        self.refactor_history.append(summary)
        self.logger.info(f"Weekly refactoring completed: {issues_found} issues found")

        return summary

    async def _identify_unused_rules(self) -> List[Dict]:
        """Identify rules that haven't been used recently."""
        # Simulate identifying unused rules
        return [
            {"rule_id": "RULE-001", "last_used": "45 days ago", "reason": "Stale rule"},
            {"rule_id": "RULE-002", "last_used": "60 days ago", "reason": "Unused rule"}
        ]

    async def _identify_duplicate_logic(self) -> List[Dict]:
        """Identify rules with duplicate logic."""
        # Simulate identifying duplicate logic
        return [
            {"rule_id": "RULE-003", "similarity_score": 0.95, "target_rule": "RULE-004"},
            {"rule_id": "RULE-005", "similarity_score": 0.92, "target_rule": "RULE-006"}
        ]

    async def _validate_uk_spelling(self) -> List[Dict]:
        """Validate UK spelling consistency across rules."""
        # Simulate finding spelling issues
        return [
            {"rule_id": "RULE-007", "issue": "American spelling detected", "fix": "Convert to UK spelling"},
            {"rule_id": "RULE-008", "issue": "Inconsistent terminology", "fix": "Standardise UK terminology"}
        ]

    async def _validate_aud_currency(self) -> List[Dict]:
        """Validate AUD currency standards across rules."""
        # Simulate finding currency issues
        return [
            {"rule_id": "RULE-009", "issue": "USD currency detected", "fix": "Convert to AUD"},
            {"rule_id": "RULE-010", "issue": "Missing currency format", "fix": "Add AUD formatting"}
        ]

    async def _optimise_rule_performance(self) -> List[str]:
        """Optimise rule performance."""
        # Simulate performance improvements
        return [
            "Reduced execution time for RULE-011 by 40%",
            "Improved success rate for RULE-012 by 25%",
            "Optimised memory usage for RULE-013"
        ]

    async def _identify_obsolete_rules(self) -> List[Dict]:
        """Identify obsolete rules for removal."""
        # Simulate identifying obsolete rules
        return [
            {"rule_id": "RULE-014", "reason": "No longer relevant", "last_used": "120 days ago"},
            {"rule_id": "RULE-015", "reason": "Replaced by newer rule", "last_used": "90 days ago"}
        ]

    def get_refactor_history(self) -> List[RefactorSummary]:


        """Get refactoring history."""
        return self.refactor_history

    def generate_refactor_report(self, summary: RefactorSummary) -> str:


        """
        Generate a human-readable refactoring report.

        Args:
            summary: Refactoring summary

        Returns:
            Formatted report string
        """
        report = f"""
# Weekly Refactoring Report - {summary.audit_timestamp.strftime('%Y-%m-%d')}

## Summary
- **Issues Found**: {summary.issues_found}
- **Rules Optimised**: {summary.rules_optimised}
- **Rules Removed**: {summary.rules_removed}
- **UK Spelling Fixes**: {summary.uk_spelling_fixes}
- **AUD Currency Fixes**: {summary.aud_currency_fixes}

## Performance Improvements
"""

        for improvement in summary.performance_improvements:
            report += f"- {improvement}\n"

        report += "\n## Recommendations\n"
        for recommendation in summary.recommendations:
            report += f"- {recommendation}\n"

        return report


def get_refactor_rules() -> list:
    """Get all refactoring rules with UK spelling and AUD currency standards."""
    return REFACTOR_RULES


async def run_weekly_refactor() -> RefactorSummary:
    """
    Run weekly refactoring process.

    Returns:
        Summary of refactoring results
    """
    engine = RuleRefactorEngine()
    return await engine.run_weekly_refactor()


def validate_rule_uk_spelling(rule_text: str) -> bool:
    """
    Validate that rule text uses UK spelling.

    Args:
        rule_text: Rule text to validate

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

    rule_text_lower = rule_text.lower()
    for uk_spelling, us_spelling in uk_spellings.items():
        if us_spelling in rule_text_lower and uk_spelling not in rule_text_lower:
            return False

    return True


def validate_rule_aud_currency(rule_data: dict) -> bool:
    """
    Validate that rule currency references are in AUD.

    Args:
        rule_data: Rule data to validate

    Returns:
        True if currency is AUD, False otherwise
    """
    if 'currency' in rule_data:
        return rule_data['currency'].upper() == 'AUD'
    return True  # Default to AUD if not specified


def convert_rule_to_uk_spelling(rule_text: str) -> str:
    """
    Convert rule text to use UK spelling.

    Args:
        rule_text: Rule text to convert

    Returns:
        Rule text with UK spelling
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

    converted_text = rule_text
    for us_spelling, uk_spelling in uk_conversions.items():
        converted_text = converted_text.replace(us_spelling, uk_spelling)

    return converted_text


def format_rule_currency(amount: float) -> str:
    """
    Format currency amount in AUD with UK number formatting.

    Args:
        amount: Amount to format

    Returns:
        Formatted AUD string
    """
    return f"A${amount:,.2f}"


# Export functions for use in other modules
__all__ = [
    'REFACTOR_RULES',
    'get_refactor_rules',
    'run_weekly_refactor',
    'RuleRefactorEngine',
    'RefactorSummary',
    'validate_rule_uk_spelling',
    'validate_rule_aud_currency',
    'convert_rule_to_uk_spelling',
    'format_rule_currency'
]
