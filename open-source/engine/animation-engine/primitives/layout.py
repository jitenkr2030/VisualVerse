"""
VisualVerse Animation Engine - Layout System

This module is part of the VisualVerse Animation Engine,
which is licensed under the Apache License, Version 2.0.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Provides layout containers like VGroup (vertical stack), HGroup (horizontal stack),
and Grid for arranging primitives automatically.
"""

from typing import List, Optional, Dict, Any, Tuple, Union
from dataclasses import dataclass
from enum import Enum
import math

from .geometry import Point, Transform
from .text import Text

class LayoutDirection(Enum):
    """Layout direction enumeration"""
    HORIZONTAL = "horizontal"
    VERTICAL = "vertical"

class Alignment(Enum):
    """Alignment enumeration"""
    START = "start"
    CENTER = "center"
    END = "end"
    STRETCH = "stretch"

class Justification(Enum):
    """Content justification enumeration"""
    START = "start"
    CENTER = "center"
    END = "end"
    SPACE_BETWEEN = "space_between"
    SPACE_AROUND = "space_around"
    SPACE_EVENLY = "space_evenly"

@dataclass
class LayoutConfig:
    """Configuration for layout containers"""
    direction: LayoutDirection = LayoutDirection.HORIZONTAL
    spacing: float = 10.0
    padding: float = 0.0
    alignment: Alignment = Alignment.CENTER
    justification: Justification = Justification.CENTER
    wrap: bool = False
    wrap_spacing: float = 10.0
    fit_content: bool = True
    
    def validate(self):
        """Validate layout configuration"""
        if self.spacing < 0:
            raise ValueError("Spacing cannot be negative")
        if self.padding < 0:
            raise ValueError("Padding cannot be negative")
        if self.wrap_spacing < 0:
            raise ValueError("Wrap spacing cannot be negative")

