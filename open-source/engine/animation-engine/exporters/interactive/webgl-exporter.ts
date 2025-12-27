/**
 * VisualVerse Animation Engine - WebGL Exporter
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

import { ISerializable } from '../../core/serializable';

/**
 * Configuration for WebGL export.
 */
export interface WebGLExportConfig {
  width: number;
  height: number;
  fps: number;
  backgroundColor: string;
  antialiasing: boolean;
  preserveDrawingBuffer: boolean;
  includeRuntime: boolean;
  minify: boolean;
  embedAssets: boolean;
  title: string;
  description: string;
  author: string;
}

/**
 * Default WebGL export configuration.
 */
export const DEFAULT_WEBGL_EXPORT_CONFIG: WebGLExportConfig = {
  width: 1280,
  height: 720,
  fps: 30,
  backgroundColor: '#1a1a2e',
  antialiasing: true,
  preserveDrawingBuffer: true,
  includeRuntime: true,
  minify: false,
  embedAssets: true,
  title: 'VisualVerse Animation',
  description: '',
  author: ''
};

/**
 * Result of a WebGL export operation.
 */
export interface WebGLExportResult {
  success: boolean;
  outputPath?: string;
  htmlContent?: string;
  fileSize: number;
  sceneDataSize: number;
  assetsSize: number;
  error?: string;
}

/**
 * Scene data structure for runtime.
 */
export interface RuntimeSceneData {
  version: string;
  title: string;
  description: string;
  width: number;
  height: number;
  fps: number;
  backgroundColor: string;
  duration: number;
  objects: RuntimeObject[];
  animations: RuntimeAnimation[];
  timeline: RuntimeTimeline;
}

/**
 * Runtime object representation.
 */
export interface RuntimeObject {
  id: string;
  type: 'circle' | 'rectangle' | 'text' | 'path' | 'image' | 'group';
  name: string;
  visible: boolean;
  transform: {
    position: [number, number, number];
    rotation: [number, number, number];
    scale: [number, number, number];
  };
  style: RuntimeStyle;
  children?: string[];
  data?: Record<string, unknown>;
}

/**
 * Runtime style properties.
 */
export interface RuntimeStyle {
  fillColor?: string;
  strokeColor?: string;
  strokeWidth?: number;
  opacity?: number;
  fontSize?: number;
  fontFamily?: string;
  textAlign?: 'left' | 'center' | 'right';
  lineHeight?: number;
}

/**
 * Runtime animation data.
 */
export interface RuntimeAnimation {
  id: string;
  objectId: string;
  property: string;
  keyframes: RuntimeKeyframe[];
  easing: string;
  duration: number;
  loop: boolean;
}

/**
 * Runtime keyframe.
 */
export interface RuntimeKeyframe {
  time: number;
  value: number | string | [number, number, number];
  easing?: string;
}

/**
 * Runtime timeline data.
 */
export interface RuntimeTimeline {
  duration: number;
  tracks: RuntimeTrack[];
}

/**
 * Runtime track data.
 */
export interface RuntimeTrack {
  id: string;
  name: string;
  type: 'visual' | 'audio' | 'effect';
  objectId?: string;
  keyframes: RuntimeKeyframe[];
}

/**
 * WebGL Exporter for Interactive HTML5 Animations.
 * 
 * This class exports scenes to self-contained HTML files with embedded
 * WebGL rendering capabilities.
 */
export class WebGLExporter {
  private config: WebGLExportConfig;

  /**
   * Create a new WebGLExporter.
   * 
   * @param config - Optional configuration for the exporter
   */
  constructor(config?: Partial<WebGLExportConfig>) {
    this.config = { ...DEFAULT_WEBGL_EXPORT_CONFIG, ...config };
  }

