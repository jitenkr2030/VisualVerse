/**
 * VisualVerse Animation Engine - Lottie Exporter
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
 * Configuration for Lottie export.
 */
export interface LottieExportConfig {
  width: number;
  height: number;
  fps: number;
  frameCount: number;
  duration: number;
  loop: boolean;
  renderer: 'svg' | 'canvas';
  progressiveLoad: boolean;
  includeAssets: boolean;
}

/**
 * Default Lottie export configuration.
 */
export const DEFAULT_LOTTIE_EXPORT_CONFIG: LottieExportConfig = {
  width: 1280,
  height: 720,
  fps: 30,
  frameCount: 300,
  duration: 10,
  loop: true,
  renderer: 'svg',
  progressiveLoad: false,
  includeAssets: false
};

/**
 * Result of a Lottie export operation.
 */
export interface LottieExportResult {
  success: boolean;
  outputPath?: string;
  jsonContent?: string;
  fileSize: number;
  frameCount: number;
  layerCount: number;
  error?: string;
}

/**
 * Lottie animation structure.
 */
export interface LottieAnimation {
  v: string;
  fr: number;
  ip: number;
  op: number;
  w: number;
  h: number;
  nm: string;
  ddd: number;
  assets: LottieAsset[];
  layers: LottieLayer[];
  markers: LottieMarker[];
}

/**
 * Lottie asset.
 */
export interface LottieAsset {
  id: string;
  layer_type?: number;
  w?: number;
  h?: number;
  p?: string;
  u?: string;
  e?: number;
  nm?: string;
  shapes?: LottieShape[];
}

/**
 * Lottie layer.
 */
export interface LottieLayer {
  ddd: number;
  ind: number;
  ty: number;
  nm: string;
  sr: number;
  ks: LottieTransform;
  ao: number;
  shapes: LottieShape[];
  ip: number;
  op: number;
  st: number;
  bm: number;
}

/**
 * Lottie transform.
 */
export interface LottieTransform {
  a?: [number, number, number];
  p?: [number, number, number];
  s?: [number, number, number];
  r?: number;
  o?: number;
}

/**
 * Lottie shape.
 */
export interface LottieShape {
  ty: string;
  nm: string;
  p?: [number, number, number];
  s?: [number, number, number];
  r?: number;
  o?: number;
  c?: [number, number, number, number];
  fill?: { c: [number, number, number, number] };
  stroke?: { c: [number, number, number, number]; w: number };
}

/**
 * Lottie marker.
 */
export interface LottieMarker {
  cm: string;
  dr: number;
}

/**
 * Lottie Exporter for Airbnb Lottie Format.
 * 
 * This class exports scenes to Lottie JSON format, enabling playback
 * in web and mobile applications with native rendering performance.
 */
export class LottieExporter {
  private config: LottieExportConfig;
  private layerCounter: number;
  private shapeCounter: number;

  /**
   * Create a new LottieExporter.
   * 
   * @param config - Optional configuration for the exporter
   */
  constructor(config?: Partial<LottieExportConfig>) {
    this.config = { ...DEFAULT_LOTTIE_EXPORT_CONFIG, ...config };
    this.layerCounter = 0;
    this.shapeCounter = 0;
  }

  /**
   * Export a scene to Lottie JSON format.
   * 
   * @param sceneData - Serialized scene data
   * @param outputPath - Path for the output JSON file
   * @returns Result of the export operation
   */
  async export(sceneData: string, outputPath: string): Promise<LottieExportResult> {
    try {
      const data = JSON.parse(sceneData);
      const animation = this.generateLottie(data);
      const jsonContent = JSON.stringify(animation, null, 2);
      
      return {
        success: true,
        outputPath,
        jsonContent,
        fileSize: new Blob([jsonContent]).size,
        frameCount: this.config.frameCount,
        layerCount: animation.layers?.length || 0
      };
    } catch (error) {
      return {
        success: false,
        fileSize: 0,
        frameCount: 0,
        layerCount: 0,
        error: error instanceof Error ? error.message : 'Unknown export error'
      };
    }
  }

