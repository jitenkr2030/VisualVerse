/**
 * VisualVerse Animation Engine - SVG Exporter
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
 * Configuration for SVG export.
 */
export interface SVGExportConfig {
  width: number;
  height: number;
  viewBox: string;
  backgroundColor: string;
  includeMetadata: boolean;
  prettyPrint: boolean;
  precision: number;
  xmlns: boolean;
  namespace: string;
}

/**
 * Default SVG export configuration.
 */
export const DEFAULT_SVG_EXPORT_CONFIG: SVGExportConfig = {
  width: 1280,
  height: 720,
  viewBox: '0 0 1280 720',
  backgroundColor: '#1a1a2e',
  includeMetadata: true,
  prettyPrint: true,
  precision: 3,
  xmlns: true,
  namespace: 'http://www.w3.org/2000/svg'
};

/**
 * Result of an SVG export operation.
 */
export interface SVGExportResult {
  success: boolean;
  outputPath?: string;
  svgContent?: string;
  fileSize: number;
  elementCount: number;
  error?: string;
}

/**
 * SVG element types.
 */
export type SVGElementType =
  | 'svg'
  | 'rect'
  | 'circle'
  | 'ellipse'
  | 'line'
  | 'polyline'
  | 'polygon'
  | 'path'
  | 'text'
  | 'tspan'
  | 'g'
  | 'defs'
  | 'linearGradient'
  | 'radialGradient'
  | 'stop'
  | 'image'
  | 'clipPath'
  | 'mask'
  | 'filter';

/**
 * Style properties for SVG elements.
 */
export interface SVGStyle {
  fill?: string;
  fillOpacity?: number;
  stroke?: string;
  strokeWidth?: number;
  strokeOpacity?: number;
  strokeDasharray?: string;
  strokeDashoffset?: number;
  strokeLinecap?: 'butt' | 'round' | 'square';
  strokeLinejoin?: 'miter' | 'round' | 'bevel';
  opacity?: number;
  visibility?: 'visible' | 'hidden' | 'collapse';
  display?: 'none' | 'inline' | 'block' | 'inline-block';
}

/**
 * Transform properties for SVG elements.
 */
export interface SVGTransform {
  translate?: [number, number];
  rotate?: number;
  scale?: [number, number];
  skewX?: number;
  skewY?: number;
  origin?: [number, number];
}

/**
 * SVG Exporter for Vector Graphics.
 * 
 * This class exports scenes to SVG format, supporting vector output
 * for infinite scalability and print-quality graphics.
 */
export class SVGExporter {
  private config: SVGExportConfig;
  private elementIdCounter: number;

  /**
   * Create a new SVGExporter.
   * 
   * @param config - Optional configuration for the exporter
   */
  constructor(config?: Partial<SVGExportConfig>) {
    this.config = { ...DEFAULT_SVG_EXPORT_CONFIG, ...config };
    this.elementIdCounter = 0;
  }

  /**
   * Export a scene to SVG format.
   * 
   * @param sceneData - Serialized scene data
   * @param outputPath - Path for the output SVG file
   * @returns Result of the export operation
   */
  async export(sceneData: string, outputPath: string): Promise<SVGExportResult> {
    try {
      const data = JSON.parse(sceneData);
      const svgContent = this.generateSVG(data);
      
      return {
        success: true,
        outputPath,
        svgContent,
        fileSize: new Blob([svgContent]).size,
        elementCount: this.countElements(svgContent)
      };
    } catch (error) {
      return {
        success: false,
        fileSize: 0,
        elementCount: 0,
        error: error instanceof Error ? error.message : 'Unknown export error'
      };
    }
  }

  /**
   * Export a scene to SVG format (buffer output).
   */
  async exportToBuffer(sceneData: string): Promise<SVGExportResult> {
    const result = await this.export(sceneData, '');
    return {
      ...result,
      outputPath: undefined
    };
  }

