#!/usr/bin/env python3
"""
Machine Learning Integration for Movember AI Rules System
Predictive analytics and intelligent rule optimisation
"""
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import accuracy_score, mean_squared_error
import sqlite3
from datetime import datetime, timedelta
import logging

class MovemberMLEngine:


    def __init__(self):


        self.db_path = "movember_ai.db"
        self.models = {}
        self.logger = logging.getLogger(__name__)

    def load_training_data(self):


        """Load data for ML training"""
        conn = sqlite3.connect(self.db_path)

        # Load grants data
        grants_df = pd.read_sql_query("""
            SELECT * FROM grants
            WHERE created_at IS NOT NULL
        """, conn)

        # Load reports data
        reports_df = pd.read_sql_query("""
            SELECT * FROM impact_reports
            WHERE created_at IS NOT NULL
        """, conn)

        conn.close()
        return grants_df, reports_df

    def train_grant_success_predictor(self):


        """Train ML model to predict grant success"""
        grants_df, _ = self.load_training_data()

        if len(grants_df) < 10:
            self.logger.warning("Insufficient data for training")
            return

        # Feature engineering - using actual database columns
        features = ['budget', 'timeline_months']
        X = grants_df[features].fillna(0)
        y = grants_df['status'].map({'approved': 1, 'rejected': 0, 'pending': 0.5})

        # Train model
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X, y)

        self.models['grant_success'] = model
        self.logger.info("Grant success predictor trained")

    def train_impact_prediction_model(self):


        """Train ML model to predict impact outcomes"""
        _, reports_df = self.load_training_data()

        if len(reports_df) < 10:
            self.logger.warning("Insufficient data for training")
            return

        # Feature engineering for impact prediction
        features = ['grant_amount', 'duration_months', 'participant_count']
        X = reports_df[features].fillna(0)
        y = reports_df['impact_score'].fillna(0)

        # Train model
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X, y)

        self.models['impact_prediction'] = model
        self.logger.info("Impact prediction model trained")

    def predict_grant_success(self, grant_data):


        """Predict likelihood of grant success"""
        if 'grant_success' not in self.models:
            self.train_grant_success_predictor()

        model = self.models['grant_success']
        features = np.array([[
            grant_data.get('budget', 0),
            grant_data.get('timeline_months', 0)
        ]])

        prediction = model.predict_proba(features)[0]
        return {
            'success_probability': prediction[1],
            'confidence': max(prediction),
            'recommendations': self._generate_grant_recommendations(grant_data)
        }

    def predict_impact_outcome(self, project_data):


        """Predict expected impact outcome"""
        if 'impact_prediction' not in self.models:
            self.train_impact_prediction_model()

        model = self.models['impact_prediction']
        features = np.array([[
            project_data.get('grant_amount', 0),
            project_data.get('duration_months', 0),
            project_data.get('participant_count', 0)
        ]])

        prediction = model.predict(features)[0]
        return {
            'predicted_impact_score': prediction,
            'confidence_interval': self._calculate_confidence_interval(prediction),
            'optimisation_suggestions': self._generate_impact_recommendations(project_data)
        }

    def _generate_grant_recommendations(self, grant_data):


        """Generate recommendations for grant improvement"""
        recommendations = []

        if grant_data.get('budget', 0) < 50000:
            recommendations.append("Consider increasing budget for better impact potential")

        if grant_data.get('timeline_months', 0) < 12:
            recommendations.append("Longer project duration may improve outcomes")

        return recommendations

    def _generate_impact_recommendations(self, project_data):


        """Generate recommendations for impact optimisation"""
        recommendations = []

        if project_data.get('participant_count', 0) < 100:
            recommendations.append("Increase participant count for broader impact")

        if project_data.get('grant_amount', 0) < 100000:
            recommendations.append("Higher funding typically leads to better outcomes")

        return recommendations

    def _calculate_confidence_interval(self, prediction):


        """Calculate confidence interval for predictions"""
        # Simplified confidence calculation
        margin = prediction * 0.1  # 10% margin
        return {
            'lower': max(0, prediction - margin),
            'upper': min(100, prediction + margin)
        }

    def optimise_rules(self):


        """Use ML insights to optimise rule performance"""
        # Analyse rule effectiveness
        rule_performance = self._analyse_rule_performance()

        # Generate optimisation suggestions
        optimisations = []
        for rule, performance in rule_performance.items():
            if performance['success_rate'] < 0.7:
                optimisations.append(f"Rule '{rule}' may need refinement")

        return optimisations

    def _analyse_rule_performance(self):


        """Analyse how well rules are performing"""
        # This would connect to the rules engine metrics
        return {
            'uk_spelling_rule': {'success_rate': 0.95},
            'aud_currency_rule': {'success_rate': 0.92},
            'grant_validation_rule': {'success_rate': 0.88}
        }

# Example usage
if __name__ == "__main__":
    ml_engine = MovemberMLEngine()

    # Train models
    ml_engine.train_grant_success_predictor()
    ml_engine.train_impact_prediction_model()

    # Example predictions
    grant_data = {
        'budget': 75000,
        'timeline_months': 18
    }

    prediction = ml_engine.predict_grant_success(grant_data)
    print(f"Grant Success Prediction: {prediction}")

    # Optimise rules
    optimisations = ml_engine.optimise_rules()
    print(f"Rule Optimisations: {optimisations}")
