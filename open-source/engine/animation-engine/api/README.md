# VisualVerse Animation Engine - API

## Overview
This module provides the public API for the VisualVerse Animation Engine. It defines types, interfaces, and core functionality available to consumers of the engine.

## License
**Apache 2.0** - This module is open source under the Apache License 2.0. See `/LICENSE` for terms.

## Module Structure

```
api/
├── types.ts              # Core type definitions
├── IRenderer.ts          # Rendering interface
├── IAnimation.ts         # Animation interface
├── IVisualObject.ts      # Visual object interface
├── IKeyframe.ts          # Keyframe interface
├── IEventBus.ts          # Event system interface
├── IPluginSystem.ts      # Plugin architecture interface
├── IExport.ts            # Export interface
└── index.ts              # Public API exports
```

## Quick Start

```typescript
import { 
  AnimationEngine, 
  VisualObject, 
  Keyframe,
  Renderer 
} from './api';

const engine = new AnimationEngine();
const scene = engine.createScene();
```

## Core Types

### AnimationEngine
Main class for creating and managing animations.

### VisualObject
Base class for all visual elements (shapes, text, images).

### Keyframe
Represents a point in animation with interpolated values.

### Renderer
Interface for rendering implementations.

## Event System

The engine uses an event bus for communication:

```typescript
engine.on('play', (event) => {
  console.log('Animation started:', event.target);
});

engine.emit('pause', { timestamp: Date.now() });
```

## Plugin System

Extend the engine with plugins:

```typescript
engine.registerPlugin('customRenderer', new CustomRenderer());
```

## License

Licensed under the Apache License, Version 2.0. See `/LICENSE` for details.
