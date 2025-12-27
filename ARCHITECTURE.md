# VisualVerse Platform Architecture

> **One Engine → Multiple Vertical Education Platforms**

> **Open-Source Core + Paid Infrastructure**

---

## Core Principle (Non-Negotiable)

> **Open what builds trust. Charge for what delivers scale, intelligence, and governance.**

This is the **Linux / Red Hat model** for education infrastructure:

- **Open-source engine** → ecosystem adoption
- **Paid platforms & services** → sustainability

---

## Repository Structure

```
visualverse/
├── LICENSE                     # Main license file
├── README.md                   # Main documentation
├── requirements.txt            # Python dependencies
│
├── open-source/                # 🎯 OPEN-SOURCE (Community Trust Layer)
│   ├── engine/                 # Animation engine core
│   ├── primitives/             # Visual elements library
│   ├── schemas/                # Content schemas & knowledge models
│   └── samples/                # Demo animations
│
├── apps/                       # 🔐 PROPRIETARY (Web Applications)
│   ├── admin-console/          # Institutional management
│   ├── creator-portal/         # Creator monetization
│   └── student-app/            # Learner experience
│
├── platforms/                  # CONTENT VERTICALS (Mixed)
│   ├── mathverse/              # Math content
│   ├── physicsverse/           # Physics content
│   ├── chemverse/              # Chemistry content
│   ├── algverse/               # Algorithm content
│   └── finverse/               # Financial content
│
├── services/                   # 🔐 PROPRIETARY (Backend Services)
│   ├── lxp/                    # Learning Experience Platform
│   ├── platform/               # Platform Services
│   └── gov/                    # Governance & Admin
│
├── infrastructure/             # 🔐 PROPRIETARY (Deployment)
│   ├── docker/
│   ├── kubernetes/
│   ├── terraform/
│   └── monitoring/
│
├── docs/                       # Documentation
├── scripts/                    # Development tools
└── tests/                      # Test suite
```

---

## 🎯 OPEN-SOURCE Components

### Directory: `open-source/`

> **Apache 2.0 License** - Free, auditable, forkable

This layer builds **community trust** and **ecosystem adoption**.

---

### 1. Visual Engine (`open-source/engine/`)

The heart of VisualVerse - a deterministic, script-based animation engine.

**Features:**
- Manim-based rendering
- Mathematical precision & repeatability
- Version-controlled outputs
- Export to video, frames, interactive HTML

**Subdirectories:**
- `animation-engine/` - Core rendering and animation
- `common/` - Shared utilities and base schemas
- `content-metadata/` - Content organization schemas
- `legacy_core/` - Legacy compatibility layer
- `recommendation-engine/` - Basic rule-based recommendations

**Why Open-Source:**
- Educators trust transparent logic
- Researchers verify correctness
- Community contributions improve engine
- Becomes an industry standard

---

### 2. Visual Primitives (`open-source/primitives/`)

Standard library of reusable visual elements.

**Includes:**
- Geometric shapes (circles, squares, polygons)
- Mathematical notation (equations, matrices)
- Graphs & charts (bar, line, scatter)
- Timelines & sequences
- Data visualization elements

**Purpose:**
- Ensures visual consistency across platforms
- Reduces duplication across subjects
- Enables third-party tooling

---

### 3. Content Schemas (`open-source/schemas/`)

JSON schemas and TypeScript interfaces defining knowledge structures.

**Schemas:**
- `concept.schema.json` - Knowledge concept definition
- `lesson.schema.json` - Lesson structure
- `animation.schema.json` - Animation metadata
- `curriculum.schema.json` - Curriculum mapping

**Purpose:**
- Defines what knowledge looks like
- Enables external integrations
- Makes VisualVerse a platform standard

---

### 4. Sample Content (`open-source/samples/`)

Demo animations for each vertical.

**Includes:**
- Intro MathVerse examples
- Basic Physics simulations
- Chemistry introduction visuals
- Algorithm flow examples
- Financial concept demos

**Purpose:**
- Demonstrates engine capabilities
- Enables quick experimentation
- Encourages educator adoption

---

## 🔐 PROPRIETARY Components

### Directory: `apps/` (Web Applications)

Enterprise-grade web applications for institutional use.

---

### 1. Admin Console (`apps/admin-console/`)

Institutional management platform.

**Features:**
- User & role management
- Content moderation
- Analytics & reporting
- Compliance & audit
- System health monitoring

**Pricing:** ₹50,000 - ₹5,00,000 / year / institution

---

### 2. Creator Portal (`apps/creator-portal/`)

Content creator monetization platform.

**Features:**
- Script-based content authoring
- Preview & version control
- Syllabus tagging
- Monetization & licensing

**Model:** Revenue share (30% platform, 70% creator)

---

### 3. Student App (`apps/student-app/`)

Learner experience platform.

**Features:**
- Visual-first learning interface
- Concept-wise progress tracking
- Personalized recommendations
- Multi-level support

---

### Directory: `services/` (Backend Services)

Microservices for intelligence and governance.

---

### 1. Learning Experience Platform (`services/lxp/`)

Adaptive learning intelligence.