  /**
   * Export to buffer instead of file.
   */
  async exportToBuffer(sceneData: string): Promise<LottieExportResult> {
    const result = await this.export(sceneData, '');
    return {
      ...result,
      outputPath: undefined
    };
  }

  /**
   * Generate Lottie animation structure.
   */
  private generateLottie(sceneData: Record<string, unknown>): LottieAnimation {
    const layers = this.extractLayers(sceneData);
    
    return {
      v: '5.7.0', // Lottie version
      fr: this.config.fps,
      ip: 0, // In point (start frame)
      op: this.config.frameCount, // Out point (end frame)
      w: this.config.width,
      h: this.config.height,
      nm: sceneData.title || 'VisualVerse Animation',
      ddd: 0, // 3D disabled
      assets: this.extractAssets(sceneData),
      layers,
      markers: []
    };
  }

  /**
   * Extract layers from scene data.
   */
  private extractLayers(sceneData: Record<string, unknown>): LottieLayer[] {
    const layers: LottieLayer[] = [];
    const objects = Array.isArray(sceneData.objects) ? sceneData.objects : [];
    const animations = Array.isArray(sceneData.animations) ? sceneData.animations : [];

    // Sort by z-order (reverse order for Lottie - bottom layers first)
    const sortedObjects = [...objects].reverse();

    for (let i = 0; i < sortedObjects.length; i++) {
      const obj = sortedObjects[i] as Record<string, unknown>;
      const layer = this.objectToLayer(obj, i);
      
      // Add animations
      const objAnimations = animations.filter(
        (a: Record<string, unknown>) => a.object_id === obj.id
      );
      
      if (objAnimations.length > 0) {
        layer.shapes = this.addAnimationsToShapes(layer.shapes, objAnimations);
      }

      layers.push(layer);
    }

    return layers;
  }

  /**
   * Convert a scene object to a Lottie layer.
   */
  private objectToLayer(obj: Record<string, unknown>, index: number): LottieLayer {
    const id = obj.id || `layer_${this.layerCounter++}`;
    const type = this.mapObjectType(obj);
    
    return {
      ddd: 0,
      ind: index + 1,
      ty: type,
      nm: id,
      sr: 1,
      ks: this.objectToTransform(obj),
      ao: 0, // Auto orient off
      shapes: this.objectToShapes(obj),
      ip: 0, // Start at frame 0
      op: this.config.frameCount, // End at final frame
      st: 0, // Start time
      bm: 0  // Blend mode normal
    };
  }

  /**
   * Map scene object type to Lottie layer type.
   */
  private mapObjectType(obj: Record<string, unknown>): number {
    const className = String(obj.class || obj.type || '');
    
    if (className.includes('Text') || className.includes('Tex')) return 5; // Text layer
    if (className.includes('Image') || className.includes('Picture')) return 2; // Image layer
    
    return 4; // Shape layer (default)
  }

  /**
   * Convert object transform to Lottie transform.
   */
  private objectToTransform(obj: Record<string, unknown>): LottieTransform {
    const transform = obj.transform as Record<string, unknown> || {};
    const position = transform.position as [number, number, number] || [0, 0, 0];
    const scale = transform.scale as [number, number, number] || [100, 100, 100];
    const rotation = transform.rotation as number || 0;
    const opacity = transform.opacity !== undefined ? (transform.opacity as number) * 100 : 100;

    return {
      a: [0, 0, 0], // Anchor point (animated)
      p: [position[0], position[1], 0],
      s: [scale[0], scale[1], 100],
      r: [rotation, 0, 0],
      o: [opacity, 0, 0]
    };
  }

  /**
   * Convert object to Lottie shapes.
   */
  private objectToShapes(obj: Record<string, unknown>): LottieShape[] {
    const shapes: LottieShape[] = [];
    const className = String(obj.class || obj.type || '');

    // Add fill
    if (obj.fill_color || obj.color) {
      const color = this.parseColor(obj.fill_color || obj.color);
      shapes.push({
        ty: 'fl',
        nm: 'Fill',
        c: color,
        o: 100
      });
    }

    // Add stroke
    if (obj.stroke_color) {
      const color = this.parseColor(obj.stroke_color);
      const width = obj.stroke_width as number || 1;
      shapes.push({
        ty: 'st',
        nm: 'Stroke',
        c: color,
        o: 100,
        w: width
      } as LottieShape);
    }

    // Create the shape geometry
    if (className.includes('Circle')) {
      shapes.push(this.circleToShape(obj));
    } else if (className.includes('Rectangle') || className.includes('Square')) {
      shapes.push(this.rectToShape(obj));
    } else if (className.includes('Path') || className.includes('VMobject')) {
      shapes.push(this.pathToShape(obj));
    } else if (className.includes('Line')) {
      shapes.push(this.lineToShape(obj));
    }

    return shapes;
  }

