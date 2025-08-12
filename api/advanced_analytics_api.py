"""
Advanced Analytics API for Movember
FastAPI endpoints for sophisticated predictive models
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import Dict, List, Optional, Any
from datetime import datetime
import json
import logging

# Import the advanced predictive models
try:
    from analytics.advanced_predictive_models import (
        AdvancedPredictiveModels, 
        ModelType, 
        PredictionHorizon,
        AdvancedAnalyticsConfig,
        ModelPerformance,
        PredictionResult,
        ModelInsight
    )
    ADVANCED_ANALYTICS_AVAILABLE = True
except ImportError as e:
    ADVANCED_ANALYTICS_AVAILABLE = False
    logging.warning(f"Advanced Analytics not available: {e}")

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/analytics/advanced", tags=["Advanced Analytics"])

# Global instance of advanced predictive models
advanced_models = None

def get_advanced_models():
    """Get or create advanced predictive models instance"""
    global advanced_models
    if advanced_models is None and ADVANCED_ANALYTICS_AVAILABLE:
        config = AdvancedAnalyticsConfig(
            enable_real_time_predictions=True,
            enable_automated_retraining=True,
            retraining_frequency_days=30,
            confidence_threshold=0.8,
            max_features=50,
            cross_validation_folds=5,
            enable_feature_engineering=True,
            enable_ensemble_models=True
        )
        advanced_models = AdvancedPredictiveModels(config)
    return advanced_models

@router.get("/health")
async def advanced_analytics_health():
    """Check if advanced analytics is available"""
    if not ADVANCED_ANALYTICS_AVAILABLE:
        raise HTTPException(status_code=503, detail="Advanced Analytics not available")
    
    models = get_advanced_models()
    if models is None:
        raise HTTPException(status_code=503, detail="Failed to initialize advanced models")
    
    return {
        "status": "healthy",
        "available": True,
        "model_types": [mt.value for mt in ModelType],
        "prediction_horizons": [ph.value for ph in PredictionHorizon],
        "total_models": len(ModelType) * len(PredictionHorizon)
    }

@router.get("/models/summary")
async def get_models_summary():
    """Get summary of all advanced predictive models"""
    if not ADVANCED_ANALYTICS_AVAILABLE:
        raise HTTPException(status_code=503, detail="Advanced Analytics not available")
    
    models = get_advanced_models()
    summary = models.get_model_summary()
    
    return {
        "summary": summary,
        "timestamp": datetime.now().isoformat(),
        "status": "success"
    }

@router.post("/models/train")
async def train_models(background_tasks: BackgroundTasks, force_retrain: bool = False):
    """Train all advanced predictive models"""
    if not ADVANCED_ANALYTICS_AVAILABLE:
        raise HTTPException(status_code=503, detail="Advanced Analytics not available")
    
    models = get_advanced_models()
    
    # Start training in background
    def train_all_models():
        try:
            performances = models.train_all_models()
            logger.info(f"Successfully trained {len(performances)} models")
            return performances
        except Exception as e:
            logger.error(f"Error training models: {e}")
            return None
    
    background_tasks.add_task(train_all_models)
    
    return {
        "message": "Model training started in background",
        "force_retrain": force_retrain,
        "total_models": len(ModelType) * len(PredictionHorizon),
        "timestamp": datetime.now().isoformat()
    }

@router.post("/models/train/{model_type}/{horizon}")
async def train_specific_model(
    model_type: str, 
    horizon: str, 
    force_retrain: bool = False
):
    """Train a specific model"""
    if not ADVANCED_ANALYTICS_AVAILABLE:
        raise HTTPException(status_code=503, detail="Advanced Analytics not available")
    
    try:
        mt = ModelType(model_type)
        ph = PredictionHorizon(horizon)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid model type or horizon: {e}")
    
    models = get_advanced_models()
    performance = models.train_model(mt, ph, force_retrain)
    
    return {
        "model_type": model_type,
        "horizon": horizon,
        "performance": {
            "accuracy": performance.accuracy,
            "precision": performance.precision,
            "recall": performance.recall,
            "f1_score": performance.f1_score,
            "mse": performance.mse,
            "r2_score": performance.r2_score,
            "training_time": performance.training_time,
            "last_updated": performance.last_updated.isoformat()
        },
        "timestamp": datetime.now().isoformat()
    }

@router.post("/predict/{model_type}/{horizon}")
async def make_prediction(
    model_type: str,
    horizon: str,
    features: Dict[str, float]
):
    """Make a prediction using a specific model"""
    if not ADVANCED_ANALYTICS_AVAILABLE:
        raise HTTPException(status_code=503, detail="Advanced Analytics not available")
    
    try:
        mt = ModelType(model_type)
        ph = PredictionHorizon(horizon)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid model type or horizon: {e}")
    
    models = get_advanced_models()
    result = models.predict(mt, ph, features)
    
    return {
        "prediction": {
            "predicted_value": result.predicted_value,
            "confidence_interval_lower": result.confidence_interval_lower,
            "confidence_interval_upper": result.confidence_interval_upper,
            "confidence_level": result.confidence_level,
            "model_used": result.model_used.value,
            "prediction_horizon": result.prediction_horizon.value,
            "features_used": result.features_used,
            "timestamp": result.timestamp.isoformat()
        },
        "input_features": features,
        "status": "success"
    }

@router.get("/insights/{model_type}/{horizon}")
async def get_model_insights(model_type: str, horizon: str):
    """Get insights from a specific model"""
    if not ADVANCED_ANALYTICS_AVAILABLE:
        raise HTTPException(status_code=503, detail="Advanced Analytics not available")
    
    try:
        mt = ModelType(model_type)
        ph = PredictionHorizon(horizon)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid model type or horizon: {e}")
    
    models = get_advanced_models()
    insights = models.generate_insights(mt, ph)
    
    return {
        "model_type": model_type,
        "horizon": horizon,
        "insights": [
            {
                "insight_type": insight.insight_type,
                "description": insight.description,
                "confidence": insight.confidence,
                "actionable": insight.actionable,
                "impact_score": insight.impact_score,
                "recommendations": insight.recommendations
            }
            for insight in insights
        ],
        "total_insights": len(insights),
        "timestamp": datetime.now().isoformat()
    }

@router.get("/insights/all")
async def get_all_insights():
    """Get insights from all models"""
    if not ADVANCED_ANALYTICS_AVAILABLE:
        raise HTTPException(status_code=503, detail="Advanced Analytics not available")
    
    models = get_advanced_models()
    all_insights = []
    
    for model_type in ModelType:
        for horizon in PredictionHorizon:
            insights = models.generate_insights(model_type, horizon)
            for insight in insights:
                all_insights.append({
                    "model_type": model_type.value,
                    "horizon": horizon.value,
                    "insight_type": insight.insight_type,
                    "description": insight.description,
                    "confidence": insight.confidence,
                    "actionable": insight.actionable,
                    "impact_score": insight.impact_score,
                    "recommendations": insight.recommendations
                })
    
    return {
        "insights": all_insights,
        "total_insights": len(all_insights),
        "model_types": [mt.value for mt in ModelType],
        "horizons": [ph.value for ph in PredictionHorizon],
        "timestamp": datetime.now().isoformat()
    }

@router.get("/performance/{model_type}")
async def get_model_performance(model_type: str):
    """Get performance metrics for a specific model type across all horizons"""
    if not ADVANCED_ANALYTICS_AVAILABLE:
        raise HTTPException(status_code=503, detail="Advanced Analytics not available")
    
    try:
        mt = ModelType(model_type)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid model type: {e}")
    
    models = get_advanced_models()
    performances = {}
    
    for horizon in PredictionHorizon:
        model_key = f"{mt.value}_{horizon.value}"
        if model_key in models.performance_metrics:
            perf = models.performance_metrics[model_key]
            performances[horizon.value] = {
                "accuracy": perf.accuracy,
                "precision": perf.precision,
                "recall": perf.recall,
                "f1_score": perf.f1_score,
                "mse": perf.mse,
                "r2_score": perf.r2_score,
                "training_time": perf.training_time,
                "last_updated": perf.last_updated.isoformat()
            }
    
    return {
        "model_type": model_type,
        "performances": performances,
        "total_horizons": len(performances),
        "timestamp": datetime.now().isoformat()
    }

@router.get("/performance/all")
async def get_all_performance():
    """Get performance metrics for all models"""
    if not ADVANCED_ANALYTICS_AVAILABLE:
        raise HTTPException(status_code=503, detail="Advanced Analytics not available")
    
    models = get_advanced_models()
    all_performances = {}
    
    for model_type in ModelType:
        all_performances[model_type.value] = {}
        for horizon in PredictionHorizon:
            model_key = f"{model_type.value}_{horizon.value}"
            if model_key in models.performance_metrics:
                perf = models.performance_metrics[model_key]
                all_performances[model_type.value][horizon.value] = {
                    "accuracy": perf.accuracy,
                    "precision": perf.precision,
                    "recall": perf.recall,
                    "f1_score": perf.f1_score,
                    "mse": perf.mse,
                    "r2_score": perf.r2_score,
                    "training_time": perf.training_time,
                    "last_updated": perf.last_updated.isoformat()
                }
    
    return {
        "performances": all_performances,
        "total_models": len(ModelType),
        "total_horizons": len(PredictionHorizon),
        "timestamp": datetime.now().isoformat()
    }

@router.get("/feature-importance/{model_type}/{horizon}")
async def get_feature_importance(model_type: str, horizon: str, top_n: int = 10):
    """Get feature importance for a specific model"""
    if not ADVANCED_ANALYTICS_AVAILABLE:
        raise HTTPException(status_code=503, detail="Advanced Analytics not available")
    
    try:
        mt = ModelType(model_type)
        ph = PredictionHorizon(horizon)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid model type or horizon: {e}")
    
    models = get_advanced_models()
    model_key = f"{mt.value}_{ph.value}"
    
    if model_key not in models.feature_importance:
        raise HTTPException(status_code=404, detail="Feature importance not available for this model")
    
    features = models.feature_importance[model_key][:top_n]
    
    return {
        "model_type": model_type,
        "horizon": horizon,
        "feature_importance": [
            {
                "feature_name": fi.feature_name,
                "importance_score": fi.importance_score,
                "rank": fi.rank,
                "category": fi.category
            }
            for fi in features
        ],
        "total_features": len(features),
        "timestamp": datetime.now().isoformat()
    }

@router.post("/batch-predict")
async def batch_predict(
    predictions: List[Dict[str, Any]]
):
    """Make multiple predictions in batch"""
    if not ADVANCED_ANALYTICS_AVAILABLE:
        raise HTTPException(status_code=503, detail="Advanced Analytics not available")
    
    models = get_advanced_models()
    results = []
    
    for pred_request in predictions:
        try:
            model_type = pred_request.get("model_type")
            horizon = pred_request.get("horizon")
            features = pred_request.get("features", {})
            
            if not all([model_type, horizon, features]):
                results.append({
                    "error": "Missing required fields: model_type, horizon, or features",
                    "request": pred_request
                })
                continue
            
            mt = ModelType(model_type)
            ph = PredictionHorizon(horizon)
            result = models.predict(mt, ph, features)
            
            results.append({
                "prediction": {
                    "predicted_value": result.predicted_value,
                    "confidence_interval_lower": result.confidence_interval_lower,
                    "confidence_interval_upper": result.confidence_interval_upper,
                    "confidence_level": result.confidence_level,
                    "model_used": result.model_used.value,
                    "prediction_horizon": result.prediction_horizon.value,
                    "features_used": result.features_used,
                    "timestamp": result.timestamp.isoformat()
                },
                "input_features": features,
                "status": "success"
            })
            
        except Exception as e:
            results.append({
                "error": str(e),
                "request": pred_request
            })
    
    return {
        "predictions": results,
        "total_requests": len(predictions),
        "successful_predictions": len([r for r in results if "error" not in r]),
        "timestamp": datetime.now().isoformat()
    }

@router.get("/config")
async def get_config():
    """Get advanced analytics configuration"""
    if not ADVANCED_ANALYTICS_AVAILABLE:
        raise HTTPException(status_code=503, detail="Advanced Analytics not available")
    
    models = get_advanced_models()
    config = models.config
    
    return {
        "config": {
            "enable_real_time_predictions": config.enable_real_time_predictions,
            "enable_automated_retraining": config.enable_automated_retraining,
            "retraining_frequency_days": config.retraining_frequency_days,
            "confidence_threshold": config.confidence_threshold,
            "max_features": config.max_features,
            "cross_validation_folds": config.cross_validation_folds,
            "enable_feature_engineering": config.enable_feature_engineering,
            "enable_ensemble_models": config.enable_ensemble_models
        },
        "available_model_types": [mt.value for mt in ModelType],
        "available_horizons": [ph.value for ph in PredictionHorizon],
        "timestamp": datetime.now().isoformat()
    }

@router.get("/export")
async def export_model_data():
    """Export all model data"""
    if not ADVANCED_ANALYTICS_AVAILABLE:
        raise HTTPException(status_code=503, detail="Advanced Analytics not available")
    
    models = get_advanced_models()
    export_data = models.export_model_data()
    
    return {
        "export_data": export_data,
        "export_timestamp": datetime.now().isoformat(),
        "total_models_exported": len(export_data.get("performance_metrics", {})),
        "status": "success"
    }

@router.get("/test")
async def test_advanced_analytics():
    """Test endpoint for advanced analytics"""
    if not ADVANCED_ANALYTICS_AVAILABLE:
        raise HTTPException(status_code=503, detail="Advanced Analytics not available")
    
    models = get_advanced_models()
    
    # Test prediction
    test_features = {
        'campaign_budget': 500000,
        'social_media_reach': 100000,
        'email_subscribers': 50000,
        'website_traffic': 100000,
        'donor_count': 10000,
        'volunteer_count': 500,
        'event_count': 20,
        'partnership_count': 15,
        'media_coverage': 50,
        'awareness_score': 75
    }
    
    try:
        prediction = models.predict(
            ModelType.IMPACT_PREDICTION,
            PredictionHorizon.MEDIUM_TERM,
            test_features
        )
        
        insights = models.generate_insights(ModelType.IMPACT_PREDICTION, PredictionHorizon.MEDIUM_TERM)
        
        return {
            "status": "success",
            "test_prediction": {
                "predicted_value": prediction.predicted_value,
                "confidence_interval": f"{prediction.confidence_interval_lower:.0f} - {prediction.confidence_interval_upper:.0f}",
                "confidence_level": f"{prediction.confidence_level:.1%}"
            },
            "test_insights_count": len(insights),
            "model_summary": models.get_model_summary(),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

def include_advanced_analytics_routes(app):
    """Include advanced analytics routes in the main FastAPI app"""
    if ADVANCED_ANALYTICS_AVAILABLE:
        app.include_router(router)
        logger.info("Advanced Analytics API routes included")
    else:
        logger.warning("Advanced Analytics API routes not included - module not available")
