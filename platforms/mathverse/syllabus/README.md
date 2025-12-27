# MathVerse - Syllabus Module

## Overview
This module defines the curriculum structure and lesson content for MathVerse, covering algebra, calculus, and linear algebra topics.

## License
**Apache 2.0** - This module is open source under the Apache License 2.0. See `/LICENSE` for terms.

## Directory Structure

```
syllabus/
├── manifest.json          # Curriculum structure
├── content/
│   ├── algebra/
│   │   ├── linear-equations.md
│   │   ├── quadratic-equations.md
│   │   ├── polynomials.md
│   │   └── systems.md
│   ├── calculus/
│   │   ├── limits.md
│   │   ├── derivatives.md
│   │   ├── integrals.md
│   │   └── series.md
│   └── linear_algebra/
│       ├── vectors.md
│       ├── matrices.md
│       ├── transformations.md
│       └── eigenvalues.md
├── assessments/
│   ├── quizzes.json
│   └── problems.json
└── README.md
```

## Curriculum Structure (manifest.json)

```json
{
  "title": "MathVerse Curriculum",
  "version": "1.0.0",
  "levels": [
    {
      "id": "algebra-fundamentals",
      "title": "Algebra Fundamentals",
      "order": 1,
      "duration": "4 weeks",
      "topics": [
        {
          "id": "linear-equations",
          "title": "Linear Equations",
          "lessons": ["intro-to-equations", "solving-basics", "applications"],
          "animations": ["algebra/linear-equations"],
          "assessments": ["quiz-1"]
        }
      ]
    }
  ]
}
```

## Content Format

Lessons are written in Markdown with embedded animation references:

```markdown
# Linear Equations

## Learning Objectives
- Understand the structure of linear equations
- Solve single-variable equations
- Graph linear functions

## Concept: What is a Linear Equation?

An equation is a statement that two expressions are equal.

<animation src="algebra/linear-equations.ts" 
           type="interactive"
           params='{"equation": "2x + 3 = 7"}' />

## Step-by-Step Solution

To solve linear equations, we use these operations:

1. Addition/subtraction of constants
2. Multiplication/division by non-zero constants
3. Check your solution

<animation src="algebra/linear-equations.ts" 
           type="step-by-step"
           params='{"showAllSteps": true}' />

## Practice Problems

1. Solve: 3x - 5 = 10
2. Find x: 2(x + 4) = 16

## Summary
- Linear equations have the form ax + b = c
- Use inverse operations to isolate the variable
- Always check your solution
```

## Assessment Format

Quizzes are defined in JSON format:

```json
{
  "id": "quiz-1",
  "title": "Linear Equations Quiz",
  "questions": [
    {
      "type": "multiple-choice",
      "question": "What is the solution to 2x + 3 = 7?",
      "options": ["x = 1", "x = 2", "x = 3", "x = 4"],
      "correctAnswer": 1,
      "explanation": "Subtract 3 from both sides: 2x = 4, then divide by 2: x = 2"
    }
  ]
}
```

## License

Licensed under the Apache License, Version 2.0. See `/LICENSE` for details.
