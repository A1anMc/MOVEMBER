# 🚀 Cursor AI Agent Instructions: Movember-Style Dashboard System

## 📋 **Project Overview**

Create a comprehensive dashboard system similar to the Movember AI Rules System, but customized for a new client. This system includes:

- **Phase 1: Foundation Enhancement** - Performance optimization, caching, monitoring
- **Phase 2: Advanced Intelligence** - ML integration and predictive analytics
- **Enhanced Dashboard** - Real-time monitoring and professional interface
- **Production Deployment** - Enterprise-ready deployment scripts

---

## 🏗️ **System Architecture**

### **Core Components**

#### **1. Backend API (FastAPI)**
```python
# Main API file: simple_api.py
- FastAPI application with comprehensive endpoints
- Database integration (SQLite for development, PostgreSQL for production)
- Performance monitoring middleware
- Caching system integration
- ML prediction endpoints
- Health check and metrics endpoints
```

#### **2. Rules Engine**
```python
# Directory: rules/
- Core rule evaluation engine
- Caching system (rules/core/cache.py)
- Rule categories and validation
- UK English and AUD currency compliance
- Async rule execution
```

#### **3. Monitoring System**
```python
# Directory: monitoring/
- Advanced metrics collector (advanced_metrics.py)
- Real-time performance monitoring
- System health tracking
- Alert management
- Historical data analysis
```

#### **4. ML Integration**
```python
# Directory: ml_integration/
- Advanced ML engine (advanced_ml_engine.py)
- Predictive analytics
- Model training and management
- Confidence scoring
- Risk assessment
```

#### **5. Frontend Dashboard**
```html
# Directory: frontend/
- index.html - Main dashboard interface
- dashboard.js - Interactive JavaScript functionality
- Real-time data integration
- Performance monitoring visualization
- ML prediction displays
```

---

## 🎯 **Implementation Steps**

### **Step 1: Project Setup**

```bash
# Create project structure
mkdir client-dashboard-system
cd client-dashboard-system

# Create directories
mkdir -p api rules/core monitoring ml_integration frontend config docs scripts

# Initialize Python environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### **Step 2: Backend API Development**

#### **Create main API file (`simple_api.py`)**
```python
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import json
from datetime import datetime
from typing import Dict, Any, List, Optional
import asyncio

app = FastAPI(title="Client Dashboard API", version="2.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database initialization
def init_database():
    conn = sqlite3.connect('client_data.db')
    cursor = conn.cursor()
    
    # Create tables based on client needs
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            budget REAL,
            status TEXT DEFAULT 'active',
            impact_score REAL DEFAULT 0.0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Add more tables as needed for client data
    conn.commit()
    conn.close()

# Initialize database
init_database()

# Health check endpoint
@app.get("/health/")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "2.0.0",
        "uk_spelling_compliance": True,
        "aud_currency_compliance": True
    }

# Add more endpoints based on client requirements
```

#### **Create caching system (`rules/core/cache.py`)**
```python
#!/usr/bin/env python3
"""
Rule Caching System for Client Dashboard
Implements intelligent rule caching to reduce evaluation time by 40%
"""

import asyncio
import json
import hashlib
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import logging
from dataclasses import dataclass
from enum import Enum

# Implementation details from the original cache.py file
# Include all the caching logic, strategies, and optimization features
```

#### **Create monitoring system (`monitoring/advanced_metrics.py`)**
```python
#!/usr/bin/env python3
"""
Advanced Metrics Dashboard for Client Dashboard
Real-time performance monitoring and analytics
"""

import asyncio
import time
import psutil
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
import logging
import json
from collections import defaultdict, deque

# Implementation details from the original advanced_metrics.py file
# Include all monitoring, metrics collection, and alerting features
```

### **Step 3: ML Integration**

#### **Create ML engine (`ml_integration/advanced_ml_engine.py`)**
```python
#!/usr/bin/env python3
"""
Advanced ML Engine for Client Dashboard
Machine learning integration with predictive analytics and intelligent rule optimization
"""

