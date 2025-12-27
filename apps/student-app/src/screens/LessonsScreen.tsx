/**
 * VisualVerse Student App - Lessons Screen
 * Browse and search available lessons
 */

import React, { useState, useEffect } from 'react';
import { useStudent } from '../state/StudentContext';
import { lessonService } from '../services/LessonService';
import { Lesson, SearchFilters } from '../types';

const LessonsScreen: React.FC = () => {
  const { state } = useStudent();
  const [lessons, setLessons] = useState<Lesson[]>([]);
  const [filteredLessons, setFilteredLessons] = useState<Lesson[]>([]);
  const [searchFilters, setSearchFilters] = useState<SearchFilters>({
    sortBy: 'relevance',
    sortOrder: 'desc'
  });
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    loadLessons();
  }, []);

  const loadLessons = async () => {
    try {
      setIsLoading(true);
      const availableLessons = await lessonService.getAvailableLessons();
      setLessons(availableLessons);
      setFilteredLessons(availableLessons);
    } catch (error) {
      console.error('Error loading lessons:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSearch = (query: string) => {
    if (!query.trim()) {
      setFilteredLessons(lessons);
      return;
    }

    const filtered = lessons.filter(lesson =>
      lesson.title.toLowerCase().includes(query.toLowerCase()) ||
      lesson.description.toLowerCase().includes(query.toLowerCase()) ||
      lesson.tags.some(tag => tag.toLowerCase().includes(query.toLowerCase()))
    );

    setFilteredLessons(filtered);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Browse Lessons</h1>
          <p className="text-gray-600">Discover engaging visual lessons across all subjects</p>
        </div>

        {/* Search and Filters */}
        <div className="bg-white rounded-lg shadow-sm p-6 mb-8">
          <div className="flex flex-col md:flex-row gap-4">
            <div className="flex-1">
              <input
                type="text"
                placeholder="Search lessons..."
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                onChange={(e) => handleSearch(e.target.value)}
              />
            </div>
            <select
              className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              value={searchFilters.subject}
              onChange={(e) => setSearchFilters({ ...searchFilters, subject: e.target.value })}
            >
              <option value="">All Subjects</option>
              {state.subjects.map(subject => (
                <option key={subject.id} value={subject.name}>
                  {subject.displayName}
                </option>
              ))}
            </select>
          </div>
        </div>

        {/* Lessons Grid */}
        {isLoading ? (
          <div className="flex justify-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredLessons.map(lesson => (
              <div key={lesson.id} className="bg-white rounded-lg shadow-sm p-6 hover:shadow-md transition-shadow">
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
                <p className="text-gray-600 text-sm mb-4">{lesson.description}</p>
                
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-500">
                    {Math.round(lesson.content.duration / 60)} min
                  </span>
                  <button
                    onClick={() => window.location.href = `/lessons/${lesson.id}`}
                    className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                  >
                    Start Lesson
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}

        {filteredLessons.length === 0 && !isLoading && (
          <div className="text-center py-12">
            <div className="text-gray-400 mb-4">
              <svg className="mx-auto h-12 w-12" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.172 16.172a4 4 0 015.656 0M9 12h6m-6-4h6m2 5.291A7.962 7.962 0 0112 15c-2.34 0-4.467-.881-6.073-2.291M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
            </div>
            <h3 className="text-lg font-medium text-gray-900 mb-2">No lessons found</h3>
            <p className="text-gray-600">Try adjusting your search criteria</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default LessonsScreen;
