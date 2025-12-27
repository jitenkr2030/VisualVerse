/**
 * VisualVerse Animation Engine - Render Pool
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

import { parentPort, workerData, isMainThread } from 'worker_threads';
import * as path from 'path';
import * as fs from 'fs/promises';

/**
 * Configuration for the render pool.
 */
export interface RenderPoolConfig {
  workerCount: number;
  maxQueueSize: number;
  taskTimeout: number;
  enableGpu: boolean;
  gpuDeviceId: number;
  memoryLimit: number;
  prioritySupport: boolean;
}

/**
 * Default render pool configuration.
 */
export const DEFAULT_RENDER_POOL_CONFIG: RenderPoolConfig = {
  workerCount: 4,
  maxQueueSize: 100,
  taskTimeout: 60000, // 60 seconds
  enableGpu: false,
  gpuDeviceId: 0,
  memoryLimit: 1024 * 1024 * 1024, // 1 GB
  prioritySupport: true
};

/**
 * Task priority levels.
 */
export enum TaskPriority {
  LOW = 0,
  NORMAL = 1,
  HIGH = 2,
  CRITICAL = 3
}

/**
 * Status of a render task.
 */
export enum RenderTaskStatus {
  PENDING = 'pending',
  PROCESSING = 'processing',
  COMPLETED = 'completed',
  FAILED = 'failed',
  CANCELLED = 'cancelled',
  TIMEOUT = 'timeout'
}

/**
 * Render task definition.
 */
export interface RenderTask {
  id: string;
  frameIndex: number;
  sceneData: string;
  parameters: RenderParameters;
  priority: TaskPriority;
  status: RenderTaskStatus;
  createdAt: number;
  startedAt?: number;
  completedAt?: number;
  result?: RenderResult;
  error?: string;
}

/**
 * Parameters for rendering a frame.
 */
export interface RenderParameters {
  width: number;
  height: number;
  quality: number;
  format: string;
  backgroundColor: string;
  transparent: boolean;
  dependencies?: string[];
}

/**
 * Result of a frame render operation.
 */
export interface RenderResult {
  frameIndex: number;
  data: ArrayBuffer;
  format: string;
  size: number;
  renderTime: number;
}

/**
 * Statistics for the render pool.
 */
export interface RenderPoolStats {
  totalWorkers: number;
  activeWorkers: number;
  queuedTasks: number;
  completedTasks: number;
  failedTasks: number;
  averageRenderTime: number;
  throughput: number; // frames per second
  queueWaitTime: number;
  utilization: number;
}

/**
 * Callback for task completion.
 */
export type TaskCallback = (task: RenderTask) => void;

/**
 * Render Pool for Parallel Frame Processing.
 * 
 * This class manages a pool of worker threads for parallel rendering
 * of animation frames, significantly improving performance for long animations.
 */
export class RenderPool {
  private config: RenderPoolConfig;
  private workers: Worker[];
  private taskQueue: RenderTask[];
  private completedTasks: Map<string, RenderTask>;
  private stats: {
    completedCount: number;
    failedCount: number;
    renderTimes: number[];
    queueWaitTimes: number[];
    activeTaskCount: number;
  };
  private callbacks: Map<RenderTaskStatus, Set<TaskCallback>>;
  private isRunning: boolean;
  private workerIdleTime: number[];

  /**
   * Create a new RenderPool.
   * 
   * @param config - Optional configuration for the pool
   */
  constructor(config?: Partial<RenderPoolConfig>) {
    this.config = { ...DEFAULT_RENDER_POOL_CONFIG, ...config };
    this.workers = [];
    this.taskQueue = [];
    this.completedTasks = new Map();
    this.stats = {
      completedCount: 0,
      failedCount: 0,
      renderTimes: [],
      queueWaitTimes: [],
      activeTaskCount: 0
    };
    this.callbacks = new Map();
    this.isRunning = false;
    this.workerIdleTime = [];

    this.setupCallbacks();
  }

  /**
   * Initialize the worker pool.
   */
  async initialize(): Promise<void> {
    if (!isMainThread) {
      // This is a worker thread
      this.setupWorker();
      return;
    }

    this.workers = [];
    this.workerIdleTime = new Array(this.config.workerCount).fill(0);

    for (let i = 0; i < this.config.workerCount; i++) {
      const worker = new Worker(path.join(__dirname, 'worker.js'), {
        workerData: { workerId: i }
      });

      worker.on('message', (result) => this.handleWorkerMessage(i, worker, result));
      worker.on('error', (error) => this.handleWorkerError(i, worker, error));
      worker.on('exit', (code) => this.handleWorkerExit(i, code));

      this.workers.push(worker);
    }

    this.isRunning = true;
  }

  /**
   * Setup the worker thread message handling.
   */
  private setupWorker(): void {
    if (isMainThread) return;

    parentPort?.on('message', async (task: RenderTask) => {
      try {
        const result = await this.renderFrame(task);
        parentPort?.postMessage({
          type: 'complete',
          taskId: task.id,
          result
        });
      } catch (error) {
        parentPort?.postMessage({
          type: 'error',
          taskId: task.id,
          error: error instanceof Error ? error.message : 'Unknown error'
        });
      }
    });

    parentPort?.postMessage({ type: 'ready' });
  }

