# Copyright 2024 VisualVerse Contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Scene Validator for VisualVerse Animation Engine

Validates scene graphs for cyclic dependencies, ensures assets exist before rendering,
and validates time-bounds are non-negative. Provides comprehensive validation
for animation scenes before processing.
"""

from typing import List, Dict, Any, Optional, Set, Tuple, Union
from dataclasses import dataclass
from enum import Enum
import logging
import math
from pathlib import Path

from ..primitives.geometry import Shape, ShapeType, Point
from ..primitives.text import Text
from ..primitives.layout import LayoutContainer

logger = logging.getLogger(__name__)

class ValidationSeverity(Enum):
    """Validation message severity levels"""
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"

@dataclass
class ValidationMessage:
    """Validation message with severity and details"""
    severity: ValidationSeverity
    message: str
    details: Optional[str] = None
    line_number: Optional[int] = None
    file_path: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert validation message to dictionary"""
        return {
            "severity": self.severity.value,
            "message": self.message,
            "details": self.details,
            "line_number": self.line_number,
            "file_path": self.file_path
        }

@dataclass
class ValidationResult:
    """Result of scene validation"""
    is_valid: bool
    messages: List[ValidationMessage]
    errors_count: int = 0
    warnings_count: int = 0
    info_count: int = 0
    
    def __post_init__(self):
        """Calculate message counts"""
        for message in self.messages:
            if message.severity == ValidationSeverity.ERROR:
                self.errors_count += 1
            elif message.severity == ValidationSeverity.WARNING:
                self.warnings_count += 1
            else:
                self.info_count += 1
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert validation result to dictionary"""
        return {
            "is_valid": self.is_valid,
            "summary": {
                "errors": self.errors_count,
                "warnings": self.warnings_count,
                "info": self.info_count,
                "total": len(self.messages)
            },
            "messages": [msg.to_dict() for msg in self.messages]
        }

class SceneValidator:
    """Validates animation scenes for correctness and safety"""
    
    def __init__(self):
        """Initialize scene validator"""
        self.max_scene_objects = 10000  # Maximum objects in a scene
        self.max_animation_duration = 3600  # Maximum duration in seconds (1 hour)
        self.min_frame_rate = 1  # Minimum FPS
        self.max_frame_rate = 120  # Maximum FPS
        self.max_resolution_width = 7680  # 8K width
        self.max_resolution_height = 4320  # 8K height
        self.min_resolution_width = 64  # Minimum width
        self.min_resolution_height = 64  # Minimum height
        self.max_file_size_mb = 1000  # Maximum output file size in MB
        
    def validate_scene_graph(self, scene_graph: Dict[str, Any]) -> ValidationResult:
        """
        Validate a scene graph structure
        
        Args:
            scene_graph: Dictionary representing scene graph structure
            
        Returns:
            ValidationResult with validation messages
        """
        messages: List[ValidationMessage] = []
        
        # Check if scene graph is a dictionary
        if not isinstance(scene_graph, dict):
            messages.append(ValidationMessage(
                ValidationSeverity.ERROR,
                "Scene graph must be a dictionary",
                f"Got {type(scene_graph).__name__}"
            ))
            return ValidationResult(False, messages)
        
        # Check for required fields
        if "objects" not in scene_graph:
            messages.append(ValidationMessage(
                ValidationSeverity.ERROR,
                "Scene graph missing required 'objects' field"
            ))
        
        if "animations" not in scene_graph:
            messages.append(ValidationMessage(
                ValidationSeverity.WARNING,
                "Scene graph missing 'animations' field",
                "No animations will be processed"
            ))
        
        # Validate objects
        if "objects" in scene_graph:
            messages.extend(self._validate_objects(scene_graph["objects"]))
        
        # Validate animations
        if "animations" in scene_graph:
            messages.extend(self._validate_animations(scene_graph["animations"], scene_graph.get("objects", {})))
        
        # Check for cyclic dependencies
        messages.extend(self._check_cyclic_dependencies(scene_graph))
        
        # Validate scene properties
        if "properties" in scene_graph:
            messages.extend(self._validate_scene_properties(scene_graph["properties"]))
        
        # Check file paths and assets
        messages.extend(self._validate_assets(scene_graph))
        
        is_valid = all(msg.severity != ValidationSeverity.ERROR for msg in messages)
        return ValidationResult(is_valid, messages)
    
    def _validate_objects(self, objects: Dict[str, Any]) -> List[ValidationMessage]:
        """Validate scene objects"""
        messages: List[ValidationMessage] = []
        
        if not isinstance(objects, dict):
            messages.append(ValidationMessage(
                ValidationSeverity.ERROR,
                "Objects must be a dictionary",
                f"Got {type(objects).__name__}"
            ))
            return messages
        
        # Check object count
        object_count = len(objects)
        if object_count > self.max_scene_objects:
            messages.append(ValidationMessage(
                ValidationSeverity.ERROR,
                f"Too many objects in scene: {object_count}",
                f"Maximum allowed: {self.max_scene_objects}"
            ))
        
        for obj_id, obj_data in objects.items():
            messages.extend(self._validate_single_object(obj_id, obj_data))
        
        return messages
    
    def _validate_single_object(self, obj_id: str, obj_data: Dict[str, Any]) -> List[ValidationMessage]:
        """Validate a single scene object"""
        messages: List[ValidationMessage] = []
        
        if not isinstance(obj_data, dict):
            messages.append(ValidationMessage(
                ValidationSeverity.ERROR,
                f"Object '{obj_id}' data must be a dictionary",
                f"Got {type(obj_data).__name__}"
            ))
            return messages
        
        # Check for required fields
        if "type" not in obj_data:
            messages.append(ValidationMessage(
                ValidationSeverity.ERROR,
                f"Object '{obj_id}' missing required 'type' field"
            ))
            return messages
        
        obj_type = obj_data["type"]
        
        # Validate object type
        try:
            shape_type = ShapeType(obj_type)
        except ValueError:
            messages.append(ValidationMessage(
                ValidationSeverity.ERROR,
                f"Object '{obj_id}' has invalid type: {obj_type}",
                f"Valid types: {[t.value for t in ShapeType]}"
            ))
            return messages
        
        # Validate based on object type
        messages.extend(self._validate_object_properties(obj_id, obj_data, shape_type))
        
        # Validate position if present
        if "position" in obj_data:
            messages.extend(self._validate_position(obj_id, obj_data["position"]))
        
        # Validate transform if present
        if "transform" in obj_data:
            messages.extend(self._validate_transform(obj_id, obj_data["transform"]))
        
        return messages
    
    def _validate_object_properties(self, obj_id: str, obj_data: Dict[str, Any], obj_type: ShapeType) -> List[ValidationMessage]:
        """Validate object properties based on type"""
        messages: List[ValidationMessage] = []
        
        if obj_type == ShapeType.CIRCLE:
            if "radius" not in obj_data:
                messages.append(ValidationMessage(
                    ValidationSeverity.ERROR,
                    f"Circle '{obj_id}' missing required 'radius' property"
                ))
            elif obj_data["radius"] <= 0:
                messages.append(ValidationMessage(
                    ValidationSeverity.ERROR,
                    f"Circle '{obj_id}' radius must be positive",
                    f"Got: {obj_data['radius']}"
                ))
        
        elif obj_type == ShapeType.RECTANGLE:
            required_props = ["width", "height"]
            for prop in required_props:
                if prop not in obj_data:
                    messages.append(ValidationMessage(
                        ValidationSeverity.ERROR,
                        f"Rectangle '{obj_id}' missing required '{prop}' property"
                    ))
                elif obj_data[prop] <= 0:
                    messages.append(ValidationMessage(
                        ValidationSeverity.ERROR,
                        f"Rectangle '{obj_id}' {prop} must be positive",
                        f"Got: {obj_data[prop]}"
                    ))
        
        elif obj_type == ShapeType.POLYGON:
            if "vertices" not in obj_data:
                messages.append(ValidationMessage(
                    ValidationSeverity.ERROR,
                    f"Polygon '{obj_id}' missing required 'vertices' property"
                ))
            elif not isinstance(obj_data["vertices"], list) or len(obj_data["vertices"]) < 3:
                messages.append(ValidationMessage(
                    ValidationSeverity.ERROR,
                    f"Polygon '{obj_id}' must have at least 3 vertices",
                    f"Got: {len(obj_data.get('vertices', []))}"
                ))
        
        elif obj_type == ShapeType.LINE:
            if "start" not in obj_data or "end" not in obj_data:
                messages.append(ValidationMessage(
                    ValidationSeverity.ERROR,
                    f"Line '{obj_id}' missing required 'start' and 'end' properties"
                ))
        
        elif obj_type == ShapeType.BEZIER_CURVE:
            if "control_points" not in obj_data:
                messages.append(ValidationMessage(
                    ValidationSeverity.ERROR,
                    f"Bézier curve '{obj_id}' missing required 'control_points' property"
                ))
            elif not isinstance(obj_data["control_points"], list) or len(obj_data["control_points"]) < 2:
                messages.append(ValidationMessage(
                    ValidationSeverity.ERROR,
                    f"Bézier curve '{obj_id}' must have at least 2 control points",
                    f"Got: {len(obj_data.get('control_points', []))}"
                ))
        
        elif obj_type == ShapeType.POLYGON:  # Text treated as polygon
            if "text" not in obj_data:
                messages.append(ValidationMessage(
                    ValidationSeverity.ERROR,
                    f"Text '{obj_id}' missing required 'text' property"
                ))
        
        return messages
    
    def _validate_position(self, obj_id: str, position: Any) -> List[ValidationMessage]:
        """Validate object position"""
        messages: List[ValidationMessage] = []
        
        if not isinstance(position, (list, tuple)) or len(position) != 2:
            messages.append(ValidationMessage(
                ValidationSeverity.ERROR,
                f"Object '{obj_id}' position must be a 2D coordinate",
                f"Got: {position}"
            ))
            return messages
        
        try:
            x, y = float(position[0]), float(position[1])
            if not math.isfinite(x) or not math.isfinite(y):
                raise ValueError("Invalid coordinate values")
        except (ValueError, TypeError) as e:
            messages.append(ValidationMessage(
                ValidationSeverity.ERROR,
                f"Object '{obj_id}' position coordinates must be valid numbers",
                f"Got: {position}, Error: {e}"
            ))
        
        return messages
    
    def _validate_transform(self, obj_id: str, transform: Dict[str, Any]) -> List[ValidationMessage]:
        """Validate object transform"""
        messages: List[ValidationMessage] = []
        
        if not isinstance(transform, dict):
            messages.append(ValidationMessage(
                ValidationSeverity.ERROR,
                f"Object '{obj_id}' transform must be a dictionary",
                f"Got: {type(transform).__name__}"
            ))
            return messages
        
        # Validate translation
        if "translation" in transform:
            messages.extend(self._validate_position(f"{obj_id}_translation", transform["translation"]))
        
        # Validate rotation
        if "rotation" in transform:
            try:
                rotation = float(transform["rotation"])
                if not math.isfinite(rotation):
                    raise ValueError("Invalid rotation value")
            except (ValueError, TypeError) as e:
                messages.append(ValidationMessage(
                    ValidationSeverity.ERROR,
                    f"Object '{obj_id}' rotation must be a valid number",
                    f"Got: {transform['rotation']}, Error: {e}"
                ))
        
        # Validate scale
        if "scale" in transform:
            if not isinstance(transform["scale"], (list, tuple)) or len(transform["scale"]) != 2:
                messages.append(ValidationMessage(
                    ValidationSeverity.ERROR,
                    f"Object '{obj_id}' scale must be a 2D scale factor",
                    f"Got: {transform['scale']}"
                ))
            else:
                try:
                    scale_x, scale_y = float(transform["scale"][0]), float(transform["scale"][1])
                    if scale_x <= 0 or scale_y <= 0:
                        messages.append(ValidationMessage(
                            ValidationSeverity.ERROR,
                            f"Object '{obj_id}' scale factors must be positive",
                            f"Got: {transform['scale']}"
                        ))
                except (ValueError, TypeError):
                    messages.append(ValidationMessage(
                        ValidationSeverity.ERROR,
                        f"Object '{obj_id}' scale factors must be valid numbers",
                        f"Got: {transform['scale']}"
                    ))
        
        return messages
    
    def _validate_animations(self, animations: Dict[str, Any], objects: Dict[str, Any]) -> List[ValidationMessage]:
        """Validate animation definitions"""
        messages: List[ValidationMessage] = []
        
        if not isinstance(animations, dict):
            messages.append(ValidationMessage(
                ValidationSeverity.ERROR,
                "Animations must be a dictionary",
                f"Got: {type(animations).__name__}"
            ))
            return messages
        
        for anim_id, anim_data in animations.items():
            messages.extend(self._validate_single_animation(anim_id, anim_data, objects))
        
        return messages
    
    def _validate_single_animation(self, anim_id: str, anim_data: Dict[str, Any], objects: Dict[str, Any]) -> List[ValidationMessage]:
        """Validate a single animation"""
        messages: List[ValidationMessage] = []
        
        if not isinstance(anim_data, dict):
            messages.append(ValidationMessage(
                ValidationSeverity.ERROR,
                f"Animation '{anim_id}' data must be a dictionary",
                f"Got: {type(anim_data).__name__}"
            ))
            return messages
        
        # Check required fields
        if "target" not in anim_data:
            messages.append(ValidationMessage(
                ValidationSeverity.ERROR,
                f"Animation '{anim_id}' missing required 'target' field"
            ))
        elif anim_data["target"] not in objects:
            messages.append(ValidationMessage(
                ValidationSeverity.ERROR,
                f"Animation '{anim_id}' targets non-existent object: {anim_data['target']}",
                f"Available objects: {list(objects.keys())}"
            ))
        
        if "property" not in anim_data:
            messages.append(ValidationMessage(
                ValidationSeverity.ERROR,
                f"Animation '{anim_id}' missing required 'property' field"
            ))
        
        if "keyframes" not in anim_data:
            messages.append(ValidationMessage(
                ValidationSeverity.ERROR,
                f"Animation '{anim_id}' missing required 'keyframes' field"
            ))
        else:
            messages.extend(self._validate_keyframes(anim_id, anim_data["keyframes"]))
        
        # Validate timing
        if "duration" in anim_data:
            try:
                duration = float(anim_data["duration"])
                if duration <= 0:
                    messages.append(ValidationMessage(
                        ValidationSeverity.ERROR,
                        f"Animation '{anim_id}' duration must be positive",
                        f"Got: {duration}"
                    ))
                elif duration > self.max_animation_duration:
                    messages.append(ValidationMessage(
                        ValidationSeverity.WARNING,
                        f"Animation '{anim_id}' duration is very long: {duration}s",
                        f"Maximum recommended: {self.max_animation_duration}s"
                    ))
            except (ValueError, TypeError):
                messages.append(ValidationMessage(
                    ValidationSeverity.ERROR,
                    f"Animation '{anim_id}' duration must be a valid number",
                    f"Got: {anim_data['duration']}"
                ))
        
        return messages
    
    def _validate_keyframes(self, anim_id: str, keyframes: Any) -> List[ValidationMessage]:
        """Validate animation keyframes"""
        messages: List[ValidationMessage] = []
        
        if not isinstance(keyframes, list):
            messages.append(ValidationMessage(
                ValidationSeverity.ERROR,
                f"Animation '{anim_id}' keyframes must be a list",
                f"Got: {type(keyframes).__name__}"
            ))
            return messages
        
        if len(keyframes) < 2:
            messages.append(ValidationMessage(
                ValidationSeverity.ERROR,
                f"Animation '{anim_id}' must have at least 2 keyframes",
                f"Got: {len(keyframes)}"
            ))
            return messages
        
        # Check time progression
        last_time = -1
        for i, keyframe in enumerate(keyframes):
            if not isinstance(keyframe, dict):
                messages.append(ValidationMessage(
                    ValidationSeverity.ERROR,
                    f"Animation '{anim_id}' keyframe {i} must be a dictionary",
                    f"Got: {type(keyframe).__name__}"
                ))
                continue
            
            if "time" not in keyframe:
                messages.append(ValidationMessage(
                    ValidationSeverity.ERROR,
                    f"Animation '{anim_id}' keyframe {i} missing 'time' field"
                ))
                continue
            
            try:
                time = float(keyframe["time"])
                if time < 0:
                    messages.append(ValidationMessage(
                        ValidationSeverity.ERROR,
                        f"Animation '{anim_id}' keyframe {i} time must be non-negative",
                        f"Got: {time}"
                    ))
                elif time <= last_time:
                    messages.append(ValidationMessage(
                        ValidationSeverity.ERROR,
                        f"Animation '{anim_id}' keyframe {i} time must be greater than previous",
                        f"Got: {time}, Last: {last_time}"
                    ))
                last_time = time
            except (ValueError, TypeError):
                messages.append(ValidationMessage(
                    ValidationSeverity.ERROR,
                    f"Animation '{anim_id}' keyframe {i} time must be a valid number",
                    f"Got: {keyframe['time']}"
                ))
        
        return messages
    
    def _check_cyclic_dependencies(self, scene_graph: Dict[str, Any]) -> List[ValidationMessage]:
        """Check for cyclic dependencies in scene graph"""
        messages: List[ValidationMessage] = []
        
        # This is a simplified check for layout containers
        objects = scene_graph.get("objects", {})
        
        # Check for circular references in layout containers
        layout_refs = {}
        for obj_id, obj_data in objects.items():
            if obj_data.get("type") == "layout_container":
                children = obj_data.get("children", [])
                layout_refs[obj_id] = children
        
        # Check for cycles using DFS
        visited = set()
        rec_stack = set()
        
        def has_cycle(node):
            if node in rec_stack:
                return True
            if node in visited:
                return False
            
            visited.add(node)
            rec_stack.add(node)
            
            for child in layout_refs.get(node, []):
                if child in layout_refs and has_cycle(child):
                    return True
            
            rec_stack.remove(node)
            return False
        
        for node in layout_refs:
            if node not in visited:
                if has_cycle(node):
                    messages.append(ValidationMessage(
                        ValidationSeverity.ERROR,
                        f"Circular dependency detected in layout container: {node}",
                        "Layout containers cannot have circular references"
                    ))
        
        return messages
    
    def _validate_scene_properties(self, properties: Dict[str, Any]) -> List[ValidationMessage]:
        """Validate scene-level properties"""
        messages: List[ValidationMessage] = []
        
        # Validate resolution
        if "resolution" in properties:
            resolution = properties["resolution"]
            if not isinstance(resolution, (list, tuple)) or len(resolution) != 2:
                messages.append(ValidationMessage(
                    ValidationSeverity.ERROR,
                    "Scene resolution must be a 2D coordinate",
                    f"Got: {resolution}"
                ))
            else:
                try:
                    width, height = int(resolution[0]), int(resolution[1])
                    if width < self.min_resolution_width or width > self.max_resolution_width:
                        messages.append(ValidationMessage(
                            ValidationSeverity.ERROR,
                            f"Scene width {width} is outside allowed range",
                            f"Range: {self.min_resolution_width}-{self.max_resolution_width}"
                        ))
                    if height < self.min_resolution_height or height > self.max_resolution_height:
                        messages.append(ValidationMessage(
                            ValidationSeverity.ERROR,
                            f"Scene height {height} is outside allowed range",
                            f"Range: {self.min_resolution_height}-{self.max_resolution_height}"
                        ))
                except (ValueError, TypeError):
                    messages.append(ValidationMessage(
                        ValidationSeverity.ERROR,
                        "Scene resolution must be valid integers",
                        f"Got: {resolution}"
                    ))
        
        # Validate frame rate
        if "frame_rate" in properties:
            try:
                fps = float(properties["frame_rate"])
                if fps < self.min_frame_rate or fps > self.max_frame_rate:
                    messages.append(ValidationMessage(
                        ValidationSeverity.ERROR,
                        f"Frame rate {fps} is outside allowed range",
                        f"Range: {self.min_frame_rate}-{self.max_frame_rate} FPS"
                    ))
            except (ValueError, TypeError):
                messages.append(ValidationMessage(
                    ValidationSeverity.ERROR,
                    "Frame rate must be a valid number",
                    f"Got: {properties['frame_rate']}"
                ))
        
        # Validate duration
        if "duration" in properties:
            try:
                duration = float(properties["duration"])
                if duration <= 0:
                    messages.append(ValidationMessage(
                        ValidationSeverity.ERROR,
                        "Scene duration must be positive",
                        f"Got: {duration}"
                    ))
                elif duration > self.max_animation_duration:
                    messages.append(ValidationMessage(
                        ValidationSeverity.WARNING,
                        f"Scene duration is very long: {duration}s",
                        f"Maximum recommended: {self.max_animation_duration}s"
                    ))
            except (ValueError, TypeError):
                messages.append(ValidationMessage(
                    ValidationSeverity.ERROR,
                    "Scene duration must be a valid number",
                    f"Got: {properties['duration']}"
                ))
        
        return messages
    
    def _validate_assets(self, scene_graph: Dict[str, Any]) -> List[ValidationMessage]:
        """Validate file paths and assets"""
        messages: List[ValidationMessage] = []
        
        # Check for file references in the scene graph
        def check_file_paths(obj):
            if isinstance(obj, dict):
                for key, value in obj.items():
                    if key in ["file_path", "image_path", "font_path", "audio_path"]:
                        if not isinstance(value, str):
                            messages.append(ValidationMessage(
                                ValidationSeverity.ERROR,
                                f"File path '{key}' must be a string",
                                f"Got: {value}"
                            ))
                        elif not Path(value).exists():
                            messages.append(ValidationMessage(
                                ValidationSeverity.WARNING,
                                f"File does not exist: {value}",
                                "Asset will not be available during rendering"
                            ))
                    else:
                        check_file_paths(value)
            elif isinstance(obj, list):
                for item in obj:
                    check_file_paths(item)
        
        check_file_paths(scene_graph)
        
        return messages
    
    def validate_timing_bounds(self, animations: List[Dict[str, Any]]) -> ValidationResult:
        """
        Validate that all animation timing bounds are non-negative
        
        Args:
            animations: List of animation dictionaries
            
        Returns:
            ValidationResult with timing validation messages
        """
        messages: List[ValidationMessage] = []
        
        for i, animation in enumerate(animations):
            if not isinstance(animation, dict):
                messages.append(ValidationMessage(
                    ValidationSeverity.ERROR,
                    f"Animation {i} must be a dictionary",
                    f"Got: {type(animation).__name__}"
                ))
                continue
            
            if "keyframes" not in animation:
                messages.append(ValidationMessage(
                    ValidationSeverity.ERROR,
                    f"Animation {i} missing keyframes"
                ))
                continue
            
            keyframes = animation["keyframes"]
            if not isinstance(keyframes, list):
                messages.append(ValidationMessage(
                    ValidationSeverity.ERROR,
                    f"Animation {i} keyframes must be a list",
                    f"Got: {type(keyframes).__name__}"
                ))
                continue
            
            # Check keyframe timing
            for j, keyframe in enumerate(keyframes):
                if not isinstance(keyframe, dict):
                    messages.append(ValidationMessage(
                        ValidationSeverity.ERROR,
                        f"Animation {i} keyframe {j} must be a dictionary",
                        f"Got: {type(keyframe).__name__}"
                    ))
                    continue
                
                if "time" not in keyframe:
                    messages.append(ValidationMessage(
                        ValidationSeverity.ERROR,
                        f"Animation {i} keyframe {j} missing time field"
                    ))
                    continue
                
                try:
                    time = float(keyframe["time"])
                    if time < 0:
                        messages.append(ValidationMessage(
                            ValidationSeverity.ERROR,
                            f"Animation {i} keyframe {j} time must be non-negative",
                            f"Got: {time}"
                        ))
                except (ValueError, TypeError):
                    messages.append(ValidationMessage(
                        ValidationSeverity.ERROR,
                        f"Animation {i} keyframe {j} time must be a valid number",
                        f"Got: {keyframe['time']}"
                    ))
        
        is_valid = all(msg.severity != ValidationSeverity.ERROR for msg in messages)
        return ValidationResult(is_valid, messages)
    
    def validate_before_rendering(self, scene_graph: Dict[str, Any]) -> ValidationResult:
        """
        Comprehensive validation before rendering
        
        Args:
            scene_graph: Scene graph to validate
            
        Returns:
            ValidationResult with all validation messages
        """
        # Combine all validation checks
        all_messages: List[ValidationMessage] = []
        
        # Validate scene graph structure
        graph_result = self.validate_scene_graph(scene_graph)
        all_messages.extend(graph_result.messages)
        
        # Validate animations separately for timing
        animations = scene_graph.get("animations", {})
        if animations:
            timing_result = self.validate_timing_bounds(list(animations.values()))
            all_messages.extend(timing_result.messages)
        
        is_valid = all(msg.severity != ValidationSeverity.ERROR for msg in all_messages)
        return ValidationResult(is_valid, all_messages)