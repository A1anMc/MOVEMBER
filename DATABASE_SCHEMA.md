# 🗄️ **Movember AI Rules System - Database Schema**

## **📋 Overview**

The Movember AI Rules System uses PostgreSQL in production with SQLite for local development. All data follows UK spelling and AUD currency standards.

**Production Database**: PostgreSQL on Render  
**Development Database**: SQLite (`movember_ai.db`)

## **🏗️ Database Architecture**

### **Core Tables**

| Table | Purpose | Records | Size |
|-------|---------|---------|------|
| `grants` | Grant applications and evaluations | ~1,000 | 2.5MB |
| `reports` | Impact reports and assessments | ~500 | 1.8MB |
| `evaluations` | Rule evaluation results | ~10,000 | 15.2MB |
| `metrics` | System performance metrics | ~50,000 | 8.7MB |
| `external_data` | Scraped external data | ~2,000 | 3.1MB |

## **📊 Table Schemas**

### **1. Grants Table**

**Purpose**: Store grant applications and their evaluation results.

```sql
CREATE TABLE grants (
    id SERIAL PRIMARY KEY,
    grant_id VARCHAR(50) UNIQUE NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    budget DECIMAL(15,2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'AUD',
    timeline_months INTEGER,
    organisation VARCHAR(255),
    contact_person VARCHAR(255),
    email VARCHAR(255),
    status VARCHAR(50) DEFAULT 'submitted',
    score DECIMAL(5,2),
    evaluation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    frameworks JSONB,
    outputs JSONB,
    outcomes JSONB,
    recommendations JSONB,
    evaluation_results JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Sample Data:**
```json
{
  "grant_id": "GRANT-2024-001",
  "title": "Men's Health Research Initiative",
  "description": "Comprehensive research into men's mental health awareness",
  "budget": 500000.00,
  "currency": "AUD",
  "timeline_months": 24,
  "organisation": "University of Sydney",
  "contact_person": "Dr. John Smith",
  "email": "john.smith@usyd.edu.au",
  "status": "evaluated",
  "score": 2.71,
  "frameworks": ["ToC", "SDG"],
  "outputs": [
    {
      "name": "Health Screenings",
      "count": 1500,
      "description": "Mental health screenings conducted"
    }
  ],
  "outcomes": [
    {
      "name": "Increased Awareness",
      "metric": "85% improvement",
      "description": "Improved mental health awareness"
    }
  ],
  "recommendations": [
    "Include measurable impact metrics aligned with Movember's mission",
    "Specify alignment with Sustainable Development Goals (SDGs)",
    "Include stakeholder engagement strategies for community involvement"
  ]
}
```

### **2. Reports Table**

**Purpose**: Store impact reports and their evaluation results.

```sql
CREATE TABLE reports (
    id SERIAL PRIMARY KEY,
    report_id VARCHAR(50) UNIQUE NOT NULL,
    title VARCHAR(255) NOT NULL,
    type VARCHAR(50) NOT NULL,
    organisation VARCHAR(255),
    contact_person VARCHAR(255),
    email VARCHAR(255),
    status VARCHAR(50) DEFAULT 'submitted',
    score DECIMAL(5,2),
    evaluation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    frameworks JSONB,
    outputs JSONB,
    outcomes JSONB,
    recommendations JSONB,
    evaluation_results JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Sample Data:**
```json
{
  "report_id": "IMP-2024-001",
  "title": "Men's Health Impact Assessment",
  "type": "impact",
  "organisation": "University of Sydney",
  "contact_person": "Dr. John Smith",
  "email": "john.smith@usyd.edu.au",
  "status": "evaluated",
  "score": 3.2,
  "frameworks": ["ToC", "SDG"],
  "outputs": [
    {
      "name": "Health Screenings",
      "count": 1500,
      "description": "Mental health screenings conducted"
    }
  ],
  "outcomes": [
    {
      "name": "Increased Awareness",
      "metric": "85% improvement",
      "description": "Improved mental health awareness"
    }
  ]
}
```

### **3. Evaluations Table**

**Purpose**: Store detailed rule evaluation results for audit and analysis.

```sql
CREATE TABLE evaluations (
    id SERIAL PRIMARY KEY,
    evaluation_id VARCHAR(50) UNIQUE NOT NULL,
    grant_id VARCHAR(50),
    report_id VARCHAR(50),
    rule_name VARCHAR(255) NOT NULL,
    success BOOLEAN NOT NULL,
    conditions_met BOOLEAN NOT NULL,
    execution_time DECIMAL(10,6),
    priority INTEGER,
    action_results JSONB,
    error_message TEXT,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (grant_id) REFERENCES grants(grant_id),
    FOREIGN KEY (report_id) REFERENCES reports(report_id)
);
```

**Sample Data:**
```json
{
  "evaluation_id": "EVAL-2024-001",
  "grant_id": "GRANT-2024-001",
  "rule_name": "validate_movember_context",
  "success": true,
  "conditions_met": false,
  "execution_time": 0.025195,
  "priority": 100,
  "action_results": [],
  "error_message": null,
  "metadata": {
    "priority": 100,
    "category": "validation"
  }
}
```

### **4. Metrics Table**

**Purpose**: Store system performance metrics and monitoring data.

```sql
CREATE TABLE metrics (
    id SERIAL PRIMARY KEY,
    metric_id VARCHAR(50) UNIQUE NOT NULL,
    metric_type VARCHAR(50) NOT NULL,
    metric_name VARCHAR(255) NOT NULL,
    metric_value DECIMAL(15,6),
    metric_unit VARCHAR(50),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Sample Data:**
```json
{
  "metric_id": "METRIC-2024-001",
  "metric_type": "system",
  "metric_name": "total_rules_executed",
  "metric_value": 74,
  "metric_unit": "count",
  "timestamp": "2025-08-08T11:08:08.392169",
  "metadata": {
    "source": "rules_engine",
    "category": "performance"
  }
}
```

### **5. External Data Table**

**Purpose**: Store scraped and collected external data.

```sql
CREATE TABLE external_data (
    id SERIAL PRIMARY KEY,
    data_id VARCHAR(50) UNIQUE NOT NULL,
    source_type VARCHAR(100) NOT NULL,
    source_url VARCHAR(500),
    title VARCHAR(255),
    description TEXT,
    budget DECIMAL(15,2),
    currency VARCHAR(3) DEFAULT 'AUD',
    deadline DATE,
    organisation VARCHAR(255),
    keywords JSONB,
    validation_results JSONB,
    raw_data JSONB,
    processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Sample Data:**
```json
{
  "data_id": "EXT-2024-001",
  "source_type": "grants_database",
  "source_url": "https://www.health.vic.gov.au/about/our-grants",
  "title": "Men's Mental Health Research Grant",
  "description": "Funding for research into men's mental health awareness",
  "budget": 500000.00,
  "currency": "AUD",
  "deadline": "2024-12-31",
  "organisation": "Victorian Department of Health",
  "keywords": ["men's health", "mental health", "research"],
  "validation_results": {
    "uk_spelling_compliance": 0.98,
    "aud_currency_compliance": 1.0,
    "mission_alignment": 0.87
  }
}
```

## **🔗 Relationships**

### **Primary Relationships**

```mermaid
erDiagram
    GRANTS ||--o{ EVALUATIONS : "has"
    REPORTS ||--o{ EVALUATIONS : "has"
    GRANTS ||--o{ METRICS : "generates"
    REPORTS ||--o{ METRICS : "generates"
    EXTERNAL_DATA ||--o{ GRANTS : "informs"
```

### **Foreign Key Constraints**

| Table | Column | References | Constraint |
|-------|--------|------------|------------|
| `evaluations` | `grant_id` | `grants.grant_id` | ON DELETE CASCADE |
| `evaluations` | `report_id` | `reports.report_id` | ON DELETE CASCADE |

## **📈 Data Models (Pydantic)**

### **Grant Model**

```python
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class Output(BaseModel):
    name: str
    count: int
    description: str

class Outcome(BaseModel):
    name: str
    metric: str
    description: str

class Grant(BaseModel):
    grant_id: str = Field(..., description="Unique grant identifier")
    title: str = Field(..., description="Grant title")
    description: Optional[str] = Field(None, description="Grant description")
    budget: float = Field(..., description="Budget amount in AUD")
    currency: str = Field(default="AUD", description="Currency code")
    timeline_months: Optional[int] = Field(None, description="Project timeline in months")
    organisation: Optional[str] = Field(None, description="Organisation name")
    contact_person: Optional[str] = Field(None, description="Contact person name")
    email: Optional[str] = Field(None, description="Contact email")
    frameworks: Optional[List[str]] = Field(None, description="Impact frameworks used")
    outputs: Optional[List[Output]] = Field(None, description="Project outputs")
    outcomes: Optional[List[Outcome]] = Field(None, description="Project outcomes")
    
    class Config:
        json_schema_extra = {
            "example": {
                "grant_id": "GRANT-2024-001",
                "title": "Men's Health Research Initiative",
                "description": "Comprehensive research into men's mental health awareness",
                "budget": 500000.00,
                "currency": "AUD",
                "timeline_months": 24,
                "organisation": "University of Sydney",
                "contact_person": "Dr. John Smith",
                "email": "john.smith@usyd.edu.au",
                "frameworks": ["ToC", "SDG"],
                "outputs": [
                    {
                        "name": "Health Screenings",
                        "count": 1500,
                        "description": "Mental health screenings conducted"
                    }
                ],
                "outcomes": [
                    {
                        "name": "Increased Awareness",
                        "metric": "85% improvement",
                        "description": "Improved mental health awareness"
                    }
                ]
            }
        }
```

### **Report Model**

```python
class Report(BaseModel):
    report_id: str = Field(..., description="Unique report identifier")
    title: str = Field(..., description="Report title")
    type: str = Field(..., description="Report type (impact, evaluation, etc.)")
    organisation: Optional[str] = Field(None, description="Organisation name")
    contact_person: Optional[str] = Field(None, description="Contact person name")
    email: Optional[str] = Field(None, description="Contact email")
    frameworks: Optional[List[str]] = Field(None, description="Impact frameworks used")
    outputs: Optional[List[Output]] = Field(None, description="Report outputs")
    outcomes: Optional[List[Outcome]] = Field(None, description="Report outcomes")
    
    class Config:
        json_schema_extra = {
            "example": {
                "report_id": "IMP-2024-001",
                "title": "Men's Health Impact Assessment",
                "type": "impact",
                "organisation": "University of Sydney",
                "contact_person": "Dr. John Smith",
                "email": "john.smith@usyd.edu.au",
                "frameworks": ["ToC", "SDG"],
                "outputs": [
                    {
                        "name": "Health Screenings",
                        "count": 1500,
                        "description": "Mental health screenings conducted"
                    }
                ],
                "outcomes": [
                    {
                        "name": "Increased Awareness",
                        "metric": "85% improvement",
                        "description": "Improved mental health awareness"
                    }
                ]
            }
        }
```

### **Evaluation Model**

```python
class ActionResult(BaseModel):
    action_name: str
    success: bool
    result: str
    error: Optional[str] = None
    execution_time: float
    metadata: Dict[str, Any] = {}

class Evaluation(BaseModel):
    evaluation_id: str = Field(..., description="Unique evaluation identifier")
    grant_id: Optional[str] = Field(None, description="Associated grant ID")
    report_id: Optional[str] = Field(None, description="Associated report ID")
    rule_name: str = Field(..., description="Rule that was evaluated")
    success: bool = Field(..., description="Whether evaluation succeeded")
    conditions_met: bool = Field(..., description="Whether conditions were met")
    execution_time: float = Field(..., description="Execution time in seconds")
    priority: int = Field(..., description="Rule priority")
    action_results: List[ActionResult] = Field(default=[], description="Action results")
    error_message: Optional[str] = Field(None, description="Error message if failed")
    metadata: Dict[str, Any] = Field(default={}, description="Additional metadata")
```

## **🔧 Database Operations**

### **Connection Management**

```python
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Production (PostgreSQL)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:pass@localhost/movember_ai")

# Development (SQLite)
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
```

### **Common Queries**

**Get Grant with Evaluations:**
```sql
SELECT g.*, 
       json_agg(e.*) as evaluations
FROM grants g
LEFT JOIN evaluations e ON g.grant_id = e.grant_id
WHERE g.grant_id = 'GRANT-2024-001'
GROUP BY g.id;
```

**Get System Metrics:**
```sql
SELECT metric_name, 
       AVG(metric_value) as avg_value,
       MAX(metric_value) as max_value,
       MIN(metric_value) as min_value
FROM metrics 
WHERE timestamp >= NOW() - INTERVAL '24 hours'
GROUP BY metric_name;
```

**Get Recent Evaluations:**
```sql
SELECT rule_name, 
       COUNT(*) as execution_count,
       AVG(execution_time) as avg_execution_time,
       SUM(CASE WHEN success THEN 1 ELSE 0 END) as success_count
FROM evaluations 
WHERE created_at >= NOW() - INTERVAL '7 days'
GROUP BY rule_name
ORDER BY execution_count DESC;
```

## **📊 Data Validation**

### **UK Spelling Validation**

```python
UK_SPELLING_MAP = {
    "color": "colour",
    "behavior": "behaviour", 
    "organization": "organisation",
    "realize": "realise",
    "analyze": "analyse",
    "center": "centre",
    "favorite": "favourite",
    "labor": "labour",
    "honor": "honour",
    "defense": "defence",
    "license": "licence",
    "practice": "practise",
    "program": "programme"
}

def validate_uk_spelling(text: str) -> Dict[str, Any]:
    """Validate and convert text to UK spelling."""
    issues = []
    corrected_text = text
    
    for us_spelling, uk_spelling in UK_SPELLING_MAP.items():
        if us_spelling in text.lower():
            issues.append({
                "found": us_spelling,
                "suggested": uk_spelling,
                "context": text[text.lower().find(us_spelling):text.lower().find(us_spelling)+len(us_spelling)]
            })
            corrected_text = corrected_text.replace(us_spelling, uk_spelling)
    
    return {
        "original": text,
        "corrected": corrected_text,
        "issues": issues,
        "compliance_score": 1.0 - (len(issues) / max(len(text.split()), 1))
    }
```

### **AUD Currency Validation**

```python
import re

def validate_aud_currency(amount: float, currency: str) -> Dict[str, Any]:
    """Validate that amounts are in AUD currency."""
    if currency != "AUD":
        return {
            "valid": False,
            "error": f"Currency must be AUD, got {currency}",
            "suggested": "AUD"
        }
    
    if amount < 0:
        return {
            "valid": False,
            "error": "Amount cannot be negative",
            "suggested": abs(amount)
        }
    
    return {
        "valid": True,
        "amount": amount,
        "currency": "AUD",
        "formatted": f"A${amount:,.2f}"
    }
```

## **🔄 Migration Guide**

### **Creating a New Migration**

```bash
# Generate migration file
alembic revision --autogenerate -m "Add new table"

# Apply migration
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

### **Sample Migration**

```python
"""Add external_data table

Revision ID: 001_add_external_data
Revises: 000_initial
Create Date: 2025-08-08 11:08:08.392169

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    op.create_table('external_data',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('data_id', sa.String(length=50), nullable=False),
        sa.Column('source_type', sa.String(length=100), nullable=False),
        sa.Column('source_url', sa.String(length=500), nullable=True),
        sa.Column('title', sa.String(length=255), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('budget', sa.Decimal(precision=15, scale=2), nullable=True),
        sa.Column('currency', sa.String(length=3), nullable=True),
        sa.Column('deadline', sa.Date(), nullable=True),
        sa.Column('organisation', sa.String(length=255), nullable=True),
        sa.Column('keywords', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('validation_results', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('raw_data', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('processed_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('data_id')
    )

def downgrade():
    op.drop_table('external_data')
```

## **📈 Performance Optimization**

### **Indexes**

```sql
-- Performance indexes
CREATE INDEX idx_grants_grant_id ON grants(grant_id);
CREATE INDEX idx_grants_status ON grants(status);
CREATE INDEX idx_grants_created_at ON grants(created_at);
CREATE INDEX idx_evaluations_grant_id ON evaluations(grant_id);
CREATE INDEX idx_evaluations_rule_name ON evaluations(rule_name);
CREATE INDEX idx_metrics_timestamp ON metrics(timestamp);
CREATE INDEX idx_metrics_metric_name ON metrics(metric_name);
```

### **Partitioning**

```sql
-- Partition metrics table by month
CREATE TABLE metrics_y2025m08 PARTITION OF metrics
FOR VALUES FROM ('2025-08-01') TO ('2025-09-01');
```

## **🔒 Security**

### **Data Encryption**

```python
from cryptography.fernet import Fernet
import base64

def encrypt_sensitive_data(data: str) -> str:
    """Encrypt sensitive data before storage."""
    key = Fernet.generate_key()
    cipher_suite = Fernet(key)
    encrypted_data = cipher_suite.encrypt(data.encode())
    return base64.b64encode(encrypted_data).decode()

def decrypt_sensitive_data(encrypted_data: str) -> str:
    """Decrypt sensitive data after retrieval."""
    key = Fernet.generate_key()
    cipher_suite = Fernet(key)
    decrypted_data = cipher_suite.decrypt(base64.b64decode(encrypted_data))
    return decrypted_data.decode()
```

### **Access Control**

```sql
-- Create read-only user
CREATE USER movember_readonly WITH PASSWORD 'secure_password';
GRANT CONNECT ON DATABASE movember_ai TO movember_readonly;
GRANT USAGE ON SCHEMA public TO movember_readonly;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO movember_readonly;
```

---

**Movember AI Rules System Database Schema v1.1** - Professional, secure, and optimised for performance. 🇦🇺 