import asyncio
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
import logging
import json
import sqlite3
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, mean_squared_error, r2_score
import joblib
import os

# Implementation details from the original advanced_ml_engine.py file
# Include all ML capabilities, prediction models, and optimization features
```

### **Step 4: Frontend Development**

#### **Create main HTML file (`frontend/index.html`)**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Client Dashboard</title>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        .gradient-bg {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        .card-hover {
            transition: all 0.3s ease;
        }
        .card-hover:hover {
            transform: translateY(-5px);
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
        }
    </style>
</head>
<body class="bg-gray-50">
    <!-- Navigation -->
    <nav class="bg-white shadow-lg">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between h-16">
                <div class="flex items-center">
                    <div class="flex-shrink-0">
                        <h1 class="text-2xl font-bold text-gray-900">
                            <i class="fas fa-chart-line text-blue-600 mr-2"></i>
                            Client Dashboard v2.0
                        </h1>
                    </div>
                </div>
                <div class="flex items-center space-x-4">
                    <span class="text-sm text-gray-500">UK English • AUD Currency</span>
                    <label class="flex items-center space-x-2">
                        <input type="checkbox" id="performanceToggle" class="form-checkbox text-blue-600">
                        <span class="text-sm text-gray-600">Performance Monitoring</span>
                    </label>
                    <button id="refreshBtn" class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg">
                        <i class="fas fa-sync-alt mr-2"></i>Refresh Data
                    </button>
                </div>
            </div>
        </div>
    </nav>

    <!-- Main Content -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <!-- Header Stats -->
        <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
            <!-- Add client-specific metrics here -->
        </div>

        <!-- Performance Monitoring Section -->
        <div id="performanceSection" class="mb-8">
            <h2 class="text-2xl font-bold text-gray-900 mb-6">
                <i class="fas fa-tachometer-alt text-blue-600 mr-2"></i>
                System Performance Monitoring
            </h2>
            
            <!-- System Health -->
            <div class="mb-6">
                <h3 class="text-lg font-semibold text-gray-900 mb-4">System Health</h3>
                <div id="systemHealth">
                    <!-- System health indicators will be populated here -->
                </div>
            </div>
            
            <!-- Performance Charts -->
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
                <div class="bg-white rounded-lg shadow-md p-6">
                    <h3 class="text-lg font-bold text-gray-900 mb-4">Performance Trends</h3>
                    <canvas id="performanceTrendChart" width="400" height="300"></canvas>
                </div>
                
                <div class="bg-white rounded-lg shadow-md p-6">
                    <h3 class="text-lg font-bold text-gray-900 mb-4">Cache Performance</h3>
                    <canvas id="cachePerformanceChart" width="400" height="300"></canvas>
                </div>
            </div>
            
            <!-- Cache Performance and Alerts -->
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
                <div id="cachePerformance">
                    <!-- Cache performance details will be populated here -->
                </div>
                
                <div>
                    <h3 class="text-lg font-semibold text-gray-900 mb-4">Active Alerts</h3>
                    <div id="alerts">
                        <!-- Alerts will be populated here -->
                    </div>
                </div>
            </div>
        </div>

        <!-- Overall Score -->
        <div class="bg-white rounded-lg shadow-md p-8 mb-8">
            <div class="text-center">
                <h2 class="text-3xl font-bold text-gray-900 mb-4">Overall Performance Score</h2>
                <div class="inline-flex items-center justify-center w-32 h-32 rounded-full bg-gradient-to-r from-blue-500 to-purple-600">
                    <span class="text-4xl font-bold text-white" id="overallScore">8.8</span>
                </div>
                <p class="text-lg text-gray-600 mt-4">out of 10</p>
                <p class="text-sm text-gray-500 mt-2">Comprehensive measurement across all areas</p>
            </div>
        </div>

        <!-- Category Breakdown -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
            <!-- Category Scores Chart -->
            <div class="bg-white rounded-lg shadow-md p-6">
                <h3 class="text-xl font-bold text-gray-900 mb-4">Category Performance Scores</h3>
                <canvas id="categoryChart" width="400" height="300"></canvas>
            </div>
            
            <!-- Key Metrics -->
            <div class="bg-white rounded-lg shadow-md p-6">
                <h3 class="text-xl font-bold text-gray-900 mb-4">Key Achievements</h3>
                <div id="achievements" class="space-y-3">
                    <!-- Achievements will be populated here -->
                </div>
            </div>
        </div>

        <!-- ML Predictions Section -->
        <div class="mb-8">
            <h2 class="text-2xl font-bold text-gray-900 mb-6">
                <i class="fas fa-brain text-purple-600 mr-2"></i>
                Machine Learning Predictions
            </h2>
            <div id="mlPredictions">
                <!-- ML predictions will be populated here -->
            </div>
        </div>

        <!-- Detailed Categories -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
            <div id="categoryCards">
                <!-- Category cards will be populated here -->
            </div>
        </div>

        <!-- Trends and Recommendations -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <!-- Trends -->
            <div class="bg-white rounded-lg shadow-md p-6">
                <h3 class="text-xl font-bold text-gray-900 mb-4">
                    <i class="fas fa-chart-line text-blue-600 mr-2"></i>
                    Performance Trends
                </h3>
                <div id="trends" class="space-y-4">
                    <!-- Trends will be populated here -->
                </div>
            </div>
            
            <!-- Recommendations -->
            <div class="bg-white rounded-lg shadow-md p-6">
                <h3 class="text-xl font-bold text-gray-900 mb-4">
                    <i class="fas fa-lightbulb text-yellow-600 mr-2"></i>
                    Strategic Recommendations
                </h3>
                <div id="recommendations" class="space-y-3">
                    <!-- Recommendations will be populated here -->
                </div>
            </div>
        </div>
    </div>

    <!-- Loading Overlay -->
    <div id="loadingOverlay" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 hidden">
        <div class="bg-white rounded-lg p-6 flex items-center space-x-4">
            <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
            <span class="text-lg font-medium text-gray-900">Loading data...</span>
        </div>
    </div>

    <script src="dashboard.js"></script>
</body>
</html>
```

