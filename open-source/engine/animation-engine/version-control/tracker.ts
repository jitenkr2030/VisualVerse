/**
 * VisualVerse Animation Engine - Version Control Tracker
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

import { ISerializable, VersionSnapshot, SerializationUtils } from '../core/serializable';

/**
 * Change types that can be tracked in a scene.
 */
export enum ChangeType {
  OBJECT_ADDED = 'object_added',
  OBJECT_REMOVED = 'object_removed',
  OBJECT_MODIFIED = 'object_modified',
  PROPERTY_CHANGED = 'property_changed',
  ANIMATION_ADDED = 'animation_added',
  ANIMATION_REMOVED = 'animation_removed',
  TIMELINE_MODIFIED = 'timeline_modified',
  METADATA_CHANGED = 'metadata_changed'
}

/**
 * Represents a single change in the scene.
 */
export interface SceneChange {
  type: ChangeType;
  timestamp: number;
  objectId?: string;
  property?: string;
  oldValue?: unknown;
  newValue?: unknown;
  description: string;
}

/**
 * Result of a commit operation.
 */
export interface CommitResult {
  success: boolean;
  commitHash: string;
  snapshot?: VersionSnapshot;
  error?: string;
}

/**
 * Result of a checkout operation.
 */
export interface CheckoutResult {
  success: boolean;
  snapshot?: VersionSnapshot;
  error?: string;
}

/**
 * Result of comparing two versions.
 */
export interface CompareResult {
  success: boolean;
  hasChanges: boolean;
  changes: SceneChange[];
  hashA: string;
  hashB: string;
  commonAncestor?: string;
  changeSummary: {
    added: number;
    removed: number;
    modified: number;
  };
}

/**
 * Status of the working directory relative to the last commit.
 */
export interface WorkingDirectoryStatus {
  clean: boolean;
  currentHash: string;
  stagedHash?: string;
  uncommittedChanges: SceneChange[];
  pendingDeletions: string[];
  pendingAdditions: string[];
}

/**
 * Configuration for the version control tracker.
 */
export interface VersionControlConfig {
  storagePath: string;
  maxSnapshots: number;
  enableAutoSave: boolean;
  autoSaveIntervalMs: number;
  authorName: string;
  authorEmail: string;
}

/**
 * Default version control configuration.
 */
export const DEFAULT_VERSION_CONTROL_CONFIG: VersionControlConfig = {
  storagePath: './.visualverse/vcs',
  maxSnapshots: 100,
  enableAutoSave: false,
  autoSaveIntervalMs: 30000,
  authorName: 'Anonymous',
  authorEmail: 'anonymous@visualverse.io'
};

/**
 * Version Control Tracker for Scene State Management.
 * 
 * This class provides git-like functionality for tracking changes in scenes,
 * enabling versioning, history navigation, and change comparison.
 */
export class VersionControlTracker {
  private snapshots: Map<string, VersionSnapshot>;
  private currentSnapshot?: VersionSnapshot;
  private scene: ISerializable;
  private config: VersionControlConfig;
  private changeHistory: SceneChange[];
  private autoSaveInterval?: ReturnType<typeof setInterval>;

  /**
   * Create a new VersionControlTracker.
   * 
   * @param scene - The scene object to track (must implement ISerializable)
   * @param config - Optional configuration for the tracker
   */
  constructor(scene: ISerializable, config?: Partial<VersionControlConfig>) {
    this.scene = scene;
    this.config = { ...DEFAULT_VERSION_CONTROL_CONFIG, ...config };
    this.snapshots = new Map();
    this.changeHistory = [];
    this.loadSnapshots();
    
    // Initialize with current state
    this.initializeCurrentState();
  }

  /**
   * Initialize tracking from the current scene state.
   */
  private async initializeCurrentState(): Promise<void> {
    const hash = await this.scene.getHash();
    this.currentSnapshot = {
      hash,
      timestamp: Date.now(),
      message: 'Initial state',
      author: this.config.authorName,
      state: this.scene.serialize(),
      metadata: {}
    };
  }

  /**
   * Load existing snapshots from storage.
   */
  private loadSnapshots(): void {
    // In a real implementation, this would read from the file system
    // For now, we initialize an empty storage
    this.snapshots.clear();
  }

  /**
   * Save snapshots to storage.
   */
  private saveSnapshots(): void {
    // In a real implementation, this would write to the file system
    // The storage path is: {storagePath}/snapshots/
  }

  /**
   * Create a commit of the current scene state.
   * 
   * @param message - Description of the changes
   * @returns Result of the commit operation
   */
  async commit(message: string): Promise<CommitResult> {
    try {
      const state = this.scene.serialize();
      const hash = await this.scene.getHash();
      
      // Check if there are actual changes
      if (this.currentSnapshot && hash === this.currentSnapshot.hash) {
        return {
          success: false,
          commitHash: hash,
          error: 'No changes to commit'
        };
      }

      const snapshot: VersionSnapshot = {
        hash,
        timestamp: Date.now(),
        message,
        author: this.config.authorName,
        state,
        parentHash: this.currentSnapshot?.hash,
        metadata: {
          email: this.config.authorEmail,
          changes: this.changeHistory.length
        }
      };

      this.snapshots.set(hash, snapshot);
      this.currentSnapshot = snapshot;
      this.changeHistory = [];
      this.saveSnapshots();

      return {
        success: true,
        commitHash: hash,
        snapshot
      };
    } catch (error) {
      return {
        success: false,
        commitHash: '',
        error: error instanceof Error ? error.message : 'Unknown error during commit'
      };
    }
  }

