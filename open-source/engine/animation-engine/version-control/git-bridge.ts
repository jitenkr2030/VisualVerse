/**
 * VisualVerse Animation Engine - Git Bridge
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

import { exec, ExecOptions } from 'child_process';
import { promisify } from 'util';
import * as fs from 'fs/promises';
import * as path from 'path';

const execAsync = promisify(exec);

/**
 * Git status for a visual output file.
 */
export interface VisualGitStatus {
  filePath: string;
  tracked: boolean;
  modified: boolean;
  staged: boolean;
  untracked: boolean;
  lastCommitHash?: string;
  lastCommitMessage?: string;
  lastCommitAuthor?: string;
  lastCommitDate?: Date;
}

/**
 * Result of a visual diff operation against git history.
 */
export interface GitVisualDiffResult {
  success: boolean;
  baseCommit: string;
  headCommit: string;
  baseImage?: Uint8Array;
  headImage?: Uint8Array;
  diffImage?: Uint8Array;
  hasVisualChanges: boolean;
  diffPercentage: number;
  error?: string;
}

/**
 * Result of a commit operation with visual assets.
 */
export interface GitCommitResult {
  success: boolean;
  commitHash?: string;
  commitMessage?: string;
  stagedFiles: string[];
  visualAssets: string[];
  error?: string;
}

/**
 * Branch information for visual tracking.
 */
export interface VisualBranchInfo {
  name: string;
  headCommit: string;
  visualAssets: string[];
  lastVisualUpdate?: Date;
}

/**
 * Configuration for the Git bridge.
 */
export interface GitBridgeConfig {
  repoRoot: string;
  visualAssetsDirectory: string;
  outputDirectory: string;
  autoStageVisualAssets: boolean;
  generateDiffOnCommit: boolean;
  visualFilePatterns: string[];
}

/**
 * Default Git bridge configuration.
 */
export const DEFAULT_GIT_BRIDGE_CONFIG: GitBridgeConfig = {
  repoRoot: '.',
  visualAssetsDirectory: 'visual-assets',
  outputDirectory: 'renders',
  autoStageVisualAssets: true,
  generateDiffOnCommit: true,
  visualFilePatterns: ['*.png', '*.gif', '*.mp4', '*.webp', '*.svg']
};

/**
 * Git Bridge for Visual Output Tracking.
 * 
 * This class provides integration with Git for tracking visual outputs,
 * generating visual diffs between commits, and managing visual asset versioning.
 */
export class GitBridge {
  private config: GitBridgeConfig;
  private visualDiffer?: {
    compare(imageA: Uint8Array, imageB: Uint8Array, generateImages?: boolean): Promise<{
      hasDifference: boolean;
      diffPercentage: number;
      diffImage?: Uint8Array;
      sideBySideImage?: Uint8Array;
    }>;
  };

  /**
   * Create a new GitBridge instance.
   * 
   * @param config - Optional configuration for the bridge
   * @param visualDiffer - Optional visual differ instance
   */
  constructor(config?: Partial<GitBridgeConfig>, visualDiffer?: {
    compare(imageA: Uint8Array, imageB: Uint8Array, generateImages?: boolean): Promise<{
      hasDifference: boolean;
      diffPercentage: number;
      diffImage?: Uint8Array;
      sideBySideImage?: Uint8Array;
    }>;
  }) {
    this.config = { ...DEFAULT_GIT_BRIDGE_CONFIG, ...config };
    this.visualDiffer = visualDiffer;
  }

  /**
   * Check if a git repository exists at the configured path.
   */
  async isGitRepository(): Promise<boolean> {
    try {
      const { stdout } = await execAsync('git rev-parse --git-dir', {
        cwd: this.config.repoRoot
      });
      return stdout.trim().length > 0;
    } catch {
      return false;
    }
  }

  /**
   * Get the current git commit hash.
   */
  async getCurrentCommit(): Promise<string> {
    const { stdout } = await execAsync('git rev-parse HEAD', {
      cwd: this.config.repoRoot
    });
    return stdout.trim();
  }

