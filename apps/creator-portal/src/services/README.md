# Creator Portal - Services Module

## Overview
This module provides API services for the VisualVerse Creator Portal. It includes HTTP clients, project management, asset handling, and authentication services.

## License
**PROPRIETARY** - This module is part of VisualVerse's institutional/enterprise offering. See `/PROPRIETARY_LICENSE.md` for licensing terms.

## Module Structure

```
services/
├── api/
│   ├── apiClient.ts      # Base HTTP client with interceptors
│   ├── endpoints.ts      # API endpoint definitions
│   └── errorHandler.ts   # Centralized error handling
├── projectService.ts     # Project CRUD operations
├── assetService.ts       # Asset upload/download handling
├── userService.ts        # User authentication and profile
├── exportService.ts      # Export and rendering services
├── collaborationService.ts  # Real-time collaboration
└── analyticsService.ts   # Usage analytics tracking
```

## Quick Start

```typescript
import { apiClient } from './services/apiClient';
import { projectService } from './services/projectService';

const client = apiClient.create({
  baseURL: process.env.API_URL,
  timeout: 30000,
});

// Fetch user projects
const projects = await projectService.getProjects();
```

## Services

### apiClient
- Base HTTP client configuration
- Request/response interceptors
- Authentication token management
- Error transformation

### projectService
- `getProjects()`: List all user projects
- `getProject(id)`: Get single project details
- `createProject(data)`: Create new project
- `updateProject(id, data)`: Update project
- `deleteProject(id)`: Remove project
- `duplicateProject(id)`: Clone existing project

### assetService
- `uploadAsset(file)`: Upload media assets
- `getAsset(id)`: Retrieve asset
- `deleteAsset(id)`: Remove asset
- `getAssetUrl(id)`: Get CDN URL for asset

### userService
- `login(credentials)`: User authentication
- `logout()`: Clear session
- `getProfile()`: Get user profile
- `updateProfile(data)`: Update profile

### exportService
- `requestExport(projectId, options)`: Request rendering
- `getExportStatus(jobId)`: Check render progress
- `downloadExport(jobId)`: Download rendered file

### collaborationService
- `joinRoom(projectId)`: Join collaboration session
- `leaveRoom(roomId)`: Exit session
- `broadcastChanges(change)`: Send updates
- `subscribeToChanges(callback)`: Receive updates

## License

This module is licensed under the VisualVerse Proprietary License. See `/PROPRIETARY_LICENSE.md` for details.
