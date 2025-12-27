# Creator Portal - Styles Module

## Overview
This module provides styling configuration and CSS utilities for the VisualVerse Creator Portal. It includes global styles, design tokens, and CSS animations.

## License
**PROPRIETARY** - This module is part of VisualVerse's institutional/enterprise offering. See `/PROPRIETARY_LICENSE.md` for licensing terms.

## Module Structure

```
styles/
├── globals.css          # Global styles and resets
├── variables.css        # CSS custom properties
├── theme.ts             # TypeScript theme configuration
├── animations.css       # CSS keyframe animations
├── utilities.css        # Utility classes
├── components.css       # Component-specific styles
└── index.css            # Main stylesheet entry
```

## Quick Start

```typescript
import './styles/index.css';
import { theme } from './styles/theme';

function App() {
  return (
    <div className="app" data-theme={theme.mode}>
      {/* Application content */}
    </div>
  );
}
```

## Design System

### Color Palette
- **Primary**: `#2563eb` (Blue)
- **Secondary**: `#7c3aed` (Purple)
- **Success**: `#10b981` (Green)
- **Warning**: `#f59e0b` (Amber)
- **Error**: `#ef4444` (Red)
- **Neutral**: Slate gray scale

### Typography
- **Font Family**: Inter, system-ui, sans-serif
- **Heading**: Bold weights (700-800)
- **Body**: Regular weights (400-500)
- **Monospace**: JetBrains Mono for code

### Spacing
- Base unit: 4px
- Scale: 4px, 8px, 12px, 16px, 24px, 32px, 48px, 64px

### Border Radius
- **Small**: 4px
- **Medium**: 8px
- **Large**: 12px
- **Full**: 9999px (circles/pills)

## CSS Custom Properties

```css
:root {
  --color-primary: #2563eb;
  --color-primary-hover: #1d4ed8;
  --color-secondary: #7c3aed;
  --color-success: #10b981;
  --color-warning: #f59e0b;
  --color-error: #ef4444;
  
  --font-family: 'Inter', system-ui, sans-serif;
  --font-mono: 'JetBrains Mono', monospace;
  
  --spacing-xs: 4px;
  --spacing-sm: 8px;
  --spacing-md: 16px;
  --spacing-lg: 24px;
  --spacing-xl: 32px;
  
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 12px;
  
  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.1);
  --shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.1);
}
```

## Animations

- **Fade In**: Opacity transition (0.2s)
- **Fade Out**: Opacity transition (0.2s)
- **Slide Up**: Transform Y transition (0.3s)
- **Slide Down**: Transform Y transition (0.3s)
- **Scale**: Transform scale transition (0.2s)
- **Pulse**: Keyframe animation (2s infinite)
- **Spin**: Rotate animation (1s linear)

## License

This module is licensed under the VisualVerse Proprietary License. See `/PROPRIETARY_LICENSE.md` for details.
