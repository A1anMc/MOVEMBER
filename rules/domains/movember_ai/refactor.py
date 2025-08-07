"""
Movember AI Weekly Rule Refactoring

Automated weekly audit and refactoring logic for the Movember AI rules system.
Includes rule usage analysis, duplicate detection, and maintenance recommendations.
"""

from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import json
import os
from dataclasses import dataclass, field
from collections import defaultdict

from rules.types import Rule, RulePriority, ContextType


@dataclass
class RuleUsageMetrics:
    """Metrics for rule usage analysis."""
    rule_name: str
    total_executions: int = 0
    last_used: Optional[datetime] = None
    success_rate: float = 0.0
    average_execution_time: float = 0.0
    stakeholder_impact: str = "low"
    mission_alignment_score: float = 0.0


@dataclass
class DuplicateRuleAnalysis:
    """Analysis of potential duplicate rules."""
    primary_rule: str
    duplicate_rules: List[str]
    similarity_score: float
    suggested_action: str
    merge_recommendation: Optional[str] = None


@dataclass
class RefactorSummary:
    """Summary of refactoring recommendations."""
    audit_date: datetime
    total_rules: int
    unused_rules: List[str]
    duplicate_groups: List[DuplicateRuleAnalysis]
    performance_issues: List[str]
    recommendations: List[str]
    next_audit_date: datetime


