import asyncio
import logging
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
import uuid

logger = logging.getLogger(__name__)

class PublicationType(Enum):
    RESEARCH_PAPER = "research_paper"
    SYSTEMATIC_REVIEW = "systematic_review"
    CLINICAL_GUIDELINE = "clinical_guideline"
    CASE_STUDY = "case_study"
    CONFERENCE_ABSTRACT = "conference_abstract"
    TECHNICAL_REPORT = "technical_report"

class PublicationStatus(Enum):
    DRAFT = "draft"
    UNDER_REVIEW = "under_review"
    REVISED = "revised"
    ACCEPTED = "accepted"
    PUBLISHED = "published"
    REJECTED = "rejected"

@dataclass
class ResearchPublication:
    publication_id: str
    title: str
    abstract: str
    authors: List[str]
    publication_type: PublicationType
    status: PublicationStatus
    created_date: datetime
    last_modified: datetime
    keywords: List[str]
    doi: Optional[str] = None
    journal: Optional[str] = None
    volume: Optional[str] = None
    issue: Optional[str] = None
    pages: Optional[str] = None
    citation_count: int = 0
    impact_factor: float = 0.0

@dataclass
class PublicationTemplate:
    template_id: str
    name: str
    publication_type: PublicationType
    structure: Dict[str, Any]
    formatting_rules: Dict[str, Any]
    required_sections: List[str]

class PublicationPipeline:
    """Automated research publication generation and management."""
    
    def __init__(self):
        self.publications: Dict[str, ResearchPublication] = {}
        self.templates: Dict[str, PublicationTemplate] = {}
        self.total_publications = 0
        self.published_count = 0
        self.citation_total = 0
        logger.info("Publication Pipeline initialized")

    def create_publication_template(self, name: str, publication_type: PublicationType,
                                   structure: Dict[str, Any], formatting_rules: Dict[str, Any],
                                   required_sections: List[str]) -> str:
        """Create a publication template."""
        template_id = str(uuid.uuid4())
        
        template = PublicationTemplate(
            template_id=template_id,
            name=name,
            publication_type=publication_type,
            structure=structure,
            formatting_rules=formatting_rules,
            required_sections=required_sections
        )
        
        self.templates[template_id] = template
        logger.info(f"Created publication template: {name}")
        return template_id

    def generate_research_publication(self, title: str, abstract: str, authors: List[str],
                                     publication_type: PublicationType, keywords: List[str],
                                     template_id: Optional[str] = None) -> str:
        """Generate a new research publication."""
        publication_id = str(uuid.uuid4())
        
        publication = ResearchPublication(
            publication_id=publication_id,
            title=title,
            abstract=abstract,
            authors=authors,
            publication_type=publication_type,
            status=PublicationStatus.DRAFT,
            created_date=datetime.now(),
            last_modified=datetime.now(),
            keywords=keywords
        )
        
        self.publications[publication_id] = publication
        self.total_publications += 1
        logger.info(f"Generated research publication: {title}")
        return publication_id

    def update_publication_status(self, publication_id: str, status: PublicationStatus) -> bool:
        """Update the status of a publication."""
        if publication_id in self.publications:
            self.publications[publication_id].status = status
            self.publications[publication_id].last_modified = datetime.now()
            
            if status == PublicationStatus.PUBLISHED:
                self.published_count += 1
            
            logger.info(f"Updated publication status to: {status.value}")
            return True
        return False

    def add_publication_metadata(self, publication_id: str, doi: str, journal: str,
                                volume: str, issue: str, pages: str) -> bool:
        """Add publication metadata."""
        if publication_id in self.publications:
            pub = self.publications[publication_id]
            pub.doi = doi
            pub.journal = journal
            pub.volume = volume
            pub.issue = issue
            pub.pages = pages
            pub.last_modified = datetime.now()
            logger.info(f"Added metadata to publication: {doi}")
            return True
        return False

    def update_citation_count(self, publication_id: str, citation_count: int) -> bool:
        """Update citation count for a publication."""
        if publication_id in self.publications:
            old_count = self.publications[publication_id].citation_count
            self.publications[publication_id].citation_count = citation_count
            self.publications[publication_id].last_modified = datetime.now()
            
            # Update total citations
            self.citation_total = self.citation_total - old_count + citation_count
            
            logger.info(f"Updated citation count to: {citation_count}")
            return True
        return False

    def generate_publication_report(self, publication_id: str) -> Optional[Dict[str, Any]]:
        """Generate a detailed report for a publication."""
        if publication_id not in self.publications:
            return None
        
        pub = self.publications[publication_id]
        
        return {
            'publication_id': pub.publication_id,
            'title': pub.title,
            'abstract': pub.abstract,
            'authors': pub.authors,
            'publication_type': pub.publication_type.value,
            'status': pub.status.value,
            'keywords': pub.keywords,
            'metadata': {
                'doi': pub.doi,
                'journal': pub.journal,
                'volume': pub.volume,
                'issue': pub.issue,
                'pages': pub.pages
            },
            'metrics': {
                'citation_count': pub.citation_count,
                'impact_factor': pub.impact_factor
            },
            'timeline': {
                'created_date': pub.created_date.isoformat(),
                'last_modified': pub.last_modified.isoformat()
            }
        }

    def get_publication_statistics(self) -> Dict[str, Any]:
        """Get comprehensive publication statistics."""
        stats = {
            'total_publications': self.total_publications,
            'published_count': self.published_count,
            'total_citations': self.citation_total,
            'publication_types': {},
            'status_distribution': {},
            'top_cited_publications': [],
            'recent_publications': []
        }
        
        # Analyze publication types
        for pub in self.publications.values():
            pub_type = pub.publication_type.value
            stats['publication_types'][pub_type] = stats['publication_types'].get(pub_type, 0) + 1
        
        # Analyze status distribution
        for pub in self.publications.values():
            status = pub.status.value
            stats['status_distribution'][status] = stats['status_distribution'].get(status, 0) + 1
        
        # Get top cited publications
        sorted_pubs = sorted(self.publications.values(), key=lambda x: x.citation_count, reverse=True)
        for pub in sorted_pubs[:5]:
            stats['top_cited_publications'].append({
                'title': pub.title,
                'citation_count': pub.citation_count,
                'doi': pub.doi,
                'authors': pub.authors
            })
        
        # Get recent publications
        sorted_by_date = sorted(self.publications.values(), key=lambda x: x.created_date, reverse=True)
        for pub in sorted_by_date[:5]:
            stats['recent_publications'].append({
                'title': pub.title,
                'created_date': pub.created_date.isoformat(),
                'status': pub.status.value,
                'publication_type': pub.publication_type.value
            })
        
        return stats

    def search_publications(self, query: str, publication_type: Optional[PublicationType] = None,
                           status: Optional[PublicationStatus] = None) -> List[ResearchPublication]:
        """Search publications by query and filters."""
        results = []
        
        for pub in self.publications.values():
            # Check query match
            query_match = (query.lower() in pub.title.lower() or 
                          query.lower() in pub.abstract.lower() or
                          any(query.lower() in keyword.lower() for keyword in pub.keywords))
            
            # Check type filter
            type_match = publication_type is None or pub.publication_type == publication_type
            
            # Check status filter
            status_match = status is None or pub.status == status
            
            if query_match and type_match and status_match:
                results.append(pub)
        
        return results