  /**
   * Generate the complete SVG content.
   */
  private generateSVG(sceneData: Record<string, unknown>): string {
    const elements = this.extractElements(sceneData);
    const defs = this.extractDefs(sceneData);
    
    let svg = this.config xmlns ? `<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="${this.config.namespace}"` : `<svg`;
    
    svg += `
  width="${this.config.width}"
  height="${this.config.height}"
  viewBox="${this.config.viewBox}"
  preserveAspectRatio="xMidYMid meet">`;

    if (this.config.includeMetadata) {
      svg += `
  <metadata>
    <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
             xmlns:dc="http://purl.org/dc/elements/1.1/"
             xmlns:cc="http://creativecommons.org/ns#">
      <cc:Work>
        <dc:format>image/svg+xml</dc:format>
        <dc:type rdf:resource="http://purl.org/dc/dcmitype/StillImage"/>
        <dc:title>VisualVerse Animation</dc:title>
      </cc:Work>
    </rdf:RDF>
  </metadata>`;
    }

    // Add defs
    if (defs.length > 0) {
      svg += `
  <defs>
${defs.join('\n')}
  </defs>`;
    }

    // Add background
    svg += `
  <rect width="100%" height="100%" fill="${this.config.backgroundColor}"/>`;

    // Add elements
    svg += `
  <g id="scene">
${elements.join('\n')}
  </g>
</svg>`;

    return this.config.prettyPrint ? this.prettyPrint(svg) : svg.trim();
  }

  /**
   * Extract SVG elements from scene data.
   */
  private extractElements(sceneData: Record<string, unknown>): string[] {
    const elements: string[] = [];
    const objects = Array.isArray(sceneData.objects) ? sceneData.objects : [];

    for (const obj of objects) {
      const element = this.objectToSVG(obj);
      if (element) {
        elements.push(element);
      }
    }

    return elements;
  }

  /**
   * Convert a scene object to SVG element.
   */
  private objectToSVG(obj: Record<string, unknown>): string | null {
    const type = this.mapObjectType(obj);
    const id = obj.id || `element_${this.elementIdCounter++}`;
    
    const transform = this.formatTransform(obj.transform);
    const style = this.formatStyle(obj.style);
    const attrs = this.formatAttributes(obj, ['id', 'type', 'class', 'transform', 'style']);

    switch (type) {
      case 'rect':
        return this.createRect(id, obj, transform, style, attrs);
      
      case 'circle':
        return this.createCircle(id, obj, transform, style, attrs);
      
      case 'ellipse':
        return this.createEllipse(id, obj, transform, style, attrs);
      
      case 'line':
        return this.createLine(id, obj, transform, style, attrs);
      
      case 'polyline':
      case 'polygon':
        return this.createPoly(id, type, obj, transform, style, attrs);
      
      case 'path':
        return this.createPath(id, obj, transform, style, attrs);
      
      case 'text':
        return this.createText(id, obj, transform, style, attrs);
      
      case 'group':
        return this.createGroup(id, obj, transform, style, attrs);
      
      default:
        return this.createGeneric(id, type, transform, style, attrs);
    }
  }

  /**
   * Map scene object type to SVG element type.
   */
  private mapObjectType(obj: Record<string, unknown>): SVGElementType {
    const className = String(obj.class || obj.type || '');
    
    if (className.includes('Circle')) return 'circle';
    if (className.includes('Rectangle') || className.includes('Square')) return 'rect';
    if (className.includes('Ellipse')) return 'ellipse';
    if (className.includes('Line') || className.includes('Arrow')) return 'line';
    if (className.includes('Polyline')) return 'polyline';
    if (className.includes('Polygon')) return 'polygon';
    if (className.includes('Path') || className.includes('VMobject')) return 'path';
    if (className.includes('Text') || className.includes('Tex')) return 'text';
    if (className.includes('Group') || className.includes('VGroup')) return 'group';
    
    return 'rect';
  }

