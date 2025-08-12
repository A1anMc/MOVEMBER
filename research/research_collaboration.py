import asyncio
import logging
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
import uuid

logger = logging.getLogger(__name__)

class CollaborationType(Enum):
    RESEARCH_PARTNERSHIP = "research_partnership"
    DATA_SHARING = "data_sharing"
    CLINICAL_TRIAL = "clinical_trial"
    PUBLICATION = "publication"
    CONFERENCE = "conference"

class InstitutionType(Enum):
    UNIVERSITY = "university"
    HOSPITAL = "hospital"
    RESEARCH_INSTITUTE = "research_institute"
    PHARMACEUTICAL = "pharmaceutical"
    NON_PROFIT = "non_profit"
    GOVERNMENT = "government"

@dataclass
class ResearchInstitution:
    institution_id: str
    name: str
    type: InstitutionType
    country: str
    expertise_areas: List[str]
    contact_email: str
    website: str
    collaboration_score: float = 0.0
    active_projects: int = 0

@dataclass
class ResearchProject:
    project_id: str
    title: str
    description: str
    lead_institution: str
    collaborating_institutions: List[str]
    start_date: datetime
    end_date: Optional[datetime] = None
    budget: float
    status: str
    research_areas: List[str]
    team_members: List[str]
    milestones: List[Dict[str, Any]]

@dataclass
class CollaborationSession:
    session_id: str
    project_id: str
    participants: List[str]
    session_type: str
    start_time: datetime
    end_time: Optional[datetime] = None
    agenda: List[str]
    outcomes: List[str]
    documents_shared: List[str]

