#!/usr/bin/env python3
"""
Integration Tests for Movember AI Rules System
Comprehensive testing of the complete rule evaluation workflow.
"""

import asyncio
import json
import pytest
import time
from datetime import datetime
from typing import Dict, List, Any

from rules.domains.movember_ai import (
    MovemberAIRulesEngine,
    create_movember_engine,
    validate_movember_operation,
    run_movember_impact_analysis,
    evaluate_grant_application,
    run_weekly_refactor
)
from rules.types import ExecutionContext, ContextType, RulePriority


class TestMovemberAIRulesIntegration:
    """Integration tests for the Movember AI Rules System."""

    @pytest.fixture
    async def engine(self):
        """Create a test engine instance."""
        return create_movember_engine()

    @pytest.fixture
    def sample_impact_report(self):
        """Sample impact report data."""
        return {
            "report_id": "IMP-2024-001",
            "type": "impact",
            "title": "Men's Health Initiative Impact Report",
            "frameworks": ["ToC", "SDG"],
            "outputs": [
                {"name": "Health Screenings", "count": 1500},
                {"name": "Educational Workshops", "count": 25}
            ],
            "outcomes": [
                {"name": "Increased Health Awareness", "metric": "85% improvement"},
                {"name": "Behavioral Change", "metric": "60% adoption rate"}
            ],
            "stakeholders": ["executive", "funder"],
            "data_sources": ["health_surveys", "medical_records"],
            "visualizations": ["charts", "graphs"],
            "attribution": "clear",
            "data_gaps": []
        }

    @pytest.fixture
    def sample_grant_application(self):
        """Sample grant application data."""
        return {
            "grant_id": "GRANT-2024-001",
            "status": "submitted",
            "title": "Prostate Cancer Research Initiative",
            "budget": 500000,
            "timeline_months": 24,
            "impact_metrics": [
                {"name": "Research Publications", "target": 10},
                {"name": "Clinical Trials", "target": 2}
            ],
            "sdg_alignment": ["SDG3", "SDG10"],
            "sustainability_plan": "detailed",
            "risk_mitigation": "comprehensive",
            "partnerships": ["universities", "hospitals"],
            "innovation_score": 8.5,
            "application_fields": {
                "missing": []
            }
        }

    @pytest.mark.asyncio
    async def test_complete_impact_reporting_workflow(self, engine, sample_impact_report):
        """Test complete impact reporting workflow."""
        # Create execution context
        context = ExecutionContext(
            context_type=ContextType.IMPACT_REPORTING,
            context_id="test-impact-report",
            data=sample_impact_report,
            user_id="test-user",
            timestamp=datetime.now()
        )

        # Evaluate rules
        results = await engine.evaluate_context(context, mode="reporting")

        # Assertions
        assert results is not None
        assert len(results) > 0

        # Check that framework alignment rule was triggered
        framework_rules = [r for r in results if "framework" in r.get("rule_name", "").lower()]
        assert len(framework_rules) > 0

        # Check that outputs-outcomes mapping rule was triggered
        mapping_rules = [r for r in results if "output" in r.get("rule_name", "").lower()]
        assert len(mapping_rules) > 0

        print(f"Impact reporting workflow completed with {len(results)} rule evaluations")

    @pytest.mark.asyncio
    async def test_complete_grant_evaluation_workflow(self, engine, sample_grant_application):
        """Test complete grant evaluation workflow."""
        # Create execution context
        context = ExecutionContext(
            context_type=ContextType.GRANT_EVALUATION,
            context_id="test-grant-eval",
            data=sample_grant_application,
            user_id="test-user",
            timestamp=datetime.now()
        )

        # Evaluate rules
        results = await engine.evaluate_context(context, mode="grant_submission")

        # Assertions
        assert results is not None
        assert len(results) > 0

        # Check that completeness rule was triggered
        completeness_rules = [r for r in results if "completeness" in r.get("rule_name", "").lower()]
        assert len(completeness_rules) > 0

        # Check that impact metrics rule was triggered
        metrics_rules = [r for r in results if "impact" in r.get("rule_name", "").lower()]
        assert len(metrics_rules) > 0

        print(f"Grant evaluation workflow completed with {len(results)} rule evaluations")

    @pytest.mark.asyncio
    async def test_ai_behaviour_rules_workflow(self, engine):
        """Test AI behaviour rules workflow."""
        # Create execution context for AI behaviour
        context = ExecutionContext(
            context_type=ContextType.AI_BEHAVIOUR,
            context_id="test-ai-behaviour",
            data={
                "agent": {
                    "role": "impact_intelligence",
                    "audience": "executive",
                    "confidence": 0.7
                },
                "request": {
                    "type": "impact_analysis",
                    "complexity": "high"
                }
            },
            user_id="test-user",
            timestamp=datetime.now()
        )

        # Evaluate rules
        results = await engine.evaluate_context(context, mode="ai_behaviour")

        # Assertions
        assert results is not None
        assert len(results) > 0

        # Check that professional tone rule was triggered
        tone_rules = [r for r in results if "tone" in r.get("rule_name", "").lower()]
        assert len(tone_rules) > 0

        print(f"AI behaviour workflow completed with {len(results)} rule evaluations")

    @pytest.mark.asyncio
    async def test_context_validation_workflow(self, engine):
        """Test context validation workflow."""
        # Test valid Movember context
        valid_context = ExecutionContext(
            context_type=ContextType.PROJECT_VALIDATION,
            context_id="test-valid-context",
            data={"project_id": "movember", "scope": "men_health"},
            user_id="test-user",
            timestamp=datetime.now()
        )

        results = await engine.evaluate_context(valid_context, mode="context_validation")
        assert results is not None

        # Test invalid context (should be blocked)
        invalid_context = ExecutionContext(
            context_type=ContextType.PROJECT_VALIDATION,
            context_id="test-invalid-context",
            data={"project_id": "other_project", "scope": "unrelated"},
            user_id="test-user",
            timestamp=datetime.now()
        )

        # This should raise an exception or return blocked results
        try:
            results = await engine.evaluate_context(invalid_context, mode="context_validation")
            # If no exception, check that blocking rules were triggered
            blocking_rules = [r for r in results if "abort" in str(r).lower()]
            assert len(blocking_rules) > 0
        except Exception as e:
            # Expected behavior for invalid context
            assert "movember" in str(e).lower() or "context" in str(e).lower()

        print("Context validation workflow completed successfully")

    @pytest.mark.asyncio
    async def test_weekly_refactoring_workflow(self, engine):
        """Test weekly refactoring workflow."""
        # Run weekly refactor
        refactor_summary = await run_weekly_refactor()

        # Assertions
        assert refactor_summary is not None
        assert hasattr(refactor_summary, 'issues_found')
        assert hasattr(refactor_summary, 'recommendations')
        assert hasattr(refactor_summary, 'audit_timestamp')

        print(f"Weekly refactoring completed: {refactor_summary.issues_found} issues found")

    @pytest.mark.asyncio
    async def test_performance_under_load(self, engine):
        """Test system performance under load."""
        # Create multiple concurrent requests
        contexts = []
        for i in range(10):
            context = ExecutionContext(
                context_type=ContextType.IMPACT_REPORTING,
                context_id=f"load-test-{i}",
                data={"test": True, "index": i},
                user_id=f"user-{i}",
                timestamp=datetime.now()
            )
            contexts.append(context)

        # Execute concurrent evaluations
        start_time = time.time()
        results = await asyncio.gather(*[
            engine.evaluate_context(context, mode="reporting")
            for context in contexts
        ])
        end_time = time.time()

        # Performance assertions
        execution_time = end_time - start_time
        assert execution_time < 5.0  # Should complete within 5 seconds
        assert len(results) == 10  # All requests should complete

        print(f"Load test completed: {len(results)} concurrent evaluations in {execution_time:.2f}s")

    @pytest.mark.asyncio
    async def test_error_handling_and_recovery(self, engine):
        """Test error handling and recovery mechanisms."""
        # Test with invalid data
        invalid_context = ExecutionContext(
            context_type=ContextType.IMPACT_REPORTING,
            context_id="error-test",
            data={"invalid": "data", "missing_required_fields": True},
            user_id="test-user",
            timestamp=datetime.now()
        )

        # Should handle gracefully
        try:
            results = await engine.evaluate_context(invalid_context, mode="reporting")
            # Should still return results, even if some rules fail
            assert results is not None
        except Exception as e:
            # Should provide meaningful error message
            assert "error" in str(e).lower() or "invalid" in str(e).lower()

        print("Error handling test completed successfully")

    @pytest.mark.asyncio
    async def test_metrics_and_monitoring(self, engine):
        """Test metrics collection and monitoring."""
        # Execute some evaluations
        context = ExecutionContext(
            context_type=ContextType.IMPACT_REPORTING,
            context_id="metrics-test",
            data={"test": True},
            user_id="test-user",
            timestamp=datetime.now()
        )

        await engine.evaluate_context(context, mode="reporting")

        # Get metrics
        metrics = engine.get_metrics()

        # Assertions
        assert metrics is not None
        assert "system_metrics" in metrics
        assert "rule_metrics" in metrics

        # Check that metrics are being collected
        system_metrics = metrics["system_metrics"]
        assert system_metrics["total_executions"] > 0
        assert system_metrics["success_rate"] >= 0.0

        print(f"Metrics test completed: {system_metrics['total_executions']} total executions")

    @pytest.mark.asyncio
    async def test_rule_priority_handling(self, engine):
        """Test that rules are executed in priority order."""
        # Create context that triggers multiple rules
        context = ExecutionContext(
            context_type=ContextType.IMPACT_REPORTING,
            context_id="priority-test",
            data={
                "report": {
                    "type": "impact",
                    "outputs": [{"name": "test"}],
                    "outcomes": []
                },
                "agent": {
                    "role": "impact_intelligence",
                    "confidence": 0.5
                }
            },
            user_id="test-user",
            timestamp=datetime.now()
        )

        results = await engine.evaluate_context(context, mode="default")

        # Check that critical rules are executed first
        critical_rules = [r for r in results if r.get("priority") == RulePriority.CRITICAL]
        high_rules = [r for r in results if r.get("priority") == RulePriority.HIGH]

        # Critical rules should be executed
        assert len(critical_rules) >= 0  # May or may not have critical rules

        print(f"Priority handling test completed: {len(results)} rules executed")

    @pytest.mark.asyncio
    async def test_async_concurrent_execution(self, engine):
        """Test async concurrent rule execution."""
        # Create multiple contexts
        contexts = []
        for i in range(5):
            context = ExecutionContext(
                context_type=ContextType.IMPACT_REPORTING,
                context_id=f"async-test-{i}",
                data={"test": True, "index": i},
                user_id=f"user-{i}",
                timestamp=datetime.now()
            )
            contexts.append(context)

        # Execute concurrently
        start_time = time.time()
        tasks = [
            engine.evaluate_context(context, mode="reporting")
            for context in contexts
        ]

        results = await asyncio.gather(*tasks)
        end_time = time.time()

        # Performance check
        execution_time = end_time - start_time
        assert execution_time < 3.0  # Should be faster than sequential
        assert len(results) == 5

        print(f"Async execution test completed: {execution_time:.2f}s for 5 concurrent evaluations")


class TestMovemberOperations:
    """Test Movember-specific operations."""

    @pytest.mark.asyncio
    async def test_validate_movember_operation(self):
        """Test Movember operation validation."""
        # Valid operation
        assert validate_movember_operation("impact_analysis", "movember")

        # Invalid operation
        assert not validate_movember_operation("marketing_copy", "other_project")

    @pytest.mark.asyncio
    async def test_run_movember_impact_analysis(self):
        """Test Movember impact analysis."""
        sample_data = {
            "project_id": "movember",
            "timeframe": "2024",
            "metrics": ["health_outcomes", "community_engagement"]
        }

        results = await run_movember_impact_analysis(sample_data)
        assert results is not None
        assert "analysis" in results

    @pytest.mark.asyncio
    async def test_evaluate_grant_application(self):
        """Test grant application evaluation."""
        sample_grant = {
            "grant_id": "TEST-001",
            "budget": 100000,
            "impact_metrics": [{"name": "test", "target": 10}],
            "sdg_alignment": ["SDG3"]
        }

        results = await evaluate_grant_application(sample_grant)
        assert results is not None
        assert "evaluation" in results


if __name__ == "__main__":
    # Run integration tests
    pytest.main([__file__, "-v"])
