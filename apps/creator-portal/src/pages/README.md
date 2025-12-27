# Creator Portal - Pages Module

## Overview
This module defines the page components and routing structure for the VisualVerse Creator Portal. It includes the main editor, project dashboard, and marketplace pages.

## License
**PROPRIETARY** - This module is part of VisualVerse's institutional/enterprise offering. See `/PROPRIETARY_LICENSE.md` for licensing terms.

## Module Structure

```
pages/
├── Editor/
│   ├── AnimationEditor.tsx
│   ├── ProjectSettings.tsx
│   └── ExportDialog.tsx
├── Dashboard/
│   ├── MyProjects.tsx
│   ├── ProjectCard.tsx
│   └── NewProjectWizard.tsx
├── Marketplace/
│   ├── AssetLibrary.tsx
│   ├── TemplateBrowser.tsx
│   └── AssetPreview.tsx
├── Account/
│   ├── Profile.tsx
│   ├── Billing.tsx
│   └── Settings.tsx
└── routes.tsx
```

## Quick Start

```typescript
import { EditorPage } from './pages/Editor/AnimationEditor';
import { MyProjects } from './pages/Dashboard/MyProjects';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/editor/:projectId" element={<EditorPage />} />
        <Route path="/dashboard" element={<MyProjects />} />
      </Routes>
    </Router>
  );
}
```

## Pages

### Editor Pages
- **AnimationEditor**: Main workspace for creating animations
- **ProjectSettings**: Project configuration and metadata
- **ExportDialog**: Export options and format selection

### Dashboard Pages
- **MyProjects**: User's project library
- **ProjectCard**: Individual project display
- **NewProjectWizard**: Project creation flow

### Marketplace Pages
- **AssetLibrary**: Browse and search assets
- **TemplateBrowser**: Pre-built animation templates
- **AssetPreview**: Detailed asset view

### Account Pages
- **Profile**: User profile management
- **Billing**: Subscription and payment management
- **Settings**: Application settings

## Routing Configuration

The pages module uses React Router with lazy loading for optimal performance.

## License

This module is licensed under the VisualVerse Proprietary License. See `/PROPRIETARY_LICENSE.md` for details.
