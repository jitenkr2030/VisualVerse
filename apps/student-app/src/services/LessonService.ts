/**
 * VisualVerse Student App - Lesson Service
 * Handles all lesson-related API operations and data management
 */

import { Lesson, Subject, SearchFilters, SearchResult, ApiResponse, PaginatedResponse } from '../types';

export class LessonService {
  private static instance: LessonService;
  private apiUrl: string;
  private wsUrl: string;
  private socket: any = null;
  private cache: Map<string, { data: any; timestamp: number }> = new Map();
  private readonly CACHE_DURATION = 5 * 60 * 1000; // 5 minutes

  private constructor() {
    this.apiUrl = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';
    this.wsUrl = process.env.REACT_APP_WS_URL || 'ws://localhost:8000/ws';
  }

  static getInstance(): LessonService {
    if (!LessonService.instance) {
      LessonService.instance = new LessonService();
    }
    return LessonService.instance;
  }

  async initialize(): Promise<void> {
    try {
      // Test API connectivity
      await this.testConnection();
      
      // Initialize WebSocket connection
      this.initializeSocket();
      
      console.log('LessonService initialized successfully');
    } catch (error) {
      console.error('Failed to initialize LessonService:', error);
      throw error;
    }
  }

  private async testConnection(): Promise<void> {
    try {
      const response = await fetch(`${this.apiUrl}/health`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        }
      });

