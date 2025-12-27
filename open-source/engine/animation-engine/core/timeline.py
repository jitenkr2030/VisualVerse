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
Timeline manager for VisualVerse animations.
Handles animation sequencing, timing, and coordination.
"""

import logging
from typing import Dict, Any, Optional, List, Callable, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import asyncio

import manim
from manim.animation.animation import Animation

logger = logging.getLogger(__name__)

class AnimationState(Enum):
    """States of animations in the timeline"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    PAUSED = "paused"
    CANCELLED = "cancelled"

class TimingMode(Enum):
    """Timing modes for animations"""
    IMMEDIATE = "immediate"
    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"
    CONDITIONAL = "conditional"

@dataclass
class TimelineEvent:
    """Represents a single event in the animation timeline"""
    event_id: str
    name: str
    animation: Optional[Animation] = None
    function: Optional[Callable] = None
    start_time: float = 0.0
    duration: float = 0.0
    delay: float = 0.0
    state: AnimationState = AnimationState.PENDING
    dependencies: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        if not self.animation and not self.function:
            raise ValueError("Event must have either animation or function")
    
    @property
    def end_time(self) -> float:
        """Calculate end time of the event"""
        return self.start_time + self.delay + self.duration
    
    @property
    def is_ready(self) -> bool:
        """Check if event dependencies are satisfied"""
        return all(dep for dep in self.dependencies)

@dataclass
class TimelineSegment:
    """A segment of the timeline with multiple events"""
    segment_id: str
    name: str
    start_time: float
    end_time: float
    events: List[TimelineEvent] = field(default_factory=list)
    mode: TimingMode = TimingMode.SEQUENTIAL
    metadata: Dict[str, Any] = field(default_factory=dict)

