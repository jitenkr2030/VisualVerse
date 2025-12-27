/**
 * VisualVerse Animation Engine - Core Types
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

// Vector Types
export interface Vector2 {
  x: number;
  y: number;
}

export interface Vector3 {
  x: number;
  y: number;
  z: number;
}

// Color Types
export type Color = string;

export interface RGBA {
  r: number;
  g: number;
  b: number;
  a: number;
}

export interface HSLA {
  h: number;
  s: number;
  l: number;
  a: number;
}

// Transform Types
export interface Transform {
  position: Vector3;
  rotation: Vector3;
  scale: Vector2;
  origin: Vector2;
}

export interface Position {
  x: number;
  y: number;
  z?: number;
}

export interface Rotation {
  x: number;
  y: number;
  z: number;
}

export interface Scale {
  x: number;
  y: number;
}

// Bounds Types
export interface Bounds {
  min: Vector2;
  max: Vector2;
}

export interface Rect {
  x: number;
  y: number;
  width: number;
  height: number;
}

// Animation Types
export interface AnimationCurve {
  keyframes: Keyframe[];
  easing: EasingFunction;
  duration: number;
}

export type EasingFunction = 
  | 'linear'
  | 'easeIn'
  | 'easeOut'
  | 'easeInOut'
  | 'bounce'
  | 'elastic'
  | 'custom';

export interface EasingPreset {
  name: string;
  fn: (t: number) => number;
}

// Render Types
export interface RenderOptions {
  width: number;
  height: number;
  fps: number;
  quality: 'low' | 'medium' | 'high' | 'ultra';
  format: 'mp4' | 'webm' | 'gif' | 'png' | 'webp';
  backgroundColor: Color;
  transparent: boolean;
}

export interface RenderResult {
  success: boolean;
  outputPath: string;
  fileSize: number;
  duration: number;
  error?: string;
}

// Scene Types
export interface SceneConfig {
  name: string;
  width: number;
  height: number;
  fps: number;
  backgroundColor: Color;
  duration?: number;
}

export interface SceneObject {
  id: string;
  type: string;
  name: string;
  visible: boolean;
  locked: boolean;
  transform: Transform;
  children?: SceneObject[];
}

// Export Types
export interface ExportConfig {
  format: 'mp4' | 'webm' | 'gif' | 'png' | 'webp';
  quality: 'draft' | 'standard' | 'high' | 'maximum';
  resolution: '720p' | '1080p' | '2k' | '4k' | 'custom';
  customWidth?: number;
  customHeight?: number;
  fps: number;
  bitrate?: number;
}

// Timeline Types
export interface TimelineTrack {
  id: string;
  name: string;
  type: 'visual' | 'audio' | 'effect';
  visible: boolean;
  locked: boolean;
  keyframes: Keyframe[];
}

export interface TimelineState {
  currentTime: number;
  duration: number;
  isPlaying: boolean;
  isPaused: boolean;
  playbackRate: number;
  zoom: number;
  scroll: number;
}

// Plugin Types
export interface PluginConfig {
  name: string;
  version: string;
  author: string;
  description: string;
  dependencies?: Record<string, string>;
}

export interface PluginContext {
  registerEffect: (effect: Effect) => void;
  registerExporter: (exporter: IExporter) => void;
  registerRenderer: (renderer: IRenderer) => void;
  getEngine: () => AnimationEngine;
}

// Event Types
export type EventType = 
  | 'scene:load'
  | 'scene:unload'
  | 'animation:play'
  | 'animation:pause'
  | 'animation:stop'
  | 'animation:complete'
  | 'render:start'
  | 'render:progress'
  | 'render:complete'
  | 'render:error'
  | 'object:add'
  | 'object:remove'
  | 'object:update'
  | 'timeline:seek'
  | 'timeline:zoom'
  | 'user:action';

export interface EngineEvent {
  type: EventType;
  timestamp: number;
  data?: Record<string, unknown>;
  source?: string;
}