# Weekly Refactoring Rules
REFACTOR_RULES = [
    Rule(
        name="auto_flag_unused_rules",
        description="Automatically flag rules that haven't been used in 30+ days",
        priority=RulePriority.MEDIUM,
        context_types=[ContextType.BUSINESS_PROCESS],
        conditions=[
            Condition("rule.last_used > 30 days ago", description="Rule not used in 30+ days"),
            Condition("rule.total_executions < 5", description="Rule has low usage")
        ],
        actions=[
            Action("flag_for_review", parameters={
                'reason': 'Stale rule – evaluate relevance',
                'suggested_action': 'review_or_archive',
                'priority': 'medium'
            }),
            Action("log_usage_metrics", parameters={
                'rule_name': 'rule.name',
                'days_since_last_use': 'days_since_last_use',
                'total_executions': 'rule.total_executions'
            })
        ],
        tags=['refactor', 'usage', 'maintenance']
    ),
    
    Rule(
        name="check_duplicate_logic",
        description="Identify rules with similar logic and suggest merges",
        priority=RulePriority.HIGH,
        context_types=[ContextType.BUSINESS_PROCESS],
        conditions=[
            Condition("rule.similarity_score >= 0.9", description="High similarity with other rules"),
            Condition("rule.duplicate_group.size > 1", description="Multiple similar rules exist")
        ],
        actions=[
            Action("suggest_merge", parameters={
                'target_rule': 'most_recent',
                'merge_strategy': 'consolidate_logic',
                'preserve_unique_features': True
            }),
            Action("create_merge_proposal", parameters={
                'primary_rule': 'rule.name',
                'duplicate_rules': 'rule.duplicate_group',
                'merge_benefits': ['reduced_complexity', 'improved_maintenance', 'consistent_behavior']
            })
        ],
        tags=['refactor', 'duplicates', 'consolidation']
    ),
    
    Rule(
        name="enforce_weekly_review",
        description="Trigger weekly audit and generate summary report",
        priority=RulePriority.CRITICAL,
        context_types=[ContextType.BUSINESS_PROCESS],
        conditions=[
            Condition("day_of_week == 'Friday'", description="Weekly audit day"),
            Condition("last_audit_date < 7 days ago", description="Audit due")
        ],
        actions=[
            Action("trigger_audit_log", parameters={
                'audit_type': 'weekly_refactor',
                'scope': 'all_rules',
                'metrics_collection': True
            }),
            Action("send_refactor_summary_to_admin", parameters={
                'recipients': ['admin@movember.com', 'rules_manager@movember.com'],
                'summary_format': 'markdown',
                'include_recommendations': True
            }),
            Action("schedule_next_audit", parameters={
                'next_audit_date': 'next_friday',
                'reminder_sent': False
            })
        ],
        tags=['refactor', 'audit', 'scheduling']
    ),
    
    Rule(
        name="flag_performance_issues",
        description="Identify rules with performance problems",
        priority=RulePriority.HIGH,
        context_types=[ContextType.BUSINESS_PROCESS],
        conditions=[
            Condition("rule.average_execution_time > 5.0", description="Slow rule execution"),
            Condition("rule.success_rate < 0.8", description="Low success rate")
        ],
        actions=[
            Action("flag_performance_issue", parameters={
                'issue_type': 'performance_problem',
                'rule_name': 'rule.name',
                'suggested_optimization': True
            }),
            Action("suggest_optimization", parameters={
                'condition_optimization': True,
                'action_streamlining': True,
                'caching_opportunities': True
            }),
            Action("schedule_performance_review", parameters={
                'review_date': 'next_week',
                'priority': 'high'
            })
        ],
        tags=['refactor', 'performance', 'optimization']
    ),
    
    Rule(
        name="validate_mission_alignment",
        description="Check if rules still align with current mission priorities",
        priority=RulePriority.MEDIUM,
        context_types=[ContextType.BUSINESS_PROCESS],
        conditions=[
            Condition("rule.mission_alignment_score < 0.7", description="Low mission alignment"),
            Condition("rule.last_mission_review > 90 days ago", description="Mission review overdue")
        ],
        actions=[
            Action("flag_mission_alignment", parameters={
                'issue_type': 'mission_misalignment',
                'rule_name': 'rule.name',
                'current_priorities': ['men_health', 'mental_health', 'research', 'community']
            }),
            Action("suggest_mission_update", parameters={
                'priority_areas': ['current_mission_focus'],
                'strategy_alignment': True,
                'stakeholder_needs': True
            }),
            Action("schedule_mission_review", parameters={
                'review_date': 'next_month',
                'stakeholder_consultation': True
            })
        ],
        tags=['refactor', 'mission', 'alignment']
    ),
    
    Rule(
        name="check_rule_dependencies",
        description="Identify and validate rule dependencies",
        priority=RulePriority.MEDIUM,
        context_types=[ContextType.BUSINESS_PROCESS],
        conditions=[
            Condition("rule.dependencies.count > 0", description="Rule has dependencies"),
            Condition("rule.dependency_health_score < 0.8", description="Dependency issues detected")
        ],
        actions=[
            Action("flag_dependency_issues", parameters={
                'issue_type': 'dependency_problem',
                'rule_name': 'rule.name',
                'affected_dependencies': 'rule.dependencies'
            }),
            Action("suggest_dependency_fixes", parameters={
                'dependency_updates': True,
                'alternative_approaches': True,
                'backward_compatibility': True
            }),
            Action("schedule_dependency_review", parameters={
                'review_date': 'next_week',
                'priority': 'medium'
            })
        ],
        tags=['refactor', 'dependencies', 'maintenance']
    ),
    
    Rule(
        name="validate_stakeholder_relevance",
        description="Ensure rules remain relevant to current stakeholder needs",
        priority=RulePriority.MEDIUM,
        context_types=[ContextType.BUSINESS_PROCESS],
        conditions=[
            Condition("rule.stakeholder_relevance_score < 0.6", description="Low stakeholder relevance"),
            Condition("rule.last_stakeholder_feedback > 180 days ago", description="Stakeholder feedback overdue")
        ],
        actions=[
            Action("flag_stakeholder_relevance", parameters={
                'issue_type': 'stakeholder_relevance',
                'rule_name': 'rule.name',
                'current_stakeholders': ['executive', 'funder', 'researcher', 'community']
            }),
            Action("suggest_stakeholder_update", parameters={
                'feedback_collection': True,
                'needs_assessment': True,
                'usability_improvement': True
            }),
            Action("schedule_stakeholder_consultation", parameters={
                'consultation_date': 'next_month',
                'feedback_methods': ['survey', 'interview', 'workshop']
            })
        ],
        tags=['refactor', 'stakeholder', 'relevance']
    )
]


