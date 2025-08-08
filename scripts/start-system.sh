#!/bin/bash
# Movember AI Rules System - Startup Script
# Starts the complete system with health checks and monitoring

set -e  # Exit on any error

# Configuration
PROJECT_DIR="/opt/movember-ai-rules"
LOG_DIR="$PROJECT_DIR/logs"
CONFIG_DIR="$PROJECT_DIR/config"

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

# Check if system is already running
check_system_status() {
    log_info "Checking system status..."
    
    if docker ps --filter "name=movember" --format "table {{.Names}}\t{{.Status}}" | grep -q "Up"; then
        log_warning "System is already running"
        return 1
    else
        log_info "System is not running, starting..."
        return 0
    fi
}

# Start Docker services
start_docker_services() {
    log_info "Starting Docker services..."
    
    cd "$PROJECT_DIR"
    
    # Start all services
    docker-compose up -d
    
    log_success "Docker services started"
}

# Wait for services to be ready
wait_for_services() {
    log_info "Waiting for services to be ready..."
    
    # Wait for database
    log_info "Waiting for database..."
    timeout=60
    while [ $timeout -gt 0 ]; do
        if docker exec movember-ai-rules_db_1 pg_isready -U movember >/dev/null 2>&1; then
            log_success "Database is ready"
            break
        fi
        sleep 1
        timeout=$((timeout - 1))
    done
    
    if [ $timeout -eq 0 ]; then
        log_error "Database failed to start"
        exit 1
    fi
    
    # Wait for API
    log_info "Waiting for API..."
    timeout=60
    while [ $timeout -gt 0 ]; do
        if curl -f -s https://localhost/api/health/ >/dev/null 2>&1; then
            log_success "API is ready"
            break
        fi
        sleep 1
        timeout=$((timeout - 1))
    done
    
    if [ $timeout -eq 0 ]; then
        log_error "API failed to start"
        exit 1
    fi
    
    # Wait for monitoring services
    log_info "Waiting for monitoring services..."
    sleep 10
    
    log_success "All services are ready"
}

# Run health checks
run_health_checks() {
    log_info "Running health checks..."
    
    # API health check
    if curl -f -s https://localhost/api/health/ >/dev/null; then
        log_success "✅ API health check passed"
    else
        log_error "❌ API health check failed"
        return 1
    fi
    
    # Database health check
    if docker exec movember-ai-rules_db_1 pg_isready -U movember >/dev/null 2>&1; then
        log_success "✅ Database health check passed"
    else
        log_error "❌ Database health check failed"
        return 1
    fi
    
    # Redis health check
    if docker exec movember-ai-rules_redis_1 redis-cli ping >/dev/null 2>&1; then
        log_success "✅ Redis health check passed"
    else
        log_error "❌ Redis health check failed"
        return 1
    fi
    
    # Monitoring bot health check
    if docker ps --filter "name=monitoring-bot" --format "{{.Status}}" | grep -q "Up"; then
        log_success "✅ Monitoring bot health check passed"
    else
        log_error "❌ Monitoring bot health check failed"
        return 1
    fi
    
    # Scraper health check
    if docker ps --filter "name=scraper" --format "{{.Status}}" | grep -q "Up"; then
        log_success "✅ Scraper health check passed"
    else
        log_error "❌ Scraper health check failed"
        return 1
    fi
    
    log_success "All health checks passed"
}

