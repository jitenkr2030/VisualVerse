"""
Base Response Schema for VisualVerse Engine

Defines standard API response wrapper with success boolean, data payload,
error message, and pagination metadata for consistent API responses.
"""

from typing import Any, Dict, Optional, List, Union
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import json

class ResponseStatus(Enum):
    """Response status enumeration"""
    SUCCESS = "success"
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"

@dataclass
class PaginationInfo:
    """Pagination information for list responses"""
    page: int = 1
    page_size: int = 20
    total_items: int = 0
    total_pages: int = 0
    has_next: bool = False
    has_previous: bool = False
    next_page: Optional[int] = None
    previous_page: Optional[int] = None
    
    def __post_init__(self):
        """Calculate derived pagination values"""
        if self.page_size > 0:
            self.total_pages = (self.total_items + self.page_size - 1) // self.page_size
            self.has_next = self.page < self.total_pages
            self.has_previous = self.page > 1
            self.next_page = self.page + 1 if self.has_next else None
            self.previous_page = self.page - 1 if self.has_previous else None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert pagination info to dictionary"""
        return {
            "page": self.page,
            "page_size": self.page_size,
            "total_items": self.total_items,
            "total_pages": self.total_pages,
            "has_next": self.has_next,
            "has_previous": self.has_previous,
            "next_page": self.next_page,
            "previous_page": self.previous_page
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PaginationInfo':
        """Create pagination info from dictionary"""
        return cls(**data)

@dataclass
class ErrorInfo:
    """Error information for error responses"""
    code: str
    message: str
    details: Optional[str] = None
    field: Optional[str] = None  # Field that caused the error
    suggestion: Optional[str] = None  # Suggested fix
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert error info to dictionary"""
        return {
            "code": self.code,
            "message": self.message,
            "details": self.details,
            "field": self.field,
            "suggestion": self.suggestion
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ErrorInfo':
        """Create error info from dictionary"""
        return cls(**data)

@dataclass
class BaseResponse:
    """Base API response wrapper"""
    success: bool
    message: str
    data: Any = None
    errors: List[ErrorInfo] = field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.utcnow)
    request_id: Optional[str] = None
    version: str = "1.0"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert response to dictionary"""
        return {
            "success": self.success,
            "message": self.message,
            "data": self._serialize_data(self.data),
            "errors": [error.to_dict() for error in self.errors],
            "pagination": self.pagination.to_dict() if self.pagination else None,
            "metadata": self.metadata,
            "timestamp": self.timestamp.isoformat() + "Z",
            "request_id": self.request_id,
            "version": self.version
        }
    
    def _serialize_data(self, data: Any) -> Any:
        """Serialize data for JSON response"""
        if data is None:
            return None
        elif isinstance(data, (str, int, float, bool)):
            return data
        elif isinstance(data, (list, tuple)):
            return [self._serialize_data(item) for item in data]
        elif isinstance(data, dict):
            return {key: self._serialize_data(value) for key, value in data.items()}
        elif hasattr(data, 'to_dict'):
            return data.to_dict()
        else:
            # Fallback for complex objects
            try:
                return json.loads(json.dumps(data, default=str))
            except (TypeError, ValueError):
                return str(data)
    
    def to_json(self) -> str:
        """Convert response to JSON string"""
        return json.dumps(self.to_dict(), default=str, indent=2)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BaseResponse':
        """Create response from dictionary"""
        # Handle datetime
        timestamp = data.get("timestamp")
        if isinstance(timestamp, str):
            timestamp = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
        elif timestamp is None:
            timestamp = datetime.utcnow()
        
        # Handle pagination
        pagination_data = data.get("pagination")
        pagination = PaginationInfo.from_dict(pagination_data) if pagination_data else None
        
        # Handle errors
        errors_data = data.get("errors", [])
        errors = [ErrorInfo.from_dict(error_data) for error_data in errors_data]
        
        return cls(
            success=data["success"],
            message=data["message"],
            data=data.get("data"),
            errors=errors,
            pagination=pagination,
            metadata=data.get("metadata", {}),
            timestamp=timestamp,
            request_id=data.get("request_id"),
            version=data.get("version", "1.0")
        )
    
    @classmethod
    def from_json(cls, json_str: str) -> 'BaseResponse':
        """Create response from JSON string"""
        data = json.loads(json_str)
        return cls.from_dict(data)

# Factory methods for common response types
def success_response(
    data: Any = None,
    message: str = "Operation completed successfully",
    pagination: Optional[PaginationInfo] = None,
    metadata: Optional[Dict[str, Any]] = None,
    request_id: Optional[str] = None
) -> BaseResponse:
    """Create a success response"""
    return BaseResponse(
        success=True,
        message=message,
        data=data,
        pagination=pagination,
        metadata=metadata or {},
        request_id=request_id
    )

def error_response(
    message: str,
    code: str = "GENERIC_ERROR",
    details: Optional[str] = None,
    field: Optional[str] = None,
    suggestion: Optional[str] = None,
    data: Any = None,
    request_id: Optional[str] = None
) -> BaseResponse:
    """Create an error response"""
    error_info = ErrorInfo(
        code=code,
        message=message,
        details=details,
        field=field,
        suggestion=suggestion
    )
    
    return BaseResponse(
        success=False,
        message=message,
        data=data,
        errors=[error_info],
        request_id=request_id
    )

def validation_error_response(
    validation_errors: List[ErrorInfo],
    message: str = "Validation failed",
    request_id: Optional[str] = None
) -> BaseResponse:
    """Create a validation error response"""
    return BaseResponse(
        success=False,
        message=message,
        errors=validation_errors,
        request_id=request_id
    )

def paginated_response(
    data: List[Any],
    page: int,
    page_size: int,
    total_items: int,
    message: str = "Data retrieved successfully",
    metadata: Optional[Dict[str, Any]] = None,
    request_id: Optional[str] = None
) -> BaseResponse:
    """Create a paginated response"""
    pagination = PaginationInfo(
        page=page,
        page_size=page_size,
        total_items=total_items
    )
    
    return BaseResponse(
        success=True,
        message=message,
        data=data,
        pagination=pagination,
        metadata=metadata or {},
        request_id=request_id
    )

def warning_response(
    data: Any = None,
    message: str = "Operation completed with warnings",
    warnings: Optional[List[str]] = None,
    metadata: Optional[Dict[str, Any]] = None,
    request_id: Optional[str] = None
) -> BaseResponse:
    """Create a warning response"""
    warning_errors = []
    if warnings:
        warning_errors = [
            ErrorInfo(code="WARNING", message=warning)
            for warning in warnings
        ]
    
    return BaseResponse(
        success=True,  # Still successful but with warnings
        message=message,
        data=data,
        errors=warning_errors,
        metadata=metadata or {},
        request_id=request_id
    )

# Response builder for complex scenarios
class ResponseBuilder:
    """Builder for creating complex responses"""
    
    def __init__(self):
        self._success = True
        self._message = ""
        self._data = None
        self._errors: List[ErrorInfo] = []
        self._pagination: Optional[PaginationInfo] = None
        self._metadata: Dict[str, Any] = {}
        self._request_id: Optional[str] = None
    
    def success(self, message: str = "Operation completed successfully") -> 'ResponseBuilder':
        """Set success status and message"""
        self._success = True
        self._message = message
        return self
    
    def error(self, message: str, code: str = "GENERIC_ERROR", details: Optional[str] = None) -> 'ResponseBuilder':
        """Set error status and message"""
        self._success = False
        self._message = message
        self._errors.append(ErrorInfo(code=code, message=message, details=details))
        return self
    
    def add_error(self, message: str, code: str = "GENERIC_ERROR", details: Optional[str] = None, 
                  field: Optional[str] = None, suggestion: Optional[str] = None) -> 'ResponseBuilder':
        """Add an additional error"""
        self._errors.append(ErrorInfo(code=code, message=message, details=details, field=field, suggestion=suggestion))
        return self
    
    def data(self, data: Any) -> 'ResponseBuilder':
        """Set response data"""
        self._data = data
        return self
    
    def pagination(self, page: int, page_size: int, total_items: int) -> 'ResponseBuilder':
        """Set pagination info"""
        self._pagination = PaginationInfo(page=page, page_size=page_size, total_items=total_items)
        return self
    
    def metadata(self, key: str, value: Any) -> 'ResponseBuilder':
        """Add metadata"""
        self._metadata[key] = value
        return self
    
    def request_id(self, request_id: str) -> 'ResponseBuilder':
        """Set request ID"""
        self._request_id = request_id
        return self
    
    def build(self) -> BaseResponse:
        """Build the final response"""
        return BaseResponse(
            success=self._success,
            message=self._message,
            data=self._data,
            errors=self._errors,
            pagination=self._pagination,
            metadata=self._metadata,
            request_id=self._request_id
        )

# Utility functions
def is_success_response(response: BaseResponse) -> bool:
    """Check if response indicates success"""
    return response.success

def is_error_response(response: BaseResponse) -> bool:
    """Check if response indicates error"""
    return not response.success

def get_response_data(response: BaseResponse) -> Any:
    """Get data from response, handling None"""
    return response.data if response.success else None

def get_response_errors(response: BaseResponse) -> List[ErrorInfo]:
    """Get errors from response"""
    return response.errors

def extract_error_messages(response: BaseResponse) -> List[str]:
    """Extract error messages from response"""
    return [error.message for error in response.errors]

def create_batch_response(results: List[BaseResponse]) -> BaseResponse:
    """Create a response from multiple sub-responses"""
    all_errors = []
    all_data = []
    overall_success = True
    
    for result in results:
        if not result.success:
            overall_success = False
            all_errors.extend(result.errors)
        else:
            all_data.append(result.data)
    
    return BaseResponse(
        success=overall_success,
        message="Batch operation completed",
        data=all_data if all_data else None,
        errors=all_errors
    )