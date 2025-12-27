"""
String Utilities for VisualVerse Engine

Sanitization logic for user inputs and unique ID generation
(UUID/NanoID) for various system identifiers.
"""

import re
import string
import secrets
import hashlib
import uuid
from typing import List, Optional, Dict, Any, Union
from dataclasses import dataclass
from enum import Enum
import unicodedata

class IDType(Enum):
    """ID type enumeration"""
    UUID = "uuid"
    NANO = "nano"
    SHORT = "short"
    CUSTOM = "custom"

@dataclass
class StringValidationResult:
    """Result of string validation"""
    is_valid: bool
    sanitized: str
    errors: List[str]
    warnings: List[str]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "is_valid": self.is_valid,
            "sanitized": self.sanitized,
            "errors": self.errors,
            "warnings": self.warnings
        }

class StringSanitizer:
    """String sanitization utility class"""
    
    # Dangerous characters that should be removed or replaced
    DANGEROUS_CHARS = {
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#x27;',
        '&': '&amp;',
        '/': '&#x2F;',
        '\\': '&#x5C;',
        '`': '&#x60;',
        '=': '&#x3D;'
    }
    
    # Characters to remove completely
    REMOVE_CHARS = {
        '\x00', '\x01', '\x02', '\x03', '\x04', '\x05', '\x06', '\x07',
        '\x08', '\x0B', '\x0C', '\x0E', '\x0F', '\x10', '\x11', '\x12',
        '\x13', '\x14', '\x15', '\x16', '\x17', '\x18', '\x19', '\x1A',
        '\x1B', '\x1C', '\x1D', '\x1E', '\x1F', '\x7F'
    }
    
    # SQL injection patterns
    SQL_PATTERNS = [
        r"(?i)(\b(union|select|insert|update|delete|drop|create|alter|exec|execute)\b)",
        r"(?i)(\bor\b|\band\b|\bnot\b)",
        r"['\";]",
        r"--",
        r"/\*.*?\*/",
        r"\bxp_",
        r"\bsp_"
    ]
    
    # XSS patterns
    XSS_PATTERNS = [
        r"<script[^>]*>.*?</script>",
        r"<[^>]*on\w+[^>]*>",
        r"javascript:",
        r"vbscript:",
        r"onload=",
        r"onerror=",
        r"<iframe[^>]*>",
        r"<object[^>]*>",
        r"<embed[^>]*>"
    ]
    
    @classmethod
    def sanitize_html(cls, text: str, allow_tags: Optional[List[str]] = None) -> str:
        """
        Sanitize HTML text by escaping dangerous characters
        
        Args:
            text: Input text
            allow_tags: List of allowed HTML tags (basic implementation)
            
        Returns:
            Sanitized text
        """
        if not text:
            return ""
        
        # Remove null bytes and control characters
        sanitized = ''.join(char for char in text if char not in cls.REMOVE_CHARS)
        
        # Escape dangerous HTML characters
        for char, replacement in cls.DANGEROUS_CHARS.items():
            sanitized = sanitized.replace(char, replacement)
        
        # Basic tag removal if no tags allowed
        if not allow_tags:
            # Remove HTML tags
            sanitized = re.sub(r'<[^>]+>', '', sanitized)
        else:
            # Basic tag whitelist (simplified)
            for tag in re.findall(r'<(\w+)[^>]*>', sanitized):
                if tag.lower() not in [t.lower() for t in allow_tags]:
                    sanitized = re.sub(rf'<{tag}[^>]*>.*?</{tag}>', '', sanitized, flags=re.IGNORECASE)
                    sanitized = re.sub(rf'<{tag}[^>]*/?>', '', sanitized, flags=re.IGNORECASE)
        
        return sanitized
    
    @classmethod
    def sanitize_filename(cls, filename: str, max_length: int = 255) -> str:
        """
        Sanitize filename for safe file system usage
        
        Args:
            filename: Input filename
            max_length: Maximum filename length
            
        Returns:
            Sanitized filename
        """
        if not filename:
            return "unnamed"
        
        # Remove dangerous characters for filenames
        dangerous_chars = '<>:"/\\|?*'
        sanitized = filename
        
        for char in dangerous_chars:
            sanitized = sanitized.replace(char, '_')
        
        # Remove control characters
        sanitized = ''.join(char for char in sanitized if ord(char) >= 32 and char not in dangerous_chars)
        
        # Replace multiple spaces/underscores with single underscore
        sanitized = re.sub(r'[_\s]+', '_', sanitized)
        
        # Remove leading/trailing dots and underscores
        sanitized = sanitized.strip('._')
        
        # Ensure not empty
        if not sanitized:
            sanitized = "unnamed"
        
        # Truncate if too long
        if len(sanitized) > max_length:
            name_part = sanitized[:max_length-10]
            extension_part = ""
            
            # Try to preserve extension
            if '.' in sanitized:
                name_part, extension_part = sanitized.rsplit('.', 1)
                extension_part = f".{extension_part}"
                if len(name_part) > max_length - len(extension_part) - 10:
                    name_part = name_part[:max_length - len(extension_part) - 10]
            
            sanitized = f"{name_part}_truncated{extension_part}"
        
        return sanitized
    
    @classmethod
    def sanitize_identifier(cls, identifier: str, allow_underscore: bool = True, 
                           allow_numbers: bool = True, max_length: int = 64) -> str:
        """
        Sanitize string for use as identifier (variable name, etc.)
        
        Args:
            identifier: Input identifier
            allow_underscore: Whether to allow underscores
            allow_numbers: Whether to allow numbers
            max_length: Maximum identifier length
            
        Returns:
            Sanitized identifier
        """
        if not identifier:
            return "identifier"
        
        # Start with valid identifier pattern
        pattern = r'[a-zA-Z_]'
        if allow_numbers:
            pattern += r'[a-zA-Z0-9_]*'
        else:
            pattern += r'[a-zA-Z_]*'
        
        # Find valid start
        match = re.search(pattern, identifier)
        if match:
            sanitized = match.group(0)
        else:
            sanitized = "identifier"
        
        # Truncate if too long
        if len(sanitized) > max_length:
            sanitized = sanitized[:max_length]
        
        # Ensure not empty
        if not sanitized:
            sanitized = "identifier"
        
        return sanitized
    
    @classmethod
    def validate_and_sanitize(cls, text: str, max_length: Optional[int] = None,
                             allowed_chars: Optional[str] = None) -> StringValidationResult:
        """
        Validate and sanitize text with detailed feedback
        
        Args:
            text: Input text
            max_length: Maximum allowed length
            allowed_chars: String of allowed characters (if None, allow most chars)
            
        Returns:
            ValidationResult with sanitized text and error details
        """
        errors = []
        warnings = []
        sanitized = text
        
        if not text:
            errors.append("Text is empty")
            return StringValidationResult(False, "", errors, warnings)
        
        # Check length
        if max_length and len(text) > max_length:
            warnings.append(f"Text truncated from {len(text)} to {max_length} characters")
            sanitized = text[:max_length]
        
        # Check for dangerous patterns
        sql_found = any(re.search(pattern, text) for pattern in cls.SQL_PATTERNS)
        if sql_found:
            warnings.append("Potential SQL injection patterns detected")
        
        xss_found = any(re.search(pattern, text) for pattern in cls.XSS_PATTERNS)
        if xss_found:
            errors.append("Potential XSS patterns detected")
        
        # Check allowed characters
        if allowed_chars:
            invalid_chars = set(text) - set(allowed_chars)
            if invalid_chars:
                errors.append(f"Invalid characters found: {', '.join(sorted(invalid_chars))}")
                # Remove invalid characters
                sanitized = ''.join(char for char in sanitized if char in allowed_chars)
        
        # Normalize Unicode
        sanitized = unicodedata.normalize('NFKC', sanitized)
        
        # Final validation
        is_valid = len(errors) == 0 and len(sanitized.strip()) > 0
        
        return StringValidationResult(is_valid, sanitized, errors, warnings)

