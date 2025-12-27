# Animation Engine

The Animation Engine is the core component responsible for rendering educational animations using Manim. This module provides a clean, abstracted interface for creating mathematical and scientific visualizations.

## Architecture

### Core Components

- **`core/`** - Core rendering infrastructure
  - `renderer.py` - Main rendering engine interface
  - `scene_base.py` - Abstract base class for all scenes
  - `camera.py` - Camera control and positioning
  - `timeline.py` - Animation timeline management

- **`primitives/`** - Basic visual elements
  - `shapes.py` - Geometric shapes and forms
  - `graphs.py` - Graph structures and plotting
  - `vectors.py` - Vector mathematics and visualization
  - `axes.py` - Coordinate systems and axes

- **`themes/`** - Visual themes and styling
  - `default_theme.py` - Standard educational theme
  - `dark_theme.py` - Dark mode for presentations
  - `accessibility_theme.py` - High contrast accessibility theme

- **`exporters/`** - Output format handlers
  - `video_exporter.py` - MP4 video export
  - `gif_exporter.py` - GIF animation export
  - `frame_exporter.py` - Individual frame export

- **`validation/`** - Content validation
  - `script_validator.py` - Animation script validation

- **`api/`** - External interfaces
  - `render_api.py` - REST API for rendering services

## Usage

```python
from visualverse.engine.animation_engine import AnimationEngine
from visualverse.engine.animation_engine.core import SceneBase

class CustomScene(SceneBase):
    def construct(self):
        # Animation logic here
        pass

engine = AnimationEngine()
result = engine.render_scene(CustomScene, "output.mp4")
```

## Dependencies

See `requirements.txt` for full dependency list.