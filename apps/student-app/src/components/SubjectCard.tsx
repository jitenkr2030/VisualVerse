/**
 * VisualVerse Student App - Subject Card Component
 * Display subject information and progress
 */

import React from 'react';
import { Subject } from '../types';

interface SubjectCardProps {
  subject: Subject;
  progress?: number;
  onClick?: () => void;
  compact?: boolean;
}

const SubjectCard: React.FC<SubjectCardProps> = ({ 
  subject, 
  progress = 0, 
  onClick,
  compact = false 
}) => {
  if (compact) {
    return (
      <div
        onClick={onClick}
        className="flex items-center justify-between p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors cursor-pointer"
      >
        <div className="flex items-center space-x-3">
          <span className="text-2xl">{subject.icon}</span>
          <div>
            <h4 className="text-sm font-medium text-gray-900">{subject.displayName}</h4>
            {progress > 0 && (
              <div className="flex items-center space-x-2 mt-1">
                <div className="w-16 bg-gray-200 rounded-full h-1">
                  <div
                    className="bg-blue-600 h-1 rounded-full"
                    style={{ width: `${progress}%` }}
                  />
                </div>
                <span className="text-xs text-gray-500">{progress}%</span>
              </div>
            )}
          </div>
        </div>
        <svg className="h-4 w-4 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
        </svg>
      </div>
    );
  }

  return (
    <div
      onClick={onClick}
      className="bg-white rounded-lg shadow-sm border border-gray-200 hover:shadow-md transition-all duration-200 cursor-pointer overflow-hidden"
    >
      <div className="p-6">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center space-x-3">
            <span className="text-3xl">{subject.icon}</span>
            <div>
              <h3 className="text-lg font-semibold text-gray-900">{subject.displayName}</h3>
              <p className="text-sm text-gray-600">{subject.description}</p>
            </div>
          </div>
          <span className="px-3 py-1 bg-gray-100 text-gray-700 text-sm rounded-full">
            {subject.difficulty}
          </span>
        </div>

        {progress > 0 && (
          <div className="mb-4">
            <div className="flex justify-between text-sm mb-2">
              <span className="text-gray-600">Progress</span>
              <span className="text-gray-900 font-medium">{progress}%</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div
                className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                style={{ width: `${progress}%` }}
              />
            </div>
          </div>
        )}

        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4 text-sm text-gray-500">
            <span>📚 {subject.learningObjectives.length} objectives</span>
            {subject.prerequisites.length > 0 && (
              <span>📋 {subject.prerequisites.length} prerequisites</span>
            )}
          </div>
          <button className="text-blue-600 hover:text-blue-800 font-medium text-sm">
            Explore →
          </button>
        </div>
      </div>

      {/* Progress indicator */}
      {progress > 0 && (
        <div className="h-1 bg-gray-200">
          <div
            className="h-1 bg-blue-600 transition-all duration-300"
            style={{ width: `${progress}%` }}
          />
        </div>
      )}
    </div>
  );
};

export default SubjectCard;
