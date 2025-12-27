/**
 * VisualVerse Animation Engine - Render Cache Manager
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
 * Cache entry for a rendered frame.
 */
export interface CacheEntry {
  hash: string;
  frameIndex: number;
  timestamp: number;
  data: ArrayBuffer;
  metadata: CacheMetadata;
}

/**
 * Metadata for a cached frame.
 */
export interface CacheMetadata {
  width: number;
  height: number;
  format: string;
  quality: number;
  renderTime: number;
  hitCount: number;
  lastAccess: number;
}

/**
 * Configuration for the cache manager.
 */
export interface CacheConfig {
  maxMemorySize: number;      // Maximum memory cache size in bytes
  maxDiskSize: number;        // Maximum disk cache size in bytes
  maxEntries: number;         // Maximum number of cache entries
  cacheDir: string;           // Directory for disk cache
  enabled: boolean;           // Enable caching
  memoryWeight: number;       // Weight of memory cache (0-1)
  compressionEnabled: boolean; // Enable compression for disk cache
  ttlMinutes: number;         // Time to live in minutes
}

/**
 * Default cache configuration.
 */
export const DEFAULT_CACHE_CONFIG: CacheConfig = {
  maxMemorySize: 256 * 1024 * 1024,  // 256 MB
  maxDiskSize: 2 * 1024 * 1024 * 1024, // 2 GB
  maxEntries: 1000,
  cacheDir: './.visualverse/cache',
  enabled: true,
  memoryWeight: 0.3,  // 30% memory, 70% disk
  compressionEnabled: true,
  ttlMinutes: 60
};

/**
 * Result of a cache lookup operation.
 */
export interface CacheLookupResult {
  hit: boolean;
  entry?: CacheEntry;
  source: 'memory' | 'disk' | 'none';
  lookupTime: number;
}

/**
 * Result of a cache store operation.
 */
export interface CacheStoreResult {
  success: boolean;
  entry?: CacheEntry;
  evictedCount: number;
  error?: string;
}

/**
 * Statistics for the cache manager.
 */
export interface CacheStats {
  enabled: boolean;
  memoryUsed: number;
  memoryEntries: number;
  diskUsed: number;
  diskEntries: number;
  totalHits: number;
  totalMisses: number;
  hitRate: number;
  averageLookupTime: number;
  totalEvictions: number;
}

/**
 * Render Cache Manager for Optimized Frame Caching.
 * 
 * This class manages a two-tier cache (memory + disk) for rendered frames,
 * significantly improving performance for repeated renders.
 */
export class RenderCacheManager {
  private config: CacheConfig;
  private memoryCache: Map<string, CacheEntry>;
  private diskCacheDir: string;
  private stats: {
    totalHits: number;
    totalMisses: number;
    totalEvictions: number;
    lookupTimes: number[];
  };

  /**
   * Create a new RenderCacheManager.
   * 
   * @param config - Optional configuration for the cache
   */
  constructor(config?: Partial<CacheConfig>) {
    this.config = { ...DEFAULT_CACHE_CONFIG, ...config };
    this.memoryCache = new Map();
    this.diskCacheDir = this.config.cacheDir;
    this.stats = {
      totalHits: 0,
      totalMisses: 0,
      totalEvictions: 0,
      lookupTimes: []
    };

    this.initializeCache();
  }

  /**
   * Initialize the cache system.
   */
  private async initializeCache(): Promise<void> {
    if (!this.config.enabled) {
      return;
    }

    // Create cache directory if it doesn't exist
    try {
      const { mkdir } = await import('fs/promises');
      await mkdir(this.diskCacheDir, { recursive: true });
    } catch (error) {
      console.warn('Failed to create cache directory:', error);
    }
  }

  /**
   * Generate a cache key from render parameters.
   */
  generateCacheKey(params: {
    sceneHash: string;
    frameIndex: number;
    width: number;
    height: number;
    format: string;
    quality: number;
  }): string {
    const keyString = `${params.sceneHash}_${params.frameIndex}_${params.width}x${params.height}_${params.format}_q${params.quality}`;
    return this.hashString(keyString);
  }

  /**
   * Hash a string to create a cache key.
   */
  private async hashString(str: string): Promise<string> {
    const encoder = new TextEncoder();
    const data = encoder.encode(str);
    const hashBuffer = await crypto.subtle.digest('SHA-256', data);
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    return hashArray.slice(0, 16).map(b => b.toString(16).padStart(2, '0')).join('');
  }

