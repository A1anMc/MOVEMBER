# 🚀 **Movember AI Rules System - API Documentation**

## **📋 Overview**

The Movember AI Rules System provides a comprehensive REST API for grant evaluation, impact reporting, and system monitoring. All endpoints return JSON responses and use UK spelling and AUD currency standards.

**Base URL**: `https://movember-api.onrender.com`

## **🔐 Authentication**

Currently, the API uses basic authentication. Include your API key in the request headers:

```bash
curl -H "Authorization: Bearer YOUR_API_KEY" \
     -H "Content-Type: application/json" \
     https://movember-api.onrender.com/health/
```

## **📊 System Health Endpoints**

### **GET /health/**

Returns comprehensive system health information.

**Response:**
```json
{
  "timestamp": "2025-08-08T11:08:08.392169",
  "system_status": "healthy",
  "uptime_percentage": 99.9,
  "active_rules": 74,
  "total_executions": 0,
  "success_rate": 0.0,
  "average_response_time": 0.5,
  "error_count": 0,
  "memory_usage": 50.0,
  "cpu_usage": 30.0,
  "disk_usage": 25.0,
  "active_connections": 5,
  "queue_size": 0,
  "last_backup": "2025-08-08T11:08:08.392154",
  "security_status": "secure",
  "compliance_status": "compliant",
  "uk_spelling_consistency": 1.0,
  "aud_currency_compliance": 1.0
}
```

### **GET /metrics/**

Returns detailed system metrics and performance data.

**Response:**
```json
{
  "status": "success",
  "metrics": {
    "system_metrics": {
      "total_rules_executed": 0,
      "total_batch_executions": 0,
      "total_execution_time": 0.0,
      "average_batch_time": 0.0,
      "peak_concurrent_rules": 0,
      "current_concurrent_rules": 0,
      "uptime_seconds": 0.002257,
      "total_executions": 0,
      "success_rate": 0.0
    },
    "rule_metrics": {},
    "alerts": [],
    "performance_thresholds": {
      "slow_execution_threshold": 5.0,
      "error_rate_threshold": 0.1,
      "memory_usage_threshold": 0.8
    }
  },
  "currency": "AUD",
  "spelling_standard": "UK"
}
```

## **🎯 Grant Management Endpoints**

### **POST /grants/**

Submit a grant application for evaluation.

