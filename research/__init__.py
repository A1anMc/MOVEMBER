"""
Research & Innovation Hub - Phase 6

This package contains the research collaboration and innovation components
for the Movember AI Rules System, enabling multi-institution research,
automated publication generation, and evidence-based insights.
"""

from .clinical_data_integration import (
    ResearchCategory,
    ResearchPaper,
    ClinicalTrial,
    ResearchInsight,
    search_research_papers,
    search_clinical_trials_research,
    generate_research_insights_for_category,
    get_clinical_integration_status
)

from .research_collaboration import (
    CollaborationType,
    InstitutionType,
    ResearchInstitution,
    ResearchProject,
    CollaborationSession,
    register_research_institution,
    create_research_project,
    get_collaboration_network_analysis,
    get_institution_performance_metrics,
    get_platform_statistics
)

from .publication_pipeline import (
    PublicationType,
    PublicationStatus,
    ResearchPublication,
    PublicationTemplate,
    create_publication_template,
    generate_research_publication,
    get_publication_statistics,
    search_publications
)

__version__ = "1.0.0"
__author__ = "Movember AI Research Team"

# Research Hub capabilities
RESEARCH_CAPABILITIES = {
    "clinical_data_integration": "Connect to medical research databases and scientific literature",
    "research_collaboration": "Multi-institution research coordination and project management",
    "publication_pipeline": "Automated research paper generation and publication management",
    "evidence_based_insights": "Generate insights from scientific literature and clinical data",
    "research_analytics": "Comprehensive research analytics and impact measurement"
}

def get_research_hub_status():
    """Get the overall status of the Research & Innovation Hub."""
    return {
        "phase": "Phase 6: Research & Innovation Hub",
        "status": "Active",
        "capabilities": RESEARCH_CAPABILITIES,
        "components": [
            "Clinical Data Integration",
            "Research Collaboration Platform", 
            "Publication Pipeline",
            "Evidence-Based Insights",
            "Research Analytics"
        ],
        "version": __version__
    }