class ResearchCollaborationPlatform:
    """Multi-institution research collaboration platform."""
    
    def __init__(self):
        self.institutions: Dict[str, ResearchInstitution] = {}
        self.projects: Dict[str, ResearchProject] = {}
        self.sessions: Dict[str, CollaborationSession] = {}
        self.total_collaborations = 0
        self.active_projects = 0
        logger.info("Research Collaboration Platform initialized")

    def register_institution(self, name: str, institution_type: InstitutionType, 
                           country: str, expertise_areas: List[str], 
                           contact_email: str, website: str) -> str:
        """Register a new research institution."""
        institution_id = str(uuid.uuid4())
        
        institution = ResearchInstitution(
            institution_id=institution_id,
            name=name,
            type=institution_type,
            country=country,
            expertise_areas=expertise_areas,
            contact_email=contact_email,
            website=website
        )
        
        self.institutions[institution_id] = institution
        logger.info(f"Registered institution: {name}")
        return institution_id

    def create_research_project(self, title: str, description: str, 
                               lead_institution: str, collaborating_institutions: List[str],
                               start_date: datetime, budget: float, 
                               research_areas: List[str], end_date: Optional[datetime] = None) -> str:
        """Create a new research project."""
        project_id = str(uuid.uuid4())
        
        project = ResearchProject(
            project_id=project_id,
            title=title,
            description=description,
            lead_institution=lead_institution,
            collaborating_institutions=collaborating_institutions,
            start_date=start_date,
            end_date=end_date,
            budget=budget,
            status="Active",
            research_areas=research_areas,
            team_members=[],
            milestones=[]
        )
        
        self.projects[project_id] = project
        self.active_projects += 1
        
        # Update institution collaboration scores
        for inst_id in [lead_institution] + collaborating_institutions:
            if inst_id in self.institutions:
                self.institutions[inst_id].active_projects += 1
                self.institutions[inst_id].collaboration_score += 0.1
        
        logger.info(f"Created research project: {title}")
        return project_id

    def start_collaboration_session(self, project_id: str, participants: List[str],
                                   session_type: str, agenda: List[str]) -> str:
        """Start a collaboration session."""
        session_id = str(uuid.uuid4())
        
        session = CollaborationSession(
            session_id=session_id,
            project_id=project_id,
            participants=participants,
            session_type=session_type,
            start_time=datetime.now(),
            agenda=agenda,
            outcomes=[],
            documents_shared=[]
        )
        
        self.sessions[session_id] = session
        self.total_collaborations += 1
        logger.info(f"Started collaboration session: {session_type}")
        return session_id

    def end_collaboration_session(self, session_id: str, outcomes: List[str]) -> bool:
        """End a collaboration session with outcomes."""
        if session_id in self.sessions:
            self.sessions[session_id].end_time = datetime.now()
            self.sessions[session_id].outcomes = outcomes
            logger.info(f"Ended collaboration session with {len(outcomes)} outcomes")
            return True
        return False

    def add_project_milestone(self, project_id: str, milestone_title: str, 
                             due_date: datetime, description: str) -> bool:
        """Add a milestone to a research project."""
        if project_id in self.projects:
            milestone = {
                'id': str(uuid.uuid4()),
                'title': milestone_title,
                'due_date': due_date.isoformat(),
                'description': description,
                'status': 'Pending',
                'completed_date': None
            }
            self.projects[project_id].milestones.append(milestone)
            logger.info(f"Added milestone to project: {milestone_title}")
            return True
        return False

    def complete_milestone(self, project_id: str, milestone_id: str) -> bool:
        """Mark a milestone as completed."""
        if project_id in self.projects:
            for milestone in self.projects[project_id].milestones:
                if milestone['id'] == milestone_id:
                    milestone['status'] = 'Completed'
                    milestone['completed_date'] = datetime.now().isoformat()
                    logger.info(f"Completed milestone: {milestone['title']}")
                    return True
        return False

    def get_collaboration_network(self) -> Dict[str, Any]:
        """Get the collaboration network analysis."""
        network_data = {
            'total_institutions': len(self.institutions),
            'total_projects': len(self.projects),
            'active_projects': self.active_projects,
            'total_sessions': self.total_collaborations,
            'institution_types': {},
            'research_areas': {},
            'collaboration_hotspots': []
        }
        
        # Analyze institution types
        for institution in self.institutions.values():
            inst_type = institution.type.value
            network_data['institution_types'][inst_type] = network_data['institution_types'].get(inst_type, 0) + 1
        
        # Analyze research areas
        for project in self.projects.values():
            for area in project.research_areas:
                network_data['research_areas'][area] = network_data['research_areas'].get(area, 0) + 1
        
        # Find collaboration hotspots
        collaboration_counts = {}
        for project in self.projects.values():
            for inst_id in project.collaborating_institutions:
                collaboration_counts[inst_id] = collaboration_counts.get(inst_id, 0) + 1
        
        # Get top collaborating institutions
        top_collaborators = sorted(collaboration_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        for inst_id, count in top_collaborators:
            if inst_id in self.institutions:
                network_data['collaboration_hotspots'].append({
                    'institution': self.institutions[inst_id].name,
                    'collaboration_count': count,
                    'country': self.institutions[inst_id].country
                })
        
        return network_data

    def get_institution_performance(self, institution_id: str) -> Optional[Dict[str, Any]]:
        """Get performance metrics for a specific institution."""
        if institution_id not in self.institutions:
            return None
        
        institution = self.institutions[institution_id]
        
        # Find projects involving this institution
        projects_involved = []
        for project in self.projects.values():
            if (institution_id == project.lead_institution or 
                institution_id in project.collaborating_institutions):
                projects_involved.append({
                    'project_id': project.project_id,
                    'title': project.title,
                    'role': 'Lead' if institution_id == project.lead_institution else 'Collaborator',
                    'status': project.status
                })
        
        # Find collaboration sessions
        sessions_involved = []
        for session in self.sessions.values():
            if institution_id in session.participants:
                sessions_involved.append({
                    'session_id': session.session_id,
                    'type': session.session_type,
                    'date': session.start_time.isoformat()
                })
        
        return {
            'institution_name': institution.name,
            'institution_type': institution.type.value,
            'country': institution.country,
            'expertise_areas': institution.expertise_areas,
            'collaboration_score': institution.collaboration_score,
            'active_projects': institution.active_projects,
            'projects_involved': projects_involved,
            'sessions_involved': sessions_involved,
            'performance_metrics': {
                'project_leadership_rate': len([p for p in projects_involved if p['role'] == 'Lead']) / max(len(projects_involved), 1),
                'collaboration_frequency': len(sessions_involved),
                'expertise_diversity': len(institution.expertise_areas)
            }
        }

    def get_platform_stats(self) -> Dict[str, Any]:
        """Get comprehensive platform statistics."""
        return {
            'total_institutions': len(self.institutions),
            'total_projects': len(self.projects),
            'active_projects': self.active_projects,
            'total_sessions': self.total_collaborations,
            'institution_types': [inst.type.value for inst in self.institutions.values()],
            'research_areas': list(set([area for project in self.projects.values() for area in project.research_areas])),
            'collaboration_network': self.get_collaboration_network(),
            'last_updated': datetime.now().isoformat()
        }

# Global instance
collaboration_platform = ResearchCollaborationPlatform()

# Initialize with sample data
def initialize_sample_data():
    """Initialize the platform with sample research institutions and projects."""
    
    # Register sample institutions
    movember_id = collaboration_platform.register_institution(
        "Movember Foundation",
        InstitutionType.NON_PROFIT,
        "Australia",
        ["prostate cancer", "testicular cancer", "mens mental health"],
        "research@movember.com",
        "https://movember.com"
    )
    
    uni_melbourne_id = collaboration_platform.register_institution(
        "University of Melbourne",
        InstitutionType.UNIVERSITY,
        "Australia",
        ["cancer research", "public health", "clinical trials"],
        "research@unimelb.edu.au",
        "https://unimelb.edu.au"
    )
    
    pcf_id = collaboration_platform.register_institution(
        "Prostate Cancer Foundation",
        InstitutionType.NON_PROFIT,
        "United States",
        ["prostate cancer", "treatment research", "patient support"],
        "research@pcf.org",
        "https://pcf.org"
    )
    
    # Create sample research projects
    project1_id = collaboration_platform.create_research_project(
        "Advanced Prostate Cancer Treatment Study",
        "Multi-center study on novel treatment approaches for advanced prostate cancer",
        movember_id,
        [uni_melbourne_id, pcf_id],
        datetime.now(),
        2500000.0,
        ["prostate cancer", "treatment", "clinical trials"]
    )
    
    project2_id = collaboration_platform.create_research_project(
        "Men's Mental Health Intervention Program",
        "Development and evaluation of mental health interventions specifically for men",
        movember_id,
        [uni_melbourne_id],
        datetime.now(),
        1500000.0,
        ["mens mental health", "intervention", "prevention"]
    )
    
    # Add milestones
    collaboration_platform.add_project_milestone(
        project1_id,
        "Protocol Development",
        datetime.now() + timedelta(days=30),
        "Develop and finalize study protocol"
    )
    
    collaboration_platform.add_project_milestone(
        project1_id,
        "Patient Recruitment",
        datetime.now() + timedelta(days=90),
        "Begin patient recruitment across all sites"
    )
    
    logger.info("Sample research collaboration data initialized")

# Initialize sample data
initialize_sample_data()

# Functions for external use
def register_research_institution(name: str, institution_type: InstitutionType, 
                                country: str, expertise_areas: List[str], 
                                contact_email: str, website: str) -> str:
    """Register a new research institution."""
    return collaboration_platform.register_institution(
        name, institution_type, country, expertise_areas, contact_email, website
    )

def create_research_project(title: str, description: str, lead_institution: str,
                           collaborating_institutions: List[str], start_date: datetime,
                           budget: float, research_areas: List[str]) -> str:
    """Create a new research project."""
    return collaboration_platform.create_research_project(
        title, description, lead_institution, collaborating_institutions,
        start_date, budget, research_areas
    )

def get_collaboration_network_analysis() -> Dict[str, Any]:
    """Get collaboration network analysis."""
    return collaboration_platform.get_collaboration_network()

def get_institution_performance_metrics(institution_id: str) -> Optional[Dict[str, Any]]:
    """Get performance metrics for a specific institution."""
    return collaboration_platform.get_institution_performance(institution_id)

def get_platform_statistics() -> Dict[str, Any]:
    """Get comprehensive platform statistics."""
    return collaboration_platform.get_platform_stats()

if __name__ == "__main__":
    async def test_collaboration_platform():
        """Test the research collaboration platform."""
        print("🤝 Testing Research Collaboration Platform...")
        
        # Test registering an institution
        print("\n🏢 Registering new institution...")
        new_institution_id = register_research_institution(
            "Test Research Institute",
            InstitutionType.RESEARCH_INSTITUTE,
            "Test Country",
            ["test research", "test area"],
            "test@test.com",
            "https://test.com"
        )
        print(f"Registered institution with ID: {new_institution_id}")
        
        # Test creating a new project
        print("\n📋 Creating new research project...")
        new_project_id = create_research_project(
            "Test Project",
            "Description for Test Project",
            new_institution_id,
            [new_institution_id], # Self-collaboration for testing
            datetime.now(),
            100000.0,
            ["test area"]
        )
        print(f"Created project with ID: {new_project_id}")
        
        # Test starting a session
        print("\n📹 Starting collaboration session...")
        session_id = collaboration_platform.start_collaboration_session(
            new_project_id,
            [new_institution_id],
            "Test Session Type",
            ["Session Agenda"]
        )
        print(f"Started session with ID: {session_id}")
        
        # Test ending a session
        print("\n📝 Ending collaboration session...")
        collaboration_platform.end_collaboration_session(
            session_id,
            ["Outcome 1", "Outcome 2"]
        )
        print("Session ended.")
        
        # Test adding a milestone
        print("\n🎯 Adding milestone to project...")
        collaboration_platform.add_project_milestone(
            new_project_id,
            "Test Milestone",
            datetime.now() + timedelta(days=10),
            "Description for Test Milestone"
        )
        print("Milestone added.")
        
        # Test completing a milestone
        print("\n✅ Completing milestone...")
        # Need to get the milestone ID first. This is a simplification.
        # In a real scenario, you'd store the milestone ID returned by add_project_milestone
        # For now, we'll just complete the first milestone found.
        if new_project_id in collaboration_platform.projects:
            first_milestone_id = collaboration_platform.projects[new_project_id].milestones[0]['id']
            collaboration_platform.complete_milestone(new_project_id, first_milestone_id)
            print(f"Completed milestone with ID: {first_milestone_id}")
        else:
            print("Project not found to complete milestone.")
        
        # Print stats
        print(f"\n📊 Platform Stats: {get_platform_statistics()}")
        print(f"\n🔗 Collaboration Network: {json.dumps(get_collaboration_network_analysis(), indent=2)}")
        print(f"\n📈 Institution Performance for {new_institution_id}: {json.dumps(get_institution_performance_metrics(new_institution_id), indent=2)}")
    
    asyncio.run(test_collaboration_platform())
