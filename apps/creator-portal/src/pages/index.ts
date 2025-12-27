// Creator Portal - Pages Module

/**
 * VisualVerse Creator Portal - Pages Module
 * 
 * PROPRIETARY MODULE - See /PROPRIETARY_LICENSE.md for licensing terms
 * 
 * This module defines page components and routing for the creator portal.
 */

// Editor Pages
export { default as AnimationEditor } from './Editor/AnimationEditor';
export { default as ProjectSettings } from './Editor/ProjectSettings';
export { default as ExportDialog } from './Editor/ExportDialog';

// Dashboard Pages
export { default as MyProjects } from './Dashboard/MyProjects';
export { default as ProjectCard } from './Dashboard/ProjectCard';
export { default as NewProjectWizard } from './Dashboard/NewProjectWizard';

// Marketplace Pages
export { default as AssetLibrary } from './Marketplace/AssetLibrary';
export { default as TemplateBrowser } from './Marketplace/TemplateBrowser';
export { default as AssetPreview } from './Marketplace/AssetPreview';

// Account Pages
export { default as Profile } from './Account/Profile';
export { default as Billing } from './Account/Billing';
export { default as Settings } from './Account/Settings';

// Routing
export { pageRoutes } from './routes';
export type { RouteConfig } from './routes';
