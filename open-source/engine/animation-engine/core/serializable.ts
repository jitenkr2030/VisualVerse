/**
 * VisualVerse Animation Engine - Serializable Interface
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
 * Interface for objects that can be serialized and versioned.
 * Implement this interface to enable scene state tracking and versioning.
 */
export interface ISerializable {
  /**
   * Serialize the object to a JSON string representation.
   * This should capture all relevant state for reconstruction.
   */
  serialize(): string;

  /**
   * Get a unique hash fingerprint of the current state.
   * Used for caching and change detection.
   */
  getHash(): string;

  /**
   * Get the type identifier for deserialization.
   */
  getTypeId(): string;
}

/**
 * Represents a versioned snapshot of scene state.
 */
export interface VersionSnapshot {
  hash: string;
  timestamp: number;
  message: string;
  author: string;
  state: string;
  parentHash?: string;
  metadata: Record<string, unknown>;
}

/**
 * Configuration for serialization options.
 */
export interface SerializationConfig {
  includeMetadata: boolean;
  includeComputed: boolean;
  prettyPrint: boolean;
  excludeFields?: string[];
}

/**
 * Default serialization configuration.
 */
export const DEFAULT_SERIALIZATION_CONFIG: SerializationConfig = {
  includeMetadata: true,
  includeComputed: false,
  prettyPrint: false,
  excludeFields: []
};

/**
 * Result of a serialization operation.
 */
export interface SerializationResult {
  success: boolean;
  serialized: string;
  hash: string;
  size: number;
  error?: string;
}

/**
 * Result of a deserialization operation.
 */
export interface DeserializationResult<T extends ISerializable> {
  success: boolean;
  object?: T;
  hash: string;
  error?: string;
}

/**
 * Utility class for serialization operations.
 */
export class SerializationUtils {
  /**
   * Create a SHA-256 hash from a string.
   */
  static async createHash(data: string): Promise<string> {
    const encoder = new TextEncoder();
    const dataBuffer = encoder.encode(data);
    const hashBuffer = await crypto.subtle.digest('SHA-256', dataBuffer);
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
  }

  /**
   * Create a hash from a binary buffer.
   */
  static async createHashFromBuffer(buffer: ArrayBuffer): Promise<string> {
    const hashBuffer = await crypto.subtle.digest('SHA-256', buffer);
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
  }

  /**
   * Deep clone an object.
   */
  static deepClone<T>(obj: T): T {
    return JSON.parse(JSON.stringify(obj));
  }

  /**
   * Merge two objects deeply.
   */
  static deepMerge<T extends Record<string, unknown>>(target: T, source: Partial<T>): T {
    const result = { ...target };
    for (const key in source) {
      if (source[key] && typeof source[key] === 'object' && !Array.isArray(source[key])) {
        result[key] = this.deepMerge(
          result[key] as Record<string, unknown>,
          source[key] as Record<string, unknown>
        ) as T[Extract<keyof T, string>];
      } else {
        result[key] = source[key] as T[Extract<keyof T, string>];
      }
    }
    return result;
  }
}
