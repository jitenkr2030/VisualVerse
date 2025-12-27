# ChemVerse - Animations Module

## Overview
This module contains chemistry animation modules for VisualVerse. It provides visualizations for organic, inorganic, and physical chemistry concepts using the Animation Engine.

## License
**Apache 2.0** - This module is open source under the Apache License 2.0. See `/LICENSE` for terms.

## Directory Structure

```
animations/
├── organic/
│   ├── hydrocarbons.ts
│   ├── functional-groups.ts
│   └── reactions.ts
├── inorganic/
│   ├── periodic-table.ts
│   ├── bonding.ts
│   └── coordination.ts
├── physical/
│   ├── thermodynamics.ts
│   ├── kinetics.ts
│   └── equilibrium.ts
├── index.ts
└── README.md
```

## Quick Start

```typescript
import { 
  animateBondFormation, 
  animateReaction,
  animateMolecule 
} from './animations';

const animation = animateMolecule({
  formula: 'H₂O',
  style: 'ball-and-stick',
  showBonds: true,
});
```

## Organic Chemistry Animations

### Hydrocarbons
- Structural formulas
- Isomer visualization
- Naming conventions

### Functional Groups
- Alcohols, ketones, aldehydes
- Carboxylic acids and esters
- Amines and amides

### Reactions
- Substitution reactions
- Addition reactions
- Elimination mechanisms

## Inorganic Chemistry Animations

### Periodic Table
- Element properties trends
- Electron configurations
- Periodic trends

### Bonding
- Ionic bonding
- Covalent bonding
- Metallic bonding

### Coordination Chemistry
- Coordination complexes
- Ligand exchange
- Crystal field theory

## Physical Chemistry Animations

### Thermodynamics
- Heat transfer
- Entropy changes
- Gibbs free energy

### Kinetics
- Reaction rates
- Activation energy
- Catalysis mechanisms

### Equilibrium
- Le Chatelier's principle
- Equilibrium shifts
- Solubility equilibrium

## Usage with Animation Engine

```typescript
import { AnimationEngine } from '@visualverse/engine';

const engine = new AnimationEngine();
const scene = engine.createScene();

const chemistryAnimations = new ChemistryAnimations(scene);
chemistryAnimations.animateReaction({
  reactants: ['CH₄', 'O₂'],
  products: ['CO₂', 'H₂O'],
  mechanism: 'combustion',
});
```

## License

Licensed under the Apache License, Version 2.0. See `/LICENSE` for details.