  /**
   * Look up a frame in the cache.
   * 
   * @param key - Cache key to look up
   * @returns Result of the cache lookup
   */
  async lookup(key: string): Promise<CacheLookupResult> {
    const startTime = performance.now();

    if (!this.config.enabled) {
      return {
        hit: false,
        source: 'none',
        lookupTime: performance.now() - startTime
      };
    }

    // Check memory cache first
    const memoryEntry = this.memoryCache.get(key);
    if (memoryEntry) {
      // Update access metadata
      memoryEntry.metadata.lastAccess = Date.now();
      memoryEntry.metadata.hitCount++;

      this.stats.totalHits++;
      this.stats.lookupTimes.push(performance.now() - startTime);

      return {
        hit: true,
        entry: memoryEntry,
        source: 'memory',
        lookupTime: performance.now() - startTime
      };
    }

    // Check disk cache
    const diskEntry = await this.loadFromDisk(key);
    if (diskEntry) {
      // Move to memory cache (cache warming)
      this.memoryCache.set(key, diskEntry);
      diskEntry.metadata.lastAccess = Date.now();
      diskEntry.metadata.hitCount++;

      this.stats.totalHits++;
      this.stats.lookupTimes.push(performance.now() - startTime);

      return {
        hit: true,
        entry: diskEntry,
        source: 'disk',
        lookupTime: performance.now() - startTime
      };
    }

    this.stats.totalMisses++;
    return {
      hit: false,
      source: 'none',
      lookupTime: performance.now() - startTime
    };
  }

  /**
   * Store a frame in the cache.
   * 
   * @param key - Cache key
   * @param frameIndex - Frame index in the animation
   * @param data - Rendered frame data
   * @param metadata - Additional metadata
   * @returns Result of the store operation
   */
  async store(
    key: string,
    frameIndex: number,
    data: ArrayBuffer,
    metadata: Partial<CacheMetadata> = {}
  ): Promise<CacheStoreResult> {
    if (!this.config.enabled) {
      return { success: false, evictedCount: 0 };
    }

    const entry: CacheEntry = {
      hash: key,
      frameIndex,
      timestamp: Date.now(),
      data,
      metadata: {
        width: metadata.width || 1920,
        height: metadata.height || 1080,
        format: metadata.format || 'png',
        quality: metadata.quality || 90,
        renderTime: metadata.renderTime || 0,
        hitCount: 0,
        lastAccess: Date.now()
      }
    };

    try {
      // Check if we need to evict entries
      const memoryUsed = this.getMemoryUsage();
      if (memoryUsed > this.config.maxMemorySize * this.config.memoryWeight) {
        await this.evictMemoryCache(memoryUsed - this.config.maxMemorySize * this.config.memoryWeight * 0.8);
      }

      // Store in memory cache
      this.memoryCache.set(key, entry);

      // Store in disk cache (async)
      this.saveToDisk(key, entry).catch(error => {
        console.warn('Failed to save to disk cache:', error);
      });

      return {
        success: true,
        entry,
        evictedCount: 0
      };
    } catch (error) {
      return {
        success: false,
        evictedCount: 0,
        error: error instanceof Error ? error.message : 'Unknown error'
      };
    }
  }

  /**
   * Load an entry from disk cache.
   */
  private async loadFromDisk(key: string): Promise<CacheEntry | null> {
    try {
      const { readFile } = await import('fs/promises');
      const path = await import('path');
      const filePath = path.join(this.diskCacheDir, `${key}.cache`);

      const fileData = await readFile(filePath);
      
      // Parse the entry (first 4 bytes are entry size, rest is data)
      const entryData = JSON.parse(fileData.slice(4).toString());
      
      // Read the actual frame data
      const dataOffset = entryData.dataOffset || 0;
      const dataLength = entryData.dataLength || 0;
      const frameData = fileData.slice(4 + entryData.jsonLength, 4 + entryData.jsonLength + dataLength);

      return {
        ...entryData,
        data: frameData.buffer
      };
    } catch {
      return null;
    }
  }

  /**
   * Save an entry to disk cache.
   */
  private async saveToDisk(key: string, entry: CacheEntry): Promise<void> {
    try {
      const { writeFile } = await import('fs/promises');
      const path = await import('path');
      const filePath = path.join(this.diskCacheDir, `${key}.cache`);

      const jsonStr = JSON.stringify({
        hash: entry.hash,
        frameIndex: entry.frameIndex,
        timestamp: entry.timestamp,
        metadata: entry.metadata
      });
      
      const jsonBuffer = Buffer.from(jsonStr);
      const dataBuffer = Buffer.from(entry.data);
      
      // Format: [4 bytes size][json][data]
      const sizeBuffer = Buffer.alloc(4);
      sizeBuffer.writeUInt32LE(jsonBuffer.length + dataBuffer.length);

      await writeFile(filePath, Buffer.concat([sizeBuffer, jsonBuffer, dataBuffer]));
    } catch (error) {
      console.warn('Failed to save to disk cache:', error);
    }
  }

