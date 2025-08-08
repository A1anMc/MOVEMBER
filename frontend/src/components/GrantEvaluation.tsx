import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { useMutation, useQuery } from 'react-query';
import axios from 'axios';

interface GrantFormData {
  title: string;
  description: string;
  budget: number;
  timeline_months: number;
  organisation: string;
  contact_person: string;
  email: string;
}

interface EvaluationResult {
  grant_id: string;
  overall_score: number;
  recommendation: string;
  ml_predictions: {
    approval_probability: number;
    impact_score: number;
    sdg_alignment: number;
    stakeholder_engagement: number;
    risk_assessment: number;
  };
  evaluation_timestamp: string;
}

const GrantEvaluation: React.FC = () => {
  const [formData, setFormData] = useState<GrantFormData>({
    title: '',
    description: '',
    budget: 0,
    timeline_months: 12,
    organisation: '',
    contact_person: '',
    email: ''
  });

  const [evaluationResult, setEvaluationResult] = useState<EvaluationResult | null>(null);

  // Fetch recent evaluations
  const { data: recentEvaluations, refetch: refetchEvaluations } = useQuery(
    'recentEvaluations',
    async () => {
      const response = await axios.get(`${import.meta.env.VITE_API_URL || 'https://movember-api.onrender.com'}/grant-evaluations/`);
      return response.data;
    },
    { refetchInterval: 30000 }
  );

  // Evaluate grant mutation
  const evaluateGrant = useMutation(
    async (grantData: GrantFormData) => {
      const response = await axios.post(
        `${import.meta.env.VITE_API_URL || 'https://movember-api.onrender.com'}/evaluate-grant/`,
        grantData
      );
      return response.data;
    },
    {
      onSuccess: (data) => {
        setEvaluationResult(data);
        refetchEvaluations();
      },
      onError: (error) => {
        console.error('Evaluation failed:', error);
      }
    }
  );

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    evaluateGrant.mutate(formData);
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: name === 'budget' || name === 'timeline_months' ? Number(value) : value
    }));
  };

  const getRecommendationColor = (recommendation: string) => {
    switch (recommendation) {
      case 'STRONG_APPROVE':
        return 'text-green-600 bg-green-100';
      case 'APPROVE':
        return 'text-green-600 bg-green-50';
      case 'CONDITIONAL_APPROVE':
        return 'text-yellow-600 bg-yellow-50';
      case 'REJECT':
        return 'text-red-600 bg-red-50';
      default:
        return 'text-gray-600 bg-gray-50';
    }
  };

  const getScoreColor = (score: number) => {
    if (score >= 0.8) return 'text-green-600';
    if (score >= 0.6) return 'text-blue-600';
    if (score >= 0.4) return 'text-yellow-600';
    return 'text-red-600';
  };

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

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Grant Submission Form */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          className="bg-white rounded-lg shadow-md p-6"
        >
          <h2 className="text-xl font-semibold text-gray-900 mb-6">
            Submit Grant for Evaluation
          </h2>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Grant Title
              </label>
              <input
                type="text"
                name="title"
                value={formData.title}
                onChange={handleInputChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Description
              </label>
              <textarea
                name="description"
                value={formData.description}
                onChange={handleInputChange}
                rows={4}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                required
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Budget (AUD)
                </label>
                <input
                  type="number"
                  name="budget"
                  value={formData.budget}
                  onChange={handleInputChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Timeline (Months)
                </label>
                <input
                  type="number"
                  name="timeline_months"
                  value={formData.timeline_months}
                  onChange={handleInputChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  required
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Organisation
              </label>
              <input
                type="text"
                name="organisation"
                value={formData.organisation}
                onChange={handleInputChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                required
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Contact Person
                </label>
                <input
                  type="text"
                  name="contact_person"
                  value={formData.contact_person}
                  onChange={handleInputChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Email
                </label>
                <input
                  type="email"
                  name="email"
                  value={formData.email}
                  onChange={handleInputChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  required
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={evaluateGrant.isLoading}
              className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50"
            >
              {evaluateGrant.isLoading ? 'Evaluating...' : 'Evaluate Grant'}
            </button>
          </form>
        </motion.div>

        {/* Evaluation Results */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          className="space-y-6"
        >
          {evaluationResult && (
            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">
                Evaluation Results
              </h2>

              <div className="space-y-4">
                <div className="flex justify-between items-center">
                  <span className="text-sm font-medium text-gray-700">Overall Score:</span>
                  <span className={`text-lg font-bold ${getScoreColor(evaluationResult.overall_score)}`}>
                    {(evaluationResult.overall_score * 100).toFixed(1)}%
                  </span>
                </div>

                <div className="flex justify-between items-center">
                  <span className="text-sm font-medium text-gray-700">Recommendation:</span>
                  <span className={`px-3 py-1 rounded-full text-sm font-medium ${getRecommendationColor(evaluationResult.recommendation)}`}>
                    {evaluationResult.recommendation.replace('_', ' ')}
                  </span>
                </div>

                <div className="border-t pt-4">
                  <h3 className="text-sm font-medium text-gray-700 mb-3">ML Predictions</h3>
                  <div className="space-y-2">
                    <div className="flex justify-between">
                      <span className="text-sm text-gray-600">Approval Probability:</span>
                      <span className="text-sm font-medium">{(evaluationResult.ml_predictions.approval_probability * 100).toFixed(1)}%</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-sm text-gray-600">Impact Score:</span>
                      <span className="text-sm font-medium">{(evaluationResult.ml_predictions.impact_score * 100).toFixed(1)}%</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-sm text-gray-600">SDG Alignment:</span>
                      <span className="text-sm font-medium">{(evaluationResult.ml_predictions.sdg_alignment * 100).toFixed(1)}%</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-sm text-gray-600">Stakeholder Engagement:</span>
                      <span className="text-sm font-medium">{(evaluationResult.ml_predictions.stakeholder_engagement * 100).toFixed(1)}%</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-sm text-gray-600">Risk Assessment:</span>
                      <span className="text-sm font-medium">{(evaluationResult.ml_predictions.risk_assessment * 100).toFixed(1)}%</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Recent Evaluations */}
          {recentEvaluations?.evaluations && recentEvaluations.evaluations.length > 0 && (
            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">
                Recent Evaluations
              </h2>

              <div className="space-y-3">
                {recentEvaluations.evaluations.slice(0, 5).map((evaluation: any) => (
                  <div key={evaluation.grant_id} className="border-b pb-3 last:border-b-0">
                    <div className="flex justify-between items-start">
                      <div className="flex-1">
                        <h3 className="text-sm font-medium text-gray-900">
                          {evaluation.grant_data?.title || evaluation.grant_id}
                        </h3>
                        <p className="text-xs text-gray-500">
                          {new Date(evaluation.created_at).toLocaleDateString()}
                        </p>
                      </div>
                      <div className="text-right">
                        <div className={`px-2 py-1 rounded text-xs font-medium ${getRecommendationColor(evaluation.recommendation)}`}>
                          {evaluation.recommendation.replace('_', ' ')}
                        </div>
                        <div className={`text-sm font-bold ${getScoreColor(evaluation.overall_score)}`}>
                          {(evaluation.overall_score * 100).toFixed(1)}%
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </motion.div>
      </div>
    </div>
  );
};

export default GrantEvaluation; 