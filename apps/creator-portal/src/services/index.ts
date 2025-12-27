// Creator Portal - Services Module

/**
 * VisualVerse Creator Portal - Services Module
 * 
 * PROPRIETARY MODULE - See /PROPRIETARY_LICENSE.md for licensing terms
 * 
 * This module provides API services for the creator portal.
 */

// API Client
export { apiClient, createApiClient } from './api/apiClient';
export { API_ENDPOINTS } from './api/endpoints';
export { apiErrorHandler, ApiError } from './api/errorHandler';

// Services
export { projectService } from './projectService';
export { assetService } from './assetService';
export { userService } from './userService';
export { exportService } from './exportService';
export { collaborationService } from './collaborationService';
export { analyticsService } from './analyticsService';

// Types
export type { ApiClientConfig } from './api/apiClient';
export type { ApiResponse } from './api/apiClient';
export type { Project, ProjectCreateData, ProjectUpdateData } from './projectService';
export type { Asset, AssetUploadOptions } from './assetService';
export type { User, UserProfile, AuthCredentials } from './userService';
export type { ExportRequest, ExportOptions, ExportStatus } from './exportService';