  /**
   * Export a scene to an interactive HTML5/WebGL format.
   * 
   * @param scene - The scene to export (must implement ISerializable)
   * @param outputPath - Path for the output HTML file
   * @returns Result of the export operation
   */
  async export(scene: ISerializable, outputPath: string): Promise<WebGLExportResult> {
    try {
      // Serialize scene data for runtime
      const sceneData = await this.serializeScene(scene);
      
      // Generate HTML content
      const htmlContent = this.generateHTML(sceneData);
      
      // Calculate sizes
      const sceneDataSize = new Blob([JSON.stringify(sceneData)]).size;
      const htmlSize = new Blob([htmlContent]).size;

      return {
        success: true,
        outputPath,
        htmlContent,
        fileSize: htmlSize,
        sceneDataSize,
        assetsSize: 0 // No external assets when embedded
      };
    } catch (error) {
      return {
        success: false,
        fileSize: 0,
        sceneDataSize: 0,
        assetsSize: 0,
        error: error instanceof Error ? error.message : 'Unknown export error'
      };
    }
  }

  /**
   * Serialize a scene to runtime data format.
   */
  private async serializeScene(scene: ISerializable): Promise<RuntimeSceneData> {
    const state = JSON.parse(scene.serialize());
    
    // Transform scene state to runtime format
    return {
      version: '1.0.0',
      title: this.config.title,
      description: this.config.description,
      width: this.config.width,
      height: this.config.height,
      fps: this.config.fps,
      backgroundColor: this.config.backgroundColor,
      duration: state.duration || 10,
      objects: this.extractObjects(state),
      animations: this.extractAnimations(state),
      timeline: this.extractTimeline(state)
    };
  }

  /**
   * Extract runtime objects from scene state.
   */
  private extractObjects(state: Record<string, unknown>): RuntimeObject[] {
    const objects: RuntimeObject[] = [];
    const sceneObjects = state.objects || state.mobjects || [];

    for (const obj of Array.isArray(sceneObjects) ? sceneObjects : []) {
      objects.push({
        id: obj.id || `obj_${objects.length}`,
        type: this.mapObjectType(obj),
        name: obj.name || `Object ${objects.length}`,
        visible: obj.visible !== false,
        transform: {
          position: obj.position || [0, 0, 0],
          rotation: obj.rotation || [0, 0, 0],
          scale: obj.scale || [1, 1, 1]
        },
        style: {
          fillColor: obj.fill_color || obj.color,
          strokeColor: obj.stroke_color,
          strokeWidth: obj.stroke_width,
          opacity: obj.opacity,
          fontSize: obj.font_size,
          fontFamily: obj.font_family
        }
      });
    }

    return objects;
  }

  /**
   * Map scene object type to runtime type.
   */
  private mapObjectType(obj: Record<string, unknown>): RuntimeObject['type'] {
    const className = obj.class || obj.type || '';
    
    if (className.includes('Circle')) return 'circle';
    if (className.includes('Rectangle') || className.includes('Square')) return 'rectangle';
    if (className.includes('Text') || className.includes('Tex')) return 'text';
    if (className.includes('Path') || className.includes('Line')) return 'path';
    if (className.includes('Image') || className.includes('ImageMobject')) return 'image';
    if (className.includes('Group') || className.includes('VGroup')) return 'group';
    
    return 'rectangle'; // Default
  }

  /**
   * Extract animations from scene state.
   */
  private extractAnimations(state: Record<string, unknown>): RuntimeAnimation[] {
    const animations: RuntimeAnimation[] = [];
    const sceneAnimations = state.animations || state.animator || [];

    let animIndex = 0;
    for (const anim of Array.isArray(sceneAnimations) ? sceneAnimations : []) {
      animations.push({
        id: `anim_${animIndex++}`,
        objectId: anim.mobject_id || anim.object_id || '',
        property: anim.property || 'position',
        keyframes: this.extractKeyframes(anim.keyframes || []),
        easing: anim.easing || 'linear',
        duration: anim.duration || 1,
        loop: anim.loop || false
      });
    }

    return animations;
  }

