# AlgVerse - Animations Module

## Overview
This module contains algorithm animation modules for VisualVerse. It provides visualizations for sorting algorithms, graph algorithms, and dynamic programming using the Animation Engine.

## License
**Apache 2.0** - This module is open source under the Apache License 2.0. See `/LICENSE` for terms.

## Directory Structure

```
animations/
├── sorting/
│   ├── bubble-sort.ts
│   ├── quick-sort.ts
│   ├── merge-sort.ts
│   └── heap-sort.ts
├── graphs/
│   ├── bfs.ts
│   ├── dfs.ts
│   ├── dijkstra.ts
│   └── prim.ts
├── dp/
│   ├── fibonacci.ts
│   ├── knapsack.ts
│   └── longest-common-subsequence.ts
├── index.ts
└── README.md
```

## Quick Start

```typescript
import { 
  animateBubbleSort, 
  animateBFS,
  animateFibonacci 
} from './animations';

const animation = animateBubbleSort({
  array: [64, 34, 25, 12, 22, 11, 90],
  speed: 500,
  showComparisons: true,
});
```

## Sorting Animations

### Bubble Sort
- Step-by-step swapping
- Pass-by-pass visualization
- Early termination detection

### Quick Sort
- Pivot selection process
- Partitioning animation
- Recursive calls visualization

### Merge Sort
- Splitting phase
- Merging with comparison
- Auxiliary array usage

### Heap Sort
- Heap construction
- Heapify process
- Sorted extraction

## Graph Algorithms Animations

### BFS (Breadth-First Search)
- Level-by-level traversal
- Queue operations
- Shortest path finding

### DFS (Depth-First Search)
- Recursive traversal
- Stack operations
- Backtracking visualization

### Dijkstra's Algorithm
- Priority queue operations
- Distance updates
- Path reconstruction

### Prim's Algorithm
- Minimum spanning tree
- Edge selection process
- Connected component growth

## Dynamic Programming Animations

### Fibonacci
- Recursive vs DP comparison
- Memoization visualization
- Bottom-up tabulation

### Knapsack Problem
- Item selection process
- Table filling animation
- Solution reconstruction

### Longest Common Subsequence
- Table building
- Backtracking path
- Multiple solutions

## Usage with Animation Engine

```typescript
import { AnimationEngine } from '@visualverse/engine';

const engine = new AnimationEngine();
const scene = engine.createScene();

const algoAnimations = new AlgorithmAnimations(scene);
algoAnimations.animateQuickSort({
  array: [38, 27, 43, 3, 9, 82, 10],
  pivotStrategy: 'last',
  showRecursion: true,
});
```

## License

Licensed under the Apache License, Version 2.0. See `/LICENSE` for details.
