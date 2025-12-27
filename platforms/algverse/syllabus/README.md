# AlgVerse - Syllabus Module

## Overview
This module defines the curriculum structure and lesson content for AlgVerse, covering sorting algorithms, graph algorithms, and dynamic programming topics.

## License
**Apache 2.0** - This module is open source under the Apache License 2.0. See `/LICENSE` for terms.

## Directory Structure

```
syllabus/
├── manifest.json          # Curriculum structure
├── content/
│   ├── sorting/
│   │   ├── introduction.md
│   │   ├── bubble-sort.md
│   │   ├── quick-sort.md
│   │   └── merge-sort.md
│   ├── graphs/
│   │   ├── graph-basics.md
│   │   ├── bfs-dfs.md
│   │   └── shortest-path.md
│   └── dp/
│       ├── intro-dp.md
│       ├── memoization.md
│       └── tabulation.md
├── assessments/
│   ├── quizzes.json
│   └── problems.json
└── README.md
```

## Curriculum Structure (manifest.json)

```json
{
  "title": "AlgVerse Curriculum",
  "version": "1.0.0",
  "levels": [
    {
      "id": "sorting-basics",
      "title": "Sorting Algorithms",
      "order": 1,
      "duration": "4 weeks",
      "topics": [
        {
          "id": "bubble-sort",
          "title": "Bubble Sort",
          "lessons": ["concept", "implementation", "optimization"],
          "animations": ["sorting/bubble-sort"],
          "assessments": ["quiz-sorting"]
        }
      ]
    }
  ]
}
```

## Content Format

Lessons are written in Markdown with embedded animation references:

```markdown
# Bubble Sort

## Learning Objectives
- Understand the bubble sort algorithm
- Analyze time and space complexity
- Identify optimization opportunities

## Concept: How Bubble Sort Works

Bubble sort repeatedly steps through the list, compares adjacent elements, and swaps them if they are in the wrong order.

<animation src="sorting/bubble-sort.ts" 
           type="interactive"
           params='{"array": [64, 34, 25, 12, 22, 11, 90], "speed": 500}' />

## Step-by-Step Process

### Pass 1
Compare and swap adjacent elements:
- [64, 34, 25, 12, 22, 11, 90] → [34, 64, 25, 12, 22, 11, 90]
- [34, 64, 25, 12, 22, 11, 90] → [34, 25, 64, 12, 22, 11, 90]
- [34, 25, 64, 12, 22, 11, 90] → [34, 25, 12, 64, 22, 11, 90]
- ...

### Pass 2
After first pass, largest element "bubbles" to end:
- Continue with remaining elements

### Optimization
If no swaps in a pass, array is sorted!

<animation src="sorting/bubble-sort.ts" 
           type="step-by-step"
           params='{"showSwaps": true, "highlightSorted": true}' />

## Complexity Analysis

| Aspect | Complexity |
|--------|------------|
| Best Case | O(n) |
| Average Case | O(n²) |
| Worst Case | O(n²) |
| Space | O(1) |
| Stable | Yes |

## Why "Bubble" Sort?

The larger elements "bubble up" to the end of the array with each pass, like bubbles rising to the surface of water.

## When to Use

- Small datasets (n < 1000)
- Nearly sorted data
- Educational purposes
- When stability is required

## Summary
- Bubble sort compares adjacent elements
- Largest elements "bubble" to correct position
- Simple but inefficient for large lists
- Can be optimized with swap flag
```

## License

Licensed under the Apache License, Version 2.0. See `/LICENSE` for details.
