/**
 * VisualVerse Animation Engine - Runtime API
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

/**
 * Event types for the runtime API.
 */
export type RuntimeEventType =
  | 'ready'
  | 'play'
  | 'pause'
  | 'stop'
  | 'complete'
  | 'frame'
  | 'timeupdate'
  | 'error'
  | 'object:hover'
  | 'object:click'
  | 'interaction';

/**
 * Event payload for runtime events.
 */
export interface RuntimeEvent {
  type: RuntimeEventType;
  timestamp: number;
  data?: Record<string, unknown>;
  target?: string;
}

/**
 * Configuration for the runtime player.
 */
export interface RuntimeConfig {
  containerId: string;
  width: number;
  height: number;
  backgroundColor: string;
  fps: number;
  autoPlay: boolean;
  loop: boolean;
  muted: boolean;
  interactive: boolean;
  showControls: boolean;
  showProgress: boolean;
  onEvent?: (event: RuntimeEvent) => void;
}

/**
 * Default runtime configuration.
 */
export const DEFAULT_RUNTIME_CONFIG: RuntimeConfig = {
  containerId: 'visualverse-container',
  width: 1280,
  height: 720,
  backgroundColor: '#1a1a2e',
  fps: 30,
  autoPlay: false,
  loop: false,
  muted: false,
  interactive: true,
  showControls: true,
  showProgress: true
};

/**
 * Object transform update payload.
 */
export interface TransformUpdate {
  objectId: string;
  position?: [number, number, number];
  rotation?: [number, number, number];
  scale?: [number, number, number];
}

/**
 * Style update payload.
 */
export interface StyleUpdate {
  objectId: string;
  fillColor?: string;
  strokeColor?: string;
  strokeWidth?: number;
  opacity?: number;
}

/**
 * Animation control options.
 */
export interface AnimationOptions {
  duration?: number;
  easing?: string;
  loop?: boolean;
  delay?: number;
}

/**
 * Runtime API for controlling embedded animations.
 * 
 * This class provides a programmatic API for controlling animations
 * embedded in web applications.
 */
export class VisualEngineRuntime {
  private config: RuntimeConfig;
  private container: HTMLElement | null;
  private canvas: HTMLCanvasElement | null;
  private eventListeners: Map<RuntimeEventType, Set<(event: RuntimeEvent) => void>>;
  private isReady: boolean = false;
  private isPlaying: boolean = false;
  private currentTime: number = 0;
  private duration: number = 10;

  /**
   * Create a new VisualEngineRuntime instance.
   * 
   * @param config - Configuration for the runtime
   */
  constructor(config?: Partial<RuntimeConfig>) {
    this.config = { ...DEFAULT_RUNTIME_CONFIG, ...config };
    this.container = null;
    this.canvas = null;
    this.eventListeners = new Map();
    this.setupEventListeners();
  }

  /**
   * Initialize the runtime with a container element.
   */
  initialize(container: HTMLElement | string): void {
    if (typeof container === 'string') {
      this.container = document.getElementById(container);
    } else {
      this.container = container;
    }

    if (!this.container) {
      throw new Error(`Container element not found`);
    }

    // Create canvas
    this.canvas = document.createElement('canvas');
    this.canvas.width = this.config.width;
    this.canvas.height = this.config.height;
    this.canvas.style.width = '100%';
    this.canvas.style.height = 'auto';
    this.canvas.style.maxWidth = '100%';
    
    // Apply background color
    this.canvas.style.backgroundColor = this.config.backgroundColor;
    
    this.container.appendChild(this.canvas);

    // Create controls if enabled
    if (this.config.showControls) {
      this.createControls();
    }

    this.isReady = true;
    this.emit({
      type: 'ready',
      timestamp: Date.now()
    });
  }

  /**
   * Load scene data into the runtime.
   */
  loadScene(sceneData: Record<string, unknown>): void {
    if (!this.isReady) {
      throw new Error('Runtime not initialized');
    }

    // In a full implementation, this would parse and prepare the scene data
    this.duration = (sceneData as { duration?: number }).duration || 10;

    this.emit({
      type: 'ready',
      timestamp: Date.now(),
      data: { sceneData }
    });
  }

