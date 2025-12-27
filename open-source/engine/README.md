# VisualVerse Engine - Open Source Components

**License:** Apache 2.0  
**Repository:** https://github.com/visualverse/visualverse

## Open Source Components

The following components are licensed under Apache 2.0 and are free to use, modify, and distribute:

### ✅ Animation Engine (`engine/animation-engine/`)

The core rendering and animation engine for VisualVerse.

- `core/` - Scene base classes, camera, timeline, renderer
- `primitives/` - Geometry, text, layout elements
- `exporters/` - FFmpeg, GIF, image export capabilities
- `themes/` - Base themes (light mode, dark mode)
- `validation/` - Scene validation logic

### ✅ Common Utilities (`engine/common/`)

Shared utilities and base schemas for the platform.

- `schemas/` - JSON schemas for concepts, lessons, animations
- `utils/` - File operations, string utilities, time utilities
- `logging/` - Standardized logging utilities
- `auth/` - Basic permission definitions

### ✅ Content Metadata (`engine/content-metadata/`)

FastAPI service for managing educational content metadata.

- `models/` - SQLAlchemy models for subjects, concepts
- `routes/` - REST API endpoints
- `services/` - Business logic for content management
- `migrations/` - Database migration scripts

## Usage

```python
from visualverse.animation_engine import Scene, Rectangle
from visualverse.common import BaseResponse
from visualverse.content_metadata import Subject, Concept
```

## Contributing

Contributions are welcome! Please see our contributing guidelines at:
https://github.com/visualverse/visualverse/blob/main/CONTRIBUTING.md

## Support

For issues and questions related to open-source components:
- GitHub Issues: https://github.com/visualverse/visualverse/issues
- Discord: https://discord.gg/visualverse

## Copyright

Copyright 2025 VisualVerse Contributors.
See LICENSE file for full license information.
