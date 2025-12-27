/**
 * VisualVerse Student App - Progress Service
 * Handles student learning progress tracking and analytics
 */

import { Progress, LearningAnalytics, ActivityItem, ApiResponse, PaginatedResponse } from '../types';

export class ProgressService {
  private static instance: ProgressService;
  private apiUrl: string;
  private cache: Map<string, { data: any; timestamp: number }> = new Map();
  private readonly CACHE_DURATION = 2 * 60 * 1000; // 2 minutes

  private constructor() {
    this.apiUrl = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';
  }

  static getInstance(): ProgressService {
    if (!ProgressService.instance) {
      ProgressService.instance = new ProgressService();
    }
    return ProgressService.instance;
  }

  async initialize(): Promise<void> {
    try {
      console.log('ProgressService initialized successfully');
    } catch (error) {
      console.error('Failed to initialize ProgressService:', error);
      throw error;
    }
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

  // Progress Tracking
  async getStudentProgress(studentId: string): Promise<Progress[]> {
    const cacheKey = `progress_${studentId}`;
    
    try {
      const cached = this.getFromCache(cacheKey);
      if (cached) {
        return cached;
      }

      const response = await fetch(`${this.apiUrl}/progress/student/${studentId}`, {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.getAuthToken()}`
        }
      });

      if (!response.ok) {
        throw new Error(`Failed to fetch progress: ${response.status}`);
      }

      const data: ApiResponse<Progress[]> = await response.json();
      const progress = data.data || [];

      this.setCache(cacheKey, progress);
      return progress;

    } catch (error) {
      console.error('Error fetching student progress:', error);
      // Return mock data for development
      return this.getMockProgress(studentId);
    }
  }

  async getLessonProgress(lessonId: string, studentId: string): Promise<Progress | null> {
    try {
      const response = await fetch(`${this.apiUrl}/progress/lesson/${lessonId}/student/${studentId}`, {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.getAuthToken()}`
        }
      });

      if (!response.ok) {
        throw new Error(`Failed to fetch lesson progress: ${response.status}`);
      }

      const data: ApiResponse<Progress> = await response.json();
      return data.data || null;

    } catch (error) {
      console.error('Error fetching lesson progress:', error);
      // Return mock data
      const mockProgress = this.getMockProgress(studentId);
      return mockProgress.find(p => p.lessonId === lessonId) || null;
    }
  }

  async updateProgress(lessonId: string, updates: Partial<Progress>): Promise<Progress> {
    try {
      const response = await fetch(`${this.apiUrl}/progress/lesson/${lessonId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.getAuthToken()}`
        },
        body: JSON.stringify(updates)
      });

      if (!response.ok) {
        throw new Error(`Failed to update progress: ${response.status}`);
      }

      const data: ApiResponse<Progress> = await response.json();
      const progress = data.data!;

      // Clear related cache
      this.clearProgressCache(lessonId);

      return progress;

    } catch (error) {
      console.error('Error updating progress:', error);
      throw error;
    }
  }

  async startLesson(lessonId: string): Promise<Progress> {
    try {
      const response = await fetch(`${this.apiUrl}/progress/lesson/${lessonId}/start`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.getAuthToken()}`
        }
      });

      if (!response.ok) {
        throw new Error(`Failed to start lesson: ${response.status}`);
      }

      const data: ApiResponse<Progress> = await response.json();
      const progress = data.data!;

      // Clear related cache
      this.clearProgressCache(lessonId);

      return progress;

    } catch (error) {
      console.error('Error starting lesson:', error);
      // Create mock progress for development
      const mockProgress: Progress = {
        id: `progress_${Date.now()}`,
        studentId: this.getCurrentStudentId(),
        lessonId,
        status: 'in_progress',
        completionPercentage: 0,
        timeSpent: 0,
        lastAccessedAt: new Date().toISOString()
      };

      return mockProgress;
    }
  }

  async completeLesson(lessonId: string): Promise<Progress> {
    try {
      const response = await fetch(`${this.apiUrl}/progress/lesson/${lessonId}/complete`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.getAuthToken()}`
        }
      });

      if (!response.ok) {
        throw new Error(`Failed to complete lesson: ${response.status}`);
      }

      const data: ApiResponse<Progress> = await response.json();
      const progress = data.data!;

      // Clear related cache
      this.clearProgressCache(lessonId);

      return progress;

    } catch (error) {
      console.error('Error completing lesson:', error);
      throw error;
    }
  }

  async trackTimeSpent(lessonId: string, timeSpent: number): Promise<void> {
    try {
      const response = await fetch(`${this.apiUrl}/progress/lesson/${lessonId}/time`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.getAuthToken()}`
        },
        body: JSON.stringify({ timeSpent })
      });

      if (!response.ok) {
        console.warn(`Failed to track time spent: ${response.status}`);
      }

    } catch (error) {
      console.error('Error tracking time spent:', error);
    }
  }

  async updateCompletionPercentage(lessonId: string, percentage: number): Promise<Progress> {
    try {
      const response = await fetch(`${this.apiUrl}/progress/lesson/${lessonId}/completion`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.getAuthToken()}`
        },
        body: JSON.stringify({ completionPercentage: percentage })
      });

      if (!response.ok) {
        throw new Error(`Failed to update completion percentage: ${response.status}`);
      }

      const data: ApiResponse<Progress> = await response.json();
      const progress = data.data!;

      // Clear related cache
      this.clearProgressCache(lessonId);

      return progress;

    } catch (error) {
      console.error('Error updating completion percentage:', error);
      throw error;
    }
  }

  // Analytics
  async getLearningAnalytics(studentId: string): Promise<LearningAnalytics> {
    const cacheKey = `analytics_${studentId}`;
    
    try {
      const cached = this.getFromCache(cacheKey);
      if (cached) {
        return cached;
      }

      const response = await fetch(`${this.apiUrl}/analytics/student/${studentId}`, {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.getAuthToken()}`
        }
      });

      if (!response.ok) {
        throw new Error(`Failed to fetch learning analytics: ${response.status}`);
      }

      const data: ApiResponse<LearningAnalytics> = await response.json();
      const analytics = data.data || this.getMockAnalytics(studentId);

      this.setCache(cacheKey, analytics);
      return analytics;

    } catch (error) {
      console.error('Error fetching learning analytics:', error);
      return this.getMockAnalytics(studentId);
    }
  }

  async getActivityHistory(studentId: string, limit = 20, offset = 0): Promise<PaginatedResponse<ActivityItem>> {
    try {
      const params = new URLSearchParams({
        limit: limit.toString(),
        offset: offset.toString()
      });

      const response = await fetch(`${this.apiUrl}/analytics/student/${studentId}/activity?${params}`, {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.getAuthToken()}`
        }
      });

      if (!response.ok) {
        throw new Error(`Failed to fetch activity history: ${response.status}`);
      }

      return await response.json();

    } catch (error) {
      console.error('Error fetching activity history:', error);
      // Return mock data
      return {
        success: true,
        data: this.getMockActivityHistory(),
        pagination: {
          page: Math.floor(offset / limit) + 1,
          limit,
          total: 20,
          totalPages: 1
        }
      };
    }
  }

  async getLearningStreak(studentId: string): Promise<number> {
    try {
      const response = await fetch(`${this.apiUrl}/analytics/student/${studentId}/streak`, {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.getAuthToken()}`
        }
      });

      if (!response.ok) {
        throw new Error(`Failed to fetch learning streak: ${response.status}`);
      }

      const data: ApiResponse<{ streak: number }> = await response.json();
      return data.data?.streak || 0;

    } catch (error) {
      console.error('Error fetching learning streak:', error);
      return 5; // Mock streak for development
    }
  }

  async getSubjectProgress(studentId: string): Promise<Record<string, number>> {
    try {
      const response = await fetch(`${this.apiUrl}/analytics/student/${studentId}/subject-progress`, {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.getAuthToken()}`
        }
      });

      if (!response.ok) {
        throw new Error(`Failed to fetch subject progress: ${response.status}`);
      }

      const data: ApiResponse<Record<string, number>> = await response.json();
      return data.data || {};

    } catch (error) {
      console.error('Error fetching subject progress:', error);
      return {
        mathematics: 75,
        physics: 60,
        chemistry: 45,
        computer_science: 80
      };
    }
  }

  async getSkillLevel(studentId: string, subjectId: string): Promise<'beginner' | 'intermediate' | 'advanced'> {
    try {
      const response = await fetch(`${this.apiUrl}/analytics/student/${studentId}/skill-level/${subjectId}`, {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.getAuthToken()}`
        }
      });

      if (!response.ok) {
        throw new Error(`Failed to fetch skill level: ${response.status}`);
      }

      const data: ApiResponse<{ skillLevel: string }> = await response.json();
      return (data.data?.skillLevel as any) || 'intermediate';

    } catch (error) {
      console.error('Error fetching skill level:', error);
      return 'intermediate';
    }
  }

  // Achievements and Gamification
  async getAchievements(studentId: string): Promise<any[]> {
    try {
      const response = await fetch(`${this.apiUrl}/gamification/student/${studentId}/achievements`, {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.getAuthToken()}`
        }
      });

      if (!response.ok) {
        throw new Error(`Failed to fetch achievements: ${response.status}`);
      }

      const data: ApiResponse<any[]> = await response.json();
      return data.data || [];

    } catch (error) {
      console.error('Error fetching achievements:', error);
      return [
        {
          id: 'first_lesson',
          title: 'First Steps',
          description: 'Complete your first lesson',
          icon: '🎯',
          earned: true,
          earnedAt: '2024-01-15T10:00:00Z'
        }
      ];
    }
  }

  async getLeaderboard(subjectId?: string): Promise<any[]> {
    try {
      const params = subjectId ? `?subject=${subjectId}` : '';
      const response = await fetch(`${this.apiUrl}/gamification/leaderboard${params}`, {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.getAuthToken()}`
        }
      });

      if (!response.ok) {
        throw new Error(`Failed to fetch leaderboard: ${response.status}`);
      }

      const data: ApiResponse<any[]> = await response.json();
      return data.data || [];

    } catch (error) {
      console.error('Error fetching leaderboard:', error);
      return [
        {
          rank: 1,
          student: { name: 'Alex Johnson', avatar: 'https://via.placeholder.com/50' },
          score: 1250
        }
      ];
    }
  }

  // Utility Methods
  private getAuthToken(): string {
    return localStorage.getItem('vv-student-token') || '';
  }

  private getCurrentStudentId(): string {
    return localStorage.getItem('vv-student-id') || 'student_123';
  }

  private clearProgressCache(lessonId: string): void {
    const keysToDelete: string[] = [];
    this.cache.forEach((_, key) => {
      if (key.includes('progress_') || key.includes('analytics_')) {
        keysToDelete.push(key);
      }
    });
    keysToDelete.forEach(key => this.cache.delete(key));
  }

  // Mock Data for Development
  private getMockProgress(studentId: string): Progress[] {
    return [
      {
        id: 'progress_1',
        studentId,
        lessonId: 'lesson_1',
        status: 'completed',
        completionPercentage: 100,
        timeSpent: 1800,
        lastAccessedAt: '2024-01-15T10:00:00Z',
        completedAt: '2024-01-15T12:00:00Z'
      },
      {
        id: 'progress_2',
        studentId,
        lessonId: 'lesson_2',
        status: 'in_progress',
        completionPercentage: 65,
        timeSpent: 1200,
        lastAccessedAt: '2024-01-16T14:30:00Z'
      }
    ];
  }

  private getMockAnalytics(studentId: string): LearningAnalytics {
    return {
      totalTimeSpent: 3600,
      lessonsCompleted: 12,
      subjectsExplored: 4,
      averageSessionDuration: 25,
      learningStreak: 5,
      preferredSubjects: ['mathematics', 'physics'],
      skillLevel: 'intermediate',
      recentActivity: this.getMockActivityHistory()
    };
  }

  private getMockActivityHistory(): ActivityItem[] {
    return [
      {
        type: 'lesson_completed',
        lessonId: 'lesson_1',
        description: 'Completed "Introduction to Calculus"',
        timestamp: '2024-01-15T12:00:00Z',
        metadata: { duration: 1800, score: 85 }
      },
      {
        type: 'lesson_started',
        lessonId: 'lesson_2',
        description: 'Started "Physics Fundamentals"',
        timestamp: '2024-01-16T14:30:00Z',
        metadata: { duration: 1200 }
      }
    ];
  }

  // Cleanup
  destroy(): void {
    this.clearCache();
  }
}

export const progressService = ProgressService.getInstance();
