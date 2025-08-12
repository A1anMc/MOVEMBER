# 🎯 **PRACTICAL EXERCISES**
**Movember AI Rules System - Hands-on Training Exercises**

**Version:** 1.0  
**Date:** August 12, 2025  
**Status:** 🚀 **READY FOR TRAINING**

---

## 📊 **EXERCISE OVERVIEW**

### **🎯 Exercise Objectives**
- **Hands-on Practice:** Real-world application of system features
- **Skill Development:** Practical mastery of all system modules
- **Confidence Building:** Increased user confidence through practice
- **Problem Solving:** Real-world scenario-based learning

### **⏱️ Exercise Structure**
- **Duration:** 30-45 minutes per exercise
- **Difficulty:** Beginner to Advanced
- **Prerequisites:** Module completion and basic system knowledge
- **Assessment:** Performance evaluation and feedback

---

## 📚 **MODULE 1: SYSTEM FUNDAMENTALS**

### **Exercise 1.1: System Health Check**
**Objective:** Verify system status and access basic endpoints

#### **Tasks:**
1. **Health Check**
   ```bash
   curl http://localhost:8000/health/
   ```
   - Verify system status is "healthy"
   - Check uptime percentage
   - Review active rules count

2. **API Documentation Access**
   - Navigate to `http://localhost:8000/docs`
   - Explore available endpoints
   - Test basic GET requests

3. **Monitoring Dashboard**
   ```bash
   curl http://localhost:8000/monitoring/health
   ```
   - Check monitoring system status
   - Review system metrics
   - Verify monitoring is active

#### **Success Criteria:**
- ✅ System health endpoint returns "healthy" status
- ✅ Swagger UI loads and displays endpoints
- ✅ Monitoring system is operational
- ✅ All basic endpoints respond correctly

---

### **Exercise 1.2: Authentication and Security**
**Objective:** Understand authentication and security features

#### **Tasks:**
1. **API Access Test**
   ```bash
   # Test without authentication
   curl http://localhost:8000/metrics/
   
   # Test with authentication (if configured)
   curl -H "Authorization: Bearer YOUR_TOKEN" http://localhost:8000/metrics/
   ```

2. **Role-based Access**
   - Test different user roles
   - Verify permission restrictions
   - Check audit logging

3. **Security Compliance**
   - Review GDPR compliance features
   - Check data protection measures
   - Verify privacy controls

#### **Success Criteria:**
- ✅ API access works with proper authentication
- ✅ Role-based permissions function correctly
- ✅ Security features are properly configured
- ✅ Compliance requirements are met

---

## 📊 **MODULE 2: IMPACT MEASUREMENT**

### **Exercise 2.1: Impact Metrics Creation**
**Objective:** Create and manage impact metrics

#### **Tasks:**
1. **Create Impact Metric**
   ```python
   import requests
   
   metric_data = {
       "name": "Men's Health Awareness Campaign",
       "category": "mens_health_awareness",
       "value": 85.5,
       "unit": "percentage",
       "baseline": 75.0,
       "target": 90.0,
       "data_source": "Survey Results",
       "collection_method": "Online Survey"
   }
   
   response = requests.post('http://localhost:8000/metrics/', json=metric_data)
   print(response.json())
   ```

2. **Retrieve Metrics**
   ```python
   response = requests.get('http://localhost:8000/metrics/')
   metrics = response.json()
   
   # Filter by category
   mens_health_metrics = [m for m in metrics['metrics'] if m['category'] == 'mens_health_awareness']
   print(f"Found {len(mens_health_metrics)} men's health metrics")
   ```

3. **Create Impact Report**
   ```python
   report_data = {
       "title": "Monthly Impact Report - August 2025",
       "period_start": "2025-08-01",
       "period_end": "2025-08-31",
       "metrics": [
           {
               "name": "Men's Health Awareness",
               "category": "mens_health_awareness",
               "value": 85.5,
               "unit": "percentage"
           },
           {
               "name": "Mental Health Support",
               "category": "mental_health",
               "value": 78.2,
               "unit": "percentage"
           }
       ]
   }
   
   response = requests.post('http://localhost:8000/reports/', json=report_data)
   print(response.json())
   ```

