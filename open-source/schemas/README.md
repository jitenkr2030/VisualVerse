# Content Schemas & Knowledge Models

> JSON schemas and TypeScript interfaces defining knowledge structures.

This directory contains the schema definitions that make VisualVerse a **platform standard** for educational content.

---

## Schema Files

### Concept Schema (`concept.schema.json`)

Defines a knowledge concept.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "properties": {
    "concept_id": {"type": "string"},
    "title": {"type": "string"},
    "description": {"type": "string"},
    "prerequisites": {"type": "array", "items": {"type": "string"}},
    "learning_objectives": {"type": "array", "items": {"type": "string"}},
    "difficulty_level": {"type": "string", "enum": ["beginner", "intermediate", "advanced"]},
    "visual_elements": {"type": "array"},
    "estimated_duration_minutes": {"type": "integer"}
  }
}
```

### Lesson Schema (`lesson.schema.json`)

Defines a lesson structure.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "properties": {
    "lesson_id": {"type": "string"},
    "title": {"type": "string"},
    "concepts": {"type": "array", "items": {"type": "string"}},
    "animations": {"type": "array"},
    "assessments": {"type": "array"},
    "learning_path": {"type": "array"}
  }
}
```

### Animation Schema (`animation.schema.json`)

Defines animation metadata.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "properties": {
    "animation_id": {"type": "string"},
    "script": {"type": "string"},
    "duration_seconds": {"type": "number"},
    "visual_style": {"type": "string"},
    "target_concepts": {"type": "array"}
  }
}
```

### Curriculum Schema (`curriculum.schema.json`)

Defines curriculum/standards mapping.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "properties": {
    "curriculum_id": {"type": "string"},
    "name": {"type": "string"},
    "standard_body": {"type": "string"},
    "grade_level": {"type": "string"},
    "concepts": {"type": "array"}
  }
}
```

---

## TypeScript Interfaces

Also provided: equivalent TypeScript interfaces in `interfaces/`

```typescript
interface Concept {
  concept_id: string;
  title: string;
  description: string;
  prerequisites: string[];
  learning_objectives: string[];
  difficulty_level: 'beginner' | 'intermediate' | 'advanced';
  visual_elements: VisualElement[];
  estimated_duration_minutes: number;
}
```

---

## Validation

Use the schemas to validate content:

```python
import json
from jsonschema import validate

with open('concept.schema.json') as schema:
    schema_data = json.load(schema)

with open('my_content.json') as content:
    content_data = json.load(content)
    
validate(instance=content_data, schema=schema_data)
```

---

## License

Apache 2.0 - See [LICENSE](../../LICENSE)
