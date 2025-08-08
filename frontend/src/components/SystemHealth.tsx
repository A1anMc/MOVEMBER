import React from 'react';
import { motion } from 'framer-motion';

interface SystemHealthProps {
  data?: any;
  loading?: boolean;
}

const SystemHealth: React.FC<SystemHealthProps> = ({ data, loading }) => {
  if (loading) {
    return (
      <div className="space-y-4">
        <div className="animate-pulse">
          <div className="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
          <div className="h-4 bg-gray-200 rounded w-1/2"></div>
        </div>
      </div>
    );
  }

  const healthData = data || {
    cpuUsage: 30,
    memoryUsage: 50,
    uptime: '99.9%',
    activeRules: 74,
    successRate: 0.92,
  };

  const getHealthColor = (value: number) => {
    if (value < 50) return 'bg-green-500';
    if (value < 80) return 'bg-yellow-500';
    return 'bg-red-500';
  };

  const getHealthText = (value: number) => {
    if (value < 50) return 'text-green-600';
    if (value < 80) return 'text-yellow-600';
    return 'text-red-600';
  };

  return (
    <div className="space-y-4">
      {/* CPU Usage */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <div className={`w-3 h-3 rounded-full ${getHealthColor(healthData.cpuUsage)}`}></div>
          <span className="text-sm font-medium text-gray-700">CPU Usage</span>
        </div>
        <span className={`text-sm font-semibold ${getHealthText(healthData.cpuUsage)}`}>
          {healthData.cpuUsage}%
        </span>
      </div>

      {/* Memory Usage */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <div className={`w-3 h-3 rounded-full ${getHealthColor(healthData.memoryUsage)}`}></div>
          <span className="text-sm font-medium text-gray-700">Memory Usage</span>
        </div>
        <span className={`text-sm font-semibold ${getHealthText(healthData.memoryUsage)}`}>
          {healthData.memoryUsage}%
        </span>
      </div>

      {/* Uptime */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <div className="w-3 h-3 rounded-full bg-green-500"></div>
          <span className="text-sm font-medium text-gray-700">Uptime</span>
        </div>
        <span className="text-sm font-semibold text-green-600">
          {healthData.uptime}
        </span>
      </div>

      {/* Active Rules */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <div className="w-3 h-3 rounded-full bg-blue-500"></div>
          <span className="text-sm font-medium text-gray-700">Active Rules</span>
        </div>
        <span className="text-sm font-semibold text-blue-600">
          {healthData.activeRules}
        </span>
      </div>

      {/* Success Rate */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <div className="w-3 h-3 rounded-full bg-green-500"></div>
          <span className="text-sm font-medium text-gray-700">Success Rate</span>
        </div>
        <span className="text-sm font-semibold text-green-600">
          {(healthData.successRate * 100).toFixed(1)}%
        </span>
      </div>

      {/* Overall Health */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        className="mt-4 p-3 bg-green-50 rounded-lg border border-green-200"
      >
        <div className="flex items-center space-x-2">
          <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
          <span className="text-sm font-medium text-green-800">
            System Healthy
          </span>
        </div>
      </motion.div>
    </div>
  );
};

export default SystemHealth; 