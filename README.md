# VisualVerse - Open-Source + Enterprise Visual Learning Platform

**One Engine, Many Verticals** - VisualVerse is a **subject-agnostic visual learning engine** built on top of Manim Community, designed to create educational animations across multiple verticals (Mathematics, Physics, Computer Science, Finance, Chemistry) using a unified architecture.

## 🎯 Core Philosophy

> **Build one subject-agnostic visual learning engine, then plug in multiple subject verticals as configurations—not separate products.**
>
> **Open the engine. Charge for the infrastructure around it.**

This is the **Red Hat + GitLab + Docker model**, applied to education.

---

## ⚖️ Licensing Model

VisualVerse uses a **dual-licensing model**:

| Component | License | Price |
|-----------|---------|-------|
| **Animation Engine** | Apache 2.0 | Free |
| **Common Utilities** | Apache 2.0 | Free |
| **Content Metadata** | Apache 2.0 | Free |
| **Core Platforms** | Apache 2.0 | Free |
| **Admin Console** | Commercial | Paid |
| **Creator Portal** | Commercial | Revenue Share |
| **Student App** | Commercial | Paid |
| **Adaptive Intelligence** | Commercial | Paid |
| **Pro Content Packs** | Commercial | Paid |
| **Enterprise Infrastructure** | Commercial | Paid |

**Open-Source Components** are free to use, modify, and distribute under Apache 2.0.  
**Proprietary Components** require a commercial license. Contact `enterprise@visualverse.io`

---

## 📂 Repository Structure

```
visualverse/
├── LICENSE                    # Apache 2.0 (Open-Source Components)
├── PROPRIETARY_LICENSE.md     # Commercial License Terms
├── README.md                  # This file
├── ARCHITECTURE.md            # Detailed Architecture Documentation
│
├── ✅ engine/                 # OPEN-SOURCE (Apache 2.0)
│   ├── animation-engine/      # Core rendering and animation
│   ├── common/                # Shared utilities and schemas
│   ├── content-metadata/      # Knowledge graph & curriculum
│   ├── legacy_core/           # Legacy compatibility
│   └── 🔐 recommendation-engine/  # Mixed (Basic=Open, Advanced=Paid)
│
├── ✅ apps/                   # PROPRIETARY (Commercial License)
│   ├── admin-console/         # Institutional management platform
│   ├── creator-portal/        # Creator monetization platform
│   └── student-app/           # Student learning experience
│
├── ✅ platforms/              # MIXED LICENSING
│   ├── mathverse/            # ✅ Core (Open) / 🔐 Pro (Paid)
│   ├── physicsverse/         # ✅ Core (Open) / 🔐 Pro (Paid)
│   ├── chemverse/            # ✅ Core (Open) / 🔐 Pro (Paid)
│   ├── algverse/             # ✅ Core (Open) / 🔐 Pro (Paid)
│   └── finverse/             # 🔐 All (Paid)
│
├── ✅ docs/                   # OPEN-SOURCE (Apache 2.0)
│
└── 🔐 infrastructure/         # PROPRIETARY (Commercial License)
    ├── docker/
    ├── kubernetes/
    ├── terraform/
    ├── ci-cd/
    └── monitoring/
```

**Legend:** ✅ = Open-Source (Apache 2.0) | 🔐 = Proprietary (Commercial)

---

## 🚀 Quick Start

### For Open-Source Development

```bash
# Clone the repository
git clone https://github.com/visualverse/visualverse.git
cd visualverse

# Install engine dependencies
cd engine/animation-engine
pip install -r requirements.txt

# Run the animation engine
python -m core.scene_base

# Explore the animation engine
cd primitives
python geometry.py
```

### For Enterprise Deployment

Contact us at `enterprise@visualverse.io` for:
- Institutional licensing
- Custom deployments
- Enterprise support
- Content partnerships

---

## ✅ Open-Source Components

### Animation Engine (`engine/animation-engine/`)

The core rendering and animation engine for VisualVerse.

**Features:**
- Scene composition and rendering primitives
- Animation timeline and transformation capabilities
- Export functionality for multiple formats (MP4, GIF, images)
- Theme support for consistent visual presentation

**Usage:**
```python
from visualverse.animation_engine import Scene, Rectangle
from visualverse.animation_engine.primitives import Circle, Text

class MathLesson(Scene):
    def construct(self):
        # Create mathematical animation
        circle = Circle(radius=2)
        text = Text("VisualVerse")
        self.add(circle, text)
```

### Common Utilities (`engine/common/`)

Shared utilities and base schemas for the platform.

**Contents:**
- Base response schemas
- File operations utilities
- String and time utilities
- Logging configuration
- Basic permission definitions

### Content Metadata (`engine/content-metadata/`)

FastAPI service for managing educational content metadata.

**Features:**
- SQLAlchemy models for subjects, concepts
- REST API routes
- Database migrations
- Search service

---

## 🔐 Proprietary Components