class IDGenerator:
    """Unique ID generation utility class"""
    
    # Nanoid alphabet (similar to NanoID)
    NANO_ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ_abcdefghijklmnopqrstuvwxyz-"
    
    # Short ID alphabet (more readable)
    SHORT_ALPHABET = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"  # Excludes ambiguous chars
    
    @classmethod
    def generate_uuid(cls, version: int = 4) -> str:
        """
        Generate UUID
        
        Args:
            version: UUID version (1, 3, 4, or 5)
            
        Returns:
            UUID string
        """
        if version == 1:
            return str(uuid.uuid1())
        elif version == 3:
            return str(uuid.uuid3(uuid.NAMESPACE_DNS, str(uuid.getnode())))
        elif version == 4:
            return str(uuid.uuid4())
        elif version == 5:
            return str(uuid.uuid5(uuid.NAMESPACE_DNS, "visualverse"))
        else:
            raise ValueError(f"Unsupported UUID version: {version}")
    
    @classmethod
    def generate_nano_id(cls, length: int = 21, alphabet: Optional[str] = None) -> str:
        """
        Generate NanoID (URL-friendly unique identifier)
        
        Args:
            length: ID length
            alphabet: Custom alphabet (default: NANO_ALPHABET)
            
        Returns:
            NanoID string
        """
        if alphabet is None:
            alphabet = cls.NANO_ALPHABET
        
        return ''.join(secrets.choice(alphabet) for _ in range(length))
    
    @classmethod
    def generate_short_id(cls, length: int = 8, alphabet: Optional[str] = None) -> str:
        """
        Generate short, human-readable ID
        
        Args:
            length: ID length
            alphabet: Custom alphabet (default: SHORT_ALPHABET)
            
        Returns:
            Short ID string
        """
        if alphabet is None:
            alphabet = cls.SHORT_ALPHABET
        
        return ''.join(secrets.choice(alphabet) for _ in range(length))
    
    @classmethod
    def generate_custom_id(cls, pattern: str, **kwargs) -> str:
        """
        Generate ID based on custom pattern
        
        Args:
            pattern: Pattern with placeholders
            **kwargs: Values for placeholders (uuid, nano, short, timestamp, random, hash)
            
        Returns:
            Formatted ID string
        """
        def replace_placeholder(match):
            placeholder = match.group(1)
            
            if placeholder == "uuid":
                return cls.generate_uuid()
            elif placeholder == "nano":
                length = int(match.group(2)) if match.group(2) else 21
                return cls.generate_nano_id(length)
            elif placeholder == "short":
                length = int(match.group(2)) if match.group(2) else 8
                return cls.generate_short_id(length)
            elif placeholder == "timestamp":
                import time
                return str(int(time.time()))
            elif placeholder == "random":
                return str(secrets.randbelow(10**int(match.group(2) or 4)))
            elif placeholder == "hash":
                data = match.group(2)
                return hashlib.md5(data.encode()).hexdigest()[:8]
            
            return match.group(0)
        
        # Pattern: {placeholder:length}
        pattern_regex = r'\{(\w+)(?::(\d+))?\}'
        return re.sub(pattern_regex, replace_placeholder, pattern)
    
    @classmethod
    def generate_job_id(cls) -> str:
        """Generate job ID for rendering tasks"""
        return f"job_{cls.generate_short_id(12)}"
    
    @classmethod
    def generate_session_id(cls) -> str:
        """Generate session ID for user sessions"""
        return f"ses_{cls.generate_nano_id()}"
    
    @classmethod
    def generate_file_id(cls) -> str:
        """Generate file ID for uploaded files"""
        timestamp = str(int(__import__('time').time()))
        nano_part = cls.generate_nano_id(16)
        return f"file_{timestamp}_{nano_part}"
    
    @classmethod
    def generate_project_id(cls) -> str:
        """Generate project ID for user projects"""
        return f"proj_{cls.generate_short_id(10)}"
    
    @classmethod
    def generate_user_id(cls) -> str:
        """Generate user ID for user accounts"""
        return f"user_{cls.generate_uuid()}"
    
    @classmethod
    def generate_render_id(cls) -> str:
        """Generate render ID for render jobs"""
        return f"rnd_{cls.generate_nano_id()}"
    
    @classmethod
    def generate_api_key(cls, prefix: str = "vk") -> str:
        """Generate API key with prefix"""
        return f"{prefix}_{cls.generate_nano_id(32)}"