  /**
   * Handle messages from worker threads.
   */
  private handleWorkerMessage(workerId: number, worker: Worker, message: {
    type: string;
    taskId?: string;
    result?: RenderResult;
    error?: string;
  }): void {
    switch (message.type) {
      case 'complete':
        if (message.taskId) {
          this.completeTask(message.taskId, message.result);
        }
        this.stats.activeTaskCount--;
        this.workerIdleTime[workerId] = Date.now();
        break;

      case 'error':
        if (message.taskId) {
          this.failTask(message.taskId, message.error);
        }
        this.stats.activeTaskCount--;
        this.workerIdleTime[workerId] = Date.now();
        break;

      case 'ready':
        // Worker is ready for tasks
        break;
    }
  }

  /**
   * Handle errors from worker threads.
   */
  private handleWorkerError(workerId: number, worker: Worker, error: Error): void {
    console.error(`Worker ${workerId} error:`, error);
  }

  /**
   * Handle worker thread exit.
   */
  private handleWorkerExit(workerId: number, code: number): void {
    console.error(`Worker ${workerId} exited with code ${code}`);
    // In a production system, we would restart the worker
  }

  /**
   * Queue a render task.
   * 
   * @param task - Task to queue
   * @returns Whether the task was queued successfully
   */
  queueTask(task: RenderTask): boolean {
    if (this.taskQueue.length >= this.config.maxQueueSize) {
      return false;
    }

    // Add to queue
    task.status = RenderTaskStatus.PENDING;
    task.createdAt = Date.now();
    this.taskQueue.push(task);

    // Sort by priority (highest first)
    this.taskQueue.sort((a, b) => b.priority - a.priority);

    // Try to assign to worker
    this.assignTasks();

    return true;
  }

  /**
   * Queue multiple render tasks.
   * 
   * @param tasks - Tasks to queue
   * @returns Number of tasks successfully queued
   */
  queueTasks(tasks: RenderTask[]): number {
    let queued = 0;
    for (const task of tasks) {
      if (this.queueTask(task)) {
        queued++;
      } else {
        break;
      }
    }
    return queued;
  }

  /**
   * Assign pending tasks to available workers.
   */
  private assignTasks(): void {
    const idleWorkers = this.workerIdleTime.map((time, i) => ({ time, i }))
      .filter(({ time }) => Date.now() - time > 100) // Worker has been idle for 100ms
      .map(({ i }) => i);

    for (const workerId of idleWorkers) {
      if (this.taskQueue.length === 0) break;

      // Find highest priority task
      const taskIndex = this.taskQueue.findIndex(t => t.status === RenderTaskStatus.PENDING);
      if (taskIndex === -1) break;

      const task = this.taskQueue[taskIndex];
      task.status = RenderTaskStatus.PROCESSING;
      task.startedAt = Date.now();
      this.taskQueue.splice(taskIndex, 1);
      this.stats.activeTaskCount++;

      // Send to worker
      this.workers[workerId].postMessage(task);
      this.workerIdleTime[workerId] = 0;
    }
  }

  /**
   * Complete a render task.
   */
  private completeTask(taskId: string, result?: RenderResult): void {
    const task = this.findTask(taskId);
    if (!task) return;

    task.status = RenderTaskStatus.COMPLETED;
    task.completedAt = Date.now();
    task.result = result;

    if (result) {
      this.stats.renderTimes.push(result.renderTime);
      this.stats.completedCount++;
    }

    // Record queue wait time
    if (task.startedAt && task.createdAt) {
      this.stats.queueWaitTimes.push(task.startedAt - task.createdAt);
    }

    this.completedTasks.set(taskId, task);
    this.notifyCallbacks(RenderTaskStatus.COMPLETED, task);

    // Try to assign more tasks
    this.assignTasks();
  }

  /**
   * Fail a render task.
   */
  private failTask(taskId: string, error?: string): void {
    const task = this.findTask(taskId);
    if (!task) return;

    task.status = RenderTaskStatus.FAILED;
    task.completedAt = Date.now();
    task.error = error;

    this.stats.failedCount++;
    this.completedTasks.set(taskId, task);
    this.notifyCallbacks(RenderTaskStatus.FAILED, task);

    // Try to assign more tasks
    this.assignTasks();
  }

  /**
   * Find a task by ID.
   */
  private findTask(taskId: string): RenderTask | undefined {
    // Check pending queue
    for (const task of this.taskQueue) {
      if (task.id === taskId) return task;
    }

    // Check completed map
    return this.completedTasks.get(taskId);
  }