#### **Success Criteria:**
- ✅ Impact metric created successfully
- ✅ Metrics retrieved and filtered correctly
- ✅ Impact report generated with proper formatting
- ✅ UK spelling and AUD currency compliance verified

---

### **Exercise 2.2: Data Integration and Validation**
**Objective:** Work with real data integration and validation

#### **Tasks:**
1. **External Data Upload**
   ```python
   # Upload external data file
   with open('health_data.csv', 'rb') as file:
       files = {'file': file}
       response = requests.post('http://localhost:8000/external-data/', files=files)
       print(response.json())
   ```

2. **Data Validation**
   ```python
   # Test data validation
   validation_data = {
       "data_source": "Movember Annual Report 2024",
       "validation_rules": ["completeness", "accuracy", "consistency"],
       "data": sample_data
   }
   
   response = requests.post('http://localhost:8000/data/validate', json=validation_data)
   print(response.json())
   ```

3. **Fallback Data Handling**
   - Test system behavior when external data is unavailable
   - Verify fallback data is used correctly
   - Check error handling and logging

#### **Success Criteria:**
- ✅ External data uploaded successfully
- ✅ Data validation returns expected results
- ✅ Fallback data handling works correctly
- ✅ Error handling is robust and informative

---

## 💰 **MODULE 3: GRANT ACQUISITION**

### **Exercise 3.1: Grant Application Creation**
**Objective:** Create and manage grant applications

#### **Tasks:**
1. **Create Grant Application**
   ```python
   grant_data = {
       "grant_id": "GRANT_2025_001",
       "title": "Men's Mental Health Research Initiative",
       "description": "Comprehensive study on mental health interventions for men aged 25-55",
       "budget": 750000,
       "timeline_months": 36,
       "organisation": "Movember Foundation",
       "contact_person": "Dr. Sarah Johnson",
       "email": "sarah.johnson@movember.com",
       "category": "research",
       "research_areas": ["mental_health", "intervention_studies"],
       "expected_outcomes": [
           "Improved mental health screening tools",
           "Enhanced intervention strategies",
           "Policy recommendations"
       ]
   }
   
   response = requests.post('http://localhost:8000/grants/', json=grant_data)
   print(response.json())
   ```

2. **Retrieve Grant Details**
   ```python
   grant_id = "GRANT_2025_001"
   response = requests.get(f'http://localhost:8000/grants/{grant_id}')
   grant = response.json()
   
   print(f"Grant: {grant['title']}")
   print(f"Budget: AUD {grant['budget']:,}")
   print(f"Timeline: {grant['timeline_months']} months")
   ```

3. **AI Success Prediction**
   ```python
   # Get AI-powered success prediction
   prediction_data = {
       "grant_id": "GRANT_2025_001",
       "analysis_type": "success_prediction"
   }
   
   response = requests.post('http://localhost:8000/grants/predict', json=prediction_data)
   prediction = response.json()
   
   print(f"Success Probability: {prediction['success_probability']:.1%}")
   print(f"Key Factors: {prediction['key_factors']}")
   print(f"Recommendations: {prediction['recommendations']}")
   ```

#### **Success Criteria:**
- ✅ Grant application created with all required fields
- ✅ Grant details retrieved correctly
- ✅ AI prediction provides meaningful insights
- ✅ Budget and timeline are properly formatted

---

### **Exercise 3.2: Grant Optimization**
**Objective:** Use AI insights to optimize grant applications