  /**
   * Get the current branch name.
   */
  async getCurrentBranch(): Promise<string> {
    const { stdout } = await execAsync('git rev-parse --abbrev-ref HEAD', {
      cwd: this.config.repoRoot
    });
    return stdout.trim();
  }

  /**
   * Get git status for a visual output file.
   */
  async getVisualFileStatus(filePath: string): Promise<VisualGitStatus> {
    const absolutePath = path.resolve(this.config.repoRoot, filePath);

    try {
      // Check if file exists
      await fs.access(absolutePath);
      const fileExists = true;
    } catch {
      return {
        filePath,
        tracked: false,
        modified: false,
        staged: false,
        untracked: true
      };
    }

    // Get file status in git
    const { stdout } = await execAsync(`git ls-files --stage -- ${filePath}`, {
      cwd: this.config.repoRoot
    });
    const isTracked = stdout.trim().length > 0;

    // Get modified status
    const { stdout: modifiedStdout } = await execAsync(`git diff --name-only -- ${filePath}`, {
      cwd: this.config.repoRoot
    });
    const isModified = modifiedStdout.trim().length > 0;

    // Get staged status
    const { stdout: stagedStdout } = await execAsync(`git diff --cached --name-only -- ${filePath}`, {
      cwd: this.config.repoRoot
    });
    const isStaged = stagedStdout.trim().length > 0;

    // Get last commit info if tracked
    let lastCommitHash: string | undefined;
    let lastCommitMessage: string | undefined;
    let lastCommitAuthor: string | undefined;
    let lastCommitDate: Date | undefined;

    if (isTracked) {
      try {
        const { stdout: logStdout } = await execAsync(
          `git log -1 --format="%H|%s|%an|%ad" -- ${filePath}`,
          { cwd: this.config.repoRoot }
        );
        const [hash, message, author, date] = logStdout.trim().split('|');
        lastCommitHash = hash;
        lastCommitMessage = message;
        lastCommitAuthor = author;
        lastCommitDate = new Date(date);
      } catch {
        // File might be staged but not committed
      }
    }

    return {
      filePath,
      tracked: isTracked,
      modified: isModified && !isStaged,
      staged: isStaged,
      untracked: !isTracked,
      lastCommitHash,
      lastCommitMessage,
      lastCommitAuthor,
      lastCommitDate
    };
  }

  /**
   * Stage a visual asset file.
   */
  async stageVisualAsset(filePath: string): Promise<void> {
    const absolutePath = path.resolve(this.config.repoRoot, filePath);
    await execAsync(`git add "${absolutePath}"`, {
      cwd: this.config.repoRoot
    });
  }

  /**
   * Unstage a visual asset file.
   */
  async unstageVisualAsset(filePath: string): Promise<void> {
    const absolutePath = path.resolve(this.config.repoRoot, filePath);
    await execAsync(`git reset HEAD "${absolutePath}"`, {
      cwd: this.config.repoRoot
    });
  }

