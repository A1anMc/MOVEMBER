// API Configuration for different environments
const API_CONFIG = {
  // Production API URL
  PRODUCTION: 'https://movember-api.onrender.com',
  // Development API URL
  DEVELOPMENT: 'http://localhost:8000',
  // Current environment (can be overridden by environment variable)
  CURRENT: process.env.NODE_ENV === 'production' 
    ? 'https://movember-api.onrender.com' 
    : 'http://localhost:8000'
};

// Get the appropriate API base URL
export const getApiBaseUrl = (): string => {
  // Check if we're in production (deployed on Render)
  if (window.location.hostname.includes('onrender.com')) {
    return API_CONFIG.PRODUCTION;
  }
  // Default to development for local testing
  return API_CONFIG.DEVELOPMENT;
};

// API endpoints
export const API_ENDPOINTS = {
  // Health checks
  HEALTH: '/health',
  ADVANCED_HEALTH: '/analytics/advanced/health',
  
  // Advanced Analytics
  ADVANCED_PERFORMANCE: '/analytics/advanced/performance/all',
  ADVANCED_INSIGHTS: '/analytics/advanced/insights/all',
  ADVANCED_PREDICT: (modelType: string, horizon: string) => 
    `/analytics/advanced/predict/${modelType}/${horizon}`,
  
  // Impact tracking
  IMPACT_SUMMARY: '/enhanced-impact/summary',
  IMPACT_HEALTH: '/enhanced-impact/health-outcomes',
  IMPACT_ECONOMIC: '/enhanced-impact/economic-impact',
  
  // Digital Analytics
  DIGITAL_SUMMARY: '/digital-analytics/summary',
  DIGITAL_SOCIAL: '/digital-analytics/social-media',
  DIGITAL_WEB: '/digital-analytics/web-performance',
  
  // Monitoring
  MONITORING_HEALTH: '/monitoring/health',
  MONITORING_METRICS: '/monitoring/metrics',
  MONITORING_ALERTS: '/monitoring/alerts'
};

// Helper function to build full API URLs
export const buildApiUrl = (endpoint: string): string => {
  return `${getApiBaseUrl()}${endpoint}`;
};