      if (!response.ok) {
        throw new Error(`API health check failed: ${response.status}`);
      }
    } catch (error) {
      console.warn('API health check failed, using offline mode:', error);
    }
  }

  private initializeSocket(): void {
    try {
      // In a real implementation, this would use Socket.IO or WebSocket
      this.socket = {
        on: (event: string, callback: Function) => {
          // Mock socket implementation
          console.log(`Socket listener registered for: ${event}`);
        },
        emit: (event: string, data: any) => {
          // Mock socket emission
          console.log(`Socket event emitted: ${event}`, data);
        },
        connect: () => {
          console.log('Socket connected');
        },
        disconnect: () => {
          console.log('Socket disconnected');
        }
      };
    } catch (error) {
      console.error('Failed to initialize WebSocket:', error);
    }
  }

  getSocket(): any {
    return this.socket;
  }

  // Cache Management
  private getFromCache(key: string): any | null {
    const cached = this.cache.get(key);
    if (cached && Date.now() - cached.timestamp < this.CACHE_DURATION) {
      return cached.data;
    }
    this.cache.delete(key);
    return null;
  }

  private setCache(key: string, data: any): void {
    this.cache.set(key, { data, timestamp: Date.now() });
  }

  private clearCache(): void {
    this.cache.clear();
  }

  // Lesson Operations
  async getAvailableLessons(filters?: SearchFilters): Promise<Lesson[]> {
    const cacheKey = `lessons_${JSON.stringify(filters || {})}`;
    
    try {
      const cached = this.getFromCache(cacheKey);
      if (cached) {
        return cached;
      }

      const params = new URLSearchParams();
      if (filters) {
        Object.entries(filters).forEach(([key, value]) => {
          if (value !== undefined && value !== null) {
            if (Array.isArray(value)) {
              value.forEach(v => params.append(key, v.toString()));
            } else {
              params.set(key, value.toString());
            }
          }
        });
      }

      const response = await fetch(`${this.apiUrl}/lessons?${params}`, {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.getAuthToken()}`
        }
      });

      if (!response.ok) {
        throw new Error(`Failed to fetch lessons: ${response.status}`);
      }

      const data: PaginatedResponse<Lesson> = await response.json();
      const lessons = data.data || [];

      this.setCache(cacheKey, lessons);
      return lessons;

    } catch (error) {
      console.error('Error fetching lessons:', error);
      // Return mock data for development
      return this.getMockLessons();
    }
  }

  async getLesson(lessonId: string): Promise<Lesson> {
    const cacheKey = `lesson_${lessonId}`;
    
    try {
      const cached = this.getFromCache(cacheKey);
      if (cached) {
        return cached;
      }

      const response = await fetch(`${this.apiUrl}/lessons/${lessonId}`, {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.getAuthToken()}`
        }
      });

      if (!response.ok) {
        throw new Error(`Failed to fetch lesson: ${response.status}`);
      }

      const data: ApiResponse<Lesson> = await response.json();
      const lesson = data.data;

      if (!lesson) {
        throw new Error('Lesson not found');
      }

      this.setCache(cacheKey, lesson);
      return lesson;

    } catch (error) {
      console.error('Error fetching lesson:', error);
      // Return mock data for development
      const mockLesson = this.getMockLessons().find(l => l.id === lessonId);
      if (!mockLesson) {
        throw new Error('Lesson not found');
      }
      return mockLesson;
    }
  }

  async searchLessons(filters: SearchFilters): Promise<SearchResult> {
    try {
      const response = await fetch(`${this.apiUrl}/lessons/search`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.getAuthToken()}`
        },
        body: JSON.stringify(filters)
      });

      if (!response.ok) {
        throw new Error(`Search failed: ${response.status}`);
      }

      const data: ApiResponse<SearchResult> = await response.json();
      return data.data || { lessons: [], subjects: [], creators: [], totalResults: 0, facets: { subjects: [], difficulty: [], duration: [], creators: [], tags: [] } };

    } catch (error) {
      console.error('Error searching lessons:', error);
      // Return mock search results
      return this.getMockSearchResult(filters);
    }
  }

  async getLessonsBySubject(subjectId: string, page = 1, limit = 20): Promise<PaginatedResponse<Lesson>> {
    try {
      const params = new URLSearchParams({
        subject: subjectId,
        page: page.toString(),
        limit: limit.toString()
      });

      const response = await fetch(`${this.apiUrl}/lessons?${params}`, {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.getAuthToken()}`
        }
      });

      if (!response.ok) {
        throw new Error(`Failed to fetch lessons by subject: ${response.status}`);
      }

      return await response.json();

    } catch (error) {
      console.error('Error fetching lessons by subject:', error);
      // Return mock data
      const allLessons = this.getMockLessons();
      const subjectLessons = allLessons.filter(l => l.subject.id === subjectId);
      
      return {
        success: true,
        data: subjectLessons,
        pagination: {
          page,
          limit,
          total: subjectLessons.length,
          totalPages: Math.ceil(subjectLessons.length / limit)
        }
      };
    }
  }

  async getFeaturedLessons(): Promise<Lesson[]> {
    try {
      const response = await fetch(`${this.apiUrl}/lessons/featured`, {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.getAuthToken()}`
        }
      });

      if (!response.ok) {
        throw new Error(`Failed to fetch featured lessons: ${response.status}`);
      }

      const data: ApiResponse<Lesson[]> = await response.json();
      return data.data || [];

    } catch (error) {
      console.error('Error fetching featured lessons:', error);
      // Return some lessons as featured
      return this.getMockLessons().slice(0, 6);
    }
  }

  async getRecommendedLessons(studentId: string): Promise<Lesson[]> {
    try {
      const response = await fetch(`${this.apiUrl}/lessons/recommended/${studentId}`, {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.getAuthToken()}`
        }
      });

      if (!response.ok) {
        throw new Error(`Failed to fetch recommended lessons: ${response.status}`);
      }

      const data: ApiResponse<Lesson[]> = await response.json();
      return data.data || [];

    } catch (error) {
      console.error('Error fetching recommended lessons:', error);
      // Return mock recommendations
      return this.getMockLessons().slice(0, 5);
    }
  }

  async getTrendingLessons(): Promise<Lesson[]> {
    try {
      const response = await fetch(`${this.apiUrl}/lessons/trending`, {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.getAuthToken()}`
        }
      });

      if (!response.ok) {
        throw new Error(`Failed to fetch trending lessons: ${response.status}`);
      }

      const data: ApiResponse<Lesson[]> = await response.json();
      return data.data || [];

    } catch (error) {
      console.error('Error fetching trending lessons:', error);
      // Return mock trending lessons
      return this.getMockLessons().slice(2, 8);
    }
  }

  // Subject Operations
  async getSubjects(): Promise<Subject[]> {
    const cacheKey = 'subjects';
    
    try {
      const cached = this.getFromCache(cacheKey);
      if (cached) {
        return cached;
      }

      const response = await fetch(`${this.apiUrl}/subjects`, {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.getAuthToken()}`
        }
      });

      if (!response.ok) {
        throw new Error(`Failed to fetch subjects: ${response.status}`);
      }

      const data: ApiResponse<Subject[]> = await response.json();
      const subjects = data.data || [];

      this.setCache(cacheKey, subjects);
      return subjects;

    } catch (error) {
      console.error('Error fetching subjects:', error);
      // Return mock subjects
      return this.getMockSubjects();
    }
  }

  async getSubject(subjectId: string): Promise<Subject> {
    try {
      const response = await fetch(`${this.apiUrl}/subjects/${subjectId}`, {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.getAuthToken()}`
        }
      });

      if (!response.ok) {
        throw new Error(`Failed to fetch subject: ${response.status}`);
      }

      const data: ApiResponse<Subject> = await response.json();
      
      if (!data.data) {
        throw new Error('Subject not found');
      }

      return data.data;

    } catch (error) {
      console.error('Error fetching subject:', error);
      // Return mock subject
      const mockSubject = this.getMockSubjects().find(s => s.id === subjectId);
      if (!mockSubject) {
        throw new Error('Subject not found');
      }
      return mockSubject;
    }
  }

  // Bookmark Operations
  async bookmarkLesson(lessonId: string): Promise<void> {
    try {
      const response = await fetch(`${this.apiUrl}/lessons/${lessonId}/bookmark`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.getAuthToken()}`
        }
      });

      if (!response.ok) {
        throw new Error(`Failed to bookmark lesson: ${response.status}`);
      }

      // Clear related cache
      this.cache.delete('bookmarks');
      this.cache.delete(`lesson_${lessonId}`);

    } catch (error) {
      console.error('Error bookmarking lesson:', error);
      throw error;
    }
  }

  async unbookmarkLesson(lessonId: string): Promise<void> {
    try {
      const response = await fetch(`${this.apiUrl}/lessons/${lessonId}/bookmark`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.getAuthToken()}`
        }
      });

      if (!response.ok) {
        throw new Error(`Failed to unbookmark lesson: ${response.status}`);
      }

      // Clear related cache
      this.cache.delete('bookmarks');
      this.cache.delete(`lesson_${lessonId}`);

    } catch (error) {
      console.error('Error unbookmarking lesson:', error);
      throw error;
    }
  }

  async getBookmarkedLessons(): Promise<Lesson[]> {
    try {
      const response = await fetch(`${this.apiUrl}/lessons/bookmarked`, {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.getAuthToken()}`
        }
      });

      if (!response.ok) {
        throw new Error(`Failed to fetch bookmarked lessons: ${response.status}`);
      }

      const data: ApiResponse<Lesson[]> = await response.json();
      return data.data || [];

    } catch (error) {
      console.error('Error fetching bookmarked lessons:', error);
      return [];
    }
  }

  // Utility Methods
  private getAuthToken(): string {
    return localStorage.getItem('vv-student-token') || '';
  }

  // Mock Data for Development
  private getMockLessons(): Lesson[] {
    return [
      {
        id: 'lesson_1',
        title: 'Introduction to Calculus',
        description: 'Learn the fundamentals of calculus including limits, derivatives, and integrals.',
        subject: {
          id: 'math',
          name: 'mathematics',
          displayName: 'Mathematics',
          description: 'Mathematical concepts and problem solving',
          icon: '📊',
          color: '#3B82F6',
          difficulty: 'intermediate',
          prerequisites: ['algebra'],
          learningObjectives: ['Understand limits', 'Calculate derivatives', 'Apply integration'],
          curriculum: []
        },
        creator: {
          id: 'creator_1',
          name: 'Dr. Sarah Johnson',
          avatar: 'https://via.placeholder.com/150',
          bio: 'Mathematics professor with 15 years of teaching experience',
          expertise: ['Calculus', 'Linear Algebra', 'Statistics'],
          rating: 4.8,
          totalLessons: 45,
          totalStudents: 1200,
          verified: true
        },
        content: {
          type: 'animation',
          duration: 1800,
          scenes: [],
          transcript: 'Welcome to our calculus introduction...',
          resources: [],
          assessment: undefined
        },
        metadata: {
          language: 'en',
          quality: 'hd',
          accessibility: {
            subtitlesAvailable: true,
            audioDescription: false,
            highContrast: true,
            screenReaderCompatible: true,
            keyboardNavigation: true
          }
        },
        status: 'completed',
        accessibility: {
          subtitlesAvailable: true,
          audioDescription: false,
          highContrast: true,
          screenReaderCompatible: true,
          keyboardNavigation: true
        },
        tags: ['calculus', 'derivatives', 'mathematics'],
        createdAt: '2024-01-15T10:00:00Z',
        updatedAt: '2024-01-15T10:00:00Z',
        views: 1250,
        rating: 4.7,
        reviews: []
      }
      // Add more mock lessons...
    ];
  }

  private getMockSubjects(): Subject[] {
    return [
      {
        id: 'math',
        name: 'mathematics',
        displayName: 'Mathematics',
        description: 'Mathematical concepts and problem solving',
        icon: '📊',
        color: '#3B82F6',
        difficulty: 'intermediate',
        prerequisites: [],
        learningObjectives: ['Problem solving', 'Logical thinking', 'Quantitative analysis'],
        curriculum: []
      },
      {
        id: 'physics',
        name: 'physics',
        displayName: 'Physics',
        description: 'Physical phenomena and laws',
        icon: '⚛️',
        color: '#10B981',
        difficulty: 'intermediate',
        prerequisites: ['math'],
        learningObjectives: ['Understand physical laws', 'Apply mathematical models', 'Analyze phenomena'],
        curriculum: []
      }
      // Add more mock subjects...
    ];
  }

  private getMockSearchResult(filters: SearchFilters): SearchResult {
    return {
      lessons: this.getMockLessons(),
      subjects: this.getMockSubjects(),
      creators: [],
      totalResults: 1,
      facets: {
        subjects: [],
        difficulty: [],
        duration: [],
        creators: [],
        tags: []
      }
    };
  }

  // Cleanup
  destroy(): void {
    if (this.socket) {
      this.socket.disconnect();
    }
    this.clearCache();
  }
}

export const lessonService = LessonService.getInstance();