  /**
   * Cancel a pending task.
   * 
   * @param taskId - ID of the task to cancel
   * @returns Whether the task was cancelled
   */
  cancelTask(taskId: string): boolean {
    const task = this.findTask(taskId);
    if (!task || task.status !== RenderTaskStatus.PENDING) {
      return false;
    }

    task.status = RenderTaskStatus.CANCELLED;
    this.notifyCallbacks(RenderTaskStatus.CANCELLED, task);

    // Remove from queue
    const index = this.taskQueue.indexOf(task);
    if (index !== -1) {
      this.taskQueue.splice(index, 1);
    }

    return true;
  }

  /**
   * Wait for all tasks to complete.
   * 
   * @param timeout - Maximum time to wait in milliseconds
   * @returns Whether all tasks completed within the timeout
   */
  async waitForCompletion(timeout?: number): Promise<boolean> {
    const startTime = Date.now();
    const timeoutMs = timeout || Infinity;

    while (this.taskQueue.length > 0 || this.stats.activeTaskCount > 0) {
      if (Date.now() - startTime > timeoutMs) {
        return false;
      }

      await this.sleep(100);
    }

    return true;
  }

  /**
   * Get pending tasks.
   */
  getPendingTasks(): RenderTask[] {
    return this.taskQueue.filter(t => t.status === RenderTaskStatus.PENDING);
  }

  /**
   * Get completed tasks.
   */
  getCompletedTasks(): RenderTask[] {
    return Array.from(this.completedTasks.values());
  }

  /**
   * Get pool statistics.
   */
  getStats(): RenderPoolStats {
    const avgRenderTime = this.stats.renderTimes.length > 0
      ? this.stats.renderTimes.reduce((a, b) => a + b, 0) / this.stats.renderTimes.length
      : 0;

    const avgQueueWaitTime = this.stats.queueWaitTimes.length > 0
      ? this.stats.queueWaitTimes.reduce((a, b) => a + b, 0) / this.stats.queueWaitTimes.length
      : 0;

    const totalTasks = this.stats.completedCount + this.stats.failedCount;
    const utilization = totalTasks > 0
      ? this.stats.activeTaskCount / this.workers.length
      : 0;

    return {
      totalWorkers: this.workers.length,
      activeWorkers: this.stats.activeTaskCount,
      queuedTasks: this.taskQueue.length,
      completedTasks: this.stats.completedCount,
      failedTasks: this.stats.failedCount,
      averageRenderTime: avgRenderTime,
      throughput: totalTasks > 0 ? totalTasks / (avgRenderTime / 1000) : 0,
      queueWaitTime: avgQueueWaitTime,
      utilization
    };
  }

  /**
   * Register a callback for task events.
   * 
   * @param status - Task status to listen for
   * @param callback - Callback function
   */
  on(status: RenderTaskStatus, callback: TaskCallback): void {
    if (!this.callbacks.has(status)) {
      this.callbacks.set(status, new Set());
    }
    this.callbacks.get(status)!.add(callback);
  }

  /**
   * Remove a callback.
   * 
   * @param status - Task status
   * @param callback - Callback to remove
   */
  off(status: RenderTaskStatus, callback: TaskCallback): void {
    this.callbacks.get(status)?.delete(callback);
  }

  /**
   * Setup default callbacks.
   */
  private setupCallbacks(): void {
    // Initialize empty callback sets
    const statuses = Object.values(RenderTaskStatus);
    for (const status of statuses) {
      this.callbacks.set(status, new Set());
    }
  }

  /**
   * Notify all callbacks for a task status.
   */
  private notifyCallbacks(status: RenderTaskStatus, task: RenderTask): void {
    this.callbacks.get(status)?.forEach(callback => {
      try {
        callback(task);
      } catch (error) {
        console.error(`Error in callback for ${status}:`, error);
      }
    });
  }

  /**
   * Sleep for a specified duration.
   */
  private sleep(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  /**
   * Render a frame (executed in worker).
   */
  private async renderFrame(task: RenderTask): Promise<RenderResult> {
    const startTime = Date.now();

    // Parse scene data
    const sceneData = JSON.parse(task.sceneData);

    // In a real implementation, this would use the rendering engine
    // For now, we simulate rendering
    await this.sleep(50 + Math.random() * 100);

    const renderTime = Date.now() - startTime;

    return {
      frameIndex: task.frameIndex,
      data: new ArrayBuffer(1024), // Placeholder
      format: task.parameters.format,
      size: 1024,
      renderTime
    };
  }

  /**
   * Shutdown the render pool.
   */
  async shutdown(): Promise<void> {
    this.isRunning = false;

    // Cancel all pending tasks
    for (const task of this.taskQueue) {
      task.status = RenderTaskStatus.CANCELLED;
    }
    this.taskQueue = [];

    // Terminate all workers
    for (const worker of this.workers) {
      worker.terminate();
    }
    this.workers = [];
  }
}

/**
 * Utility function to create a render task.
 */
export function createRenderTask(
  id: string,
  frameIndex: number,
  sceneData: string,
  parameters: RenderParameters,
  priority: TaskPriority = TaskPriority.NORMAL
): RenderTask {
  return {
    id,
    frameIndex,
    sceneData,
    parameters,
    priority,
    status: RenderTaskStatus.PENDING,
    createdAt: Date.now()
  };
}
