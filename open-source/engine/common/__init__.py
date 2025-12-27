"""
VisualVerse Common Utilities - Open-Source Foundation

This module provides shared utilities and base schemas
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
- Base response schemas
- File operations utilities
- String utilities
- Time utilities
- Logging configuration
- Basic permission definitions

For more information, visit: https://visualverse.io
"""

from .schemas import *
from .auth import *
from .logging import *
from .utils import *

__all__ = [
    # Schemas
    "BaseModel",
    "ConceptSchema", 
    "LessonSchema",
    "AnimationSchema",
    
    # Auth
    "Permissions",
    "AuthContext",
    
    # Logging
    "get_logger",
    "setup_logging",
    
    # Utils
    "generate_id",
    "validate_email",
    "sanitize_filename",
]
