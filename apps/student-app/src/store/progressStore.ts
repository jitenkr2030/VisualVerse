import { create } from 'zustand';
import api from '../services/api';

interface LessonProgress {
  lessonId: string;
  courseId: string;
  status: 'not_started' | 'in_progress' | 'completed';
  progress: number;
  timeSpent: number;
  lastAccessedAt: string;
  completedAt?: string;
  quizScore?: number;
  notes?: string;
  bookmarks?: string[];
}

interface CourseProgress {
  courseId: string;
  totalLessons: number;
  completedLessons: number;
  progress: number;
  totalTimeSpent: number;
  currentModule: string;
  currentLesson: string;
  lastAccessedAt: string;
}

interface Streak {
  current: number;
  longest: number;
  lastActivity: string;
}

interface UserStats {
  totalCoursesEnrolled: number;
  totalCoursesCompleted: number;
  totalLessonsCompleted: number;
  totalTimeSpent: number;
  averageQuizScore: number;
  streak: Streak;
  achievements: string[];
  rank: number;
}

interface ProgressState {
  lessonProgress: Record<string, LessonProgress>;
  courseProgress: Record<string, CourseProgress>;
  userStats: UserStats | null;
  isLoading: boolean;
  error: string | null;
  
  // Actions
  fetchLessonProgress: (lessonId: string) => Promise<LessonProgress | null>;
  updateLessonProgress: (lessonId: string, data: Partial<LessonProgress>) => Promise<void>;
  fetchCourseProgress: (courseId: string) => Promise<CourseProgress | null>;
  fetchUserStats: () => Promise<void>;
  markLessonComplete: (lessonId: string, courseId: string) => Promise<void>;
  clearError: () => void;
}

export const useProgressStore = create<ProgressState>((set, get) => ({
  lessonProgress: {},
  courseProgress: {},
  userStats: null,
  isLoading: false,
  error: null,

  fetchLessonProgress: async (lessonId: string) => {
    const existing = get().lessonProgress[lessonId];
    if (existing) return existing;

    set({ isLoading: true, error: null });
    try {
      const response = await api.get(`/progress/lessons/${lessonId}`);
      const progress = response.data;
      
      set((state) => ({
        lessonProgress: {
          ...state.lessonProgress,
          [lessonId]: progress,
        },
        isLoading: false,
      }));
      
      return progress;
    } catch (error: any) {
      set({ error: error.response?.data?.message || 'Failed to fetch progress', isLoading: false });
      return null;
    }
  },

  updateLessonProgress: async (lessonId: string, data: Partial<LessonProgress>) => {
    set({ isLoading: true, error: null });
    try {
      const response = await api.put(`/progress/lessons/${lessonId}`, data);
      
      set((state) => ({
        lessonProgress: {
          ...state.lessonProgress,
          [lessonId]: response.data,
        },
        isLoading: false,
      }));
    } catch (error: any) {
      set({ error: error.response?.data?.message || 'Failed to update progress', isLoading: false });
      throw error;
    }
  },

  fetchCourseProgress: async (courseId: string) => {
    const existing = get().courseProgress[courseId];
    if (existing) return existing;

    set({ isLoading: true, error: null });
    try {
      const response = await api.get(`/progress/courses/${courseId}`);
      const progress = response.data;
      
      set((state) => ({
        courseProgress: {
          ...state.courseProgress,
          [courseId]: progress,
        },
        isLoading: false,
      }));
      
      return progress;
    } catch (error: any) {
      set({ error: error.response?.data?.message || 'Failed to fetch course progress', isLoading: false });
      return null;
    }
  },

  fetchUserStats: async () => {
    set({ isLoading: true, error: null });
    try {
      const response = await api.get('/progress/stats');
      set({
        userStats: response.data,
        isLoading: false,
      });
    } catch (error: any) {
      set({ error: error.response?.data?.message || 'Failed to fetch stats', isLoading: false });
    }
  },

  markLessonComplete: async (lessonId: string, courseId: string) => {
    set({ isLoading: true, error: null });
    try {
      const response = await api.post(`/progress/lessons/${lessonId}/complete`);
      
      set((state) => ({
        lessonProgress: {
          ...state.lessonProgress,
          [lessonId]: response.data.lessonProgress,
        },
        isLoading: false,
      }));

      // Also update course progress
      await get().fetchCourseProgress(courseId);
      
      // Update user stats
      await get().fetchUserStats();
    } catch (error: any) {
      set({ error: error.response?.data?.message || 'Failed to mark lesson complete', isLoading: false });
      throw error;
    }
  },

  clearError: () => set({ error: null }),
}));
