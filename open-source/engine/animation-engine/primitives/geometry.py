"""
VisualVerse Animation Engine - Geometric Primitives

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

Defines abstract base classes for shapes and implements concrete classes
for Circle, Rectangle, Polygon, Line, and BezierCurve with coordinate
and transformation support.
"""

import math
import numpy as np
from abc import ABC, abstractmethod
from typing import List, Tuple, Optional, Union, Dict, Any
from dataclasses import dataclass
from enum import Enum

class ShapeType(Enum):
    """Enumeration of supported shape types"""
    CIRCLE = "circle"
    RECTANGLE = "rectangle"
    POLYGON = "polygon"
    LINE = "line"
    BEZIER_CURVE = "bezier_curve"
    ELLIPSE = "ellipse"
    TRIANGLE = "triangle"

@dataclass
class Point:
    """Represents a 2D point"""
    x: float
    y: float
    
    def distance_to(self, other: 'Point') -> float:
        """Calculate distance to another point"""
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)
    
    def __add__(self, other: 'Point') -> 'Point':
        return Point(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other: 'Point') -> 'Point':
        return Point(self.x - other.x, self.y - other.y)
    
    def __mul__(self, scalar: float) -> 'Point':
        return Point(self.x * scalar, self.y * scalar)
    
    def __repr__(self):
        return f"Point({self.x}, {self.y})"

@dataclass
class Transform:
    """Represents a 2D transformation"""
    translation: Point = Point(0, 0)
    rotation: float = 0.0  # degrees
    scale_x: float = 1.0
    scale_y: float = 1.0
    
    def apply(self, point: Point) -> Point:
        """Apply transformation to a point"""
        # Translation
        x = point.x + self.translation.x
        y = point.y + self.translation.y
        
        # Scale
        x *= self.scale_x
        y *= self.scale_y
        
        # Rotation (if needed for future 3D support)
        if self.rotation != 0:
            angle_rad = math.radians(self.rotation)
            cos_a = math.cos(angle_rad)
            sin_a = math.sin(angle_rad)
            x_new = x * cos_a - y * sin_a
            y_new = x * sin_a + y * cos_a
            x, y = x_new, y_new
        
        return Point(x, y)

