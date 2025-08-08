#!/usr/bin/env python3
"""
Machine Learning Models for Movember AI Rules System
Advanced analytics and prediction models for grant evaluation and impact assessment.
"""

import asyncio
import logging
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
import joblib
import json
from datetime import datetime
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.svm import SVC, SVR
from sklearn.neural_network import MLPClassifier, MLPRegressor
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.feature_selection import SelectKBest, f_classif, f_regression
import warnings
warnings.filterwarnings('ignore')

logger = logging.getLogger(__name__)

class MLModelManager:
    """Manages multiple ML models for different prediction tasks."""
    
    def __init__(self, models_dir: str = "ml_integration/models"):
        self.models_dir = models_dir
        self.models = {}
        self.scalers = {}
        self.feature_selectors = {}
        self.model_metrics = {}
        self.training_history = []
        
    async def train_grant_evaluation_model(self, training_data: pd.DataFrame) -> Dict[str, Any]:
        """Train model for grant evaluation and scoring."""
        try:
            # Prepare data
            X, y = self._prepare_grant_evaluation_data(training_data)
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            
            # Feature selection
            feature_selector = SelectKBest(score_func=f_classif, k=10)
            X_train_selected = feature_selector.fit_transform(X_train, y_train)
            X_test_selected = feature_selector.transform(X_test)
            
            # Scale features
            scaler = StandardScaler()
            X_train_scaled = scaler.fit_transform(X_train_selected)
            X_test_scaled = scaler.transform(X_test_selected)
            
            # Train multiple models
            models = {
                "random_forest": RandomForestClassifier(n_estimators=100, random_state=42),
                "gradient_boosting": GradientBoostingClassifier(random_state=42),
                "logistic_regression": LogisticRegression(random_state=42),
                "svm": SVC(random_state=42),
                "neural_network": MLPClassifier(hidden_layer_sizes=(100, 50), random_state=42)
            }
            
            best_model = None
            best_score = 0
            model_results = {}
            
            for name, model in models.items():
                # Train model
                model.fit(X_train_scaled, y_train)
                
                # Predict
                y_pred = model.predict(X_test_scaled)
                
                # Calculate metrics
                accuracy = accuracy_score(y_test, y_pred)
                precision = precision_score(y_test, y_pred, average='weighted')
                recall = recall_score(y_test, y_pred, average='weighted')
                f1 = f1_score(y_test, y_pred, average='weighted')
                
                model_results[name] = {
                    "accuracy": accuracy,
                    "precision": precision,
                    "recall": recall,
                    "f1_score": f1
                }
                
                # Track best model
                if f1 > best_score:
                    best_score = f1
                    best_model = model
            
            # Save best model and components
            self.models["grant_evaluation"] = best_model
            self.scalers["grant_evaluation"] = scaler
            self.feature_selectors["grant_evaluation"] = feature_selector
            self.model_metrics["grant_evaluation"] = model_results
            
            # Save model
            await self._save_model("grant_evaluation", best_model, scaler, feature_selector)
            
            return {
                "task": "grant_evaluation",
                "best_model": "random_forest" if best_model.__class__.__name__ == "RandomForestClassifier" else "other",
                "metrics": model_results,
                "best_score": best_score,
                "feature_importance": self._get_feature_importance(best_model, feature_selector)
            }
            
        except Exception as e:
            logger.error(f"Failed to train grant evaluation model: {e}")
            return {"error": str(e)}
    
    async def train_impact_prediction_model(self, training_data: pd.DataFrame) -> Dict[str, Any]:
        """Train model for impact prediction."""
        try:
            # Prepare data
            X, y = self._prepare_impact_prediction_data(training_data)
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            
            # Feature selection
            feature_selector = SelectKBest(score_func=f_regression, k=8)
            X_train_selected = feature_selector.fit_transform(X_train, y_train)
            X_test_selected = feature_selector.transform(X_test)
            
            # Scale features
            scaler = StandardScaler()
            X_train_scaled = scaler.fit_transform(X_train_selected)
            X_test_scaled = scaler.transform(X_test_selected)
            
            # Train regression models
            models = {
                "random_forest": RandomForestRegressor(n_estimators=100, random_state=42),
                "gradient_boosting": GradientBoostingClassifier(random_state=42),
                "linear_regression": LinearRegression(),
                "svm": SVR(),
                "neural_network": MLPRegressor(hidden_layer_sizes=(100, 50), random_state=42)
            }
            
            best_model = None
            best_score = 0
            model_results = {}
            
            for name, model in models.items():
                # Train model
                model.fit(X_train_scaled, y_train)
                
                # Predict
                y_pred = model.predict(X_test_scaled)
                
                # Calculate metrics
                mse = mean_squared_error(y_test, y_pred)
                r2 = r2_score(y_test, y_pred)
                
                model_results[name] = {
                    "mse": mse,
                    "r2_score": r2,
                    "rmse": np.sqrt(mse)
                }
                
                # Track best model
                if r2 > best_score:
                    best_score = r2
                    best_model = model
            
            # Save best model and components
            self.models["impact_prediction"] = best_model
            self.scalers["impact_prediction"] = scaler
            self.feature_selectors["impact_prediction"] = feature_selector
            self.model_metrics["impact_prediction"] = model_results
            
            # Save model
            await self._save_model("impact_prediction", best_model, scaler, feature_selector)
            
            return {
                "task": "impact_prediction",
                "best_model": "random_forest" if best_model.__class__.__name__ == "RandomForestRegressor" else "other",
                "metrics": model_results,
                "best_score": best_score,
                "feature_importance": self._get_feature_importance(best_model, feature_selector)
            }
            
        except Exception as e:
            logger.error(f"Failed to train impact prediction model: {e}")
            return {"error": str(e)}
    
    async def train_sdg_alignment_model(self, training_data: pd.DataFrame) -> Dict[str, Any]:
        """Train model for SDG alignment prediction."""
        try:
            # Prepare data
            X, y = self._prepare_sdg_alignment_data(training_data)
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            
            # Feature selection
            feature_selector = SelectKBest(score_func=f_classif, k=6)
            X_train_selected = feature_selector.fit_transform(X_train, y_train)
            X_test_selected = feature_selector.transform(X_test)
            
            # Scale features
            scaler = StandardScaler()
            X_train_scaled = scaler.fit_transform(X_train_selected)
            X_test_scaled = scaler.transform(X_test_selected)
            
            # Train classification models
            models = {
                "random_forest": RandomForestClassifier(n_estimators=100, random_state=42),
                "gradient_boosting": GradientBoostingClassifier(random_state=42),
                "logistic_regression": LogisticRegression(random_state=42),
                "svm": SVC(random_state=42),
                "neural_network": MLPClassifier(hidden_layer_sizes=(100, 50), random_state=42)
            }
            
            best_model = None
            best_score = 0
            model_results = {}
            
            for name, model in models.items():
                # Train model
                model.fit(X_train_scaled, y_train)
                
                # Predict
                y_pred = model.predict(X_test_scaled)
                
                # Calculate metrics
                accuracy = accuracy_score(y_test, y_pred)
                precision = precision_score(y_test, y_pred, average='weighted')
                recall = recall_score(y_test, y_pred, average='weighted')
                f1 = f1_score(y_test, y_pred, average='weighted')
                
                model_results[name] = {
                    "accuracy": accuracy,
                    "precision": precision,
                    "recall": recall,
                    "f1_score": f1
                }
                
                # Track best model
                if f1 > best_score:
                    best_score = f1
                    best_model = model
            
            # Save best model and components
            self.models["sdg_alignment"] = best_model
            self.scalers["sdg_alignment"] = scaler
            self.feature_selectors["sdg_alignment"] = feature_selector
            self.model_metrics["sdg_alignment"] = model_results
            
            # Save model
            await self._save_model("sdg_alignment", best_model, scaler, feature_selector)
            
            return {
                "task": "sdg_alignment",
                "best_model": "random_forest" if best_model.__class__.__name__ == "RandomForestClassifier" else "other",
                "metrics": model_results,
                "best_score": best_score,
                "feature_importance": self._get_feature_importance(best_model, feature_selector)
            }
            
        except Exception as e:
            logger.error(f"Failed to train SDG alignment model: {e}")
            return {"error": str(e)}
    
    def _prepare_grant_evaluation_data(self, data: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
        """Prepare data for grant evaluation model."""
        # Select features
        feature_columns = [
            "amount", "timeline_months", "category_encoded", 
            "target_demographic_encoded", "location_encoded",
            "organisation_size", "contact_experience_level",
            "description_length", "has_budget_breakdown",
            "has_timeline_details", "has_stakeholder_plan",
            "has_impact_metrics", "has_sdg_alignment"
        ]
        
        # Select target
        target_column = "approval_probability"
        
        # Filter data
        available_columns = data.columns.tolist()
        selected_features = [col for col in feature_columns if col in available_columns]
        
        if target_column not in available_columns:
            # Create target based on overall score
            data[target_column] = (data.get("overall_score", 0) >= 0.7).astype(int)
        
        X = data[selected_features].fillna(0).values
        y = data[target_column].values
        
        return X, y
    
    def _prepare_impact_prediction_data(self, data: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
        """Prepare data for impact prediction model."""
        # Select features
        feature_columns = [
            "amount", "timeline_months", "category_encoded",
            "organisation_size", "has_impact_metrics",
            "has_stakeholder_plan", "has_sdg_alignment"
        ]
        
        # Select target
        target_column = "impact_potential"
        
        # Filter data
        available_columns = data.columns.tolist()
        selected_features = [col for col in feature_columns if col in available_columns]
        
        X = data[selected_features].fillna(0).values
        y = data[target_column].fillna(0.5).values
        
        return X, y
    
    def _prepare_sdg_alignment_data(self, data: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
        """Prepare data for SDG alignment model."""
        # Select features
        feature_columns = [
            "category_encoded", "has_sdg_alignment",
            "has_impact_metrics", "has_stakeholder_plan",
            "organisation_size", "amount"
        ]
        
        # Select target
        target_column = "overall_sdg_alignment_score"
        
        # Filter data
        available_columns = data.columns.tolist()
        selected_features = [col for col in feature_columns if col in available_columns]
        
        if target_column not in available_columns:
            # Create target based on SDG alignment
            data[target_column] = (data.get("has_sdg_alignment", 0) >= 0.5).astype(int)
        
        X = data[selected_features].fillna(0).values
        y = data[target_column].values
        
        return X, y
    
    def _get_feature_importance(self, model, feature_selector) -> Dict[str, float]:
        """Get feature importance from model."""
        try:
            if hasattr(model, 'feature_importances_'):
                # Get selected feature indices
                selected_features = feature_selector.get_support()
                feature_importance = model.feature_importances_
                
                # Map to original feature names
                importance_dict = {}
                for i, important in enumerate(selected_features):
                    if important:
                        importance_dict[f"feature_{i}"] = float(feature_importance[i])
                
                return importance_dict
            else:
                return {"feature_importance": "Not available for this model type"}
        except Exception as e:
            return {"feature_importance": f"Error: {str(e)}"}
    
    async def _save_model(self, model_name: str, model, scaler, feature_selector) -> bool:
        """Save trained model and components."""
        try:
            import os
            os.makedirs(self.models_dir, exist_ok=True)
            
            # Save model
            joblib.dump(model, f"{self.models_dir}/{model_name}_model.pkl")
            
            # Save scaler
            joblib.dump(scaler, f"{self.models_dir}/{model_name}_scaler.pkl")
            
            # Save feature selector
            joblib.dump(feature_selector, f"{self.models_dir}/{model_name}_selector.pkl")
            
            # Save metadata
            metadata = {
                "model_name": model_name,
                "model_type": model.__class__.__name__,
                "training_date": datetime.now().isoformat(),
                "feature_count": feature_selector.n_features_in_,
                "selected_features": int(feature_selector.n_features_in_)
            }
            
            with open(f"{self.models_dir}/{model_name}_metadata.json", 'w') as f:
                json.dump(metadata, f, indent=2)
            
            logger.info(f"Saved model {model_name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save model {model_name}: {e}")
            return False
    
    async def load_model(self, model_name: str) -> bool:
        """Load trained model and components."""
        try:
            # Load model
            model_path = f"{self.models_dir}/{model_name}_model.pkl"
            if os.path.exists(model_path):
                self.models[model_name] = joblib.load(model_path)
                self.scalers[model_name] = joblib.load(f"{self.models_dir}/{model_name}_scaler.pkl")
                self.feature_selectors[model_name] = joblib.load(f"{self.models_dir}/{model_name}_selector.pkl")
                logger.info(f"Loaded model {model_name}")
                return True
            else:
                logger.warning(f"Model {model_name} not found")
                return False
                
        except Exception as e:
            logger.error(f"Failed to load model {model_name}: {e}")
            return False
    
    async def predict_grant_evaluation(self, grant_data: Dict[str, Any]) -> Dict[str, Any]:
        """Predict grant evaluation using trained model."""
        try:
            if "grant_evaluation" not in self.models:
                await self.load_model("grant_evaluation")
            
            if "grant_evaluation" not in self.models:
                return {"error": "Model not available"}
            
            # Prepare features
            features = self._extract_grant_features_for_prediction(grant_data)
            
            # Transform features
            feature_selector = self.feature_selectors["grant_evaluation"]
            scaler = self.scalers["grant_evaluation"]
            model = self.models["grant_evaluation"]
            
            # Select and scale features
            features_selected = feature_selector.transform([features])
            features_scaled = scaler.transform(features_selected)
            
            # Make prediction
            prediction = model.predict(features_scaled)[0]
            probability = model.predict_proba(features_scaled)[0] if hasattr(model, 'predict_proba') else None
            
            return {
                "prediction": int(prediction),
                "probability": probability.tolist() if probability is not None else None,
                "confidence": float(max(probability)) if probability is not None else 0.5,
                "model_used": model.__class__.__name__
            }
            
        except Exception as e:
            logger.error(f"Failed to predict grant evaluation: {e}")
            return {"error": str(e)}
    
    def _extract_grant_features_for_prediction(self, grant_data: Dict[str, Any]) -> List[float]:
        """Extract features from grant data for prediction."""
        # This would be similar to the feature extraction in the data pipeline
        # For now, return a simple feature vector
        return [
            float(grant_data.get("amount", 0)),
            float(grant_data.get("timeline_months", 0)),
            self._encode_category(grant_data.get("category", "")),
            self._encode_demographic(grant_data.get("target_demographic", "")),
            self._encode_location(grant_data.get("location", "")),
            self._estimate_organisation_size(grant_data.get("organisation", "")),
            self._estimate_contact_experience(grant_data.get("contact_person", "")),
            len(grant_data.get("description", "")),
            1 if grant_data.get("budget") else 0,
            1 if grant_data.get("timeline_months") else 0,
            self._check_stakeholder_plan(grant_data),
            self._check_impact_metrics(grant_data),
            self._check_sdg_alignment(grant_data)
        ]
    
    def _encode_category(self, category: str) -> int:
        """Encode category as integer."""
        category_mapping = {
            "mental_health": 1,
            "physical_health": 2,
            "education": 3,
            "community": 4,
            "research": 5
        }
        return category_mapping.get(category.lower(), 0)
    
    def _encode_demographic(self, demographic: str) -> int:
        """Encode demographic as integer."""
        demographic_mapping = {
            "young_men": 1,
            "men": 2,
            "all": 3,
            "women": 4,
            "children": 5
        }
        return demographic_mapping.get(demographic.lower(), 0)
    
    def _encode_location(self, location: str) -> int:
        """Encode location as integer."""
        location_mapping = {
            "victoria": 1,
            "new_south_wales": 2,
            "queensland": 3,
            "western_australia": 4,
            "south_australia": 5,
            "tasmania": 6,
            "northern_territory": 7,
            "australian_capital_territory": 8
        }
        return location_mapping.get(location.lower().replace(" ", "_"), 0)
    
    def _estimate_organisation_size(self, organisation: str) -> int:
        """Estimate organisation size based on name patterns."""
        org_lower = organisation.lower()
        if any(word in org_lower for word in ["university", "hospital", "government", "department"]):
            return 3  # Large
        elif any(word in org_lower for word in ["foundation", "institute", "association"]):
            return 2  # Medium
        else:
            return 1  # Small
    
    def _estimate_contact_experience(self, contact: str) -> int:
        """Estimate contact experience level."""
        contact_lower = contact.lower()
        if "dr." in contact_lower or "professor" in contact_lower:
            return 3  # High experience
        elif "manager" in contact_lower or "director" in contact_lower:
            return 2  # Medium experience
        else:
            return 1  # Low experience
    
    def _check_stakeholder_plan(self, grant_data: Dict[str, Any]) -> int:
        """Check if grant has stakeholder engagement plan."""
        description = grant_data.get("description", "").lower()
        keywords = ["stakeholder", "community", "partnership", "engagement"]
        return 1 if any(keyword in description for keyword in keywords) else 0
    
    def _check_impact_metrics(self, grant_data: Dict[str, Any]) -> int:
        """Check if grant has impact metrics."""
        description = grant_data.get("description", "").lower()
        keywords = ["impact", "outcome", "measurement", "evaluation", "metrics"]
        return 1 if any(keyword in description for keyword in keywords) else 0
    
    def _check_sdg_alignment(self, grant_data: Dict[str, Any]) -> int:
        """Check if grant has SDG alignment."""
        description = grant_data.get("description", "").lower()
        keywords = ["sdg", "sustainable development", "goal", "target"]
        return 1 if any(keyword in description for keyword in keywords) else 0

async def main():
    """Test the ML model training system."""
    # Create sample training data
    np.random.seed(42)
    n_samples = 100
    
    sample_data = pd.DataFrame({
        "amount": np.random.uniform(10000, 100000, n_samples),
        "timeline_months": np.random.randint(6, 36, n_samples),
        "category_encoded": np.random.randint(1, 6, n_samples),
        "target_demographic_encoded": np.random.randint(1, 6, n_samples),
        "location_encoded": np.random.randint(1, 9, n_samples),
        "organisation_size": np.random.randint(1, 4, n_samples),
        "contact_experience_level": np.random.randint(1, 4, n_samples),
        "description_length": np.random.randint(100, 1000, n_samples),
        "has_budget_breakdown": np.random.randint(0, 2, n_samples),
        "has_timeline_details": np.random.randint(0, 2, n_samples),
        "has_stakeholder_plan": np.random.randint(0, 2, n_samples),
        "has_impact_metrics": np.random.randint(0, 2, n_samples),
        "has_sdg_alignment": np.random.randint(0, 2, n_samples),
        "overall_score": np.random.uniform(0, 10, n_samples),
        "approval_probability": np.random.randint(0, 2, n_samples),
        "impact_potential": np.random.uniform(0, 1, n_samples)
    })
    
    # Initialize model manager
    model_manager = MLModelManager()
    
    # Train models
    print("Training ML models...")
    
    grant_eval_result = await model_manager.train_grant_evaluation_model(sample_data)
    print(f"Grant evaluation model: {grant_eval_result}")
    
    impact_pred_result = await model_manager.train_impact_prediction_model(sample_data)
    print(f"Impact prediction model: {impact_pred_result}")
    
    sdg_result = await model_manager.train_sdg_alignment_model(sample_data)
    print(f"SDG alignment model: {sdg_result}")
    
    print("✅ ML model training system ready!")

if __name__ == "__main__":
    asyncio.run(main()) 