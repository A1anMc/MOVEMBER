import React from 'react';
import { motion } from 'framer-motion';

interface MLPredictionsProps {
  data?: any;
  loading?: boolean;
}

const MLPredictions: React.FC<MLPredictionsProps> = ({ data, loading }) => {
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

  const mlData = data || {
    grantApprovalPrediction: { accuracy: 0.87, confidence: 0.82, trend: 'improving' },
    impactPrediction: { accuracy: 0.79, confidence: 0.75, trend: 'stable' },
    sdgAlignment: { accuracy: 0.84, confidence: 0.78, trend: 'improving' },
    stakeholderEngagement: { accuracy: 0.81, confidence: 0.76, trend: 'improving' },
  };

  const getTrendColor = (trend: string) => {
    switch (trend) {
      case 'improving':
        return 'text-green-600';
      case 'stable':
        return 'text-blue-600';
      case 'declining':
        return 'text-red-600';
      default:
        return 'text-gray-600';
    }
  };

  const getTrendIcon = (trend: string) => {
    switch (trend) {
      case 'improving':
        return '↗';
      case 'stable':
        return '→';
      case 'declining':
        return '↘';
      default:
        return '→';
    }
  };

  const predictions = [
    {
      name: 'Grant Approval',
      accuracy: mlData.grantApprovalPrediction.accuracy,
      confidence: mlData.grantApprovalPrediction.confidence,
      trend: mlData.grantApprovalPrediction.trend,
      color: 'bg-blue-500',
    },
    {
      name: 'Impact Prediction',
      accuracy: mlData.impactPrediction.accuracy,
      confidence: mlData.impactPrediction.confidence,
      trend: mlData.impactPrediction.trend,
      color: 'bg-green-500',
    },
    {
      name: 'SDG Alignment',
      accuracy: mlData.sdgAlignment.accuracy,
      confidence: mlData.sdgAlignment.confidence,
      trend: mlData.sdgAlignment.trend,
      color: 'bg-purple-500',
    },
    {
      name: 'Stakeholder Engagement',
      accuracy: mlData.stakeholderEngagement.accuracy,
      confidence: mlData.stakeholderEngagement.confidence,
      trend: mlData.stakeholderEngagement.trend,
      color: 'bg-orange-500',
    },
  ];

  return (
    <div className="space-y-4">
      {predictions.map((prediction, index) => (
        <motion.div
          key={prediction.name}
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: index * 0.1 }}
          className="bg-gray-50 rounded-lg p-4"
        >
          <div className="flex items-center justify-between mb-2">
            <div className="flex items-center space-x-3">
              <div className={`w-3 h-3 rounded-full ${prediction.color}`}></div>
              <span className="text-sm font-medium text-gray-700">
                {prediction.name}
              </span>
            </div>
            <span className={`text-sm font-semibold ${getTrendColor(prediction.trend)}`}>
              {getTrendIcon(prediction.trend)} {prediction.trend}
            </span>
          </div>
          
          <div className="grid grid-cols-2 gap-4">
            <div>
              <span className="text-xs text-gray-500">Accuracy</span>
              <p className="text-lg font-bold text-gray-900">
                {(prediction.accuracy * 100).toFixed(1)}%
              </p>
            </div>
            <div>
              <span className="text-xs text-gray-500">Confidence</span>
              <p className="text-lg font-bold text-gray-900">
                {(prediction.confidence * 100).toFixed(1)}%
              </p>
            </div>
          </div>
        </motion.div>
      ))}

      {/* ML Status */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.5 }}
        className="mt-4 p-3 bg-blue-50 rounded-lg border border-blue-200"
      >
        <div className="flex items-center space-x-2">
          <div className="w-2 h-2 bg-blue-500 rounded-full animate-pulse"></div>
          <span className="text-sm font-medium text-blue-800">
            ML Models Active - Real-time Predictions
          </span>
        </div>
      </motion.div>
    </div>
  );
};

export default MLPredictions; 