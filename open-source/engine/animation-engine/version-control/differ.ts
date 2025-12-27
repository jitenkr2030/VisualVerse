/**
 * VisualVerse Animation Engine - Visual Differ
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
 * Result of a visual comparison operation.
 */
export interface DiffResult {
  hasDifference: boolean;
  diffPercentage: number;
  diffImage?: Uint8Array;
  sideBySideImage?: Uint8Array;
  overlayImage?: Uint8Array;
  analysis: DiffAnalysis;
}

/**
 * Analysis details of the difference.
 */
export interface DiffAnalysis {
  totalPixels: number;
  differentPixels: number;
  maxDiffValue: number;
  affectedRegions: DiffRegion[];
  severity: 'none' | 'minor' | 'moderate' | 'significant';
  likelyCause?: string;
}

/**
 * A region where differences were detected.
 */
export interface DiffRegion {
  x: number;
  y: number;
  width: number;
  height: number;
  diffPercentage: number;
  avgColorDiff: number;
}

/**
 * Configuration for the visual differ.
 */
export interface VisualDiffConfig {
  threshold: number;              // Pixel difference threshold (0-1)
  ignoreAntialiasing: boolean;     // Ignore anti-aliasing differences
  ignoreColors: boolean;           // Ignore color differences (compare structure only)
  alphaThreshold: number;          // Alpha difference threshold
  diffColor: [number, number, number]; // RGB color for diff highlighting
  diffBlendMode: 'multiply' | 'screen' | 'overlay';
  includeRegions: boolean;         // Include region analysis
  maxRegions: number;              // Maximum regions to report
}

/**
 * Default visual diff configuration.
 */
export const DEFAULT_VISUAL_DIFF_CONFIG: VisualDiffConfig = {
  threshold: 0.1,                 // 10% difference threshold
  ignoreAntialiasing: true,        // Ignore anti-aliasing
  ignoreColors: false,             // Compare colors
  alphaThreshold: 0.1,             // 10% alpha difference
  diffColor: [255, 0, 128],        // Magenta for differences
  diffBlendMode: 'multiply',
  includeRegions: true,
  maxRegions: 10
};

/**
 * Visual Difference Analyzer for comparing rendered frames.
 * 
 * This class provides tools to compare two visual outputs and detect
 * differences with various analysis options.
 */
export class VisualDiffer {
  private config: VisualDiffConfig;

  /**
   * Create a new VisualDiffer instance.
   * 
   * @param config - Optional configuration for the differ
   */
  constructor(config?: Partial<VisualDiffConfig>) {
    this.config = { ...DEFAULT_VISUAL_DIFF_CONFIG, ...config };
  }

  /**
   * Compare two image buffers and generate a diff result.
   * 
   * @param imageA - First image buffer (PNG or compatible format)
   * @param imageB - Second image buffer (PNG or compatible format)
   * @param generateImages - Whether to generate diff images
   * @returns Diff result with analysis
   */
  async compare(
    imageA: Uint8Array,
    imageB: Uint8Array,
    generateImages: boolean = true
  ): Promise<DiffResult> {
    // Decode images
    const imgDataA = await this.decodeImage(imageA);
    const imgDataB = await this.decodeImage(imageB);

    // Check if dimensions match
    if (imgDataA.width !== imgDataB.width || imgDataA.height !== imgDataB.height) {
      return this.createDimensionMismatchResult(imgDataA, imgDataB);
    }

    // Compare pixels
    const diffResult = this.comparePixelData(imgDataA, imgDataB);

    // Generate diff images if requested
    let diffImage: Uint8Array | undefined;
    let sideBySideImage: Uint8Array | undefined;
    let overlayImage: Uint8Array | undefined;

    if (generateImages) {
      diffImage = this.generateDiffImage(imgDataA, imgDataB, diffResult.diffMap);
      sideBySideImage = this.generateSideBySideImage(imgDataA, imgDataB);
      overlayImage = this.generateOverlayImage(imgDataA, imgDataB, diffResult.diffMap);
    }

    // Analyze affected regions
    const regions = this.analyzeRegions(diffResult.diffMap, imgDataA.width);

    // Determine severity
    const severity = this.determineSeverity(diffResult.diffPercentage);

    // Guess likely cause
    const likelyCause = this.guessLikelyCause(regions, diffResult.diffPercentage);

    const analysis: DiffAnalysis = {
      totalPixels: imgDataA.width * imgDataA.height,
      differentPixels: diffResult.differentPixels,
      maxDiffValue: diffResult.maxDiff,
      affectedRegions: regions.slice(0, this.config.maxRegions),
      severity,
      likelyCause
    };

    return {
      hasDifference: diffResult.differentPixels > 0,
      diffPercentage: diffResult.diffPercentage,
      diffImage,
      sideBySideImage,
      overlayImage,
      analysis
    };
  }

