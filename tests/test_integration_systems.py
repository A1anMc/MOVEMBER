#!/usr/bin/env python3
"""
Integration Tests for Three-System Interaction
Tests that Grant Support, Impact Reporting, and AI Rules Engine work together seamlessly.
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
    process_grant_with_integration,
    process_impact_with_integration,
    validate_system_integration
)
from rules.domains.movember_ai.integration import (
    MovemberSystemIntegrator,
    create_movember_integrator,
    SystemType,
    EventType
)
from rules.types import ExecutionContext, ContextType


class TestThreeSystemIntegration:
    """Test integration between Grant Support, Impact Reporting, and AI Rules Engine."""
    
    @pytest.fixture
    async def integrator(self):
        """Create a system integrator for testing."""
        return await create_movember_integrator()
    
    @pytest.fixture
    def sample_grant_data(self):
        """Sample grant data for testing."""
        return {
            "grant_id": "GRANT-INTEGRATION-001",
            "title": "Men's Health Research Initiative",
            "status": "submitted",
            "budget": 750000,
            "timeline_months": 24,
            "impact_metrics": [
                {"name": "Health Screenings", "target": 5000},
                {"name": "Research Publications", "target": 15},
                {"name": "Community Engagement", "target": 1000}
            ],
            "sdg_alignment": ["SDG3", "SDG10"],
            "sustainability_plan": "detailed",
            "risk_mitigation": "comprehensive",
            "partnerships": ["universities", "hospitals", "community_organizations"],
            "innovation_score": 8.5,
            "application_fields": {"missing": []},
            "user_id": "test-user",
            "project_id": "movember"
        }
    
    @pytest.fixture
    def sample_impact_data(self):
        """Sample impact data for testing."""
        return {
            "report_id": "IMPACT-INTEGRATION-001",
            "grant_id": "GRANT-INTEGRATION-001",
            "type": "impact",
            "title": "Men's Health Research Initiative Impact Report",
            "frameworks": ["ToC", "CEMP", "SDG"],
            "outputs": [
                {"name": "Health Screenings", "count": 5200},
                {"name": "Research Publications", "count": 18},
                {"name": "Community Engagement", "count": 1200}
            ],
            "outcomes": [
                {"name": "Improved Health Awareness", "metric": "85% improvement"},
                {"name": "Behavioral Change", "metric": "70% adoption rate"},
                {"name": "Research Impact", "metric": "12 citations"}
            ],
            "stakeholders": ["executive", "funder", "researcher"],
            "data_sources": ["health_surveys", "medical_records", "research_database"],
            "visualizations": ["charts", "graphs", "maps"],
            "attribution": "clear",
            "data_gaps": [],
            "user_id": "test-user",
            "project_id": "movember"
        }
    
    @pytest.mark.asyncio
    async def test_grant_lifecycle_with_all_systems(self, integrator, sample_grant_data):
        """Test complete grant lifecycle with all three systems integrated."""
        logger.info("Testing grant lifecycle with all systems")
        
        # Process grant through all systems
        result = await integrator.process_grant_lifecycle(sample_grant_data)
        
        # Verify all systems were involved
        assert "submission" in result
        assert "evaluation" in result
        assert "approval" in result
        assert "impact_plan" in result
        assert "validation" in result
        
        # Check submission results
        submission = result["submission"]
        assert submission["status"] == "submitted"
        assert "validation_results" in submission
        assert "completeness_check" in submission
        
        # Check evaluation results
        evaluation = result["evaluation"]
        assert "technical_evaluation" in evaluation
        assert "impact_assessment" in evaluation
        assert "ai_validation" in evaluation
        assert "overall_score" in evaluation
        assert "recommendation" in evaluation
        
        # Check approval results
        approval = result["approval"]
        assert approval["status"] == "approved"
        assert "approval_conditions" in approval
        assert "monitoring_requirements" in approval
        assert "funding_terms" in approval
        
        # Check impact plan
        impact_plan = result["impact_plan"]
        assert "impact_plan" in impact_plan
        assert "validation_results" in impact_plan
        assert "monitoring_framework" in impact_plan
        assert "reporting_schedule" in impact_plan
        
        # Check cross-system validation
        validation = result["validation"]
        assert validation.validation_status in ["passed", "failed"]
        assert hasattr(validation, "systems_involved")
        assert len(validation.systems_involved) == 3  # All three systems
        
        logger.info(f"Grant lifecycle completed successfully with {len(result)} phases")
    
    @pytest.mark.asyncio
    async def test_impact_reporting_with_all_systems(self, integrator, sample_impact_data):
        """Test impact reporting with all three systems integrated."""
        logger.info("Testing impact reporting with all systems")
        
        # Process impact reporting through all systems
        result = await integrator.process_impact_reporting(sample_impact_data)
        
        # Verify all systems were involved
        assert "collection" in result
        assert "analysis" in result
        assert "report" in result
        assert "grant_update" in result
        assert "validation" in result
        
        # Check data collection results
        collection = result["collection"]
        assert collection["status"] == "collected"
        assert "data_quality" in collection
        assert "validation_results" in collection
        assert "missing_data" in collection
        
        # Check analysis results
        analysis = result["analysis"]
        assert "framework_analysis" in analysis
        assert "grant_outcomes" in analysis
        assert "ai_analysis" in analysis
        assert "comprehensive_analysis" in analysis
        assert "recommendations" in analysis
        
        # Check report generation
        report = result["report"]
        assert "report" in report
        assert "validation_results" in report
        assert "stakeholder_communication" in report
        assert "visualizations" in report
        
        # Check grant update
        grant_update = result["grant_update"]
        assert "grant_update" in grant_update
        assert "follow_up_actions" in grant_update
        assert "performance_metrics" in grant_update
        
        # Check cross-system validation
        validation = result["validation"]
        assert validation.validation_status in ["passed", "failed"]
        assert hasattr(validation, "systems_involved")
        assert len(validation.systems_involved) == 3  # All three systems
        
        logger.info(f"Impact reporting completed successfully with {len(result)} phases")
    
    @pytest.mark.asyncio
    async def test_cross_system_data_flow(self, integrator, sample_grant_data, sample_impact_data):
        """Test data flow between all three systems."""
        logger.info("Testing cross-system data flow")
        
        # Step 1: Process grant
        grant_result = await integrator.process_grant_lifecycle(sample_grant_data)
        
        # Step 2: Process impact reporting
        impact_result = await integrator.process_impact_reporting(sample_impact_data)
        
        # Step 3: Verify data consistency across systems
        consistency_check = await integrator._validate_cross_system_consistency({
            "grant_data": sample_grant_data,
            "impact_data": sample_impact_data
        })
        
        # Verify data flow
        assert grant_result["grant_id"] == sample_grant_data["grant_id"]
        assert impact_result["report_id"] == sample_impact_data["report_id"]
        assert impact_result["report"]["report"]["grant_id"] == sample_grant_data["grant_id"]
        
        # Check that grant outcomes are reflected in impact report
        grant_outcomes = impact_result["analysis"]["grant_outcomes"]
        assert grant_outcomes["grant_id"] == sample_grant_data["grant_id"]
        assert "outcomes_achieved" in grant_outcomes
        assert "success_rate" in grant_outcomes
        
        # Check cross-system validation
        assert consistency_check.validation_status in ["passed", "failed"]
        assert len(consistency_check.systems_involved) == 3
        
        logger.info("Cross-system data flow verified successfully")
    
    @pytest.mark.asyncio
    async def test_event_triggering_between_systems(self, integrator, sample_grant_data):
        """Test that events in one system trigger actions in other systems."""
        logger.info("Testing event triggering between systems")
        
        # Process grant to trigger events
        result = await integrator.process_grant_lifecycle(sample_grant_data)
        
        # Check that events were created
        assert len(integrator.event_queue) > 0
        
        # Verify event types
        event_types = [event.event_type for event in integrator.event_queue]
        assert EventType.GRANT_SUBMITTED in event_types
        assert EventType.GRANT_APPROVED in event_types
        assert EventType.IMPACT_REPORT_CREATED in event_types
        
        # Verify system involvement
        system_types = [event.system_type for event in integrator.event_queue]
        assert SystemType.GRANT_SUPPORT in system_types
        assert SystemType.IMPACT_REPORTING in system_types
        assert SystemType.AI_RULES_ENGINE in system_types
        
        # Check event data consistency
        for event in integrator.event_queue:
            assert event.timestamp is not None
            assert event.data is not None
            assert "grant_id" in event.data or "report_id" in event.data
        
        logger.info(f"Event triggering verified: {len(integrator.event_queue)} events created")
    
    @pytest.mark.asyncio
    async def test_system_validation_coordination(self, integrator, sample_grant_data):
        """Test that validation is coordinated across all systems."""
        logger.info("Testing system validation coordination")
        
        # Process grant to trigger validations
        result = await integrator.process_grant_lifecycle(sample_grant_data)
        
        # Check validation history
        assert len(integrator.validation_history) > 0
        
        # Verify validation structure
        for validation in integrator.validation_history:
            assert hasattr(validation, "validation_id")
            assert hasattr(validation, "systems_involved")
            assert hasattr(validation, "validation_status")
            assert hasattr(validation, "errors")
            assert hasattr(validation, "warnings")
            assert hasattr(validation, "recommendations")
            assert hasattr(validation, "timestamp")
            
            # Check that all three systems are involved
            assert len(validation.systems_involved) == 3
            assert SystemType.GRANT_SUPPORT in validation.systems_involved
            assert SystemType.IMPACT_REPORTING in validation.systems_involved
            assert SystemType.AI_RULES_ENGINE in validation.systems_involved
        
        logger.info(f"System validation coordination verified: {len(integrator.validation_history)} validations")
    
    @pytest.mark.asyncio
    async def test_error_handling_across_systems(self, integrator):
        """Test error handling when one system fails."""
        logger.info("Testing error handling across systems")
        
        # Create invalid data that should cause errors
        invalid_grant_data = {
            "grant_id": "INVALID-GRANT",
            "status": "submitted",
            # Missing required fields
        }
        
        try:
            result = await integrator.process_grant_lifecycle(invalid_grant_data)
            
            # Even with errors, should get structured response
            assert "submission" in result
            assert "validation" in result
            
            # Check that validation caught errors
            validation = result["validation"]
            assert validation.validation_status == "failed"
            assert len(validation.errors) > 0
            
        except Exception as e:
            # Should handle errors gracefully
            assert "error" in str(e).lower() or "validation" in str(e).lower()
        
        logger.info("Error handling across systems verified")
    
    @pytest.mark.asyncio
    async def test_performance_with_all_systems(self, integrator, sample_grant_data, sample_impact_data):
        """Test performance when all three systems are involved."""
        logger.info("Testing performance with all systems")
        
        # Measure grant processing time
        start_time = time.time()
        grant_result = await integrator.process_grant_lifecycle(sample_grant_data)
        grant_time = time.time() - start_time
        
        # Measure impact processing time
        start_time = time.time()
        impact_result = await integrator.process_impact_reporting(sample_impact_data)
        impact_time = time.time() - start_time
        
        # Performance assertions
        assert grant_time < 10.0  # Should complete within 10 seconds
        assert impact_time < 10.0  # Should complete within 10 seconds
        
        # Check that all systems are active
        for system_type, status in integrator.system_status.items():
            assert status == "active"
        
        logger.info(f"Performance verified: Grant processing {grant_time:.2f}s, Impact processing {impact_time:.2f}s")
    
    @pytest.mark.asyncio
    async def test_concurrent_system_operations(self, integrator, sample_grant_data, sample_impact_data):
        """Test concurrent operations across all systems."""
        logger.info("Testing concurrent system operations")
        
        # Run grant and impact processing concurrently
        start_time = time.time()
        results = await asyncio.gather(
            integrator.process_grant_lifecycle(sample_grant_data),
            integrator.process_impact_reporting(sample_impact_data)
        )
        total_time = time.time() - start_time
        
        # Verify both operations completed
        grant_result, impact_result = results
        assert "submission" in grant_result
        assert "collection" in impact_result
        
        # Performance check for concurrent operations
        assert total_time < 15.0  # Should be faster than sequential
        
        logger.info(f"Concurrent operations verified: {total_time:.2f}s for both operations")
    
    @pytest.mark.asyncio
    async def test_system_integration_metrics(self, integrator, sample_grant_data):
        """Test that integration provides proper metrics and monitoring."""
        logger.info("Testing system integration metrics")
        
        # Process grant to generate metrics
        result = await integrator.process_grant_lifecycle(sample_grant_data)
        
        # Check system status
        for system_type, status in integrator.system_status.items():
            assert status == "active"
        
        # Check event queue metrics
        assert len(integrator.event_queue) > 0
        
        # Check validation history
        assert len(integrator.validation_history) > 0
        
        # Verify event types and system involvement
        event_system_counts = {}
        for event in integrator.event_queue:
            system_type = event.system_type.value
            event_system_counts[system_type] = event_system_counts.get(system_type, 0) + 1
        
        # Should have events from all systems
        assert len(event_system_counts) >= 2  # At least 2 systems involved
        
        logger.info(f"Integration metrics verified: {len(integrator.event_queue)} events, {len(integrator.validation_history)} validations")


class TestSystemIntegrationAPI:
    """Test the high-level integration API functions."""
    
    @pytest.mark.asyncio
    async def test_process_grant_with_integration_api(self, sample_grant_data):
        """Test the high-level grant processing API."""
        logger.info("Testing grant processing API")
        
        result = await process_grant_with_integration(sample_grant_data)
        
        # Verify API response structure
        assert "grant_id" in result
        assert "submission" in result
        assert "evaluation" in result
        assert "approval" in result
        assert "impact_plan" in result
        assert "validation" in result
        assert "timestamp" in result
        
        logger.info("Grant processing API verified")
    
    @pytest.mark.asyncio
    async def test_process_impact_with_integration_api(self, sample_impact_data):
        """Test the high-level impact processing API."""
        logger.info("Testing impact processing API")
        
        result = await process_impact_with_integration(sample_impact_data)
        
        # Verify API response structure
        assert "report_id" in result
        assert "collection" in result
        assert "analysis" in result
        assert "report" in result
        assert "grant_update" in result
        assert "validation" in result
        assert "timestamp" in result
        
        logger.info("Impact processing API verified")
    
    @pytest.mark.asyncio
    async def test_validate_system_integration_api(self, sample_grant_data, sample_impact_data):
        """Test the system integration validation API."""
        logger.info("Testing system integration validation API")
        
        combined_data = {
            "grant_data": sample_grant_data,
            "impact_data": sample_impact_data
        }
        
        result = await validate_system_integration(combined_data)
        
        # Verify validation result structure
        assert hasattr(result, "validation_id")
        assert hasattr(result, "systems_involved")
        assert hasattr(result, "validation_status")
        assert hasattr(result, "errors")
        assert hasattr(result, "warnings")
        assert hasattr(result, "recommendations")
        assert hasattr(result, "timestamp")
        
        # Check that all three systems are involved
        assert len(result.systems_involved) == 3
        
        logger.info("System integration validation API verified")


if __name__ == "__main__":
    # Run integration tests
    pytest.main([__file__, "-v"]) 