**Request Body:**
```json
{
  "grant_id": "GRANT-2024-001",
  "title": "Men's Health Research Initiative",
  "description": "Comprehensive research into men's mental health awareness",
  "budget": 500000,
  "timeline_months": 24,
  "organisation": "University of Sydney",
  "contact_person": "Dr. John Smith",
  "email": "john.smith@usyd.edu.au",
  "currency": "AUD",
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

**Response:**
```json
{
  "status": "success",
  "grant_id": "GRANT-2024-001",
  "evaluation_results": [
    {
      "rule_name": "validate_movember_context",
      "success": true,
      "conditions_met": false,
      "action_results": [],
      "error": null,
      "execution_time": 0.02519536018371582,
      "metadata": {
        "priority": 100
      },
      "priority": 100
    }
  ],
  "recommendations": [
    "Include measurable impact metrics aligned with Movember's mission",
    "Specify alignment with Sustainable Development Goals (SDGs)",
    "Include stakeholder engagement strategies for community involvement"
  ],
  "score": 2.7142857142857144,
  "currency": "AUD",
  "spelling_standard": "UK"
}
```

### **GET /grants/{grant_id}**

Retrieve details of a specific grant.

**Response:**
```json
{
  "grant_id": "GRANT-2024-001",
  "title": "Men's Health Research Initiative",
  "status": "evaluated",
  "evaluation_date": "2025-08-08T11:08:08.392169",
  "score": 2.7142857142857144,
  "recommendations": [...],
  "evaluation_results": [...]
}
```

## **📈 Impact Reporting Endpoints**

### **POST /reports/**

Submit an impact report for evaluation.

**Request Body:**
```json
{
  "report_id": "IMP-2024-001",
  "title": "Men's Health Impact Assessment",
  "type": "impact",
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
  "organisation": "University of Sydney",
  "contact_person": "Dr. John Smith",
  "email": "john.smith@usyd.edu.au"
}
```

**Response:**
```json
{
  "status": "success",
  "report_id": "IMP-2024-001",
  "evaluation_results": [...],
  "recommendations": [...],
  "score": 3.2,
  "currency": "AUD",
  "spelling_standard": "UK"
}
```

### **GET /reports/{report_id}**

Retrieve details of a specific impact report.

## **🌐 External Data Collection**

### **POST /external-data/**

Collect external data from various sources.

**Request Body:**
```json
{
  "source_type": "grants_database",
  "endpoint": "https://api.example.com/grants",
  "parameters": {
    "category": "health_research",
    "region": "Australia",
    "year": 2024
  },
  "data_format": "json",
  "validation_rules": [
    "uk_spelling",
    "aud_currency",
    "mission_alignment"
  ]
}
```

**Response:**
```json
{
  "status": "success",
  "data_collected": 150,
  "validation_results": {
    "uk_spelling_compliance": 0.98,
    "aud_currency_compliance": 0.95,
    "mission_alignment": 0.87
  },
  "processed_records": 142,
  "errors": 8,
  "currency": "AUD",
  "spelling_standard": "UK"
}
```

## **🤖 Data Scraping Endpoints**

### **POST /scraper/**

Trigger web scraping for grant opportunities.

**Request Body:**
```json
{
  "target_urls": [
    "https://www.health.vic.gov.au/about/our-grants",
    "https://www.grants.gov.au/Go/List"
  ],
  "selectors": {
    "grant_items": "h2, h3, .grant-item, .program-item",
    "title": "h2, h3",
    "description": "p, .description",
    "budget": ".budget, .amount"
  },
  "filters": {
    "keywords": ["men's health", "mental health", "research"],
    "max_results": 10,
    "date_range": "2024-01-01 to 2024-12-31"
  }
}
```

**Response:**
```json
{
  "status": "success",
  "scraped_data": [
    {
      "title": "Men's Mental Health Research Grant",
      "description": "Funding for research into men's mental health awareness",
      "budget": "A$500,000",
      "deadline": "2024-12-31",
      "source": "https://www.health.vic.gov.au/about/our-grants"
    }
  ],
  "total_found": 15,
  "processed": 10,
  "errors": 0,
  "currency": "AUD",
  "spelling_standard": "UK"
}
```

## **📊 Error Codes & Responses**

### **HTTP Status Codes**

| Code | Description | Example |
|------|-------------|---------|
| **200** | Success | Request completed successfully |
| **201** | Created | New resource created successfully |
| **400** | Bad Request | Invalid request data |
| **401** | Unauthorized | Missing or invalid API key |
| **403** | Forbidden | Insufficient permissions |
| **404** | Not Found | Resource not found |
| **422** | Validation Error | Request data validation failed |
| **500** | Internal Server Error | Server processing error |

### **Error Response Format**

```json
{
  "detail": "Error description",
  "error_code": "VALIDATION_ERROR",
  "timestamp": "2025-08-08T11:08:08.392169",
  "request_id": "req_123456789",
  "currency": "AUD",
  "spelling_standard": "UK"
}
```

### **Common Error Codes**

| Error Code | Description | Solution |
|------------|-------------|----------|
| `VALIDATION_ERROR` | Request data doesn't meet requirements | Check request format and required fields |
| `AUTHENTICATION_ERROR` | Invalid or missing API key | Include valid API key in Authorization header |
| `RATE_LIMIT_EXCEEDED` | Too many requests | Wait before making additional requests |
| `RESOURCE_NOT_FOUND` | Requested resource doesn't exist | Check resource ID and permissions |
| `PROCESSING_ERROR` | Server error during processing | Retry request or contact support |

## **🔧 Rate Limiting**

- **Rate Limit**: 100 requests per minute per API key
- **Burst Limit**: 10 requests per second
- **Headers**: Rate limit information included in response headers

```bash
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1640995200
```

## **📝 Request/Response Standards**

### **Currency Format**
- **Display**: `A$1,234.56`
- **Input**: `1234.56` (number) or `"A$1,234.56"` (string)
- **Validation**: All amounts must be in AUD

### **Date Format**
- **ISO 8601**: `2025-08-08T11:08:08.392169`
- **Date Only**: `2025-08-08`
- **Timezone**: UTC (all timestamps)

### **UK Spelling Standards**
- `color` → `colour`
- `behavior` → `behaviour`
- `organization` → `organisation`
- `realize` → `realise`
- `analyze` → `analyse`

## **🧪 Testing Examples**

### **Test Health Endpoint**
```bash
curl -s https://movember-api.onrender.com/health/ | jq '.'
```

### **Test Grant Evaluation**
```bash
curl -s -X POST https://movember-api.onrender.com/grants/ \
  -H "Content-Type: application/json" \
  -d '{
    "grant_id": "test-001",
    "title": "Test Grant",
    "budget": 100000,
    "timeline_months": 12,
    "organisation": "Test Org",
    "contact_person": "Test Person",
    "email": "test@example.com",
    "description": "Test description"
  }' | jq '.'
```

### **Test Metrics Endpoint**
```bash
curl -s https://movember-api.onrender.com/metrics/ | jq '.'
```

## **📚 Additional Resources**

- **Swagger UI**: `https://movember-api.onrender.com/docs`
- **OpenAPI Schema**: `https://movember-api.onrender.com/openapi.json`
- **System Architecture**: See `docs/SYSTEM_ARCHITECTURE.md`
- **Troubleshooting**: See `DEBUGGING_GUIDE.md`

---

**Movember AI Rules System API v1.1** - Professional, compliant, and ready for production use. 🇦🇺 