  /**
   * Extract keyframes from animation data.
   */
  private extractKeyframes(keyframes: Array<Record<string, unknown>>): RuntimeKeyframe[] {
    return keyframes.map((kf, index) => ({
      time: kf.time || kf.rate || (index / keyframes.length),
      value: kf.value || kf.end_value || 0,
      easing: kf.easing
    }));
  }

  /**
   * Extract timeline data from scene state.
   */
  private extractTimeline(state: Record<string, unknown>): RuntimeTimeline {
    return {
      duration: state.duration || 10,
      tracks: (state.tracks || []).map((track: Record<string, unknown>, index: number) => ({
        id: `track_${index}`,
        name: track.name || `Track ${index + 1}`,
        type: track.type || 'visual',
        objectId: track.object_id,
        keyframes: this.extractKeyframes((track.keyframes || []) as Array<Record<string, unknown>>)
      }))
    };
  }

  /**
   * Generate the complete HTML content for the exported animation.
   */
  private generateHTML(sceneData: RuntimeSceneData): string {
    const sceneDataJSON = JSON.stringify(sceneData);
    const runtimeScript = this.generateRuntimeScript();
    const shaderCode = this.generateShaders();
    
    return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${sceneData.title}</title>
  <style>
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }
    
    body {
      background-color: #0a0a0f;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      min-height: 100vh;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      color: #ffffff;
    }
    
    #container {
      position: relative;
      width: ${sceneData.width}px;
      height: ${sceneData.height}px;
    }
    
    #canvas {
      width: 100%;
      height: 100%;
      display: block;
    }
    
    #controls {
      position: absolute;
      bottom: 20px;
      left: 50%;
      transform: translateX(-50%);
      display: flex;
      gap: 12px;
      padding: 12px 20px;
      background: rgba(0, 0, 0, 0.7);
      border-radius: 8px;
      backdrop-filter: blur(10px);
    }
    
    .control-btn {
      width: 40px;
      height: 40px;
      border: none;
      border-radius: 50%;
      background: rgba(255, 255, 255, 0.1);
      color: white;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: background 0.2s;
    }
    
    .control-btn:hover {
      background: rgba(255, 255, 255, 0.2);
    }
    
    #progress-container {
      position: absolute;
      bottom: 0;
      left: 0;
      right: 0;
      height: 4px;
      background: rgba(255, 255, 255, 0.1);
    }
    
    #progress-bar {
      height: 100%;
      background: linear-gradient(90deg, #6366f1, #8b5cf6);
      width: 0%;
      transition: width 0.1s linear;
    }
    
    #info {
      position: absolute;
      top: 10px;
      left: 10px;
      font-size: 12px;
      opacity: 0.7;
    }
  </style>
</head>
<body>
  <div id="container">
    <canvas id="canvas" width="${sceneData.width}" height="${sceneData.height}"></canvas>
    <div id="info">${sceneData.title} • ${sceneData.fps} FPS</div>
    <div id="progress-container">
      <div id="progress-bar"></div>
    </div>
    <div id="controls">
      <button class="control-btn" id="play-btn" aria-label="Play">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
          <path d="M8 5v14l11-7z"/>
        </svg>
      </button>
      <button class="control-btn" id="pause-btn" aria-label="Pause" style="display:none;">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
          <path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z"/>
        </svg>
      </button>
      <button class="control-btn" id="restart-btn" aria-label="Restart">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
          <path d="M12 5V1L7 6l5 5V7c3.31 0 6 2.69 6 6s-2.69 6-6 6-6-2.69-6-6H4c0 4.42 3.58 8 8 8s8-3.58 8-8-3.58-8-8-8z"/>
        </svg>
      </button>
    </div>
  </div>

  <script>
    // Scene data embedded for offline use
    const SCENE_DATA = ${sceneDataJSON};
    
    // Runtime script
    ${runtimeScript}
    
    // Shader code
    ${shaderCode}
  </script>