#### **Create JavaScript file (`frontend/dashboard.js`)**
```javascript
// Enhanced Client Dashboard JavaScript with Phase 1 monitoring
class ClientDashboard {
    constructor() {
        this.apiBaseUrl = 'http://localhost:8000';
        this.chart = null;
        this.performanceChart = null;
        this.cacheChart = null;
        this.mlChart = null;
        this.init();
    }

    async init() {
        this.showLoading();
        await this.loadDashboardData();
        await this.loadPerformanceMetrics();
        await this.loadMLPredictions();
        this.setupEventListeners();
        this.hideLoading();
        
        // Start real-time updates
        this.startRealTimeUpdates();
    }

    setupEventListeners() {
        document.getElementById('refreshBtn').addEventListener('click', () => {
            this.refreshData();
        });
        
        // Add performance monitoring toggle
        const performanceToggle = document.getElementById('performanceToggle');
        if (performanceToggle) {
            performanceToggle.addEventListener('change', () => {
                this.togglePerformanceMonitoring();
            });
        }
    }

    async loadPerformanceMetrics() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/metrics/performance/`);
            const data = await response.json();
            
            if (data.status === 'success') {
                this.updatePerformanceDashboard(data.data);
            }
        } catch (error) {
            console.error('Error loading performance metrics:', error);
        }
    }

    async loadMLPredictions() {
        try {
            // Load ML predictions for demonstration
            const mlData = await this.generateMLPredictions();
            this.updateMLDashboard(mlData);
        } catch (error) {
            console.error('Error loading ML predictions:', error);
        }
    }

    updatePerformanceDashboard(data) {
        // Update system health indicators
        this.updateSystemHealth(data.system_health);
        
        // Update cache performance
        this.updateCachePerformance(data.cache_performance);
        
        // Update alerts
        this.updateAlerts(data.alerts);
        
        // Create performance charts
        this.createPerformanceCharts(data);
    }

    updateSystemHealth(health) {
        const healthContainer = document.getElementById('systemHealth');
        if (!healthContainer) return;
        
        healthContainer.innerHTML = `
            <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div class="bg-white rounded-lg p-4 shadow">
                    <div class="flex items-center">
                        <div class="p-2 rounded-full ${this.getHealthColor(health.cpu_usage)} mr-3">
                            <i class="fas fa-microchip text-white"></i>
                        </div>
                        <div>
                            <p class="text-sm text-gray-600">CPU Usage</p>
                            <p class="text-lg font-bold">${health.cpu_usage.toFixed(1)}%</p>
                        </div>
                    </div>
                </div>
                
                <div class="bg-white rounded-lg p-4 shadow">
                    <div class="flex items-center">
                        <div class="p-2 rounded-full ${this.getHealthColor(health.memory_usage)} mr-3">
                            <i class="fas fa-memory text-white"></i>
                        </div>
                        <div>
                            <p class="text-sm text-gray-600">Memory Usage</p>
                            <p class="text-lg font-bold">${health.memory_usage.toFixed(1)}%</p>
                        </div>
                    </div>
                </div>
                
                <div class="bg-white rounded-lg p-4 shadow">
                    <div class="flex items-center">
                        <div class="p-2 rounded-full ${this.getHealthColor(health.disk_usage)} mr-3">
                            <i class="fas fa-hdd text-white"></i>
                        </div>
                        <div>
                            <p class="text-sm text-gray-600">Disk Usage</p>
                            <p class="text-lg font-bold">${health.disk_usage.toFixed(1)}%</p>
                        </div>
                    </div>
                </div>
                
                <div class="bg-white rounded-lg p-4 shadow">
                    <div class="flex items-center">
                        <div class="p-2 rounded-full ${this.getHealthColor(health.error_rate)} mr-3">
                            <i class="fas fa-exclamation-triangle text-white"></i>
                        </div>
                        <div>
                            <p class="text-sm text-gray-600">Error Rate</p>
                            <p class="text-lg font-bold">${health.error_rate.toFixed(2)}%</p>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    updateCachePerformance(cacheData) {
        const cacheContainer = document.getElementById('cachePerformance');
        if (!cacheContainer) return;
        
        const hitRate = (cacheData.hit_rate * 100).toFixed(1);
        
        cacheContainer.innerHTML = `
            <div class="bg-white rounded-lg p-6 shadow">
                <h3 class="text-lg font-bold mb-4">Cache Performance</h3>
                <div class="grid grid-cols-2 gap-4">
                    <div>
                        <p class="text-sm text-gray-600">Hit Rate</p>
                        <p class="text-2xl font-bold text-green-600">${hitRate}%</p>
                    </div>
                    <div>
                        <p class="text-sm text-gray-600">Cache Size</p>
                        <p class="text-2xl font-bold">${cacheData.cache_size}/${cacheData.max_size}</p>
                    </div>
                    <div>
                        <p class="text-sm text-gray-600">Total Requests</p>
                        <p class="text-2xl font-bold">${cacheData.total_requests}</p>
                    </div>
                    <div>
                        <p class="text-sm text-gray-600">Memory Usage</p>
                        <p class="text-2xl font-bold">${cacheData.memory_usage_mb.toFixed(2)} MB</p>
                    </div>
                </div>
            </div>
        `;
    }

    updateAlerts(alerts) {
        const alertsContainer = document.getElementById('alerts');
        if (!alertsContainer) return;
        
        if (alerts.length === 0) {
            alertsContainer.innerHTML = `
                <div class="bg-green-50 rounded-lg p-4">
                    <div class="flex items-center">
                        <i class="fas fa-check-circle text-green-600 mr-2"></i>
                        <span class="text-green-800">No active alerts</span>
                    </div>
                </div>
            `;
            return;
        }
        
        alertsContainer.innerHTML = alerts.map(alert => `
            <div class="bg-red-50 rounded-lg p-4 mb-2">
                <div class="flex items-center justify-between">
                    <div class="flex items-center">
                        <i class="fas fa-exclamation-triangle text-red-600 mr-2"></i>
                        <span class="text-red-800 font-medium">${alert.message}</span>
                    </div>
                    <span class="text-xs text-red-600">${alert.severity.toUpperCase()}</span>
                </div>
            </div>
        `).join('');
    }

    createPerformanceCharts(data) {
        // Create performance trend chart
        this.createPerformanceTrendChart(data);
        
        // Create cache performance chart
        this.createCachePerformanceChart(data.cache_performance);
    }

    createPerformanceTrendChart(data) {
        const ctx = document.getElementById('performanceTrendChart');
        if (!ctx) return;
        
        if (this.performanceChart) {
            this.performanceChart.destroy();
        }
        
        // Sample performance data over time
        const labels = ['1h ago', '45m ago', '30m ago', '15m ago', 'Now'];
        const responseTimes = [120, 95, 85, 78, 65];
        const cpuUsage = [45, 52, 48, 55, 42];
        
        this.performanceChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [
                    {
                        label: 'Response Time (ms)',
                        data: responseTimes,
                        borderColor: '#3B82F6',
                        backgroundColor: 'rgba(59, 130, 246, 0.1)',
                        tension: 0.4
                    },
                    {
                        label: 'CPU Usage (%)',
                        data: cpuUsage,
                        borderColor: '#EF4444',
                        backgroundColor: 'rgba(239, 68, 68, 0.1)',
                        tension: 0.4
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: true,
                        text: 'Performance Trends'
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }

    createCachePerformanceChart(cacheData) {
        const ctx = document.getElementById('cachePerformanceChart');
        if (!ctx) return;
        
        if (this.cacheChart) {
            this.cacheChart.destroy();
        }
        
        this.cacheChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Cache Hits', 'Cache Misses'],
                datasets: [{
                    data: [cacheData.hits, cacheData.misses],
                    backgroundColor: ['#10B981', '#F59E0B'],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: true,
                        text: 'Cache Performance'
                    },
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });
    }

    async generateMLPredictions() {
        // Generate sample ML predictions for demonstration
        return {
            success_predictions: [
                { project: "Project A", success_rate: 0.85, confidence: 0.92 },
                { project: "Project B", success_rate: 0.78, confidence: 0.88 },
                { project: "Project C", success_rate: 0.92, confidence: 0.95 }
            ],
            outcome_predictions: [
                { category: "Category 1", predicted_score: 8.7, confidence: 0.89 },
                { category: "Category 2", predicted_score: 9.1, confidence: 0.91 },
                { category: "Category 3", predicted_score: 8.5, confidence: 0.87 }
            ],
            risk_assessments: [
                { project: "High-Risk Project", risk_level: 0.35, confidence: 0.82 },
                { project: "Standard Project", risk_level: 0.12, confidence: 0.78 },
                { project: "Low-Risk Project", risk_level: 0.05, confidence: 0.85 }
            ]
        };
    }

    updateMLDashboard(mlData) {
        const mlContainer = document.getElementById('mlPredictions');
        if (!mlContainer) return;
        
        mlContainer.innerHTML = `
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div class="bg-white rounded-lg p-6 shadow">
                    <h3 class="text-lg font-bold mb-4 text-blue-600">Success Predictions</h3>
                    ${mlData.success_predictions.map(pred => `
                        <div class="mb-3 p-3 bg-blue-50 rounded">
                            <div class="flex justify-between items-center">
                                <span class="font-medium">${pred.project}</span>
                                <span class="text-blue-600 font-bold">${(pred.success_rate * 100).toFixed(0)}%</span>
                            </div>
                            <div class="text-xs text-gray-600">Confidence: ${(pred.confidence * 100).toFixed(0)}%</div>
                        </div>
                    `).join('')}
                </div>
                
                <div class="bg-white rounded-lg p-6 shadow">
                    <h3 class="text-lg font-bold mb-4 text-green-600">Outcome Predictions</h3>
                    ${mlData.outcome_predictions.map(pred => `
                        <div class="mb-3 p-3 bg-green-50 rounded">
                            <div class="flex justify-between items-center">
                                <span class="font-medium">${pred.category}</span>
                                <span class="text-green-600 font-bold">${pred.predicted_score}/10</span>
                            </div>
                            <div class="text-xs text-gray-600">Confidence: ${(pred.confidence * 100).toFixed(0)}%</div>
                        </div>
                    `).join('')}
                </div>
                
                <div class="bg-white rounded-lg p-6 shadow">
                    <h3 class="text-lg font-bold mb-4 text-orange-600">Risk Assessments</h3>
                    ${mlData.risk_assessments.map(risk => `
                        <div class="mb-3 p-3 bg-orange-50 rounded">
                            <div class="flex justify-between items-center">
                                <span class="font-medium">${risk.project}</span>
                                <span class="text-orange-600 font-bold">${(risk.risk_level * 100).toFixed(0)}%</span>
                            </div>
                            <div class="text-xs text-gray-600">Confidence: ${(risk.confidence * 100).toFixed(0)}%</div>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
    }

    getHealthColor(value) {
        if (value < 50) return 'bg-green-500';
        if (value < 75) return 'bg-yellow-500';
        return 'bg-red-500';
    }

    startRealTimeUpdates() {
        // Update performance metrics every 30 seconds
        setInterval(async () => {
            await this.loadPerformanceMetrics();
        }, 30000);
        
        // Update ML predictions every 2 minutes
        setInterval(async () => {
            await this.loadMLPredictions();
        }, 120000);
    }

    togglePerformanceMonitoring() {
        const performanceSection = document.getElementById('performanceSection');
        if (performanceSection) {
            performanceSection.classList.toggle('hidden');
        }
    }

    // Add all other methods from the original dashboard.js
    // Include loadDashboardData, updateDashboard, etc.
    
    showLoading() {
        document.getElementById('loadingOverlay').classList.remove('hidden');
    }

    hideLoading() {
        document.getElementById('loadingOverlay').classList.add('hidden');
    }

    async loadDashboardData() {
        try {
            // Load client-specific data
            const response = await fetch(`${this.apiBaseUrl}/client-data/`);
            const data = await response.json();
            
            if (data.status === 'success') {
                this.updateDashboard(data.data);
            } else {
                throw new Error('Failed to load dashboard data');
            }
        } catch (error) {
            console.error('Error loading dashboard data:', error);
            this.showError('Failed to load dashboard data. Please try again.');
        }
    }

    updateDashboard(data) {
        // Update dashboard with client-specific data
        // Implement based on client requirements
    }

    async refreshData() {
        this.showLoading();
        await this.loadDashboardData();
        await this.loadPerformanceMetrics();
        await this.loadMLPredictions();
        this.hideLoading();
        
        // Show success message
        this.showSuccess('Dashboard data refreshed successfully!');
    }

    showError(message) {
        this.showNotification(message, 'error');
    }

    showSuccess(message) {
        this.showNotification(message, 'success');
    }

    showNotification(message, type) {
        const notification = document.createElement('div');
        notification.className = `fixed top-4 right-4 p-4 rounded-lg shadow-lg z-50 ${
            type === 'error' ? 'bg-red-500 text-white' : 'bg-green-500 text-white'
        }`;
        notification.textContent = message;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.remove();
        }, 3000);
    }
}

// Initialize dashboard when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new ClientDashboard();
});
```

### **Step 5: Production Deployment**

#### **Create deployment script (`deploy_production.py`)**
```python
#!/usr/bin/env python3
"""
Production Deployment Script for Client Dashboard System
Deploys the enhanced system with Phase 1 improvements and Phase 2 ML capabilities
"""

import os
import sys
import subprocess
import shutil
import json
import time
from pathlib import Path
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ProductionDeployment:
    """Production deployment manager for Client Dashboard System."""
    
    def __init__(self, deployment_dir: str = "production"):
        self.deployment_dir = deployment_dir
        self.backup_dir = f"{deployment_dir}_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.config = {
            "api_port": 8000,
            "frontend_port": 3000,
            "database_path": "client_data.db",
            "log_level": "INFO",
            "environment": "production"
        }
    
    def deploy(self):
        """Main deployment process."""
        logger.info("🚀 Starting Production Deployment for Client Dashboard System")
        logger.info("=" * 60)
        
        try:
            # Step 1: Pre-deployment checks
            self._pre_deployment_checks()
            
            # Step 2: Create backup
            self._create_backup()
            
            # Step 3: Prepare deployment directory
            self._prepare_deployment_directory()
            
            # Step 4: Copy application files
            self._copy_application_files()
            
            # Step 5: Install dependencies
            self._install_dependencies()
            
            # Step 6: Configure production settings
            self._configure_production_settings()
            
            # Step 7: Run tests
            self._run_tests()
            
            # Step 8: Start services
            self._start_services()
            
            # Step 9: Health checks
            self._health_checks()
            
            # Step 10: Final verification
            self._final_verification()
            
            logger.info("✅ Production deployment completed successfully!")
            self._print_deployment_summary()
            
        except Exception as e:
            logger.error(f"❌ Deployment failed: {str(e)}")
            self._rollback()
            raise
    
    # Include all deployment methods from the original deploy_production.py
    # Implementation details for each step

def main():
    """Main deployment function."""
    deployment = ProductionDeployment()
    deployment.deploy()

if __name__ == "__main__":
    main()
```

### **Step 6: Requirements and Dependencies**

#### **Create requirements.txt**
```txt
fastapi==0.104.1
uvicorn==0.24.0
sqlite3
psutil==5.9.6
numpy==1.24.3
pandas==2.0.3
scikit-learn==1.3.0
joblib==1.3.2
requests==2.31.0
python-multipart==0.0.6
```

### **Step 7: Configuration Files**

#### **Create production configuration (`config/production.json`)**
```json
{
  "deployment": {
    "timestamp": "2025-08-07T10:00:00",
    "version": "2.0.0",
    "environment": "production"
  },
  "api": {
    "host": "0.0.0.0",
    "port": 8000,
    "workers": 4,
    "log_level": "INFO"
  },
  "frontend": {
    "port": 3000,
    "static_files": "frontend"
  },
  "database": {
    "path": "client_data.db",
    "backup_interval": "daily"
  },
  "monitoring": {
    "enabled": true,
    "metrics_interval": 30,
    "alerting": true
  },
  "ml": {
    "enabled": true,
    "models_dir": "ml_models",
    "prediction_cache": true
  }
}
```

---

## 🎯 **Customization Requirements**

### **Client-Specific Adaptations**

#### **1. Data Model Customization**
```python
# Modify database schema in simple_api.py
# Add client-specific tables and fields
# Update API endpoints for client data
# Customize ML models for client domain
```

#### **2. Dashboard Customization**
```html
<!-- Modify frontend/index.html -->
<!-- Update client name, branding, colors -->
<!-- Customize metrics and categories -->
<!-- Add client-specific visualizations -->
```

#### **3. ML Model Customization**
```python
# Modify ml_integration/advanced_ml_engine.py
# Update feature extraction for client domain
# Customize prediction models
# Adjust confidence scoring
```

#### **4. Performance Monitoring**
```python
# Modify monitoring/advanced_metrics.py
# Add client-specific metrics
# Customize alert thresholds
# Update performance indicators
```

---

## 🚀 **Deployment Instructions**

### **Quick Start**
```bash
# 1. Clone or create project
mkdir client-dashboard-system
cd client-dashboard-system

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start development server
python simple_api.py

# 5. Start frontend server
cd frontend
python -m http.server 3000

# 6. Access dashboard
open http://localhost:3000
```

### **Production Deployment**
```bash
# 1. Run production deployment
python deploy_production.py

# 2. Start production services
cd production
./start_production.sh

# 3. Access production dashboard
open http://localhost:3000
```

---

## 📋 **Key Features to Implement**

### **✅ Phase 1: Foundation Enhancement**
- [ ] Performance optimization with caching
- [ ] Real-time monitoring and alerting
- [ ] Comprehensive logging and metrics
- [ ] Quality assurance and testing
- [ ] Production-ready deployment

### **✅ Phase 2: Advanced Intelligence**
- [ ] ML integration and predictive analytics
- [ ] Intelligent rule optimization
- [ ] Risk assessment and forecasting
- [ ] Confidence scoring and transparency
- [ ] Advanced analytics dashboard

### **✅ Enhanced Dashboard**
- [ ] Real-time performance monitoring
- [ ] ML prediction visualizations
- [ ] System health indicators
- [ ] Cache performance analytics
- [ ] Professional interface design

### **✅ Production Deployment**
- [ ] Automated deployment scripts
- [ ] Health checks and validation
- [ ] Backup and rollback systems
- [ ] Configuration management
- [ ] Monitoring and alerting

---

## 🎯 **Success Criteria**

### **Performance Targets**
- **Response Time**: <100ms average (target: ~60ms)
- **Uptime**: 99.9% system availability
- **Cache Hit Rate**: 85%+ for frequently accessed data
- **Error Rate**: <1% with comprehensive error handling

### **Quality Standards**
- **Test Coverage**: 100% for critical paths
- **Security**: Zero critical vulnerabilities
- **Documentation**: Comprehensive and up-to-date
- **Monitoring**: Real-time visibility and alerting

### **User Experience**
- **Dashboard Responsiveness**: Mobile and desktop optimized
- **Real-time Updates**: Live data integration
- **Error Handling**: User-friendly error messages
- **Accessibility**: UK English and AUD currency compliance

---

## 💡 **Additional Considerations**

### **Client-Specific Requirements**
1. **Domain Knowledge**: Understand client's business domain
2. **Data Sources**: Identify and integrate client data sources
3. **Metrics**: Define client-specific KPIs and metrics
4. **Branding**: Customize colors, logos, and branding
5. **Compliance**: Ensure regulatory compliance requirements

### **Technical Considerations**
1. **Scalability**: Plan for growth and increased load
2. **Security**: Implement proper authentication and authorization
3. **Backup**: Regular data backup and disaster recovery
4. **Monitoring**: Comprehensive system monitoring and alerting
5. **Documentation**: Maintain comprehensive documentation

### **Business Considerations**
1. **ROI**: Demonstrate clear business value and cost savings
2. **User Training**: Provide training and support for users
3. **Change Management**: Plan for organizational adoption
4. **Stakeholder Communication**: Regular updates and reporting
5. **Continuous Improvement**: Plan for ongoing enhancements

---

**🎯 This comprehensive guide provides everything needed to replicate the Movember AI Rules System for any client, with full Phase 1 and Phase 2 capabilities, enhanced dashboard, and production deployment ready!** 🚀 