  /**
   * Convert circle object to Lottie shape.
   */
  private circleToShape(obj: Record<string, unknown>): LottieShape {
    const x = obj.x as number || 0;
    const y = obj.y as number || 0;
    const radius = obj.radius as number || 50;

    return {
      ty: 'el',
      nm: 'Ellipse',
      p: [x, y, 0],
      s: [radius * 2, radius * 2]
    };
  }

  /**
   * Convert rectangle object to Lottie shape.
   */
  private rectToShape(obj: Record<string, unknown>): LottieShape {
    const x = obj.x as number || 0;
    const y = obj.y as number || 0;
    const width = obj.width as number || 100;
    const height = obj.height as number || 100;
    const cornerRadius = obj.corner_radius as number || 0;

    // In Lottie, rectangles are paths
    const halfWidth = width / 2;
    const halfHeight = height / 2;

    // Calculate corner points
    const radius = Math.min(cornerRadius, Math.min(halfWidth, halfHeight));

    // Create path data for rounded rectangle
    const p1 = [x - halfWidth + radius, y - halfHeight];
    const p2 = [x + halfWidth - radius, y - halfHeight];
    const p3 = [x + halfWidth, y - halfHeight + radius];
    const p4 = [x + halfWidth, y + halfHeight - radius];
    const p5 = [x + halfWidth - radius, y + halfHeight];
    const p6 = [x - halfWidth + radius, y + halfHeight];
    const p7 = [x - halfWidth, y + halfHeight - radius];
    const p8 = [x - halfWidth, y - halfHeight + radius];

    const pathData = [
      `M ${p1[0]} ${p1[1]}`,
      `H ${p2[0]}`,
      `A ${radius} ${radius} 0 0 1 ${p3[0]} ${p3[1]}`,
      `V ${p4[1]}`,
      `A ${radius} ${radius} 0 0 1 ${p5[0]} ${p5[1]}`,
      `H ${p6[0]}`,
      `A ${radius} ${radius} 0 0 1 ${p7[0]} ${p7[1]}`,
      `V ${p8[1]}`,
      `A ${radius} ${radius} 0 0 1 ${p1[0]} ${p1[1]}`,
      'Z'
    ].join(' ');

    return {
      ty: 'sh',
      nm: 'Rectangle',
      p: [0, 0, 0],
      ks: {
        a: [0, 0, 0],
        p: [0, 0, 0],
        s: [100, 100, 100],
        r: [0, 0, 0],
        o: [100, 0, 0]
      },
      shapes: [{
        ty: 'rd',
        nm: 'Round',
        ix: 1,
        r: radius,
        nm: 'Rectangle'
      }] as LottieShape[],
      ind: this.shapeCounter++
    } as unknown as LottieShape;
  }

  /**
   * Convert path object to Lottie shape.
   */
  private pathToShape(obj: Record<string, unknown>): LottieShape {
    const points = obj.points;
    let pathData = '';

    if (Array.isArray(points) && points.length > 0) {
      const first = points[0];
      pathData = `M ${first[0]} ${first[1]}`;
      
      for (let i = 1; i < points.length; i++) {
        const p = points[i];
        pathData += ` L ${p[0]} ${p[1]}`;
      }
      
      pathData += ' Z';
    } else if (obj.d && typeof obj.d === 'string') {
      pathData = obj.d;
    } else {
      // Default rectangle
      const width = obj.width as number || 100;
      const height = obj.height as number || 100;
      pathData = `M -${width/2} -${height/2} h ${width} v ${height} h -${width} z`;
    }

    return {
      ty: 'sh',
      nm: 'Path',
      ks: {
        a: [0, 0, 0],
        p: [0, 0, 0],
        s: [100, 100, 100],
        r: [0, 0, 0],
        o: [100, 0, 0]
      },
      ind: this.shapeCounter++
    } as unknown as LottieShape;
  }

