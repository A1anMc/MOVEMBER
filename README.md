# Movember AI Rules System v1.1

A comprehensive, production-ready rules engine for the Movember Impact Intelligence Agent with UK spelling and AUD currency standards throughout.

## 🚀 **Quick Start**

### **1. Deploy to Production**
```bash
# Clone the repository
git clone https://github.com/A1anMc/MOVEMBER.git
cd MOVEMBER

# Run production deployment (requires sudo)
sudo ./scripts/deploy-production.sh
```

### **2. Start the System**
```bash
# Start all services
sudo ./scripts/start-system.sh
```

### **3. Access the System**
- **API**: https://localhost/api/
- **Grafana Dashboard**: http://localhost:3000
- **Prometheus Metrics**: http://localhost:9090
- **Health Check**: https://localhost/health

## 🏗️ **System Architecture**

### **Core Components**
- **Rules Engine**: AI behaviour, grant lifecycle, impact reporting
- **API Layer**: RESTful endpoints with FastAPI
- **Monitoring Bot**: Automated health checks and alerts
- **Data Scraper**: External data collection with validation
- **Database**: PostgreSQL with Redis caching
- **Monitoring**: Prometheus + Grafana stack

### **Standards Compliance**
- ✅ **UK Spelling** throughout all text
- ✅ **AUD Currency** formatting (A$1,234.56)
- ✅ **Professional tone** for stakeholder communications
- ✅ **Data integrity** and source validation
- ✅ **Mission alignment** with Movember's goals

## 📋 **Features**

### **AI Behaviour Rules**
- Professional tone enforcement
- Uncertainty handling with transparency
- Data integrity validation
- Mission alignment checks
- Stakeholder role adaptation

### **Grant Lifecycle Management**
- Application completeness validation
- Budget realism checks (AUD currency)
- Impact metrics linkage
- SDG alignment requirements
- Sustainability plan validation

### **Impact Reporting**
- Framework compliance (ToC, CEMP, SDG)
- Output-outcome mapping validation
- Data visualisation requirements
- Attribution vs contribution clarity
- Stakeholder appropriateness checks

### **Context Validation**
- Movember project scope enforcement
- Data source authority validation
- Stakeholder permission checks
- Geographic scope validation
- Temporal context validation

### **Weekly Refactoring**
- Unused rule identification
- Duplicate logic detection
- Performance optimisation
- UK spelling consistency checks
- AUD currency compliance validation

## 🔧 **API Endpoints**

### **Grant Management**
```bash
# Submit grant application
POST /api/grants/
{
  "grant_id": "GRANT-2024-001",
  "title": "Men's Health Research Initiative",
  "budget": 500000,
  "currency": "AUD",
  "timeline_months": 24,
  "organisation": "University of Sydney"
}

# Get grant details
GET /api/grants/{grant_id}
```

### **Impact Reporting**
```bash
# Submit impact report
POST /api/reports/
{
  "report_id": "IMP-2024-001",
  "title": "Men's Health Impact Assessment",
  "type": "impact",
  "frameworks": ["ToC", "SDG"],
  "outputs": [{"name": "Health Screenings", "count": 1500}],
  "outcomes": [{"name": "Increased Awareness", "metric": "85% improvement"}]
}

# Get report details
GET /api/reports/{report_id}
```

### **External Data Collection**
```bash
# Collect external data
POST /api/external-data/
{
  "source_type": "grants_database",
  "endpoint": "https://api.example.com/grants",
  "parameters": {"category": "health_research"},
  "data_format": "json"
}
```

### **System Monitoring**
```bash
# Get system health
GET /api/health/

# Get system metrics
GET /api/metrics/
```

## 🛠️ **Management Commands**

### **System Control**
```bash
# Start system
sudo ./scripts/start-system.sh

# Stop system
sudo systemctl stop movember-ai-rules

# View logs
docker-compose logs -f

# Health check
./scripts/health-check.sh

# Backup system
./scripts/backup.sh
```

### **Monitoring**
```bash
# Check system status
docker ps --filter "name=movember"

# View Grafana dashboard
open http://localhost:3000

# View Prometheus metrics
open http://localhost:9090
```

## 📊 **Quality Standards**

### **UK Spelling Compliance**
- `color` → `colour`
- `behavior` → `behaviour`
- `organization` → `organisation`
- `realize` → `realise`
- `analyze` → `analyse`
- And 15+ more conversions

