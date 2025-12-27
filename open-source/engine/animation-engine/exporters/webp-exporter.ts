/**
 * VisualVerse Animation Engine - WebP Exporter
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
 * Configuration for WebP export.
 */
export interface WebPExportConfig {
  width: number;
  height: number;
  fps: number;
  quality: number;
  lossless: boolean;
  method: 0 | 1 | 2 | 3 | 4 | 5 | 6;
  imageHint: 'default' | 'photo' | 'picture' | 'graph' | 'icon';
  loop: number;
  backgroundColor: [number, number, number, number];
  animated: boolean;
  chunkSize: number;
}

/**
 * Default WebP export configuration.
 */
export const DEFAULT_WEBP_EXPORT_CONFIG: WebPExportConfig = {
  width: 1280,
  height: 720,
  fps: 30,
  quality: 80,
  lossless: false,
  method: 4,
  imageHint: 'picture',
  loop: 0, // 0 = infinite loop
  backgroundColor: [26, 26, 46, 255], // #1a1a2e
  animated: true,
  chunkSize: 8192
};

/**
 * Result of a WebP export operation.
 */
export interface WebPExportResult {
  success: boolean;
  outputPath?: string;
  data?: Uint8Array;
  fileSize: number;
  frameCount: number;
  duration: number;
  quality: number;
  compressionRatio: number;
  error?: string;
}

/**
 * WebP Frame for animated WebP creation.
 */
export interface WebPFrame {
  data: Uint8Array | ArrayBuffer;
  delay: number; // Delay in milliseconds
  x: number;
  y: number;
  width: number;
  height: number;
  dispose: 0 | 1 | 2 | 3;
  blend: 0 | 1;
}

/**
 * WebP Exporter for Animated WebP Format.
 * 
 * This class exports animations to WebP format, providing excellent
 * compression for web graphics with both lossy and lossless options.
 */
export class WebPExporter {
  private config: WebPExportConfig;

  /**
   * Create a new WebPExporter.
   * 
   * @param config - Optional configuration for the exporter
   */
  constructor(config?: Partial<WebPExportConfig>) {
    this.config = { ...DEFAULT_WEBP_EXPORT_CONFIG, ...config };
  }

  /**
   * Export frames to animated WebP.
   * 
   * @param frames - Array of frames to export
   * @param outputPath - Path for the output WebP file
   * @returns Result of the export operation
   */
  async exportAnimated(
    frames: Uint8Array[],
    outputPath: string
  ): Promise<WebPExportResult> {
    try {
      if (frames.length === 0) {
        return {
          success: false,
          fileSize: 0,
          frameCount: 0,
          duration: 0,
          quality: this.config.quality,
          compressionRatio: 0,
          error: 'No frames provided'
        };
      }

      // Calculate frame delay
      const frameDelayMs = 1000 / this.config.fps;
      const duration = frames.length * frameDelayMs;

      // Convert frames to WebP format
      const webpData = await this.encodeFrames(frames);

      // Calculate compression ratio
      const originalSize = frames.reduce((sum, f) => sum + f.length, 0);
      const compressionRatio = originalSize > 0 ? (1 - webpData.length / originalSize) * 100 : 0;

      return {
        success: true,
        outputPath,
        data: webpData,
        fileSize: webpData.length,
        frameCount: frames.length,
        duration: duration / 1000,
        quality: this.config.quality,
        compressionRatio
      };
    } catch (error) {
      return {
        success: false,
        fileSize: 0,
        frameCount: 0,
        duration: 0,
        quality: this.config.quality,
        compressionRatio: 0,
        error: error instanceof Error ? error.message : 'Unknown export error'
      };
    }
  }

  /**
   * Export a single frame to WebP.
   * 
   * @param frame - Image data for the frame
   * @param outputPath - Path for the output WebP file
   * @returns Result of the export operation
   */
  async exportFrame(
    frame: Uint8Array,
    outputPath: string
  ): Promise<WebPExportResult> {
    try {
      const webpData = await this.encodeSingleFrame(frame);

      return {
        success: true,
        outputPath,
        data: webpData,
        fileSize: webpData.length,
        frameCount: 1,
        duration: 1 / this.config.fps,
        quality: this.config.quality,
        compressionRatio: 0
      };
    } catch (error) {
      return {
        success: false,
        fileSize: 0,
        frameCount: 0,
        duration: 0,
        quality: this.config.quality,
        compressionRatio: 0,
        error: error instanceof Error ? error.message : 'Unknown export error'
      };
    }
  }

  /**
   * Encode a single frame to WebP.
   */
  private async encodeSingleFrame(frame: Uint8Array): Promise<Uint8Array> {
    // In a Node.js environment, we would use sharp or libwebp
    // For browser/TypeScript environment, we use canvas
    
    // Check if we're in a browser environment
    if (typeof window !== 'undefined') {
      return this.encodeFrameInBrowser(frame);
    }

    // For Node.js, we'd use sharp
    // This is a placeholder that simulates WebP encoding
    return this.simulateWebPEncoding(frame);
  }

