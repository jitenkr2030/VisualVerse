# VisualVerse Recommendation Engine

**Licensing:** Mixed (See below)

The Recommendation Engine provides intelligent learning path generation and content recommendations for VisualVerse. It uses machine learning algorithms and user behavior analysis to personalize the learning experience.

## ⚖️ Licensing Model

This module has **mixed licensing**:

### ✅ Open-Source Components (Apache 2.0)

The following components are open-source and free to use:

- **`engines/rule_based.py`** - Rule-based recommendation system
- **`models/learning_path.py`** - Basic learning path structures
- **`services/progress_tracker.py`** - Basic progress tracking

These components provide:
- Predefined rules and curriculum standards
- Consistent recommendations based on learning objectives
- Fast response times for basic recommendations

### 🔐 Proprietary Components (Commercial License)

The following components require a commercial license:

- **`engines/graph_based.py`** - Graph-based learning path generation
- **`engines/adaptive_engine.py`** - Machine learning adaptive recommendations
- **`engines/recommendation_engines.py`** - Advanced recommendation algorithms
- **`models/learner_profile.py`** - Advanced user learning profiles
- **`models/mastery_state.py`** - Sophisticated mastery tracking
- **`models/interaction.py`** - Interaction tracking and analysis
- **`models/user_profile.py`** - User profiling algorithms
- **`services/weakness_detector.py`** - Advanced weakness detection
- **`services/prediction_service.py`** - ML-based prediction service
- **`app/main.py`** - Advanced API endpoints

These components provide:
- Concept dependency graphs and optimal learning paths
- Machine learning-based personalization
- Adaptive recommendations that improve over time
- Sophisticated learner profiling
- Mastery tracking algorithms
- Advanced analytics and insights

## 🏗️ Architecture

```
RECOMMENDATION ENGINE
│
├── OPEN-SOURCE (Apache 2.0)
│   ├── rule_based.py          # Rule-based recommendations
│   ├── basic_progress.py      # Simple progress tracking
│   └── learning_path.py       # Basic path structures
│
└── PROPRIETARY (Commercial)
    ├── graph_based.py         # Graph algorithms
    ├── adaptive_engine.py     # ML-based adaptation
    ├── collaborative_filtering.py  # User-based CF
    ├── content_based.py       # Content-based filtering
    ├── prediction_service.py  # ML predictions
    ├── learner_profile.py     # Profile management
    ├── mastery_state.py       # Mastery algorithms
    ├── interaction.py         # Behavior tracking
    ├── user_profile.py        # User modeling
    └── weakness_detector.py   # Gap analysis
```

## 🚀 Usage

### Open-Source Components

```python
from visualverse.engine.recommendation_engine.engines import RuleBasedEngine

# Create rule-based recommendation engine (OPEN-SOURCE)
engine = RuleBasedEngine()

# Generate basic learning path
path = engine.generate_learning_path(
    user_id="user123",
    subject="mathematics",
    current_level="intermediate",
    goals=["calculus"]
)
```

### Proprietary Components

```python
# For proprietary components, obtain a commercial license
from visualverse.engine.recommendation_engine.engines import AdaptiveEngine

# This requires a commercial license
engine = AdaptiveEngine(api_key="YOUR_LICENSE_KEY")

# Generate adaptive learning path
path = engine.generate_adaptive_path(
    user_id="user123",
    subject="mathematics",
    adapt_to_learning_style=True,
    use_ml_predictions=True
)
```

## 📡 API Endpoints

### Open-Source Endpoints

- `GET /recommend/{user_id}` - Basic content recommendations
- `POST /track_interaction` - Track user interactions

### Proprietary Endpoints (Require License)

- `POST /learning-paths/generate` - Advanced path generation
- `GET /learning-paths/{path_id}` - Get learning paths
- `GET /recommendations/concepts` - Concept recommendations
- `GET /recommendations/difficulty` - Difficulty adjustments
- `POST /recommendations/feedback` - ML feedback loop
- `GET /analytics/learning-patterns` - Pattern analysis
- `GET /analytics/weakness-detection` - Weakness identification
- `GET /analytics/progress-prediction` - Progress prediction

## 💼 Obtaining a License

For access to proprietary components, contact:

**Enterprise Sales:** enterprise@visualverse.io

## 📚 Dependencies

- FastAPI for REST API
- Scikit-learn for machine learning algorithms
- Pandas for data processing
- NetworkX for graph algorithms
- NumPy for numerical computations

See `app/requirements.txt` for full dependency list.

## 🤝 Contributing

Contributions to open-source components are welcome!
See our contributing guidelines at:
https://github.com/visualverse/visualverse/blob/main/CONTRIBUTING.md

**Note:** Proprietary components do not accept external contributions.

## © Copyright

**Open-Source Components:** Copyright 2025 VisualVerse Contributors (Apache 2.0)  
**Proprietary Components:** Copyright 2025 VisualVerse - All Rights Reserved