class TextProcessor:
    """Text processing utilities"""
    
    @classmethod
    def truncate_text(cls, text: str, max_length: int, suffix: str = "...") -> str:
        """
        Truncate text to maximum length with suffix
        
        Args:
            text: Input text
            max_length: Maximum length including suffix
            suffix: Suffix to add when truncating
            
        Returns:
            Truncated text
        """
        if len(text) <= max_length:
            return text
        
        if len(suffix) >= max_length:
            return suffix[:max_length]
        
        return text[:max_length - len(suffix)] + suffix
    
    @classmethod
    def slugify(cls, text: str, lowercase: bool = True, 
                allow_unicode: bool = False) -> str:
        """
        Convert text to URL-friendly slug
        
        Args:
            text: Input text
            lowercase: Convert to lowercase
            allow_unicode: Allow Unicode characters
            
        Returns:
            URL-friendly slug
        """
        if not text:
            return ""
        
        # Normalize Unicode
        text = unicodedata.normalize('NFKD', text)
        
        # Remove combining characters
        text = ''.join(char for char in text if not unicodedata.combining(char))
        
        # Replace spaces and underscores with hyphens
        text = re.sub(r'[_\s]+', '-', text)
        
        # Remove invalid characters
        pattern = r'[^a-zA-Z0-9\-]' if allow_unicode else r'[^a-zA-Z0-9\-\u4e00-\u9fff]'
        text = re.sub(pattern, '', text)
        
        # Remove multiple consecutive hyphens
        text = re.sub(r'-+', '-', text)
        
        # Remove leading/trailing hyphens
        text = text.strip('-')
        
        if lowercase:
            text = text.lower()
        
        return text
    
    @classmethod
    def camel_to_snake(cls, text: str) -> str:
        """Convert CamelCase to snake_case"""
        # Insert underscore between lowercase and uppercase
        text = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', text)
        # Replace multiple underscores with single
        text = re.sub(r'_+', '_', text)
        # Convert to lowercase
        return text.lower()
    
    @classmethod
    def snake_to_camel(cls, text: str, capitalize: bool = False) -> str:
        """Convert snake_case to CamelCase"""
        parts = text.split('_')
        if capitalize:
            parts = [part.capitalize() for part in parts]
        else:
            parts = [parts[0].lower()] + [part.capitalize() for part in parts[1:]]
        return ''.join(parts)
    
    @classmethod
    def remove_duplicates(cls, text: str, preserve_order: bool = True) -> str:
        """Remove duplicate words while preserving order"""
        words = text.split()
        if preserve_order:
            seen = set()
            result = []
            for word in words:
                if word not in seen:
                    seen.add(word)
                    result.append(word)
            return ' '.join(result)
        else:
            return ' '.join(dict.fromkeys(words).keys())
    
    @classmethod
    def count_words(cls, text: str) -> int:
        """Count words in text"""
        if not text:
            return 0
        return len(text.split())
    
    @classmethod
    def count_characters(cls, text: str, include_spaces: bool = True) -> int:
        """Count characters in text"""
        if not text:
            return 0
        if include_spaces:
            return len(text)
        return len(text.replace(' ', ''))
    
    @classmethod
    def extract_keywords(cls, text: str, max_keywords: int = 10, 
                        min_word_length: int = 3) -> List[str]:
        """
        Extract keywords from text (simple implementation)
        
        Args:
            text: Input text
            max_keywords: Maximum number of keywords
            min_word_length: Minimum word length to consider
            
        Returns:
            List of keywords
        """
        if not text:
            return []
        
        # Simple word extraction
        words = re.findall(r'\b[a-zA-Z]{' + str(min_word_length) + r',}\b', text.lower())
        
        # Count word frequency
        word_count = {}
        for word in words:
            word_count[word] = word_count.get(word, 0) + 1
        
        # Sort by frequency and return top keywords
        sorted_words = sorted(word_count.items(), key=lambda x: x[1], reverse=True)
        return [word for word, count in sorted_words[:max_keywords]]

# Utility functions for common operations
def generate_unique_filename(original_name: str, existing_names: List[str]) -> str:
    """Generate unique filename by adding counter if needed"""
    base_name, extension = os.path.splitext(original_name)
    counter = 1
    
    while f"{base_name}{extension}" in existing_names:
        new_name = f"{base_name}_{counter}{extension}"
        counter += 1
    
    return new_name

def sanitize_email(email: str) -> str:
    """Basic email sanitization"""
    return email.strip().lower()

def validate_email(email: str) -> bool:
    """Basic email validation"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def extract_domain_from_url(url: str) -> Optional[str]:
    """Extract domain from URL"""
    try:
        from urllib.parse import urlparse
        parsed = urlparse(url)
        return parsed.netloc
    except Exception:
        return None

def create_hash(content: str, algorithm: str = 'md5') -> str:
    """Create hash from string content"""
    if algorithm == 'md5':
        return hashlib.md5(content.encode()).hexdigest()
    elif algorithm == 'sha1':
        return hashlib.sha1(content.encode()).hexdigest()
    elif algorithm == 'sha256':
        return hashlib.sha256(content.encode()).hexdigest()
    else:
        raise ValueError(f"Unsupported hash algorithm: {algorithm}")