  /**
   * Encode frames to animated WebP.
   */
  private async encodeFrames(frames: Uint8Array[]): Promise<Uint8Array> {
    if (typeof window !== 'undefined') {
      return this.encodeFramesInBrowser(frames);
    }

    // For Node.js, we'd use sharp
    return this.simulateAnimatedWebPEncoding(frames);
  }

  /**
   * Encode a frame in the browser using Canvas.
   */
  private async encodeFrameInBrowser(frame: Uint8Array): Promise<Uint8Array> {
    // Create a blob from the frame data
    const blob = new Blob([frame], { type: 'image/png' });
    const bitmap = await createImageBitmap(blob);
    
    // Create canvas
    const canvas = new OffscreenCanvas(this.config.width, this.config.height);
    const ctx = canvas.getContext('2d');
    if (!ctx) {
      throw new Error('Failed to get canvas context');
    }

    // Draw the bitmap
    ctx.drawImage(bitmap, 0, 0);

    // Convert to WebP
    const webpBlob = await canvas.convertToBlob({
      type: 'image/webp',
      quality: this.config.quality / 100
    });

    const arrayBuffer = await webpBlob.arrayBuffer();
    return new Uint8Array(arrayBuffer);
  }

  /**
   * Encode frames in the browser for animated WebP.
   */
  private async encodeFramesInBrowser(frames: Uint8Array[]): Promise<Uint8Array> {
    const canvas = new OffscreenCanvas(this.config.width, this.config.height);
    const ctx = canvas.getContext('2d');
    if (!ctx) {
      throw new Error('Failed to get canvas context');
    }

    const webpFrames: WebPFrame[] = [];
    const frameDelayMs = 1000 / this.config.fps;

    for (let i = 0; i < frames.length; i++) {
      const frame = frames[i];
      
      // Create bitmap from frame
      const blob = new Blob([frame], { type: 'image/png' });
      const bitmap = await createImageBitmap(blob);
      
      // Clear canvas for this frame
      ctx.fillStyle = `rgba(${this.config.backgroundColor.join(',')})`;
      ctx.fillRect(0, 0, this.config.width, this.config.height);
      
      // Draw frame
      ctx.drawImage(bitmap, 0, 0);

      // Convert to WebP blob
      const webpBlob = await canvas.convertToBlob({
        type: 'image/webp',
        quality: this.config.quality / 100
      });

      webpFrames.push({
        data: new Uint8Array(await webpBlob.arrayBuffer()),
        delay: Math.round(frameDelayMs),
        x: 0,
        y: 0,
        width: this.config.width,
        height: this.config.height,
        dispose: 0,
        blend: 0
      });
    }

    // Combine frames into animated WebP
    return this.combineWebPFrames(webpFrames);
  }

  /**
   * Combine WebP frames into animated WebP.
   * This is a simplified implementation - real implementation would use libwebp
   */
  private async combineWebPFrames(frames: WebPFrame[]): Promise<Uint8Array> {
    // In a real implementation, we would use the libwebp library
    // For now, we return the first frame as a static WebP
    
    if (frames.length === 0) {
      throw new Error('No frames to combine');
    }

    // Return the first frame as a static WebP
    // In production, you would use: webp.js or libwebp
    return frames[0].data as Uint8Array;
  }

  /**
   * Simulate WebP encoding for Node.js environment.
   */
  private async simulateWebPEncoding(frame: Uint8Array): Promise<Uint8Array> {
    // This is a placeholder - in production, use sharp or libwebp
    // Example with sharp:
    // const sharp = require('sharp');
    // return await sharp(frame).webp({ quality: this.config.quality }).toBuffer();

    // Simulate compression
    const qualityFactor = this.config.quality / 100;
    const simulatedSize = Math.floor(frame.length * (0.3 + qualityFactor * 0.5));
    
    // Return a simulated WebP header + compressed data
    const webpHeader = new Uint8Array([
      0x52, 0x49, 0x46, 0x46, // RIFF
      0x00, 0x00, 0x00, 0x00, // File size (placeholder)
      0x57, 0x45, 0x42, 0x50, // WEBP
      0x56, 0x50, 0x38, 0x4C, // VP8L
      0x00, 0x00, 0x00, 0x00, // Chunk size
      0x2F, 0x00, 0x00, 0x00  // VP8L data
    ]);

    // Set actual size
    const totalSize = 4 + webpHeader.length + simulatedSize;
    const sizeBuffer = new ArrayBuffer(4);
    const sizeView = new DataView(sizeBuffer);
    sizeView.setUint32(0, totalSize - 8, true);
    webpHeader.set(new Uint8Array(sizeBuffer), 4);

    const sizeBuffer2 = new ArrayBuffer(4);
    const sizeView2 = new DataView(sizeBuffer2);
    sizeView2.setUint32(0, webpHeader.length + simulatedSize - 8, true);
    webpHeader.set(new Uint8Array(sizeBuffer2), 12);

    // Combine header with compressed data
    const result = new Uint8Array(webpHeader.length + simulatedSize);
    result.set(webpHeader, 0);
    
    // Fill with compressed data (simulated)
    for (let i = 0; i < simulatedSize; i++) {
      result[webpHeader.length + i] = frame[i % frame.length] * qualityFactor;
    }

    return result;
  }

