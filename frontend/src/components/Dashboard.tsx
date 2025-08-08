import React from 'react';
import { useQuery } from 'react-query';
import { motion } from 'framer-motion';
import { 
  ChartBarIcon, 
  UserGroupIcon, 
  CurrencyDollarIcon, 
  GlobeAltIcon,
  TrendingUpIcon,
  CogIcon
} from '@heroicons/react/24/outline';
import { fetchDashboardData, fetchSystemHealth, fetchMLPredictions } from '../api/dashboard';
import StatCard from './StatCard';
import Chart from './Chart';
import SystemHealth from './SystemHealth';
import MLPredictions from './MLPredictions';

const Dashboard: React.FC = () => {
  const { data: dashboardData, isLoading: dashboardLoading } = useQuery(
    'dashboard',
    fetchDashboardData,
    { refetchInterval: 30000 }
  );

  const { data: healthData, isLoading: healthLoading } = useQuery(
    'systemHealth',
    fetchSystemHealth,
    { refetchInterval: 10000 }
  );

  const { data: mlData, isLoading: mlLoading } = useQuery(
    'mlPredictions',
    fetchMLPredictions,
    { refetchInterval: 60000 }
  );

  if (dashboardLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="mb-8"
      >
        <h1 className="text-3xl font-bold text-gray-900">
          Movember AI Rules System Dashboard
        </h1>
        <p className="mt-2 text-gray-600">
          Advanced analytics and machine learning insights for grant evaluation
        </p>
      </motion.div>

      {/* Key Metrics */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8"
      >
        <StatCard
          title="People Reached"
          value={dashboardData?.peopleReached || '8.5M'}
          icon={UserGroupIcon}
          trend="+12%"
          trendDirection="up"
        />
        <StatCard
          title="Total Funding"
          value={dashboardData?.totalFunding || '$125M AUD'}
          icon={CurrencyDollarIcon}
          trend="+8%"
          trendDirection="up"
        />
        <StatCard
          title="Countries"
          value={dashboardData?.countries || '25'}
          icon={GlobeAltIcon}
          trend="+2"
          trendDirection="up"
        />
        <StatCard
          title="System Health"
          value={healthData?.overallHealth || '99.9%'}
          icon={CogIcon}
          trend="Stable"
          trendDirection="neutral"
        />
      </motion.div>

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Left Column - Analytics */}
        <div className="lg:col-span-2 space-y-8">
          {/* Grant Evaluation Chart */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.2 }}
            className="bg-white rounded-lg shadow-md p-6"
          >
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-xl font-semibold text-gray-900">
                Grant Evaluation Performance
              </h2>
              <TrendingUpIcon className="h-6 w-6 text-green-600" />
            </div>
            <Chart
              data={dashboardData?.grantEvaluationData}
              type="line"
              height={300}
            />
          </motion.div>

          {/* ML Predictions */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.3 }}
            className="bg-white rounded-lg shadow-md p-6"
          >
            <h2 className="text-xl font-semibold text-gray-900 mb-4">
              Machine Learning Insights
            </h2>
            <MLPredictions data={mlData} loading={mlLoading} />
          </motion.div>
        </div>

        {/* Right Column - System Health & Quick Actions */}
        <div className="space-y-8">
          {/* System Health */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.2 }}
            className="bg-white rounded-lg shadow-md p-6"
          >
            <h2 className="text-xl font-semibold text-gray-900 mb-4">
              System Health
            </h2>
            <SystemHealth data={healthData} loading={healthLoading} />
          </motion.div>

          {/* Quick Actions */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.3 }}
            className="bg-white rounded-lg shadow-md p-6"
          >
            <h2 className="text-xl font-semibold text-gray-900 mb-4">
              Quick Actions
            </h2>
            <div className="space-y-3">
              <button className="w-full bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition-colors">
                Evaluate New Grant
              </button>
              <button className="w-full bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg transition-colors">
                Run Analytics Report
              </button>
              <button className="w-full bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded-lg transition-colors">
                View ML Insights
              </button>
            </div>
          </motion.div>

          {/* Recent Activity */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.4 }}
            className="bg-white rounded-lg shadow-md p-6"
          >
            <h2 className="text-xl font-semibold text-gray-900 mb-4">
              Recent Activity
            </h2>
            <div className="space-y-3">
              {dashboardData?.recentActivity?.map((activity: any, index: number) => (
                <div key={index} className="flex items-center space-x-3 p-3 bg-gray-50 rounded-lg">
                  <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                  <div className="flex-1">
                    <p className="text-sm font-medium text-gray-900">{activity.title}</p>
                    <p className="text-xs text-gray-500">{activity.time}</p>
                  </div>
                </div>
              ))}
            </div>
          </motion.div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard; 