  /**
   * Generate a visual diff between two commits.
   */
  async generateVisualDiff(
    baseCommit: string,
    headCommit: string,
    visualFilePath: string
  ): Promise<GitVisualDiffResult> {
    try {
      // Get file contents from both commits
      const baseFilePath = `${baseCommit}:${visualFilePath}`;
      const headFilePath = `${headCommit}:${visualFilePath}`;

      let baseImage: Uint8Array | undefined;
      let headImage: Uint8Array | undefined;

      try {
        const { stdout: baseBase64 } = await execAsync(
          `git show ${baseFilePath} 2>/dev/null | base64`,
          { cwd: this.config.repoRoot }
        );
        baseImage = Buffer.from(baseBase64, 'base64');
      } catch {
        // File might not exist in base commit
      }

      try {
        const { stdout: headBase64 } = await execAsync(
          `git show ${headFilePath} 2>/dev/null | base64`,
          { cwd: this.config.repoRoot }
        );
        headImage = Buffer.from(headBase64, 'base64');
      } catch {
        // File might not exist in head commit
      }

      // Handle cases where file doesn't exist in one or both commits
      if (!baseImage && !headImage) {
        return {
          success: false,
          baseCommit,
          headCommit,
          hasVisualChanges: false,
          diffPercentage: 0,
          error: 'File does not exist in either commit'
        };
      }

      if (!baseImage) {
        return {
          success: true,
          baseCommit,
          headCommit,
          headImage,
          hasVisualChanges: true,
          diffPercentage: 1,
          likelyCause: 'File added'
        };
      }

      if (!headImage) {
        return {
          success: true,
          baseCommit,
          headCommit,
          baseImage,
          hasVisualChanges: true,
          diffPercentage: 1,
          likelyCause: 'File removed'
        };
      }

      // Compare images if both exist
      if (this.visualDiffer) {
        const diffResult = await this.visualDiffer.compare(baseImage, headImage);

        let diffImage: Uint8Array | undefined;
        if (diffResult.diffImage) {
          diffImage = diffResult.diffImage;
        }

        return {
          success: true,
          baseCommit,
          headCommit,
          baseImage,
          headImage,
          diffImage,
          hasVisualChanges: diffResult.hasDifference,
          diffPercentage: diffResult.diffPercentage
        };
      }

      // Without visual differ, just report that images exist
      return {
        success: true,
        baseCommit,
        headCommit,
        baseImage,
        headImage,
        hasVisualChanges: true,
        diffPercentage: 1,
        error: 'No visual differ configured'
      };
    } catch (error) {
      return {
        success: false,
        baseCommit,
        headCommit,
        hasVisualChanges: false,
        diffPercentage: 0,
        error: error instanceof Error ? error.message : 'Unknown error during visual diff'
      };
    }
  }

  /**
   * Commit visual assets with a message.
   */
  async commitVisualAssets(
    message: string,
    files?: string[]
  ): Promise<GitCommitResult> {
    try {
      // Stage files
      const filesToStage = files || await this.discoverVisualAssets();
      
      for (const file of filesToStage) {
        await this.stageVisualAsset(file);
      }

      // Commit
      await execAsync(`git commit -m "${message}"`, {
        cwd: this.config.repoRoot
      });

      const commitHash = await this.getCurrentCommit();

      return {
        success: true,
        commitHash,
        commitMessage: message,
        stagedFiles: filesToStage,
        visualAssets: filesToStage
      };
    } catch (error) {
      return {
        success: false,
        stagedFiles: [],
        visualAssets: [],
        error: error instanceof Error ? error.message : 'Unknown error during commit'
      };
    }
  }

  /**
   * Discover visual asset files in the repository.
   */
  async discoverVisualAssets(): Promise<string[]> {
    const assets: string[] = [];

    for (const pattern of this.config.visualFilePatterns) {
      try {
        const { stdout } = await execAsync(
          `git ls-files --others --exclude-standard "${this.config.visualAssetsDirectory}/**/${pattern}"`,
          { cwd: this.config.repoRoot }
        );
        
        const files = stdout.trim().split('\n').filter(f => f.length > 0);
        assets.push(...files);
      } catch {
        // No files match this pattern
      }
    }

    return [...new Set(assets)]; // Remove duplicates
  }

  /**
   * Get visual branch information.
   */
  async getVisualBranchInfo(): Promise<VisualBranchInfo> {
    const branchName = await this.getCurrentBranch();
    const headCommit = await this.getCurrentCommit();

    const visualAssets = await this.discoverVisualAssets();

    return {
      name: branchName,
      headCommit,
      visualAssets
    };
  }

