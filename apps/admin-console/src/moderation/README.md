# Admin Console - Moderation Module

## Overview
This module provides content moderation tools for the VisualVerse platform. It enables administrators to review reported content, manage user bans, and maintain platform quality standards.

## License
**PROPRIETARY** - This module is part of VisualVerse's institutional/enterprise offering. See `/PROPRIETARY_LICENSE.md` for licensing terms.

## Module Structure

```
moderation/
├── components/
│   ├── ReportedContentQueue.tsx
│   ├── UserBanTools.tsx
│   ├── ContentReview.tsx
│   ├── ModerationHistory.tsx
│   └── AutoModerationSettings.tsx
├── hooks/
│   ├── useModeration.ts
│   ├── useContentQueue.ts
│   └── useUserActions.ts
├── services/
│   └── moderationService.ts
├── types/
│   └── moderation.types.ts
├── utils/
│   ├── autoModeration.ts
│   └── severityLevels.ts
└── index.ts
```

## Quick Start

```typescript
import { ModerationProvider } from './moderation';
import { ReportedContentQueue } from './components/ReportedContentQueue';

function ModerationConsole() {
  return (
    <ModerationProvider>
      <ReportedContentQueue />
    </ModerationProvider>
  );
}
```

## Features

- **Content Queue Management**: Review and act on reported content
- **User Ban Tools**: Temporary and permanent user suspension
- **Auto-Moderation**: AI-assisted content flagging and classification
- **Moderation History**: Audit trail for all moderation actions
- **Bulk Actions**: Mass approve/reject capabilities for efficiency
- **Escalation Workflow**: Route complex cases to senior moderators

## Moderation Actions

The module supports the following actions:
- **Approve**: Content is acceptable, report dismissed
- **Reject**: Content violates guidelines, removed
- **Warn**: User receives warning for minor violations
- **Suspend**: Temporary account suspension (configurable duration)
- **Ban**: Permanent account termination for severe violations

## API Integration

The moderation module integrates with:
- Content reporting API endpoints
- User management service
- Notification service for alerts
- External AI moderation services (optional)

## License

This module is licensed under the VisualVerse Proprietary License. See `/PROPRIETARY_LICENSE.md` for details.