  /**
   * Convert line object to Lottie shape.
   */
  private lineToShape(obj: Record<string, unknown>): LottieShape {
    const x1 = obj.x1 as number || 0;
    const y1 = obj.y1 as number || 0;
    const x2 = obj.x2 as number || 100;
    const y2 = obj.y2 as number || 100;

    const pathData = `M ${x1} ${y1} L ${x2} ${y2}`;

    return {
      ty: 'sh',
      nm: 'Line',
      ks: {
        a: [0, 0, 0],
        p: [0, 0, 0],
        s: [100, 100, 100],
        r: [0, 0, 0],
        o: [100, 0, 0]
      },
      ind: this.shapeCounter++
    } as unknown as LottieShape;
  }

  /**
   * Add animations to shape properties.
   */
  private addAnimationsToShapes(
    shapes: LottieShape[],
    animations: Array<Record<string, unknown>>
  ): LottieShape[] {
    // In a full implementation, this would convert animation keyframes
    // to Lottie animation structures
    
    for (const animation of animations) {
      const property = animation.property as string;
      const keyframes = animation.keyframes as Array<Record<string, unknown>>;

      if (keyframes && keyframes.length > 0) {
        // Add animation data to shapes
        // This is simplified - real implementation would be more complex
      }
    }

    return shapes;
  }

  /**
   * Extract assets from scene data.
   */
  private extractAssets(sceneData: Record<string, unknown>): LottieAsset[] {
    const assets: LottieAsset[] = [];
    const images = Array.isArray(sceneData.images) ? sceneData.images : [];

    for (const image of images) {
      assets.push({
        id: image.id || `image_${assets.length}`,
        layer_type: 2,
        w: image.width,
        h: image.height,
        p: image.path,
        u: image.url || '',
        e: 0,
        nm: image.name || 'Image'
      });
    }

    return assets;
  }

  /**
   * Parse color string to Lottie format [r, g, b, a].
   */
  private parseColor(colorStr: unknown): [number, number, number, number] {
    if (!colorStr) return [0, 0, 0, 1];
    
    const color = String(colorStr);
    
    // Handle hex colors
    if (color.startsWith('#')) {
      const hex = color.slice(1);
      const r = parseInt(hex.substr(0, 2), 16) / 255;
      const g = parseInt(hex.substr(2, 2), 16) / 255;
      const b = parseInt(hex.substr(4, 2), 16) / 255;
      return [r, g, b, 1];
    }
    
    // Handle named colors (simplified)
    const namedColors: Record<string, [number, number, number, number]> = {
      'white': [1, 1, 1, 1],
      'black': [0, 0, 0, 1],
      'red': [1, 0, 0, 1],
      'green': [0, 1, 0, 1],
      'blue': [0, 0, 1, 1],
      'transparent': [0, 0, 0, 0]
    };

    return namedColors[color.toLowerCase()] || [0, 0, 0, 1];
  }

  /**
   * Generate a minimal Lottie file for testing.
   */
  generateMinimal(): LottieAnimation {
    return {
      v: '5.7.0',
      fr: 30,
      ip: 0,
      op: 60,
      w: 1280,
      h: 720,
      nm: 'Test Animation',
      ddd: 0,
      assets: [],
      layers: [
        {
          ddd: 0,
          ind: 1,
          ty: 4,
          nm: 'Background',
          sr: 1,
          ks: {
            a: [0, 0, 0],
            p: [640, 360, 0],
            s: [100, 100, 100],
            r: [0, 0, 0],
            o: [100, 0, 0]
          },
          ao: 0,
          shapes: [
            {
              ty: 'rc',
              nm: 'Background Rect',
              p: [0, 0, 0],
              s: [1280, 720],
              r: 0,
              o: 100,
              c: [0.1, 0.1, 0.18, 1]
            }
          ],
          ip: 0,
          op: 60,
          st: 0,
          bm: 0
        }
      ],
      markers: []
    };
  }
}
