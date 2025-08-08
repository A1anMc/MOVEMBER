import React from 'react';
import { motion } from 'framer-motion';

const GrantEvaluation: React.FC = () => {
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="mb-8"
      >
        <h1 className="text-3xl font-bold text-gray-900">
          Grant Evaluation Interface
        </h1>
        <p className="mt-2 text-gray-600">
          Submit and evaluate grants using our AI-powered rules system
        </p>
      </motion.div>

      <div className="bg-white rounded-lg shadow-md p-8">
        <div className="text-center">
          <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg className="w-8 h-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
          </div>
          <h2 className="text-xl font-semibold text-gray-900 mb-2">
            Grant Evaluation Coming Soon
          </h2>
          <p className="text-gray-600 mb-6">
            This interface will allow you to submit grants for evaluation using our advanced AI rules system.
          </p>
          <div className="space-y-2 text-sm text-gray-500">
            <p>• Real-time grant evaluation</p>
            <p>• ML-powered scoring</p>
            <p>• SDG alignment analysis</p>
            <p>• Stakeholder engagement assessment</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default GrantEvaluation; 