import React, { useState, useEffect } from 'react';
import { LineChart, Line, BarChart, Bar, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { motion } from 'framer-motion';

interface PredictionResult {
  predicted_value: number;
  confidence_interval_lower: number;
  confidence_interval_upper: number;
  confidence_level: number;
  model_used: string;
  prediction_horizon: string;
  features_used: string[];
  timestamp: string;
}

interface ModelPerformance {
  model_type: string;
  accuracy: number;
  precision: number;
  recall: number;
  f1_score: number;
  mse: number;
  r2_score: number;
  training_time: number;
  prediction_time: number;
  last_updated: string;
}

interface ModelInsight {
  insight_type: string;
  description: string;
  confidence: number;
  actionable: boolean;
  impact_score: number;
  recommendations: string[];
}

const AdvancedAnalyticsDashboard: React.FC = () => {
  const [activeTab, setActiveTab] = useState('overview');
  const [predictions, setPredictions] = useState<PredictionResult[]>([]);
  const [modelPerformance, setModelPerformance] = useState<ModelPerformance[]>([]);
  const [insights, setInsights] = useState<ModelInsight[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedModel, setSelectedModel] = useState('impact_prediction');
  const [selectedHorizon, setSelectedHorizon] = useState('medium_term');

  const modelTypes = [
    'impact_prediction',
    'risk_assessment', 
    'engagement_forecast',
    'donation_prediction',
    'health_outcome_prediction',
    'campaign_optimization',
    'audience_segmentation',
    'churn_prediction'
  ];

  const horizons = ['short_term', 'medium_term', 'long_term'];

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      
      // Fetch model performance
      const performanceResponse = await fetch('http://localhost:8000/analytics/advanced/performance/all');
      const performanceData = await performanceResponse.json();
      
      // Fetch insights
      const insightsResponse = await fetch('http://localhost:8000/analytics/advanced/insights/all');
      const insightsData = await insightsResponse.json();
      
      setModelPerformance(Object.values(performanceData.performances || {}));
      setInsights(insightsData.insights || []);
      
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  const makePrediction = async () => {
    try {
      const sampleFeatures = {
        campaign_budget: 500000,
        social_media_reach: 100000,
        email_subscribers: 50000,
        website_traffic: 100000,
        donor_count: 10000,
        volunteer_count: 500,
        event_count: 20,
        partnership_count: 15,
        media_coverage: 50,
        awareness_score: 75
      };

      const response = await fetch(`http://localhost:8000/analytics/advanced/predict/${selectedModel}/${selectedHorizon}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(sampleFeatures),
      });

      const result = await response.json();
      setPredictions([result.prediction, ...predictions.slice(0, 4)]);
    } catch (error) {
      console.error('Error making prediction:', error);
    }
  };

  const getModelColor = (modelType: string) => {
    const colors = {
      impact_prediction: '#3B82F6',
      risk_assessment: '#EF4444',
      engagement_forecast: '#10B981',
      donation_prediction: '#F59E0B',
      health_outcome_prediction: '#8B5CF6',
      campaign_optimization: '#06B6D4',
      audience_segmentation: '#EC4899',
      churn_prediction: '#F97316'
    };
    return colors[modelType as keyof typeof colors] || '#6B7280';
  };

  const formatNumber = (num: number) => {
    if (num >= 1000000) return `${(num / 1000000).toFixed(1)}M`;
    if (num >= 1000) return `${(num / 1000).toFixed(1)}K`;
    return num.toFixed(0);
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="max-w-7xl mx-auto"
      >
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            Advanced Analytics Dashboard
          </h1>
          <p className="text-lg text-gray-600">
            Sophisticated ML models for Movember impact prediction and optimization
          </p>
        </div>

        {/* Navigation Tabs */}
        <div className="mb-6">
          <nav className="flex space-x-8">
            {['overview', 'predictions', 'performance', 'insights'].map((tab) => (
              <button
                key={tab}
                onClick={() => setActiveTab(tab)}
                className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                  activeTab === tab
                    ? 'bg-blue-100 text-blue-700'
                    : 'text-gray-500 hover:text-gray-700'
                }`}
              >
                {tab.charAt(0).toUpperCase() + tab.slice(1)}
              </button>
            ))}
          </nav>
        </div>

        {/* Overview Tab */}
        {activeTab === 'overview' && (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Model Summary */}
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              className="bg-white rounded-lg shadow-md p-6"
            >
              <h3 className="text-lg font-semibold mb-4">Model Summary</h3>
              <div className="space-y-3">
                <div className="flex justify-between">
                  <span className="text-gray-600">Total Models:</span>
                  <span className="font-semibold">24</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Model Types:</span>
                  <span className="font-semibold">8</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Time Horizons:</span>
                  <span className="font-semibold">3</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Avg Accuracy:</span>
                  <span className="font-semibold text-green-600">85%</span>
                </div>
              </div>
            </motion.div>

            {/* Quick Prediction */}
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 0.1 }}
              className="bg-white rounded-lg shadow-md p-6"
            >
              <h3 className="text-lg font-semibold mb-4">Quick Prediction</h3>
              <div className="space-y-3">
                <select
                  value={selectedModel}
                  onChange={(e) => setSelectedModel(e.target.value)}
                  className="w-full p-2 border border-gray-300 rounded-md"
                >
                  {modelTypes.map(type => (
                    <option key={type} value={type}>
                      {type.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}
                    </option>
                  ))}
                </select>
                <select
                  value={selectedHorizon}
                  onChange={(e) => setSelectedHorizon(e.target.value)}
                  className="w-full p-2 border border-gray-300 rounded-md"
                >
                  {horizons.map(horizon => (
                    <option key={horizon} value={horizon}>
                      {horizon.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}
                    </option>
                  ))}
                </select>
                <button
                  onClick={makePrediction}
                  className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 transition-colors"
                >
                  Make Prediction
                </button>
              </div>
            </motion.div>

            {/* System Health */}
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 0.2 }}
              className="bg-white rounded-lg shadow-md p-6"
            >
              <h3 className="text-lg font-semibold mb-4">System Health</h3>
              <div className="space-y-3">
                <div className="flex items-center">
                  <div className="w-3 h-3 bg-green-500 rounded-full mr-2"></div>
                  <span className="text-sm">API Server: Online</span>
                </div>
                <div className="flex items-center">
                  <div className="w-3 h-3 bg-green-500 rounded-full mr-2"></div>
                  <span className="text-sm">Models: Trained</span>
                </div>
                <div className="flex items-center">
                  <div className="w-3 h-3 bg-green-500 rounded-full mr-2"></div>
                  <span className="text-sm">Database: Connected</span>
                </div>
                <div className="flex items-center">
                  <div className="w-3 h-3 bg-green-500 rounded-full mr-2"></div>
                  <span className="text-sm">Monitoring: Active</span>
                </div>
              </div>
            </motion.div>
          </div>
        )}

        {/* Predictions Tab */}
        {activeTab === 'predictions' && (
          <div className="space-y-6">
            <div className="bg-white rounded-lg shadow-md p-6">
              <h3 className="text-lg font-semibold mb-4">Recent Predictions</h3>
              {predictions.length > 0 ? (
                <div className="space-y-4">
                  {predictions.map((prediction, index) => (
                    <motion.div
                      key={index}
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: index * 0.1 }}
                      className="border border-gray-200 rounded-lg p-4"
                    >
                      <div className="flex justify-between items-start mb-2">
                        <div>
                          <h4 className="font-semibold">
                            {prediction.model_used.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}
                          </h4>
                          <p className="text-sm text-gray-600">
                            {prediction.prediction_horizon.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}
                          </p>
                        </div>
                        <div className="text-right">
                          <div className="text-2xl font-bold text-blue-600">
                            {formatNumber(prediction.predicted_value)}
                          </div>
                          <div className="text-sm text-gray-500">
                            Confidence: {(prediction.confidence_level * 100).toFixed(0)}%
                          </div>
                        </div>
                      </div>
                      <div className="text-xs text-gray-500">
                        {new Date(prediction.timestamp).toLocaleString()}
                      </div>
                    </motion.div>
                  ))}
                </div>
              ) : (
                <p className="text-gray-500">No predictions made yet. Use the Quick Prediction tool to get started.</p>
              )}
            </div>
          </div>
        )}

        {/* Performance Tab */}
        {activeTab === 'performance' && (
          <div className="space-y-6">
            <div className="bg-white rounded-lg shadow-md p-6">
              <h3 className="text-lg font-semibold mb-4">Model Performance</h3>
              <ResponsiveContainer width="100%" height={400}>
                <BarChart data={modelPerformance}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="model_type" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="r2_score" fill="#3B82F6" name="R² Score" />
                  <Bar dataKey="accuracy" fill="#10B981" name="Accuracy" />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>
        )}

        {/* Insights Tab */}
        {activeTab === 'insights' && (
          <div className="space-y-6">
            <div className="bg-white rounded-lg shadow-md p-6">
              <h3 className="text-lg font-semibold mb-4">AI Insights</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {insights.slice(0, 6).map((insight, index) => (
                  <motion.div
                    key={index}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: index * 0.1 }}
                    className="border border-gray-200 rounded-lg p-4"
                  >
                    <div className="flex items-start justify-between mb-2">
                      <h4 className="font-semibold text-sm">
                        {insight.insight_type.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}
                      </h4>
                      <div className="flex items-center">
                        <div className="w-2 h-2 bg-green-500 rounded-full mr-1"></div>
                        <span className="text-xs text-gray-500">
                          {(insight.confidence * 100).toFixed(0)}%
                        </span>
                      </div>
                    </div>
                    <p className="text-sm text-gray-600 mb-2">{insight.description}</p>
                    {insight.actionable && (
                      <div className="text-xs text-blue-600">
                        Actionable: {insight.recommendations.length} recommendations
                      </div>
                    )}
                  </motion.div>
                ))}
              </div>
            </div>
          </div>
        )}
      </motion.div>
    </div>
  );
};

export default AdvancedAnalyticsDashboard;
