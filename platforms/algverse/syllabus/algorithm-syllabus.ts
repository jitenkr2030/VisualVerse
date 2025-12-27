/**
 * Algorithms Syllabus - AlgVerse Platform
 * 
 * This file defines the comprehensive curriculum structure for algorithms and data structures,
 * covering fundamental algorithms through advanced competitive programming concepts.
 * 
 * Licensed under the Apache License, Version 2.0
 */

export interface AlgorithmUnit {
  id: string;
  name: string;
  description: string;
  algorithms: string[];
  data_structures: string[];
  duration_hours: number;
  difficulty_level: 'beginner' | 'elementary' | 'intermediate' | 'advanced' | 'expert';
  prerequisites: string[];
  learning_outcomes: string[];
  coding_exercises: string[];
  complexity_analysis: string[];
  standards: string[];
}

export interface AlgorithmSection {
  id: string;
  name: string;
  description: string;
  units: AlgorithmUnit[];
  total_duration_hours: number;
  sequence_order: number;
}

export interface AlgorithmSyllabus {
  subject: 'algorithms';
  display_name: 'Algorithms & Data Structures';
  description: 'Comprehensive algorithms curriculum from basics through competitive programming';
  total_duration_hours: number;
  sections: AlgorithmSection[];
  applicable_standards: string[];
  target_audience: string[];
}

// ============================================
// SECTION 1: PROGRAMMING FUNDAMENTALS
// ============================================

const section1: AlgorithmSection = {
  id: 'programming-fundamentals',
  name: 'Programming Fundamentals',
  description: 'Essential programming concepts for algorithm implementation',
  units: [],
  total_duration_hours: 60,
  sequence_order: 1
};

section1.units = [
  {
    id: 'programming-basics',
    name: 'Programming Basics and Pseudocode',
    description: 'Introduction to programming concepts and algorithm description',
    algorithms: [],
    data_structures: [],
    duration_hours: 15,
    difficulty_level: 'beginner',
    prerequisites: [],
    learning_outcomes: [
      'Understand basic programming constructs',
      'Write clear pseudocode for algorithms',
      'Implement basic input/output operations',
      'Debug simple programs'
    ],
    coding_exercises: ['hello-world', 'basic-calculations', 'conditional-programs', 'loops-practice'],
    complexity_analysis: [],
    standards: ['K12CS.3A', 'K12CS.3B']
  },
  {
    id: 'functions-recursion',
    name: 'Functions and Recursion',
    description: 'Modular programming and recursive problem solving',
    algorithms: ['factorial', 'fibonacci', 'recursive-search'],
    data_structures: ['call-stack'],
    duration_hours: 20,
    difficulty_level: 'beginner',
    prerequisites: ['programming-basics'],
    learning_outcomes: [
      'Write modular functions with parameters and return values',
      'Understand recursive function execution',
      'Trace recursive algorithms step by step',
      'Convert recursive to iterative solutions'
    ],
    coding_exercises: ['recursive-factorial', 'fibonacci-versions', 'recursive-search', 'tower-of-hanoi'],
    complexity_analysis: ['recurrence-relations', 'recursive-complexity'],
    standards: ['K12CS.3A', 'K12CS.3B', 'APCS-A.3']
  },
  {
    id: 'arrays-strings',
    name: 'Arrays and Strings',
    description: 'Working with sequential data structures',
    algorithms: ['linear-search', 'bubble-sort', 'selection-sort', 'string-matching-basic'],
    data_structures: ['array', 'string'],
    duration_hours: 25,
    difficulty_level: 'elementary',
    prerequisites: ['functions-recursion'],
    learning_outcomes: [
      'Perform operations on arrays and strings',
      'Implement basic search algorithms',
      'Apply simple sorting algorithms',
      'Manipulate string data effectively'
    ],
    coding_exercises: ['array-manipulation', 'string-operations', 'search-implementations', 'sorting-basic'],
    complexity_analysis: ['O(n)', 'O(n²)', 'linear-vs-quadratic'],
    standards: ['K12CS.3A', 'APCS-A.4', 'APCS-A.6']
  }
];

// ============================================
// SECTION 2: DATA STRUCTURES FUNDAMENTALS
// ============================================

const section2: AlgorithmSection = {
  id: 'data-structures-basic',
  name: 'Fundamental Data Structures',
  description: 'Core data structures for efficient data organization',
  units: [],
  total_duration_hours: 100,
  sequence_order: 2
};

