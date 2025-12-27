import { create } from 'zustand';
import api from '../services/api';

interface Lesson {
  id: string;
  title: string;
  description: string;
  type: 'video' | 'article' | 'quiz' | 'interactive';
  duration: number;
  content: string;
  resources: Resource[];
  order: number;
}

interface Module {
  id: string;
  title: string;
  description: string;
  lessons: Lesson[];
  order: number;
  isLocked: boolean;
}

interface Course {
  id: string;
  title: string;
  description: string;
  thumbnail: string;
  instructor: {
    id: string;
    name: string;
    avatar: string;
  };
  category: string;
  tags: string[];
  difficulty: 'beginner' | 'intermediate' | 'advanced';
  duration: number;
  lessonsCount: number;
  modules: Module[];
  rating: number;
  enrollmentsCount: number;
  price: number;
  isEnrolled: boolean;
  progress?: number;
  lastAccessedLesson?: string;
}

interface CourseFilters {
  category?: string;
  difficulty?: string;
  search?: string;
  sortBy?: 'popular' | 'rating' | 'newest' | 'price';
}

interface CourseState {
  courses: Course[];
  currentCourse: Course | null;
  enrolledCourses: Course[];
  recommendedCourses: Course[];
  filters: CourseFilters;
  isLoading: boolean;
  error: string | null;
  
  // Actions
  fetchCourses: (filters?: CourseFilters) => Promise<void>;
  fetchCourseById: (courseId: string) => Promise<void>;
  fetchEnrolledCourses: () => Promise<void>;
  fetchRecommendedCourses: () => Promise<void>;
  enrollInCourse: (courseId: string) => Promise<void>;
  setFilters: (filters: CourseFilters) => void;
  clearError: () => void;
}

export const useCourseStore = create<CourseState>((set, get) => ({
  courses: [],
  currentCourse: null,
  enrolledCourses: [],
  recommendedCourses: [],
  filters: {},
  isLoading: false,
  error: null,

  fetchCourses: async (filters?: CourseFilters) => {
    set({ isLoading: true, error: null });
    try {
      const params = new URLSearchParams();
      if (filters) {
        Object.entries(filters).forEach(([key, value]) => {
          if (value) params.append(key, value);
        });
      }
      
      const response = await api.get(`/courses?${params.toString()}`);
      set({
        courses: response.data.courses,
        isLoading: false,
      });
    } catch (error: any) {
      const message = error.response?.data?.message || 'Failed to fetch courses.';
      set({ error: message, isLoading: false });
    }
  },

  fetchCourseById: async (courseId: string) => {
    set({ isLoading: true, error: null });
    try {
      const response = await api.get(`/courses/${courseId}`);
      set({
        currentCourse: response.data,
        isLoading: false,
      });
    } catch (error: any) {
      const message = error.response?.data?.message || 'Failed to fetch course.';
      set({ error: message, isLoading: false });
    }
  },

  fetchEnrolledCourses: async () => {
    set({ isLoading: true, error: null });
    try {
      const response = await api.get('/courses/enrolled');
      set({
        enrolledCourses: response.data.courses,
        isLoading: false,
      });
    } catch (error: any) {
      const message = error.response?.data?.message || 'Failed to fetch enrolled courses.';
      set({ error: message, isLoading: false });
    }
  },

  fetchRecommendedCourses: async () => {
    set({ isLoading: true, error: null });
    try {
      const response = await api.get('/courses/recommended');
      set({
        recommendedCourses: response.data.courses,
        isLoading: false,
      });
    } catch (error: any) {
      const message = error.response?.data?.message || 'Failed to fetch recommendations.';
      set({ error: message, isLoading: false });
    }
  },

  enrollInCourse: async (courseId: string) => {
    set({ isLoading: true, error: null });
    try {
      await api.post(`/courses/${courseId}/enroll`);
      await get().fetchCourseById(courseId);
      await get().fetchEnrolledCourses();
    } catch (error: any) {
      const message = error.response?.data?.message || 'Failed to enroll in course.';
      set({ error: message, isLoading: false });
      throw error;
    }
  },

  setFilters: (filters: CourseFilters) => {
    set({ filters });
  },

  clearError: () => set({ error: null }),
}));
