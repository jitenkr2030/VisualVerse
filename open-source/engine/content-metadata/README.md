# Content Metadata Service

The Content Metadata Service manages the knowledge graph, curriculum data, and content relationships for VisualVerse. This service provides the foundation for intelligent content organization and learning path generation.

## Architecture

### Core Components

- **`models/`** - Data models and schemas
  - `subject.py` - Subject definitions and metadata
  - `course.py` - Course structures and organization
  - `concept.py` - Individual concept definitions
  - `prerequisite.py` - Learning prerequisite relationships
  - `syllabus.py` - Curriculum mapping and standards

- **`services/`** - Business logic services
  - `tagging_service.py` - Content tagging and categorization
  - `dependency_graph.py` - Learning dependency management
  - `curriculum_mapper.py` - Standard curriculum mapping

- **`routes/`** - API endpoints
  - `subjects.py` - Subject management endpoints
  - `courses.py` - Course management endpoints
  - `concepts.py` - Concept management endpoints

- **`app/`** - Service application
  - `main.py` - FastAPI application entry point
  - `database.py` - Database configuration and management
  - `config.py` - Service configuration

## Database Schema

The service uses a graph database (Neo4j) for relationship management with the following key entities:

- **Subject**: Educational domains (Math, Physics, etc.)
- **Course**: Organized learning units within subjects
- **Concept**: Individual learning concepts
- **Prerequisite**: Dependencies between concepts
- **Syllabus**: Curriculum standards mapping

## API Endpoints

### Subject Management
- `GET /subjects` - List all subjects
- `GET /subjects/{subject_id}` - Get subject details
- `POST /subjects` - Create new subject
- `PUT /subjects/{subject_id}` - Update subject

### Course Management
- `GET /courses` - List courses
- `GET /courses/{course_id}` - Get course details
- `POST /courses` - Create new course
- `GET /courses/{course_id}/concepts` - Get course concepts

### Concept Management
- `GET /concepts` - List concepts
- `GET /concepts/{concept_id}` - Get concept details
- `POST /concepts` - Create new concept
- `GET /concepts/{concept_id}/prerequisites` - Get prerequisites
- `GET /concepts/{concept_id}/dependents` - Get dependent concepts

### Learning Path
- `GET /learning-paths/{subject_id}` - Generate learning path
- `GET /learning-paths/{subject_id}/adaptive` - Adaptive learning path

## Usage Example

```python
from visualverse.engine.content_metadata.services import DependencyGraphService

# Create dependency graph service
service = DependencyGraphService()

# Generate learning path for mathematics
path = service.generate_learning_path(
    subject="mathematics",
    start_level="basic_arithmetic",
    target_level="calculus"
)

# Get prerequisites for a concept
prereqs = service.get_prerequisites("quadratic_equations")
```

## Dependencies

- FastAPI for REST API
- Neo4j driver for graph database
- Pydantic for data validation
- NetworkX for graph algorithms

See `app/requirements.txt` for full dependency list.