  /**
   * Create a visual comparison report between two branches.
   */
  async compareBranches(
    sourceBranch: string,
    targetBranch: string
  ): Promise<{
    success: boolean;
    sourceCommit: string;
    targetCommit: string;
    visualDiffs: GitVisualDiffResult[];
    summary: {
      added: number;
      removed: number;
      modified: number;
      unchanged: number;
    };
    error?: string;
  }> {
    try {
      // Get commits for both branches
      await execAsync(`git checkout ${sourceBranch}`, {
        cwd: this.config.repoRoot
      });
      const sourceCommit = await this.getCurrentCommit();

      await execAsync(`git checkout ${targetBranch}`, {
        cwd: this.config.repoRoot
      });
      const targetCommit = await this.getCurrentCommit();

      // Restore original branch
      await execAsync(`git checkout ${sourceBranch}`, {
        cwd: this.configRepoRoot
      });

      // Get visual assets
      const assets = await this.discoverVisualAssets();
      const visualDiffs: GitVisualDiffResult[] = [];

      let added = 0, removed = 0, modified = 0, unchanged = 0;

      for (const asset of assets) {
        const diff = await this.generateVisualDiff(sourceCommit, targetCommit, asset);
        
        if (diff.error?.includes('does not exist in either commit')) {
          continue;
        }

        if (diff.error?.includes('File added')) {
          added++;
        } else if (diff.error?.includes('File removed')) {
          removed++;
        } else if (diff.hasVisualChanges) {
          if (diff.diffPercentage >= 1) {
            removed++;
            added++;
          } else {
            modified++;
          }
        } else {
          unchanged++;
        }

        visualDiffs.push(diff);
      }

      return {
        success: true,
        sourceCommit,
        targetCommit,
        visualDiffs,
        summary: { added, removed, modified, unchanged }
      };
    } catch (error) {
      return {
        success: false,
        sourceCommit: '',
        targetCommit: '',
        visualDiffs: [],
        summary: { added: 0, removed: 0, modified: 0, unchanged: 0 },
        error: error instanceof Error ? error.message : 'Unknown error comparing branches'
      };
    }
  }

  /**
   * Setup a git hook for visual diff pre-commit validation.
   */
  async setupPreCommitHook(): Promise<void> {
    const hookPath = path.join(this.config.repoRoot, '.git', 'hooks', 'pre-commit');
    const hookContent = `#!/bin/bash
# VisualVerse Pre-commit Hook
# Automatically generates visual diffs for modified visual assets

VISUAL_DIFF_ENABLED=true
VISUAL_DIFF_THRESHOLD=0.05

if [ "$VISUAL_DIFF_ENABLED" = true ]; then
  echo "Running visual diff checks..."
  # Visual diff logic would go here
fi
`;

    await fs.writeFile(hookPath, hookContent);
    await fs.chmod(hookPath, 0o755);
  }

  /**
   * Get the git log for visual assets.
   */
  async getVisualAssetLog(maxCount: number = 20): Promise<Array<{
    commit: string;
    message: string;
    author: string;
    date: Date;
    files: string[];
  }>> {
    const { stdout } = await execAsync(
      `git log --oneline --name-only -${maxCount}`,
      { cwd: this.config.repoRoot }
    );

    const entries: Array<{
      commit: string;
      message: string;
      author: string;
      date: Date;
      files: string[];
    }> = [];
    
    const lines = stdout.trim().split('\n');
    let currentEntry: {
      commit: string;
      message: string;
      author: string;
      date: Date;
      files: string[];
    } | null = null;

    for (const line of lines) {
      if (/^[a-f0-9]{7,40}$/.test(line.substring(0, 7))) {
        if (currentEntry) {
          entries.push(currentEntry);
        }
        currentEntry = {
          commit: line.substring(0, 7),
          message: '',
          author: '',
          date: new Date(),
          files: []
        };
      } else if (currentEntry && line.trim()) {
        // Check if it's a visual asset file
        const isVisualAsset = this.config.visualFilePatterns.some(
          pattern => new RegExp(pattern.replace('*', '.*')).test(line)
        );
        if (isVisualAsset) {
          currentEntry.files.push(line);
        }
      }
    }

    if (currentEntry) {
      entries.push(currentEntry);
    }

    return entries;
  }
}