class Shape(ABC):
    """Abstract base class for all geometric shapes"""
    
    def __init__(self, shape_type: ShapeType):
        self.shape_type = shape_type
        self.transform = Transform()
        self.color = (0, 0, 0)  # RGB
        self.fill_color: Optional[Tuple[int, int, int]] = None
        self.stroke_width: float = 1.0
        self.opacity: float = 1.0
    
    @abstractmethod
    def get_coordinates(self) -> List[Point]:
        """Get the geometric coordinates of this shape"""
        pass
    
    @abstractmethod
    def get_bounding_box(self) -> Tuple[Point, Point]:
        """Get the bounding box (top-left, bottom-right) of this shape"""
        pass
    
    def transform_coordinates(self, coordinates: List[Point]) -> List[Point]:
        """Apply transformation to a list of coordinates"""
        return [self.transform.apply(coord) for coord in coordinates]
    
    def get_transformed_coordinates(self) -> List[Point]:
        """Get coordinates after applying transformation"""
        return self.transform_coordinates(self.get_coordinates())
    
    def apply_transform(self, transform: Transform):
        """Apply a transformation to this shape"""
        self.transform = transform
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert shape to dictionary representation"""
        return {
            "type": self.shape_type.value,
            "transform": {
                "translation": {"x": self.transform.translation.x, "y": self.transform.translation.y},
                "rotation": self.transform.rotation,
                "scale_x": self.transform.scale_x,
                "scale_y": self.transform.scale_y
            },
            "color": self.color,
            "fill_color": self.fill_color,
            "stroke_width": self.stroke_width,
            "opacity": self.opacity,
            "coordinates": [{"x": p.x, "y": p.y} for p in self.get_transformed_coordinates()]
        }

class Circle(Shape):
    """Represents a circle"""
    
    def __init__(self, center: Point, radius: float):
        super().__init__(ShapeType.CIRCLE)
        self.center = center
        self.radius = radius
    
    def get_coordinates(self) -> List[Point]:
        """Get circle coordinates (approximate with polygon)"""
        num_points = 32  # Resolution of circle approximation
        coordinates = []
        
        for i in range(num_points):
            angle = 2 * math.pi * i / num_points
            x = self.center.x + self.radius * math.cos(angle)
            y = self.center.y + self.radius * math.sin(angle)
            coordinates.append(Point(x, y))
        
        return coordinates
    
    def get_bounding_box(self) -> Tuple[Point, Point]:
        """Get bounding box of circle"""
        top_left = Point(self.center.x - self.radius, self.center.y - self.radius)
        bottom_right = Point(self.center.x + self.radius, self.center.y + self.radius)
        return (top_left, bottom_right)
    
    def contains_point(self, point: Point) -> bool:
        """Check if a point is inside the circle"""
        distance = point.distance_to(self.center)
        return distance <= self.radius
    
    def area(self) -> float:
        """Calculate circle area"""
        return math.pi * self.radius ** 2
    
    def circumference(self) -> float:
        """Calculate circle circumference"""
        return 2 * math.pi * self.radius

class Rectangle(Shape):
    """Represents a rectangle"""
    
    def __init__(self, top_left: Point, width: float, height: float):
        super().__init__(ShapeType.RECTANGLE)
        self.top_left = top_left
        self.width = width
        self.height = height
    
    def get_coordinates(self) -> List[Point]:
        """Get rectangle coordinates"""
        return [
            self.top_left,
            Point(self.top_left.x + self.width, self.top_left.y),
            Point(self.top_left.x + self.width, self.top_left.y + self.height),
            Point(self.top_left.x, self.top_left.y + self.height)
        ]
    
    def get_bounding_box(self) -> Tuple[Point, Point]:
        """Get bounding box of rectangle"""
        return (self.top_left, Point(self.top_left.x + self.width, self.top_left.y + self.height))
    
    def contains_point(self, point: Point) -> bool:
        """Check if a point is inside the rectangle"""
        return (self.top_left.x <= point.x <= self.top_left.x + self.width and
                self.top_left.y <= point.y <= self.top_left.y + self.height)
    
    def area(self) -> float:
        """Calculate rectangle area"""
        return self.width * self.height
    
    def get_center(self) -> Point:
        """Get center point of rectangle"""
        return Point(
            self.top_left.x + self.width / 2,
            self.top_left.y + self.height / 2
        )

class Polygon(Shape):
    """Represents a general polygon"""
    
    def __init__(self, vertices: List[Point]):
        super().__init__(ShapeType.POLYGON)
        if len(vertices) < 3:
            raise ValueError("Polygon must have at least 3 vertices")
        self.vertices = vertices
    
    def get_coordinates(self) -> List[Point]:
        """Get polygon coordinates"""
        return self.vertices.copy()
    
    def get_bounding_box(self) -> Tuple[Point, Point]:
        """Get bounding box of polygon"""
        xs = [v.x for v in self.vertices]
        ys = [v.y for v in self.vertices]
        
        top_left = Point(min(xs), min(ys))
        bottom_right = Point(max(xs), max(ys))
        return (top_left, bottom_right)
    
    def contains_point(self, point: Point) -> bool:
        """Check if a point is inside the polygon using ray casting"""
        # Simple ray casting algorithm
        x, y = point.x, point.y
        n = len(self.vertices)
        inside = False
        
        p1x, p1y = self.vertices[0].x, self.vertices[0].y
        for i in range(1, n + 1):
            p2x, p2y = self.vertices[i % n].x, self.vertices[i % n].y
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y
        
        return inside
    
    def area(self) -> float:
        """Calculate polygon area using shoelace formula"""
        n = len(self.vertices)
        area = 0.0
        
        for i in range(n):
            j = (i + 1) % n
            area += self.vertices[i].x * self.vertices[j].y
            area -= self.vertices[j].x * self.vertices[i].y
        
        return abs(area) / 2.0

class Triangle(Polygon):
    """Represents a triangle (special case of polygon)"""
    
    def __init__(self, vertex1: Point, vertex2: Point, vertex3: Point):
        super().__init__([vertex1, vertex2, vertex3])
        self.shape_type = ShapeType.TRIANGLE
    
    def get_circumcenter(self) -> Optional[Point]:
        """Get circumcenter of triangle"""
        v1, v2, v3 = self.vertices
        
        # Calculate circumcenter using perpendicular bisectors
        d = 2 * (v1.x * (v2.y - v3.y) + v2.x * (v3.y - v1.y) + v3.x * (v1.y - v2.y))
        
        if abs(d) < 1e-10:  # Points are collinear
            return None
        
        ux = ((v1.x**2 + v1.y**2) * (v2.y - v3.y) + 
              (v2.x**2 + v2.y**2) * (v3.y - v1.y) + 
              (v3.x**2 + v3.y**2) * (v1.y - v2.y)) / d
        
        uy = ((v1.x**2 + v1.y**2) * (v3.x - v2.x) + 
              (v2.x**2 + v2.y**2) * (v1.x - v3.x) + 
              (v3.x**2 + v3.y**2) * (v2.x - v1.x)) / d
        
        return Point(ux, uy)

class Line(Shape):
    """Represents a line segment"""
    
    def __init__(self, start_point: Point, end_point: Point):
        super().__init__(ShapeType.LINE)
        self.start_point = start_point
        self.end_point = end_point
    
    def get_coordinates(self) -> List[Point]:
        """Get line coordinates"""
        return [self.start_point, self.end_point]
    
    def get_bounding_box(self) -> Tuple[Point, Point]:
        """Get bounding box of line"""
        xs = [self.start_point.x, self.end_point.x]
        ys = [self.start_point.y, self.end_point.y]
        
        top_left = Point(min(xs), min(ys))
        bottom_right = Point(max(xs), max(ys))
        return (top_left, bottom_right)
    
    def length(self) -> float:
        """Calculate line length"""
        return self.start_point.distance_to(self.end_point)
    
    def slope(self) -> Optional[float]:
        """Calculate line slope (rise over run)"""
        dx = self.end_point.x - self.start_point.x
        dy = self.end_point.y - self.start_point.y
        
        if abs(dx) < 1e-10:  # Vertical line
            return None
        return dy / dx
    
    def angle(self) -> float:
        """Calculate line angle in degrees"""
        dx = self.end_point.x - self.start_point.x
        dy = self.end_point.y - self.start_point.y
        return math.degrees(math.atan2(dy, dx))

class BezierCurve(Shape):
    """Represents a Bézier curve"""
    
    def __init__(self, control_points: List[Point]):
        super().__init__(ShapeType.BEZIER_CURVE)
        if len(control_points) < 2:
            raise ValueError("Bézier curve must have at least 2 control points")
        self.control_points = control_points
    
    def get_coordinates(self, num_points: int = 100) -> List[Point]:
        """Get Bézier curve coordinates"""
        if len(self.control_points) == 2:
            # Linear Bézier curve
            return self._linear_bezier(num_points)
        elif len(self.control_points) == 3:
            # Quadratic Bézier curve
            return self._quadratic_bezier(num_points)
        elif len(self.control_points) == 4:
            # Cubic Bézier curve
            return self._cubic_bezier(num_points)
        else:
            # General Bézier curve
            return self._general_bezier(num_points)
    
    def _linear_bezier(self, num_points: int) -> List[Point]:
        """Calculate linear Bézier curve"""
        p0, p1 = self.control_points
        points = []
        
        for i in range(num_points + 1):
            t = i / num_points
            x = (1 - t) * p0.x + t * p1.x
            y = (1 - t) * p0.y + t * p1.y
            points.append(Point(x, y))
        
        return points
    
    def _quadratic_bezier(self, num_points: int) -> List[Point]:
        """Calculate quadratic Bézier curve"""
        p0, p1, p2 = self.control_points
        points = []
        
        for i in range(num_points + 1):
            t = i / num_points
            x = (1 - t)**2 * p0.x + 2 * (1 - t) * t * p1.x + t**2 * p2.x
            y = (1 - t)**2 * p0.y + 2 * (1 - t) * t * p1.y + t**2 * p2.y
            points.append(Point(x, y))
        
        return points
    
    def _cubic_bezier(self, num_points: int) -> List[Point]:
        """Calculate cubic Bézier curve"""
        p0, p1, p2, p3 = self.control_points
        points = []
        
        for i in range(num_points + 1):
            t = i / num_points
            x = (1 - t)**3 * p0.x + 3 * (1 - t)**2 * t * p1.x + 3 * (1 - t) * t**2 * p2.x + t**3 * p3.x
            y = (1 - t)**3 * p0.y + 3 * (1 - t)**2 * t * p1.y + 3 * (1 - t) * t**2 * p2.y + t**3 * p3.y
            points.append(Point(x, y))
        
        return points
    
    def _general_bezier(self, num_points: int) -> List[Point]:
        """Calculate general Bézier curve using de Casteljau's algorithm"""
        n = len(self.control_points) - 1
        points = []
        
        for i in range(num_points + 1):
            t = i / num_points
            curve_point = self._de_casteljau(t, self.control_points)
            points.append(curve_point)
        
        return points
    
    def _de_casteljau(self, t: float, points: List[Point]) -> Point:
        """De Casteljau's algorithm for Bézier curve evaluation"""
        if len(points) == 1:
            return points[0]
        
        new_points = []
        for i in range(len(points) - 1):
            x = (1 - t) * points[i].x + t * points[i + 1].x
            y = (1 - t) * points[i].y + t * points[i + 1].y
            new_points.append(Point(x, y))
        
        return self._de_casteljau(t, new_points)
    
    def get_bounding_box(self) -> Tuple[Point, Point]:
        """Get bounding box of Bézier curve"""
        coords = self.get_coordinates()
        xs = [p.x for p in coords]
        ys = [p.y for p in coords]
        
        top_left = Point(min(xs), min(ys))
        bottom_right = Point(max(xs), max(ys))
        return (top_left, bottom_right)

# Factory functions for easy shape creation
def create_circle(center_x: float, center_y: float, radius: float) -> Circle:
    """Create a circle"""
    return Circle(Point(center_x, center_y), radius)

def create_rectangle(x: float, y: float, width: float, height: float) -> Rectangle:
    """Create a rectangle"""
    return Rectangle(Point(x, y), width, height)

def create_triangle(x1: float, y1: float, x2: float, y2: float, x3: float, y3: float) -> Triangle:
    """Create a triangle"""
    return Triangle(Point(x1, y1), Point(x2, y2), Point(x3, y3))

def create_line(x1: float, y1: float, x2: float, y2: float) -> Line:
    """Create a line"""
    return Line(Point(x1, y1), Point(x2, y2))

def create_bezier_curve(control_points: List[Tuple[float, float]]) -> BezierCurve:
    """Create a Bézier curve from control points"""
    points = [Point(x, y) for x, y in control_points]
    return BezierCurve(points)