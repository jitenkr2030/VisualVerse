# Creator Portal - Components Module

## Overview
This module provides reusable UI components for the VisualVerse Creator Portal. It includes canvas controls, timeline editors, toolbars, and common atomic components used throughout the creator experience.

## License
**PROPRIETARY** - This module is part of VisualVerse's institutional/enterprise offering. See `/PROPRIETARY_LICENSE.md` for licensing terms.

## Module Structure

```
components/
├── Canvas/
│   ├── AnimationCanvas.tsx
│   ├── CanvasToolbar.tsx
│   ├── LayerPanel.tsx
│   └── PropertyPanel.tsx
├── Timeline/
│   ├── Timeline.tsx
│   ├── Track.tsx
│   ├── Keyframe.tsx
│   ├── Playhead.tsx
│   └── TimelineZoom.tsx
├── Toolbar/
│   ├── ToolSelector.tsx
│   ├── ShapeTools.tsx
│   ├── TextTools.tsx
│   └── TransformTools.tsx
├── Common/
│   ├── Button.tsx
│   ├── Input.tsx
│   ├── Modal.tsx
│   ├── Dropdown.tsx
│   └── Tooltip.tsx
└── index.ts
```

## Quick Start

```typescript
import { AnimationCanvas } from './components/Canvas/AnimationCanvas';
import { Timeline } from './components/Timeline/Timeline';

function EditorWorkspace() {
  return (
    <div className="editor-workspace">
      <AnimationCanvas />
      <Timeline />
    </div>
  );
}
```

## Component Categories

### Canvas Components
- **AnimationCanvas**: Main drawing and preview area
- **CanvasToolbar**: Tools for canvas manipulation
- **LayerPanel**: Layer visibility and ordering controls
- **PropertyPanel**: Object property editing

### Timeline Components
- **Timeline**: Main timeline visualization
- **Track**: Individual animation tracks
- **Keyframe**: Keyframe markers
- **Playhead**: Current time indicator
- **TimelineZoom**: Zoom controls

### Toolbar Components
- **ToolSelector**: Tool selection interface
- **ShapeTools**: Shape creation tools
- **TextTools**: Text editing tools
- **TransformTools**: Transform operations

### Common Components
- **Button**: Reusable button with variants
- **Input**: Text input with validation
- **Modal**: Dialog overlays
- **Dropdown**: Select dropdowns
- **Tooltip**: Information hints

## License

This module is licensed under the VisualVerse Proprietary License. See `/PROPRIETARY_LICENSE.md` for details.
