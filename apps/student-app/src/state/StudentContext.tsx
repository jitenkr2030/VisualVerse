/**
 * VisualVerse Student App - State Management
 * React Context for managing student application state
 */

import React, { createContext, useContext, useReducer, useEffect, ReactNode } from 'react';
import { Student, Lesson, Progress, Subject, Notification, SearchFilters } from '../types';

// State Interface
interface StudentState {
  // User State
  student: Student | null;
  isAuthenticated: boolean;
  
  // Content State
  lessons: Lesson[];
  subjects: Subject[];
  currentLesson: Lesson | null;
  searchResults: Lesson[];
  searchFilters: SearchFilters;
  
  // Progress State
  progress: Progress[];
  currentProgress: Progress | null;
  learningAnalytics: any;
  
  // UI State
  isLoading: boolean;
  isOffline: boolean;
  notifications: Notification[];
  theme: 'light' | 'dark' | 'system';
  
  // Player State
  isPlaying: boolean;
  currentTime: number;
  duration: number;
  volume: number;
  playbackSpeed: number;
  quality: string;
  subtitlesEnabled: boolean;
  
  // App State
  sidebarOpen: boolean;
  currentView: string;
  error: string | null;
}

// Actions
type StudentAction =
  // Authentication
  | { type: 'SET_STUDENT'; payload: Student }
  | { type: 'LOGOUT' }
  
  // Content
  | { type: 'SET_LESSONS'; payload: Lesson[] }
  | { type: 'ADD_LESSON'; payload: Lesson }
  | { type: 'UPDATE_LESSON'; payload: { id: string; updates: Partial<Lesson> } }
  | { type: 'REMOVE_LESSON'; payload: string }
  | { type: 'SET_CURRENT_LESSON'; payload: Lesson | null }
  | { type: 'SET_SUBJECTS'; payload: Subject[] }
  | { type: 'SET_SEARCH_RESULTS'; payload: Lesson[] }
  | { type: 'SET_SEARCH_FILTERS'; payload: SearchFilters }
  
  // Progress
  | { type: 'SET_PROGRESS'; payload: Progress[] }
  | { type: 'ADD_PROGRESS'; payload: Progress }
  | { type: 'UPDATE_PROGRESS'; payload: { id: string; updates: Partial<Progress> } }
  | { type: 'SET_CURRENT_PROGRESS'; payload: Progress | null }
  | { type: 'SET_LEARNING_ANALYTICS'; payload: any }
  
  // UI
  | { type: 'SET_LOADING'; payload: boolean }
  | { type: 'SET_OFFLINE'; payload: boolean }
  | { type: 'ADD_NOTIFICATION'; payload: Notification }
  | { type: 'REMOVE_NOTIFICATION'; payload: string }
  | { type: 'MARK_NOTIFICATION_READ'; payload: string }
  | { type: 'SET_THEME'; payload: 'light' | 'dark' | 'system' }
  | { type: 'TOGGLE_SIDEBAR' }
  | { type: 'SET_CURRENT_VIEW'; payload: string }
  | { type: 'SET_ERROR'; payload: string | null }
  
  // Player
  | { type: 'SET_PLAYING'; payload: boolean }
  | { type: 'SET_CURRENT_TIME'; payload: number }
  | { type: 'SET_DURATION'; payload: number }
  | { type: 'SET_VOLUME'; payload: number }
  | { type: 'SET_PLAYBACK_SPEED'; payload: number }
  | { type: 'SET_QUALITY'; payload: string }
  | { type: 'TOGGLE_SUBTITLES' };

// Initial State
const initialState: StudentState = {
  // User State
  student: null,
  isAuthenticated: false,
  
  // Content State
  lessons: [],
  subjects: [],
  currentLesson: null,
  searchResults: [],
  searchFilters: {
    sortBy: 'relevance',
    sortOrder: 'desc'
  },
  
  // Progress State
  progress: [],
  currentProgress: null,
  learningAnalytics: null,
  
  // UI State
  isLoading: false,
  isOffline: false,
  notifications: [],
  theme: 'system',
  
  // Player State
  isPlaying: false,
  currentTime: 0,
  duration: 0,
  volume: 1,
  playbackSpeed: 1,
  quality: 'auto',
  subtitlesEnabled: false,
  
  // App State
  sidebarOpen: false,
  currentView: 'home',
  error: null
};