#### **Tasks:**
1. **Optimization Analysis**
   ```python
   optimization_data = {
       "grant_id": "GRANT_2025_001",
       "optimization_type": "budget_allocation",
       "constraints": {
           "max_budget": 1000000,
           "min_timeline": 24,
           "required_outcomes": ["policy_recommendations"]
       }
   }
   
   response = requests.post('http://localhost:8000/grants/optimize', json=optimization_data)
   optimization = response.json()
   
   print("Optimization Results:")
   print(f"Recommended Budget: AUD {optimization['recommended_budget']:,}")
   print(f"Timeline: {optimization['recommended_timeline']} months")
   print(f"Expected Success Rate: {optimization['expected_success_rate']:.1%}")
   ```

2. **Risk Assessment**
   ```python
   risk_data = {
       "grant_id": "GRANT_2025_001",
       "risk_factors": ["budget_overrun", "timeline_delay", "scope_creep"]
   }
   
   response = requests.post('http://localhost:8000/grants/risk-assessment', json=risk_data)
   risks = response.json()
   
   print("Risk Assessment:")
   for risk in risks['risks']:
       print(f"- {risk['factor']}: {risk['probability']:.1%} probability, {risk['impact']} impact")
   ```

#### **Success Criteria:**
- ✅ Optimization analysis provides actionable recommendations
- ✅ Risk assessment identifies potential issues
- ✅ AI insights are relevant and useful
- ✅ Recommendations are within constraints

---

## 🔬 **MODULE 4: RESEARCH & INNOVATION HUB**

### **Exercise 4.1: Clinical Data Integration**
**Objective:** Search and analyze clinical research data

#### **Tasks:**
1. **Research Paper Search**
   ```python
   # Search for prostate cancer research papers
   search_params = {
       "query": "prostate cancer screening",
       "limit": 10,
       "category": "prostate_cancer"
   }
   
   response = requests.get('http://localhost:8000/research/papers/', params=search_params)
   papers = response.json()
   
   print(f"Found {papers['total_results']} papers:")
   for paper in papers['papers'][:3]:
       print(f"- {paper['title']}")
       print(f"  Relevance: {paper['relevance_score']:.1%}")
       print(f"  Publication Date: {paper['publication_date']}")
   ```

2. **Clinical Trials Search**
   ```python
   # Search for clinical trials
   trial_params = {
       "query": "mental health intervention",
       "status": "recruiting",
       "limit": 5
   }
   
   response = requests.get('http://localhost:8000/research/trials/', params=trial_params)
   trials = response.json()
   
   print(f"Found {trials['total_results']} clinical trials:")
   for trial in trials['trials'][:3]:
       print(f"- {trial['title']}")
       print(f"  Status: {trial['status']}")
       print(f"  Location: {trial['location']}")
   ```

3. **Research Insights Generation**
   ```python
   # Generate insights for mental health category
   response = requests.get('http://localhost:8000/research/insights/mental_health')
   insights = response.json()
   
   print(f"Generated {insights['total_insights']} insights:")
   for insight in insights['insights'][:3]:
       print(f"- {insight['title']}")
       print(f"  Confidence: {insight['confidence_level']:.1%}")
       print(f"  Clinical Relevance: {insight['clinical_relevance']}")
   ```

#### **Success Criteria:**
- ✅ Research papers found and ranked by relevance
- ✅ Clinical trials retrieved with proper filtering
- ✅ Research insights generated with confidence levels
- ✅ Data quality and relevance verified

---

### **Exercise 4.2: Research Collaboration**
**Objective:** Set up and manage research collaboration

#### **Tasks:**
1. **Create Research Project**
   ```python
   project_data = {
       "title": "Advanced Prostate Cancer Treatment Study",
       "description": "Multi-institution study on novel treatment approaches",
       "lead_institution": "University of Melbourne",
       "collaborating_institutions": ["Prostate Cancer Foundation", "Movember Foundation"],
       "research_areas": ["prostate_cancer", "treatment", "clinical_trials"],
       "budget": 2000000,
       "timeline_months": 48
   }
   
   response = requests.post('http://localhost:8000/research/projects/', json=project_data)
   project = response.json()
   
   print(f"Project created: {project['project_id']}")
   print(f"Title: {project['title']}")
   print(f"Status: {project['status']}")
   ```

