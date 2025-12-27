/**
 * VisualVerse Student App - Lesson Card Component
 * Display lesson information in card format
 */

import React from 'react';
import { Lesson, Progress } from '../types';

interface LessonCardProps {
  lesson: Lesson;
  progress?: Progress;
  onStart: () => void;
  variant?: 'default' | 'compact';
}

const LessonCard: React.FC<LessonCardProps> = ({ 
  lesson, 
  progress, 
  onStart, 
  variant = 'default' 
}) => {
  const getStatusText = () => {
    if (progress) {
      switch (progress.status) {
        case 'completed':
          return 'Completed';
        case 'in_progress':
          return `In Progress (${progress.completionPercentage}%)`;
        default:
          return 'Not Started';
      }
    }
    return 'Available';
  };

  const getStatusColor = () => {
    if (progress) {
      switch (progress.status) {
        case 'completed':
          return 'text-green-600 bg-green-100';
        case 'in_progress':
          return 'text-blue-600 bg-blue-100';
        default:
          return 'text-gray-600 bg-gray-100';
      }
    }
    return 'text-blue-600 bg-blue-100';
  };

  if (variant === 'compact') {
    return (
      <div className="bg-white rounded-lg shadow-sm p-4 border border-gray-200 hover:shadow-md transition-shadow">
        <div className="flex items-start justify-between mb-2">
          <h3 className="text-sm font-semibold text-gray-900 truncate">{lesson.title}</h3>
          <span className={`px-2 py-1 text-xs rounded-full ${getStatusColor()}`}>
            {getStatusText()}
          </span>
        </div>
        <p className="text-xs text-gray-600 mb-3 line-clamp-2">{lesson.description}</p>
        <div className="flex items-center justify-between">
          <span className="text-xs text-gray-500">
            {Math.round(lesson.content.duration / 60)} min
          </span>
          <button
            onClick={onStart}
            className="px-3 py-1 text-xs bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors"
          >
            {progress?.status === 'completed' ? 'Review' : 'Continue'}
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 hover:shadow-md transition-shadow overflow-hidden">
      {/* Lesson Header */}
      <div className="p-6">
        <div className="flex items-start justify-between mb-4">
          <span className="px-3 py-1 bg-blue-100 text-blue-800 text-sm rounded-full">
            {lesson.subject.displayName}
          </span>
          <div className="flex items-center text-yellow-400">
            <span className="text-sm text-gray-600 mr-1">{lesson.rating}</span>
            <span>★</span>
          </div>
        </div>

        <h3 className="text-lg font-semibold text-gray-900 mb-2">{lesson.title}</h3>
        <p className="text-gray-600 text-sm mb-4 line-clamp-3">{lesson.description}</p>

        {/* Progress Bar */}
        {progress && (
          <div className="mb-4">
            <div className="flex justify-between text-sm mb-1">
              <span className="text-gray-600">Progress</span>
              <span className="text-gray-900">{progress.completionPercentage}%</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div
                className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                style={{ width: `${progress.completionPercentage}%` }}
              />
            </div>
          </div>
        )}

        {/* Lesson Meta */}
        <div className="flex items-center justify-between text-sm text-gray-500 mb-4">
          <span>{Math.round(lesson.content.duration / 60)} min</span>
          <span>{lesson.views} views</span>
          <span className={`px-2 py-1 rounded-full text-xs ${getStatusColor()}`}>
            {getStatusText()}
          </span>
        </div>

        {/* Action Button */}
        <button
          onClick={onStart}
          className="w-full px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium"
        >
          {progress?.status === 'completed' ? 'Review Lesson' : 
           progress?.status === 'in_progress' ? 'Continue Learning' : 
           'Start Lesson'}
        </button>
      </div>

      {/* Creator Info */}
      <div className="bg-gray-50 px-6 py-3 border-t">
        <div className="flex items-center">
          <img
            src={lesson.creator.avatar || 'https://via.placeholder.com/32'}
            alt={lesson.creator.name}
            className="w-8 h-8 rounded-full mr-3"
          />
          <div className="flex-1 min-w-0">
            <p className="text-sm font-medium text-gray-900 truncate">
              {lesson.creator.name}
            </p>
            <p className="text-xs text-gray-500">
              {lesson.creator.totalStudents} students
            </p>
          </div>
          {lesson.creator.verified && (
            <span className="text-blue-500 text-xs">✓ Verified</span>
          )}
        </div>
      </div>
    </div>
  );
};

export default LessonCard;
