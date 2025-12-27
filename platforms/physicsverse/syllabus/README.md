# PhysicsVerse - Syllabus Module

## Overview
This module defines the curriculum structure and lesson content for PhysicsVerse, covering mechanics, electromagnetism, and optics topics.

## License
**Apache 2.0** - This module is open source under the Apache License 2.0. See `/LICENSE` for terms.

## Directory Structure

```
syllabus/
├── manifest.json          # Curriculum structure
├── content/
│   ├── mechanics/
│   │   ├── kinematics.md
│   │   ├── forces.md
│   │   ├── energy.md
│   │   └── momentum.md
│   ├── electromagnetism/
│   │   ├── electrostatics.md
│   │   ├── circuits.md
│   │   ├── magnetism.md
│   │   └── induction.md
│   └── optics/
│       ├── reflection.md
│       ├── refraction.md
│       ├── lenses.md
│       └── waves.md
├── assessments/
│   ├── quizzes.json
│   └── problems.json
└── README.md
```

## Curriculum Structure (manifest.json)

```json
{
  "title": "PhysicsVerse Curriculum",
  "version": "1.0.0",
  "levels": [
    {
      "id": "mechanics-basics",
      "title": "Mechanics Basics",
      "order": 1,
      "duration": "6 weeks",
      "topics": [
        {
          "id": "kinematics",
          "title": "Kinematics",
          "lessons": ["motion-terms", "velocity-acceleration", "projectile-motion"],
          "animations": ["mechanics/kinematics"],
          "assessments": ["quiz-kinematics"]
        }
      ]
    }
  ]
}
```

## Content Format

Lessons are written in Markdown with embedded animation references:

```markdown
# Projectile Motion

## Learning Objectives
- Understand the independence of horizontal and vertical motion
- Calculate trajectory of projectiles
- Analyze range and maximum height

## Concept: What is Projectile Motion?

Projectile motion is the motion of an object thrown into the air, subject to only the acceleration of gravity.

<animation src="mechanics/kinematics.ts" 
           type="interactive"
           params='{"showVectors": true, "angle": 45, "velocity": 20}' />

## The Physics

The horizontal and vertical motions are independent:

**Horizontal Motion:**
- Initial velocity: v₀ × cos(θ)
- Acceleration: 0
- Position: x = v₀ × cos(θ) × t

**Vertical Motion:**
- Initial velocity: v₀ × sin(θ)
- Acceleration: -g (gravity)
- Position: y = v₀ × sin(θ) × t - ½gt²

<animation src="mechanics/kinematics.ts" 
           type="breakdown"
           params='{"showComponents": true}' />

## Equations of Motion

1. x = v₀ × cos(θ) × t
2. y = v₀ × sin(θ) × t - ½gt²
3. vx = v₀ × cos(θ)
4. vy = v₀ × sin(θ) - gt

## Summary
- Horizontal and vertical motions are independent
- Gravity affects only the vertical component
- Trajectory is parabolic
```

## License

Licensed under the Apache License, Version 2.0. See `/LICENSE` for details.
