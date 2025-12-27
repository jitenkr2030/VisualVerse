# VisualVerse Open-Source Core

> **Open where trust matters. Build what educates.**

This directory contains VisualVerse's open-source components that form the **Community Trust Layer**. These components are freely available, auditable, and forkable under the Apache 2.0 license.

---

## Directory Structure

```
open-source/
├── engine/           ← Core visual animation engine (Manim-based)
├── primitives/       ← Standard visual elements library
├── schemas/          ← Content schemas & knowledge models
└── samples/          ← Demo animations & onboarding content
```

---

## Open-Source Components

### 1. Visual Engine (`engine/`)

The heart of VisualVerse - a deterministic, script-based animation engine for creating educational visuals.

**Features:**
- Manim-based rendering
- Mathematical precision & repeatability
- Version-controlled outputs
- Export to video, frames, interactive HTML

**Usage:**
```python
from visualverse.engine import Scene, Square, FadeIn

class ExampleScene(Scene):
    def construct(self):
        square = Square()
        self.play(FadeIn(square))
```

---

### 2. Visual Primitives (`primitives/`)

Standard library of visual elements used across all verticals.

**Includes:**
- Shapes (geometric, path-based)
- Graphs & charts
- Timelines & sequences
- Mathematical notation
- Charts & data visualization

**Purpose:**
- Ensures visual consistency across platforms
- Reduces duplication across subjects
- Enables third-party tooling

---

### 3. Content Schemas (`schemas/`)

JSON schemas and TypeScript interfaces defining knowledge structures.

**Schemas:**
- `concept.schema.json` - Knowledge concept definition
- `lesson.schema.json` - Lesson structure
- `animation.schema.json` - Animation metadata
- `curriculum.schema.json` - Curriculum mapping

**Purpose:**
- Defines what knowledge looks like
- Enables external integrations
- Makes VisualVerse a platform standard

---

### 4. Sample Content (`samples/`)

Demo animations and example content for each vertical.

**Includes:**
- Intro MathVerse examples
- Basic Physics simulations
- Chemistry introduction visuals
- Algorithm flow examples
- Financial concept demos

**Purpose:**
- Demonstrates engine capabilities
- Enables quick experimentation
- Encourages educator adoption

---

## License

All components in this directory are licensed under **Apache 2.0**.

See [LICENSE](../LICENSE) for details.

---

## Contributing

Contributions are welcome! Please read our [CONTRIBUTING.md](../CONTRIBUTING.md) guidelines before submitting PRs.

---

## Community

- **GitHub**: https://github.com/visualverse/visualverse
- **Documentation**: https://docs.visualverse.dev
- **Discord**: https://discord.gg/visualverse

---

> **Note:** This is the open-source foundation of VisualVerse. For paid features (advanced learning intelligence, full vertical content, institutional tools), see the `platforms/`, `services/`, and `apps/` directories.