**Features:**
- Progress tracking
- Adaptive assessments
- Recommendation engine
- Engagement & gamification
- Multi-level content adaptation

**Value:**
- Personalizes learning journeys
- Optimizes concept retention
- Enables outcome-based education

---

### 2. Platform Services (`services/platform/`)

Core platform functionality.

**Features:**
- Licensing management
- Syllabus management
- Version control for content
- User authentication

---

### 3. Governance Platform (`services/gov/`)

Institutional governance & compliance.

**Features:**
- Identity & access management
- Content moderation
- Institutional analytics
- GDPR/CCPA compliance
- Audit logging

---

### Directory: `platforms/` (Vertical Content)

Subject-specific content packages with tiered access (sample vs pro).

**Platforms:**
- `mathverse/` - Mathematics curriculum
- `physicsverse/` - Physics simulations
- `chemverse/` - Chemistry visualizations
- `algverse/` - Algorithm visualizations
- `finverse/` - Financial modeling

**Structure Per Platform:**
```
platforms/{platform}/
├── __init__.py
├── {platform}_plugin.py          # Platform plugin with Manim integration
├── sample/                        # Open-source sample content
│   └── README.md
├── pro/                           # Proprietary premium content
│   └── README.md
├── animations/                    # TypeScript animation definitions
├── syllabus/                      # Curriculum content
└── README.md
```

**Sample Directory (Open-Source):**
Contains freely available sample content under MIT License:
- Basic concept visualizations
- Introductory examples
- Reference materials

**Pro Directory (Proprietary):**
Contains premium content requiring a license:
- Advanced topic coverage
- High-quality Manim animations
- Expert-level problems
- Institutional materials

**Licensing:**
- `sample/` content → MIT License (Open-Source)
- `pro/` content → Proprietary (Paid)
- Plugins → Apache 2.0 (Open-Source engine integration)

---

### Directory: `infrastructure/` (Deployment)

Enterprise deployment configurations.

**Features:**
- Docker configurations
- Kubernetes manifests
- Terraform cloud infrastructure
- Monitoring (Prometheus/Grafana)
- CI/CD pipelines

**Value:**
- On-premises deployment
- Custom integration
- SLA guarantees
- Dedicated support

---

## 📜 Licensing Summary

| Component | License | Access |
|-----------|---------|--------|
| open-source/engine | Apache 2.0 | Public |
| open-source/primitives | Apache 2.0 | Public |
| open-source/schemas | Apache 2.0 | Public |
| open-source/samples | Apache 2.0 | Public |
| apps/admin-console | Proprietary | Paid |
| apps/creator-portal | Proprietary | Paid |
| apps/student-app | Proprietary | Paid |
| services/lxp | Proprietary | Paid |
| services/platform | Proprietary | Paid |
| services/gov | Proprietary | Paid |
| platforms/* | Mixed | Mixed |
| infrastructure | Proprietary | Paid |

---

## 🏗️ Visual Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     STUDENT EXPERIENCE                          │
│                    (apps/student-app)                           │
│                        [Proprietary]                            │
├─────────────────────────────────────────────────────────────────┤
│                    CREATOR PORTAL                               │
│                   (apps/creator-portal)                         │
│                        [Proprietary]                            │
├─────────────────────────────────────────────────────────────────┤
│                    ADMIN CONSOLE                                │
│                  (apps/admin-console)                           │
│                        [Proprietary]                            │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    SERVICES                              │   │
│  │         (services/lxp, platform, gov)                   │   │
│  │                   [Proprietary]                          │   │
│  └─────────────────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                  OPEN-SOURCE CORE                       │   │
│  │            (open-source/engine - Apache 2.0)            │   │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐   │   │
│  │  │ Primit-  │ │  Scene   │ │Export-   │ │ Schemas  │   │   │
│  │  │   ives   │ │  Base    │ │  ers     │ │          │   │   │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘   │   │
│  └─────────────────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────────────┤
│                     PLATFORMS                                  │
│            (mathverse, physicsverse, etc.)                     │
│         [Basic = Open, Full = Paid]                            │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🚀 Getting Started

### For Open-Source Development

```bash
# Clone the repository
git clone https://github.com/visualverse/visualverse.git
cd visualverse

# Install dependencies
pip install -r requirements.txt

# Run the animation engine
cd open-source/engine
python -m animation_engine

# Explore visual primitives
cd open-source/primitives

# Check content schemas
cd open-source/schemas

# Run sample animations
cd open-source/samples
```

### For Enterprise Deployment

Contact us at `enterprise@visualverse.io` for:
- Institutional licensing
- Custom deployments
- Enterprise support
- Content partnerships

---

## 📞 Support & Contact

- **GitHub Issues:** For open-source engine issues
- **Enterprise Sales:** `enterprise@visualverse.io`
- **Documentation:** `/docs/`
- **Discord:** Community server for discussions

---

## © License

VisualVerse is dual-licensed:

- **Open-Source Components:** Licensed under Apache 2.0
- **Proprietary Components:** See respective directories

See `LICENSE` file for full license information.

---

*VisualVerse - Democratizing Education Through Animation*
