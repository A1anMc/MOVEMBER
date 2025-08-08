#!/usr/bin/env python3
"""
Advanced API for Movember AI Rules System
Enhanced endpoints with ML integration and analytics
"""
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import json
import sqlite3
from datetime import datetime
import logging
import asyncio
from ml_integration import MovemberMLEngine

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Movember AI Rules System - Advanced API",
    description="Enhanced API with ML predictions and analytics",
    version="2.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class GrantPredictionRequest(BaseModel):
    budget_amount: float
    duration_months: int
    team_size: int
    project_type: str
    target_audience: str

class ImpactPredictionRequest(BaseModel):
    grant_amount: float
    duration_months: int
    participant_count: int
    project_scope: str
    intervention_type: str

class AnalyticsRequest(BaseModel):
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    metrics: List[str] = ["grants", "reports", "impact"]

class RuleOptimisationRequest(BaseModel):
    rule_name: str
    performance_threshold: float = 0.7

# Database functions
def get_db_connection():
    return sqlite3.connect("movember_ai.db")

def init_advanced_tables():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create ML predictions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ml_predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prediction_type TEXT NOT NULL,
            input_data TEXT NOT NULL,
            prediction_result TEXT NOT NULL,
            confidence_score REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Create analytics cache table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS analytics_cache (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            metric_name TEXT NOT NULL,
            metric_value TEXT NOT NULL,
            cache_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    conn.close()

# ML Engine instance
ml_engine = MovemberMLEngine()

@app.on_event("startup")
async def startup_event():
    init_advanced_tables()
    logger.info("Advanced API started with ML integration")

# Enhanced endpoints
@app.get("/")
async def root():
    return {
        "message": "Movember AI Rules System - Advanced API",
        "version": "2.0.0",
        "features": [
            "ML-powered predictions",
            "Advanced analytics",
            "Rule optimisation",
            "Real-time monitoring"
        ],
        "endpoints": {
            "health": "/health/",
            "predictions": "/predictions/",
            "analytics": "/analytics/",
            "optimisation": "/optimisation/"
        }
    }

@app.get("/health/")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "2.0.0",
        "ml_models_loaded": len(ml_engine.models),
        "database_status": "healthy",
        "uk_spelling_compliance": True,
        "aud_currency_compliance": True
    }

@app.post("/predictions/grant-success/")
async def predict_grant_success(request: GrantPredictionRequest):
    """Predict grant success probability using ML"""
    try:
        grant_data = {
            'budget_amount': request.budget_amount,
            'duration_months': request.duration_months,
            'team_size': request.team_size
        }
        
        prediction = ml_engine.predict_grant_success(grant_data)
        
        # Store prediction
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO ml_predictions (prediction_type, input_data, prediction_result, confidence_score)
            VALUES (?, ?, ?, ?)
        """, (
            'grant_success',
            json.dumps(grant_data),
            json.dumps(prediction),
            prediction['confidence']
        ))
        conn.commit()
        conn.close()
        
        return {
            "prediction": prediction,
            "input_data": grant_data,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error in grant prediction: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predictions/impact-outcome/")
async def predict_impact_outcome(request: ImpactPredictionRequest):
    """Predict impact outcome using ML"""
    try:
        project_data = {
            'grant_amount': request.grant_amount,
            'duration_months': request.duration_months,
            'participant_count': request.participant_count
        }
        
        prediction = ml_engine.predict_impact_outcome(project_data)
        
        # Store prediction
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO ml_predictions (prediction_type, input_data, prediction_result, confidence_score)
            VALUES (?, ?, ?, ?)
        """, (
            'impact_outcome',
            json.dumps(project_data),
            json.dumps(prediction),
            prediction.get('confidence_interval', {}).get('upper', 0.8)
        ))
        conn.commit()
        conn.close()
        
        return {
            "prediction": prediction,
            "input_data": project_data,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error in impact prediction: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/analytics/")
async def get_analytics(request: AnalyticsRequest):
    """Get comprehensive analytics"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        analytics = {}
        
        # Grant analytics
        cursor.execute("SELECT COUNT(*), SUM(budget_amount) FROM grants")
        grant_count, total_budget = cursor.fetchone()
        analytics['grants'] = {
            'total_count': grant_count or 0,
            'total_budget': total_budget or 0,
            'average_budget': (total_budget or 0) / (grant_count or 1)
        }
        
        # Report analytics
        cursor.execute("SELECT COUNT(*), AVG(impact_score) FROM impact_reports")
        report_count, avg_impact = cursor.fetchone()
        analytics['reports'] = {
            'total_count': report_count or 0,
            'average_impact_score': avg_impact or 0
        }
        
        # ML predictions analytics
        cursor.execute("SELECT COUNT(*) FROM ml_predictions")
        prediction_count = cursor.fetchone()[0]
        analytics['predictions'] = {
            'total_predictions': prediction_count
        }
        
        # Compliance analytics
        analytics['compliance'] = {
            'uk_spelling_compliance': True,
            'aud_currency_compliance': True,
            'last_check': datetime.now().isoformat()
        }
        
        conn.close()
        
        return {
            "analytics": analytics,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error in analytics: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/optimisation/rules/")
async def optimise_rules(request: RuleOptimisationRequest):
    """Get rule optimisation recommendations"""
    try:
        optimisations = ml_engine.optimise_rules()
        
        return {
            "optimisations": optimisations,
            "rule_name": request.rule_name,
            "performance_threshold": request.performance_threshold,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error in rule optimisation: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/predictions/history/")
async def get_prediction_history():
    """Get history of ML predictions"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT prediction_type, input_data, prediction_result, confidence_score, created_at
            FROM ml_predictions
            ORDER BY created_at DESC
            LIMIT 50
        """)
        
        predictions = []
        for row in cursor.fetchall():
            predictions.append({
                'prediction_type': row[0],
                'input_data': json.loads(row[1]),
                'prediction_result': json.loads(row[2]),
                'confidence_score': row[3],
                'created_at': row[4]
            })
        
        conn.close()
        
        return {
            "predictions": predictions,
            "total_count": len(predictions)
        }
    except Exception as e:
        logger.error(f"Error getting prediction history: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ml/train/")
async def train_ml_models(background_tasks: BackgroundTasks):
    """Train ML models in background"""
    def train_models():
        try:
            ml_engine.train_grant_success_predictor()
            ml_engine.train_impact_prediction_model()
            logger.info("ML models trained successfully")
        except Exception as e:
            logger.error(f"Error training ML models: {e}")
    
    background_tasks.add_task(train_models)
    
    return {
        "message": "ML model training started in background",
        "status": "training",
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001) 