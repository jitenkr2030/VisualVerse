# Contributing to VisualVerse

Thank you for your interest in contributing to VisualVerse! This document outlines the guidelines for contributing to our open-source components and the process for becoming a commercial partner.

## 📋 Table of Contents

1. [Contributing to Open-Source Components](#contributing-to-open-source-components)
2. [Commercial Licensing](#commercial-licensing)
3. [Code of Conduct](#code-of-conduct)
4. [Getting Started](#getting-started)
5. [Submitting Changes](#submitting-changes)
6. [Communication](#communication)

---

## 🤝 Contributing to Open-Source Components

VisualVerse's open-source components are licensed under **Apache 2.0**. We welcome contributions from the community!

### ✅ What You Can Contribute

- **Animation Engine** (`engine/animation-engine/`)
  - New primitives and shapes
  - Export format support
  - Theme implementations
  - Performance optimizations
  - Bug fixes

- **Common Utilities** (`engine/common/`)
  - Schema improvements
  - Utility functions
  - Documentation enhancements
  - Test coverage

- **Content Metadata** (`engine/content-metadata/`)
  - API endpoint improvements
  - Database optimizations
  - Search functionality
  - Documentation

- **Platform Modules** (`platforms/*/`)
  - New animations for existing platforms
  - Syllabus improvements
  - Sample content
  - Bug fixes

### ❌ What Cannot Be Contributed

The following components are proprietary and **do not accept external contributions**:

- `apps/admin-console/` - Enterprise management platform
- `apps/creator-portal/` - Creator monetization platform
- `apps/student-app/` - Student experience platform
- `engine/recommendation-engine/` - Advanced AI components
- `platforms/*/pro/` - Professional content packs
- `infrastructure/` - Enterprise deployment configurations

For these components, please contact `enterprise@visualverse.io` for partnership opportunities.

### 📝 Contribution Process

1. **Fork** the repository
2. **Create** a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make** your changes following our coding standards
4. **Add** tests for new functionality
5. **Ensure** all tests pass:
   ```bash
   python -m pytest tests/
   ```
6. **Submit** a pull request with clear description

### 📐 Coding Standards

#### Python Code Style
- Follow PEP 8 guidelines
- Use type hints for all functions
- Write comprehensive docstrings
- Include unit tests for new features

```python
from typing import List, Optional

def process_content(content_ids: List[str], filter_by: Optional[str] = None) -> List[dict]:
    """
    Process educational content based on specified filters.
    
    Args:
        content_ids: List of content identifiers to process
        filter_by: Optional filter criterion (e.g., 'difficulty', 'subject')
    
    Returns:
        List of processed content dictionaries
    
    Example:
        >>> process_content(['math_001', 'math_002'], filter_by='beginner')
        [{'id': 'math_001', 'level': 'beginner', ...}]
    """
    # Implementation
    pass
```

#### Documentation
- Update README.md for new features
- Add docstrings to all public functions
- Include usage examples in documentation
- Update API documentation for endpoint changes

#### Testing
- Write unit tests for new functionality
- Maintain test coverage above 80%
- Use pytest framework
- Include integration tests for API changes

```python
import pytest
from visualverse.animation_engine import Scene

class TestScene:
    def test_scene_creation(self):
        """Test that a scene can be created successfully."""
        scene = Scene()
        assert scene is not None
    
    def test_add_primitive(self):
        """Test adding a primitive to a scene."""
        scene = Scene()
        rectangle = scene.add_rectangle(width=2, height=1)
        assert rectangle in scene.get_objects()
```

---

## 💼 Commercial Licensing

For proprietary components, VisualVerse offers several licensing options.

### Institutional License

For educational institutions deploying VisualVerse at scale.

| Feature | Starter | Professional | Enterprise | Unlimited |
|---------|---------|--------------|------------|-----------|
| Users | Up to 500 | 501-5,000 | 5,001-25,000 | 25,000+ |
| Price (INR) | ₹50,000/year | ₹2,00,000/year | ₹5,00,000/year | Custom |
| Admin Console | ✅ | ✅ | ✅ | ✅ |
| Analytics | Basic | Advanced | Full | Full |
| Support | Email | Email + Chat | 24/7 Phone | Dedicated |
| SLA | - | 99.5% | 99.9% | 99.99% |

### Professional Content License

For access to premium content packs.

| Subject | Individual | Institutional |
|---------|------------|---------------|
| MathVerse Pro | ₹5,000 | ₹1,50,000/year |
| PhysicsVerse Pro | ₹5,000 | ₹1,50,000/year |
| ChemistryVerse Pro | ₹5,000 | ₹1,50,000/year |
| FinVerse | ₹10,000 | ₹3,00,000/year |

### Creator License

For content creators using the Creator Portal.

- **Platform Fee:** 30% of earnings
- **Creator Share:** 70% of earnings
- **Includes:** Distribution, payments, analytics

### Enterprise Agreement

For large organizations requiring custom solutions.

- Custom feature development
- On-premises deployment
- SLA guarantees
- Dedicated support engineer
- Quarterly business reviews

**Contact:** `enterprise@visualverse.io`

---

## 📖 Code of Conduct

### Our Pledge

We as members, contributors, and leaders pledge to make participation in our community a harassment-free experience for everyone, regardless of age, body size, visible or invisible disability, ethnicity, sex characteristics, gender identity and expression, level of experience, education, socio-economic status, nationality, personal appearance, race, religion, or sexual identity and orientation.

### Our Standards

Examples of behavior that contributes to a positive environment:

- Using welcoming and inclusive language
- Being respectful of differing viewpoints and experiences
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards other community members

Examples of unacceptable behavior:

- The use of sexualized language or imagery
- Trolling, insulting/derogatory comments, and personal or political attacks
- Public or private harassment
- Publishing others' private information without permission
- Other conduct which could reasonably be considered inappropriate

### Enforcement

Community leaders will follow these Community Impact Guidelines in determining the consequences for any action they deem in violation of this Code of Conduct.

---

## 🚀 Getting Started

### Development Environment Setup

```bash
# Clone the repository
git clone https://github.com/visualverse/visualverse.git
cd visualverse

# Set up Python environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Install development dependencies
pip install pytest black flake8 mypy

# Run tests
python -m pytest tests/

# Check code style
black --check .
flake8 .
mypy .
```

### Building Documentation

```bash
# Install documentation dependencies
pip install sphinx sphinx_rtd_theme

# Build HTML documentation
cd docs
make html
```

---

## 📤 Submitting Changes

### Pull Request Process

1. **Ensure** all tests pass locally
2. **Update** documentation for any changed functionality
3. **Add** entry to CHANGELOG.md following [Keep a Changelog](https://keepachangelog.com/) format
4. **Request** review from maintainers
5. **Address** feedback and resolve issues
6. **Merge** after approval

### Pull Request Template

```markdown
## Description
Describe your changes concisely.

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to change)
- [ ] Documentation update
- [ ] Test improvement

## Testing
Describe how the changes were tested.

## Checklist
- [ ] My code follows the style guidelines of this project
- [ ] I have performed a self-review of my code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes
```

### Commit Messages

Follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

Types:
- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation only changes
- `style`: Changes that do not affect the meaning of the code (white-space, formatting, etc)
- `refactor`: A code change that neither fixes a bug nor adds a feature
- `perf`: A code change that improves performance
- `test`: Adding missing tests or correcting existing tests
- `chore`: Changes to the build process or auxiliary tools

Examples:
```
feat(animation-engine): add support for 3D primitives
fix(content-metadata): resolve pagination issue in search API
docs(readme): update installation instructions
refactor(common): improve error handling in schemas
```

---

## 💬 Communication

### Channels

- **GitHub Issues:** Bug reports, feature requests, and discussions
- **GitHub Discussions:** Q&A and community conversations
- **Discord:** Real-time chat with community and team
- **Email:** `enterprise@visualverse.io` for commercial inquiries

### Response Time

- **GitHub Issues:** 2-3 business days
- **Commercial Inquiries:** 1 business day
- **Security Issues:** Send to `security@visualverse.io` for immediate response

---

## 📜 License

By contributing to VisualVerse's open-source components, you agree that your contributions will be licensed under the Apache License, Version 2.0.

For proprietary components, please contact `enterprise@visualverse.io` for licensing information.

---

**Thank you for contributing to VisualVerse!** 🎓✨

*Together, we're democratizing education through animation.*
