# MathVerse - Animations Module

## Overview
This module contains mathematical animation modules for VisualVerse. It provides visualizations for algebra, calculus, and linear algebra concepts using the Animation Engine.

## License
**Apache 2.0** - This module is open source under the Apache License 2.0. See `/LICENSE` for terms.

## Directory Structure

```
animations/
├── algebra/
│   ├── linear-equations.ts
│   ├── quadratic-equations.ts
│   ├── polynomials.ts
│   └── systems.ts
├── calculus/
│   ├── limits.ts
│   ├── derivatives.ts
│   ├── integrals.ts
│   └── series.ts
├── linear_algebra/
│   ├── vectors.ts
│   ├── matrices.ts
│   ├── transformations.ts
│   └── eigenvalues.ts
├── index.ts
└── README.md
```

## Quick Start

```typescript
import { 
  animateLinearEquation, 
  animateDerivative,
  animateVector 
} from './animations';

const animation = animateLinearEquation({
  equation: '2x + 3 = 7',
  steps: true,
  duration: 3000,
});
```

## Algebra Animations

### Linear Equations
- Solving single-variable equations
- Visualizing step-by-step solutions
- Graphing linear functions

### Quadratic Equations
- Parabola visualization
- Vertex form transformations
- Root finding animations

### Polynomials
- Polynomial graphs
- Degree effects
- Roots and factors

### Systems of Equations
- Graphical solution visualization
- Intersection points
- Elimination method steps

## Calculus Animations

### Limits
- Visualizing limit approaches
- Infinite limits
- Continuity demonstrations

### Derivatives
- Slope visualization
- Tangent line animation
- Rate of change demonstrations

### Integrals
- Area under curves
- Riemann sums
- Fundamental theorem visualization

### Series
- Convergence animations
- Taylor series expansions
- Fourier series demonstrations

## Linear Algebra Animations

### Vectors
- Vector addition/subtraction
- Dot product visualization
- Cross product in 3D

### Matrices
- Matrix multiplication
- Row operations
- Determinant calculations

### Transformations
- Linear transformations
- Eigenvector visualization
- Rotation and scaling

### Eigenvalues
- Eigenvector directions
- Diagonalization process
- Spectral decomposition

## Usage with Animation Engine

```typescript
import { AnimationEngine } from '@visualverse/engine';

const engine = new AnimationEngine();
const scene = engine.createScene();

const algebraAnimations = new AlgebraAnimations(scene);
algebraAnimations.animateQuadratic({
  vertex: [-2, -1],
  a: 0.5,
  showRoots: true,
});
```

## License

Licensed under the Apache License, Version 2.0. See `/LICENSE` for details.