# Global instance
publication_pipeline = PublicationPipeline()

# Initialize with sample templates and publications
def initialize_sample_publications():
    """Initialize the pipeline with sample publications."""
    
    # Create templates
    research_paper_template = publication_pipeline.create_publication_template(
        "Standard Research Paper",
        PublicationType.RESEARCH_PAPER,
        {
            "sections": ["Abstract", "Introduction", "Methods", "Results", "Discussion", "Conclusion", "References"],
            "word_limit": 8000,
            "abstract_limit": 250
        },
        {
            "font": "Times New Roman",
            "size": 12,
            "spacing": "double",
            "margins": "1 inch"
        },
        ["Abstract", "Introduction", "Methods", "Results", "Discussion", "References"]
    )
    
    # Generate sample publications
    pub1_id = publication_pipeline.generate_research_publication(
        "Advances in Prostate Cancer Screening: A Systematic Review",
        "This systematic review examines recent advances in prostate cancer screening methods...",
        ["Smith J", "Johnson A", "Brown K"],
        PublicationType.SYSTEMATIC_REVIEW,
        ["prostate cancer", "screening", "systematic review"]
    )
    
    pub2_id = publication_pipeline.generate_research_publication(
        "Mental Health Interventions for Men: Effectiveness and Barriers",
        "Study examining the effectiveness of mental health interventions specifically designed for men...",
        ["Davis M", "Wilson P", "Taylor R"],
        PublicationType.RESEARCH_PAPER,
        ["mens mental health", "interventions", "effectiveness"]
    )
    
    # Update status and add metadata
    publication_pipeline.update_publication_status(pub1_id, PublicationStatus.PUBLISHED)
    publication_pipeline.add_publication_metadata(
        pub1_id, "10.1000/abc123", "Journal of Men's Health", "15", "3", "45-52"
    )
    publication_pipeline.update_citation_count(pub1_id, 25)
    
    publication_pipeline.update_publication_status(pub2_id, PublicationStatus.UNDER_REVIEW)
    
    logger.info("Sample publication data initialized")

# Initialize sample data
initialize_sample_publications()

# Functions for external use
def create_publication_template(name: str, publication_type: PublicationType,
                               structure: Dict[str, Any], formatting_rules: Dict[str, Any],
                               required_sections: List[str]) -> str:
    """Create a publication template."""
    return publication_pipeline.create_publication_template(
        name, publication_type, structure, formatting_rules, required_sections
    )

def generate_research_publication(title: str, abstract: str, authors: List[str],
                                 publication_type: PublicationType, keywords: List[str]) -> str:
    """Generate a new research publication."""
    return publication_pipeline.generate_research_publication(
        title, abstract, authors, publication_type, keywords
    )

def get_publication_statistics() -> Dict[str, Any]:
    """Get comprehensive publication statistics."""
    return publication_pipeline.get_publication_statistics()

def search_publications(query: str, publication_type: Optional[PublicationType] = None,
                       status: Optional[PublicationStatus] = None) -> List[ResearchPublication]:
    """Search publications."""
    return publication_pipeline.search_publications(query, publication_type, status)