class TimelineManager:
    """
    Advanced timeline manager for coordinating complex animations.
    
    Provides timeline-based animation sequencing, dependency management,
    and sophisticated timing control.
    """
    
    def __init__(self, scene: Optional[manim.Scene] = None):
        self.scene = scene
        self.timeline = []
        self.current_time = 0.0
        self.total_duration = 0.0
        self.is_playing = False
        self.playback_speed = 1.0
        self.events_registry = {}
        self.callbacks = {}
        
        # Timeline state
        self._timeline_started = False
        self._timeline_completed = False
        
        logger.info("Timeline manager initialized")
    
    def create_segment(self, segment_id: str, name: str, start_time: float = 0.0,
                      mode: TimingMode = TimingMode.SEQUENTIAL) -> TimelineSegment:
        """Create a new timeline segment"""
        segment = TimelineSegment(
            segment_id=segment_id,
            name=name,
            start_time=start_time,
            end_time=start_time,  # Will be updated when events are added
            mode=mode
        )
        
        self.timeline.append(segment)
        return segment
    
    def add_event_to_segment(self, segment_id: str, event: TimelineEvent) -> bool:
        """Add an event to a specific segment"""
        segment = self._get_segment(segment_id)
        if not segment:
            logger.error(f"Segment {segment_id} not found")
            return False
        
        # Add event to segment
        segment.events.append(event)
        self.events_registry[event.event_id] = event
        
        # Update segment end time
        segment.end_time = max(segment.end_time, event.end_time)
        
        # Update total duration
        self.total_duration = max(self.total_duration, segment.end_time)
        
        logger.info(f"Added event {event.event_id} to segment {segment_id}")
        return True
    
    def add_animation_event(self, segment_id: str, event_id: str, name: str,
                           animation: Animation, start_time: float = 0.0,
                           delay: float = 0.0, dependencies: List[str] = None) -> bool:
        """Add an animation event to the timeline"""
        event = TimelineEvent(
            event_id=event_id,
            name=name,
            animation=animation,
            start_time=start_time,
            duration=animation.run_time,
            delay=delay,
            dependencies=dependencies or []
        )
        
        return self.add_event_to_segment(segment_id, event)
    
    def add_function_event(self, segment_id: str, event_id: str, name: str,
                          function: Callable, start_time: float = 0.0,
                          delay: float = 0.0, duration: float = 0.0,
                          dependencies: List[str] = None) -> bool:
        """Add a function event to the timeline"""
        event = TimelineEvent(
            event_id=event_id,
            name=name,
            function=function,
            start_time=start_time,
            duration=duration,
            delay=delay,
            dependencies=dependencies or []
        )
        
        return self.add_event_to_segment(segment_id, event)
    
    def execute_timeline(self, scene: Optional[manim.Scene] = None) -> bool:
        """Execute the entire timeline"""
        if not scene and not self.scene:
            logger.error("No scene provided for timeline execution")
            return False
        
        target_scene = scene or self.scene
        self.is_playing = True
        self._timeline_started = True
        self._timeline_completed = False
        
        logger.info(f"Starting timeline execution with {len(self.timeline)} segments")
        
        try:
            # Sort segments by start time
            sorted_segments = sorted(self.timeline, key=lambda x: x.start_time)
            
            for segment in sorted_segments:
                self._execute_segment(target_scene, segment)
            
            self._timeline_completed = True
            logger.info("Timeline execution completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"Timeline execution failed: {str(e)}", exc_info=True)
            return False
        
        finally:
            self.is_playing = False
    
    def _execute_segment(self, scene: manim.Scene, segment: TimelineSegment):
        """Execute a single timeline segment"""
        logger.info(f"Executing segment: {segment.name}")
        
        # Sort events by start time within segment
        sorted_events = sorted(segment.events, key=lambda x: x.start_time)
        
        if segment.mode == TimingMode.PARALLEL:
            # Execute all events in parallel
            animations = []
            for event in sorted_events:
                if event.animation:
                    animations.append(event.animation)
            
            if animations:
                scene.play(*animations)
        
        elif segment.mode == TimingMode.SEQUENTIAL:
            # Execute events sequentially
            for event in sorted_events:
                self._execute_event(scene, event)
        
        elif segment.mode == TimingMode.IMMEDIATE:
            # Execute all events immediately
            for event in sorted_events:
                if event.animation:
                    scene.play(event.animation)
                elif event.function:
                    event.function()
    
    def _execute_event(self, scene: manim.Scene, event: TimelineEvent):
        """Execute a single event"""
        logger.debug(f"Executing event: {event.name}")
        
        try:
            # Update event state
            event.state = AnimationState.RUNNING
            
            # Wait for dependencies
            if event.dependencies:
                self._wait_for_dependencies(event.dependencies)
            
            # Wait for start time
            if event.start_time > 0:
                scene.wait(event.start_time)
            
            # Wait for delay
            if event.delay > 0:
                scene.wait(event.delay)
            
            # Execute animation or function
            if event.animation:
                scene.play(event.animation)
            elif event.function:
                event.function()
            
            # Update event state
            event.state = AnimationState.COMPLETED
            
        except Exception as e:
            event.state = AnimationState.CANCELLED
            logger.error(f"Event {event.event_id} failed: {str(e)}", exc_info=True)
    
    def _wait_for_dependencies(self, dependencies: List[str]):
        """Wait for dependent events to complete"""
        for dep_id in dependencies:
            dep_event = self.events_registry.get(dep_id)
            if dep_event:
                while dep_event.state != AnimationState.COMPLETED:
                    import time
                    time.sleep(0.1)  # Poll for dependency completion
    
    def _get_segment(self, segment_id: str) -> Optional[TimelineSegment]:
        """Get segment by ID"""
        return next((seg for seg in self.timeline if seg.segment_id == segment_id), None)
    
    def create_intro_sequence(self, duration: float = 3.0) -> str:
        """Create a standard intro sequence"""
        segment_id = "intro"
        segment = self.create_segment(segment_id, "Introduction", 0.0, TimingMode.SEQUENTIAL)
        
        # Add title appearance
        title_event = TimelineEvent(
            event_id="intro_title",
            name="Title Appearance",
            function=lambda: self._create_title_animation(),
            start_time=0.5,
            duration=1.5
        )
        self.add_event_to_segment(segment_id, title_event)
        
        # Add subtitle appearance
        subtitle_event = TimelineEvent(
            event_id="intro_subtitle",
            name="Subtitle Appearance",
            function=lambda: self._create_subtitle_animation(),
            start_time=2.0,
            duration=1.0
        )
        self.add_event_to_segment(segment_id, subtitle_event)
        
        return segment_id
    
    def create_outro_sequence(self, duration: float = 2.0) -> str:
        """Create a standard outro sequence"""
        segment_id = "outro"
        segment = self.create_segment(segment_id, "Conclusion", 0.0, TimingMode.SEQUENTIAL)
        
        # Add thank you message
        outro_event = TimelineEvent(
            event_id="outro_thanks",
            name="Thank You Message",
            function=lambda: self._create_outro_animation(),
            start_time=0.5,
            duration=1.5
        )
        self.add_event_to_segment(segment_id, outro_event)
        
        return segment_id
    
    def _create_title_animation(self):
        """Create title animation"""
        if self.scene:
            title = manim.Text("VisualVerse", font_size=72, color=manim.BLUE)
            title.scale(0)
            self.scene.add(title)
            self.scene.play(title.animate.scale(1.2))
            self.scene.wait(1)
            self.scene.play(title.animate.scale(1.0))
    
    def _create_subtitle_animation(self):
        """Create subtitle animation"""
        if self.scene:
            subtitle = manim.Text("Visual Learning Platform", font_size=36, color=manim.GRAY)
            subtitle.move_to((0, -2, 0))
            subtitle.scale(0)
            self.scene.add(subtitle)
            self.scene.play(subtitle.animate.scale(1))
    
    def _create_outro_animation(self):
        """Create outro animation"""
        if self.scene:
            outro = manim.Text("Thank you for watching!", font_size=48, color=manim.GREEN)
            outro.scale(0)
            self.scene.add(outro)
            self.scene.play(outro.animate.scale(1))
    
    def add_callback(self, event_id: str, callback: Callable, timing: str = "after"):
        """Add callback for event completion"""
        if event_id not in self.callbacks:
            self.callbacks[event_id] = []
        self.callbacks[event_id].append({"callback": callback, "timing": timing})
    
    def get_timeline_status(self) -> Dict[str, Any]:
        """Get current timeline status"""
        total_events = sum(len(seg.events) for seg in self.timeline)
        completed_events = sum(
            len([e for e in seg.events if e.state == AnimationState.COMPLETED])
            for seg in self.timeline
        )
        
        return {
            "total_segments": len(self.timeline),
            "total_events": total_events,
            "completed_events": completed_events,
            "current_time": self.current_time,
            "total_duration": self.total_duration,
            "is_playing": self.is_playing,
            "playback_speed": self.playback_speed,
            "timeline_started": self._timeline_started,
            "timeline_completed": self._timeline_completed,
            "segments": [
                {
                    "id": seg.segment_id,
                    "name": seg.name,
                    "event_count": len(seg.events),
                    "mode": seg.mode.value
                }
                for seg in self.timeline
            ]
        }
    
    def pause_timeline(self):
        """Pause timeline execution"""
        self.is_playing = False
        logger.info("Timeline paused")
    
    def resume_timeline(self):
        """Resume timeline execution"""
        self.is_playing = True
        logger.info("Timeline resumed")
    
    def reset_timeline(self):
        """Reset timeline to initial state"""
        for segment in self.timeline:
            for event in segment.events:
                event.state = AnimationState.PENDING
        
        self.current_time = 0.0
        self.is_playing = False
        self._timeline_started = False
        self._timeline_completed = False
        
        logger.info("Timeline reset")
    
    def export_timeline(self, filename: str):
        """Export timeline configuration to file"""
        import json
        from pathlib import Path
        
        timeline_data = {
            "segments": [
                {
                    "segment_id": seg.segment_id,
                    "name": seg.name,
                    "start_time": seg.start_time,
                    "end_time": seg.end_time,
                    "mode": seg.mode.value,
                    "events": [
                        {
                            "event_id": event.event_id,
                            "name": event.name,
                            "start_time": event.start_time,
                            "duration": event.duration,
                            "delay": event.delay,
                            "dependencies": event.dependencies,
                            "state": event.state.value
                        }
                        for event in seg.events
                    ]
                }
                for seg in self.timeline
            ],
            "metadata": {
                "total_duration": self.total_duration,
                "exported_at": datetime.now().isoformat()
            }
        }
        
        Path(filename).parent.mkdir(parents=True, exist_ok=True)
        with open(filename, 'w') as f:
            json.dump(timeline_data, f, indent=2)
        
        logger.info(f"Timeline exported to: {filename}")

# Convenience functions for common timeline patterns

def create_intro_outro_timeline(duration: float = 5.0) -> Tuple[str, str]:
    """Create a standard intro/outro timeline"""
    intro_id = "intro_sequence"
    outro_id = "outro_sequence"
    
    return intro_id, outro_id

def create_step_by_step_timeline(steps: List[str], step_duration: float = 2.0) -> str:
    """Create a step-by-step timeline"""
    segment_id = "steps"
    segment = TimelineSegment(
        segment_id=segment_id,
        name="Step by Step",
        start_time=0.0,
        end_time=len(steps) * step_duration,
        mode=TimingMode.SEQUENTIAL
    )
    
    for i, step in enumerate(steps):
        event = TimelineEvent(
            event_id=f"step_{i}",
            name=f"Step {i+1}: {step}",
            function=lambda s=step: _display_step(s),
            start_time=i * step_duration,
            duration=step_duration
        )
        segment.events.append(event)
    
    return segment_id

def _display_step(step: str):
    """Display a single step"""
    # Implementation for displaying steps
    pass