// Reducer
function studentReducer(state: StudentState, action: StudentAction): StudentState {
  switch (action.type) {
    // Authentication
    case 'SET_STUDENT':
      return {
        ...state,
        student: action.payload,
        isAuthenticated: true
      };
      
    case 'LOGOUT':
      return {
        ...state,
        student: null,
        isAuthenticated: false,
        lessons: [],
        progress: [],
        currentLesson: null,
        currentProgress: null,
        notifications: []
      };
      
    // Content
    case 'SET_LESSONS':
      return {
        ...state,
        lessons: action.payload
      };
      
    case 'ADD_LESSON':
      return {
        ...state,
        lessons: [...state.lessons, action.payload]
      };
      
    case 'UPDATE_LESSON':
      return {
        ...state,
        lessons: state.lessons.map(lesson =>
          lesson.id === action.payload.id
            ? { ...lesson, ...action.payload.updates }
            : lesson
        ),
        currentLesson: state.currentLesson?.id === action.payload.id
          ? { ...state.currentLesson, ...action.payload.updates }
          : state.currentLesson
      };
      
    case 'REMOVE_LESSON':
      return {
        ...state,
        lessons: state.lessons.filter(lesson => lesson.id !== action.payload),
        currentLesson: state.currentLesson?.id === action.payload ? null : state.currentLesson
      };
      
    case 'SET_CURRENT_LESSON':
      return {
        ...state,
        currentLesson: action.payload
      };
      
    case 'SET_SUBJECTS':
      return {
        ...state,
        subjects: action.payload
      };
      
    case 'SET_SEARCH_RESULTS':
      return {
        ...state,
        searchResults: action.payload
      };
      
    case 'SET_SEARCH_FILTERS':
      return {
        ...state,
        searchFilters: { ...state.searchFilters, ...action.payload }
      };
      
    // Progress
    case 'SET_PROGRESS':
      return {
        ...state,
        progress: action.payload
      };
      
    case 'ADD_PROGRESS':
      return {
        ...state,
        progress: [...state.progress, action.payload]
      };
      
    case 'UPDATE_PROGRESS':
      return {
        ...state,
        progress: state.progress.map(p =>
          p.id === action.payload.id
            ? { ...p, ...action.payload.updates }
            : p
        ),
        currentProgress: state.currentProgress?.id === action.payload.id
          ? { ...state.currentProgress, ...action.payload.updates }
          : state.currentProgress
      };
      
    case 'SET_CURRENT_PROGRESS':
      return {
        ...state,
        currentProgress: action.payload
      };
      
    case 'SET_LEARNING_ANALYTICS':
      return {
        ...state,
        learningAnalytics: action.payload
      };
      
    // UI
    case 'SET_LOADING':
      return {
        ...state,
        isLoading: action.payload
      };
      
    case 'SET_OFFLINE':
      return {
        ...state,
        isOffline: action.payload
      };
      
    case 'ADD_NOTIFICATION':
      return {
        ...state,
        notifications: [action.payload, ...state.notifications]
      };
      
    case 'REMOVE_NOTIFICATION':
      return {
        ...state,
        notifications: state.notifications.filter(n => n.id !== action.payload)
      };
      
    case 'MARK_NOTIFICATION_READ':
      return {
        ...state,
        notifications: state.notifications.map(n =>
          n.id === action.payload ? { ...n, read: true } : n
        )
      };
      
    case 'SET_THEME':
      return {
        ...state,
        theme: action.payload
      };
      
    case 'TOGGLE_SIDEBAR':
      return {
        ...state,
        sidebarOpen: !state.sidebarOpen
      };
      
    case 'SET_CURRENT_VIEW':
      return {
        ...state,
        currentView: action.payload
      };
      
    case 'SET_ERROR':
      return {
        ...state,
        error: action.payload
      };
      
    // Player
    case 'SET_PLAYING':
      return {
        ...state,
        isPlaying: action.payload
      };
      
    case 'SET_CURRENT_TIME':
      return {
        ...state,
        currentTime: action.payload
      };
      
    case 'SET_DURATION':
      return {
        ...state,
        duration: action.payload
      };
      
    case 'SET_VOLUME':
      return {
        ...state,
        volume: action.payload
      };
      
    case 'SET_PLAYBACK_SPEED':
      return {
        ...state,
        playbackSpeed: action.payload
      };
      
    case 'SET_QUALITY':
      return {
        ...state,
        quality: action.payload
      };
      
    case 'TOGGLE_SUBTITLES':
      return {
        ...state,
        subtitlesEnabled: !state.subtitlesEnabled
      };
      
    default:
      return state;
  }
}

