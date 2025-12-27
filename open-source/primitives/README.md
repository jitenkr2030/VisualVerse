# Visual Primitives Library

> Standard visual elements for educational content.

This library provides a collection of reusable visual components that work across all VisualVerse verticals (Math, Physics, Chemistry, Algorithms, Finance).

---

## Categories

### Geometric Shapes
- Basic shapes (circle, square, triangle, rectangle)
- Polygons and regular polygons
- Path-based shapes
- 3D primitives

### Mathematical Notation
- Equations and formulas
- Mathematical symbols
- Matrix representations
- Set notation

### Graphs & Charts
- Function plots
- Bar charts and pie charts
- Histograms
- Network graphs

### Timelines & Sequences
- Number lines
- Time axes
- Step visualizations
- Flowchart elements

### Data Visualization
- Statistical charts
- Scatter plots
- Heatmaps
- Tree diagrams

---

## Usage

```python
from visualverse.primitives import Circle, Square, NumberLine

# Create geometric shapes
circle = Circle(radius=1, color=BLUE)
square = Square(side_length=2, color=RED)

# Create mathematical primitives
number_line = NumberLine(x_range=[-5, 5], unit_length=0.5)

# Combine in a scene
scene.add(circle, square, number_line)
```

---

## Standards

All primitives follow these principles:

1. **Accessibility** - WCAG 2.1 compliant colors
2. **Responsiveness** - Scale to different contexts
3. **Themeable** - Support light/dark modes
4. **Exportable** - Work with all export targets

---

## License

Apache 2.0 - See [LICENSE](../../LICENSE)