section2.units = [
  {
    id: 'linked-lists',
    name: 'Linked Lists',
    description: 'Dynamic data structure with pointer-based organization',
    algorithms: ['linked-list-search', 'linked-list-insert', 'linked-list-delete', 'reverse-linked-list', 'detect-cycle'],
    data_structures: ['singly-linked-list', 'doubly-linked-list', 'circular-linked-list'],
    duration_hours: 25,
    difficulty_level: 'intermediate',
    prerequisites: ['arrays-strings'],
    learning_outcomes: [
      'Implement singly and doubly linked lists',
      'Perform insertions and deletions in linked lists',
      'Detect cycles using Floyd\'s algorithm',
      'Compare array and linked list performance'
    ],
    coding_exercises: ['linked-list-implementation', 'list-reversal', 'cycle-detection', 'merge-two-lists'],
    complexity_analysis: ['O(n) access', 'O(1) insertion-deletion', 'space-complexity'],
    standards: ['APCS-A.4', 'APCS-A.8', 'CLRS.10']
  },
  {
    id: 'stacks-queues',
    name: 'Stacks and Queues',
    description: 'Linear data structures with restricted access patterns',
    algorithms: ['stack-operations', 'queue-operations', 'parentheses-matching', 'circular-queue', 'priority-queue-intro'],
    data_structures: ['stack', 'queue', 'deque', 'priority-queue'],
    duration_hours: 20,
    difficulty_level: 'intermediate',
    prerequisites: ['linked-lists'],
    learning_outcomes: [
      'Implement stack and queue data structures',
      'Apply stacks for expression evaluation',
      'Use queues for scheduling and breadth-first operations',
      'Understand real-world applications of each structure'
    ],
    coding_exercises: ['stack-implementation', 'queue-using-arrays', 'expression-evaluation', 'sliding-window-max'],
    complexity_analysis: ['O(1) operations', 'amortized-analysis'],
    standards: ['APCS-A.4', 'CLRS.10']
  },
  {
    id: 'binary-trees',
    name: 'Binary Trees and Binary Search Trees',
    description: 'Hierarchical data structures for efficient searching',
    algorithms: ['tree-traversal', 'tree-search', 'tree-insert', 'tree-delete', 'height-calculation', 'balance-check'],
    data_structures: ['binary-tree', 'binary-search-tree', 'heap-intro'],
    duration_hours: 30,
    difficulty_level: 'advanced',
    prerequisites: ['stacks-queues'],
    learning_outcomes: [
      'Implement binary tree and BST operations',
      'Perform inorder, preorder, and postorder traversals',
      'Search, insert, and delete nodes in BST',
      'Analyze tree height and balance properties'
    ],
    coding_exercises: ['tree-implementation', 'traversal-patterns', 'bst-operations', 'tree-height', 'lowest-common-ancestor'],
    complexity_analysis: ['O(log n) BST operations', 'O(n) worst-case', 'tree-properties'],
    standards: ['APCS-A.8', 'CLRS.12', 'CLRS.13']
  },
  {
    id: 'heaps-priority-queues',
    name: 'Heaps and Priority Queues',
    description: 'Complete binary trees for priority-based operations',
    algorithms: ['heapify', 'heap-insert', 'heap-extract', 'heap-sort'],
    data_structures: ['binary-heap', 'min-heap', 'max-heap', 'priority-queue'],
    duration_hours: 25,
    difficulty_level: 'advanced',
    prerequisites: ['binary-trees'],
    learning_outcomes: [
      'Implement min-heap and max-heap data structures',
      'Perform heap operations with proper heapify',
      'Apply heap sort algorithm',
      'Use priority queues in algorithm design'
    ],
    coding_exercises: ['heap-implementation', 'k-largest-elements', 'merge-k-sorted', 'median-maintenance'],
    complexity_analysis: ['O(log n) heap operations', 'O(n log n) heap sort', 'build-heap O(n)'],
    standards: ['CLRS.6', 'APCS-A.8']
  }
];

// ============================================
// SECTION 3: ALGORITHM DESIGN PARADIGMS
// ============================================

const section3: AlgorithmSection = {
  id: 'algorithm-paradigms',
  name: 'Algorithm Design Paradigms',
  description: 'Fundamental approaches to algorithm design and problem solving',
  units: [],
  total_duration_hours: 120,
  sequence_order: 3
};

