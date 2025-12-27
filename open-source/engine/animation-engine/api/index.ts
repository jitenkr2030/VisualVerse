/**
 * VisualVerse Animation Engine - Public API
 * 
 * Copyright 2024 VisualVerse Contributors
 * 
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 * 
 *     http://www.apache.org/licenses/LICENSE-2.0
 * 
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

// Core Classes
export { AnimationEngine } from './AnimationEngine';
export { Scene } from './Scene';
export { Timeline } from './Timeline';
export { Camera } from './Camera';

// Visual Objects
export { VisualObject } from './VisualObject';
export { Shape } from './Shape';
export { Text } from './Text';
export { Image } from './Group';
export { Group } from './Group';

// Animation Types
export { Keyframe } from './Keyframe';
export { Animation } from './Animation';
export { EasingFunction, EasingFunctions } from './Easing';

// Renderer Interface
export type { IRenderer } from './IRenderer';
export { CanvasRenderer } from './CanvasRenderer';
export { WebGLRenderer } from './WebGLRenderer';

// Export Interface
export type { IExporter } from './IExporter';
export { VideoExporter } from './VideoExporter';
export { ImageExporter } from './ImageExporter';
export { GIFExporter } from './GIFExporter';

// Event System
export type { IEventBus, EventHandler } from './IEventBus';
export { EventBus } from './EventBus';

// Plugin System
export type { IPlugin, IPluginContext } from './IPluginSystem';
export { PluginRegistry } from './PluginSystem';

// Utility Functions
export { interpolate } from './interpolation';
export { generateId } from './utils';
export { validateScene } from './validation';

// Type Definitions
export type { 
  Vector2, 
  Vector3, 
  Color, 
  RGBA,
  HSLA,
  Transform,
  Position,
  Rotation,
  Scale,
  Bounds,
  Rect,
  AnimationCurve,
  EasingFunction,
  EasingPreset,
  RenderOptions,
  RenderResult,
  SceneConfig,
  SceneObject,
  ExportConfig,
  TimelineTrack,
  TimelineState,
  PluginConfig,
  PluginContext,
  EventType,
  EngineEvent
} from './types';

// Re-export common types
export * from './types';

// ============================================
// Version Control Module
// ============================================
export { 
  VersionControlTracker, 
  VisualDiffer, 
  GitBridge,
  ISerializable,
  SerializationUtils
} from '../version-control';

export type {
  VersionSnapshot,
  SceneChange,
  ChangeType,
  CommitResult,
  CheckoutResult,
  CompareResult,
  WorkingDirectoryStatus,
  VisualGitStatus,
  GitVisualDiffResult,
  GitCommitResult,
  VisualBranchInfo,
  DiffResult,
  DiffAnalysis,
  DiffRegion,
  VisualDiffConfig
} from '../version-control';

// ============================================
// Runtime Module
// ============================================
export { 
  VisualEngineRuntime, 
  createRuntime, 
  loadSceneFromURL 
} from '../runtime';

export type {
  RuntimeEventType,
  RuntimeEvent,
  RuntimeConfig,
  TransformUpdate,
  StyleUpdate,
  AnimationOptions
} from '../runtime';

// ============================================
// Optimization Module
// ============================================
export { 
  RenderCacheManager,
  RenderPool,
  createRenderTask,
  TaskPriority,
  RenderTaskStatus
} from '../optimization';

export type {
  CacheEntry,
  CacheMetadata,
  CacheConfig,
  CacheLookupResult,
  CacheStoreResult,
  CacheStats,
  RenderPoolConfig,
  RenderTask,
  RenderParameters,
  RenderResult as RenderPoolResult,
  RenderPoolStats
} from '../optimization';

// ============================================
// Interactive Export Module
// ============================================
export { WebGLExporter } from '../exporters/interactive';

export type {
  WebGLExportConfig,
  WebGLExportResult,
  RuntimeSceneData,
  RuntimeObject,
  RuntimeStyle,
  RuntimeAnimation,
  RuntimeKeyframe,
  RuntimeTimeline,
  RuntimeTrack
} from '../exporters/interactive';

// ============================================
// Vector Exporters Module
// ============================================
export { 
  SVGExporter, 
  LottieExporter 
} from '../exporters/vector';

export type {
  SVGExportConfig,
  SVGExportResult,
  SVGElementType,
  SVGStyle,
  SVGTransform,
  LottieExportConfig,
  LottieExportResult,
  LottieAnimation,
  LottieAsset,
  LottieLayer,
  LottieTransform,
  LottieShape,
  LottieMarker
} from '../exporters/vector';

// ============================================
// WebP Exporter
// ============================================
export { WebPExporter } from '../exporters/webp-exporter';

export type {
  WebPExportConfig,
  WebPExportResult,
  WebPFrame
} from '../exporters/webp-exporter';