  /**
   * Decode an image buffer to image data.
   */
  private async decodeImage(buffer: Uint8Array): Promise<ImageData> {
    // Create a blob from the buffer
    const blob = new Blob([buffer], { type: 'image/png' });
    const bitmap = await createImageBitmap(blob);
    
    const canvas = new OffscreenCanvas(bitmap.width, bitmap.height);
    const ctx = canvas.getContext('2d');
    if (!ctx) {
      throw new Error('Failed to get canvas context');
    }
    
    ctx.drawImage(bitmap, 0, 0);
    return ctx.getImageData(0, 0, bitmap.width, bitmap.height);
  }

  /**
   * Compare pixel data from two images.
   */
  private comparePixelData(
    imgDataA: ImageData,
    imgDataB: ImageData
  ): { diffMap: Uint8Array; differentPixels: number; diffPercentage: number; maxDiff: number } {
    const { width, height, data: dataA } = imgDataA;
    const dataB = imgDataB.data;
    const diffMap = new Uint8Array(width * height);
    
    let differentPixels = 0;
    let maxDiff = 0;

    for (let i = 0; i < dataA.length; i += 4) {
      const pixelIndex = i / 4;
      const x = pixelIndex % width;
      const y = Math.floor(pixelIndex / width);

      // Skip anti-aliasing pixels if configured
      if (this.config.ignoreAntialiasing && this.isAntiAliasingPixel(dataA, dataB, i, x, y, width)) {
        diffMap[pixelIndex] = 0;
        continue;
      }

      // Calculate pixel difference
      const diff = this.calculatePixelDiff(dataA, dataB, i);

      if (diff > 0) {
        differentPixels++;
        diffMap[pixelIndex] = Math.min(255, diff * 255);
        maxDiff = Math.max(maxDiff, diff);
      } else {
        diffMap[pixelIndex] = 0;
      }
    }

    const totalPixels = width * height;
    const diffPercentage = differentPixels / totalPixels;

    return { diffMap, differentPixels, diffPercentage, maxDiff };
  }

  /**
   * Check if a pixel is an anti-aliasing pixel.
   */
  private isAntiAliasingPixel(
    dataA: Uint8ClampedArray,
    dataB: Uint8ClampedArray,
    index: number,
    x: number,
    y: number,
    width: number
  ): boolean {
    // Check neighboring pixels for gradual color transitions
    const neighbors = [
      this.getPixelDiff(dataA, dataA, index - 4, index, width),
      this.getPixelDiff(dataA, dataA, index + 4, index, width),
      this.getPixelDiff(dataA, dataA, index - width * 4, index, width),
      this.getPixelDiff(dataA, dataA, index + width * 4, index, width)
    ];

    // If all neighbors have similar differences, it's likely anti-aliasing
    const avgNeighborDiff = neighbors.reduce((a, b) => a + b, 0) / neighbors.length;
    const currentDiff = this.getPixelDiff(dataA, dataB, index, index + 4);

    return Math.abs(currentDiff - avgNeighborDiff) < 0.1;
  }

  /**
   * Get the difference between two pixels.
   */
  private getPixelDiff(
    dataA: Uint8ClampedArray,
    dataB: Uint8ClampedArray,
    indexA: number,
    indexB: number
  ): number {
    let totalDiff = 0;
    for (let j = 0; j < 4; j++) {
      totalDiff += Math.abs(dataA[indexA + j] - dataB[indexB + j]);
    }
    return totalDiff / (4 * 255);
  }

  /**
   * Calculate the difference between two pixels.
   */
  private calculatePixelDiff(dataA: Uint8ClampedArray, dataB: Uint8ClampedArray, index: number): number {
    let totalDiff = 0;

    if (!this.config.ignoreColors) {
      // Compare RGBA channels
      for (let j = 0; j < 4; j++) {
        const diff = Math.abs(dataA[index + j] - dataB[index + j]);
        
        // Handle alpha specially
        if (j === 3) {
          if (diff / 255 < this.config.alphaThreshold) {
            continue;
          }
        }
        
        totalDiff += diff;
      }
    } else {
      // Compare only structure (alpha/luminance)
      const lumA = 0.299 * dataA[index] + 0.587 * dataA[index + 1] + 0.114 * dataA[index + 2];
      const lumB = 0.299 * dataB[index] + 0.587 * dataB[index + 1] + 0.114 * dataB[index + 2];
      totalDiff = Math.abs(lumA - lumB);
    }

    return Math.min(1, totalDiff / (4 * 255));
  }

