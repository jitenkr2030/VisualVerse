# Sample Content

> Demo animations and example content for the VisualVerse open-source engine.

This directory contains sample content demonstrating the capabilities of the VisualVerse animation engine across different verticals.

---

## Directories

### `mathverse/`
Introductory math concepts:
- Basic algebra
- Geometry fundamentals
- Calculus introduction
- Linear algebra basics

### `physicsverse/`
Basic physics simulations:
- Motion and kinematics
- Simple forces
- Wave mechanics
- Basic optics

### `chemverse/`
Introductory chemistry:
- Atomic structure
- Basic bonding
- Simple reactions
- Molecular shapes

### `algverse/`
Algorithm fundamentals:
- Sorting algorithms
- Data structure basics
- Graph traversal
- Recursion visualization

### `finverse/`
Financial concepts:
- Compound interest
- Basic risk modeling
- Portfolio visualization
- Market dynamics

---

## Usage

Run samples to see the engine in action:

```bash
# Run all samples
python samples/run_all.py

# Run specific vertical
python samples/mathverse/run.py

# Generate video output
python samples/mathverse/generate.py --output video
```

---

## Creating New Samples

1. Create a new directory for your topic
2. Add a `sample.py` file with your animation
3. Include a `README.md` explaining the concept
4. Add metadata in `__init__.py`

Example:

```python
from visualverse.engine import Scene, Circle, FadeIn

class BasicCircleScene(Scene):
    def construct(self):
        circle = Circle(radius=1)
        self.play(FadeIn(circle))
```

---

## Contribution

Contribute your own samples! See [CONTRIBUTING.md](../../CONTRIBUTING.md).

---

## License

Apache 2.0 - See [LICENSE](../../LICENSE)