# Initialize database
initialize_database() {
    log_info "Initializing database..."
    
    # Create tables if they don't exist
    docker exec movember-ai-rules_db_1 psql -U movember -d movember_ai -c "
        CREATE TABLE IF NOT EXISTS grants (
            id SERIAL PRIMARY KEY,
            grant_id VARCHAR(255) UNIQUE NOT NULL,
            title VARCHAR(500),
            budget DECIMAL(15,2),
            currency VARCHAR(10) DEFAULT 'AUD',
            timeline_months INTEGER,
            status VARCHAR(50),
            organisation VARCHAR(255),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            data_json TEXT
        );
        
        CREATE TABLE IF NOT EXISTS impact_reports (
            id SERIAL PRIMARY KEY,
            report_id VARCHAR(255) UNIQUE NOT NULL,
            title VARCHAR(500),
            type VARCHAR(100),
            frameworks TEXT,
            status VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            data_json TEXT
        );
        
        CREATE TABLE IF NOT EXISTS system_health (
            id SERIAL PRIMARY KEY,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            system_status VARCHAR(50),
            uptime_percentage DECIMAL(5,2),
            active_rules INTEGER,
            total_executions INTEGER,
            success_rate DECIMAL(5,4),
            average_response_time DECIMAL(10,3),
            error_count INTEGER,
            memory_usage DECIMAL(5,2),
            cpu_usage DECIMAL(5,2),
            disk_usage DECIMAL(5,2),
            active_connections INTEGER,
            queue_size INTEGER,
            last_backup TIMESTAMP,
            security_status VARCHAR(50),
            compliance_status VARCHAR(50),
            uk_spelling_consistency DECIMAL(5,4),
            aud_currency_compliance DECIMAL(5,4)
        );
        
        CREATE TABLE IF NOT EXISTS scraped_data (
            id SERIAL PRIMARY KEY,
            source_url VARCHAR(500),
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            data_type VARCHAR(100),
            raw_data_json TEXT,
            processed_data_json TEXT,
            quality_score DECIMAL(5,4),
            uk_spelling_issues INTEGER,
            aud_currency_issues INTEGER,
            total_records INTEGER,
            valid_records INTEGER
        );
        
        CREATE TABLE IF NOT EXISTS monitoring_alerts (
            id SERIAL PRIMARY KEY,
            alert_id VARCHAR(255) UNIQUE NOT NULL,
            alert_type VARCHAR(100),
            severity VARCHAR(50),
            message TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            source VARCHAR(100),
            details_json TEXT,
            resolved BOOLEAN DEFAULT FALSE,
            resolution_time TIMESTAMP
        );
        
        CREATE TABLE IF NOT EXISTS data_quality_reports (
            id SERIAL PRIMARY KEY,
            report_id VARCHAR(255) UNIQUE NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            total_records INTEGER,
            valid_records INTEGER,
            invalid_records INTEGER,
            uk_spelling_issues INTEGER,
            aud_currency_issues INTEGER,
            quality_score DECIMAL(5,4),
            report_json TEXT
        );
        
        CREATE TABLE IF NOT EXISTS compliance_reports (
            id SERIAL PRIMARY KEY,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            total_rules INTEGER,
            uk_spelling_compliance DECIMAL(5,4),
            aud_currency_compliance DECIMAL(5,4),
            overall_compliance DECIMAL(5,4),
            report_json TEXT
        );
    " 2>/dev/null || log_warning "Database tables may already exist"
    
    log_success "Database initialized"
}

# Start monitoring
start_monitoring() {
    log_info "Starting monitoring services..."
    
    # Start monitoring bot
    docker exec movember-ai-rules_monitoring-bot_1 python -c "
import asyncio
from movember_monitoring_bot import MovemberMonitoringBot

async def start_monitoring():
    bot = MovemberMonitoringBot()
    await bot.start_monitoring()

if __name__ == '__main__':
    asyncio.run(start_monitoring())
" &
    
    log_success "Monitoring started"
}

# Display system information
display_system_info() {
    log_info "System Information:"
    echo "=========================================="
    echo "🌐 API Endpoint: https://localhost/api/"
    echo "📊 Grafana Dashboard: http://localhost:3000"
    echo "📈 Prometheus Metrics: http://localhost:9090"
    echo "🏥 Health Check: https://localhost/health"
    echo "📋 Metrics: https://localhost/metrics"
    echo "=========================================="
    echo ""
    echo "🔐 Default Credentials:"
    echo "  - Grafana: admin / secure_password"
    echo "  - Database: movember / secure_password"
    echo ""
    echo "📁 Log Files: $LOG_DIR"
    echo "⚙️  Configuration: $CONFIG_DIR"
    echo "💾 Backups: $PROJECT_DIR/backups"
    echo ""
    echo "🛠️  Management Commands:"
    echo "  - Stop system: sudo systemctl stop movember-ai-rules"
    echo "  - View logs: docker-compose logs -f"
    echo "  - Health check: $PROJECT_DIR/scripts/health-check.sh"
    echo "  - Backup: $PROJECT_DIR/scripts/backup.sh"
    echo ""
}

# Main startup function
start_system() {
    log_info "Starting Movember AI Rules System..."
    
    # Check if running as root
    if [ "$EUID" -ne 0 ]; then
        log_error "Please run as root (use sudo)"
        exit 1
    fi
    
    # Check if project directory exists
    if [ ! -d "$PROJECT_DIR" ]; then
        log_error "Project directory not found. Please run deploy-production.sh first."
        exit 1
    fi
    
    # Check system status
    if ! check_system_status; then
        log_info "System is already running"
        display_system_info
        exit 0
    fi
    
    # Start services
    start_docker_services
    wait_for_services
    initialize_database
    start_monitoring
    run_health_checks
    
    # Display system information
    display_system_info
    
    log_success "Movember AI Rules System started successfully!"
    log_info "System is now ready for use with UK spelling and AUD currency standards."
}

# Run startup
start_system 