class LayoutContainer:
    """Base class for layout containers"""
    
    def __init__(self, config: Optional[LayoutConfig] = None):
        self.config = config or LayoutConfig()
        self.config.validate()
        
        self.children: List[Any] = []
        self.bounding_box: Optional[Tuple[Point, Point]] = None
        
    def add_child(self, child: Any):
        """Add a child element to the container"""
        self.children.append(child)
        self._invalidate_layout()
    
    def remove_child(self, child: Any):
        """Remove a child element from the container"""
        if child in self.children:
            self.children.remove(child)
            self._invalidate_layout()
    
    def clear_children(self):
        """Remove all children from the container"""
        self.children.clear()
        self._invalidate_layout()
    
    def _invalidate_layout(self):
        """Mark layout as needing recalculation"""
        self.bounding_box = None
    
    def calculate_layout(self):
        """Calculate the layout for all children"""
        if not self.children:
            self.bounding_box = None
            return
        
        # Default implementation - subclasses should override
        self._calculate_default_layout()
    
    def _calculate_default_layout(self):
        """Default layout calculation (simple positioning)"""
        if not self.children:
            return
        
        x_offset = self.config.padding
        y_offset = self.config.padding
        
        for child in self.children:
            if hasattr(child, 'get_bounding_box'):
                bbox = child.get_bounding_box()
                if bbox:
                    # Apply offset based on direction
                    if self.config.direction == LayoutDirection.HORIZONTAL:
                        # Position to the right of previous child
                        if hasattr(child, 'position'):
                            child.position = Point(x_offset, y_offset)
                        x_offset += bbox[1].x - bbox[0].x + self.config.spacing
                    else:  # VERTICAL
                        # Position below previous child
                        if hasattr(child, 'position'):
                            child.position = Point(x_offset, y_offset)
                        y_offset += bbox[1].y - bbox[0].y + self.config.spacing
        
        # Calculate container bounding box
        self._update_container_bbox()
    
    def _update_container_bbox(self):
        """Update container bounding box"""
        if not self.children:
            return
        
        all_bboxes = []
        for child in self.children:
            if hasattr(child, 'get_bounding_box'):
                bbox = child.get_bounding_box()
                if bbox:
                    all_bboxes.append(bbox)
        
        if not all_bboxes:
            return
        
        min_x = min(bbox[0].x for bbox in all_bboxes)
        min_y = min(bbox[0].y for bbox in all_bboxes)
        max_x = max(bbox[1].x for bbox in all_bboxes)
        max_y = max(bbox[1].y for bbox in all_bboxes)
        
        self.bounding_box = (Point(min_x, min_y), Point(max_x, max_y))
    
    def get_bounding_box(self) -> Optional[Tuple[Point, Point]]:
        """Get the bounding box of the container"""
        if self.bounding_box is None:
            self.calculate_layout()
        return self.bounding_box
    
    def get_content_size(self) -> Tuple[float, float]:
        """Get the size of the content area"""
        bbox = self.get_bounding_box()
        if not bbox:
            return (0, 0)
        
        return (bbox[1].x - bbox[0].x, bbox[1].y - bbox[0].y)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert layout container to dictionary"""
        return {
            "type": self.__class__.__name__,
            "config": {
                "direction": self.config.direction.value,
                "spacing": self.config.spacing,
                "padding": self.config.padding,
                "alignment": self.config.alignment.value,
                "justification": self.config.justification.value,
                "wrap": self.config.wrap,
                "wrap_spacing": self.config.wrap_spacing,
                "fit_content": self.config.fit_content
            },
            "children_count": len(self.children),
            "bounding_box": self._bbox_to_dict(self.bounding_box) if self.bounding_box else None,
            "content_size": self.get_content_size()
        }
    
    def _bbox_to_dict(self, bbox: Optional[Tuple[Point, Point]]) -> Optional[Dict[str, Any]]:
        """Convert bounding box to dictionary"""
        if not bbox:
            return None
        
        return {
            "top_left": {"x": bbox[0].x, "y": bbox[0].y},
            "bottom_right": {"x": bbox[1].x, "y": bbox[1].y}
        }

class VGroup(LayoutContainer):
    """Vertical group - arranges children vertically"""
    
    def __init__(self, config: Optional[LayoutConfig] = None):
        if config is None:
            config = LayoutConfig(direction=LayoutDirection.VERTICAL)
        super().__init__(config)
    
    def calculate_layout(self):
        """Calculate vertical layout"""
        if not self.children:
            self.bounding_box = None
            return
        
        # Sort children by their y position for vertical layout
        sorted_children = sorted(self.children, key=lambda child: self._get_child_y(child))
        
        y_position = self.config.padding
        max_width = 0
        
        for child in sorted_children:
            if hasattr(child, 'get_bounding_box'):
                bbox = child.get_bounding_box()
                if bbox:
                    child_width = bbox[1].x - bbox[0].x
                    child_height = bbox[1].y - bbox[0].y
                    
                    # Calculate x position based on alignment
                    x_position = self._calculate_x_position(child_width, max_width)
                    
                    # Apply positioning
                    if hasattr(child, 'position'):
                        child.position = Point(x_position, y_position)
                    
                    y_position += child_height + self.config.spacing
                    max_width = max(max_width, child_width)
        
        # Update container bounding box
        total_height = y_position - self.config.spacing + self.config.padding
        self.bounding_box = (
            Point(self.config.padding, self.config.padding),
            Point(max_width + self.config.padding, total_height + self.config.padding)
        )
    
    def _calculate_x_position(self, child_width: float, max_width: float) -> float:
        """Calculate x position based on alignment"""
        if self.config.alignment == Alignment.START:
            return self.config.padding
        elif self.config.alignment == Alignment.CENTER:
            return self.config.padding + (max_width - child_width) / 2
        elif self.config.alignment == Alignment.END:
            return self.config.padding + max_width - child_width
        else:  # STRETCH
            return self.config.padding
    
    def _get_child_y(self, child) -> float:
        """Get y position of child for sorting"""
        if hasattr(child, 'position'):
            return child.position.y
        elif hasattr(child, 'get_bounding_box'):
            bbox = child.get_bounding_box()
            if bbox:
                return bbox[0].y
        return 0

class HGroup(LayoutContainer):
    """Horizontal group - arranges children horizontally"""
    
    def __init__(self, config: Optional[LayoutConfig] = None):
        if config is None:
            config = LayoutConfig(direction=LayoutDirection.HORIZONTAL)
        super().__init__(config)
    
    def calculate_layout(self):
        """Calculate horizontal layout"""
        if not self.children:
            self.bounding_box = None
            return
        
        # Sort children by their x position for horizontal layout
        sorted_children = sorted(self.children, key=lambda child: self._get_child_x(child))
        
        x_position = self.config.padding
        max_height = 0
        
        for child in sorted_children:
            if hasattr(child, 'get_bounding_box'):
                bbox = child.get_bounding_box()
                if bbox:
                    child_width = bbox[1].x - bbox[0].x
                    child_height = bbox[1].y - bbox[0].y
                    
                    # Calculate y position based on alignment
                    y_position = self._calculate_y_position(child_height, max_height)
                    
                    # Apply positioning
                    if hasattr(child, 'position'):
                        child.position = Point(x_position, y_position)
                    
                    x_position += child_width + self.config.spacing
                    max_height = max(max_height, child_height)
        
        # Update container bounding box
        total_width = x_position - self.config.spacing + self.config.padding
        self.bounding_box = (
            Point(self.config.padding, self.config.padding),
            Point(total_width + self.config.padding, max_height + self.config.padding)
        )
    
    def _calculate_y_position(self, child_height: float, max_height: float) -> float:
        """Calculate y position based on alignment"""
        if self.config.alignment == Alignment.START:
            return self.config.padding
        elif self.config.alignment == Alignment.CENTER:
            return self.config.padding + (max_height - child_height) / 2
        elif self.config.alignment == Alignment.END:
            return self.config.padding + max_height - child_height
        else:  # STRETCH
            return self.config.padding
    
    def _get_child_x(self, child) -> float:
        """Get x position of child for sorting"""
        if hasattr(child, 'position'):
            return child.position.x
        elif hasattr(child, 'get_bounding_box'):
            bbox = child.get_bounding_box()
            if bbox:
                return bbox[0].x
        return 0

class Grid(LayoutContainer):
    """Grid layout - arranges children in a grid"""
    
    def __init__(self, rows: int, columns: int, config: Optional[LayoutConfig] = None):
        super().__init__(config)
        self.rows = rows
        self.columns = columns
        
        if rows <= 0 or columns <= 0:
            raise ValueError("Rows and columns must be positive")
    
    def calculate_layout(self):
        """Calculate grid layout"""
        if not self.children:
            self.bounding_box = None
            return
        
        # Calculate cell dimensions
        cell_width, cell_height = self._calculate_cell_dimensions()
        
        # Position each child in the grid
        for i, child in enumerate(self.children):
            if i >= self.rows * self.columns:
                break  # Grid is full
            
            row = i // self.columns
            col = i % self.columns
            
            x = col * (cell_width + self.config.spacing) + self.config.padding
            y = row * (cell_height + self.config.spacing) + self.config.padding
            
            if hasattr(child, 'position'):
                child.position = Point(x, y)
        
        # Update container bounding box
        total_width = self.columns * cell_width + (self.columns - 1) * self.config.spacing + 2 * self.config.padding
        total_height = self.rows * cell_height + (self.rows - 1) * self.config.spacing + 2 * self.config.padding
        
        self.bounding_box = (
            Point(0, 0),
            Point(total_width, total_height)
        )
    
    def _calculate_cell_dimensions(self) -> Tuple[float, float]:
        """Calculate dimensions of grid cells"""
        if not self.children:
            return (100, 100)  # Default cell size
        
        # Find the maximum child dimensions
        max_width = 0
        max_height = 0
        
        for child in self.children[:self.rows * self.columns]:
            if hasattr(child, 'get_bounding_box'):
                bbox = child.get_bounding_box()
                if bbox:
                    width = bbox[1].x - bbox[0].x
                    height = bbox[1].y - bbox[0].y
                    max_width = max(max_width, width)
                    max_height = max(max_height, height)
        
        return (max_width, max_height)
    
    def get_cell_position(self, row: int, column: int) -> Optional[Point]:
        """Get the position of a specific grid cell"""
        if not self.bounding_box:
            self.calculate_layout()
        
        if row < 0 or row >= self.rows or column < 0 or column >= self.columns:
            return None
        
        cell_width, cell_height = self._calculate_cell_dimensions()
        x = column * (cell_width + self.config.spacing) + self.config.padding
        y = row * (cell_height + self.config.spacing) + self.config.padding
        
        return Point(x, y)
    
    def get_child_at(self, row: int, column: int) -> Optional[Any]:
        """Get the child at a specific grid position"""
        index = row * self.columns + column
        if 0 <= index < len(self.children):
            return self.children[index]
        return None

class FlexContainer(LayoutContainer):
    """Flexible container that can switch between horizontal and vertical layout"""
    
    def __init__(self, config: Optional[LayoutConfig] = None):
        super().__init__(config)
    
    def set_direction(self, direction: LayoutDirection):
        """Change layout direction"""
        self.config.direction = direction
        self._invalidate_layout()
    
    def wrap_children(self, max_width: float) -> List[List[Any]]:
        """Wrap children into lines based on max width"""
        if not self.children:
            return []
        
        lines = []
        current_line = []
        current_width = 0
        
        for child in self.children:
            if hasattr(child, 'get_bounding_box'):
                bbox = child.get_bounding_box()
                if bbox:
                    child_width = bbox[1].x - bbox[0].x
                    
                    if current_width + child_width + self.config.spacing <= max_width or not current_line:
                        current_line.append(child)
                        current_width += child_width + self.config.spacing
                    else:
                        if current_line:
                            lines.append(current_line)
                        current_line = [child]
                        current_width = child_width
        
        if current_line:
            lines.append(current_line)
        
        return lines

# Utility functions for easy layout creation
def create_vgroup(
    *children,
    spacing: float = 10.0,
    padding: float = 0.0,
    alignment: Alignment = Alignment.CENTER
) -> VGroup:
    """Create a vertical group with children"""
    config = LayoutConfig(
        direction=LayoutDirection.VERTICAL,
        spacing=spacing,
        padding=padding,
        alignment=alignment
    )
    
    group = VGroup(config)
    for child in children:
        group.add_child(child)
    
    return group

def create_hgroup(
    *children,
    spacing: float = 10.0,
    padding: float = 0.0,
    alignment: Alignment = Alignment.CENTER
) -> HGroup:
    """Create a horizontal group with children"""
    config = LayoutConfig(
        direction=LayoutDirection.HORIZONTAL,
        spacing=spacing,
        padding=padding,
        alignment=alignment
    )
    
    group = HGroup(config)
    for child in children:
        group.add_child(child)
    
    return group

def create_grid(
    rows: int,
    columns: int,
    *children,
    spacing: float = 10.0,
    padding: float = 0.0
) -> Grid:
    """Create a grid with children"""
    config = LayoutConfig(
        spacing=spacing,
        padding=padding
    )
    
    grid = Grid(rows, columns, config)
    for child in children:
        grid.add_child(child)
    
    return grid