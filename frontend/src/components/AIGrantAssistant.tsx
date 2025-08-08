import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { useMutation } from 'react-query';
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

interface AISuggestions {
  title_enhancement: string;
  description_improvements: string[];
  budget_optimization: string;
  timeline_suggestions: string;
  impact_metrics: string[];
  sdg_alignment: string[];
  stakeholder_strategies: string[];
  risk_mitigation: string[];
  success_factors: string[];
  overall_score: number;
}

const AIGrantAssistant: React.FC = () => {
  const [formData, setFormData] = useState<GrantFormData>({
    title: '',
    description: '',
    budget: 0,
    timeline_months: 12,
    organisation: '',
    contact_person: '',
    email: ''
  });

  const [suggestions, setSuggestions] = useState<AISuggestions | null>(null);
  const [activeTab, setActiveTab] = useState('form');

  // AI Assistant mutation
  const getAISuggestions = useMutation(
    async (grantData: GrantFormData) => {
      const response = await axios.post(
        `${import.meta.env.VITE_API_URL || 'https://movember-api.onrender.com'}/ai-grant-assistant/`,
        grantData
      );
      return response.data;
    },
    {
      onSuccess: (data) => {
        setSuggestions(data.suggestions);
        setActiveTab('suggestions');
      },
      onError: (error) => {
        console.error('AI Assistant failed:', error);
      }
    }
  );

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    getAISuggestions.mutate(formData);
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: name === 'budget' || name === 'timeline_months' ? Number(value) : value
    }));
  };

  const getScoreColor = (score: number) => {
    if (score >= 0.8) return 'text-green-600';
    if (score >= 0.6) return 'text-blue-600';
    if (score >= 0.4) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getScoreLabel = (score: number) => {
    if (score >= 0.8) return 'Excellent';
    if (score >= 0.6) return 'Good';
    if (score >= 0.4) return 'Fair';
    return 'Needs Improvement';
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="mb-8"
      >
        <h1 className="text-3xl font-bold text-gray-900">
          AI Grant Writing Assistant
        </h1>
        <p className="mt-2 text-gray-600">
          Get AI-powered suggestions to improve your grant application and increase approval chances
        </p>
      </motion.div>

      {/* Tab Navigation */}
      <div className="mb-6">
        <nav className="flex space-x-8">
          <button
            onClick={() => setActiveTab('form')}
            className={`py-2 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'form'
                ? 'border-blue-500 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            Grant Form
          </button>
          {suggestions && (
            <button
              onClick={() => setActiveTab('suggestions')}
              className={`py-2 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'suggestions'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              AI Suggestions
            </button>
          )}
        </nav>
      </div>

      {activeTab === 'form' && (
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          className="bg-white rounded-lg shadow-md p-6"
        >
          <h2 className="text-xl font-semibold text-gray-900 mb-6">
            Enter Your Grant Details
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
                placeholder="e.g., Men's Mental Health Support Program"
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
                rows={6}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Describe your project, objectives, and expected outcomes..."
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
              disabled={getAISuggestions.isLoading}
              className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50"
            >
              {getAISuggestions.isLoading ? 'Analyzing...' : 'Get AI Suggestions'}
            </button>
          </form>
        </motion.div>
      )}

      {activeTab === 'suggestions' && suggestions && (
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          className="space-y-6"
        >
          {/* Overall Score */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-xl font-semibold text-gray-900">
                AI Analysis Results
              </h2>
              <div className="text-right">
                <div className={`text-2xl font-bold ${getScoreColor(suggestions.overall_score)}`}>
                  {(suggestions.overall_score * 100).toFixed(0)}%
                </div>
                <div className="text-sm text-gray-600">
                  {getScoreLabel(suggestions.overall_score)}
                </div>
              </div>
            </div>
          </div>

          {/* Title Enhancement */}
          {suggestions.title_enhancement && (
            <div className="bg-white rounded-lg shadow-md p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-3">
                Title Enhancement
              </h3>
              <p className="text-gray-700">{suggestions.title_enhancement}</p>
            </div>
          )}

          {/* Description Improvements */}
          {suggestions.description_improvements.length > 0 && (
            <div className="bg-white rounded-lg shadow-md p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-3">
                Description Improvements
              </h3>
              <ul className="space-y-2">
                {suggestions.description_improvements.map((improvement, index) => (
                  <li key={index} className="flex items-start">
                    <span className="text-blue-500 mr-2">•</span>
                    <span className="text-gray-700">{improvement}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Budget & Timeline */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {suggestions.budget_optimization && (
              <div className="bg-white rounded-lg shadow-md p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-3">
                  Budget Optimization
                </h3>
                <p className="text-gray-700">{suggestions.budget_optimization}</p>
              </div>
            )}

            {suggestions.timeline_suggestions && (
              <div className="bg-white rounded-lg shadow-md p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-3">
                  Timeline Suggestions
                </h3>
                <p className="text-gray-700">{suggestions.timeline_suggestions}</p>
              </div>
            )}
          </div>

          {/* Impact Metrics */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-3">
              Suggested Impact Metrics
            </h3>
            <ul className="space-y-2">
              {suggestions.impact_metrics.map((metric, index) => (
                <li key={index} className="flex items-start">
                  <span className="text-green-500 mr-2">✓</span>
                  <span className="text-gray-700">{metric}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* SDG Alignment */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-3">
              SDG Alignment Opportunities
            </h3>
            <ul className="space-y-2">
              {suggestions.sdg_alignment.map((sdg, index) => (
                <li key={index} className="flex items-start">
                  <span className="text-purple-500 mr-2">🌍</span>
                  <span className="text-gray-700">{sdg}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* Stakeholder Strategies */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-3">
              Stakeholder Engagement Strategies
            </h3>
            <ul className="space-y-2">
              {suggestions.stakeholder_strategies.map((strategy, index) => (
                <li key={index} className="flex items-start">
                  <span className="text-blue-500 mr-2">🤝</span>
                  <span className="text-gray-700">{strategy}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* Risk Mitigation */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-3">
              Risk Mitigation Strategies
            </h3>
            <ul className="space-y-2">
              {suggestions.risk_mitigation.map((risk, index) => (
                <li key={index} className="flex items-start">
                  <span className="text-orange-500 mr-2">⚠️</span>
                  <span className="text-gray-700">{risk}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* Success Factors */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-3">
              Key Success Factors
            </h3>
            <ul className="space-y-2">
              {suggestions.success_factors.map((factor, index) => (
                <li key={index} className="flex items-start">
                  <span className="text-green-500 mr-2">🎯</span>
                  <span className="text-gray-700">{factor}</span>
                </li>
              ))}
            </ul>
          </div>
        </motion.div>
      )}
    </div>
  );
};

export default AIGrantAssistant; 