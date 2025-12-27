"""
Time Utilities for VisualVerse Engine

Helpers for timestamp formatting, timezone conversions, and calculating
duration between frames for animation timing.
"""

from typing import Union, Optional, Dict, Any
from datetime import datetime, timedelta, timezone
import time
import re

def now_utc() -> datetime:
    """Get current UTC time"""
    return datetime.now(timezone.utc)

def now_local() -> datetime:
    """Get current local time"""
    return datetime.now()

def timestamp_to_datetime(timestamp: Union[int, float, str]) -> datetime:
    """
    Convert various timestamp formats to datetime object
    
    Args:
        timestamp: Timestamp in various formats (int, float, or ISO string)
        
    Returns:
        datetime object in UTC
    """
    if isinstance(timestamp, (int, float)):
        # Unix timestamp
        return datetime.fromtimestamp(timestamp, tz=timezone.utc)
    elif isinstance(timestamp, str):
        # ISO format string
        try:
            # Handle Z suffix
            if timestamp.endswith('Z'):
                timestamp = timestamp[:-1] + '+00:00'
            return datetime.fromisoformat(timestamp)
        except ValueError:
            raise ValueError(f"Invalid timestamp format: {timestamp}")
    else:
        raise ValueError(f"Unsupported timestamp type: {type(timestamp)}")

def datetime_to_timestamp(dt: datetime) -> float:
    """
    Convert datetime to Unix timestamp
    
    Args:
        dt: datetime object
        
    Returns:
        Unix timestamp (float)
    """
    if dt.tzinfo is None:
        # Assume UTC if no timezone info
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.timestamp()

