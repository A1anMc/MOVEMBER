#!/bin/bash
# Movember AI Rules System - Production Deployment Script
# Deploys the complete system with UK spelling and AUD currency standards

set -e  # Exit on any error

# Configuration
PROJECT_NAME="movember-ai-rules"
ENVIRONMENT="production"
REGION="ap-southeast-2"  # Sydney region for AUD compliance
DOMAIN="movember-ai-rules.com"
GITHUB_REPO="https://github.com/A1anMc/MOVEMBER.git"

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
    command -v docker >/dev/null 2>&1 || { log_error "Docker is required but not installed. Aborting."; exit 1; }
    command -v docker-compose >/dev/null 2>&1 || { log_error "Docker Compose is required but not installed. Aborting."; exit 1; }
    command -v git >/dev/null 2>&1 || { log_error "Git is required but not installed. Aborting."; exit 1; }
    command -v python3 >/dev/null 2>&1 || { log_error "Python 3 is required but not installed. Aborting."; exit 1; }
    
    log_success "Prerequisites check passed"
}

# Create project structure
create_project_structure() {
    log_info "Creating project structure..."
    
    # Create directories
    mkdir -p /opt/movember-ai-rules/{api,bots,scrapers,database,logs,config,ssl}
    mkdir -p /opt/movember-ai-rules/backups
    mkdir -p /opt/movember-ai-rules/monitoring
    
    # Set permissions (macOS compatible)
    chmod 755 /opt/movember-ai-rules
    # Use current user instead of root:root for macOS compatibility
    chown -R $(whoami):staff /opt/movember-ai-rules
    
    log_success "Project structure created"
}

# Clone repository
clone_repository() {
    log_info "Cloning Movember AI Rules System repository..."
    
    cd /opt/movember-ai-rules
    
    if [ -d ".git" ]; then
        log_info "Repository already exists, pulling latest changes..."
        git pull origin main
    else
        git clone $GITHUB_REPO .
    fi
    
    log_success "Repository cloned/updated"
}

# Create Docker configuration
create_docker_config() {
    log_info "Creating Docker configuration..."
    
    cat > /opt/movember-ai-rules/docker-compose.yml << 'EOF'
version: '3.8'

services:
  # API Service
  api:
    build: ./api
    ports:
      - "8000:8000"
    environment:
      - ENVIRONMENT=production
      - DATABASE_URL=postgresql://movember:secure_password@db:5432/movember_ai
      - REDIS_URL=redis://redis:6379
      - LOG_LEVEL=INFO
    depends_on:
      - db
      - redis
    volumes:
      - ./logs:/app/logs
      - ./config:/app/config
    restart: unless-stopped
    networks:
      - movember-network

  # Database
  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=movember_ai
      - POSTGRES_USER=movember
      - POSTGRES_PASSWORD=secure_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./database/init:/docker-entrypoint-initdb.d
    ports:
      - "5432:5432"
    restart: unless-stopped
    networks:
      - movember-network

  # Redis Cache
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    restart: unless-stopped
    networks:
      - movember-network

  # Monitoring Bot
  monitoring-bot:
    build: ./bots
    environment:
      - ENVIRONMENT=production
      - DATABASE_URL=postgresql://movember:secure_password@db:5432/movember_ai
      - LOG_LEVEL=INFO
    depends_on:
      - db
    volumes:
      - ./logs:/app/logs
      - ./config:/app/config
    restart: unless-stopped
    networks:
      - movember-network

  # Data Scraper
  scraper:
    build: ./scrapers
    environment:
      - ENVIRONMENT=production
      - DATABASE_URL=postgresql://movember:secure_password@db:5432/movember_ai
      - LOG_LEVEL=INFO
    depends_on:
      - db
    volumes:
      - ./logs:/app/logs
      - ./config:/app/config
    restart: unless-stopped
    networks:
      - movember-network

  # Nginx Reverse Proxy
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
      - ./logs/nginx:/var/log/nginx
    depends_on:
      - api
    restart: unless-stopped
    networks:
      - movember-network

  # Monitoring Stack
  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    restart: unless-stopped
    networks:
      - movember-network

  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=secure_password
    volumes:
      - grafana_data:/var/lib/grafana
    restart: unless-stopped
    networks:
      - movember-network

volumes:
  postgres_data:
  redis_data:
  prometheus_data:
  grafana_data:

networks:
  movember-network:
    driver: bridge
EOF

    log_success "Docker configuration created"
}

