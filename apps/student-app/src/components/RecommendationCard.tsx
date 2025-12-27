/**
 * VisualVerse Student App - Recommendation Card Component
 * Display personalized lesson recommendations
 */

import React from 'react';
import { Lesson } from '../types';

interface RecommendationCardProps {
  lesson: Lesson;
  reason: string;
  onStart: () => void;
}

const RecommendationCard: React.FC<RecommendationCardProps> = ({ lesson, reason, onStart }) => {
  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow">
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center space-x-2">
          <span className="px-2 py-1 bg-purple-100 text-purple-800 text-xs rounded-full">
            Recommended
          </span>
          <span className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded-full">
            {lesson.subject.displayName}
          </span>
        </div>
        <div className="flex items-center text-yellow-400">
          <span className="text-sm text-gray-600 mr-1">{lesson.rating}</span>
          <span>★</span>
        </div>
      </div>

      <h3 className="text-lg font-semibold text-gray-900 mb-2">{lesson.title}</h3>
      <p className="text-gray-600 text-sm mb-4">{lesson.description}</p>
      
      <div className="bg-purple-50 border border-purple-200 rounded-lg p-3 mb-4">
        <p className="text-sm text-purple-800">
          <span className="font-medium">Why recommended:</span> {reason}
        </p>
      </div>

      <div className="flex items-center justify-between">
        <span className="text-sm text-gray-500">
          {Math.round(lesson.content.duration / 60)} min
        </span>
        <button
          onClick={onStart}
          className="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors font-medium"
        >
          Start Learning
        </button>
      </div>
    </div>
  );
};

export default RecommendationCard;