2. **Collaboration Network Analysis**
   ```python
   response = requests.get('http://localhost:8000/research/collaboration/network')
   network = response.json()
   
   print("Collaboration Network:")
   print(f"Total Institutions: {network['total_institutions']}")
   print(f"Active Projects: {network['active_projects']}")
   print(f"Collaboration Score: {network['collaboration_score']:.2f}")
   ```

3. **Publication Pipeline**
   ```python
   # Get publication statistics
   response = requests.get('http://localhost:8000/research/publications/stats')
   stats = response.json()
   
   print("Publication Statistics:")
   print(f"Total Publications: {stats['total_publications']}")
   print(f"Published: {stats['published']}")
   print(f"Under Review: {stats['under_review']}")
   print(f"Average Citations: {stats['average_citations']:.1f}")
   ```

#### **Success Criteria:**
- ✅ Research project created with proper collaboration setup
- ✅ Network analysis provides meaningful insights
- ✅ Publication statistics are accurate and useful
- ✅ Collaboration features work correctly

---

## 📈 **MODULE 5: ADVANCED ANALYTICS**

### **Exercise 5.1: Predictive Analytics**
**Objective:** Use predictive models for trend analysis

#### **Tasks:**
1. **Trend Prediction**
   ```python
   prediction_data = {
       "metric": "mens_health_awareness",
       "period_months": 12,
       "confidence_level": 0.95
   }
   
   response = requests.post('http://localhost:8000/analytics/predict', json=prediction_data)
   prediction = response.json()
   
   print("Trend Prediction:")
   print(f"Current Value: {prediction['current_value']:.1f}%")
   print(f"Predicted Value (12 months): {prediction['predicted_value']:.1f}%")
   print(f"Confidence Interval: {prediction['confidence_interval']}")
   print(f"Key Factors: {prediction['key_factors']}")
   ```

2. **Grant Success Prediction**
   ```python
   grant_prediction_data = {
       "grant_id": "GRANT_2025_001",
       "prediction_type": "success_probability",
       "model_version": "latest"
   }
   
   response = requests.post('http://localhost:8000/analytics/grant-prediction', json=grant_prediction_data)
   grant_prediction = response.json()
   
   print("Grant Success Prediction:")
   print(f"Success Probability: {grant_prediction['success_probability']:.1%}")
   print(f"Model Accuracy: {grant_prediction['model_accuracy']:.1%}")
   print(f"Key Predictors: {grant_prediction['key_predictors']}")
   print(f"Recommendations: {grant_prediction['recommendations']}")
   ```

#### **Success Criteria:**
- ✅ Trend predictions are reasonable and well-explained
- ✅ Grant success predictions provide actionable insights
- ✅ Model accuracy and confidence levels are provided
- ✅ Recommendations are practical and useful

---

### **Exercise 5.2: Real-time Analytics Dashboard**
**Objective:** Create and customize analytics dashboards

#### **Tasks:**
1. **Dashboard Creation**
   ```python
   dashboard_data = {
       "title": "Executive Impact Dashboard",
       "widgets": [
           {
               "type": "metric_summary",
               "title": "Key Performance Indicators",
               "metrics": ["mens_health_awareness", "grant_success_rate", "research_publications"]
           },
           {
               "type": "trend_chart",
               "title": "Impact Trends",
               "metric": "mens_health_awareness",
               "period": "12_months"
           },
           {
               "type": "alert_summary",
               "title": "System Alerts",
               "alert_levels": ["warning", "error", "critical"]
           }
       ]
   }
   
   response = requests.post('http://localhost:8000/dashboard/create', json=dashboard_data)
   dashboard = response.json()
   
   print(f"Dashboard created: {dashboard['dashboard_id']}")
   print(f"URL: {dashboard['url']}")
   ```