class RuleRefactorEngine:
    """Engine for automated rule refactoring and maintenance."""
    
    def __init__(self, rules_directory: str = "rules/"):
        self.rules_directory = rules_directory
        self.audit_log_file = f"{rules_directory}logs/refactor_audit.json"
        self.summary_directory = f"{rules_directory}reports/"
        
        # Ensure directories exist
        os.makedirs(f"{rules_directory}logs/", exist_ok=True)
        os.makedirs(self.summary_directory, exist_ok=True)
    
    def run_weekly_audit(self) -> RefactorSummary:
        """Run the weekly audit and generate summary."""
        audit_date = datetime.now()
        
        # Collect all rules
        all_rules = self._collect_all_rules()
        
        # Analyze rule usage
        usage_metrics = self._analyze_rule_usage(all_rules)
        
        # Find unused rules
        unused_rules = self._identify_unused_rules(usage_metrics)
        
        # Find duplicate rules
        duplicate_groups = self._identify_duplicate_rules(all_rules)
        
        # Identify performance issues
        performance_issues = self._identify_performance_issues(usage_metrics)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            unused_rules, duplicate_groups, performance_issues
        )
        
        # Create summary
        summary = RefactorSummary(
            audit_date=audit_date,
            total_rules=len(all_rules),
            unused_rules=unused_rules,
            duplicate_groups=duplicate_groups,
            performance_issues=performance_issues,
            recommendations=recommendations,
            next_audit_date=audit_date + timedelta(days=7)
        )
        
        # Save audit log
        self._save_audit_log(summary)
        
        # Generate summary report
        self._generate_summary_report(summary)
        
        return summary
    
    def _collect_all_rules(self) -> List[Rule]:
        """Collect all rules from the system."""
        all_rules = []
        
        # Import rule modules
        from rules.domains.movember_ai.behaviours import get_ai_behaviour_rules
        from rules.domains.movember_ai.reporting import get_impact_report_rules
        from rules.domains.movember_ai.grant_rules import get_grant_rules
        from rules.domains.movember_ai.context import get_project_rules
        
        # Collect rules from all modules
        all_rules.extend(get_ai_behaviour_rules())
        all_rules.extend(get_impact_report_rules())
        all_rules.extend(get_grant_rules())
        all_rules.extend(get_project_rules())
        all_rules.extend(REFACTOR_RULES)
        
        return all_rules
    
    def _analyze_rule_usage(self, rules: List[Rule]) -> Dict[str, RuleUsageMetrics]:
        """Analyze usage metrics for all rules."""
        usage_metrics = {}
        
        for rule in rules:
            # Simulate usage metrics (in real implementation, these would come from actual usage data)
            metrics = RuleUsageMetrics(
                rule_name=rule.name,
                total_executions=self._get_rule_executions(rule.name),
                last_used=self._get_last_usage(rule.name),
                success_rate=self._get_success_rate(rule.name),
                average_execution_time=self._get_execution_time(rule.name),
                stakeholder_impact=self._get_stakeholder_impact(rule.name),
                mission_alignment_score=self._get_mission_alignment(rule.name)
            )
            usage_metrics[rule.name] = metrics
        
        return usage_metrics
    
    def _identify_unused_rules(self, usage_metrics: Dict[str, RuleUsageMetrics]) -> List[str]:
        """Identify rules that haven't been used recently."""
        unused_rules = []
        thirty_days_ago = datetime.now() - timedelta(days=30)
        
        for rule_name, metrics in usage_metrics.items():
            if (metrics.last_used is None or metrics.last_used < thirty_days_ago) and metrics.total_executions < 5:
                unused_rules.append(rule_name)
        
        return unused_rules
    
    def _identify_duplicate_rules(self, rules: List[Rule]) -> List[DuplicateRuleAnalysis]:
        """Identify potential duplicate rules."""
        duplicate_groups = []
        
        # Group rules by similarity
        rule_groups = self._group_similar_rules(rules)
        
        for group in rule_groups:
            if len(group) > 1:
                # Calculate similarity scores
                similarity_scores = self._calculate_similarity_scores(group)
                
                # Find the most similar pair
                max_similarity = max(similarity_scores.values())
                if max_similarity >= 0.9:
                    primary_rule = max(group, key=lambda r: r.priority.value)
                    duplicate_rules = [r.name for r in group if r.name != primary_rule.name]
                    
                    duplicate_groups.append(DuplicateRuleAnalysis(
                        primary_rule=primary_rule.name,
                        duplicate_rules=duplicate_rules,
                        similarity_score=max_similarity,
                        suggested_action="merge",
                        merge_recommendation=f"Merge {', '.join(duplicate_rules)} into {primary_rule.name}"
                    ))
        
        return duplicate_groups
    
    def _identify_performance_issues(self, usage_metrics: Dict[str, RuleUsageMetrics]) -> List[str]:
        """Identify rules with performance issues."""
        performance_issues = []
        
        for rule_name, metrics in usage_metrics.items():
            if metrics.average_execution_time > 5.0:
                performance_issues.append(f"{rule_name}: Slow execution ({metrics.average_execution_time:.2f}s)")
            
            if metrics.success_rate < 0.8:
                performance_issues.append(f"{rule_name}: Low success rate ({metrics.success_rate:.1%})")
        
        return performance_issues
    
    def _generate_recommendations(self, unused_rules: List[str], 
                                duplicate_groups: List[DuplicateRuleAnalysis],
                                performance_issues: List[str]) -> List[str]:
        """Generate refactoring recommendations."""
        recommendations = []
        
        if unused_rules:
            recommendations.append(f"Review {len(unused_rules)} unused rules for potential removal or updates")
        
        if duplicate_groups:
            recommendations.append(f"Consider merging {len(duplicate_groups)} duplicate rule groups")
        
        if performance_issues:
            recommendations.append(f"Optimize {len(performance_issues)} rules with performance issues")
        
        recommendations.extend([
            "Schedule stakeholder consultation for rule relevance assessment",
            "Update mission alignment for rules with low alignment scores",
            "Review and update rule dependencies",
            "Consider implementing rule versioning for better maintenance"
        ])
        
        return recommendations
    
    def _save_audit_log(self, summary: RefactorSummary) -> None:
        """Save audit log to JSON file."""
        audit_log = {
            'audit_date': summary.audit_date.isoformat(),
            'total_rules': summary.total_rules,
            'unused_rules': summary.unused_rules,
            'duplicate_groups': [
                {
                    'primary_rule': group.primary_rule,
                    'duplicate_rules': group.duplicate_rules,
                    'similarity_score': group.similarity_score,
                    'suggested_action': group.suggested_action
                }
                for group in summary.duplicate_groups
            ],
            'performance_issues': summary.performance_issues,
            'recommendations': summary.recommendations,
            'next_audit_date': summary.next_audit_date.isoformat()
        }
        
        with open(self.audit_log_file, 'w') as f:
            json.dump(audit_log, f, indent=2)
    
    def _generate_summary_report(self, summary: RefactorSummary) -> None:
        """Generate markdown summary report."""
        report_filename = f"refactor_summary_{summary.audit_date.strftime('%Y%m%d')}.md"
        report_path = os.path.join(self.summary_directory, report_filename)
        
        with open(report_path, 'w') as f:
            f.write(f"# Movember AI Rules Refactor Summary\n")
            f.write(f"**Audit Date:** {summary.audit_date.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write(f"## Executive Summary\n")
            f.write(f"- **Total Rules:** {summary.total_rules}\n")
            f.write(f"- **Unused Rules:** {len(summary.unused_rules)}\n")
            f.write(f"- **Duplicate Groups:** {len(summary.duplicate_groups)}\n")
            f.write(f"- **Performance Issues:** {len(summary.performance_issues)}\n\n")
            
            f.write(f"## Detailed Findings\n\n")
            
            if summary.unused_rules:
                f.write(f"### Unused Rules\n")
                for rule in summary.unused_rules:
                    f.write(f"- {rule}\n")
                f.write(f"\n")
            
            if summary.duplicate_groups:
                f.write(f"### Duplicate Rule Groups\n")
                for group in summary.duplicate_groups:
                    f.write(f"- **Primary:** {group.primary_rule}\n")
                    f.write(f"  - **Duplicates:** {', '.join(group.duplicate_rules)}\n")
                    f.write(f"  - **Similarity:** {group.similarity_score:.2f}\n")
                    f.write(f"  - **Recommendation:** {group.merge_recommendation}\n\n")
            
            if summary.performance_issues:
                f.write(f"### Performance Issues\n")
                for issue in summary.performance_issues:
                    f.write(f"- {issue}\n")
                f.write(f"\n")
            
            f.write(f"## Recommendations\n")
            for i, recommendation in enumerate(summary.recommendations, 1):
                f.write(f"{i}. {recommendation}\n")
            
            f.write(f"\n**Next Audit Date:** {summary.next_audit_date.strftime('%Y-%m-%d')}\n")
    
    # Helper methods for simulated metrics
    def _get_rule_executions(self, rule_name: str) -> int:
        """Get execution count for a rule (simulated)."""
        # In real implementation, this would query actual usage data
        return hash(rule_name) % 100  # Simulated data
    
    def _get_last_usage(self, rule_name: str) -> Optional[datetime]:
        """Get last usage date for a rule (simulated)."""
        # In real implementation, this would query actual usage data
        days_ago = hash(rule_name) % 60
        return datetime.now() - timedelta(days=days_ago) if days_ago > 0 else None
    
    def _get_success_rate(self, rule_name: str) -> float:
        """Get success rate for a rule (simulated)."""
        # In real implementation, this would query actual usage data
        return 0.7 + (hash(rule_name) % 30) / 100  # Simulated data
    
    def _get_execution_time(self, rule_name: str) -> float:
        """Get average execution time for a rule (simulated)."""
        # In real implementation, this would query actual usage data
        return 0.5 + (hash(rule_name) % 50) / 10  # Simulated data
    
    def _get_stakeholder_impact(self, rule_name: str) -> str:
        """Get stakeholder impact level (simulated)."""
        # In real implementation, this would be based on actual impact data
        impact_levels = ['low', 'medium', 'high']
        return impact_levels[hash(rule_name) % 3]
    
    def _get_mission_alignment(self, rule_name: str) -> float:
        """Get mission alignment score (simulated)."""
        # In real implementation, this would be based on actual alignment analysis
        return 0.6 + (hash(rule_name) % 40) / 100  # Simulated data
    
    def _group_similar_rules(self, rules: List[Rule]) -> List[List[Rule]]:
        """Group rules by similarity (simplified implementation)."""
        # In real implementation, this would use more sophisticated similarity analysis
        groups = []
        processed = set()
        
        for i, rule1 in enumerate(rules):
            if rule1.name in processed:
                continue
            
            group = [rule1]
            processed.add(rule1.name)
            
            for rule2 in rules[i+1:]:
                if rule2.name not in processed and self._are_rules_similar(rule1, rule2):
                    group.append(rule2)
                    processed.add(rule2.name)
            
            if len(group) > 1:
                groups.append(group)
        
        return groups
    
    def _are_rules_similar(self, rule1: Rule, rule2: Rule) -> bool:
        """Check if two rules are similar (simplified implementation)."""
        # In real implementation, this would use more sophisticated similarity analysis
        return (rule1.priority == rule2.priority and 
                any(tag in rule2.tags for tag in rule1.tags))
    
    def _calculate_similarity_scores(self, rules: List[Rule]) -> Dict[str, float]:
        """Calculate similarity scores between rules (simplified implementation)."""
        # In real implementation, this would use more sophisticated similarity analysis
        scores = {}
        for i, rule1 in enumerate(rules):
            for rule2 in rules[i+1:]:
                key = f"{rule1.name}_{rule2.name}"
                # Simplified similarity calculation
                similarity = 0.5  # Base similarity
                if rule1.priority == rule2.priority:
                    similarity += 0.2
                if any(tag in rule2.tags for tag in rule1.tags):
                    similarity += 0.3
                scores[key] = min(similarity, 1.0)
        return scores


def get_refactor_rules():
    """Get all refactoring rules."""
    return REFACTOR_RULES


def run_weekly_refactor():
    """Run the weekly refactor process."""
    engine = RuleRefactorEngine()
    summary = engine.run_weekly_audit()
    
    print(f"✅ Weekly refactor completed!")
    print(f"📊 Summary: {summary.total_rules} rules analyzed")
    print(f"🚨 Issues found: {len(summary.unused_rules)} unused, {len(summary.duplicate_groups)} duplicates")
    print(f"📋 Report generated: {engine.summary_directory}")
    
    return summary


if __name__ == "__main__":
    run_weekly_refactor() 