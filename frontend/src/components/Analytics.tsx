import React from 'react';
import { motion } from 'framer-motion';

const Analytics: React.FC = () => {
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="mb-8"
      >
        <h1 className="text-3xl font-bold text-gray-900">
          Advanced Analytics
        </h1>
        <p className="mt-2 text-gray-600">
          Comprehensive analytics and insights for grant evaluation performance
        </p>
      </motion.div>

      <div className="bg-white rounded-lg shadow-md p-8">
        <div className="text-center">
          <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg className="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
            </svg>
          </div>
          <h2 className="text-xl font-semibold text-gray-900 mb-2">
            Analytics Dashboard Coming Soon
          </h2>
          <p className="text-gray-600 mb-6">
            Advanced analytics with detailed insights and performance metrics.
          </p>
          <div className="space-y-2 text-sm text-gray-500">
            <p>• Performance trends and patterns</p>
            <p>• Grant evaluation analytics</p>
            <p>• SDG alignment tracking</p>
            <p>• Stakeholder engagement metrics</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Analytics; 