section3.units = [
  {
    id: 'divide-conquer',
    name: 'Divide and Conquer',
    description: 'Breaking problems into smaller subproblems',
    algorithms: ['merge-sort', 'quick-sort', 'binary-search', 'closest-pair', 'strassen-matrix', 'karatsuba-multiplication'],
    data_structures: ['merge-sort-recursion'],
    duration_hours: 30,
    difficulty_level: 'advanced',
    prerequisites: ['heaps-priority-queues'],
    learning_outcomes: [
      'Apply divide and conquer to sorting',
      'Implement efficient search algorithms',
      'Analyze divide and conquer time complexity',
      'Recognize problems suitable for divide and conquer'
    ],
    coding_exercises: ['merge-sort-implementation', 'quick-sort-variants', 'binary-search-variants', 'matrix-multiplication'],
    complexity_analysis: ['master-theorem', 'recurrence-relations', 'best-worst-average'],
    standards: ['CLRS.4', 'CLRS.7', 'APCS-A.7']
  },
  {
    id: 'greedy-algorithms',
    name: 'Greedy Algorithms',
    description: 'Making locally optimal choices for global solutions',
    algorithms: ['activity-selection', 'huffman-coding', 'dijkstra-algorithm', 'prims-algorithm', 'fractional-knapsack', 'coin-change-greedy'],
    data_structures: ['priority-queue-use', 'disjoint-set'],
    duration_hours: 35,
    difficulty_level: 'advanced',
    prerequisites: ['divide-conquer'],
    learning_outcomes: [
      'Understand the greedy choice property',
      'Prove correctness of greedy algorithms',
      'Apply greedy approach to optimization problems',
      'Compare greedy with dynamic programming solutions'
    ],
    coding_exercises: ['activity-selection', 'huffman-coding', 'dijkstra-implementation', 'prim-mst', 'fractional-knapsack'],
    complexity_analysis: ['greedy-choice-proof', 'optimal-substructure', 'complexity-comparison'],
    standards: ['CLRS.16', 'CLRS.23', 'CLRS.24']
  },
  {
    id: 'dynamic-programming',
    name: 'Dynamic Programming',
    description: 'Solving overlapping subproblems with memoization',
    algorithms: ['fibonacci-dp', 'knapsack', 'longest-common-subsequence', 'edit-distance', 'matrix-chain-multiplication', 'optimal-binary-search-tree'],
    data_structures: ['dp-table', 'memoization-cache'],
    duration_hours: 35,
    difficulty_level: 'expert',
    prerequisites: ['greedy-algorithms'],
    learning_outcomes: [
      'Identify problems with optimal substructure',
      'Implement top-down and bottom-up DP',
      'Optimize space complexity of DP solutions',
      'Solve classic DP problems'
    ],
    coding_exercises: ['fibonacci-memoized', '0-1-knapsack', 'lcs-implementation', 'edit-distance', 'dp-table-optimization'],
    complexity_analysis: ['state-definition', 'transition-formulation', 'space-optimization', 'time-complexity'],
    standards: ['CLRS.15', 'APCS-A.9', 'CLRS.14']
  },
  {
    id: 'backtracking',
    name: 'Backtracking and Branch and Bound',
    description: 'Systematic search through solution spaces',
    algorithms: ['n-queens', 'subset-sum', 'permutations-combinations', 'sudoku-solver', 'graph-coloring', 'knapsack-branch-bound'],
    data_structures: ['recursion-backtracking', 'pruning-conditions'],
    duration_hours: 20,
    difficulty_level: 'advanced',
    prerequisites: ['dynamic-programming'],
    learning_outcomes: [
      'Implement systematic backtracking solutions',
      'Apply pruning to reduce search space',
      'Solve constraint satisfaction problems',
      'Analyze backtracking time complexity'
    ],
    coding_exercises: ['n-queens', 'sudoku-solver', 'subset-sum', 'permutation-generation', 'word-search'],
    complexity_analysis: ['search-tree-size', 'pruning-effectiveness', 'worst-case-complexity'],
    standards: ['CLRS.5', 'CLRS.34']
  }
];

// ============================================
// SECTION 4: GRAPH ALGORITHMS
// ============================================

const section4: AlgorithmSection = {
  id: 'graph-algorithms',
  name: 'Graph Algorithms',
  description: 'Algorithms for graph representation and traversal',
  units: [],
  total_duration_hours: 100,
  sequence_order: 4
};