  /**
   * Create a rectangle element.
   */
  private createRect(
    id: string,
    obj: Record<string, unknown>,
    transform: string,
    style: string,
    attrs: string
  ): string {
    const x = this.formatNumber((obj.x as number) || 0);
    const y = this.formatNumber((obj.y as number) || 0);
    const width = this.formatNumber((obj.width as number) || 100);
    const height = this.formatNumber((obj.height as number) || 100);
    const rx = this.formatNumber((obj.corner_radius as number) || 0);
    const ry = this.formatNumber(rx);

    return this.wrapElement('rect', {
      id,
      x, y, width, height, rx, ry,
      transform,
      style
    }, attrs);
  }

  /**
   * Create a circle element.
   */
  private createCircle(
    id: string,
    obj: Record<string, unknown>,
    transform: string,
    style: string,
    attrs: string
  ): string {
    const cx = this.formatNumber((obj.x as number) || 0);
    const cy = this.formatNumber((obj.y as number) || 0);
    const r = this.formatNumber((obj.radius as number) || 50);

    return this.wrapElement('circle', {
      id,
      cx, cy, r,
      transform,
      style
    }, attrs);
  }

  /**
   * Create an ellipse element.
   */
  private createEllipse(
    id: string,
    obj: Record<string, unknown>,
    transform: string,
    style: string,
    attrs: string
  ): string {
    const cx = this.formatNumber((obj.x as number) || 0);
    const cy = this.formatNumber((obj.y as number) || 0);
    const rx = this.formatNumber((obj.radius_x as number) || 50);
    const ry = this.formatNumber((obj.radius_y as number) || 30);

    return this.wrapElement('ellipse', {
      id,
      cx, cy, rx, ry,
      transform,
      style
    }, attrs);
  }

  /**
   * Create a line element.
   */
  private createLine(
    id: string,
    obj: Record<string, unknown>,
    transform: string,
    style: string,
    attrs: string
  ): string {
    const x1 = this.formatNumber((obj.x1 as number) || 0);
    const y1 = this.formatNumber((obj.y1 as number) || 0);
    const x2 = this.formatNumber((obj.x2 as number) || 100);
    const y2 = this.formatNumber((obj.y2 as number) || 100);

    return this.wrapElement('line', {
      id,
      x1, y1, x2, y2,
      transform,
      style
    }, attrs);
  }

  /**
   * Create a polyline or polygon element.
   */
  private createPoly(
    id: string,
    type: SVGElementType,
    obj: Record<string, unknown>,
    transform: string,
    style: string,
    attrs: string
  ): string {
    const points = obj.points;
    let pointsStr = '';
    
    if (Array.isArray(points)) {
      pointsStr = points.map((p: number[]) => 
        `${this.formatNumber(p[0])},${this.formatNumber(p[1])}`
      ).join(' ');
    }

    return this.wrapElement(type, {
      id,
      points: pointsStr,
      transform,
      style
    }, attrs);
  }

  /**
   * Create a path element.
   */
  private createPath(
    id: string,
    obj: Record<string, unknown>,
    transform: string,
    style: string,
    attrs: string
  ): string {
    const d = this.pathDataFromObject(obj);
    return this.wrapElement('path', {
      id,
      d,
      transform,
      style
    }, attrs);
  }

  /**
   * Generate path data from object properties.
   */
  private pathDataFromObject(obj: Record<string, unknown>): string {
    // Check for explicit path data
    if (obj.d && typeof obj.d === 'string') {
      return obj.d;
    }

    // Generate from points
    const points = obj.points;
    if (Array.isArray(points) && points.length > 0) {
      const first = points[0];
      let d = `M ${this.formatNumber(first[0])},${this.formatNumber(first[1])}`;
      
      for (let i = 1; i < points.length; i++) {
        const p = points[i];
        d += ` L ${this.formatNumber(p[0])},${this.formatNumber(p[1])}`;
      }
      
      return d;
    }

    // Generate from bounding box
    const x = obj.x as number || 0;
    const y = obj.y as number || 0;
    const width = obj.width as number || 100;
    const height = obj.height as number || 100;

    return `M ${x},${y} h ${width} v ${height} h -${width} z`;
  }

