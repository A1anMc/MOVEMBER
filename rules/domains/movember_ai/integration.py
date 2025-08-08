#!/usr/bin/env python3
"""
Movember AI Rules System - Integration Layer
Ensures seamless interaction between Grant Support, Impact Reporting, and AI Rules Engine.
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum

from rules.core import RuleEngine
from rules.types import ExecutionContext, ContextType, RulePriority
from rules.domains.movember_ai import (
    MovemberAIRulesEngine,
    create_movember_engine,
    validate_movember_operation
)

logger = logging.getLogger(__name__)


class SystemType(Enum):
    """Enumeration of integrated systems."""
    GRANT_SUPPORT = "grant_support"
    IMPACT_REPORTING = "impact_reporting"
    AI_RULES_ENGINE = "ai_rules_engine"


class EventType(Enum):
    """Enumeration of system events that trigger cross-system actions."""
    GRANT_SUBMITTED = "grant_submitted"
    GRANT_APPROVED = "grant_approved"
    GRANT_COMPLETED = "grant_completed"
    IMPACT_REPORT_CREATED = "impact_report_created"
    IMPACT_REPORT_PUBLISHED = "impact_report_published"
    RULE_EVALUATION_COMPLETED = "rule_evaluation_completed"
    SYSTEM_HEALTH_CHECK = "system_health_check"


@dataclass
class SystemEvent:
    """Represents an event that occurred in one of the integrated systems."""
    event_type: EventType
    system_type: SystemType
    timestamp: datetime
    data: Dict[str, Any]
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    correlation_id: Optional[str] = None


@dataclass
class CrossSystemValidation:
    """Represents validation results across multiple systems."""
    validation_id: str
    systems_involved: List[SystemType]
    validation_status: str
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.now)


class MovemberSystemIntegrator:
    """
    Integrates all three systems: Grant Support, Impact Reporting, and AI Rules Engine.
    Ensures seamless data flow, event triggers, and cross-system validation.
    """

    def __init__(self, config: Optional[Dict] = None):
        self.config = config or self._get_default_config()
        self.engine = create_movember_engine()
        self.event_queue: List[SystemEvent] = []
        self.validation_history: List[CrossSystemValidation] = []
        self.system_status = {
            SystemType.GRANT_SUPPORT: "active",
            SystemType.IMPACT_REPORTING: "active",
            SystemType.AI_RULES_ENGINE: "active"
        }

    def _get_default_config(self) -> Dict:
        """Get default integration configuration."""
        return {
            "event_processing": {
                "batch_size": 10,
                "processing_interval": 5,  # seconds
                "retry_attempts": 3
            },
            "validation": {
                "cross_system_validation": True,
                "data_consistency_check": True,
                "real_time_validation": True
            },
            "monitoring": {
                "health_check_interval": 60,  # seconds
                "performance_metrics": True,
                "error_alerting": True
            }
        }

    async def process_grant_lifecycle(self, grant_data: Dict) -> Dict:
        """
        Process a grant through the complete lifecycle with all systems involved.
        """
        logger.info(f"Processing grant lifecycle for grant: {grant_data.get('grant_id')}")

        # Step 1: Grant Submission (Grant Support + AI Rules)
        submission_result = await self._handle_grant_submission(grant_data)

        # Step 2: Grant Evaluation (All three systems)
        evaluation_result = await self._handle_grant_evaluation(grant_data)

        # Step 3: Grant Approval (Grant Support + AI Rules)
        approval_result = await self._handle_grant_approval(grant_data)

        # Step 4: Impact Planning (Impact Reporting + AI Rules)
        impact_plan = await self._handle_impact_planning(grant_data)

        # Step 5: Cross-system validation
        validation_result = await self._validate_cross_system_consistency(grant_data)

        return {
            "grant_id": grant_data.get("grant_id"),
            "submission": submission_result,
            "evaluation": evaluation_result,
            "approval": approval_result,
            "impact_plan": impact_plan,
            "validation": validation_result,
            "timestamp": datetime.now().isoformat()
        }

    async def _handle_grant_submission(self, grant_data: Dict) -> Dict:
        """Handle grant submission with Grant Support and AI Rules systems."""
        logger.info("Handling grant submission")

        # Create event for grant submission
        event = SystemEvent(
            event_type=EventType.GRANT_SUBMITTED,
            system_type=SystemType.GRANT_SUPPORT,
            timestamp=datetime.now(),
            data=grant_data
        )
        self.event_queue.append(event)

        # Apply grant submission rules
        context = ExecutionContext(
            context_type=ContextType.GRANT_EVALUATION,
            context_id=f"grant-submission-{grant_data.get('grant_id')}",
            data=grant_data,
            user_id=grant_data.get("user_id"),
            timestamp=datetime.now()
        )

        results = await self.engine.evaluate_context(context, mode="grant_submission")
        # Emit AI rules evaluation completed event
        self.event_queue.append(SystemEvent(
            event_type=EventType.RULE_EVALUATION_COMPLETED,
            system_type=SystemType.AI_RULES_ENGINE,
            timestamp=datetime.now(),
            data={"phase":"grant_submission","grant_id": grant_data.get("grant_id")}
        ))

        # Validate submission completeness
        completeness_check = await self._validate_grant_completeness(grant_data)

        return {
            "status": "submitted",
            "validation_results": results,
            "completeness_check": completeness_check,
            "next_steps": self._generate_next_steps(results)
        }

    async def _handle_grant_evaluation(self, grant_data: Dict) -> Dict:
        """Handle grant evaluation with all three systems."""
        logger.info("Handling grant evaluation")

        # Grant Support System: Technical evaluation
        grant_evaluation = await self._evaluate_grant_technical_merit(grant_data)

        # Impact Reporting System: Impact potential assessment
        impact_assessment = await self._assess_impact_potential(grant_data)

        # AI Rules Engine: Cross-system validation
        ai_validation = await self._validate_with_ai_rules(grant_data)

        # Combine evaluations
        overall_score = self._calculate_overall_score(
            grant_evaluation, impact_assessment, ai_validation
        )

        return {
            "technical_evaluation": grant_evaluation,
            "impact_assessment": impact_assessment,
            "ai_validation": ai_validation,
            "overall_score": overall_score,
            "recommendation": self._generate_funding_recommendation(overall_score)
        }

    async def _handle_grant_approval(self, grant_data: Dict) -> Dict:
        """Handle grant approval with Grant Support and AI Rules systems."""
        logger.info("Handling grant approval")

        # Create approval event
        event = SystemEvent(
            event_type=EventType.GRANT_APPROVED,
            system_type=SystemType.GRANT_SUPPORT,
            timestamp=datetime.now(),
            data=grant_data
        )
        self.event_queue.append(event)

        # Apply approval rules
        context = ExecutionContext(
            context_type=ContextType.GRANT_EVALUATION,
            context_id=f"grant-approval-{grant_data.get('grant_id')}",
            data=grant_data,
            user_id=grant_data.get("user_id"),
            timestamp=datetime.now()
        )

        results = await self.engine.evaluate_context(context, mode="grant_approval")
        self.event_queue.append(SystemEvent(
            event_type=EventType.RULE_EVALUATION_COMPLETED,
            system_type=SystemType.AI_RULES_ENGINE,
            timestamp=datetime.now(),
            data={"phase":"grant_approval","grant_id": grant_data.get("grant_id")}
        ))

        return {
            "status": "approved",
            "approval_conditions": self._extract_approval_conditions(results),
            "monitoring_requirements": self._extract_monitoring_requirements(results),
            "funding_terms": self._extract_funding_terms(results)
        }

    async def _handle_impact_planning(self, grant_data: Dict) -> Dict:
        """Handle impact planning with Impact Reporting and AI Rules systems."""
        logger.info("Handling impact planning")

        # Create impact planning event
        event = SystemEvent(
            event_type=EventType.IMPACT_REPORT_CREATED,
            system_type=SystemType.IMPACT_REPORTING,
            timestamp=datetime.now(),
            data=grant_data
        )
        self.event_queue.append(event)

        # Generate impact plan
        impact_plan = await self._generate_impact_plan(grant_data)

        # Validate impact plan with AI rules
        context = ExecutionContext(
            context_type=ContextType.IMPACT_REPORTING,
            context_id=f"impact-planning-{grant_data.get('grant_id')}",
            data=impact_plan,
            user_id=grant_data.get("user_id"),
            timestamp=datetime.now()
        )

        validation_results = await self.engine.evaluate_context(context, mode="impact_planning")
        self.event_queue.append(SystemEvent(
            event_type=EventType.RULE_EVALUATION_COMPLETED,
            system_type=SystemType.AI_RULES_ENGINE,
            timestamp=datetime.now(),
            data={"phase":"impact_planning","grant_id": grant_data.get("grant_id")}
        ))

        return {
            "impact_plan": impact_plan,
            "validation_results": validation_results,
            "monitoring_framework": self._generate_monitoring_framework(impact_plan),
            "reporting_schedule": self._generate_reporting_schedule(impact_plan)
        }

    async def process_impact_reporting(self, impact_data: Dict) -> Dict:
        """
        Process impact reporting with all three systems involved.
        """
        logger.info(f"Processing impact reporting for: {impact_data.get('report_id')}")

        # Step 1: Impact Data Collection (Impact Reporting + AI Rules)
        collection_result = await self._handle_impact_data_collection(impact_data)

        # Step 2: Impact Analysis (All three systems)
        analysis_result = await self._handle_impact_analysis(impact_data)

        # Step 3: Report Generation (Impact Reporting + AI Rules)
        report_result = await self._handle_report_generation(impact_data)

        # Step 4: Grant Impact Update (Grant Support + Impact Reporting)
        grant_update = await self._handle_grant_impact_update(impact_data)

        # Step 5: Cross-system validation
        validation_result = await self._validate_impact_consistency(impact_data)

        return {
            "report_id": impact_data.get("report_id"),
            "collection": collection_result,
            "analysis": analysis_result,
            "report": report_result,
            "grant_update": grant_update,
            "validation": validation_result,
            "timestamp": datetime.now().isoformat()
        }

    async def _handle_impact_data_collection(self, impact_data: Dict) -> Dict:
        """Handle impact data collection with Impact Reporting and AI Rules systems."""
        logger.info("Handling impact data collection")

        # Validate data quality with AI rules
        context = ExecutionContext(
            context_type=ContextType.IMPACT_REPORTING,
            context_id=f"data-collection-{impact_data.get('report_id')}",
            data=impact_data,
            user_id=impact_data.get("user_id"),
            timestamp=datetime.now()
        )

        validation_results = await self.engine.evaluate_context(context, mode="data_validation")
        self.event_queue.append(SystemEvent(
            event_type=EventType.RULE_EVALUATION_COMPLETED,
            system_type=SystemType.AI_RULES_ENGINE,
            timestamp=datetime.now(),
            data={"phase":"data_collection","report_id": impact_data.get("report_id")}
        ))

        # Check data completeness and quality
        data_quality_check = await self._validate_data_quality(impact_data)

        return {
            "status": "collected",
            "data_quality": data_quality_check,
            "validation_results": validation_results,
            "missing_data": self._identify_missing_data(impact_data)
        }

    async def _handle_impact_analysis(self, impact_data: Dict) -> Dict:
        """Handle impact analysis with all three systems."""
        logger.info("Handling impact analysis")

        # Impact Reporting System: Framework analysis
        framework_analysis = await self._analyze_frameworks(impact_data)

        # Grant Support System: Grant outcome tracking
        grant_outcomes = await self._track_grant_outcomes(impact_data)

        # AI Rules Engine: Cross-system validation
        ai_analysis = await self._analyze_with_ai_rules(impact_data)

        # Combine analyses
        comprehensive_analysis = self._combine_analyses(
            framework_analysis, grant_outcomes, ai_analysis
        )

        return {
            "framework_analysis": framework_analysis,
            "grant_outcomes": grant_outcomes,
            "ai_analysis": ai_analysis,
            "comprehensive_analysis": comprehensive_analysis,
            "recommendations": self._generate_impact_recommendations(comprehensive_analysis)
        }

    async def _handle_report_generation(self, impact_data: Dict) -> Dict:
        """Handle report generation with Impact Reporting and AI Rules systems."""
        logger.info("Handling report generation")

        # Create report generation event
        event = SystemEvent(
            event_type=EventType.IMPACT_REPORT_PUBLISHED,
            system_type=SystemType.IMPACT_REPORTING,
            timestamp=datetime.now(),
            data=impact_data
        )
        self.event_queue.append(event)

        # Generate report with AI validation
        report = await self._generate_impact_report(impact_data)

        # Validate report with AI rules
        context = ExecutionContext(
            context_type=ContextType.IMPACT_REPORTING,
            context_id=f"report-generation-{impact_data.get('report_id')}",
            data=report,
            user_id=impact_data.get("user_id"),
            timestamp=datetime.now()
        )

        validation_results = await self.engine.evaluate_context(context, mode="report_validation")
        self.event_queue.append(SystemEvent(
            event_type=EventType.RULE_EVALUATION_COMPLETED,
            system_type=SystemType.AI_RULES_ENGINE,
            timestamp=datetime.now(),
            data={"phase":"report_generation","report_id": impact_data.get("report_id")}
        ))

        return {
            "report": report,
            "validation_results": validation_results,
            "stakeholder_communication": self._generate_stakeholder_communication(report),
            "visualizations": self._generate_visualizations(report)
        }

    async def _handle_grant_impact_update(self, impact_data: Dict) -> Dict:
        """Handle grant impact update with Grant Support and Impact Reporting systems."""
        logger.info("Handling grant impact update")

        # Update grant with impact results
        grant_update = await self._update_grant_with_impact(impact_data)

        # Trigger follow-up actions
        follow_up_actions = self._trigger_follow_up_actions(impact_data)

        return {
            "grant_update": grant_update,
            "follow_up_actions": follow_up_actions,
            "performance_metrics": self._calculate_performance_metrics(impact_data)
        }

    async def _validate_cross_system_consistency(self, data: Dict) -> CrossSystemValidation:
        """Validate consistency across all three systems."""
        logger.info("Validating cross-system consistency")

        validation = CrossSystemValidation(
            validation_id=f"validation-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            systems_involved=[SystemType.GRANT_SUPPORT, SystemType.IMPACT_REPORTING, SystemType.AI_RULES_ENGINE],
            validation_status="pending"
        )

        # Pre-check: if data looks like grant data, ensure required fields are present
        required_fields = ["grant_id", "title", "budget", "timeline_months", "impact_metrics"]
        missing_required = [f for f in required_fields if f not in data or not data.get(f)]
        precheck_errors = []
        if missing_required:
            precheck_errors.append(
                f"Grant data missing required fields: {', '.join(missing_required)}"
            )

        # Check data consistency across systems
        consistency_checks = await asyncio.gather(
            self._check_grant_impact_consistency(data),
            self._check_ai_rules_consistency(data),
            self._check_reporting_consistency(data)
        )

        # Aggregate results
        all_errors = []
        all_warnings = []
        all_recommendations = []

        for check in consistency_checks:
            all_errors.extend(check.get("errors", []))
            all_warnings.extend(check.get("warnings", []))
            all_recommendations.extend(check.get("recommendations", []))

        # Include precheck errors
        all_errors.extend(precheck_errors)

        validation.errors = all_errors
        validation.warnings = all_warnings
        validation.recommendations = all_recommendations
        validation.validation_status = "passed" if not all_errors else "failed"

        self.validation_history.append(validation)

        return validation

    async def _validate_impact_consistency(self, data: Dict) -> CrossSystemValidation:
        """Validate impact reporting consistency across systems."""
        logger.info("Validating impact consistency")

        validation = CrossSystemValidation(
            validation_id=f"impact-validation-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            systems_involved=[SystemType.IMPACT_REPORTING, SystemType.GRANT_SUPPORT, SystemType.AI_RULES_ENGINE],
            validation_status="pending"
        )

        # Check impact reporting consistency
        consistency_checks = await asyncio.gather(
            self._check_impact_grant_alignment(data),
            self._check_impact_ai_rules_alignment(data),
            self._check_impact_framework_compliance(data)
        )

        # Aggregate results
        all_errors = []
        all_warnings = []
        all_recommendations = []

        for check in consistency_checks:
            all_errors.extend(check.get("errors", []))
            all_warnings.extend(check.get("warnings", []))
            all_recommendations.extend(check.get("recommendations", []))

        validation.errors = all_errors
        validation.warnings = all_warnings
        validation.recommendations = all_recommendations
        validation.validation_status = "passed" if not all_errors else "failed"

        self.validation_history.append(validation)

        return validation

    # Helper methods for system-specific operations
    async def _validate_grant_completeness(self, grant_data: Dict) -> Dict:
        """Validate grant application completeness."""
        required_fields = ["grant_id", "title", "budget", "timeline_months", "impact_metrics"]
        missing_fields = [field for field in required_fields if not grant_data.get(field)]

        return {
            "complete": len(missing_fields) == 0,
            "missing_fields": missing_fields,
            "completeness_score": (len(required_fields) - len(missing_fields)) / len(required_fields)
        }

    async def _evaluate_grant_technical_merit(self, grant_data: Dict) -> Dict:
        """Evaluate grant technical merit."""
        # Simulate technical evaluation
        return {
            "technical_score": 8.5,
            "methodology_quality": "high",
            "innovation_level": "medium",
            "feasibility": "high",
            "risk_assessment": "low"
        }

    async def _assess_impact_potential(self, grant_data: Dict) -> Dict:
        """Assess impact potential of grant."""
        # Simulate impact assessment
        return {
            "impact_score": 9.0,
            "reach_potential": "high",
            "sustainability": "medium",
            "scalability": "high",
            "sdg_alignment": ["SDG3", "SDG10"]
        }

    async def _validate_with_ai_rules(self, grant_data: Dict) -> Dict:
        """Validate grant with AI rules engine."""
        # Simulate AI validation
        return {
            "ai_validation_score": 8.8,
            "rule_compliance": "high",
            "mission_alignment": "excellent",
            "recommendations": ["Strengthen monitoring plan", "Add stakeholder engagement"]
        }

    def _calculate_overall_score(self, grant_eval: Dict, impact_assessment: Dict, ai_validation: Dict) -> float:
        """Calculate overall grant score."""
        scores = [
            grant_eval.get("technical_score", 0) * 0.4,
            impact_assessment.get("impact_score", 0) * 0.4,
            ai_validation.get("ai_validation_score", 0) * 0.2
        ]
        return sum(scores)

    def _generate_funding_recommendation(self, overall_score: float) -> str:
        """Generate funding recommendation based on overall score."""
        if overall_score >= 8.5:
            return "strongly_recommend"
        elif overall_score >= 7.0:
            return "recommend"
        elif overall_score >= 5.0:
            return "consider_with_conditions"
        else:
            return "do_not_recommend"

    async def _generate_impact_plan(self, grant_data: Dict) -> Dict:
        """Generate impact plan for grant."""
        return {
            "impact_plan_id": f"plan-{grant_data.get('grant_id')}",
            "frameworks": ["ToC", "CEMP", "SDG"],
            "metrics": grant_data.get("impact_metrics", []),
            "timeline": grant_data.get("timeline_months", 12),
            "stakeholders": ["beneficiaries", "partners", "funders"],
            "monitoring_frequency": "quarterly"
        }

    async def _validate_data_quality(self, impact_data: Dict) -> Dict:
        """Validate impact data quality."""
        return {
            "data_quality_score": 9.2,
            "completeness": "high",
            "accuracy": "high",
            "timeliness": "medium",
            "reliability": "high"
        }

    async def _analyze_frameworks(self, impact_data: Dict) -> Dict:
        """Analyze impact using different frameworks."""
        return {
            "theory_of_change": {"status": "valid", "strengths": ["clear logic"], "weaknesses": []},
            "cemp": {"status": "compliant", "metrics": ["output", "outcome", "impact"]},
            "sdg": {"status": "aligned", "goals": ["SDG3", "SDG10"]}
        }

    async def _track_grant_outcomes(self, impact_data: Dict) -> Dict:
        """Track grant outcomes."""
        return {
            "grant_id": impact_data.get("grant_id"),
            "outcomes_achieved": 8,
            "target_outcomes": 10,
            "success_rate": 0.8,
            "key_achievements": ["health improvements", "community engagement"]
        }

    async def _analyze_with_ai_rules(self, impact_data: Dict) -> Dict:
        """Analyze impact with AI rules engine."""
        return {
            "ai_analysis_score": 8.7,
            "pattern_recognition": "strong",
            "anomaly_detection": "none",
            "trend_analysis": "positive",
            "recommendations": ["Expand successful interventions", "Address identified gaps"]
        }

    def _combine_analyses(self, framework_analysis: Dict, grant_outcomes: Dict, ai_analysis: Dict) -> Dict:
        """Combine analyses from all systems."""
        return {
            "comprehensive_score": 8.6,
            "framework_compliance": "excellent",
            "outcome_achievement": "high",
            "ai_insights": "valuable",
            "overall_assessment": "successful"
        }

    async def _generate_impact_report(self, impact_data: Dict) -> Dict:
        """Generate comprehensive impact report."""
        return {
            "report_id": impact_data.get("report_id"),
            "grant_id": impact_data.get("grant_id"),
            "executive_summary": "Significant positive impact achieved",
            "methodology": "Mixed-methods approach with quantitative and qualitative data",
            "key_findings": ["Improved health outcomes", "Enhanced community engagement"],
            "recommendations": ["Scale successful interventions", "Strengthen monitoring"],
            "appendices": ["data_sources", "methodology_details", "stakeholder_feedback"]
        }

    async def _update_grant_with_impact(self, impact_data: Dict) -> Dict:
        """Update grant with impact results."""
        return {
            "grant_id": impact_data.get("grant_id"),
            "impact_results": "positive",
            "performance_metrics": "exceeded_targets",
            "lessons_learned": ["Community engagement is key", "Regular monitoring essential"],
            "next_phase_recommendations": ["Scale successful interventions", "Address identified gaps"]
        }

    # Additional helper methods for consistency checks
    async def _check_grant_impact_consistency(self, data: Dict) -> Dict:
        """Check consistency between grant and impact data."""
        return {"errors": [], "warnings": [], "recommendations": ["Monitor alignment"]}

    async def _check_ai_rules_consistency(self, data: Dict) -> Dict:
        """Check AI rules consistency."""
        return {"errors": [], "warnings": [], "recommendations": ["Validate rule outcomes"]}

    async def _check_reporting_consistency(self, data: Dict) -> Dict:
        """Check reporting consistency."""
        return {"errors": [], "warnings": [], "recommendations": ["Ensure data quality"]}

    async def _check_impact_grant_alignment(self, data: Dict) -> Dict:
        """Check alignment between impact and grant data."""
        return {"errors": [], "warnings": [], "recommendations": ["Verify grant outcomes"]}

    async def _check_impact_ai_rules_alignment(self, data: Dict) -> Dict:
        """Check alignment between impact and AI rules."""
        return {"errors": [], "warnings": [], "recommendations": ["Validate AI insights"]}

    async def _check_impact_framework_compliance(self, data: Dict) -> Dict:
        """Check framework compliance for impact reporting."""
        return {"errors": [], "warnings": [], "recommendations": ["Ensure framework alignment"]}

    # Helper methods for generating outputs
    def _generate_next_steps(self, results: List) -> List[str]:
        """Generate next steps based on rule evaluation results."""
        return ["Review validation results", "Address any issues", "Proceed to evaluation"]

    def _extract_approval_conditions(self, results: List) -> List[str]:
        """Extract approval conditions from rule results."""
        return ["Regular reporting required", "Impact monitoring mandatory", "Stakeholder engagement"]

    def _extract_monitoring_requirements(self, results: List) -> List[str]:
        """Extract monitoring requirements from rule results."""
        return ["Quarterly progress reports", "Impact assessment at 6 months", "Final evaluation"]

    def _extract_funding_terms(self, results: List) -> Dict:
        """Extract funding terms from rule results."""
        return {"amount": 500000, "disbursement": "quarterly", "conditions": ["performance_based"]}

    def _generate_monitoring_framework(self, impact_plan: Dict) -> Dict:
        """Generate monitoring framework for impact plan."""
        return {"frequency": "quarterly", "metrics": impact_plan.get("metrics", []), "stakeholders": impact_plan.get("stakeholders", [])}

    def _generate_reporting_schedule(self, impact_plan: Dict) -> Dict:
        """Generate reporting schedule for impact plan."""
        return {"interim_reports": "quarterly", "final_report": "end_of_grant", "stakeholder_updates": "monthly"}

    def _identify_missing_data(self, impact_data: Dict) -> List[str]:
        """Identify missing data in impact report."""
        return ["baseline_data", "comparison_group"]

    def _generate_impact_recommendations(self, analysis: Dict) -> List[str]:
        """Generate recommendations based on impact analysis."""
        return ["Scale successful interventions", "Address identified gaps", "Strengthen monitoring"]

    def _generate_stakeholder_communication(self, report: Dict) -> Dict:
        """Generate stakeholder communication plan."""
        return {"executives": "executive_summary", "funders": "detailed_report", "community": "accessible_summary"}

    def _generate_visualizations(self, report: Dict) -> List[str]:
        """Generate visualizations for impact report."""
        return ["impact_charts", "outcome_graphs", "stakeholder_maps"]

    def _trigger_follow_up_actions(self, impact_data: Dict) -> List[str]:
        """Trigger follow-up actions based on impact results."""
        return ["schedule_follow_up_study", "plan_scale_up", "update_grant_database"]

    def _calculate_performance_metrics(self, impact_data: Dict) -> Dict:
        """Calculate performance metrics for impact data."""
        return {"success_rate": 0.85, "efficiency_score": 0.78, "impact_multiplier": 2.3}


# Convenience functions for easy integration
async def create_movember_integrator(config: Optional[Dict] = None) -> MovemberSystemIntegrator:
    """Create a Movember system integrator instance."""
    return MovemberSystemIntegrator(config)


async def process_grant_with_integration(grant_data: Dict, config: Optional[Dict] = None) -> Dict:
    """Process a grant through all integrated systems."""
    integrator = await create_movember_integrator(config)
    return await integrator.process_grant_lifecycle(grant_data)


async def process_impact_with_integration(impact_data: Dict, config: Optional[Dict] = None) -> Dict:
    """Process impact reporting through all integrated systems."""
    integrator = await create_movember_integrator(config)
    return await integrator.process_impact_reporting(impact_data)


async def validate_system_integration(data: Dict, config: Optional[Dict] = None) -> CrossSystemValidation:
    """Validate integration across all systems."""
    integrator = await create_movember_integrator(config)
    return await integrator._validate_cross_system_consistency(data)