section4.units = [
  {
    id: 'graph-representation',
    name: 'Graph Representation and Traversal',
    description: 'Ways to represent graphs and traverse them',
    algorithms: ['bfs', 'dfs', 'connected-components', 'topological-sort'],
    data_structures: ['adjacency-matrix', 'adjacency-list', 'graph-adjacency'],
    duration_hours: 25,
    difficulty_level: 'intermediate',
    prerequisites: ['binary-trees'],
    learning_outcomes: [
      'Choose appropriate graph representation',
      'Implement BFS and DFS traversal',
      'Find connected components in graphs',
      'Perform topological sorting on DAGs'
    ],
    coding_exercises: ['graph-implementation', 'bfs-shortest-path', 'dfs-maze', 'connected-components', 'course-schedule'],
    complexity_analysis: ['O(V+E) traversal', 'space-representations', 'queue-vs-stack'],
    standards: ['CLRS.22', 'APCS-A.8']
  },
  {
    id: 'shortest-paths',
    name: 'Shortest Path Algorithms',
    description: 'Finding shortest paths in graphs',
    algorithms: ['dijkstra', 'bellman-ford', 'floyd-warshall', 'johnson-algorithm', 'a-star-search'],
    data_structures: ['priority-queue', 'distance-array'],
    duration_hours: 30,
    difficulty_level: 'advanced',
    prerequisites: ['graph-representation', 'greedy-algorithms'],
    learning_outcomes: [
      'Implement Dijkstra\'s algorithm with priority queue',
      'Handle negative weights with Bellman-Ford',
      'Solve all-pairs shortest paths with Floyd-Warshall',
      'Apply A* for informed search'
    ],
    coding_exercises: ['dijkstra-implementation', 'negative-cycle-detection', 'all-pairs-shortest', 'a-star-maze'],
    complexity_analysis: ['O((V+E)logV) dijkstra', 'O(VE) bellman-ford', 'O(V³) floyd-warshall'],
    standards: ['CLRS.24', 'CLRS.25', 'CLRS.26']
  },
  {
    id: 'minimum-spanning-trees',
    name: 'Minimum Spanning Trees',
    description: 'Finding minimum weight connected subgraphs',
    algorithms: ['prim', 'kruskal', 'boruvka'],
    data_structures: ['disjoint-set-union', 'union-find'],
    duration_hours: 20,
    difficulty_level: 'advanced',
    prerequisites: ['graph-representation'],
    learning_outcomes: [
      'Implement Prim\'s and Kruskal\'s algorithms',
      'Use union-find data structure efficiently',
      'Analyze MST correctness and complexity',
      'Apply MST to network design problems'
    ],
    coding_exercises: ['prim-implementation', 'kruskal-with-union-find', 'mst-applications'],
    complexity_analysis: ['O(E log V) kruskal', 'O(E log V) prim', 'union-find optimization'],
    standards: ['CLRS.23', 'CLRS.21']
  },
  {
    id: 'network-flow',
    name: 'Network Flow and Matching',
    description: 'Maximum flow and bipartite matching problems',
    algorithms: ['ford-fulkerson', 'edmonds-karp', 'dinic-algorithm', 'bipartite-matching', 'max-flow-min-cut'],
    data_structures: ['residual-graph', 'level-graph'],
    duration_hours: 25,
    difficulty_level: 'expert',
    prerequisites: ['shortest-paths'],
    learning_outcomes: [
      'Understand flow networks and cut capacity',
      'Implement Ford-Fulkerson and Edmonds-Karp',
      'Solve bipartite matching problems',
      'Apply max-flow min-cut theorem'
    ],
    coding_exercises: ['ford-fulkerson', 'max-flow-applications', 'bipartite-matching', 'min-cut-calculation'],
    complexity_analysis: ['O(VE²) edmonds-karp', 'O(E√V) bipartite-matching', 'capacity-scaling'],
    standards: ['CLRS.26', 'CLRS.27']
  }
];

// ============================================
// SECTION 5: ADVANCED TOPICS
// ============================================

const section5: AlgorithmSection = {
  id: 'advanced-algorithms',
  name: 'Advanced Algorithm Topics',
  description: 'Complex algorithms for specialized problems',
  units: [],
  total_duration_hours: 80,
  sequence_order: 5
};

