# 🔧 **Movember AI Rules System - Troubleshooting Guide**

## **📋 Overview**

This guide covers common issues, their causes, and step-by-step solutions for the Movember AI Rules System. All solutions follow UK spelling and AUD currency standards.

## **🚨 Critical Issues**

### **1. API Not Responding**

**Symptoms:**
- `502 Bad Gateway` errors
- `Connection refused` messages
- Health endpoint returns errors

**Causes:**
- Render service sleeping (free tier)
- Database connection issues
- Application crashes

**Solutions:**

#### **Check Service Status**
```bash
# Check API health
curl -s https://movember-api.onrender.com/health/ | jq '.'

# Check if service is awake
curl -s -I https://movember-api.onrender.com/health/
```

#### **Wake Up Service**
```bash
# Make a request to wake up the service
curl -s https://movember-api.onrender.com/health/ > /dev/null

# Wait 30 seconds for full startup
sleep 30

# Test again
curl -s https://movember-api.onrender.com/health/ | jq '.'
```

#### **Check Render Dashboard**
1. Go to [Render Dashboard](https://dashboard.render.com)
2. Navigate to `movember-api` service
3. Check logs for errors
4. Restart service if needed

### **2. Database Connection Errors**

**Symptoms:**
- `psycopg2.OperationalError: connection to server failed`
- `sqlalchemy.exc.OperationalError`
- Database timeout errors

**Causes:**
- PostgreSQL service down
- Connection pool exhausted
- Network connectivity issues

**Solutions:**

#### **Check Database Status**
```bash
# Test database connection
python -c "
import os
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

try:
    engine = create_engine(os.getenv('DATABASE_URL'))
    with engine.connect() as conn:
        result = conn.execute('SELECT 1')
        print('✅ Database connection successful')
except OperationalError as e:
    print(f'❌ Database connection failed: {e}')
"
```

#### **Reset Database Connection**
```python
# In your application code
import time
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

# Configure connection pool
engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,
    pool_recycle=3600
)
```

### **3. Rules Engine Errors**

**Symptoms:**
- `AttributeError: 'NoneType' object has no attribute`
- `TypeError: '<' not supported between instances`
- Rule evaluation failures

**Causes:**
- Missing data in context
- Type mismatches
- Circular import issues

**Solutions:**

#### **Check Rule Context**
```python
# Add debugging to rule evaluation
import logging

logger = logging.getLogger(__name__)

def evaluate_rule(context):
    try:
        # Log context for debugging
        logger.info(f"Evaluating rule with context: {context}")
        
        # Add null checks
        if not context or not hasattr(context, 'data'):
            logger.warning("Context is missing or invalid")
            return {"success": False, "error": "Invalid context"}
            
        # Continue with evaluation
        result = perform_evaluation(context)
        return result
        
    except Exception as e:
        logger.error(f"Rule evaluation failed: {e}")
        return {"success": False, "error": str(e)}
```

#### **Fix Type Issues**
```python
# Ensure proper type handling
from typing import Union, Optional

def safe_compare(a: Union[int, float, None], b: Union[int, float, None]) -> bool:
    """Safely compare values that might be None."""
    if a is None or b is None:
        return False
    return a < b

# Use in rules
if safe_compare(context.budget, 100000):
    # Process condition
    pass
```

## **⚠️ Medium Priority Issues**

### **4. Frontend Build Failures**

**Symptoms:**
- `npm run build` fails
- TypeScript compilation errors
- Missing dependencies

**Solutions:**

#### **Clean and Reinstall**
```bash
# Navigate to frontend directory
cd frontend

# Clean node_modules
rm -rf node_modules package-lock.json

# Reinstall dependencies
npm install

# Try build again
npm run build
```

#### **Fix TypeScript Errors**
```bash
# Check TypeScript errors
npx tsc --noEmit

# Fix common issues
# 1. Add missing type definitions
npm install --save-dev @types/react @types/react-dom

# 2. Update tsconfig.json
# Add "skipLibCheck": true to compilerOptions
```

#### **Check Environment Variables**
```bash
# Ensure environment variables are set
echo $VITE_API_URL

# Create .env.local if missing
cat > .env.local << EOF
VITE_API_URL=https://movember-api.onrender.com
VITE_APP_NAME=Movember AI Rules System
EOF
```

### **5. Test Failures**

**Symptoms:**
- `pytest` fails with errors
- Integration tests timeout
- Unit tests fail

**Solutions:**

#### **Run Tests with Verbose Output**
```bash
# Run tests with detailed output
python -m pytest tests/ -v --tb=long

# Run specific test file
python -m pytest tests/test_integration_systems.py -v

# Run with coverage
python -m pytest tests/ --cov=rules --cov-report=html
```

#### **Fix Common Test Issues**
```python
# Add proper async handling
import pytest
import pytest_asyncio

@pytest_asyncio.fixture
async def test_context():
    """Create test context."""
    return {
        "grant_id": "test-001",
        "title": "Test Grant",
        "budget": 100000,
        "currency": "AUD"
    }

@pytest.mark.asyncio
async def test_grant_evaluation(test_context):
    """Test grant evaluation."""
    from rules.domains.movember_ai import MovemberAIRulesEngine
    
    engine = MovemberAIRulesEngine()
    result = await engine.evaluate_context(test_context)
    
    assert result is not None
    assert "evaluation_results" in result
```

### **6. Code Quality Issues**

**Symptoms:**
- Flake8 errors
- Linting failures
- Code formatting issues

**Solutions:**

#### **Run Code Quality Fixes**
```bash
# Run automated fixes
python fix_code_quality.py

# Check remaining issues
python -m flake8 rules/ api/ tests/ --count --select=E9,F63,F7,F82 --show-source --statistics
```

#### **Fix Common Issues**
```python
# 1. Add missing imports
import logging
from typing import Optional, Dict, Any

# 2. Fix undefined variables
logger = logging.getLogger(__name__)

# 3. Add proper type hints
def process_data(data: Dict[str, Any]) -> Optional[str]:
    """Process data with proper typing."""
    if not data:
        return None
    return str(data.get('value', ''))
```

## **📊 Performance Issues**

### **7. Slow API Responses**

**Symptoms:**
- Response times > 5 seconds
- Timeout errors
- High memory usage

**Solutions:**

#### **Check Performance Metrics**
```bash
# Get current metrics
curl -s https://movember-api.onrender.com/metrics/ | jq '.'

# Check response time
time curl -s https://movember-api.onrender.com/health/
```

#### **Optimize Database Queries**
```python
# Add database indexing
from sqlalchemy import Index

# Create indexes for common queries
Index('idx_grants_status', 'grants.status')
Index('idx_grants_created_at', 'grants.created_at')
Index('idx_evaluations_grant_id', 'evaluations.grant_id')
```

#### **Implement Caching**
```python
import redis
from functools import wraps

redis_client = redis.Redis.from_url(os.getenv('REDIS_URL'))

def cache_result(ttl=300):
    """Cache function results."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            cache_key = f"{func.__name__}:{hash(str(args) + str(kwargs))}"
            
            # Try to get from cache
            cached = redis_client.get(cache_key)
            if cached:
                return json.loads(cached)
            
            # Execute function
            result = func(*args, **kwargs)
            
            # Cache result
            redis_client.setex(cache_key, ttl, json.dumps(result))
            return result
        return wrapper
    return decorator
```

### **8. Memory Leaks**

**Symptoms:**
- Increasing memory usage
- Application crashes
- Slow performance over time

**Solutions:**

#### **Monitor Memory Usage**
```python
import psutil
import gc

def monitor_memory():
    """Monitor memory usage."""
    process = psutil.Process()
    memory_info = process.memory_info()
    
    print(f"Memory usage: {memory_info.rss / 1024 / 1024:.2f} MB")
    
    # Force garbage collection
    gc.collect()
    
    return memory_info.rss / 1024 / 1024
```

#### **Fix Common Memory Issues**
```python
# 1. Close database connections
def get_db_session():
    """Get database session with proper cleanup."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

# 2. Clear large objects
def process_large_data(data):
    """Process large data with memory management."""
    for chunk in data_chunks(data, 1000):
        process_chunk(chunk)
        del chunk  # Explicitly delete processed data
        gc.collect()  # Force garbage collection
```

## **🔐 Security Issues**

### **9. Authentication Errors**

**Symptoms:**
- `401 Unauthorized` errors
- `403 Forbidden` responses
- Invalid API key errors

**Solutions:**

#### **Check API Key**
```bash
# Test with API key
curl -H "Authorization: Bearer YOUR_API_KEY" \
     https://movember-api.onrender.com/health/

# Check if key is valid
curl -H "Authorization: Bearer invalid_key" \
     https://movember-api.onrender.com/health/
```

#### **Regenerate API Key**
```python
import secrets

# Generate new API key
new_api_key = secrets.token_urlsafe(32)
print(f"New API key: {new_api_key}")

# Update in environment
os.environ['API_KEY'] = new_api_key
```

### **10. Data Validation Errors**

**Symptoms:**
- `422 Validation Error` responses
- Invalid data format errors
- Currency validation failures

**Solutions:**

#### **Validate Request Data**
```python
from pydantic import BaseModel, validator
from typing import Optional

class GrantRequest(BaseModel):
    grant_id: str
    title: str
    budget: float
    currency: str = "AUD"
    
    @validator('currency')
    def validate_currency(cls, v):
        if v != "AUD":
            raise ValueError("Currency must be AUD")
        return v
    
    @validator('budget')
    def validate_budget(cls, v):
        if v <= 0:
            raise ValueError("Budget must be positive")
        return v
```

## **🌐 Network Issues**

### **11. CORS Errors**

**Symptoms:**
- `CORS policy` errors in browser
- Cross-origin request failures
- Frontend can't connect to API

**Solutions:**

#### **Configure CORS in API**
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://movember-frontend.onrender.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### **12. Rate Limiting**

**Symptoms:**
- `429 Too Many Requests` errors
- Rate limit exceeded messages
- Request throttling

**Solutions:**

#### **Implement Rate Limiting**
```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.post("/grants/")
@limiter.limit("10/minute")
async def evaluate_grant(request: Request):
    # Your endpoint logic
    pass
```

## **📝 Logging and Debugging**

### **13. Enable Debug Logging**

```python
import logging

# Configure detailed logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('debug.log'),
        logging.StreamHandler()
    ]
)

# Log specific operations
logger = logging.getLogger(__name__)
logger.debug("Processing grant evaluation")
logger.info("Grant evaluation completed")
logger.error("Evaluation failed", exc_info=True)
```

### **14. Debug API Requests**

```bash
# Enable verbose curl output
curl -v https://movember-api.onrender.com/health/

# Check response headers
curl -I https://movember-api.onrender.com/health/

# Test with different content types
curl -H "Content-Type: application/json" \
     -d '{"test": "data"}' \
     https://movember-api.onrender.com/grants/
```

## **🔄 Recovery Procedures**

### **15. Service Recovery**

```bash
# 1. Check service status
curl -s https://movember-api.onrender.com/health/

# 2. If down, restart on Render dashboard
# Go to https://dashboard.render.com
# Navigate to movember-api service
# Click "Manual Deploy"

# 3. Wait for deployment
sleep 60

# 4. Test again
curl -s https://movember-api.onrender.com/health/
```

### **16. Database Recovery**

```python
# Reset database connection
from sqlalchemy import create_engine
import time

def reset_database_connection():
    """Reset database connection with retry logic."""
    max_retries = 3
    retry_delay = 5
    
    for attempt in range(max_retries):
        try:
            engine = create_engine(DATABASE_URL)
            with engine.connect() as conn:
                conn.execute("SELECT 1")
                print("✅ Database connection restored")
                return engine
        except Exception as e:
            print(f"❌ Attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
                retry_delay *= 2
    
    raise Exception("Failed to restore database connection")
```

## **📞 Getting Help**

### **17. Collect Debug Information**

```bash
# Create debug report
cat > debug_report.txt << EOF
=== Movember AI Rules System Debug Report ===
Date: $(date)
Version: $(cat VERSION)

=== System Information ===
OS: $(uname -a)
Python: $(python --version)
Node: $(node --version)
NPM: $(npm --version)

=== API Status ===
$(curl -s https://movember-api.onrender.com/health/ | jq '.')

=== Database Status ===
$(python -c "import os; from sqlalchemy import create_engine; print('Database URL:', os.getenv('DATABASE_URL', 'Not set'))")

=== Recent Logs ===
$(tail -n 50 logs/app.log 2>/dev/null || echo "No logs found")

=== Test Results ===
$(python -m pytest tests/ --tb=short 2>&1 | tail -n 20)
EOF

echo "Debug report saved to debug_report.txt"
```

### **18. Contact Information**

- **GitHub Issues**: Report bugs on the repository
- **Documentation**: Check `docs/` directory
- **Logs**: Check `/opt/movember-ai-rules/logs/`
- **Health Check**: Run `./scripts/health-check.sh`

## **✅ Prevention Checklist**

### **Before Deployment**
- [ ] All tests passing
- [ ] Code quality checks clean
- [ ] Environment variables set
- [ ] Database migrations applied
- [ ] API endpoints tested

### **After Deployment**
- [ ] Health endpoint responding
- [ ] Database connection working
- [ ] Frontend loading correctly
- [ ] Monitoring alerts configured
- [ ] Backup procedures tested

### **Regular Maintenance**
- [ ] Monitor system metrics
- [ ] Review error logs
- [ ] Update dependencies
- [ ] Test backup/restore
- [ ] Performance optimization

---

**Movember AI Rules System Troubleshooting Guide v1.1** - Comprehensive solutions for all common issues. 🇦🇺 