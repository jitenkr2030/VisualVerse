/**
 * VisualVerse Animation Engine - Version Control Module
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

// Export version control components
export { VersionControlTracker } from './tracker';
export { VisualDiffer } from './differ';
export { GitBridge } from './git-bridge';

// Export types
export {
  VersionSnapshot,
  SceneChange,
  ChangeType,
  CommitResult,
  CheckoutResult,
  CompareResult,
  WorkingDirectoryStatus,
  VisualGitStatus,
  GitVisualDiffResult,
  GitCommitResult,
  VisualBranchInfo,
  DiffResult,
  DiffAnalysis,
  DiffRegion,
  VisualDiffConfig
} from './tracker';

// Re-export from core
export { ISerializable, SerializationUtils, SerializationResult, DeserializationResult } from '../core/serializable';
