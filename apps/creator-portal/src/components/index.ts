// Creator Portal - Components Module

/**
 * VisualVerse Creator Portal - Components Module
 * 
 * PROPRIETARY MODULE - See /PROPRIETARY_LICENSE.md for licensing terms
 * 
 * This module provides reusable UI components for the creator portal,
 * including canvas controls, timeline editors, and common atomic elements.
 */

// Canvas Components
export { default as AnimationCanvas } from './Canvas/AnimationCanvas';
export { default as CanvasToolbar } from './Canvas/CanvasToolbar';
export { default as LayerPanel } from './Canvas/LayerPanel';
export { default as PropertyPanel } from './Canvas/PropertyPanel';

// Timeline Components
export { default as Timeline } from './Timeline/Timeline';
export { default as Track } from './Timeline/Track';
export { default as Keyframe } from './Timeline/Keyframe';
export { default as Playhead } from './Timeline/Playhead';
export { default as TimelineZoom } from './Timeline/TimelineZoom';

// Toolbar Components
export { default as ToolSelector } from './Toolbar/ToolSelector';
export { default as ShapeTools } from './Toolbar/ShapeTools';
export { default as TextTools } from './Toolbar/TextTools';
export { default as TransformTools } from './Toolbar/TransformTools';

// Common Components
export { default as Button } from './Common/Button';
export { default as Input } from './Common/Input';
export { default as Modal } from './Common/Modal';
export { default as Dropdown } from './Common/Dropdown';
export { default as Tooltip } from './Common/Tooltip';

// Component Types
export type { CanvasProps } from './Canvas/AnimationCanvas';
export type { TimelineProps } from './Timeline/Timeline';
export type { ButtonVariant, ButtonSize } from './Common/Button';
