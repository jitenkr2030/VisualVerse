// Admin Console - Dashboards Module

/**
 * VisualVerse Admin Console - Dashboards Module
 * 
 * PROPRIETARY MODULE - See /PROPRIETARY_LICENSE.md for licensing terms
 * 
 * This module provides dashboard components and layout configurations
 * for the VisualVerse administrative interface.
 */

// Re-export all dashboard components
export { default as OverviewDashboard } from './components/OverviewDashboard';
export { default as UserManagementDashboard } from './components/UserManagementDashboard';
export { default as ContentDashboard } from './components/ContentDashboard';
export { default as AnalyticsDashboard } from './components/AnalyticsDashboard';
export { default as SystemDashboard } from './components/SystemDashboard';

// Re-export layout components
export { default as AdminLayout } from './layout/AdminLayout';
export { default as Sidebar } from './layout/Sidebar';
export { default as Header } from './layout/Header';

// Re-export hooks and utilities
export { useDashboard } from './hooks/useDashboard';
export { useSidebar } from './hooks/useSidebar';
export { dashboardRoutes } from './config/routes';
export { default as dashboardTheme } from './config/theme';
