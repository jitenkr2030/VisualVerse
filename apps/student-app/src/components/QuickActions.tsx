/**
 * VisualVerse Student App - Quick Actions Component
 * Quick access to common actions
 */

import React from 'react';

interface QuickActionsProps {
  onAction: (action: string) => void;
}

const QuickActions: React.FC<QuickActionsProps> = ({ onAction }) => {
  const actions = [
    {
      id: 'continue_learning',
      title: 'Continue Learning',
      description: 'Resume your in-progress lessons',
      icon: '▶️',
      color: 'bg-blue-600 hover:bg-blue-700'
    },
    {
      id: 'browse_subjects',
      title: 'Browse Subjects',
      description: 'Explore different subject areas',
      icon: '📚',
      color: 'bg-green-600 hover:bg-green-700'
    },
    {
      id: 'view_progress',
      title: 'View Progress',
      description: 'Check your learning statistics',
      icon: '📊',
      color: 'bg-purple-600 hover:bg-purple-700'
    },
    {
      id: 'search_lessons',
      title: 'Search Lessons',
      description: 'Find specific content',
      icon: '🔍',
      color: 'bg-orange-600 hover:bg-orange-700'
    }
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      {actions.map(action => (
        <button
          key={action.id}
          onClick={() => onAction(action.id)}
          className={`${action.color} text-white p-4 rounded-lg transition-colors text-left`}
        >
          <div className="flex items-center space-x-3 mb-2">
            <span className="text-2xl">{action.icon}</span>
            <h3 className="font-semibold">{action.title}</h3>
          </div>
          <p className="text-sm opacity-90">{action.description}</p>
        </button>
      ))}
    </div>
  );
};

export default QuickActions;
