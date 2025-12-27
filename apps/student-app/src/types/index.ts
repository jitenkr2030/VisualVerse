/**
 * VisualVerse Student App - Type Definitions
 * Comprehensive type definitions for the student interface
 */

// Core User Types
export interface Student {
  id: string;
  name: string;
  email: string;
  avatar?: string;
  gradeLevel: string;
  school?: string;
  preferences: StudentPreferences;
  subscriptionTier: 'free' | 'premium' | 'enterprise';
  createdAt: string;
  lastActiveAt: string;
}

export interface StudentPreferences {
  preferredSubjects: string[];
  learningStyle: 'visual' | 'auditory' | 'kinesthetic' | 'mixed';
  difficultyLevel: 'beginner' | 'intermediate' | 'advanced' | 'adaptive';
  sessionDuration: number; // in minutes
  notificationsEnabled: boolean;
  autoplayEnabled: boolean;
  subtitlesEnabled: boolean;
  language: string;
}

// Lesson Types
export interface Lesson {
  id: string;
  title: string;
  description: string;
  subject: Subject;
  creator: Creator;
  content: LessonContent;
  metadata: LessonMetadata;
  status: LessonStatus;
  accessibility: AccessibilityFeatures;
  tags: string[];
  createdAt: string;
  updatedAt: string;
  views: number;
  rating: number;
  reviews: Review[];
}

export interface LessonContent {
  type: 'animation' | 'interactive' | 'video' | 'mixed';
  duration: number; // in seconds
  scenes: Scene[];
  transcript?: string;
  resources: Resource[];
  assessment?: Assessment;
}

export interface Scene {
  id: string;
  title: string;
  description: string;
  content: SceneContent;
  duration: number;
  type: 'intro' | 'explanation' | 'example' | 'exercise' | 'conclusion';
  interactiveElements?: InteractiveElement[];
}

export interface SceneContent {
  script: string;
  visuals: VisualElement[];
  audio?: AudioElement[];
  animations: Animation[];
}

export interface VisualElement {
  id: string;
  type: 'text' | 'image' | 'graph' | 'diagram' | 'formula' | 'chart';
  content: any;
  position: Position;
  style: VisualStyle;
  animation?: AnimationConfig;
}

export interface AudioElement {
  id: string;
  type: 'narration' | 'sound_effect' | 'music';
  url: string;
  duration: number;
  volume: number;
}

export interface Animation {
  id: string;
  type: 'fade' | 'slide' | 'scale' | 'rotate' | 'custom';
  duration: number;
  delay: number;
  easing: string;
  keyframes?: Keyframe[];
}

export interface Keyframe {
  time: number;
  properties: Record<string, any>;
}

// Subject and Category Types
export interface Subject {
  id: string;
  name: string;
  displayName: string;
  description: string;
  icon: string;
  color: string;
  difficulty: DifficultyLevel;
  prerequisites: string[];
  learningObjectives: string[];
  curriculum: CurriculumStandard[];
}

export interface CurriculumStandard {
  id: string;
  name: string;
  region: string;
  gradeLevel: string;
  standards: string[];
}

// Creator Types
export interface Creator {
  id: string;
  name: string;
  avatar?: string;
  bio: string;
  expertise: string[];
  rating: number;
  totalLessons: number;
  totalStudents: number;
  verified: boolean;
}

// Progress and Assessment Types
export interface Progress {
  id: string;
  studentId: string;
  lessonId: string;
  status: ProgressStatus;
  completionPercentage: number;
  timeSpent: number; // in seconds
  lastAccessedAt: string;
  completedAt?: string;
  quizScores?: QuizScore[];
  notes?: StudentNote[];
  bookmarks?: Bookmark[];
}

export interface QuizScore {
  questionId: string;
  correct: boolean;
  timeSpent: number;
  attempts: number;
}

export interface StudentNote {
  id: string;
  timestamp: number; // video timestamp in seconds
  content: string;
  createdAt: string;
  updatedAt: string;
}

export interface Bookmark {
  id: string;
  timestamp: number;
  label: string;
  createdAt: string;
}

// Interactive Elements
export interface InteractiveElement {
  id: string;
  type: 'quiz' | 'drag_drop' | 'multiple_choice' | 'slider' | 'input_field';
  question: string;
  options?: string[];
  correctAnswer?: any;
  feedback: string;
  position: Position;
  timing: InteractionTiming;
}

export interface InteractionTiming {
  startTime: number;
  endTime?: number;
  duration?: number;
}

// Assessment Types
export interface Assessment {
  id: string;
  type: 'quiz' | 'assignment' | 'project';
  title: string;
  description: string;
  questions: Question[];
  timeLimit?: number;
  attempts: number;
  passingScore: number;
  dueDate?: string;
}