  /**
   * Generate a diff image highlighting the differences.
   */
  private generateDiffImage(
    imgDataA: ImageData,
    imgDataB: ImageData,
    diffMap: Uint8Array
  ): Uint8Array {
    const { width, height, data } = imgDataA;
    const outputData = new Uint8ClampedArray(width * height * 4);

    for (let i = 0; i < data.length; i += 4) {
      const pixelIndex = i / 4;
      const diffValue = diffMap[pixelIndex];

      if (diffValue > 0) {
        // Blend diff color with original
        const blendFactor = Math.min(1, diffValue * 2);
        outputData[i] = Math.round(data[i] * (1 - blendFactor) + this.config.diffColor[0] * blendFactor);
        outputData[i + 1] = Math.round(data[i + 1] * (1 - blendFactor) + this.config.diffColor[1] * blendFactor);
        outputData[i + 2] = Math.round(data[i + 2] * (1 - blendFactor) + this.config.diffColor[2] * blendFactor);
        outputData[i + 3] = 255;
      } else {
        // No difference - show original in grayscale
        const gray = Math.round(0.299 * data[i] + 0.587 * data[i + 1] + 0.114 * data[i + 2]);
        outputData[i] = gray;
        outputData[i + 1] = gray;
        outputData[i + 2] = gray;
        outputData[i + 3] = 255;
      }
    }

    return new Uint8Array(outputData.buffer);
  }

  /**
   * Generate a side-by-side comparison image.
   */
  private generateSideBySideImage(imgDataA: ImageData, imgDataB: ImageData): Uint8Array {
    const { width, height, data: dataA } = imgDataA;
    const dataB = imgDataB.data;
    const outputWidth = width * 2;
    const outputData = new Uint8ClampedArray(outputWidth * height * 4);

    // Left side - Image A
    for (let y = 0; y < height; y++) {
      for (let x = 0; x < width; x++) {
        const srcIndex = (y * width + x) * 4;
        const dstIndex = (y * outputWidth + x) * 4;
        
        outputData[dstIndex] = dataA[srcIndex];
        outputData[dstIndex + 1] = dataA[srcIndex + 1];
        outputData[dstIndex + 2] = dataA[srcIndex + 2];
        outputData[dstIndex + 3] = dataA[srcIndex + 3];
      }
    }

    // Right side - Image B
    for (let y = 0; y < height; y++) {
      for (let x = 0; x < width; x++) {
        const srcIndex = (y * width + x) * 4;
        const dstIndex = (y * outputWidth + width + x) * 4;
        
        outputData[dstIndex] = dataB[srcIndex];
        outputData[dstIndex + 1] = dataB[srcIndex + 1];
        outputData[dstIndex + 2] = dataB[srcIndex + 2];
        outputData[dstIndex + 3] = dataB[srcIndex + 3];
      }
    }

    return new Uint8Array(outputData.buffer);
  }

  /**
   * Generate an overlay comparison image.
   */
  private generateOverlayImage(
    imgDataA: ImageData,
    imgDataB: ImageData,
    diffMap: Uint8Array
  ): Uint8Array {
    const { width, height, data: dataA } = imgDataA;
    const dataB = imgDataB.data;
    const outputData = new Uint8ClampedArray(width * height * 4);

    for (let i = 0; i < dataA.length; i += 4) {
      const pixelIndex = i / 4;
      const diffValue = diffMap[pixelIndex];

      if (diffValue > 0) {
        // Show both images blended
        outputData[i] = Math.round((dataA[i] + dataB[i]) / 2);
        outputData[i + 1] = Math.round((dataA[i + 1] + dataB[i + 1]) / 2);
        outputData[i + 2] = Math.round((dataA[i + 2] + dataB[i + 2]) / 2);
        outputData[i + 3] = 255;
      } else {
        // No difference - show green
        outputData[i] = 0;
        outputData[i + 1] = 200;
        outputData[i + 2] = 100;
        outputData[i + 3] = 255;
      }
    }

    return new Uint8Array(outputData.buffer);
  }

