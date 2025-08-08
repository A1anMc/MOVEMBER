#!/usr/bin/env python3
"""
Data Quality Assurance System for Movember AI Rules System
Ensures data integrity, completeness, and accuracy for real data
"""
import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging
from typing import Dict, List, Any, Tuple
import json

class DataQualityAssurance:
    def __init__(self):
        self.db_path = "movember_ai.db"
        self.logger = logging.getLogger(__name__)
        
        # Quality thresholds
        self.quality_thresholds = {
            'completeness': 0.95,  # 95% of required fields must be present
            'accuracy': 0.90,       # 90% of data must pass validation
            'consistency': 0.85,    # 85% of data must be internally consistent
            'timeliness': 0.80      # 80% of data must be within acceptable age
        }
    
    def assess_data_quality(self, data_type: str) -> Dict[str, Any]:
        """Comprehensive data quality assessment"""
        conn = sqlite3.connect(self.db_path)
        
        if data_type == 'grants':
            df = pd.read_sql_query("SELECT * FROM real_grants", conn)
        elif data_type == 'research':
            df = pd.read_sql_query("SELECT * FROM real_research", conn)
        elif data_type == 'impact':
            df = pd.read_sql_query("SELECT * FROM real_impact", conn)
        else:
            df = pd.read_sql_query("SELECT * FROM grants", conn)
        
        conn.close()
        
        if len(df) == 0:
            return {
                'data_type': data_type,
                'total_records': 0,
                'quality_score': 0.0,
                'issues': ['No data available'],
                'recommendations': ['Collect more data']
            }
        
        # Quality metrics
        completeness_score = self._assess_completeness(df, data_type)
        accuracy_score = self._assess_accuracy(df, data_type)
        consistency_score = self._assess_consistency(df, data_type)
        timeliness_score = self._assess_timeliness(df, data_type)
        
        # Overall quality score
        overall_score = np.mean([completeness_score, accuracy_score, consistency_score, timeliness_score])
        
        # Identify issues
        issues = self._identify_issues(df, data_type)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(df, data_type, overall_score)
        
        return {
            'data_type': data_type,
            'total_records': len(df),
            'quality_score': overall_score,
            'completeness_score': completeness_score,
            'accuracy_score': accuracy_score,
            'consistency_score': consistency_score,
            'timeliness_score': timeliness_score,
            'issues': issues,
            'recommendations': recommendations,
            'assessment_date': datetime.now().isoformat()
        }
    
    def _assess_completeness(self, df: pd.DataFrame, data_type: str) -> float:
        """Assess data completeness"""
        if data_type == 'grants':
            required_fields = ['grant_id', 'title', 'budget', 'currency']
        elif data_type == 'research':
            required_fields = ['publication_id', 'title', 'authors']
        elif data_type == 'impact':
            required_fields = ['indicator_id', 'value', 'year']
        else:
            required_fields = ['grant_id', 'title', 'budget']
        
        # Check for missing values in required fields
        missing_counts = df[required_fields].isnull().sum()
        total_required = len(required_fields) * len(df)
        missing_total = missing_counts.sum()
        
        completeness_score = 1 - (missing_total / total_required)
        return completeness_score
    
    def _assess_accuracy(self, df: pd.DataFrame, data_type: str) -> float:
        """Assess data accuracy"""
        accuracy_checks = 0
        passed_checks = 0
        
        # Budget validation
        if 'budget' in df.columns:
            accuracy_checks += 1
            if df['budget'].dtype in ['int64', 'float64'] and (df['budget'] >= 0).all():
                passed_checks += 1
        
        # Currency validation
        if 'currency' in df.columns:
            accuracy_checks += 1
            valid_currencies = ['USD', 'GBP', 'AUD', 'EUR', 'CAD']
            if df['currency'].isin(valid_currencies).all():
                passed_checks += 1
        
        # Date validation
        if 'deadline' in df.columns:
            accuracy_checks += 1
            try:
                pd.to_datetime(df['deadline'])
                passed_checks += 1
            except:
                pass
        
        # Year validation
        if 'year' in df.columns:
            accuracy_checks += 1
            current_year = datetime.now().year
            if (df['year'] >= 2020) & (df['year'] <= current_year + 1).all():
                passed_checks += 1
        
        return passed_checks / accuracy_checks if accuracy_checks > 0 else 1.0
    
    def _assess_consistency(self, df: pd.DataFrame, data_type: str) -> float:
        """Assess data consistency"""
        consistency_checks = 0
        passed_checks = 0
        
        # Check for duplicate IDs
        if 'grant_id' in df.columns:
            consistency_checks += 1
            if df['grant_id'].nunique() == len(df):
                passed_checks += 1
        
        if 'publication_id' in df.columns:
            consistency_checks += 1
            if df['publication_id'].nunique() == len(df):
                passed_checks += 1
        
        # Check for logical consistency
        if 'budget' in df.columns and 'currency' in df.columns:
            consistency_checks += 1
            # Budget should be positive for all records
            if (df['budget'] > 0).all():
                passed_checks += 1
        
        # Check for date consistency
        if 'deadline' in df.columns:
            consistency_checks += 1
            try:
                deadlines = pd.to_datetime(df['deadline'])
                # Deadlines should be in the future
                if (deadlines > datetime.now()).all():
                    passed_checks += 1
            except:
                pass
        
        return passed_checks / consistency_checks if consistency_checks > 0 else 1.0
    
    def _assess_timeliness(self, df: pd.DataFrame, data_type: str) -> float:
        """Assess data timeliness"""
        if 'collected_at' not in df.columns:
            return 1.0  # Can't assess timeliness without collection date
        
        try:
            collection_dates = pd.to_datetime(df['collected_at'])
            days_old = (datetime.now() - collection_dates).dt.days
            
            # Data is considered timely if collected within last 30 days
            timely_data = (days_old <= 30).sum()
            timeliness_score = timely_data / len(df)
            
            return timeliness_score
        except:
            return 1.0  # Default to timely if can't assess
    
    def _identify_issues(self, df: pd.DataFrame, data_type: str) -> List[str]:
        """Identify specific data quality issues"""
        issues = []
        
        # Check for missing required fields
        if data_type == 'grants':
            required_fields = ['grant_id', 'title', 'budget']
        elif data_type == 'research':
            required_fields = ['publication_id', 'title']
        elif data_type == 'impact':
            required_fields = ['indicator_id', 'value']
        else:
            required_fields = ['grant_id', 'title']
        
        for field in required_fields:
            if field in df.columns and df[field].isnull().sum() > 0:
                issues.append(f"Missing {field} in {df[field].isnull().sum()} records")
        
        # Check for invalid budgets
        if 'budget' in df.columns:
            invalid_budgets = (df['budget'] <= 0).sum()
            if invalid_budgets > 0:
                issues.append(f"Invalid budget values in {invalid_budgets} records")
        
        # Check for old data
        if 'collected_at' in df.columns:
            try:
                collection_dates = pd.to_datetime(df['collected_at'])
                old_data = (datetime.now() - collection_dates).dt.days > 30
                if old_data.sum() > 0:
                    issues.append(f"Data older than 30 days in {old_data.sum()} records")
            except:
                pass
        
        return issues
    
    def _generate_recommendations(self, df: pd.DataFrame, data_type: str, quality_score: float) -> List[str]:
        """Generate recommendations for improving data quality"""
        recommendations = []
        
        if quality_score < self.quality_thresholds['completeness']:
            recommendations.append("Implement data validation at source to ensure completeness")
        
        if quality_score < self.quality_thresholds['accuracy']:
            recommendations.append("Add data validation rules for budget, currency, and date fields")
        
        if quality_score < self.quality_thresholds['consistency']:
            recommendations.append("Implement duplicate detection and removal processes")
        
        if quality_score < self.quality_thresholds['timeliness']:
            recommendations.append("Set up automated data collection with regular refresh schedules")
        
        if len(df) < 100:
            recommendations.append("Collect more data to improve statistical significance")
        
        if 'budget' in df.columns and df['budget'].std() == 0:
            recommendations.append("Diversify data sources to get more varied budget ranges")
        
        return recommendations
    
    def generate_quality_report(self) -> Dict[str, Any]:
        """Generate comprehensive quality report for all data types"""
        data_types = ['grants', 'research', 'impact']
        report = {
            'overall_quality_score': 0.0,
            'data_types': {},
            'summary': {},
            'recommendations': []
        }
        
        total_score = 0
        total_records = 0
        
        for data_type in data_types:
            assessment = self.assess_data_quality(data_type)
            report['data_types'][data_type] = assessment
            
            if assessment['total_records'] > 0:
                total_score += assessment['quality_score']
                total_records += assessment['total_records']
        
        if len(data_types) > 0:
            report['overall_quality_score'] = total_score / len(data_types)
        
        report['summary'] = {
            'total_records': total_records,
            'data_types_assessed': len(data_types),
            'quality_threshold': self.quality_thresholds['completeness'],
            'report_generated': datetime.now().isoformat()
        }
        
        # Generate overall recommendations
        overall_recommendations = []
        for data_type, assessment in report['data_types'].items():
            if assessment['quality_score'] < self.quality_thresholds['completeness']:
                overall_recommendations.append(f"Improve {data_type} data quality")
        
        if total_records < 1000:
            overall_recommendations.append("Increase data collection volume")
        
        report['recommendations'] = overall_recommendations
        
        return report

def main():
    """Main function to run data quality assessment"""
    qa = DataQualityAssurance()
    
    # Generate comprehensive quality report
    report = qa.generate_quality_report()
    
    print("📊 Data Quality Assessment Report")
    print("=" * 50)
    print(f"Overall Quality Score: {report['overall_quality_score']:.2%}")
    print(f"Total Records: {report['summary']['total_records']}")
    print(f"Data Types Assessed: {report['summary']['data_types_assessed']}")
    print()
    
    for data_type, assessment in report['data_types'].items():
        print(f"📋 {data_type.upper()} Data:")
        print(f"  - Records: {assessment['total_records']}")
        print(f"  - Quality Score: {assessment['quality_score']:.2%}")
        print(f"  - Issues: {len(assessment['issues'])}")
        print()
    
    if report['recommendations']:
        print("🔧 Recommendations:")
        for rec in report['recommendations']:
            print(f"  - {rec}")
    
    # Save report to file
    with open('data_quality_report.json', 'w') as f:
        json.dump(report, f, indent=2, default=str)
    
    print(f"\n✅ Quality report saved to data_quality_report.json")

if __name__ == "__main__":
    main() 