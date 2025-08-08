import React from 'react';
import { motion } from 'framer-motion';

const MLInsights: React.FC = () => {
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="mb-8"
      >
        <h1 className="text-3xl font-bold text-gray-900">
          Machine Learning Insights
        </h1>
        <p className="mt-2 text-gray-600">
          Advanced ML predictions and insights for grant evaluation
        </p>
      </motion.div>

      <div className="bg-white rounded-lg shadow-md p-8">
        <div className="text-center">
          <div className="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg className="w-8 h-8 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
            </svg>
          </div>
          <h2 className="text-xl font-semibold text-gray-900 mb-2">
            ML Insights Dashboard Coming Soon
          </h2>
          <p className="text-gray-600 mb-6">
            Deep machine learning insights and predictive analytics.
          </p>
          <div className="space-y-2 text-sm text-gray-500">
            <p>• Grant approval predictions</p>
            <p>• Impact outcome forecasting</p>
            <p>• SDG alignment analysis</p>
            <p>• Stakeholder engagement insights</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default MLInsights; 