// Context
const StudentContext = createContext<{
  state: StudentState;
  dispatch: React.Dispatch<StudentAction>;
  
  // Convenience methods
  login: (student: Student) => void;
  logout: () => void;
  setCurrentLesson: (lesson: Lesson | null) => void;
  updateProgress: (lessonId: string, progressData: Partial<Progress>) => void;
  addNotification: (notification: Omit<Notification, 'id' | 'timestamp' | 'read'>) => void;
  toggleTheme: () => void;
  setSearchFilters: (filters: Partial<SearchFilters>) => void;
  clearError: () => void;
} | undefined>(undefined);

// Provider Component
interface StudentProviderProps {
  children: ReactNode;
}

export const StudentProvider: React.FC<StudentProviderProps> = ({ children }) => {
  const [state, dispatch] = useReducer(studentReducer, initialState);

  // Initialize theme
  useEffect(() => {
    const savedTheme = localStorage.getItem('vv-student-theme') as 'light' | 'dark' | 'system' || 'system';
    dispatch({ type: 'SET_THEME', payload: savedTheme });
  }, []);

  // Apply theme
  useEffect(() => {
    const root = document.documentElement;
    
    if (state.theme === 'system') {
      const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
      root.classList.toggle('dark', prefersDark);
    } else {
      root.classList.toggle('dark', state.theme === 'dark');
    }
  }, [state.theme]);

  // Handle online/offline status
  useEffect(() => {
    const handleOnline = () => dispatch({ type: 'SET_OFFLINE', payload: false });
    const handleOffline = () => dispatch({ type: 'SET_OFFLINE', payload: true });

    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);

    // Set initial status
    dispatch({ type: 'SET_OFFLINE', payload: !navigator.onLine });

    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []);

  // Convenience methods
  const login = (student: Student) => {
    dispatch({ type: 'SET_STUDENT', payload: student });
    localStorage.setItem('vv-student-token', student.id);
  };

  const logout = () => {
    dispatch({ type: 'LOGOUT' });
    localStorage.removeItem('vv-student-token');
  };

  const setCurrentLesson = (lesson: Lesson | null) => {
    dispatch({ type: 'SET_CURRENT_LESSON', payload: lesson });
  };

  const updateProgress = (lessonId: string, progressData: Partial<Progress>) => {
    const existingProgress = state.progress.find(p => p.lessonId === lessonId);
    if (existingProgress) {
      dispatch({ 
        type: 'UPDATE_PROGRESS', 
        payload: { id: existingProgress.id, updates: progressData }
      });
    } else {
      // Create new progress entry
      const newProgress: Progress = {
        id: `progress_${Date.now()}`,
        studentId: state.student?.id || '',
        lessonId,
        status: 'in_progress',
        completionPercentage: 0,
        timeSpent: 0,
        lastAccessedAt: new Date().toISOString(),
        ...progressData
      };
      dispatch({ type: 'ADD_PROGRESS', payload: newProgress });
    }
  };

  const addNotification = (notification: Omit<Notification, 'id' | 'timestamp' | 'read'>) => {
    const newNotification: Notification = {
      ...notification,
      id: `notification_${Date.now()}`,
      timestamp: new Date().toISOString(),
      read: false
    };
    dispatch({ type: 'ADD_NOTIFICATION', payload: newNotification });
  };

  const toggleTheme = () => {
    const newTheme = state.theme === 'light' ? 'dark' : 'light';
    dispatch({ type: 'SET_THEME', payload: newTheme });
    localStorage.setItem('vv-student-theme', newTheme);
  };

  const setSearchFilters = (filters: Partial<SearchFilters>) => {
    dispatch({ type: 'SET_SEARCH_FILTERS', payload: filters });
  };

  const clearError = () => {
    dispatch({ type: 'SET_ERROR', payload: null });
  };

  const value = {
    state,
    dispatch,
    login,
    logout,
    setCurrentLesson,
    updateProgress,
    addNotification,
    toggleTheme,
    setSearchFilters,
    clearError
  };

  return (
    <StudentContext.Provider value={value}>
      {children}
    </StudentContext.Provider>
  );
};

// Custom Hook
export const useStudent = () => {
  const context = useContext(StudentContext);
  if (context === undefined) {
    throw new Error('useStudent must be used within a StudentProvider');
  }
  return context;
};

export default StudentContext;
