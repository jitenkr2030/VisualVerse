/**
 * VisualVerse Student App - User Service
 * Handles user authentication and profile management
 */

import { Student, StudentPreferences, ApiResponse } from '../types';

export class UserService {
  private static instance: UserService;
  private apiUrl: string;
  private currentStudent: Student | null = null;

  private constructor() {
    this.apiUrl = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';
  }

  static getInstance(): UserService {
    if (!UserService.instance) {
      UserService.instance = new UserService();
    }
    return UserService.instance;
  }

  async initialize(): Promise<void> {
    try {
      // Check for existing authentication
      const token = localStorage.getItem('vv-student-token');
      if (token) {
        await this.validateToken(token);
      }

      console.log('UserService initialized successfully');
    } catch (error) {
      console.error('Failed to initialize UserService:', error);
      // Clear invalid token
      localStorage.removeItem('vv-student-token');
    }
  }

  // Authentication Methods
  async login(email: string, password: string): Promise<Student> {
    try {
      const response = await fetch(`${this.apiUrl}/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password })
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.message || 'Login failed');
      }

      const data: ApiResponse<{ student: Student; token: string }> = await response.json();
      const { student, token } = data.data!;

      if (!token) {
        throw new Error('No authentication token received');
      }

      // Store token and student data
      localStorage.setItem('vv-student-token', token);
      this.currentStudent = student;

      return student;

    } catch (error) {
      console.error('Login error:', error);
      throw error;
    }
  }

  async register(userData: {
    name: string;
    email: string;
    password: string;
    gradeLevel: string;
    school?: string;
  }): Promise<Student> {
    try {
      const response = await fetch(`${this.apiUrl}/auth/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData)
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.message || 'Registration failed');
      }

      const data: ApiResponse<{ student: Student; token: string }> = await response.json();
      const { student, token } = data.data!;

      if (!token) {
        throw new Error('No authentication token received');
      }

      // Store token and student data
      localStorage.setItem('vv-student-token', token);
      this.currentStudent = student;