  /**
   * Analyze affected regions in the diff.
   */
  private analyzeRegions(diffMap: Uint8Array, width: number): DiffRegion[] {
    if (!this.config.includeRegions) {
      return [];
    }

    const height = diffMap.length / width;
    const regions: DiffRegion[] = [];
    const visited = new Set<string>();

    // Simple connected component analysis
    for (let y = 0; y < height; y++) {
      for (let x = 0; x < width; x++) {
        const index = y * width + x;
        const key = `${x},${y}`;

        if (diffMap[index] > 0 && !visited.has(key)) {
          const region = this.floodFillRegion(diffMap, width, height, x, y, visited);
          regions.push(region);
        }
      }
    }

    // Sort by size (most significant first)
    regions.sort((a, b) => b.diffPercentage - a.diffPercentage);

    return regions;
  }

  /**
   * Flood fill to find a connected region of differences.
   */
  private floodFillRegion(
    diffMap: Uint8Array,
    width: number,
    height: number,
    startX: number,
    startY: number,
    visited: Set<string>
  ): DiffRegion {
    const stack = [{ x: startX, y: startY }];
    const pixels: { x: number; y: number }[] = [];
    let totalColorDiff = 0;
    let diffPixelCount = 0;

    while (stack.length > 0) {
      const { x, y } = stack.pop()!;
      const key = `${x},${y}`;

      if (x < 0 || x >= width || y < 0 || y >= height || visited.has(key)) {
        continue;
      }

      const index = y * width + x;
      if (diffMap[index] === 0) {
        continue;
      }

      visited.add(key);
      pixels.push({ x, y });
      totalColorDiff += diffMap[index];
      diffPixelCount++;

      // Add neighbors
      stack.push({ x: x + 1, y });
      stack.push({ x: x - 1, y });
      stack.push({ x, y: y + 1 });
      stack.push({ x, y: y - 1 });
    }

    // Calculate bounding box
    const xs = pixels.map(p => p.x);
    const ys = pixels.map(p => p.y);
    const minX = Math.min(...xs);
    const maxX = Math.max(...xs);
    const minY = Math.min(...ys);
    const maxY = Math.max(...ys);

    return {
      x: minX,
      y: minY,
      width: maxX - minX + 1,
      height: maxY - minY + 1,
      diffPercentage: diffPixelCount / pixels.length,
      avgColorDiff: totalColorDiff / diffPixelCount
    };
  }

  /**
   * Determine the severity of differences.
   */
  private determineSeverity(diffPercentage: number): 'none' | 'minor' | 'moderate' | 'significant' {
    if (diffPercentage === 0) return 'none';
    if (diffPercentage < 0.01) return 'minor';
    if (diffPercentage < 0.05) return 'moderate';
    return 'significant';
  }

  /**
   * Guess the likely cause of differences based on region analysis.
   */
  private guessLikelyCause(regions: DiffRegion[], diffPercentage: number): string | undefined {
    if (diffPercentage === 0) return undefined;

    if (regions.length === 0) return 'Uniform color shift';

    // Check for specific patterns
    const totalArea = regions.reduce((sum, r) => sum + r.width * r.height, 0);
    const hasLargeRegions = regions.some(r => r.width * r.height > totalArea * 0.5);
    const hasManySmallRegions = regions.length > 50;

    if (hasLargeRegions) {
      if (regions.length === 1) return 'Element position change';
      return 'Multiple element changes';
    }

    if (hasManySmallRegions) return 'Anti-aliasing or rendering artifact';
    if (regions.every(r => r.width === 1 && r.height === 1)) return 'Pixel-perfect alignment issue';

    return 'Partial element modification';
  }

  /**
   * Create a result for dimension mismatches.
   */
  private createDimensionMismatchResult(imgDataA: ImageData, imgDataB: ImageData): DiffResult {
    return {
      hasDifference: true,
      diffPercentage: 1,
      analysis: {
        totalPixels: imgDataA.width * imgDataA.height,
        differentPixels: imgDataA.width * imgDataA.height,
        maxDiffValue: 1,
        affectedRegions: [],
        severity: 'significant',
        likelyCause: 'Dimension mismatch'
      }
    };
  }

  /**
   * Check if two images are visually identical within threshold.
   */
  async isIdentical(imageA: Uint8Array, imageB: Uint8Array, customThreshold?: number): Promise<boolean> {
    const threshold = customThreshold ?? this.config.threshold;
    const result = await this.compare(imageA, imageB, false);
    return result.diffPercentage <= threshold;
  }
}
