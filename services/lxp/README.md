# Learner Experience Platform (LXP)

## Overview

The VisualVerse Learner Experience Platform (LXP) is a comprehensive, visual-first learning environment that provides personalized educational experiences for students across K-12, higher education, and professional training levels. The platform integrates interactive visualizations from the VisualVerse vertical services with advanced progress tracking, AI-driven recommendations, and adaptive learning paths.

## Architecture

The LXP follows a modern microservices-inspired architecture with clear separation of concerns:

### Core Components

**1. Progress Tracking System**
- Persistent tracking of learner progress across content
- Concept mastery evaluation with multiple metrics
- Achievement and gamification system
- Milestone tracking and reporting

**2. Learning Analytics Engine**
- Real-time event tracking and analysis
- Learning pattern detection
- Engagement metrics and insights
- Predictive analytics for outcomes

**3. Personalized Recommendations**
- AI-driven content recommendations
- Adaptive learning path generation
- Difficulty adjustment based on performance
- Interest profiling and preference learning

**4. Multi-Level Support**
- K-12 curriculum alignment
- Higher education content organization
- Professional and corporate training paths
- Adaptive scaffolding with graduated difficulty
- Multi-language internationalization

## Project Structure

```
visualverse-lxp/
├── apps/
│   ├── web-student/              # Next.js Student Application
│   │   ├── components/           # React components
│   │   │   ├── dashboard/        # Dashboard widgets
│   │   │   ├── player/           # Visualization player
│   │   │   ├── discovery/        # Content browser
│   │   │   ├── progress/         # Progress visualization
│   │   │   └── shared/           # Shared UI components
│   │   ├── pages/                # Next.js pages
│   │   ├── lib/                  # Utilities
│   │   ├── hooks/                # Custom React hooks
│   │   ├── styles/               # Global styles
│   │   └── public/               # Static assets
│   │
│   └── service-api/              # FastAPI Backend
│       ├── app/
│       │   ├── api/              # API endpoints
│       │   │   └── v1/
│       │   ├── core/             # Core configuration
│       │   ├── models/           # Database models
│       │   ├── schemas/          # Pydantic schemas
│       │   ├── services/         # Business logic
│       │   └── middleware/       # Auth, logging, etc.
│       └── tests/                # API tests
│
├── services/
│   ├── progress/                 # Progress tracking service
│   ├── analytics/                # Learning analytics service
│   ├── recommendations/          # Recommendation engine
│   └── multi-level/              # Multi-level support
│
├── packages/
│   ├── ui-kit/                   # Shared UI components
│   └── design-tokens/            # Design tokens
│
├── docs/                         # Documentation
├── scripts/                      # Utility scripts
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── package.json
└── README.md
```

## Installation

### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL 14+
- Redis 7+
- Git

### Setup

```bash
# Clone the repository
git clone https://github.com/visualverse/lxp.git
cd lxp

# Install backend dependencies
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Install frontend dependencies
cd apps/web-student
npm install
cd ../..

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# Initialize database
cd apps/service-api
alembic upgrade head
cd ../..

# Start services
docker-compose up -d
```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | postgresql://user:pass@localhost:5432/lxp |
| `REDIS_URL` | Redis connection string | redis://localhost:6379/0 |
| `JWT_SECRET` | JWT signing secret | - |
| `STRIPE_SECRET_KEY` | Stripe API key | - |
| `STORAGE_DIR` | Local storage directory | /tmp/visualverse-lxp |
| `LOG_LEVEL` | Logging level | INFO |

### Database Schema

The LXP uses PostgreSQL with the following core tables:

- `users` - User accounts and profiles
- `concepts` - Learning concepts and topics
- `learning_objects` - Content items (visualizations)
- `user_progress` - Progress records
- `sessions` - Learning sessions
- `achievements` - Achievement records
- `competency_snapshots` - Competency evaluations
- `learning_events` - Analytics events
- `recommendations` - Generated recommendations

