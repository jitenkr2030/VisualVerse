# VisualVerse Student App

The Student App is a React-based single-page application built with Vite, TypeScript, and TailwindCSS. It provides students with an interactive learning platform featuring video lessons, progress tracking, achievements, and more.

## Tech Stack

- **Framework**: React 18 with TypeScript
- **Build Tool**: Vite 5
- **Styling**: TailwindCSS 3.4
- **State Management**: Zustand
- **Routing**: React Router DOM 6
- **HTTP Client**: Axios
- **Icons**: Lucide React
- **Animations**: Framer Motion

## Project Structure

```
src/
├── assets/              # Static assets (images, fonts, etc.)
├── components/
│   ├── auth/           # Authentication components
│   ├── common/         # Reusable UI components
│   └── layout/         # Layout components
├── hooks/              # Custom React hooks
├── pages/
│   ├── auth/          # Authentication pages
│   └── student/       # Student-facing pages
├── services/          # API services
├── store/             # Zustand state stores
├── types/             # TypeScript type definitions
└── utils/             # Utility functions
```

## Getting Started

### Prerequisites

- Node.js 18+
- npm or yarn

### Installation

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## Key Features

- **Authentication**: Login, registration, password reset
- **Dashboard**: Learning stats, recent courses, daily goals
- **Course Catalog**: Browse and search courses by category/difficulty
- **Video Lessons**: Interactive video player with progress tracking
- **Progress Tracking**: Track lesson completion, quiz scores, learning streaks
- **Achievements**: Unlock badges for reaching milestones
- **Responsive Design**: Optimized for desktop and mobile devices

## Environment Variables

Create a `.env` file in the root directory:

```env
VITE_API_URL=http://localhost:8000/api
VITE_WS_URL=ws://localhost:8000/ws
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run lint` - Run ESLint
- `npm run preview` - Preview production build