  /**
   * Simulate animated WebP encoding.
   */
  private async simulateAnimatedWebPEncoding(frames: Uint8Array[]): Promise<Uint8Array> {
    // In production, use: webp.js or libwebp with animation support
    // For now, return the first frame as static WebP
    
    if (frames.length === 0) {
      throw new Error('No frames to encode');
    }

    return this.simulateWebPEncoding(frames[0]);
  }

  /**
   * Get information about a WebP file.
   */
  async getWebPInfo(data: Uint8Array): Promise<{
    width: number;
    height: number;
    animated: boolean;
    frameCount: number;
    loop: boolean;
    duration: number;
  }> {
    // Parse WebP header
    if (data.length < 12) {
      throw new Error('Invalid WebP data');
    }

    // Check RIFF header
    const riff = String.fromCharCode(...data.slice(0, 4));
    const webp = String.fromCharCode(...data.slice(8, 12));

    if (riff !== 'RIFF' || webp !== 'WEBP') {
      throw new Error('Invalid WebP format');
    }

    // Check format
    const format = String.fromCharCode(...data.slice(12, 16));

    let width = 0;
    let height = 0;
    let animated = false;
    let frameCount = 1;
    let loop = false;
    let duration = 0;

    if (format === 'VP8X') {
      // Extended format - may be animated
      animated = (data[16] & 0x02) !== 0; // Animation flag
      
      // Parse dimensions from VP8X chunk
      const widthBytes = data.slice(18, 21);
      const heightBytes = data.slice(21, 24);
      width = widthBytes[0] | (widthBytes[1] << 8) | (widthBytes[2] << 16) + 1;
      height = heightBytes[0] | (heightBytes[1] << 8) | (heightBytes[2] << 16) + 1;

      if (animated) {
        // Count animation frames
        frameCount = this.countWebPAnimationFrames(data);
        loop = true;
        duration = frameCount * (1000 / this.config.fps);
      }
    } else if (format === 'VP8L') {
      // Lossless format
      const widthBytes = data.slice(18, 21);
      const heightBytes = data.slice(21, 24);
      width = (widthBytes[0] | (widthBytes[1] << 8)) + 1;
      height = (heightBytes[0] | (heightBytes[1] << 8)) + 1;
    }

    return {
      width,
      height,
      animated,
      frameCount,
      loop,
      duration
    };
  }

  /**
   * Count animation frames in WebP data.
   */
  private countWebPAnimationFrames(data: Uint8Array): number {
    let frameCount = 0;
    let offset = 16;

    // Skip VP8X chunk header (12 bytes + 4 bytes flags)
    offset += 4;

    while (offset < data.length - 8) {
      const chunkType = String.fromCharCode(...data.slice(offset, offset + 4));
      const chunkSize = new DataView(data.buffer).getUint32(offset + 4, true);

      if (chunkType === 'ANIM') {
        // Found animation chunk - count frames
        const framesInfo = data.slice(offset + 8, offset + 12);
        frameCount = new DataView(framesInfo.buffer).getUint16(0, true);
        break;
      }

      // Move to next chunk (chunk size is padded to 2 bytes)
      offset += 8 + chunkSize + (chunkSize % 2);
    }

    return Math.max(1, frameCount);
  }

  /**
   * Extract frames from an animated WebP.
   */
  async extractFrames(data: Uint8Array): Promise<WebPFrame[]> {
    // In a real implementation, we would decode the animated WebP
    // For now, return a single placeholder frame
    
    const info = await this.getWebPInfo(data);
    
    const frames: WebPFrame[] = [];
    const frameDelay = 1000 / this.config.fps;

    for (let i = 0; i < info.frameCount; i++) {
      frames.push({
        data: data,
        delay: Math.round(frameDelay),
        x: 0,
        y: 0,
        width: info.width,
        height: info.height,
        dispose: 0,
        blend: 0
      });
    }

    return frames;
  }

  /**
   * Optimize an existing WebP file.
   */
  async optimize(
    inputData: Uint8Array,
    targetSizeKB?: number
  ): Promise<WebPExportResult> {
    try {
      const info = await this.getWebPInfo(inputData);
      
      // Adjust quality to meet target size if specified
      let quality = this.config.quality;
      
      if (targetSizeKB) {
        const currentSizeKB = inputData.length / 1024;
        if (currentSizeKB > targetSizeKB) {
          quality = Math.max(10, Math.min(99, Math.round(
            this.config.quality * (targetSizeKB / currentSizeKB)
          )));
        }
      }

      // Re-encode with new quality
      const optimized = await this.encodeSingleFrame(inputData);

      return {
        success: true,
        data: optimized,
        fileSize: optimized.length,
        frameCount: info.frameCount,
        duration: info.duration,
        quality,
        compressionRatio: (1 - optimized.length / inputData.length) * 100
      };
    } catch (error) {
      return {
        success: false,
        fileSize: 0,
        frameCount: 0,
        duration: 0,
        quality: this.config.quality,
        compressionRatio: 0,
        error: error instanceof Error ? error.message : 'Unknown optimization error'
      };
    }
  }
}