## API Reference

### Progress Endpoints

```
GET    /api/v1/progress/{user_id}           - Get user progress
POST   /api/v1/progress/{user_id}/session   - Record session
PUT    /api/v1/progress/{user_id}/concept   - Update concept progress
GET    /api/v1/progress/{user_id}/report    - Get progress report
GET    /api/v1/progress/{user_id}/achievements - Get achievements
```

### Analytics Endpoints

```
POST   /api/v1/analytics/event              - Track learning event
GET    /api/v1/analytics/{user_id}/patterns - Get learning patterns
GET    /api/v1/analytics/{user_id}/engagement - Get engagement metrics
GET    /api/v1/analytics/{user_id}/report   - Get analytics report
```

### Recommendations Endpoints

```
GET    /api/v1/recommendations/{user_id}    - Get recommendations
GET    /api/v1/recommendations/path/{user_id} - Get learning path
POST   /api/v1/recommendations/feedback     - Submit feedback
```

### Multi-Level Endpoints

```
GET    /api/v1/levels                        - List education levels
GET    /api/v1/levels/{level}/config         - Get level config
GET    /api/v1/levels/{level}/path           - Get learning path
PUT    /api/v1/profile/{user_id}             - Update profile
GET    /api/v1/profile/{user_id}             - Get profile
```

## Frontend Development

### Tech Stack

- **Framework**: Next.js 14 with TypeScript
- **Styling**: Tailwind CSS
- **State Management**: React Context + Zustand
- **Data Fetching**: React Query (TanStack Query)
- **Charts**: Recharts
- **Visualization**: D3.js
- **Testing**: Jest + React Testing Library
- **E2E Testing**: Playwright

### Component Structure

```
components/
├── dashboard/
│   ├── ProgressOverview.tsx
│   ├── StreakWidget.tsx
│   ├── RecentActivity.tsx
│   └── DailyGoal.tsx
├── player/
│   ├── VisualizationPlayer.tsx
│   ├── Controls.tsx
│   ├── Timeline.tsx
│   └── Annotations.tsx
├── discovery/
│   ├── ContentBrowser.tsx
│   ├── SearchFilters.tsx
│   └── ContentCard.tsx
├── progress/
│   ├── ProgressChart.tsx
│   ├── SkillTree.tsx
│   ├── AchievementBadge.tsx
│   └── MasteryGauge.tsx
└── shared/
    ├── Button.tsx
    ├── Modal.tsx
    ├── Toast.tsx
    └── Loading.tsx
```

### Running Frontend

```bash
cd apps/web-student
npm run dev
# Open http://localhost:3000
```

## Backend Development

### Tech Stack

- **Framework**: FastAPI
- **Database**: SQLAlchemy with PostgreSQL
- **Caching**: Redis
- **Authentication**: JWT with refresh tokens
- **Testing**: Pytest
- **Documentation**: Auto-generated OpenAPI

### Running Backend

```bash
cd apps/service-api
uvicorn app.main:app --reload
# API docs at http://localhost:8000/docs
```

## Testing

### Backend Tests

```bash
cd apps/service-api
pytest tests/ -v --cov
```

### Frontend Tests

```bash
cd apps/web-student
npm test
npm run test:e2e
```

### Integration Tests

```bash
docker-compose -f docker-compose.test.yml up
```

## Deployment

### Production Build

```bash
# Backend
cd apps/service-api
docker build -t visualverse-lxp-api .

# Frontend
cd apps/web-student
npm run build
docker build -t visualverse-lxp-web .
```

### Docker Compose

```bash
docker-compose up -d
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes
4. Run tests
5. Submit pull request

## License

MIT License - see LICENSE file for details.

## Support

- Documentation: https://docs.visualverse.io/lxp
- Discord: https://discord.gg/visualverse
- Email: support@visualverse.io

---

Built with ❤️ for learners everywhere
