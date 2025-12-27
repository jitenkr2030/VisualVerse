# ChemVerse - Syllabus Module

## Overview
This module defines the curriculum structure and lesson content for ChemVerse, covering organic, inorganic, and physical chemistry topics.

## License
**Apache 2.0** - This module is open source under the Apache License 2.0. See `/LICENSE` for terms.

## Directory Structure

```
syllabus/
├── manifest.json          # Curriculum structure
├── content/
│   ├── organic/
│   │   ├── hydrocarbons.md
│   │   ├── functional-groups.md
│   │   └── reactions.md
│   ├── inorganic/
│   │   ├── periodic-table.md
│   │   ├── bonding.md
│   │   └── coordination.md
│   └── physical/
│       ├── thermodynamics.md
│       ├── kinetics.md
│       └── equilibrium.md
├── assessments/
│   ├── quizzes.json
│   └── problems.json
└── README.md
```

## Curriculum Structure (manifest.json)

```json
{
  "title": "ChemVerse Curriculum",
  "version": "1.0.0",
  "levels": [
    {
      "id": "organic-basics",
      "title": "Organic Chemistry Basics",
      "order": 1,
      "duration": "8 weeks",
      "topics": [
        {
          "id": "hydrocarbons",
          "title": "Hydrocarbons",
          "lessons": ["alkanes", "alkenes", "alkynes", "aromatics"],
          "animations": ["organic/hydrocarbons"],
          "assessments": ["quiz-hydrocarbons"]
        }
      ]
    }
  ]
}
```

## Content Format

Lessons are written in Markdown with embedded animation references:

```markdown
# Hydrocarbons

## Learning Objectives
- Classify hydrocarbons by structure
- Understand naming conventions
- Visualize molecular geometry

## What are Hydrocarbons?

Hydrocarbons are organic compounds consisting only of hydrogen and carbon atoms.

<animation src="organic/hydrocarbons.ts" 
           type="interactive"
           params='{"formula": "CH₄", "style": "ball-and-stick"}' />

## Types of Hydrocarbons

### Alkanes (Single Bonds)
- General formula: CₙH₂ₙ₊₂
- Saturated hydrocarbons
- Example: Methane (CH₄)

### Alkenes (Double Bonds)
- General formula: CₙH₂ₙ
- Unsaturated hydrocarbons
- Example: Ethene (C₂H₄)

### Alkynes (Triple Bonds)
- General formula: CₙH₂ₙ₋₂
- Highly unsaturated
- Example: Ethyne (C₂H₂)

<animation src="organic/hydrocarbons.ts" 
           type="comparison"
           params='{"types": ["alkane", "alkene", "alkyne"]}' />

## Structural Isomers

Same molecular formula, different structures:

C₄H₁₀ can be:
1. n-Butane (straight chain)
2. Isobutane (branched)

<animation src="organic/hydrocarbons.ts" 
           type="isomers"
           params='{"formula": "C₄H₁₀"}' />

## Summary
- Hydrocarbons contain only C and H
- Classified by carbon-carbon bonds
- Isomers have same formula, different structure
```

## License

Licensed under the Apache License, Version 2.0. See `/LICENSE` for details.