2. **Real-time Data Visualization**
   ```python
   # Get real-time metrics for dashboard
   response = requests.get('http://localhost:8000/analytics/realtime')
   realtime_data = response.json()
   
   print("Real-time Analytics:")
   print(f"Active Users: {realtime_data['active_users']}")
   print(f"System Performance: {realtime_data['system_performance']:.1f}%")
   print(f"Recent Alerts: {realtime_data['recent_alerts']}")
   print(f"Data Freshness: {realtime_data['data_freshness']} seconds ago")
   ```

#### **Success Criteria:**
- ✅ Dashboard created with proper widgets and layout
- ✅ Real-time data updates correctly
- ✅ Visualizations are clear and informative
- ✅ Dashboard is accessible and functional

---

## ⚙️ **MODULE 6: SYSTEM ADMINISTRATION**

### **Exercise 6.1: Monitoring and Maintenance**
**Objective:** Manage system monitoring and maintenance

#### **Tasks:**
1. **Monitoring Configuration**
   ```python
   # Update monitoring thresholds
   thresholds = {
       "cpu_usage": 75.0,
       "memory_usage": 80.0,
       "disk_usage": 85.0,
       "response_time": 1.5,
       "error_rate": 2.0
   }
   
   response = requests.put('http://localhost:8000/monitoring/thresholds', json=thresholds)
   result = response.json()
   
   print("Thresholds updated:")
   for key, value in result['thresholds'].items():
       print(f"- {key}: {value}")
   ```

2. **Alert Management**
   ```python
   # Get active alerts
   response = requests.get('http://localhost:8000/monitoring/alerts?active_only=true')
   alerts = response.json()
   
   print(f"Active Alerts: {alerts['total_alerts']}")
   for alert in alerts['alerts'][:3]:
       print(f"- {alert['title']}: {alert['level']}")
       print(f"  Message: {alert['message']}")
       print(f"  Time: {alert['timestamp']}")
   ```

3. **Performance Optimization**
   ```python
   # Get performance summary
   response = requests.get('http://localhost:8000/monitoring/performance?hours=24')
   performance = response.json()
   
   print("Performance Summary (24 hours):")
   print(f"Total Metrics: {performance['total_metrics']}")
   print(f"Average Response Time: {performance['average_response_time']:.2f}ms")
   print(f"Error Rate: {performance['error_rate']:.2f}%")
   print(f"Uptime: {performance['uptime']:.1f}%")
   ```

#### **Success Criteria:**
- ✅ Monitoring thresholds updated successfully
- ✅ Alert management provides clear information
- ✅ Performance metrics are accurate and useful
- ✅ System optimization recommendations are actionable

---

## 📊 **ASSESSMENT CRITERIA**

### **Performance Evaluation**
- **Task Completion:** 90% of tasks completed successfully
- **Accuracy:** 85% accuracy in data handling and analysis
- **Efficiency:** Tasks completed within time limits
- **Problem Solving:** Ability to troubleshoot and resolve issues
- **Best Practices:** Proper usage of system features and security

### **Certification Levels**
- **Basic:** Complete all Module 1-2 exercises
- **Intermediate:** Complete all Module 1-4 exercises
- **Advanced:** Complete all Module 1-6 exercises with 90%+ accuracy

### **Feedback and Improvement**
- **Exercise Feedback:** Detailed feedback on performance
- **Skill Gap Analysis:** Identification of areas for improvement
- **Additional Training:** Recommendations for further development
- **Continuous Learning:** Ongoing skill development opportunities

---

**Practical Exercises Created:** August 12, 2025  
**Status:** 🚀 **READY FOR TRAINING**

**These hands-on exercises will ensure users develop practical mastery of the Movember AI Rules System and can effectively apply their knowledge in real-world scenarios.**