section5.units = [
  {
    id: 'string-algorithms',
    name: 'String Algorithms',
    description: 'Efficient algorithms for string processing',
    algorithms: ['kmp', 'rabin-karp', 'z-algorithm', 'trie', 'suffix-array', 'manacher-algorithm'],
    data_structures: ['trie', 'suffix-tree', 'rolling-hash'],
    duration_hours: 25,
    difficulty_level: 'expert',
    prerequisites: ['dynamic-programming'],
    learning_outcomes: [
      'Implement KMP and Rabin-Karp string matching',
      'Build and search Trie data structures',
      'Solve longest palindrome substring problems',
      'Apply string algorithms to text processing'
    ],
    coding_exercises: ['kmp-implementation', 'rabin-karp', 'trie-operations', 'longest-palindrome'],
    complexity_analysis: ['O(n+m) KMP', 'O(n+m) Z-algorithm', 'trie-complexity'],
    standards: ['CLRS.32', 'CLRS.33']
  },
  {
    id: 'computational-geometry',
    name: 'Computational Geometry',
    description: 'Algorithms for geometric problems',
    algorithms: ['convex-hull', 'line-intersection', 'point-in-polygon', 'closest-pair-optimized', 'sweep-line'],
    data_structures: ['balanced-tree-sweep'],
    duration_hours: 25,
    difficulty_level: 'expert',
    prerequisites: ['divide-conquer'],
    learning_outcomes: [
      'Implement convex hull algorithms (Graham scan, Jarvis)',
      'Detect line segment intersections',
      'Solve point location problems',
      'Apply sweep line algorithms'
    ],
    coding_exercises: ['convex-hull', 'line-intersection', 'point-in-polygon', 'closest-pair'],
    complexity_analysis: ['O(n log n) convex-hull', 'O(n log n) closest-pair', 'sweep-line O(n log n)'],
    standards: ['CLRS.33', 'Computational-Geometry-Standard']
  },
  {
    id: 'np-completeness',
    name: 'NP-Completeness and Approximation',
    description: 'Understanding problem hardness and approximation algorithms',
    algorithms: ['vertex-cover-approximation', 'set-cover-approximation', 'tsp-approximation', '3-sat-reduction'],
    data_structures: [],
    duration_hours: 30,
    difficulty_level: 'expert',
    prerequisites: ['network-flow'],
    learning_outcomes: [
      'Understand P, NP, and NP-complete classes',
      'Perform reductions between NP-complete problems',
      'Apply approximation algorithms',
      'Handle NP-hard problems in practice'
    ],
    coding_exercises: ['np-hardness-identification', 'approximation-ratio', 'heuristic-solutions'],
    complexity_analysis: ['polynomial-reduction', 'approximation-ratios', 'exponential-algorithms'],
    standards: ['CLRS.34', 'CLRS.35']
  }
];

// ============================================
// SECTION 6: COMPETITIVE PROGRAMMING
// ============================================

const section6: AlgorithmSection = {
  id: 'competitive-programming',
  name: 'Competitive Programming',
  description: 'Algorithm competition techniques and problem-solving strategies',
  units: [],
  total_duration_hours: 60,
  sequence_order: 6
};

