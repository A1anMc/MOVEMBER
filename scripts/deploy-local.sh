#!/bin/bash
# Movember AI Rules System - Local Development Deployment
# Deploys the system for local development without Docker

set -e  # Exit on any error

# Configuration
PROJECT_NAME="movember-ai-rules"
ENVIRONMENT="development"
PROJECT_DIR="$HOME/movember-ai-rules"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check prerequisites
check_prerequisites() {
    log_info "Checking prerequisites..."
    
    # Check if required tools are installed
    command -v python3 >/dev/null 2>&1 || { log_error "Python 3 is required but not installed. Aborting."; exit 1; }
    command -v pip3 >/dev/null 2>&1 || { log_error "pip3 is required but not installed. Aborting."; exit 1; }
    command -v git >/dev/null 2>&1 || { log_error "Git is required but not installed. Aborting."; exit 1; }
    
    log_success "Prerequisites check passed"
}

# Create project structure
create_project_structure() {
    log_info "Creating project structure..."
    
    # Create directories
    mkdir -p "$PROJECT_DIR"/{api,bots,scrapers,database,logs,config,backups}
    
    log_success "Project structure created"
}

# Clone repository
clone_repository() {
    log_info "Cloning Movember AI Rules System repository..."
    
    cd "$PROJECT_DIR"
    
    if [ -d ".git" ]; then
        log_info "Repository already exists, pulling latest changes..."
        git pull origin main
    else
        git clone https://github.com/A1anMc/MOVEMBER.git .
    fi
    
    log_success "Repository cloned/updated"
}

# Create virtual environment
create_virtual_environment() {
    log_info "Creating Python virtual environment..."
    
    cd "$PROJECT_DIR"
    
    # Create virtual environment
    python3 -m venv venv
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Upgrade pip
    pip install --upgrade pip
    
    log_success "Virtual environment created"
}

# Install dependencies
install_dependencies() {
    log_info "Installing Python dependencies..."
    
    cd "$PROJECT_DIR"
    source venv/bin/activate
    
    # Install requirements
    pip install -r requirements.txt
    
    log_success "Dependencies installed"
}

# Create configuration files
create_config_files() {
    log_info "Creating configuration files..."
    
    cd "$PROJECT_DIR"
    
    # Create .env file
    cat > .env << 'EOF'
ENVIRONMENT=development
DATABASE_URL=sqlite:///movember_ai.db
REDIS_URL=redis://localhost:6379
LOG_LEVEL=INFO
SECRET_KEY=your-secret-key-here
DEBUG=True
EOF
    
    # Create database
    python3 -c "
import sqlite3
conn = sqlite3.connect('movember_ai.db')
cursor = conn.cursor()

# Create tables
cursor.execute('''
CREATE TABLE IF NOT EXISTS grants (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    grant_id TEXT UNIQUE NOT NULL,
    title TEXT,
    budget REAL,
    currency TEXT DEFAULT 'AUD',
    timeline_months INTEGER,
    status TEXT,
    organisation TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_json TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS impact_reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    report_id TEXT UNIQUE NOT NULL,
    title TEXT,
    type TEXT,
    frameworks TEXT,
    status TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_json TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS system_health (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    system_status TEXT,
    uptime_percentage REAL,
    active_rules INTEGER,
    total_executions INTEGER,
    success_rate REAL,
    average_response_time REAL,
    error_count INTEGER,
    memory_usage REAL,
    cpu_usage REAL,
    disk_usage REAL,
    active_connections INTEGER,
    queue_size INTEGER,
    last_backup TIMESTAMP,
    security_status TEXT,
    compliance_status TEXT,
    uk_spelling_consistency REAL,
    aud_currency_compliance REAL
)
''')

conn.commit()
conn.close()
print('Database created successfully')
"
    
    log_success "Configuration files created"
}

