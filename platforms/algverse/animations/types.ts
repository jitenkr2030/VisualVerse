/**
 * AlgVerse Animation Types
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

// Sorting Algorithm Types
export interface SortOptions {
  array: number[];
  speed?: number;
  showComparisons?: boolean;
  showSwaps?: boolean;
}

export interface QuickSortOptions extends SortOptions {
  pivotStrategy?: 'first' | 'last' | 'middle' | 'random';
  showRecursion?: boolean;
  highlightPivot?: boolean;
}

export interface MergeSortOptions extends SortOptions {
  showMergeSteps?: boolean;
  showAuxiliaryArray?: boolean;
  highlightSortedSegments?: boolean;
}

// Graph Algorithm Types
export interface GraphOptions {
  nodes: string[];
  edges: Array<[string, string]>;
  directed?: boolean;
  weighted?: boolean;
}

export interface BFSOptions extends GraphOptions {
  startNode: string;
  showVisited?: boolean;
  showQueue?: boolean;
  highlightLevel?: boolean;
}

export interface DFSOptions extends GraphOptions {
  startNode: string;
  showVisited?: boolean;
  showStack?: boolean;
  showBacktracking?: boolean;
}

export interface DijkstraOptions extends GraphOptions {
  startNode: string;
  endNode: string;
  showDistances?: boolean;
  showRelaxation?: boolean;
  highlightShortestPath?: boolean;
}

// Dynamic Programming Types
export interface DPOptions {
  showTable?: boolean;
  showRecursion?: boolean;
  speed?: number;
}

export interface FibonacciOptions extends DPOptions {
  n: number;
  showTree?: boolean;
  compareMethods?: boolean;
}

export interface KnapsackOptions extends DPOptions {
  capacity: number;
  items: Array<{ weight: number; value: number }>;
  showItemSelection?: boolean;
  highlightOptimal?: boolean;
}

export interface LCSOptions extends DPOptions {
  string1: string;
  string2: string;
  showMatchingChars?: boolean;
  highlightLCS?: boolean;
}