section6.units = [
  {
    id: 'cp-strategies',
    name: 'CP Problem-Solving Strategies',
    description: 'Techniques for competitive programming contests',
    algorithms: ['two-pointers', 'sliding-window', 'binary-search-applications', 'frequency-counting', 'prefix-sums'],
    data_structures: ['hash-map', 'prefix-array'],
    duration_hours: 20,
    difficulty_level: 'intermediate',
    prerequisites: ['graph-algorithms'],
    learning_outcomes: [
      'Apply two-pointer technique',
      'Implement sliding window maximum',
      'Use prefix sums for range queries',
      'Choose appropriate data structures for CP'
    ],
    coding_exercises: ['two-pointer-problems', 'sliding-window-variants', 'prefix-sum-queries', 'frequency-counting'],
    complexity_analysis: ['O(n) patterns', 'space-time-tradeoff'],
    standards: ['CP-Algorithms', 'Codeforces-Training']
  },
  {
    id: 'advanced-ds',
    name: 'Advanced Data Structures',
    description: 'Complex data structures for competitive programming',
    algorithms: ['segment-tree', 'fenwick-tree', 'disjoint-set-optimized', 'sparse-table'],
    data_structures: ['segment-tree', 'fenwick-tree', 'sparse-table'],
    duration_hours: 25,
    difficulty_level: 'expert',
    prerequisites: ['cp-strategies'],
    learning_outcomes: [
      'Implement segment tree with lazy propagation',
      'Use Fenwick tree for prefix queries',
      'Apply sparse table for RMQ',
      'Choose appropriate advanced DS for problems'
    ],
    coding_exercises: ['segment-tree-range-query', 'fenwick-tree', 'range-sum-queries', 'lca-with-sparse-table'],
    complexity_analysis: ['O(log n) segment-tree', 'O(log n) fenwick', 'O(1) sparse-table'],
    standards: ['CP-Algorithms', 'Codeforces-Training']
  },
  {
    id: 'math-algo',
    name: 'Mathematical Algorithms',
    description: 'Number theory and combinatorial algorithms',
    algorithms: ['gcd-lcm', 'extended-euclid', 'sieve-prime', 'modular-arithmetic', 'fast-exponentiation', 'combinatorics'],
    data_structures: [],
    duration_hours: 15,
    difficulty_level: 'intermediate',
    prerequisites: ['programming-basics'],
    learning_outcomes: [
      'Implement GCD and extended Euclidean algorithm',
      'Generate primes using sieve methods',
      'Apply modular arithmetic operations',
      'Calculate combinations efficiently'
    ],
    coding_exercises: ['prime-sieve', 'modular-inverse', 'fast-power', 'ncr-combinatorics'],
    complexity_analysis: ['O(n log log n) sieve', 'O(log n) extended-gcd', 'O(1) modular'],
    standards: ['CLRS.31', 'Number-Theory-Standard']
  }
];

// ============================================
// COMPLETE SYLLABUS DEFINITION
// ============================================

export const algorithmSyllabus: AlgorithmSyllabus = {
  subject: 'algorithms',
  display_name: 'Algorithms & Data Structures',
  description: 'Comprehensive algorithms curriculum from programming fundamentals through competitive programming',
  total_duration_hours: 520,
  sections: [section1, section2, section3, section4, section5, section6],
  applicable_standards: [
    'AP Computer Science A',
    'AP Computer Science Principles',
    'K12 Computer Science Standards',
    'ACM/IEEE Computing Curricula',
    'LeetCode Problem Categories',
    'Codeforces Problem Sets'
  ],
  target_audience: ['High School', 'Undergraduate', 'Graduate', 'Professional']
};

// Export utility functions
export function getAlgorithmUnitById(syllabus: AlgorithmSyllabus, unitId: string): AlgorithmUnit | undefined {
  for (const section of syllabus.sections) {
    const unit = section.units.find(u => u.id === unitId);
    if (unit) return unit;
  }
  return undefined;
}

export function getAlgorithmPrerequisites(syllabus: AlgorithmSyllabus, unitId: string): AlgorithmUnit[] {
  const unit = getAlgorithmUnitById(syllabus, unitId);
  if (!unit) return [];
  return unit.prerequisites
    .map(prereqId => getAlgorithmUnitById(syllabus, prereqId))
    .filter((u): u is AlgorithmUnit => u !== undefined);
}

export function generateAlgorithmLearningPath(
  syllabus: AlgorithmSyllabus,
  startUnitId: string,
  targetUnitId: string
): AlgorithmUnit[] {
  const path: AlgorithmUnit[] = [];
  const visited = new Set<string>();
  
  function addUnitAndPrerequisites(unitId: string) {
    if (visited.has(unitId)) return;
    
    const unit = getAlgorithmUnitById(syllabus, unitId);
    if (!unit) return;
    
    // Add prerequisites first
    for (const prereqId of unit.prerequisites) {
      addUnitAndPrerequisites(prereqId);
    }
    
    visited.add(unitId);
    path.push(unit);
  }
  
  // Add all units from start to target
  for (const section of syllabus.sections) {
    for (const unit of section.units) {
      if (unit.id >= startUnitId && unit.id <= targetUnitId) {
        addUnitAndPrerequisites(unit.id);
      }
    }
  }
  
  return path;
}

export function calculateAlgorithmTotalDuration(syllabus: AlgorithmSyllabus, unitIds: string[]): number {
  return unitIds.reduce((total, unitId) => {
    const unit = getAlgorithmUnitById(syllabus, unitId);
    return total + (unit?.duration_hours || 0);
  }, 0);
}

export function getCodingExercises(syllabus: AlgorithmSyllabus, unitId: string): string[] {
  const unit = getAlgorithmUnitById(syllabus, unitId);
  return unit?.coding_exercises || [];
}