</body>
</html>`;
  }

  /**
   * Generate the JavaScript runtime script.
   */
  private generateRuntimeScript(): string {
    return `
      class VisualVerseRuntime {
        constructor(canvas, sceneData) {
          this.canvas = canvas;
          this.gl = canvas.getContext('webgl', {
            antialiasing: ${this.config.antialiasing},
            preserveDrawingBuffer: ${this.config.preserveDrawingBuffer}
          });
          
          if (!this.gl) {
            throw new Error('WebGL not supported');
          }
          
          this.sceneData = sceneData;
          this.objects = new Map();
          this.animations = [];
          this.currentTime = 0;
          this.isPlaying = false;
          this.lastFrameTime = 0;
          
          this.init();
        }
        
        init() {
          const gl = this.gl;
          
          // Set viewport
          gl.viewport(0, 0, this.canvas.width, this.canvas.height);
          
          // Set clear color
          const bgColor = this.parseColor(this.sceneData.backgroundColor);
          gl.clearColor(bgColor.r, bgColor.g, bgColor.b, 1.0);
          
          // Create shader program
          this.program = this.createProgram();
          gl.useProgram(this.program);
          
          // Initialize objects
          this.initializeObjects();
          
          // Initialize animations
          this.initializeAnimations();
          
          // Setup event listeners
          this.setupControls();
        }
        
        parseColor(colorStr) {
          const hex = colorStr.replace('#', '');
          return {
            r: parseInt(hex.substr(0, 2), 16) / 255,
            g: parseInt(hex.substr(2, 2), 16) / 255,
            b: parseInt(hex.substr(4, 2), 16) / 255
          };
        }
        
        createShader(type, source) {
          const gl = this.gl;
          const shader = gl.createShader(type);
          gl.shaderSource(shader, source);
          gl.compileShader(shader);
          
          if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
            console.error('Shader compile error:', gl.getShaderInfoLog(shader));
            gl.deleteShader(shader);
            return null;
          }
          
          return shader;
        }
        
        createProgram() {
          const gl = this.gl;
          
          const vertexShader = this.createShader(gl.VERTEX_SHADER, VERTEX_SHADER);
          const fragmentShader = this.createShader(gl.FRAGMENT_SHADER, FRAGMENT_SHADER);
          
          const program = gl.createProgram();
          gl.attachShader(program, vertexShader);
          gl.attachShader(program, fragmentShader);
          gl.linkProgram(program);
          
          if (!gl.getProgramParameter(program, gl.LINK_STATUS)) {
            console.error('Program link error:', gl.getProgramInfoLog(program));
            return null;
          }
          
          return program;
        }
        
        initializeObjects() {
          for (const objData of this.sceneData.objects) {
            this.objects.set(objData.id, {
              data: objData,
              transform: { ...objData.transform }
            });
          }
        }
        
        initializeAnimations() {
          for (const animData of this.sceneData.animations) {
            this.animations.push({
              ...animData,
              currentKeyframe: 0,
              progress: 0
            });
          }
        }
        
        setupControls() {
          const playBtn = document.getElementById('play-btn');
          const pauseBtn = document.getElementById('pause-btn');
          const restartBtn = document.getElementById('restart-btn');
          
          if (playBtn) {
            playBtn.addEventListener('click', () => this.play());
          }
          
          if (pauseBtn) {
            pauseBtn.addEventListener('click', () => this.pause());
          }
          
          if (restartBtn) {
            restartBtn.addEventListener('click', () => this.restart());
          }
        }
        
        play() {
          if (!this.isPlaying) {
            this.isPlaying = true;
            this.lastFrameTime = performance.now();
            document.getElementById('play-btn').style.display = 'none';
            document.getElementById('pause-btn').style.display = 'flex';
            this.render();
          }
        }
        
        pause() {
          this.isPlaying = false;
          document.getElementById('play-btn').style.display = 'flex';
          document.getElementById('pause-btn').style.display = 'none';
        }
        
        restart() {
          this.currentTime = 0;
          this.updateAnimations();
          this.render();
        }
        
        updateAnimations() {
          for (const anim of this.animations) {
            const obj = this.objects.get(anim.objectId);
            if (!obj) continue;
            
            const keyframes = anim.keyframes;
            if (keyframes.length < 2) continue;
            
            // Find current keyframes
            let prevKf = keyframes[0];
            let nextKf = keyframes[keyframes.length - 1];
            
            for (let i = 0; i < keyframes.length - 1; i++) {
              if (keyframes[i].time <= this.currentTime && keyframes[i + 1].time >= this.currentTime) {
                prevKf = keyframes[i];
                nextKf = keyframes[i + 1];
                break;
              }
            }
            
            // Interpolate
            const duration = nextKf.time - prevKf.time;
            const elapsed = this.currentTime - prevKf.time;
            const t = Math.min(1, Math.max(0, duration > 0 ? elapsed / duration : 0));
            const easedT = this.applyEasing(t, anim.easing);
            
            const startValue = Array.isArray(prevKf.value) ? prevKf.value : [prevKf.value, prevKf.value, prevKf.value];
            const endValue = Array.isArray(nextKf.value) ? nextKf.value : [nextKf.value, nextKf.value, nextKf.value];
            
            obj.transform[anim.property] = startValue.map((v, i) => v + (endValue[i] - v) * easedT);
          }
        }
        
        applyEasing(t, easing) {
          switch (easing) {
            case 'easeIn':
              return t * t;
            case 'easeOut':
              return t * (2 - t);
            case 'easeInOut':
              return t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t;
            default:
              return t;
          }
        }
        
        render() {
          if (!this.isPlaying) return;
          
          const now = performance.now();
          const deltaTime = (now - this.lastFrameTime) / 1000;
          this.lastFrameTime = now;
          
          this.currentTime += deltaTime;
          
          // Update progress bar
          const progress = (this.currentTime / this.sceneData.duration) * 100;
          document.getElementById('progress-bar').style.width = progress + '%';
          
          // Check if animation should loop or end
          if (this.currentTime >= this.sceneData.duration) {
            const looping = this.animations.some(a => a.loop);
            if (looping) {
              this.currentTime = 0;
            } else {
              this.pause();
              return;
            }
          }
          
          this.updateAnimations();
          
          const gl = this.gl;
          gl.clear(gl.COLOR_BUFFER_BIT);
          
          // Render objects would go here
          // For brevity, this is a simplified rendering setup
          
          requestAnimationFrame(() => this.render());
        }
        
        getCurrentState() {
          return {
            time: this.currentTime,
            objects: Array.from(this.objects.entries()).map(([id, obj]) => ({
              id,
              transform: obj.transform
            }))
          };
        }
      }
      
      // Initialize runtime when DOM is ready
      document.addEventListener('DOMContentLoaded', () => {
        const canvas = document.getElementById('canvas');
        window.runtime = new VisualVerseRuntime(canvas, SCENE_DATA);
        
        // Auto-play if configured
        ${this.config.fps > 0 ? 'window.runtime.play();' : ''}
      });
    `;
  }

  /**
   * Generate WebGL shader code.
   */
  private generateShaders(): string {
    return `
      const VERTEX_SHADER = \`
        attribute vec2 a_position;
        uniform vec2 u_resolution;
        uniform vec2 u_translation;
        uniform vec2 u_scale;
        
        void main() {
          vec2 position = a_position * u_scale + u_translation;
          vec2 clipSpace = (position / u_resolution) * 2.0 - 1.0;
          gl_Position = vec4(clipSpace * vec2(1, -1), 0, 1);
        }
      \`;
      
      const FRAGMENT_SHADER = \`
        precision mediump float;
        uniform vec4 u_color;
        
        void main() {
          gl_FragColor = u_color;
        }
      \`;
    `;
  }

  /**
   * Export to a buffer instead of file.
   */
  async exportToBuffer(scene: ISerializable): Promise<WebGLExportResult> {
    const result = await this.export(scene, '');
    return {
      ...result,
      outputPath: undefined,
      htmlContent: result.htmlContent
    };
  }
}