### Admin Console (`apps/admin-console/`)

Enterprise-grade platform for managing VisualVerse deployments.

**Features:**
- Administrative dashboards
- User management and authentication
- Compliance reporting
- Analytics and insights
- Moderation capabilities

**Pricing:** ₹50,000 - ₹5,00,000 / year / institution

### Creator Portal (`apps/creator-portal/`)

Platform for content creators to publish, distribute, and monetize.

**Features:**
- Creator dashboard
- Earnings management
- Content licensing
- Distribution controls

**Model:** Revenue share (30% platform, 70% creator)

### Student App (`apps/student-app/`)

Consumer-facing application for students to access VisualVerse content.

**Features:**
- Personalized learning experience
- Progress tracking
- Cross-platform access

### Adaptive Intelligence (`engine/recommendation-engine/`)

Advanced AI-powered recommendation and adaptive learning system.

**Open-Source:** Rule-based engine (basic recommendations)

**Proprietary:**
- Collaborative filtering engine
- Content-based recommendations
- Hybrid recommendation system
- Learner profiling
- Mastery tracking algorithms

### Vertical Content Packs (`platforms/*/pro/`)

Comprehensive, curriculum-aligned content packages.

**Examples:**
- MathVerse Pro - IIT-level mathematics
- PhysicsVerse Pro - Advanced physics
- FinVerse - Professional finance content

**Pricing:** Tiered by institution size and content depth

---

## 🏗️ Architecture Overview

VisualVerse is built on a modular, enterprise-grade architecture with clear separation of concerns:

```
┌─────────────────────────────────────────────────────────────────┐
│                     STUDENT EXPERIENCE                          │
│                    (Proprietary - Paid)                         │
├─────────────────────────────────────────────────────────────────┤
│                   CREATOR PORTAL                                │
│              (Proprietary - Revenue Share)                      │
├─────────────────────────────────────────────────────────────────┤
│                  ADMIN CONSOLE                                  │
│             (Proprietary - Institutional)                       │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────┐   │
│  │           RECOMMENDATION ENGINE                          │   │
│  │    Open (Basic)  │  Proprietary (Advanced/AI)           │   │
│  └─────────────────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              ANIMATION ENGINE                            │   │
│  │                   (Apache 2.0 - Open Source)            │   │
│  │  ┌─────────┐ ┌──────────┐ ┌─────────┐ ┌────────────┐   │   │
│  │  │ Primit- │ │  Scene   │ │Export-  │ │ Validation │   │   │
│  │  │   ives  │ │  Base    │ │  ers    │ │            │   │   │
│  │  └─────────┘ └──────────┘ └─────────┘ └────────────┘   │   │
│  └─────────────────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────────────┤
│                    CONTENT METADATA                             │
│                   (Apache 2.0 - Open Source)                   │
│         Subjects │ Concepts │ Search │ API Routes              │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📚 Documentation

### Architecture Documentation
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Complete architecture overview
- **[engine/animation-engine/README.md](engine/animation-engine/README.md)** - Rendering system
- **[engine/content-metadata/README.md](engine/content-metadata/README.md)** - Knowledge graph
- **[engine/recommendation-engine/README.md](engine/recommendation-engine/README.md)** - Learning intelligence
- **[PROPRIETARY_LICENSE.md](PROPRIETARY_LICENSE.md)** - Commercial licensing terms

### API Documentation
- **Content Metadata API**: `http://localhost:8001/docs`
- **Recommendation Engine API**: `http://localhost:8002/docs`

---

## 🛠️ Technology Stack

### Core Technologies
- **Python 3.11+**: Modern async/await support
- **Manim**: Mathematical animation rendering
- **FastAPI**: High-performance REST APIs
- **Pydantic**: Data validation and serialization

### Infrastructure
- **Docker**: Containerization
- **Kubernetes**: Container orchestration
- **Terraform**: Infrastructure as Code

### Frontend Technologies
- **React**: User interface framework
- **TypeScript**: Type-safe development

---

## 🤝 Contributing

Contributions to **open-source components** are welcome! Please see our contributing guidelines at:
https://github.com/visualverse/visualverse/blob/main/CONTRIBUTING.md

**Note:** Proprietary components do not accept external contributions.

---

## 📞 Support & Contact

- **GitHub Issues:** For open-source engine issues
- **Enterprise Sales:** `enterprise@visualverse.io`
- **Documentation:** `/docs/`
- **Discord:** Join our community server

---

## 📄 License

**VisualVerse is dual-licensed:**

- **Open-Source Components:** Licensed under Apache 2.0
  - See [LICENSE](LICENSE) file for details
  - Animation engine, common utilities, content metadata, core platforms

- **Proprietary Components:** Commercial License
  - See [PROPRIETARY_LICENSE.md](PROPRIETARY_LICENSE.md) for details
  - Admin console, creator portal, student app, advanced recommendations, pro content

---

**VisualVerse** - Democratizing Education Through Animation

*One Engine, Many Verticals*