export interface Question {
  id: string;
  type: 'multiple_choice' | 'true_false' | 'short_answer' | 'essay' | 'diagram';
  question: string;
  options?: string[];
  correctAnswer: any;
  explanation: string;
  points: number;
  difficulty: DifficultyLevel;
}

// Resource Types
export interface Resource {
  id: string;
  type: 'pdf' | 'link' | 'video' | 'worksheet' | 'reference';
  title: string;
  description: string;
  url: string;
  size?: number;
  downloadAllowed: boolean;
}

// Review Types
export interface Review {
  id: string;
  studentId: string;
  studentName: string;
  rating: number; // 1-5 stars
  comment: string;
  createdAt: string;
  helpful: number;
  verified: boolean;
}

// Accessibility Types
export interface AccessibilityFeatures {
  subtitlesAvailable: boolean;
  audioDescription: boolean;
  highContrast: boolean;
  screenReaderCompatible: boolean;
  keyboardNavigation: boolean;
  signLanguage?: string;
}

// Utility Types
export interface Position {
  x: number;
  y: number;
  z?: number;
}

export interface VisualStyle {
  fontSize?: number;
  fontFamily?: string;
  color?: string;
  backgroundColor?: string;
  border?: string;
  borderRadius?: number;
  padding?: number;
  margin?: number;
  opacity?: number;
  rotation?: number;
  scale?: number;
}

export interface AnimationConfig {
  type: string;
  duration: number;
  delay: number;
  easing: string;
  loop?: boolean;
  direction?: 'normal' | 'reverse' | 'alternate';
}

// Status Enums
export type LessonStatus = 'draft' | 'processing' | 'completed' | 'error' | 'archived';
export type ProgressStatus = 'not_started' | 'in_progress' | 'completed' | 'paused';
export type DifficultyLevel = 'beginner' | 'intermediate' | 'advanced';

// API Response Types
export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
  message?: string;
  pagination?: {
    page: number;
    limit: number;
    total: number;
    totalPages: number;
  };
}

export interface PaginatedResponse<T> extends ApiResponse<T[]> {
  pagination: {
    page: number;
    limit: number;
    total: number;
    totalPages: number;
  };
}

// Search and Filter Types
export interface SearchFilters {
  query?: string;
  subjects?: string[];
  difficulty?: DifficultyLevel[];
  duration?: {
    min?: number;
    max?: number;
  };
  rating?: number;
  creator?: string;
  tags?: string[];
  sortBy?: 'relevance' | 'rating' | 'views' | 'newest' | 'duration';
  sortOrder?: 'asc' | 'desc';
}

export interface SearchResult {
  lessons: Lesson[];
  subjects: Subject[];
  creators: Creator[];
  totalResults: number;
  facets: SearchFacets;
}

export interface SearchFacets {
  subjects: FacetItem[];
  difficulty: FacetItem[];
  duration: FacetItem[];
  creators: FacetItem[];
  tags: FacetItem[];
}

export interface FacetItem {
  value: string;
  count: number;
  selected: boolean;
}

// Configuration Types
export interface AppConfig {
  apiUrl: string;
  wsUrl: string;
  maxVideoQuality: string;
  defaultLanguage: string;
  supportedLanguages: string[];
  features: {
    offlineMode: boolean;
    downloadLessons: boolean;
    socialSharing: boolean;
    collaborativeFeatures: boolean;
  };
  limits: {
    maxConcurrentLessons: number;
    maxDownloadSize: number;
    maxSessionDuration: number;
  };
}

// Error Types
export interface AppError {
  code: string;
  message: string;
  details?: any;
  timestamp: string;
  context?: string;
}

// Notification Types
export interface Notification {
  id: string;
  type: 'info' | 'success' | 'warning' | 'error';
  title: string;
  message: string;
  timestamp: string;
  read: boolean;
  actions?: NotificationAction[];
  relatedEntity?: {
    type: 'lesson' | 'progress' | 'achievement';
    id: string;
  };
}

export interface NotificationAction {
  label: string;
  action: string;
  style: 'primary' | 'secondary' | 'danger';
}

// Analytics Types
export interface AnalyticsEvent {
  event: string;
  properties: Record<string, any>;
  userId?: string;
  timestamp: string;
  sessionId: string;
}

export interface LearningAnalytics {
  totalTimeSpent: number;
  lessonsCompleted: number;
  subjectsExplored: number;
  averageSessionDuration: number;
  learningStreak: number;
  preferredSubjects: string[];
  skillLevel: DifficultyLevel;
  recentActivity: ActivityItem[];
}

export interface ActivityItem {
  type: 'lesson_started' | 'lesson_completed' | 'quiz_completed' | 'achievement_earned';
  lessonId?: string;
  description: string;
  timestamp: string;
  metadata?: Record<string, any>;
}