  /**
   * Get the current memory usage of the cache.
   */
  private getMemoryUsage(): number {
    let usage = 0;
    for (const entry of this.memoryCache.values()) {
      usage += entry.data.byteLength;
    }
    return usage;
  }

  /**
   * Evict entries from memory cache to free space.
   */
  private async evictMemoryCache(targetFreed: number): Promise<number> {
    let freed = 0;
    const entries = Array.from(this.memoryCache.entries())
      .sort((a, b) => a[1].metadata.lastAccess - b[1].metadata.lastAccess); // LRU

    for (const [key, entry] of entries) {
      if (freed >= targetFreed) {
        break;
      }

      // Move to disk before evicting
      await this.saveToDisk(key, entry);
      this.memoryCache.delete(key);
      freed += entry.data.byteLength;
      this.stats.totalEvictions++;
    }

    return freed;
  }

  /**
   * Invalidate cache entries matching a pattern.
   * 
   * @param pattern - Pattern to match (supports * wildcards)
   */
  async invalidate(pattern: string): Promise<number> {
    const regex = new RegExp('^' + pattern.replace(/\*/g, '.*') + '$');
    let invalidated = 0;

    for (const key of this.memoryCache.keys()) {
      if (regex.test(key)) {
        this.memoryCache.delete(key);
        invalidated++;
      }
    }

    // Also invalidate disk cache
    try {
      const { readdir, unlink } = await import('fs/promises');
      const path = await import('path');
      
      const files = await readdir(this.diskCacheDir);
      for (const file of files) {
        if (regex.test(file.replace('.cache', ''))) {
          await unlink(path.join(this.diskCacheDir, file));
          invalidated++;
        }
      }
    } catch {
      // Directory might not exist
    }

    return invalidated;
  }

  /**
   * Clear all cache entries.
   */
  async clear(): Promise<void> {
    this.memoryCache.clear();
    
    try {
      const { readdir, unlink, rmdir } = await import('fs/promises');
      const files = await readdir(this.diskCacheDir);
      
      for (const file of files) {
        await unlink(this.diskCacheDir + '/' + file);
      }
    } catch {
      // Directory might not exist
    }

    this.stats.totalHits = 0;
    this.stats.totalMisses = 0;
    this.stats.totalEvictions = 0;
    this.stats.lookupTimes = [];
  }

  /**
   * Get cache statistics.
   */
  getStats(): CacheStats {
    const totalRequests = this.stats.totalHits + this.stats.totalMisses;
    const avgLookupTime = this.stats.lookupTimes.length > 0
      ? this.stats.lookupTimes.reduce((a, b) => a + b, 0) / this.stats.lookupTimes.length
      : 0;

    return {
      enabled: this.config.enabled,
      memoryUsed: this.getMemoryUsage(),
      memoryEntries: this.memoryCache.size,
      diskUsed: 0, // Would need filesystem query
      diskEntries: 0,
      totalHits: this.stats.totalHits,
      totalMisses: this.stats.totalMisses,
      hitRate: totalRequests > 0 ? this.stats.totalHits / totalRequests : 0,
      averageLookupTime: avgLookupTime,
      totalEvictions: this.stats.totalEvictions
    };
  }

  /**
   * Preload frames into cache for faster first playback.
   * 
   * @param keys - Array of cache keys to preload
   */
  async preload(keys: string[]): Promise<void> {
    for (const key of keys) {
      if (!this.memoryCache.has(key)) {
        const result = await this.lookup(key);
        if (!result.hit) {
          // Mark for future preload if data becomes available
        }
      }
    }
  }

  /**
   * Get the hit rate for a specific time window.
   * 
   * @param windowMinutes - Time window in minutes
   */
  getHitRate(windowMinutes?: number): number {
    const totalRequests = this.stats.totalHits + this.stats.totalMisses;
    if (totalRequests === 0) return 0;
    return this.stats.totalHits / totalRequests;
  }

  /**
   * Dispose of the cache manager.
   */
  async dispose(): Promise<void> {
    await this.clear();
  }
}
