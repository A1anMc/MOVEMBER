#!/usr/bin/env python3
"""
Simple ML test
"""
import sqlite3
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import numpy as np

# Test database connection and data
conn = sqlite3.connect("movember_ai.db")
grants_df = pd.read_sql_query("SELECT * FROM grants", conn)
conn.close()

print(f"Found {len(grants_df)} grants")
print(f"Columns: {list(grants_df.columns)}")
print(f"Status values: {grants_df['status'].unique()}")
print(f"Status data type: {grants_df['status'].dtype}")

if len(grants_df) >= 10:
    # Use correct column names
    features = ['budget', 'timeline_months']
    X = grants_df[features].fillna(0)
    
    # Fix status mapping - use only discrete values
    status_mapping = {'approved': 1, 'rejected': 0, 'pending': 0}
    y = grants_df['status'].map(status_mapping).fillna(0)  # Default to rejected for unknown statuses
    
    print(f"Target values: {y.unique()}")
    print(f"Target data type: {y.dtype}")
    print(f"Target sample: {y.head()}")
    
    # Convert to integer to ensure discrete values
    y = y.astype(int)
    print(f"After conversion - Target values: {y.unique()}")
    print(f"After conversion - Target data type: {y.dtype}")
    
    # Train model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    
    # Test prediction
    test_data = np.array([[75000, 18]])
    prediction = model.predict_proba(test_data)[0]
    
    print(f"✅ ML model trained successfully!")
    print(f"Success probability: {prediction[1]:.2f}")
    print(f"Confidence: {max(prediction):.2f}")
else:
    print(f"❌ Insufficient data: {len(grants_df)} grants (need 10+)") 