  /**
   * Create playback controls.
   */
  private createControls(): void {
    const controls = document.createElement('div');
    controls.className = 'visualverse-controls';
    controls.style.cssText = `
      position: absolute;
      bottom: 10px;
      left: 50%;
      transform: translateX(-50%);
      display: flex;
      gap: 8px;
      padding: 8px 12px;
      background: rgba(0, 0, 0, 0.6);
      border-radius: 6px;
      backdrop-filter: blur(8px);
    `;

    // Play/Pause button
    const playPauseBtn = document.createElement('button');
    playPauseBtn.className = 'visualverse-btn';
    playPauseBtn.innerHTML = '▶';
    playPauseBtn.style.cssText = `
      width: 32px;
      height: 32px;
      border: none;
      border-radius: 50%;
      background: rgba(255, 255, 255, 0.1);
      color: white;
      cursor: pointer;
      font-size: 12px;
    `;
    playPauseBtn.onclick = () => this.togglePlay();

    // Restart button
    const restartBtn = document.createElement('button');
    restartBtn.className = 'visualverse-btn';
    restartBtn.innerHTML = '↺';
    restartBtn.style.cssText = `
      width: 32px;
      height: 32px;
      border: none;
      border-radius: 50%;
      background: rgba(255, 255, 255, 0.1);
      color: white;
      cursor: pointer;
      font-size: 14px;
    `;
    restartBtn.onclick = () => this.restart();

    controls.appendChild(playPauseBtn);
    controls.appendChild(restartBtn);

    if (this.container) {
      this.container.style.position = 'relative';
      this.container.appendChild(controls);
    }
  }

  /**
   * Start or resume playback.
   */
  play(): void {
    this.isPlaying = true;
    this.emit({
      type: 'play',
      timestamp: Date.now()
    });
  }

  /**
   * Pause playback.
   */
  pause(): void {
    this.isPlaying = false;
    this.emit({
      type: 'pause',
      timestamp: Date.now()
    });
  }

  /**
   * Toggle play/pause state.
   */
  togglePlay(): void {
    if (this.isPlaying) {
      this.pause();
    } else {
      this.play();
    }
  }

  /**
   * Stop playback and reset to beginning.
   */
  stop(): void {
    this.isPlaying = false;
    this.currentTime = 0;
    this.emit({
      type: 'stop',
      timestamp: Date.now()
    });
  }

  /**
   * Restart playback from the beginning.
   */
  restart(): void {
    this.currentTime = 0;
    this.emit({
      type: 'stop',
      timestamp: Date.now()
    });
    if (this.isPlaying) {
      this.play();
    }
  }

  /**
   * Seek to a specific time.
   * 
   * @param time - Time in seconds
   */
  seek(time: number): void {
    this.currentTime = Math.max(0, Math.min(time, this.duration));
    this.emit({
      type: 'timeupdate',
      timestamp: Date.now(),
      data: { time: this.currentTime }
    });
  }

  /**
   * Jump forward by a specified duration.
   * 
   * @param seconds - Seconds to jump forward
   */
  forward(seconds: number = 5): void {
    this.seek(this.currentTime + seconds);
  }

  /**
   * Jump backward by a specified duration.
   * 
   * @param seconds - Seconds to jump backward
   */
  rewind(seconds: number = 5): void {
    this.seek(this.currentTime - seconds);
  }

  /**
   * Set the playback speed.
   * 
   * @param rate - Playback rate (1 = normal, 0.5 = half speed, 2 = double speed)
   */
  setPlaybackRate(rate: number): void {
    this.emit({
      type: 'interaction',
      timestamp: Date.now(),
      data: { playbackRate: rate }
    });
  }

  /**
   * Update an object's transform properties.
   * 
   * @param update - Transform update payload
   */
  updateTransform(update: TransformUpdate): void {
    this.emit({
      type: 'interaction',
      timestamp: Date.now(),
      data: { type: 'transform', ...update }
    });
  }

