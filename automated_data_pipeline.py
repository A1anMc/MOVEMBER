#!/usr/bin/env python3
"""
Automated Data Pipeline for Movember AI Rules System
Continuous collection, processing, and quality assurance of real data
"""
import asyncio
import schedule
import time
import logging
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Any
import json
from real_data_sources import RealDataCollector
from data_quality_assurance import DataQualityAssurance
import numpy as np

class AutomatedDataPipeline:
    def __init__(self):
        self.collector = RealDataCollector()
        self.qa = DataQualityAssurance()
        self.logger = logging.getLogger(__name__)
        
        # Pipeline configuration
        self.schedule_config = {
            'grants': {
                'frequency': 'daily',
                'time': '09:00',
                'sources': ['grantconnect', 'charity_commission', 'research_council']
            },
            'research': {
                'frequency': 'weekly',
                'time': '10:00',
                'sources': ['pubmed', 'researchgate', 'arxiv']
            },
            'impact': {
                'frequency': 'monthly',
                'time': '11:00',
                'sources': ['sdg_database', 'who_health_data', 'unicef_data']
            }
        }
        
        # Performance tracking
        self.performance_metrics = {
            'last_run': {},
            'success_count': {},
            'error_count': {},
            'data_volume': {}
        }
    
    async def run_data_collection(self, data_type: str):
        """Run data collection for specific type"""
        try:
            self.logger.info(f"Starting {data_type} data collection...")
            start_time = datetime.now()
            
            if data_type == 'grants':
                data = await self.collector.collect_real_grants_data()
            elif data_type == 'research':
                data = await self.collector.collect_real_research_data()
            elif data_type == 'impact':
                data = await self.collector.collect_real_impact_data()
            else:
                raise ValueError(f"Unknown data type: {data_type}")
            
            # Store the data
            self.collector.store_real_data(data, data_type)
            
            # Update performance metrics
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            self.performance_metrics['last_run'][data_type] = end_time.isoformat()
            self.performance_metrics['success_count'][data_type] = self.performance_metrics['success_count'].get(data_type, 0) + 1
            self.performance_metrics['data_volume'][data_type] = len(data)
            
            self.logger.info(f"✅ {data_type} collection completed: {len(data)} records in {duration:.2f}s")
            
            # Run quality assessment
            await self.run_quality_assessment(data_type)
            
        except Exception as e:
            self.logger.error(f"❌ Error in {data_type} collection: {e}")
            self.performance_metrics['error_count'][data_type] = self.performance_metrics['error_count'].get(data_type, 0) + 1
    
    async def run_quality_assessment(self, data_type: str):
        """Run quality assessment for collected data"""
        try:
            self.logger.info(f"Running quality assessment for {data_type}...")
            
            assessment = self.qa.assess_data_quality(data_type)
            
            # Store quality assessment results
            self._store_quality_assessment(assessment)
            
            # Alert if quality is below threshold
            if assessment['quality_score'] < self.qa.quality_thresholds['completeness']:
                self.logger.warning(f"⚠️ {data_type} data quality below threshold: {assessment['quality_score']:.2%}")
                
                # Generate alert
                await self._generate_quality_alert(data_type, assessment)
            
            self.logger.info(f"✅ Quality assessment completed for {data_type}")
            
        except Exception as e:
            self.logger.error(f"❌ Error in quality assessment for {data_type}: {e}")
    
    def _store_quality_assessment(self, assessment: Dict[str, Any]):
        """Store quality assessment results"""
        conn = sqlite3.connect(self.collector.db_path)
        cursor = conn.cursor()
        
        # Create quality assessment table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS quality_assessments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data_type TEXT NOT NULL,
                quality_score REAL,
                total_records INTEGER,
                completeness_score REAL,
                accuracy_score REAL,
                consistency_score REAL,
                timeliness_score REAL,
                issues TEXT,
                recommendations TEXT,
                assessment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Store assessment
        cursor.execute("""
            INSERT INTO quality_assessments 
            (data_type, quality_score, total_records, completeness_score, 
             accuracy_score, consistency_score, timeliness_score, issues, recommendations)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            assessment['data_type'],
            assessment['quality_score'],
            assessment['total_records'],
            assessment['completeness_score'],
            assessment['accuracy_score'],
            assessment['consistency_score'],
            assessment['timeliness_score'],
            json.dumps(assessment['issues']),
            json.dumps(assessment['recommendations'])
        ))
        
        conn.commit()
        conn.close()
    
    async def _generate_quality_alert(self, data_type: str, assessment: Dict[str, Any]):
        """Generate quality alert for low-quality data"""
        alert = {
            'type': 'quality_alert',
            'data_type': data_type,
            'quality_score': assessment['quality_score'],
            'threshold': self.qa.quality_thresholds['completeness'],
            'issues': assessment['issues'],
            'recommendations': assessment['recommendations'],
            'timestamp': datetime.now().isoformat()
        }
        
        # Store alert
        conn = sqlite3.connect(self.collector.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS quality_alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                alert_type TEXT NOT NULL,
                data_type TEXT NOT NULL,
                quality_score REAL,
                threshold REAL,
                issues TEXT,
                recommendations TEXT,
                alert_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            INSERT INTO quality_alerts 
            (alert_type, data_type, quality_score, threshold, issues, recommendations)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            alert['type'],
            alert['data_type'],
            alert['quality_score'],
            alert['threshold'],
            json.dumps(alert['issues']),
            json.dumps(alert['recommendations'])
        ))
        
        conn.commit()
        conn.close()
        
        self.logger.warning(f"🚨 Quality alert generated for {data_type}")
    
    def setup_schedules(self):
        """Setup automated schedules"""
        # Daily grants collection
        schedule.every().day.at("09:00").do(
            lambda: asyncio.run(self.run_data_collection('grants'))
        )
        
        # Weekly research collection
        schedule.every().monday.at("10:00").do(
            lambda: asyncio.run(self.run_data_collection('research'))
        )
        
        # Monthly impact collection
        schedule.every().month.at("11:00").do(
            lambda: asyncio.run(self.run_data_collection('impact'))
        )
        
        # Daily quality assessment
        schedule.every().day.at("12:00").do(
            lambda: asyncio.run(self.run_full_quality_assessment())
        )
        
        # Weekly performance report
        schedule.every().friday.at("14:00").do(
            lambda: asyncio.run(self.generate_performance_report())
        )
    
    async def run_full_quality_assessment(self):
        """Run quality assessment for all data types"""
        self.logger.info("Running full quality assessment...")
        
        data_types = ['grants', 'research', 'impact']
        for data_type in data_types:
            await self.run_quality_assessment(data_type)
        
        self.logger.info("✅ Full quality assessment completed")
    
    async def generate_performance_report(self):
        """Generate weekly performance report"""
        self.logger.info("Generating performance report...")
        
        report = {
            'period': 'weekly',
            'generated_at': datetime.now().isoformat(),
            'performance_metrics': self.performance_metrics,
            'quality_summary': {},
            'recommendations': []
        }
        
        # Get quality summary
        qa = DataQualityAssurance()
        for data_type in ['grants', 'research', 'impact']:
            assessment = qa.assess_data_quality(data_type)
            report['quality_summary'][data_type] = {
                'quality_score': assessment['quality_score'],
                'total_records': assessment['total_records'],
                'issues_count': len(assessment['issues'])
            }
        
        # Generate recommendations
        overall_quality = np.mean([report['quality_summary'][dt]['quality_score'] for dt in report['quality_summary']])
        if overall_quality < 0.8:
            report['recommendations'].append("Overall data quality needs improvement")
        
        # Save report
        with open(f'performance_report_{datetime.now().strftime("%Y%m%d")}.json', 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        self.logger.info("✅ Performance report generated")
    
    def start_pipeline(self):
        """Start the automated data pipeline"""
        self.logger.info("🚀 Starting automated data pipeline...")
        
        # Setup schedules
        self.setup_schedules()
        
        # Run initial collection
        asyncio.run(self.run_data_collection('grants'))
        asyncio.run(self.run_data_collection('research'))
        asyncio.run(self.run_data_collection('impact'))
        
        # Start scheduling loop
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute

def main():
    """Main function to start the pipeline"""
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('data_pipeline.log'),
            logging.StreamHandler()
        ]
    )
    
    # Start pipeline
    pipeline = AutomatedDataPipeline()
    pipeline.start_pipeline()

if __name__ == "__main__":
    main() 