  /**
   * Checkout a previous version of the scene.
   * 
   * @param commitHash - Hash of the commit to checkout
   * @returns Result of the checkout operation
   */
  async checkout(commitHash: string): Promise<CheckoutResult> {
    try {
      const snapshot = this.snapshots.get(commitHash);
      
      if (!snapshot) {
        return {
          success: false,
          error: `Commit ${commitHash} not found`
        };
      }

      // In a real implementation, this would deserialize and apply the snapshot
      this.currentSnapshot = snapshot;
      this.changeHistory = [];

      return {
        success: true,
        snapshot
      };
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Unknown error during checkout'
      };
    }
  }

  /**
   * Get the history of commits.
   * 
   * @param limit - Maximum number of commits to return
   * @returns Array of version snapshots
   */
  getHistory(limit: number = 50): VersionSnapshot[] {
    const snapshots = Array.from(this.snapshots.values());
    return snapshots
      .sort((a, b) => b.timestamp - a.timestamp)
      .slice(0, limit);
  }

  /**
   * Compare two versions of the scene.
   * 
   * @param hashA - First version hash
   * @param hashB - Second version hash
   * @returns Comparison result
   */
  async compare(hashA: string, hashB: string): Promise<CompareResult> {
    try {
      const snapshotA = this.snapshots.get(hashA);
      const snapshotB = this.snapshots.get(hashB);

      if (!snapshotA || !snapshotB) {
        return {
          success: false,
          hasChanges: false,
          changes: [],
          hashA,
          hashB,
          changeSummary: { added: 0, removed: 0, modified: 0 },
          error: 'One or both commits not found'
        };
      }

      // Parse the states
      const stateA = JSON.parse(snapshotA.state);
      const stateB = JSON.parse(snapshotB.state);

      // Compare states and collect changes
      const changes = this.diffStates(stateA, stateB);

      // Calculate change summary
      const summary = {
        added: changes.filter(c => c.type === ChangeType.OBJECT_ADDED || c.type === ChangeType.ANIMATION_ADDED).length,
        removed: changes.filter(c => c.type === ChangeType.OBJECT_REMOVED || c.type === ChangeType.ANIMATION_REMOVED).length,
        modified: changes.filter(c => c.type === ChangeType.OBJECT_MODIFIED || c.type === ChangeType.PROPERTY_CHANGED).length
      };

      return {
        success: true,
        hasChanges: changes.length > 0,
        changes,
        hashA,
        hashB,
        changeSummary: summary
      };
    } catch (error) {
      return {
        success: false,
        hasChanges: false,
        changes: [],
        hashA,
        hashB,
        changeSummary: { added: 0, removed: 0, modified: 0 },
        error: error instanceof Error ? error.message : 'Unknown error during comparison'
      };
    }
  }

  /**
   * Diff two state objects and return the changes.
   */
  private diffStates(stateA: Record<string, unknown>, stateB: Record<string, unknown>): SceneChange[] {
    const changes: SceneChange[] = [];

    // Check for modified or new properties
    for (const key in stateB) {
      if (!(key in stateA)) {
        changes.push({
          type: ChangeType.PROPERTY_CHANGED,
          timestamp: Date.now(),
          property: key,
          newValue: stateB[key],
          description: `Property '${key}' was added`
        });
      } else if (JSON.stringify(stateA[key]) !== JSON.stringify(stateB[key])) {
        changes.push({
          type: ChangeType.PROPERTY_CHANGED,
          timestamp: Date.now(),
          property: key,
          oldValue: stateA[key],
          newValue: stateB[key],
          description: `Property '${key}' was modified`
        });
      }
    }

    // Check for removed properties
    for (const key in stateA) {
      if (!(key in stateB)) {
        changes.push({
          type: ChangeType.PROPERTY_CHANGED,
          timestamp: Date.now(),
          property: key,
          oldValue: stateA[key],
          description: `Property '${key}' was removed`
        });
      }
    }

    return changes;
  }

  /**
   * Get the current status of the working directory.
   */
  async getStatus(): Promise<WorkingDirectoryStatus> {
    const currentHash = await this.scene.getHash();
    const isClean = this.currentSnapshot && currentHash === this.currentSnapshot.hash;

    return {
      clean: isClean,
      currentHash,
      uncommittedChanges: [...this.changeHistory],
      pendingDeletions: [],
      pendingAdditions: []
    };
  }

  /**
   * Record a change to the scene.
   */
  recordChange(change: SceneChange): void {
    this.changeHistory.push(change);
  }

  /**
   * Get the current commit hash.
   */
  async getCurrentHash(): Promise<string> {
    return await this.scene.getHash();
  }

  /**
   * Start auto-save functionality.
   */
  startAutoSave(): void {
    if (this.config.enableAutoSave) {
      this.autoSaveInterval = setInterval(async () => {
        await this.commit('Auto-save');
      }, this.config.autoSaveIntervalMs);
    }
  }

  /**
   * Stop auto-save functionality.
   */
  stopAutoSave(): void {
    if (this.autoSaveInterval) {
      clearInterval(this.autoSaveInterval);
      this.autoSaveInterval = undefined;
    }
  }

  /**
   * Get a specific snapshot by hash.
   */
  getSnapshot(hash: string): VersionSnapshot | undefined {
    return this.snapshots.get(hash);
  }

  /**
   * Get the number of snapshots.
   */
  getSnapshotCount(): number {
    return this.snapshots.size;
  }
}