  /**
   * Update an object's style properties.
   * 
   * @param update - Style update payload
   */
  updateStyle(update: StyleUpdate): void {
    this.emit({
      type: 'interaction',
      timestamp: Date.now(),
      data: { type: 'style', ...update }
    });
  }

  /**
   * Trigger an animation on a specific object.
   * 
   * @param objectId - ID of the object to animate
   * @param property - Property to animate
   * @param targetValue - Target value for the animation
   * @param options - Animation options
   */
  animate(
    objectId: string,
    property: string,
    targetValue: number | string | [number, number, number],
    options?: AnimationOptions
  ): void {
    this.emit({
      type: 'interaction',
      timestamp: Date.now(),
      data: {
        type: 'animation',
        objectId,
        property,
        targetValue,
        options
      }
    });
  }

  /**
   * Show or hide an object.
   * 
   * @param objectId - ID of the object
   * @param visible - Whether the object should be visible
   */
  setVisibility(objectId: string, visible: boolean): void {
    this.emit({
      type: 'interaction',
      timestamp: Date.now(),
      data: { type: 'visibility', objectId, visible }
    });
  }

  /**
   * Get the current playback state.
   */
  getState(): {
    isReady: boolean;
    isPlaying: boolean;
    currentTime: number;
    duration: number;
    progress: number;
  } {
    return {
      isReady: this.isReady,
      isPlaying: this.isPlaying,
      currentTime: this.currentTime,
      duration: this.duration,
      progress: this.currentTime / this.duration
    };
  }

  /**
   * Add an event listener.
   * 
   * @param type - Event type to listen for
   * @param callback - Callback function
   */
  on(type: RuntimeEventType, callback: (event: RuntimeEvent) => void): void {
    if (!this.eventListeners.has(type)) {
      this.eventListeners.set(type, new Set());
    }
    this.eventListeners.get(type)!.add(callback);
  }

  /**
   * Remove an event listener.
   * 
   * @param type - Event type
   * @param callback - Callback function to remove
   */
  off(type: RuntimeEventType, callback: (event: RuntimeEvent) => void): void {
    this.eventListeners.get(type)?.delete(callback);
  }

  /**
   * Setup internal event handling.
   */
  private setupEventListeners(): void {
    // Initialize empty listener sets for common events
    const eventTypes: RuntimeEventType[] = [
      'ready', 'play', 'pause', 'stop', 'complete',
      'frame', 'timeupdate', 'error', 'object:hover',
      'object:click', 'interaction'
    ];

    for (const type of eventTypes) {
      this.eventListeners.set(type, new Set());
    }
  }

  /**
   * Emit an event to all listeners.
   */
  private emit(event: RuntimeEvent): void {
    // Call configured callback if provided
    if (this.config.onEvent) {
      this.config.onEvent(event);
    }

    // Call all registered listeners
    this.eventListeners.get(event.type)?.forEach(callback => {
      try {
        callback(event);
      } catch (error) {
        console.error(`Error in event listener for ${event.type}:`, error);
      }
    });
  }

  /**
   * Dispose of the runtime and clean up resources.
   */
  dispose(): void {
    this.pause();
    this.isReady = false;
    
    if (this.canvas && this.container) {
      this.container.removeChild(this.canvas);
    }
    
    this.canvas = null;
    this.container = null;
    this.eventListeners.clear();
  }
}

/**
 * Utility function to create a runtime instance from an HTML element.
 */
export function createRuntime(
  container: HTMLElement | string,
  config?: Partial<RuntimeConfig>
): VisualEngineRuntime {
  const runtime = new VisualEngineRuntime(config);
  runtime.initialize(container);
  return runtime;
}

/**
 * Utility function to load a scene from a URL.
 */
export async function loadSceneFromURL(
  url: string
): Promise<Record<string, unknown>> {
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`Failed to load scene: ${response.statusText}`);
  }
  return response.json();
}
