# VisualVerse Platforms - Content Verticals

This directory contains platform-specific modules for different educational verticals.

## 📁 Structure

```
platforms/
├── mathverse/           # Mathematics platform
│   ├── animations/      # ✅ OPEN-SOURCE (Core animations)
│   ├── syllabus/        # ✅ OPEN-SOURCE (Curriculum structure)
│   ├── sample/          # ✅ OPEN-SOURCE (Sample content)
│   └── pro/             # 🔐 PROPRIETARY (IIT-level content)
│
├── physicsverse/        # Physics platform
│   ├── animations/      # ✅ OPEN-SOURCE (Core animations)
│   ├── syllabus/        # ✅ OPEN-SOURCE (Curriculum structure)
│   ├── sample/          # ✅ OPEN-SOURCE (Sample content)
│   └── pro/             # 🔐 PROPRIETARY (Advanced content)
│
├── chemverse/           # Chemistry platform
│   ├── animations/      # ✅ OPEN-SOURCE (Core animations)
│   ├── syllabus/        # ✅ OPEN-SOURCE (Curriculum structure)
│   ├── sample/          # ✅ OPEN-SOURCE (Sample content)
│   └── pro/             # 🔐 PROPRIETARY (Professional content)
│
├── algverse/            # Algorithms platform
│   ├── animations/      # ✅ OPEN-SOURCE (Core animations)
│   ├── syllabus/        # ✅ OPEN-SOURCE (Curriculum structure)
│   ├── sample/          # ✅ OPEN-SOURCE (Sample content)
│   └── pro/             # 🔐 PROPRIETARY (Advanced algorithms)
│
└── finverse/            # Finance platform
    ├── animations/      # 🔐 PROPRIETARY (All content)
    ├── syllabus/        # 🔐 PROPRIETARY (All content)
    └── sample/          # 🔐 PROPRIETARY (All content)
```

## ⚖️ Licensing

### ✅ Open-Source Components (Apache 2.0)

Core animations and curriculum structures are open-source under Apache 2.0.

**Contents:**
- Basic animation implementations
- Standard curriculum structures
- Sample content for demonstration
- Educational examples

**Usage:**
```python
from visualverse.platforms.mathverse import MathVerse

math = MathVerse()
lessons = math.get_core_lessons()
```

### 🔐 Proprietary Content Packs (Commercial License)

Professional content packs require a commercial license.

**Examples:**
- `mathverse/pro/` - IIT-level mathematics content
- `physicsverse/pro/` - Advanced physics for competitive exams
- `finverse/` - Professional finance content (all proprietary)

**Features:**
- Comprehensive animation libraries
- Assessment questions
- Teacher guides
- Progress indicators
- Curriculum mapping

**Pricing:** Tiered by institution size and content depth

**Contact:** enterprise@visualverse.io

## 📚 Available Content

### MathVerse
- ✅ Basic algebra (Open-Source)
- ✅ Calculus introduction (Open-Source)
- 🔐 IIT-JEE mathematics (Pro)
- 🔐 Advanced calculus (Pro)

### PhysicsVerse
- ✅ Mechanics basics (Open-Source)
- ✅ Electromagnetism introduction (Open-Source)
- 🔐 Advanced mechanics (Pro)
- 🔐 Competitive exam physics (Pro)

### ChemistryVerse
- ✅ Basic chemistry (Open-Source)
- ✅ Organic chemistry introduction (Open-Source)
- 🔐 Inorganic chemistry (Pro)
- 🔐 Physical chemistry (Pro)

### AlgorithmVerse
- ✅ Sorting algorithms (Open-Source)
- ✅ Graph algorithms introduction (Open-Source)
- 🔐 Advanced algorithms (Pro)
- 🔐 Competitive programming (Pro)

### FinVerse
- 🔐 All content (Proprietary)
- Financial markets
- Investment strategies
- Risk management

## 🎯 Content Quality

### Open-Source Content
- Basic to intermediate complexity
- Educational demonstrations
- Community maintained
- Standard quality

### Pro Content
- Advanced complexity
- Professional quality
- Expert reviewed
- Continuously updated
- Assessment integration
- Teacher resources

## 🤝 Contributing

Contributions to open-source content are welcome!
See contributing guidelines at:
https://github.com/visualverse/visualverse/blob/main/CONTRIBUTING.md

**Note:** Pro content does not accept external contributions.

## © Copyright

**Open-Source Content:** Copyright 2025 VisualVerse Contributors (Apache 2.0)  
**Pro Content:** Copyright 2025 VisualVerse - All Rights Reserved

For licensing inquiries: enterprise@visualverse.io
