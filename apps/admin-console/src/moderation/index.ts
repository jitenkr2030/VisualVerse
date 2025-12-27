// Admin Console - Moderation Module

/**
 * VisualVerse Admin Console - Moderation Module
 * 
 * PROPRIETARY MODULE - See /PROPRIETARY_LICENSE.md for licensing terms
 * 
 * This module provides content moderation tools for maintaining
 * platform quality and community standards.
 */

// Re-export all moderation components
export { default as ReportedContentQueue } from './components/ReportedContentQueue';
export { default as UserBanTools } from './components/UserBanTools';
export { default as ContentReview } from './components/ContentReview';
export { default as ModerationHistory } from './components/ModerationHistory';
export { default as AutoModerationSettings } from './components/AutoModerationSettings';

// Re-export hooks and utilities
export { useModeration } from './hooks/useModeration';
export { useContentQueue } from './hooks/useContentQueue';
export { useUserActions } from './hooks/useUserActions';
export { ModerationAction } from './types/ModerationAction';
export { ModerationStatus } from './types/ModerationStatus';
export { autoModerate } from './utils/autoModeration';
export { calculateSeverity } from './utils/severityLevels';

// Re-export services
export { moderationService } from './services/moderationService';