  /**
   * Create a text element.
   */
  private createText(
    id: string,
    obj: Record<string, unknown>,
    transform: string,
    style: string,
    attrs: string
  ): string {
    const x = this.formatNumber((obj.x as number) || 0);
    const y = this.formatNumber((obj.y as number) || 0);
    const text = String(obj.text || obj.content || '');
    const fontSize = this.formatNumber((obj.font_size as number) || 24);
    const textAnchor = obj.text_align || 'middle';

    const tspan = this.wrapElement('tspan', {
      'font-size': fontSize,
      'x': x,
      'dy': '0.35em'
    }, '', text);

    return this.wrapElement('text', {
      id,
      x, y,
      'text-anchor': textAnchor,
      transform,
      style
    }, attrs, tspan);
  }

  /**
   * Create a group element.
   */
  private createGroup(
    id: string,
    obj: Record<string, unknown>,
    transform: string,
    style: string,
    attrs: string
  ): string {
    const children = Array.isArray(obj.children) ? obj.children : [];
    const childElements = children
      .map((child: Record<string, unknown>) => this.objectToSVG(child))
      .filter(Boolean)
      .join('\n    ');

    return this.wrapElement('g', {
      id,
      transform,
      style
    }, attrs, childElements);
  }

  /**
   * Create a generic element for unmapped types.
   */
  private createGeneric(
    id: string,
    type: string,
    transform: string,
    style: string,
    attrs: string
  ): string {
    return this.wrapElement('g', {
      id,
      transform,
      style
    }, attrs);
  }

  /**
   * Extract defs (gradients, patterns, etc.) from scene data.
   */
  private extractDefs(sceneData: Record<string, unknown>): string[] {
    const defs: string[] = [];
    const gradients = Array.isArray(sceneData.gradients) ? sceneData.gradients : [];

    for (const gradient of gradients) {
      const def = this.gradientToDef(gradient);
      if (def) {
        defs.push(def);
      }
    }

    return defs;
  }

  /**
   * Convert a gradient to SVG defs.
   */
  private gradientToDef(gradient: Record<string, unknown>): string | null {
    const id = gradient.id || `gradient_${this.elementIdCounter++}`;
    const type = gradient.type || 'linear';
    const stops = Array.isArray(gradient.stops) ? gradient.stops : [];

    if (type === 'linear') {
      const x1 = this.formatNumber((gradient.x1 as number) || 0);
      const y1 = this.formatNumber((gradient.y1 as number) || 0);
      const x2 = this.formatNumber((gradient.x2 as number) || 100);
      const y2 = this.formatNumber((gradient.y2 as number) || 0);

      const stopElements = stops.map((stop: Record<string, unknown>) => {
        const offset = stop.offset || '0%';
        const color = stop.color || '#000';
        const opacity = stop.opacity !== undefined ? stop.opacity : 1;
        return `    <stop offset="${offset}" stop-color="${color}" stop-opacity="${opacity}"/>`;
      }).join('\n');

      return `  <linearGradient id="${id}" x1="${x1}%" y1="${y1}%" x2="${x2}%" y2="${y2}%">
${stopElements}
  </linearGradient>`;
    }

    if (type === 'radial') {
      const cx = this.formatNumber((gradient.cx as number) || 50);
      const cy = this.formatNumber((gradient.cy as number) || 50);
      const r = this.formatNumber((gradient.r as number) || 50);

      const stopElements = stops.map((stop: Record<string, unknown>) => {
        const offset = stop.offset || '0%';
        const color = stop.color || '#000';
        const opacity = stop.opacity !== undefined ? stop.opacity : 1;
        return `    <stop offset="${offset}" stop-color="${color}" stop-opacity="${opacity}"/>`;
      }).join('\n');

      return `  <radialGradient id="${id}" cx="${cx}%" cy="${cy}%" r="${r}%">
${stopElements}
  </radialGradient>`;
    }

    return null;
  }