def format_duration(seconds: Union[int, float], format_type: str = "hms") -> str:
    """
    Format duration in seconds to human-readable string
    
    Args:
        seconds: Duration in seconds
        format_type: Format type ('hms', 'compact', 'words')
        
    Returns:
        Formatted duration string
    """
    if seconds < 0:
        seconds = 0
    
    if format_type == "hms":
        # Hours:Minutes:Seconds format
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{secs:02d}"
        else:
            return f"{minutes:02d}:{secs:02d}"
    
    elif format_type == "compact":
        # Compact format (1h 30m 45s)
        parts = []
        
        hours = int(seconds // 3600)
        if hours > 0:
            parts.append(f"{hours}h")
        
        minutes = int((seconds % 3600) // 60)
        if minutes > 0:
            parts.append(f"{minutes}m")
        
        secs = int(seconds % 60)
        if secs > 0 or not parts:
            parts.append(f"{secs}s")
        
        return " ".join(parts)
    
    elif format_type == "words":
        # Full words format
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        
        parts = []
        if hours > 0:
            parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
        if minutes > 0:
            parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
        if secs > 0 or not parts:
            parts.append(f"{secs} second{'s' if secs != 1 else ''}")
        
        if len(parts) == 1:
            return parts[0]
        elif len(parts) == 2:
            return f"{parts[0]} and {parts[1]}"
        else:
            return f"{parts[0]}, {parts[1]} and {parts[2]}"
    
    else:
        raise ValueError(f"Unknown format type: {format_type}")

def parse_duration(duration_str: str) -> float:
    """
    Parse duration string to seconds
    
    Args:
        duration_str: Duration string in various formats
        
    Returns:
        Duration in seconds
    """
    duration_str = duration_str.strip().lower()
    
    # Try direct float conversion
    try:
        return float(duration_str)
    except ValueError:
        pass
    
    # Parse time format (HH:MM:SS or MM:SS)
    time_pattern = r'^(\d{1,2}):(\d{1,2}):(\d{1,2})$'
    match = re.match(time_pattern, duration_str)
    if match:
        hours, minutes, seconds = map(int, match.groups())
        return hours * 3600 + minutes * 60 + seconds
    
    # Parse compact format (e.g., "1h 30m 45s", "90m", "30s")
    total_seconds = 0
    
    # Hours
    hours_match = re.search(r'(\d+(?:\.\d+)?)\s*h', duration_str)
    if hours_match:
        total_seconds += float(hours_match.group(1)) * 3600
    
    # Minutes
    minutes_match = re.search(r'(\d+(?:\.\d+)?)\s*m', duration_str)
    if minutes_match:
        total_seconds += float(minutes_match.group(1)) * 60
    
    # Seconds
    seconds_match = re.search(r'(\d+(?:\.\d+)?)\s*s', duration_str)
    if seconds_match:
        total_seconds += float(seconds_match.group(1))
    
    if total_seconds > 0:
        return total_seconds
    
    raise ValueError(f"Could not parse duration string: {duration_str}")

def frames_to_duration(frame_count: int, fps: float) -> float:
    """
    Calculate duration from frame count and FPS
    
    Args:
        frame_count: Number of frames
        fps: Frames per second
        
    Returns:
        Duration in seconds
    """
    if fps <= 0:
        raise ValueError("FPS must be positive")
    
    return frame_count / fps

def duration_to_frames(duration: float, fps: float) -> int:
    """
    Calculate frame count from duration and FPS
    
    Args:
        duration: Duration in seconds
        fps: Frames per second
        
    Returns:
        Number of frames
    """
    if fps <= 0:
        raise ValueError("FPS must be positive")
    
    return int(round(duration * fps))

def calculate_frame_time(frame_number: int, fps: float) -> float:
    """
    Calculate timestamp for a specific frame
    
    Args:
        frame_number: Frame number (0-based or 1-based)
        fps: Frames per second
        
    Returns:
        Timestamp in seconds from start
    """
    if fps <= 0:
        raise ValueError("FPS must be positive")
    
    return frame_number / fps

def interpolate_time(start_time: float, end_time: float, progress: float) -> float:
    """
    Interpolate time between start and end based on progress
    
    Args:
        start_time: Start time in seconds
        end_time: End time in seconds
        progress: Progress ratio (0.0 to 1.0)
        
    Returns:
        Interpolated time in seconds
    """
    progress = max(0.0, min(1.0, progress))  # Clamp to [0, 1]
    return start_time + (end_time - start_time) * progress

def get_timezone_aware_now(timezone_str: str = "UTC") -> datetime:
    """
    Get current time in specified timezone
    
    Args:
        timezone_str: Timezone identifier (e.g., "UTC", "America/New_York")
        
    Returns:
        Current time in specified timezone
    """
    try:
        tz = timezone(timedelta(seconds=time.timezone))
        if timezone_str != "UTC":
            # This is a simplified implementation
            # In production, you'd use pytz or zoneinfo
            tz = timezone.utc
        
        return datetime.now(tz)
    except Exception:
        # Fallback to UTC
        return datetime.now(timezone.utc)

def format_timestamp(dt: datetime, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    Format datetime with custom format string
    
    Args:
        dt: datetime object
        format_str: strftime format string
        
    Returns:
        Formatted timestamp string
    """
    return dt.strftime(format_str)

def format_timestamp_utc(dt: datetime, include_tz: bool = True) -> str:
    """
    Format datetime as ISO 8601 string
    
    Args:
        dt: datetime object
        include_tz: Whether to include timezone info
        
    Returns:
        ISO 8601 formatted string
    """
    if include_tz and dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    
    iso_str = dt.isoformat()
    
    if include_tz and not dt.tzinfo:
        iso_str += "Z"
    
    return iso_str

def time_difference(start_dt: datetime, end_dt: Optional[datetime] = None) -> Dict[str, Any]:
    """
    Calculate detailed time difference between two datetimes
    
    Args:
        start_dt: Start datetime
        end_dt: End datetime (defaults to now)
        
    Returns:
        Dictionary with time difference breakdown
    """
    if end_dt is None:
        end_dt = now_utc()
    
    if start_dt.tzinfo is None:
        start_dt = start_dt.replace(tzinfo=timezone.utc)
    if end_dt.tzinfo is None:
        end_dt = end_dt.replace(tzinfo=timezone.utc)
    
    diff = end_dt - start_dt
    total_seconds = diff.total_seconds()
    
    # Calculate breakdown
    days = diff.days
    seconds_remainder = diff.seconds
    hours = seconds_remainder // 3600
    seconds_remainder %= 3600
    minutes = seconds_remainder // 60
    seconds = seconds_remainder % 60
    
    return {
        "total_seconds": total_seconds,
        "total_minutes": total_seconds / 60,
        "total_hours": total_seconds / 3600,
        "total_days": total_seconds / 86400,
        "days": days,
        "hours": hours,
        "minutes": minutes,
        "seconds": seconds,
        "microseconds": diff.microseconds,
        "formatted": format_duration(abs(total_seconds)),
        "is_future": total_seconds < 0,
        "is_past": total_seconds > 0,
        "is_present": abs(total_seconds) < 1.0
    }

def time_since(timestamp: Union[int, float, str]) -> Dict[str, Any]:
    """
    Calculate time since a given timestamp
    
    Args:
        timestamp: Timestamp to compare against now
        
    Returns:
        Dictionary with time since breakdown
    """
    dt = timestamp_to_datetime(timestamp)
    return time_difference(dt, now_utc())

def time_until(timestamp: Union[int, float, str]) -> Dict[str, Any]:
    """
    Calculate time until a given timestamp
    
    Args:
        timestamp: Future timestamp
        
    Returns:
        Dictionary with time until breakdown
    """
    dt = timestamp_to_datetime(timestamp)
    return time_difference(now_utc(), dt)

def validate_time_range(start_time: Union[int, float, str], end_time: Union[int, float, str]) -> bool:
    """
    Validate that end time is after start time
    
    Args:
        start_time: Start timestamp
        end_time: End timestamp
        
    Returns:
        True if valid range, False otherwise
    """
    try:
        start_dt = timestamp_to_datetime(start_time)
        end_dt = timestamp_to_datetime(end_time)
        return end_dt > start_dt
    except Exception:
        return False

def get_animation_timing_info(fps: float, duration: float, total_frames: Optional[int] = None) -> Dict[str, Any]:
    """
    Get comprehensive animation timing information
    
    Args:
        fps: Frames per second
        duration: Animation duration in seconds
        total_frames: Total frames (auto-calculated if None)
        
    Returns:
        Dictionary with timing information
    """
    if fps <= 0:
        raise ValueError("FPS must be positive")
    
    if total_frames is None:
        total_frames = duration_to_frames(duration, fps)
    
    frame_duration = 1.0 / fps
    
    return {
        "fps": fps,
        "duration_seconds": duration,
        "total_frames": total_frames,
        "frame_duration": frame_duration,
        "frame_duration_ms": frame_duration * 1000,
        "total_duration_formatted": format_duration(duration),
        "frame_duration_formatted": format_duration(frame_duration, "compact"),
        "effective_fps": total_frames / duration if duration > 0 else 0,
        "estimated_render_time": duration * 0.1  # Rough estimate (10x real-time)
    }