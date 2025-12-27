"""
FinVerse Animation Service

This module provides animation services for financial data and scenarios in the
VisualVerse learning platform. It handles market animations, scenario transitions,
and time-based visualizations.

Author: MiniMax Agent
Version: 1.0.0
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple, Callable
from enum import Enum
from .fin_core import (
    Portfolio, Position, ScenarioInputs, ScenarioResult, ScenarioPlanner,
    OHLCV, Security, TimeFrame
)


class AnimationState(str, Enum):
    """States of animation playback."""
    IDLE = "idle"
    PLAYING = "playing"
    PAUSED = "paused"
    COMPLETED = "completed"
    ERROR = "error"


class AnimationEasing(str, Enum):
    """Easing functions for smooth animations."""
    LINEAR = "linear"
    EASE_IN = "ease_in"
    EASE_OUT = "ease_out"
    EASE_IN_OUT = "ease_in_out"
    BOUNCE = "bounce"


class AnimationType(str, Enum):
    """Types of financial animations."""
    PRICE_UPDATE = "price_update"
    PORTFOLIO_GROWTH = "portfolio_growth"
    SCENARIO_COMPARISON = "scenario_comparison"
    REBALANCING = "rebalancing"
    MARKET_TICKER = "market_ticker"
    SCROLL = "scroll"
    FADE = "fade"


@dataclass
class AnimationFrame:
    """A single frame of animation data."""
    timestamp: float
    data: Dict[str, Any] = field(default_factory=dict)
    interpolation_factor: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "timestamp": self.timestamp,
            "data": self.data,
            "interpolationFactor": self.interpolation_factor
        }


@dataclass
class Keyframe:
    """Animation keyframe with interpolation settings."""
    time_ms: float
    value: Any
    easing: AnimationEasing = AnimationEASE_IN_OUT
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "timeMs": self.time_ms,
            "value": self.value,
            "easing": self.easing.value
        }


@dataclass
class AnimationConfig:
    """Configuration for animations."""
    duration_ms: int = 1000
    fps: int = 30
    easing: AnimationEasing = AnimationEASE_IN_OUT
    loop: bool = False
    auto_play: bool = False
    preserve_state: bool = True


@dataclass
class PriceAnimation:
    """Animation for price updates."""
    symbol: str
    start_price: float
    end_price: float
    frames: List[AnimationFrame] = field(default_factory=list)
    config: AnimationConfig = field(default_factory=AnimationConfig)
    state: AnimationState = AnimationState.IDLE
    
    @property
    def change_percent(self) -> float:
        """Get the price change percentage."""
        if self.start_price == 0:
            return 0
        return ((self.end_price - self.start_price) / self.start_price) * 100
    
    def get_progress(self) -> float:
        """Get animation progress as a fraction (0-1)."""
        if not self.frames:
            return 0.0
        return self.frames[-1].timestamp / self.config.duration_ms if self.config.duration_ms > 0 else 1.0


@dataclass
class PortfolioAnimation:
    """Animation for portfolio changes."""
    portfolio_id: str
    start_portfolio: Dict[str, Any]
    end_portfolio: Dict[str, Any]
    frames: List[AnimationFrame] = field(default_factory=list)
    config: AnimationConfig = field(default_factory=AnimationConfig)
    state: AnimationState = AnimationState.IDLE
    
    def get_progress(self) -> float:
        """Get animation progress."""
        if not self.frames:
            return 0.0
        return self.frames[-1].timestamp / self.config.duration_ms if self.config.duration_ms > 0 else 1.0


@dataclass
class ScenarioAnimation:
    """Animation for scenario comparisons."""
    scenarios: List[ScenarioResult] = field(default_factory=list)
    frames: List[AnimationFrame] = field(default_factory=list)
    current_scenario_index: int = 0
    config: AnimationConfig = field(default_factory=AnimationConfig)
    state: AnimationState = AnimationState.IDLE
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "scenarios": [s.to_dict() for s in self.scenarios],
            "currentScenarioIndex": self.current_scenario_index,
            "state": self.state.value,
            "progress": self.get_progress()
        }
    
    def get_progress(self) -> float:
        """Get animation progress."""
        if not self.frames:
            return 0.0
        return self.frames[-1].timestamp / self.config.duration_ms if self.config.duration_ms > 0 else 1.0


@dataclass
class TransitionState:
    """State for smooth transitions between data states."""
    from_state: Dict[str, Any]
    to_state: Dict[str, Any]
    progress: float = 0.0
    interpolated_state: Dict[str, Any] = field(default_factory=dict)
    
    def interpolate(self, progress: float) -> Dict[str, Any]:
        """Interpolate between states."""
        self.progress = progress
        self.interpolated_state = {}
        
        for key in self.from_state:
            if key in self.to_state:
                start = self.from_state[key]
                end = self.to_state[key]
                if isinstance(start, (int, float)) and isinstance(end, (int, float)):
                    self.interpolated_state[key] = start + (end - start) * progress
                else:
                    self.interpolated_state[key] = end if progress > 0.5 else start
        
        return self.interpolated_state


class EasingFunctions:
    """Collection of easing functions."""
    
    @staticmethod
    def linear(t: float) -> float:
        """Linear easing."""
        return t
    
    @staticmethod
    def ease_in(t: float) -> float:
        """Ease in - starts slow, accelerates."""
        return t * t
    
    @staticmethod
    def ease_out(t: float) -> float:
        """Ease out - starts fast, decelerates."""
        return t * (2 - t)
    
    @staticmethod
    def ease_in_out(t: float) -> float:
        """Ease in out - slow start and end, fast middle."""
        return 2 * t * t if t < 0.5 else 1 - pow(-2 * t + 2, 2) / 2
    
    @staticmethod
    def apply(easing: AnimationEasing, t: float) -> float:
        """Apply an easing function."""
        functions = {
            AnimationEasing.LINEAR: EasingFunctions.linear,
            AnimationEasing.EASE_IN: EasingFunctions.ease_in,
            AnimationEasing.EASE_OUT: EasingFunctions.ease_out,
            AnimationEasing.EASE_IN_OUT: EasingFunctions.ease_in_out,
        }
        func = functions.get(easing, EasingFunctions.linear)
        return func(t)


class PriceAnimator:
    """Handles price update animations."""
    
    @staticmethod
    def animate_price_change(
        start_price: float,
        end_price: float,
        config: AnimationConfig = None
    ) -> PriceAnimation:
        """Create a price change animation."""
        cfg = config or AnimationConfig()
        
        animation = PriceAnimation(
            symbol="",
            start_price=start_price,
            end_price=end_price,
            config=cfg
        )
        
        num_frames = int(cfg.duration_ms / 1000 * cfg.fps)
        
        for i in range(num_frames + 1):
            progress = i / num_frames
            eased_progress = EasingFunctions.apply(cfg.easing, progress)
            current_price = start_price + (end_price - start_price) * eased_progress
            
            animation.frames.append(AnimationFrame(
                timestamp=i * (cfg.duration_ms / num_frames),
                data={"price": current_price},
                interpolation_factor=eased_progress
            ))
        
        return animation
    
    @staticmethod
    def animate_price_series(
        prices: List[float],
        config: AnimationConfig = None
    ) -> List[PriceAnimation]:
        """Create animations for a series of price updates."""
        cfg = config or AnimationConfig()
        animations = []
        
        for i in range(1, len(prices)):
            animation = PriceAnimator.animate_price_change(
                prices[i-1], prices[i], cfg
            )
            animation.symbol = f"Price update {i}"
            animations.append(animation)
        
        return animations


class PortfolioAnimator:
    """Handles portfolio change animations."""
    
    @staticmethod
    def animate_portfolio_change(
        portfolio_id: str,
        start_portfolio: Dict[str, Any],
        end_portfolio: Dict[str, Any],
        config: AnimationConfig = None
    ) -> PortfolioAnimation:
        """Create a portfolio change animation."""
        cfg = config or AnimationConfig()
        
        animation = PortfolioAnimation(
            portfolio_id=portfolio_id,
            start_portfolio=start_portfolio,
            end_portfolio=end_portfolio,
            config=cfg
        )
        
        num_frames = int(cfg.duration_ms / 1000 * cfg.fps)
        
        for i in range(num_frames + 1):
            progress = i / num_frames
            eased_progress = EasingFunctions.apply(cfg.easing, progress)
            
            frame_data = {}
            for key in start_portfolio:
                if key in end_portfolio:
                    start = start_portfolio[key]
                    end = end_portfolio[key]
                    if isinstance(start, (int, float)) and isinstance(end, (int, float)):
                        frame_data[key] = start + (end - start) * eased_progress
                    else:
                        frame_data[key] = end if progress > 0.5 else start
            
            animation.frames.append(AnimationFrame(
                timestamp=i * (cfg.duration_ms / num_frames),
                data=frame_data,
                interpolation_factor=eased_progress
            ))
        
        return animation
    
    @staticmethod
    def animate_rebalancing(
        start_weights: Dict[str, float],
        end_weights: Dict[str, float],
        config: AnimationConfig = None
    ) -> PortfolioAnimation:
        """Create a rebalancing animation."""
        cfg = config or AnimationConfig()
        
        start_portfolio = {"weights": start_weights, "rebalancing": True}
        end_portfolio = {"weights": end_weights, "rebalancing": False}
        
        return PortfolioAnimator.animate_portfolio_change(
            "rebalance", start_portfolio, end_portfolio, cfg
        )


class ScenarioAnimator:
    """Handles scenario comparison animations."""
    
    @staticmethod
    def animate_scenario_comparison(
        inputs: ScenarioInputs,
        variations: List[Dict[str, Any]] = None,
        config: AnimationConfig = None
    ) -> ScenarioAnimation:
        """Create a scenario comparison animation."""
        cfg = config or AnimationConfig()
        
        animation = ScenarioAnimation(config=cfg)
        
        # Base scenario
        base_result = ScenarioPlanner.project_growth(inputs)
        animation.scenarios.append(base_result)
        
        # Variations
        if variations:
            for variation in variations:
                modified_inputs = ScenarioInputs(
                    initial_investment=variation.get("initial_investment", inputs.initial_investment),
                    monthly_contribution=variation.get("monthly_contribution", inputs.monthly_contribution),
                    annual_return_rate=variation.get("annual_return_rate", inputs.annual_return_rate),
                    inflation_rate=variation.get("inflation_rate", inputs.inflation_rate),
                    investment_horizon_years=inputs.investment_horizon_years
                )
                result = ScenarioPlanner.project_growth(modified_inputs)
                result.scenario_name = variation.get("name", "Variant")
                animation.scenarios.append(result)
        
        # Generate animation frames for transitions
        num_frames = int(cfg.duration_ms / 1000 * cfg.fps)
        
        for i in range(num_frames + 1):
            progress = i / num_frames
            eased_progress = EasingFunctions.apply(cfg.easing, progress)
            
            # Interpolate between scenario results
            frame_data = {"progress": eased_progress}
            
            animation.frames.append(AnimationFrame(
                timestamp=i * (cfg.duration_ms / num_frames),
                data=frame_data,
                interpolation_factor=eased_progress
            ))
        
        return animation
    
    @staticmethod
    def animate_growth_projection(
        scenario_result: ScenarioResult,
        config: AnimationConfig = None
    ) -> ScenarioAnimation:
        """Create an animation for growth projection."""
        cfg = config or AnimationConfig()
        
        animation = ScenarioAnimation(
            scenarios=[scenario_result],
            config=cfg
        )
        
        num_frames = int(cfg.duration_ms / 1000 * cfg.fps)
        
        for i in range(num_frames + 1):
            progress = i / num_frames
            eased_progress = EasingFunctions.apply(cfg.easing, progress)
            
            # Calculate interpolated value at this point
            year_idx = int(eased_progress * len(scenario_result.yearly_projections))
            year_idx = min(year_idx, len(scenario_result.yearly_projections) - 1)
            
            frame_data = {
                "progress": eased_progress,
                "year": scenario_result.yearly_projections[year_idx]["year"],
                "balance": scenario_result.yearly_projections[year_idx]["balance"],
                "contributions": scenario_result.yearly_projections[year_idx]["contributions"],
                "earnings": scenario_result.yearly_projections[year_idx]["earnings"]
            }
            
            animation.frames.append(AnimationFrame(
                timestamp=i * (cfg.duration_ms / num_frames),
                data=frame_data,
                interpolation_factor=eased_progress
            ))
        
        return animation


class MarketTickerAnimator:
    """Handles market ticker animations."""
    
    @staticmethod
    def create_ticker_data(
        securities: List[Security],
        update_interval_ms: int = 5000
    ) -> Dict[str, Any]:
        """Create ticker animation data."""
        ticker_items = []
        
        for security in securities:
            change = security.get_price_change_percent()
            ticker_items.append({
                "symbol": security.symbol,
                "price": security.current_price,
                "change": change,
                "changeColor": "#10B981" if change >= 0 else "#EF4444",
                "direction": "up" if change >= 0 else "down"
            })
        
        return {
            "items": ticker_items,
            "updateIntervalMs": update_interval_ms,
            "scrollSpeed": "normal",
            "pauseOnHover": True
        }


class FinVerseAnimationService:
    """
    Service for financial animations and transitions.
    
    This service provides comprehensive animation capabilities for financial
    data including price updates, portfolio changes, and scenario comparisons.
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        """Initialize the animation service."""
        self.config = config or {}
        self._active_animations: Dict[str, Any] = {}
    
    def configure(self, config: Dict[str, Any]) -> None:
        """Configure the service with custom settings."""
        self.config.update(config)
        if "default_duration" in config:
            self._default_duration = config["default_duration"]
    
    def animate_price_change(
        self,
        start_price: float,
        end_price: float,
        duration_ms: int = None
    ) -> PriceAnimation:
        """Create a price change animation."""
        duration = duration_ms or self.config.get("default_duration", 1000)
        config = AnimationConfig(duration_ms=duration)
        return PriceAnimator.animate_price_change(start_price, end_price, config)
    
    def animate_price_series(
        self,
        prices: List[float],
        duration_ms: int = None
    ) -> List[PriceAnimation]:
        """Create animations for a series of price updates."""
        duration = duration_ms or self.config.get("default_duration", 500)
        config = AnimationConfig(duration_ms=duration)
        return PriceAnimator.animate_price_series(prices, config)
    
    def animate_portfolio_change(
        self,
        portfolio_id: str,
        start_portfolio: Dict[str, Any],
        end_portfolio: Dict[str, Any],
        duration_ms: int = None
    ) -> PortfolioAnimation:
        """Create a portfolio change animation."""
        duration = duration_ms or self.config.get("default_duration", 2000)
        config = AnimationConfig(duration_ms=duration)
        return PortfolioAnimator.animate_portfolio_change(
            portfolio_id, start_portfolio, end_portfolio, config
        )
    
    def animate_rebalancing(
        self,
        start_weights: Dict[str, float],
        end_weights: Dict[str, float],
        duration_ms: int = None
    ) -> PortfolioAnimation:
        """Create a portfolio rebalancing animation."""
        duration = duration_ms or self.config.get("default_duration", 1500)
        config = AnimationConfig(duration_ms=duration)
        return PortfolioAnimator.animate_rebalancing(start_weights, end_weights, config)
    
    def animate_scenario_comparison(
        self,
        inputs: ScenarioInputs,
        variations: List[Dict[str, Any]] = None,
        duration_ms: int = None
    ) -> ScenarioAnimation:
        """Create a scenario comparison animation."""
        duration = duration_ms or self.config.get("default_duration", 3000)
        config = AnimationConfig(duration_ms=duration)
        return ScenarioAnimator.animate_scenario_comparison(
            inputs, variations, config
        )
    
    def animate_growth_projection(
        self,
        scenario_result: ScenarioResult,
        duration_ms: int = None
    ) -> ScenarioAnimation:
        """Create a growth projection animation."""
        duration = duration_ms or self.config.get("default_duration", 2000)
        config = AnimationConfig(duration_ms=duration)
        return ScenarioAnimator.animate_growth_projection(scenario_result, config)
    
    def create_market_ticker(
        self,
        securities: List[Security],
        update_interval_ms: int = 5000
    ) -> Dict[str, Any]:
        """Create market ticker animation data."""
        return MarketTickerAnimator.create_ticker_data(
            securities, update_interval_ms
        )
    
    def get_animation_frame(
        self,
        animation: Any,
        time_ms: float
    ) -> Optional[AnimationFrame]:
        """Get a specific frame from an animation."""
        if hasattr(animation, 'frames'):
            for frame in animation.frames:
                if abs(frame.timestamp - time_ms) < 1:
                    return frame
        return None
    
    def get_animation_data(
        self,
        animation: Any,
        format: str = "json"
    ) -> str:
        """Get animation data for rendering."""
        if hasattr(animation, 'to_dict'):
            data = animation.to_dict()
        else:
            data = {"error": "Animation type not supported"}
        
        if format == "json":
            return json.dumps(data, indent=2)
        return str(data)
    
    def get_animation_status(self, animation: Any) -> Dict[str, Any]:
        """Get the current status of an animation."""
        return {
            "state": animation.state.value if hasattr(animation.state, 'value') else "unknown",
            "progress": animation.get_progress() if hasattr(animation, 'get_progress') else 0,
            "duration_ms": animation.config.duration_ms if hasattr(animation, 'config') else 0
        }


def create_fin_animation_service(config: dict = None) -> FinVerseAnimationService:
    """
    Create a FinVerseAnimationService instance.
    
    Args:
        config: Optional configuration dictionary
        
    Returns:
        Configured FinVerseAnimationService instance
    """
    service = FinVerseAnimationService(config)
    return service


__all__ = [
    "AnimationState",
    "AnimationEasing",
    "AnimationType",
    "AnimationFrame",
    "Keyframe",
    "AnimationConfig",
    "PriceAnimation",
    "PortfolioAnimation",
    "ScenarioAnimation",
    "TransitionState",
    "EasingFunctions",
    "PriceAnimator",
    "PortfolioAnimator",
    "ScenarioAnimator",
    "MarketTickerAnimator",
    "FinVerseAnimationService",
    "create_fin_animation_service"
]