      return student;

    } catch (error) {
      console.error('Registration error:', error);
      throw error;
    }
  }

  async logout(): Promise<void> {
    try {
      const token = this.getAuthToken();
      if (token) {
        await fetch(`${this.apiUrl}/auth/logout`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          }
        });
      }
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      // Clear local data regardless of API call success
      localStorage.removeItem('vv-student-token');
      this.currentStudent = null;
    }
  }

  async validateToken(token: string): Promise<boolean> {
    try {
      const response = await fetch(`${this.apiUrl}/auth/validate`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (!response.ok) {
        throw new Error('Token validation failed');
      }

      const data: ApiResponse<Student> = await response.json();
      this.currentStudent = data.data || null;
      
      return !!this.currentStudent;

    } catch (error) {
      console.error('Token validation error:', error);
      return false;
    }
  }

  // Profile Methods
  async getCurrentStudent(): Promise<Student> {
    if (this.currentStudent) {
      return this.currentStudent;
    }

    try {
      const token = this.getAuthToken();
      if (!token) {
        throw new Error('No authentication token');
      }

      const response = await fetch(`${this.apiUrl}/users/profile`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (!response.ok) {
        throw new Error('Failed to fetch profile');
      }

      const data: ApiResponse<Student> = await response.json();
      this.currentStudent = data.data!;
      
      return this.currentStudent;

    } catch (error) {
      console.error('Error fetching profile:', error);
      // Return mock student for development
      return this.getMockStudent();
    }
  }

  async updateProfile(updates: Partial<Student>): Promise<Student> {
    try {
      const token = this.getAuthToken();
      if (!token) {
        throw new Error('No authentication token');
      }

      const response = await fetch(`${this.apiUrl}/users/profile`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(updates)
      });

      if (!response.ok) {
        throw new Error('Failed to update profile');
      }

      const data: ApiResponse<Student> = await response.json();
      this.currentStudent = data.data!;
      
      return this.currentStudent;

    } catch (error) {
      console.error('Error updating profile:', error);
      throw error;
    }
  }

  async updatePreferences(preferences: Partial<StudentPreferences>): Promise<StudentPreferences> {
    try {
      const token = this.getAuthToken();
      if (!token) {
        throw new Error('No authentication token');
      }

      const response = await fetch(`${this.apiUrl}/users/preferences`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(preferences)
      });

      if (!response.ok) {
        throw new Error('Failed to update preferences');
      }

      const data: ApiResponse<StudentPreferences> = await response.json();
      
      if (this.currentStudent) {
        this.currentStudent.preferences = { ...this.currentStudent.preferences, ...data.data! };
      }
      
      return data.data!;

    } catch (error) {
      console.error('Error updating preferences:', error);
      throw error;
    }
  }

  async changePassword(currentPassword: string, newPassword: string): Promise<void> {
    try {
      const token = this.getAuthToken();
      if (!token) {
        throw new Error('No authentication token');
      }

      const response = await fetch(`${this.apiUrl}/auth/change-password`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          currentPassword,
          newPassword
        })
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.message || 'Failed to change password');
      }

    } catch (error) {
      console.error('Error changing password:', error);
      throw error;
    }
  }

  async requestPasswordReset(email: string): Promise<void> {
    try {
      const response = await fetch(`${this.apiUrl}/auth/reset-password`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email })
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.message || 'Failed to request password reset');
      }

    } catch (error) {
      console.error('Error requesting password reset:', error);
      throw error;
    }
  }

  async resetPassword(token: string, newPassword: string): Promise<void> {
    try {
      const response = await fetch(`${this.apiUrl}/auth/reset-password/confirm`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          token,
          newPassword
        })
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.message || 'Failed to reset password');
      }

    } catch (error) {
      console.error('Error resetting password:', error);
      throw error;
    }
  }

  async deleteAccount(): Promise<void> {
    try {
      const token = this.getAuthToken();
      if (!token) {
        throw new Error('No authentication token');
      }

      const response = await fetch(`${this.apiUrl}/users/account`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.message || 'Failed to delete account');
      }

      // Clear local data
      localStorage.removeItem('vv-student-token');
      this.currentStudent = null;

    } catch (error) {
      console.error('Error deleting account:', error);
      throw error;
    }
  }

  // Utility Methods
  getAuthToken(): string | null {
    return localStorage.getItem('vv-student-token');
  }

  isAuthenticated(): boolean {
    return !!this.getAuthToken() && !!this.currentStudent;
  }

  getCurrentStudentSync(): Student | null {
    return this.currentStudent;
  }

  // Mock Data for Development
  private getMockStudent(): Student {
    return {
      id: 'student_123',
      name: 'Alex Johnson',
      email: 'alex.johnson@example.com',
      avatar: 'https://via.placeholder.com/150',
      gradeLevel: '10th Grade',
      school: 'Lincoln High School',
      preferences: {
        preferredSubjects: ['mathematics', 'physics'],
        learningStyle: 'visual',
        difficultyLevel: 'intermediate',
        sessionDuration: 30,
        notificationsEnabled: true,
        autoplayEnabled: false,
        subtitlesEnabled: true,
        language: 'en'
      },
      subscriptionTier: 'premium',
      createdAt: '2024-01-01T00:00:00Z',
      lastActiveAt: new Date().toISOString()
    };
  }

  // Social Features (Future Implementation)
  async getFriends(): Promise<Student[]> {
    try {
      const token = this.getAuthToken();
      if (!token) {
        throw new Error('No authentication token');
      }

      const response = await fetch(`${this.apiUrl}/users/friends`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (!response.ok) {
        throw new Error('Failed to fetch friends');
      }

      const data: ApiResponse<Student[]> = await response.json();
      return data.data || [];

    } catch (error) {
      console.error('Error fetching friends:', error);
      return [];
    }
  }

  async sendFriendRequest(userId: string): Promise<void> {
    try {
      const token = this.getAuthToken();
      if (!token) {
        throw new Error('No authentication token');
      }

      const response = await fetch(`${this.apiUrl}/users/friends/request`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ userId })
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.message || 'Failed to send friend request');
      }

    } catch (error) {
      console.error('Error sending friend request:', error);
      throw error;
    }
  }

  async acceptFriendRequest(requestId: string): Promise<void> {
    try {
      const token = this.getAuthToken();
      if (!token) {
        throw new Error('No authentication token');
      }

      const response = await fetch(`${this.apiUrl}/users/friends/accept`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ requestId })
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.message || 'Failed to accept friend request');
      }

    } catch (error) {
      console.error('Error accepting friend request:', error);
      throw error;
    }
  }

  // Cleanup
  destroy(): void {
    this.currentStudent = null;
  }
}

export const userService = UserService.getInstance();
