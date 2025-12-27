/**
 * VisualVerse Student App - Progress Card Component
 * Display learning progress and statistics
 */

import React from 'react';
import { Progress } from '../types';

interface ProgressCardProps {
  progress: Progress;
  lessonTitle: string;
  onClick?: () => void;
}

const ProgressCard: React.FC<ProgressCardProps> = ({ progress, lessonTitle, onClick }) => {
  return (
    <div
      onClick={onClick}
      className="bg-white rounded-lg shadow-sm border border-gray-200 p-4 hover:shadow-md transition-shadow cursor-pointer"
    >
      <div className="flex items-center justify-between mb-3">
        <h4 className="font-medium text-gray-900 truncate">{lessonTitle}</h4>
        <span className={`px-2 py-1 text-xs rounded-full ${
          progress.status === 'completed' ? 'bg-green-100 text-green-800' :
          progress.status === 'in_progress' ? 'bg-blue-100 text-blue-800' :
          'bg-gray-100 text-gray-800'
        }`}>
          {progress.status}
        </span>
      </div>
      
      <div className="mb-3">
        <div className="flex justify-between text-sm mb-1">
          <span>Progress</span>
          <span>{progress.completionPercentage}%</span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-2">
          <div
            className="bg-blue-600 h-2 rounded-full"
            style={{ width: `${progress.completionPercentage}%` }}
          />
        </div>
      </div>
      
      <div className="text-xs text-gray-500">
        Last accessed: {new Date(progress.lastAccessedAt).toLocaleDateString()}
      </div>
    </div>
  );
};

export default ProgressCard;
