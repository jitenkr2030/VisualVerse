"""
VisualVerse Content Metadata Service - Open-Source Foundation

This module provides content organization and metadata management
for the VisualVerse platform, licensed under Apache 2.0.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Contents:
- Subject models and management
- Concept organization and hierarchy
- Content metadata schemas
- Search and discovery services
- API routes for content management

For more information, visit: https://visualverse.io
"""

from .models.subject import Subject
from .models.concept import Concept
from .services.concept_service import ConceptService
from .services.search_service import SearchService
from .routes.subjects import router as subjects_router
from .routes.concepts import router as concepts_router

__version__ = "1.0.0"
__author__ = "VisualVerse Contributors"

__all__ = [
    # Models
    "Subject",
    "Concept",
    # Services
    "ConceptService",
    "SearchService",
    # Routes
    "subjects_router",
    "concepts_router",
]