# Create startup scripts
create_startup_scripts() {
    log_info "Creating startup scripts..."
    
    cd "$PROJECT_DIR"
    
    # Create API startup script
    cat > start_api.sh << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
source venv/bin/activate
python -m uvicorn api.movember_api:app --host 0.0.0.0 --port 8000 --reload
EOF
    
    # Create monitoring bot startup script
    cat > start_monitoring.sh << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
source venv/bin/activate
python -c "
import asyncio
from bots.movember_monitoring_bot import MovemberMonitoringBot

async def main():
    bot = MovemberMonitoringBot()
    await bot.start_monitoring()

if __name__ == '__main__':
    asyncio.run(main())
"
EOF
    
    # Create scraper startup script
    cat > start_scraper.sh << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
source venv/bin/activate
python -c "
import asyncio
from scrapers.movember_data_scraper import MovemberDataScraper

async def main():
    async with MovemberDataScraper() as scraper:
        # Example scraping
        config = scraper.create_grants_scraping_config('https://example.com')
        await scraper.scrape_grants_data(config)

if __name__ == '__main__':
    asyncio.run(main())
"
EOF
    
    # Make scripts executable
    chmod +x start_api.sh start_monitoring.sh start_scraper.sh
    
    log_success "Startup scripts created"
}

# Create health check script
create_health_check_script() {
    log_info "Creating health check script..."
    
    cd "$PROJECT_DIR"
    
    cat > health_check.sh << 'EOF'
#!/bin/bash

# Health check for Movember AI Rules System

API_URL="http://localhost:8000/health/"
LOG_DIR="$HOME/movember-ai-rules/logs"

echo "🏥 Movember AI Rules System Health Check"
echo "=========================================="

# Check if API is running
if curl -f -s "$API_URL" > /dev/null; then
    echo "✅ API is healthy"
else
    echo "❌ API health check failed"
    echo "   Try starting the API: ./start_api.sh"
fi

# Check if database exists
if [ -f "movember_ai.db" ]; then
    echo "✅ Database exists"
else
    echo "❌ Database not found"
fi

# Check if virtual environment exists
if [ -d "venv" ]; then
    echo "✅ Virtual environment exists"
else
    echo "❌ Virtual environment not found"
fi

# Check log files
if [ -d "$LOG_DIR" ]; then
    echo "✅ Log directory exists"
else
    echo "❌ Log directory not found"
fi

echo "=========================================="
echo "🌐 API: http://localhost:8000/"
echo "📋 Health: http://localhost:8000/health/"
echo "📊 Metrics: http://localhost:8000/metrics/"
echo "=========================================="
EOF
    
    chmod +x health_check.sh
    
    log_success "Health check script created"
}

# Display system information
display_system_info() {
    log_info "System Information:"
    echo "=========================================="
    echo "🌐 API Endpoint: http://localhost:8000/"
    echo "🏥 Health Check: http://localhost:8000/health/"
    echo "📋 Metrics: http://localhost:8000/metrics/"
    echo "=========================================="
    echo ""
    echo "📁 Project Directory: $PROJECT_DIR"
    echo "🐍 Virtual Environment: $PROJECT_DIR/venv"
    echo "💾 Database: $PROJECT_DIR/movember_ai.db"
    echo "📁 Logs: $PROJECT_DIR/logs"
    echo ""
    echo "🛠️  Management Commands:"
    echo "  - Start API: cd $PROJECT_DIR && ./start_api.sh"
    echo "  - Start Monitoring: cd $PROJECT_DIR && ./start_monitoring.sh"
    echo "  - Start Scraper: cd $PROJECT_DIR && ./start_scraper.sh"
    echo "  - Health Check: cd $PROJECT_DIR && ./health_check.sh"
    echo ""
}

# Main deployment function
deploy_system() {
    log_info "Starting Movember AI Rules System local deployment..."
    
    # Execute deployment steps
    check_prerequisites
    create_project_structure
    clone_repository
    create_virtual_environment
    install_dependencies
    create_config_files
    create_startup_scripts
    create_health_check_script
    
    # Display system information
    display_system_info
    
    log_success "Local deployment completed successfully!"
    log_info "To start the system:"
    log_info "  cd $PROJECT_DIR"
    log_info "  ./start_api.sh"
    log_info ""
    log_info "System will be available at:"
    log_info "  - API: http://localhost:8000/"
    log_info "  - Health: http://localhost:8000/health/"
    log_info "  - Metrics: http://localhost:8000/metrics/"
}

# Run deployment
deploy_system 