/**
 * VisualVerse Student App - Main Application Entry Point
 * React-based interface for students to access visual learning content
 * 
 * PROPRIETARY MODULE - See /PROPRIETARY_LICENSE.md for licensing terms
 * 
 * This module is part of VisualVerse's institutional/enterprise offering.
 * Copyright 2024 VisualVerse Contributors - All Rights Reserved
 */

import React, { useEffect, useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ErrorBoundary } from 'react-error-boundary';
import { Toaster } from 'react-hot-toast';

// Components
import Layout from '../components/Layout';
import LoadingSpinner from '../components/LoadingSpinner';
import ErrorFallback from '../components/ErrorFallback';

// Screens
import HomeScreen from '../screens/HomeScreen';
import LessonsScreen from '../screens/LessonsScreen';
import LessonViewerScreen from '../screens/LessonViewerScreen';
import ProfileScreen from '../screens/ProfileScreen';
import ProgressScreen from '../screens/ProgressScreen';
import SearchScreen from '../screens/SearchScreen';
import SubjectScreen from '../screens/SubjectScreen';

// Services and State
import { StudentProvider } from '../state/StudentContext';
import { LessonService } from '../services/LessonService';
import { UserService } from '../services/UserService';
import { ProgressService } from '../services/ProgressService';

// Types
import { Student, Lesson, Progress, Subject } from '../types';

// Error Handler Component
function ErrorHandler({ error, resetErrorBoundary }: { error: Error; resetErrorBoundary: () => void }) {
  return (
    <ErrorFallback 
      error={error} 
      resetErrorBoundary={resetErrorBoundary}
      message="Something went wrong with the Student App. Please refresh the page or contact support."
    />
  );
}

// Main App Component
const App: React.FC = () => {
  const [isLoading, setIsLoading] = useState(true);
  const [student, setStudent] = useState<Student | null>(null);
  const [lessons, setLessons] = useState<Lesson[]>([]);
  const [subjects, setSubjects] = useState<Subject[]>([]);
  const [progress, setProgress] = useState<Progress[]>([]);

  useEffect(() => {
    initializeApp();
  }, []);

  const initializeApp = async () => {
    try {
      setIsLoading(true);
      
      // Initialize services
      await Promise.all([
        LessonService.initialize(),
        UserService.initialize(),
        ProgressService.initialize()
      ]);
      
      // Load initial data
      await loadInitialData();
      
      // Set up real-time updates
      setupRealtimeUpdates();
      
    } catch (error) {
      console.error('Failed to initialize Student App:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const loadInitialData = async () => {
    try {
      // Load student profile
      const studentProfile = await UserService.getCurrentStudent();
      setStudent(studentProfile);
      
      // Load available lessons
      const availableLessons = await LessonService.getAvailableLessons();
      setLessons(availableLessons);
      
      // Load subjects
      const availableSubjects = await LessonService.getSubjects();
      setSubjects(availableSubjects);
      
      // Load student progress
      const studentProgress = await ProgressService.getStudentProgress(studentProfile.id);
      setProgress(studentProgress);
      
    } catch (error) {
      console.error('Failed to load initial data:', error);
    }
  };

  const setupRealtimeUpdates = () => {
    // Set up WebSocket connection for real-time updates
    const socket = LessonService.getSocket();
    
    socket.on('lesson_update', (data: { lessonId: string; status: string; progress: number }) => {
      setLessons(prevLessons => 
        prevLessons.map(lesson => 
          lesson.id === data.lessonId 
            ? { ...lesson, status: data.status, renderProgress: data.progress }
            : lesson
        )
      );
    });
    
    socket.on('progress_update', (data: { lessonId: string; progress: Progress }) => {
      setProgress(prevProgress => {
        const filtered = prevProgress.filter(p => p.lessonId !== data.lessonId);
        return [...filtered, data.progress];
      });
    });
    
    socket.on('new_lesson', (lesson: Lesson) => {
      setLessons(prevLessons => [...prevLessons, lesson]);
    });
  };

  // Loading State
  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
        <div className="text-center">
          <LoadingSpinner size="large" />
          <p className="mt-4 text-gray-600">Loading VisualVerse Student App...</p>
        </div>
      </div>
    );
  }

  return (
    <ErrorBoundary FallbackComponent={ErrorHandler} onError={(error) => console.error(error)}>
      <StudentProvider value={{ student, setStudent, lessons, setLessons, subjects, setSubjects, progress, setProgress }}>
        <Router>
          <div className="min-h-screen bg-gray-50">
            <Layout>
              <Routes>
                <Route path="/" element={<HomeScreen />} />
                <Route path="/lessons" element={<LessonsScreen />} />
                <Route path="/lessons/:lessonId" element={<LessonViewerScreen />} />
                <Route path="/subjects" element={<SubjectScreen />} />
                <Route path="/subjects/:subjectId" element={<SubjectScreen />} />
                <Route path="/search" element={<SearchScreen />} />
                <Route path="/progress" element={<ProgressScreen />} />
                <Route path="/profile" element={<ProfileScreen />} />
                <Route path="*" element={<Navigate to="/" replace />} />
              </Routes>
            </Layout>
            <Toaster 
              position="top-right"
              toastOptions={{
                duration: 4000,
                style: {
                  background: '#363636',
                  color: '#fff',
                },
                success: {
                  duration: 3000,
                  iconTheme: {
                    primary: '#4ade80',
                    secondary: '#fff',
                  },
                },
                error: {
                  duration: 5000,
                  iconTheme: {
                    primary: '#ef4444',
                    secondary: '#fff',
                  },
                },
              }}
            />
          </div>
        </Router>
      </StudentProvider>
    </ErrorBoundary>
  );
};

export default App;
