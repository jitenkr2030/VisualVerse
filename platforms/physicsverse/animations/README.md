# PhysicsVerse - Animations Module

## Overview
This module contains physics animation modules for VisualVerse. It provides visualizations for mechanics, electromagnetism, and optics concepts using the Animation Engine.

## License
**Apache 2.0** - This module is open source under the Apache License 2.0. See `/LICENSE` for terms.

## Directory Structure

```
animations/
├── mechanics/
│   ├── kinematics.ts
│   ├── forces.ts
│   ├── energy.ts
│   └── momentum.ts
├── electromagnetism/
│   ├── electrostatics.ts
│   ├── circuits.ts
│   ├── magnetism.ts
│   └── induction.ts
├── optics/
│   ├── reflection.ts
│   ├── refraction.ts
│   ├── lenses.ts
│   └── waves.ts
├── index.ts
└── README.md
```

## Quick Start

```typescript
import { 
  animateProjectile, 
  animateCircuit,
  animateLens 
} from './animations';

const animation = animateProjectile({
  initialVelocity: 20,
  angle: 45,
  gravity: 9.8,
  showTrajectory: true,
});
```

## Mechanics Animations

### Kinematics
- Position, velocity, acceleration graphs
- Projectile motion trajectories
- Relative motion demonstrations

### Forces
- Free body diagrams
- Newton's laws visualizations
- Friction and tension forces

### Energy
- Kinetic and potential energy
- Conservation of energy
- Work-energy theorem

### Momentum
- Collision simulations
- Impulse visualization
- Conservation of momentum

## Electromagnetism Animations

### Electrostatics
- Electric field lines
- Coulomb's law forces
- Equipotential surfaces

### Circuits
- Current flow visualization
- Series and parallel circuits
- Ohm's law demonstrations

### Magnetism
- Magnetic field patterns
- Force on moving charges
- Electromagnets

### Electromagnetic Induction
- Faraday's law
- Lenz's law
- AC generator animation

## Optics Animations

### Reflection
- Law of reflection
- Plane and curved mirrors
- Image formation

### Refraction
- Snell's law
- Total internal reflection
- Refractive index effects

### Lenses
- Converging/diverging lenses
- Ray diagrams
- Image formation

### Waves
- Wave properties
- Interference patterns
- Diffraction effects

## Usage with Animation Engine

```typescript
import { AnimationEngine } from '@visualverse/engine';

const engine = new AnimationEngine();
const scene = engine.createScene();

const physicsAnimations = new PhysicsAnimations(scene);
physicsAnimations.animateCircuit({
  components: ['battery', 'resistor1', 'resistor2'],
  showCurrent: true,
  voltage: 12,
});
```

## License

Licensed under the Apache License, Version 2.0. See `/LICENSE` for details.
