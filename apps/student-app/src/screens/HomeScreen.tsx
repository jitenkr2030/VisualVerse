/**
 * VisualVerse Student App - Home Screen
 * Main landing page showing featured content and quick access
 */

import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useStudent } from '../state/StudentContext';
import { lessonService } from '../services/LessonService';
import { progressService } from '../services/ProgressService';
import { Lesson, Subject, LearningAnalytics } from '../types';

// Components
import LoadingSpinner from '../components/LoadingSpinner';
import LessonCard from '../components/LessonCard';
import SubjectCard from '../components/SubjectCard';
import ProgressCard from '../components/ProgressCard';
import QuickActions from '../components/QuickActions';
import RecommendationCard from '../components/RecommendationCard';

const HomeScreen: React.FC = () => {
  const { state, dispatch } = useStudent();
  const [featuredLessons, setFeaturedLessons] = useState<Lesson[]>([]);
  const [recommendedLessons, setRecommendedLessons] = useState<Lesson[]>([]);
  const [recentActivity, setRecentActivity] = useState<any[]>([]);
  const [analytics, setAnalytics] = useState<LearningAnalytics | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    loadHomeData();
  }, [state.student]);

  const loadHomeData = async () => {
    if (!state.student) return;

    try {
      setIsLoading(true);

      // Load data in parallel
      const [
        featured,
        recommended,
        studentProgress,
        activity,
        analyticsData
      ] = await Promise.all([
        lessonService.getFeaturedLessons(),
        lessonService.getRecommendedLessons(state.student.id),
        progressService.getStudentProgress(state.student.id),
        progressService.getActivityHistory(state.student.id, 5),
        progressService.getLearningAnalytics(state.student.id)
      ]);

      setFeaturedLessons(featured);
      setRecommendedLessons(recommended);
      setRecentActivity(activity.data || []);
      setAnalytics(analyticsData);

      // Update state
      dispatch({ type: 'SET_LESSONS', payload: [...featured, ...recommended] });
      dispatch({ type: 'SET_PROGRESS', payload: studentProgress });
      dispatch({ type: 'SET_LEARNING_ANALYTICS', payload: analyticsData });

    } catch (error) {
      console.error('Error loading home data:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleLessonStart = (lesson: Lesson) => {
    dispatch({ type: 'SET_CURRENT_LESSON', payload: lesson });
    // Navigate to lesson viewer
    window.location.href = `/lessons/${lesson.id}`;
  };

  const handleQuickAction = (action: string) => {
    switch (action) {
      case 'continue_learning':
        // Find the lesson with highest progress that's not completed
        const inProgressLesson = state.progress
          .filter(p => p.status === 'in_progress')
          .sort((a, b) => b.completionPercentage - a.completionPercentage)[0];
        
        if (inProgressLesson) {
          const lesson = state.lessons.find(l => l.id === inProgressLesson.lessonId);
          if (lesson) {
            handleLessonStart(lesson);
          }
        }
        break;
      
      case 'browse_subjects':
        window.location.href = '/subjects';
        break;
      
      case 'view_progress':
        window.location.href = '/progress';
        break;
      
      case 'search_lessons':
        window.location.href = '/search';
        break;
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
        <LoadingSpinner size="large" />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Hero Section */}
      <div className="bg-gradient-to-r from-blue-600 to-purple-600 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
          <div className="text-center">
            <h1 className="text-4xl font-bold mb-4">
              Welcome back, {state.student?.name?.split(' ')[0]}!
            </h1>
            <p className="text-xl text-blue-100 mb-8">
              Continue your learning journey with VisualVerse
            </p>
            
            {/* Quick Stats */}
            {analytics && (
              <div className="grid grid-cols-1 md:grid-cols-4 gap-6 max-w-4xl mx-auto">
                <div className="bg-white/10 backdrop-blur-sm rounded-lg p-4">
                  <div className="text-3xl font-bold">{analytics.lessonsCompleted}</div>
                  <div className="text-blue-100">Lessons Completed</div>
                </div>
                <div className="bg-white/10 backdrop-blur-sm rounded-lg p-4">
                  <div className="text-3xl font-bold">{Math.round(analytics.totalTimeSpent / 60)}</div>
                  <div className="text-blue-100">Minutes Learned</div>
                </div>
                <div className="bg-white/10 backdrop-blur-sm rounded-lg p-4">
                  <div className="text-3xl font-bold">{analytics.subjectsExplored}</div>
                  <div className="text-blue-100">Subjects Explored</div>
                </div>
                <div className="bg-white/10 backdrop-blur-sm rounded-lg p-4">
                  <div className="text-3xl font-bold">{analytics.learningStreak}</div>
                  <div className="text-blue-100">Day Streak</div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Quick Actions */}
        <div className="mb-8">
          <QuickActions onAction={handleQuickAction} />
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main Content */}
          <div className="lg:col-span-2 space-y-8">
            {/* Continue Learning */}
            {state.progress.filter(p => p.status === 'in_progress').length > 0 && (
              <section>
                <div className="flex items-center justify-between mb-6">
                  <h2 className="text-2xl font-bold text-gray-900">Continue Learning</h2>
                  <Link 
                    to="/progress" 
                    className="text-blue-600 hover:text-blue-800 font-medium"
                  >
                    View All Progress →
                  </Link>
                </div>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {state.progress
                    .filter(p => p.status === 'in_progress')
                    .slice(0, 4)
                    .map(progress => {
                      const lesson = state.lessons.find(l => l.id === progress.lessonId);
                      if (!lesson) return null;
                      
                      return (
                        <LessonCard
                          key={lesson.id}
                          lesson={lesson}
                          progress={progress}
                          onStart={() => handleLessonStart(lesson)}
                          variant="compact"
                        />
                      );
                    })}
                </div>
              </section>
            )}

            {/* Featured Lessons */}
            <section>
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-2xl font-bold text-gray-900">Featured Lessons</h2>
                <Link 
                  to="/lessons" 
                  className="text-blue-600 hover:text-blue-800 font-medium"
                >
                  View All Lessons →
                </Link>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {featuredLessons.slice(0, 4).map(lesson => (
                  <LessonCard
                    key={lesson.id}
                    lesson={lesson}
                    onStart={() => handleLessonStart(lesson)}
                  />
                ))}
              </div>
            </section>

            {/* Recommended for You */}
            {recommendedLessons.length > 0 && (
              <section>
                <div className="flex items-center justify-between mb-6">
                  <h2 className="text-2xl font-bold text-gray-900">Recommended for You</h2>
                </div>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {recommendedLessons.slice(0, 4).map(lesson => (
                    <RecommendationCard
                      key={lesson.id}
                      lesson={lesson}
                      reason="Based on your learning history"
                      onStart={() => handleLessonStart(lesson)}
                    />
                  ))}
                </div>
              </section>
            )}
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Subjects Overview */}
            <div className="bg-white rounded-lg shadow-sm p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Explore Subjects</h3>
              <div className="space-y-3">
                {state.subjects.slice(0, 5).map(subject => (
                  <SubjectCard
                    key={subject.id}
                    subject={subject}
                    progress={analytics?.preferredSubjects.includes(subject.name) ? 75 : 0}
                    onClick={() => window.location.href = `/subjects/${subject.id}`}
                    compact
                  />
                ))}
              </div>
              <Link 
                to="/subjects" 
                className="block mt-4 text-center text-blue-600 hover:text-blue-800 font-medium"
              >
                View All Subjects →
              </Link>
            </div>

            {/* Recent Activity */}
            <div className="bg-white rounded-lg shadow-sm p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Recent Activity</h3>
              
              {recentActivity.length > 0 ? (
                <div className="space-y-3">
                  {recentActivity.map((activity, index) => (
                    <div key={index} className="flex items-start space-x-3">
                      <div className="flex-shrink-0">
                        <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
                          <span className="text-blue-600 text-sm">
                            {activity.type === 'lesson_completed' ? '✅' : 
                             activity.type === 'lesson_started' ? '▶️' : '📚'}
                          </span>
                        </div>
                      </div>
                      <div className="flex-1 min-w-0">
                        <p className="text-sm text-gray-900">{activity.description}</p>
                        <p className="text-xs text-gray-500">
                          {new Date(activity.timestamp).toLocaleDateString()}
                        </p>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-gray-500 text-sm">No recent activity</p>
              )}
              
              <Link 
                to="/progress" 
                className="block mt-4 text-center text-blue-600 hover:text-blue-800 font-medium"
              >
                View Full History →
              </Link>
            </div>

            {/* Learning Insights */}
            {analytics && (
              <div className="bg-white rounded-lg shadow-sm p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Learning Insights</h3>
                
                <div className="space-y-4">
                  <div>
                    <div className="flex justify-between text-sm mb-1">
                      <span>Overall Progress</span>
                      <span>{Math.round((analytics.lessonsCompleted / 20) * 100)}%</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div 
                        className="bg-blue-600 h-2 rounded-full" 
                        style={{ width: `${Math.min((analytics.lessonsCompleted / 20) * 100, 100)}%` }}
                      />
                    </div>
                  </div>
                  
                  <div className="text-sm text-gray-600">
                    <p>🎯 Preferred subjects: {analytics.preferredSubjects.join(', ')}</p>
                    <p>⏱️ Avg session: {analytics.averageSessionDuration} min</p>
                    <p>🔥 Current streak: {analytics.learningStreak} days</p>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default HomeScreen;