### **AUD Currency Formatting**
- Display: `A$1,234.56`
- Validation: Ensures all currency is AUD
- Conversion: Automatic from other currencies
- Formatting: UK number formatting (commas as thousands separators)

### **Data Quality Metrics**
- **UK spelling consistency**: >98%
- **AUD currency compliance**: >99%
- **Data completeness**: >95%
- **Source validation**: 100%

## 🔒 **Security Features**

### **Authentication & Authorization**
- JWT token authentication
- Role-based access control (RBAC)
- API rate limiting (10 requests/second)
- SSL/TLS encryption

### **Data Protection**
- Database encryption at rest
- Secure API communications
- Audit logging for all operations
- GDPR compliance measures

### **Monitoring & Alerting**
- Real-time health monitoring
- Automated alert generation
- Performance metrics tracking
- Security incident detection

## 📈 **Performance Metrics**

### **System Performance**
- **Uptime**: >99.9%
- **Response time**: <500ms average
- **Throughput**: 1000+ requests/second
- **Error rate**: <0.1%

### **Quality Metrics**
- **Rule execution success**: >95%
- **Data validation accuracy**: >98%
- **UK spelling compliance**: >98%
- **AUD currency compliance**: >99%

## 🚀 **Deployment Options**

### **Local Development**
```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
python -m pytest tests/

# Start development server
python -m uvicorn api.movember_api:app --reload
```

### **Production Deployment**
```bash
# Full production deployment
sudo ./scripts/deploy-production.sh

# Start production system
sudo ./scripts/start-system.sh
```

### **Docker Deployment**
```bash
# Build and start with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## 📚 **Documentation**

### **API Documentation**
- **Swagger UI**: https://localhost/api/docs
- **ReDoc**: https://localhost/api/redoc
- **OpenAPI Schema**: https://localhost/api/openapi.json

### **System Documentation**
- **Architecture**: `docs/SYSTEM_ARCHITECTURE.md`
- **Requirements**: `docs/SYSTEM_REQUIREMENTS.md`
- **Roadmap**: `docs/MOVEMBER_AI_ROADMAP.md`

## 🧪 **Testing**

### **Run All Tests**
```bash
# Unit tests
python -m pytest tests/unit/

# Integration tests
python -m pytest tests/integration/

# System tests
python -m pytest tests/system/

# All tests with coverage
python -m pytest tests/ --cov=rules --cov-report=html
```

### **Test Categories**
- **Unit tests**: Individual component testing
- **Integration tests**: Cross-system workflows
- **Performance tests**: Load and stress testing
- **Security tests**: Vulnerability and penetration testing
- **Compliance tests**: UK spelling and AUD currency validation

## 🔧 **Configuration**

### **Environment Variables**
```bash
# Database
DATABASE_URL=postgresql://movember:secure_password@localhost:5432/movember_ai

# Redis
REDIS_URL=redis://localhost:6379

# Logging
LOG_LEVEL=INFO

# Environment
ENVIRONMENT=production
```

### **Custom Configuration**
- **Rules engine**: Modify rules in `rules/domains/movember_ai/`
- **API endpoints**: Extend in `api/movember_api.py`
- **Monitoring**: Configure in `bots/movember_monitoring_bot.py`
- **Scraping**: Customize in `scrapers/movember_data_scraper.py`

## 📞 **Support**

### **Getting Help**
- **Documentation**: Check the docs/ directory
- **Issues**: Report on GitHub Issues
- **Logs**: Check `/opt/movember-ai-rules/logs/`
- **Health**: Run `./scripts/health-check.sh`

### **Troubleshooting**
```bash
# Check system status
docker ps --filter "name=movember"

# View recent logs
docker-compose logs --tail=100

# Restart services
docker-compose restart

# Reset database (WARNING: Data loss)
docker-compose down -v && docker-compose up -d
```

## 📄 **License**

MIT License - See LICENSE file for details.

## 🤝 **Contributing**

1. Fork the repository
2. Create a feature branch
3. Make changes with UK spelling and AUD currency
4. Add tests for new functionality
5. Submit a pull request

## 🎯 **Success Metrics**

- **System uptime**: >99.9%
- **Data quality score**: >95%
- **UK spelling compliance**: >98%
- **AUD currency compliance**: >99%
- **User satisfaction**: >90%
- **Performance**: <500ms average response time

---

**Movember AI Rules System v1.1** - Transforming impact intelligence with professional standards and Australian compliance. 🇦🇺 