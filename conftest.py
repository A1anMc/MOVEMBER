import logging
import pytest
import builtins
import pytest_asyncio

from rules.domains.movember_ai import create_movember_engine
from rules.domains.movember_ai.integration import create_movember_integrator

logger = logging.getLogger(__name__)

# Ensure a global `logger` name is available for tests that reference it directly
builtins.logger = logger

@pytest.fixture
def sample_grant_data():
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
def sample_impact_data():
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

@pytest_asyncio.fixture
async def engine():
    return create_movember_engine()

@pytest_asyncio.fixture
async def integrator():
    return await create_movember_integrator() 