# Create API Dockerfile
create_api_dockerfile() {
    log_info "Creating API Dockerfile..."
    
    cat > /opt/movember-ai-rules/api/Dockerfile << 'EOF'
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health/ || exit 1

# Start application
CMD ["uvicorn", "movember_api:app", "--host", "0.0.0.0", "--port", "8000"]
EOF

    log_success "API Dockerfile created"
}

# Create requirements.txt
create_requirements() {
    log_info "Creating requirements.txt..."
    
    cat > /opt/movember-ai-rules/requirements.txt << 'EOF'
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
redis==5.0.1
httpx==0.25.2
aiohttp==3.9.1
beautifulsoup4==4.12.2
pandas==2.1.4
pydantic==2.6.1
python-multipart>=0.0.7
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-dotenv==1.0.0
prometheus-client==0.19.0
structlog==23.2.0
EOF

    log_success "Requirements.txt created"
}

# Create Nginx configuration
create_nginx_config() {
    log_info "Creating Nginx configuration..."
    
    mkdir -p /opt/movember-ai-rules/nginx
    
    cat > /opt/movember-ai-rules/nginx/nginx.conf << 'EOF'
events {
    worker_connections 1024;
}

http {
    upstream api_backend {
        server api:8000;
    }

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;

    server {
        listen 80;
        server_name localhost;
        return 301 https://$server_name$request_uri;
    }

    server {
        listen 443 ssl http2;
        server_name localhost;

        # SSL configuration
        ssl_certificate /etc/nginx/ssl/cert.pem;
        ssl_certificate_key /etc/nginx/ssl/key.pem;
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
        ssl_prefer_server_ciphers off;

        # Security headers
        add_header X-Frame-Options DENY;
        add_header X-Content-Type-Options nosniff;
        add_header X-XSS-Protection "1; mode=block";
        add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

        # API routes
        location /api/ {
            limit_req zone=api burst=20 nodelay;
            proxy_pass http://api_backend/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # Health check
        location /health {
            proxy_pass http://api_backend/health/;
        }

        # Metrics
        location /metrics {
            proxy_pass http://api_backend/metrics/;
        }

        # Static files (if any)
        location /static/ {
            alias /var/www/static/;
            expires 1y;
            add_header Cache-Control "public, immutable";
        }
    }
}
EOF

    log_success "Nginx configuration created"
}

# Create SSL certificates (self-signed for development)
create_ssl_certificates() {
    log_info "Creating SSL certificates..."
    
    mkdir -p /opt/movember-ai-rules/ssl
    
    # Generate self-signed certificate
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
        -keyout /opt/movember-ai-rules/ssl/key.pem \
        -out /opt/movember-ai-rules/ssl/cert.pem \
        -subj "/C=AU/ST=NSW/L=Sydney/O=Movember/CN=movember-ai-rules.com"
    
    log_success "SSL certificates created"
}

# Create monitoring configuration
create_monitoring_config() {
    log_info "Creating monitoring configuration..."
    
    mkdir -p /opt/movember-ai-rules/monitoring
    
    cat > /opt/movember-ai-rules/monitoring/prometheus.yml << 'EOF'
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'movember-api'
    static_configs:
      - targets: ['api:8000']
    metrics_path: '/metrics/'
    scrape_interval: 5s

  - job_name: 'movember-monitoring-bot'
    static_configs:
      - targets: ['monitoring-bot:8001']
    metrics_path: '/metrics/'
    scrape_interval: 10s

  - job_name: 'movember-scraper'
    static_configs:
      - targets: ['scraper:8002']
    metrics_path: '/metrics/'
    scrape_interval: 30s
EOF

    log_success "Monitoring configuration created"
}

# Create systemd service files
create_systemd_services() {
    log_info "Creating service files..."
    
    # Check if we're on macOS
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # Create launchd service for macOS
        cat > ~/Library/LaunchAgents/com.movember.ai-rules.plist << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.movember.ai-rules</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/bin/docker-compose</string>
        <string>-f</string>
        <string>/opt/movember-ai-rules/docker-compose.yml</string>
        <string>up</string>
        <string>-d</string>
    </array>
    <key>WorkingDirectory</key>
    <string>/opt/movember-ai-rules</string>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/opt/movember-ai-rules/logs/launchd.log</string>
    <key>StandardErrorPath</key>
    <string>/opt/movember-ai-rules/logs/launchd-error.log</string>
</dict>
</plist>
EOF
        
        # Load the service
        launchctl load ~/Library/LaunchAgents/com.movember.ai-rules.plist
        
        log_success "Launchd service created for macOS"
    else
        # Create systemd service for Linux
        cat > /etc/systemd/system/movember-ai-rules.service << 'EOF'
[Unit]
Description=Movember AI Rules System
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/opt/movember-ai-rules
ExecStart=/usr/bin/docker-compose up -d
ExecStop=/usr/bin/docker-compose down
TimeoutStartSec=0

[Install]
WantedBy=multi-user.target
EOF

        systemctl daemon-reload
        systemctl enable movember-ai-rules.service
        
        log_success "Systemd service created for Linux"
    fi
}

# Create backup script
create_backup_script() {
    log_info "Creating backup script..."
    
    cat > /opt/movember-ai-rules/scripts/backup.sh << 'EOF'
#!/bin/bash

BACKUP_DIR="/opt/movember-ai-rules/backups"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_NAME="movember_backup_$DATE"

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Backup database
docker exec movember-ai-rules_db_1 pg_dump -U movember movember_ai > "$BACKUP_DIR/${BACKUP_NAME}_database.sql"

# Backup configuration files
tar -czf "$BACKUP_DIR/${BACKUP_NAME}_config.tar.gz" -C /opt/movember-ai-rules config/

# Backup logs
tar -czf "$BACKUP_DIR/${BACKUP_NAME}_logs.tar.gz" -C /opt/movember-ai-rules logs/

# Clean up old backups (keep last 7 days)
find "$BACKUP_DIR" -name "movember_backup_*" -mtime +7 -delete

echo "Backup completed: $BACKUP_NAME"
EOF

    chmod +x /opt/movember-ai-rules/scripts/backup.sh
    
    # Add to crontab for daily backups
    (crontab -l 2>/dev/null; echo "0 2 * * * /opt/movember-ai-rules/scripts/backup.sh") | crontab -
    
    log_success "Backup script created"
}

# Create health check script
create_health_check_script() {
    log_info "Creating health check script..."
    
    cat > /opt/movember-ai-rules/scripts/health-check.sh << 'EOF'
#!/bin/bash

# Health check for Movember AI Rules System

API_URL="https://localhost/api/health/"
GRAFANA_URL="http://localhost:3000"
PROMETHEUS_URL="http://localhost:9090"

# Check API health
if curl -f -s "$API_URL" > /dev/null; then
    echo "✅ API is healthy"
else
    echo "❌ API health check failed"
    exit 1
fi

# Check Grafana
if curl -f -s "$GRAFANA_URL" > /dev/null; then
    echo "✅ Grafana is healthy"
else
    echo "❌ Grafana health check failed"
fi

# Check Prometheus
if curl -f -s "$PROMETHEUS_URL" > /dev/null; then
    echo "✅ Prometheus is healthy"
else
    echo "❌ Prometheus health check failed"
fi

# Check Docker containers
if docker ps --filter "name=movember" --format "table {{.Names}}\t{{.Status}}" | grep -q "Up"; then
    echo "✅ All containers are running"
else
    echo "❌ Some containers are not running"
    docker ps --filter "name=movember"
fi
EOF

    chmod +x /opt/movember-ai-rules/scripts/health-check.sh
    
    log_success "Health check script created"
}

# Main deployment function
deploy_system() {
    log_info "Starting Movember AI Rules System deployment..."
    
    # Check if we're on macOS
    if [[ "$OSTYPE" == "darwin"* ]]; then
        log_info "Detected macOS - using macOS-compatible deployment"
    else
        # Check if running as root (Linux only)
        if [ "$EUID" -ne 0 ]; then
            log_error "Please run as root (use sudo)"
            exit 1
        fi
    fi
    
    # Execute deployment steps
    check_prerequisites
    create_project_structure
    clone_repository
    create_docker_config
    create_api_dockerfile
    create_requirements
    create_nginx_config
    create_ssl_certificates
    create_monitoring_config
    create_systemd_services
    create_backup_script
    create_health_check_script
    
    # Start the system
    log_info "Starting Movember AI Rules System..."
    cd /opt/movember-ai-rules
    docker-compose up -d
    
    # Wait for services to start
    log_info "Waiting for services to start..."
    sleep 30
    
    # Run health check
    log_info "Running health check..."
    /opt/movember-ai-rules/scripts/health-check.sh
    
    log_success "Deployment completed successfully!"
    log_info "System is now running at:"
    log_info "  - API: https://localhost/api/"
    log_info "  - Grafana: http://localhost:3000"
    log_info "  - Prometheus: http://localhost:9090"
    log_info "  - Health Check: https://localhost/health"
}

# Run deployment
deploy_system 