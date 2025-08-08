// Enhanced Movember Impact Dashboard JavaScript with Phase 1 monitoring
class MovemberDashboard {
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
            grant_success_predictions: [
                { project: "Mental Health Initiative", success_rate: 0.85, confidence: 0.92 },
                { project: "Prostate Cancer Research", success_rate: 0.78, confidence: 0.88 },
                { project: "Community Engagement", success_rate: 0.92, confidence: 0.95 }
            ],
            impact_predictions: [
                { category: "Mental Health", predicted_score: 8.7, confidence: 0.89 },
                { category: "Research Funding", predicted_score: 9.1, confidence: 0.91 },
                { category: "Community Engagement", predicted_score: 8.5, confidence: 0.87 }
            ],
            risk_assessments: [
                { project: "High-Risk Initiative", risk_level: 0.35, confidence: 0.82 },
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
                    <h3 class="text-lg font-bold mb-4 text-blue-600">Grant Success Predictions</h3>
                    ${mlData.grant_success_predictions.map(pred => `
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
                    <h3 class="text-lg font-bold mb-4 text-green-600">Impact Predictions</h3>
                    ${mlData.impact_predictions.map(pred => `
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

    showLoading() {
        document.getElementById('loadingOverlay').classList.remove('hidden');
    }

    hideLoading() {
        document.getElementById('loadingOverlay').classList.add('hidden');
    }

    async loadDashboardData() {
        try {
            // Load global impact data
            const globalResponse = await fetch(`${this.apiBaseUrl}/impact/global/`);
            const globalData = await globalResponse.json();

            // Load dashboard data
            const dashboardResponse = await fetch(`${this.apiBaseUrl}/impact/dashboard/`);
            const dashboardData = await dashboardResponse.json();

            if (globalData.status === 'success' && dashboardData.status === 'success') {
                this.updateDashboard(globalData.data, dashboardData.data);
            } else {
                throw new Error('Failed to load dashboard data');
            }
        } catch (error) {
            console.error('Error loading dashboard data:', error);
            this.showError('Failed to load dashboard data. Please try again.');
        }
    }

    updateDashboard(globalData, dashboardData) {
        // Update header stats
        this.updateHeaderStats(dashboardData.key_metrics);
        
        // Update overall score
        this.updateOverallScore(globalData.overall_impact_score);
        
        // Update category chart
        this.updateCategoryChart(dashboardData.category_scores);
        
        // Update achievements
        this.updateAchievements(globalData.key_highlights);
        
        // Update category cards
        this.updateCategoryCards(globalData.category_breakdown);
        
        // Update trends
        this.updateTrends(globalData.trends);
        
        // Update recommendations
        this.updateRecommendations(globalData.recommendations);
    }

    updateHeaderStats(keyMetrics) {
        document.getElementById('peopleReached').textContent = keyMetrics.total_people_reached;
        document.getElementById('totalFunding').textContent = keyMetrics.total_funding;
        document.getElementById('countries').textContent = keyMetrics.total_countries;
        document.getElementById('researchProjects').textContent = keyMetrics.total_research_projects;
    }

    updateOverallScore(score) {
        document.getElementById('overallScore').textContent = score.toFixed(1);
    }

    updateCategoryChart(categoryScores) {
        const ctx = document.getElementById('categoryChart').getContext('2d');
        
        // Destroy existing chart if it exists
        if (this.chart) {
            this.chart.destroy();
        }

        const categories = Object.keys(categoryScores);
        const scores = Object.values(categoryScores);

        this.chart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: categories.map(cat => this.formatCategoryName(cat)),
                datasets: [{
                    label: 'Impact Score',
                    data: scores,
                    backgroundColor: this.generateColors(scores.length),
                    borderColor: this.generateColors(scores.length),
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 10,
                        ticks: {
                            stepSize: 2
                        }
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return `Score: ${context.parsed.y}/10`;
                            }
                        }
                    }
                }
            }
        });
    }

    updateAchievements(achievements) {
        const container = document.getElementById('achievements');
        container.innerHTML = '';

        achievements.forEach(achievement => {
            const div = document.createElement('div');
            div.className = 'flex items-start space-x-3 p-3 bg-green-50 rounded-lg';
            div.innerHTML = `
                <i class="fas fa-check-circle text-green-600 mt-1"></i>
                <span class="text-sm text-gray-700">${achievement}</span>
            `;
            container.appendChild(div);
        });
    }

    updateCategoryCards(categoryBreakdown) {
        const container = document.getElementById('categoryCards');
        container.innerHTML = '';

        Object.entries(categoryBreakdown).forEach(([category, data]) => {
            const card = this.createCategoryCard(category, data);
            container.appendChild(card);
        });
    }

    createCategoryCard(category, data) {
        const card = document.createElement('div');
        card.className = 'bg-white rounded-lg shadow-md p-6 card-hover';
        
        const scoreColor = this.getScoreColor(data.impact_score);
        const icon = this.getCategoryIcon(category);
        
        card.innerHTML = `
            <div class="flex items-center justify-between mb-4">
                <div class="flex items-center">
                    <div class="p-2 rounded-full ${scoreColor.bg} mr-3">
                        <i class="${icon} ${scoreColor.text} text-lg"></i>
                    </div>
                    <h4 class="text-lg font-semibold text-gray-900">${this.formatCategoryName(category)}</h4>
                </div>
                <div class="text-right">
                    <span class="text-2xl font-bold ${scoreColor.text}">${data.impact_score}</span>
                    <span class="text-sm text-gray-500">/10</span>
                </div>
            </div>
            <div class="space-y-2">
                ${data.metrics.slice(0, 2).map(metric => `
                    <div class="flex justify-between text-sm">
                        <span class="text-gray-600">${metric.name}:</span>
                        <span class="font-medium">${this.formatMetricValue(metric.value, metric.unit)}</span>
                    </div>
                `).join('')}
            </div>
            <div class="mt-4 pt-4 border-t border-gray-200">
                <div class="text-sm text-gray-600">
                    <strong>Achievement:</strong> ${data.achievements[0]}
                </div>
            </div>
        `;
        
        return card;
    }

    updateTrends(trends) {
        const container = document.getElementById('trends');
        container.innerHTML = '';

        // Overall trend
        const trendCard = document.createElement('div');
        trendCard.className = 'bg-blue-50 rounded-lg p-4';
        trendCard.innerHTML = `
            <div class="flex items-center justify-between">
                <span class="font-medium text-gray-900">Overall Trend</span>
                <span class="text-green-600 font-semibold capitalize">${trends.overall_trend}</span>
            </div>
        `;
        container.appendChild(trendCard);

        // Growth rate
        const growthCard = document.createElement('div');
        growthCard.className = 'bg-green-50 rounded-lg p-4';
        growthCard.innerHTML = `
            <div class="flex items-center justify-between">
                <span class="font-medium text-gray-900">Growth Rate</span>
                <span class="text-green-600 font-semibold">${(trends.growth_rate * 100).toFixed(1)}%</span>
            </div>
        `;
        container.appendChild(growthCard);

        // Key growth areas
        const growthAreasCard = document.createElement('div');
        growthAreasCard.className = 'bg-purple-50 rounded-lg p-4';
        growthAreasCard.innerHTML = `
            <div class="mb-2">
                <span class="font-medium text-gray-900">Key Growth Areas</span>
            </div>
            <div class="space-y-1">
                ${trends.key_growth_areas.map(area => `
                    <span class="inline-block bg-purple-200 text-purple-800 text-xs px-2 py-1 rounded mr-1 mb-1">
                        ${this.formatCategoryName(area)}
                    </span>
                `).join('')}
            </div>
        `;
        container.appendChild(growthAreasCard);
    }

    updateRecommendations(recommendations) {
        const container = document.getElementById('recommendations');
        container.innerHTML = '';

        recommendations.forEach((recommendation, index) => {
            const div = document.createElement('div');
            div.className = 'flex items-start space-x-3 p-3 bg-yellow-50 rounded-lg';
            div.innerHTML = `
                <div class="flex-shrink-0 w-6 h-6 bg-yellow-600 text-white rounded-full flex items-center justify-center text-xs font-bold">
                    ${index + 1}
                </div>
                <span class="text-sm text-gray-700">${recommendation}</span>
            `;
            container.appendChild(div);
        });
    }

    formatCategoryName(category) {
        return category
            .split('_')
            .map(word => word.charAt(0).toUpperCase() + word.slice(1))
            .join(' ');
    }

    formatMetricValue(value, unit) {
        if (value >= 1000000) {
            return `${(value / 1000000).toFixed(1)}M ${unit}`;
        } else if (value >= 1000) {
            return `${(value / 1000).toFixed(1)}K ${unit}`;
        }
        return `${value.toLocaleString()} ${unit}`;
    }

    getScoreColor(score) {
        if (score >= 9.0) {
            return { text: 'text-green-600', bg: 'bg-green-100' };
        } else if (score >= 8.5) {
            return { text: 'text-blue-600', bg: 'bg-blue-100' };
        } else if (score >= 8.0) {
            return { text: 'text-yellow-600', bg: 'bg-yellow-100' };
        } else {
            return { text: 'text-red-600', bg: 'bg-red-100' };
        }
    }

    getCategoryIcon(category) {
        const icons = {
            'mens_health_awareness': 'fas fa-bullhorn',
            'mental_health': 'fas fa-brain',
            'prostate_cancer': 'fas fa-microscope',
            'testicular_cancer': 'fas fa-stethoscope',
            'suicide_prevention': 'fas fa-heart',
            'research_funding': 'fas fa-flask',
            'community_engagement': 'fas fa-hands-helping',
            'global_reach': 'fas fa-globe',
            'advocacy': 'fas fa-gavel',
            'education': 'fas fa-graduation-cap'
        };
        return icons[category] || 'fas fa-chart-bar';
    }

    generateColors(count) {
        const colors = [
            '#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6',
            '#06B6D4', '#84CC16', '#F97316', '#EC4899', '#6366F1'
        ];
        return colors.slice(0, count);
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
    new MovemberDashboard();
}); 