  /**
   * Format transform attributes.
   */
  private formatTransform(transform: unknown): string {
    if (!transform) return '';
    
    const t = transform as Record<string, unknown>;
    const parts: string[] = [];

    if (t.translate) {
      const [x, y] = t.translate as [number, number];
      parts.push(`translate(${this.formatNumber(x)}, ${this.formatNumber(y)})`);
    }

    if (t.rotate !== undefined) {
      parts.push(`rotate(${this.formatNumber(t.rotate as number)})`);
    }

    if (t.scale) {
      const [x, y] = t.scale as [number, number];
      parts.push(`scale(${this.formatNumber(x)}, ${this.formatNumber(y)})`);
    }

    if (t.skewX !== undefined) {
      parts.push(`skewX(${this.formatNumber(t.skewX as number)})`);
    }

    if (t.skewY !== undefined) {
      parts.push(`skewY(${this.formatNumber(t.skewY as number)})`);
    }

    return parts.length > 0 ? parts.join(' ') : '';
  }

  /**
   * Format style attributes.
   */
  private formatStyle(style: unknown): string {
    if (!style) return '';
    
    const s = style as Record<string, unknown>;
    const parts: string[] = [];

    if (s.fill) parts.push(`fill: ${s.fill}`);
    if (s.fillOpacity !== undefined) parts.push(`fill-opacity: ${s.fillOpacity}`);
    if (s.stroke) parts.push(`stroke: ${s.stroke}`);
    if (s.strokeWidth !== undefined) parts.push(`stroke-width: ${this.formatNumber(s.strokeWidth as number)}`);
    if (s.strokeOpacity !== undefined) parts.push(`stroke-opacity: ${s.strokeOpacity}`);
    if (s.strokeDasharray) parts.push(`stroke-dasharray: ${s.strokeDasharray}`);
    if (s.opacity !== undefined) parts.push(`opacity: ${s.opacity}`);
    if (s.visibility) parts.push(`visibility: ${s.visibility}`);

    return parts.join('; ');
  }

  /**
   * Format additional attributes.
   */
  private formatAttributes(
    obj: Record<string, unknown>,
    exclude: string[]
  ): string {
    const attrs: string[] = [];
    
    for (const [key, value] of Object.entries(obj)) {
      if (exclude.includes(key)) continue;
      if (key === 'style' || key === 'transform') continue;
      if (key === 'children' || key === 'points') continue;
      if (key === 'class') attrs.push(`class="${value}"`);
      if (typeof value === 'string' || typeof value === 'number') {
        attrs.push(`${key}="${value}"`);
      }
    }

    return attrs.join(' ');
  }

  /**
   * Wrap content in an SVG element.
   */
  private wrapElement(
    type: string,
    attrs: Record<string, string>,
    extraAttrs: string,
    content?: string
  ): string {
    const attrStr = Object.entries(attrs)
      .filter(([_, v]) => v !== '')
      .map(([k, v]) => `${k}="${v}"`)
      .join(' ');
    
    const allAttrs = [attrStr, extraAttrs].filter(Boolean).join(' ');

    if (content) {
      return `  <${type} ${allAttrs}>
    ${content.replace(/\n/g, '\n    ')}
  </${type}>`;
    }

    return `  <${type} ${allAttrs}/>`;
  }

  /**
   * Format a number to specified precision.
   */
  private formatNumber(value: number): string {
    if (value === 0) return '0';
    return value.toFixed(this.config.precision).replace(/\.?0+$/, '');
  }

  /**
   * Pretty print SVG content.
   */
  private prettyPrint(svg: string): string {
    return svg;
  }

  /**
   * Count elements in SVG content.
   */
  private countElements(svg: string): number {
    const matches = svg.match(/<[a-z]+/gi);
    return matches ? matches.length : 0;
  }
}
