#!/usr/bin/env python3
"""
Add sample data for ML training
"""
import sqlite3
from datetime import datetime, timedelta
import json

def add_sample_data():
    conn = sqlite3.connect("movember_ai.db")
    cursor = conn.cursor()

    # Add sample grants
    sample_grants = [
        ("GRANT001", "Men's Health Research Grant", 75000, "AUD", 18, "approved", "Health Research Org", "2024-01-15"),
        ("GRANT002", "Prostate Cancer Awareness", 50000, "AUD", 12, "approved", "Cancer Foundation", "2024-02-20"),
        ("GRANT003", "Mental Health Initiative", 100000, "AUD", 24, "approved", "Mental Health Org", "2024-03-10"),
        ("GRANT004", "Testicular Cancer Screening", 30000, "AUD", 6, "rejected", "Medical Centre", "2024-04-05"),
        ("GRANT005", "Suicide Prevention Program", 150000, "AUD", 36, "approved", "Crisis Support", "2024-05-12"),
        ("GRANT006", "Physical Activity Campaign", 45000, "AUD", 9, "rejected", "Fitness Org", "2024-06-18"),
        ("GRANT007", "Nutrition Education", 60000, "AUD", 15, "approved", "Nutrition Institute", "2024-07-22"),
        ("GRANT008", "Stress Management Workshop", 25000, "AUD", 8, "pending", "Wellness Centre", "2024-08-30"),
        ("GRANT009", "Sleep Health Research", 80000, "AUD", 20, "approved", "Sleep Research", "2024-09-14"),
        ("GRANT010", "Social Connection Program", 40000, "AUD", 10, "approved", "Community Org", "2024-10-25")
    ]

    for grant in sample_grants:
        cursor.execute("""
            INSERT OR REPLACE INTO grants
            (grant_id, title, budget, currency, timeline_months, status, organisation, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, grant)

    # Check if impact_reports table exists, if not create it
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS impact_reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            report_id TEXT UNIQUE NOT NULL,
            title TEXT,
            grant_amount REAL,
            duration_months INTEGER,
            participant_count INTEGER,
            impact_score REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Add sample impact reports
    sample_reports = [
        ("REPORT001", "Men's Health Research Impact", 75000, 18, 500, 85, "2024-07-15"),
        ("REPORT002", "Prostate Cancer Awareness Results", 50000, 12, 300, 78, "2024-08-20"),
        ("REPORT003", "Mental Health Initiative Outcomes", 100000, 24, 800, 92, "2024-09-10"),
        ("REPORT004", "Suicide Prevention Impact", 150000, 36, 1200, 88, "2024-10-12"),
        ("REPORT005", "Nutrition Education Results", 60000, 15, 400, 82, "2024-11-22"),
        ("REPORT006", "Sleep Health Research Impact", 80000, 20, 600, 90, "2024-12-14"),
        ("REPORT007", "Social Connection Outcomes", 40000, 10, 250, 75, "2025-01-25")
    ]

    for report in sample_reports:
        cursor.execute("""
            INSERT OR REPLACE INTO impact_reports
            (report_id, title, grant_amount, duration_months, participant_count, impact_score, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, report)

    conn.commit()
    conn.close()

    print("✅ Sample data added successfully!")
    print("📊 Added 10 sample grants and 7 impact reports")

if __name__ == "__main__":
    add_sample_data()
