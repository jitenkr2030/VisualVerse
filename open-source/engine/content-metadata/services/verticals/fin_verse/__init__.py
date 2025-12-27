"""
FinVerse - Financial Visualization and Learning Platform

This package provides comprehensive financial visualization and educational
capabilities for the VisualVerse learning platform. It includes services for
financial concept management, chart visualization, animation, and algorithmic
problem solving.

Submodules:
- fin_core: Mathematical foundations and financial data structures
- fin_concept_service: Formula management and educational content
- fin_visual_service: Financial charts and portfolio visualization
- fin_animation_service: Market data animations and scenario transitions
- fin_reasoning_engine: Financial analysis and calculations

Author: MiniMax Agent
Version: 1.0.0
"""

from .fin_core import (
    AssetClass,
    TransactionType,
    ChartType,
    TimeFrame,
    IndicatorType,
    PriceQuote,
    OHLCV,
    Security,
    Position,
    Transaction,
    Portfolio,
    CashFlow,
    AmortizationSchedule,
    FinancialCalculator,
    RiskAnalyzer,
    TechnicalIndicator,
    ScenarioInputs,
    ScenarioResult,
    ScenarioPlanner,
    ChartConfig,
    PortfolioVisualConfig
)

from .fin_concept_service import (
    FinanceDomain,
    DifficultyLevel,
    FormulaDefinition,
    FinanceConcept,
    LessonContent,
    MarketTerm,
    FormulaRepository,
    ConceptRepository,
    FinVerseConceptService,
    create_fin_concept_service
)

from .fin_visual_service import (
    ChartStyle,
    ColorPalette,
    DataPoint,
    ChartSeries,
    CandlestickData,
    AxisConfig,
    LegendConfig,
    TooltipConfig,
    FinancialChart,
    PortfolioAllocation,
    PerformanceData,
    RiskMetricsDisplay,
    TechnicalIndicatorDisplay,
    ChartFactory,
    PortfolioVisualizer,
    CorrelationHeatmap,
    FinVerseVisualService,
    create_fin_visual_service
)

from .fin_animation_service import (
    AnimationState,
    AnimationEasing,
    AnimationType,
    AnimationFrame,
    Keyframe,
    AnimationConfig,
    PriceAnimation,
    PortfolioAnimation,
    ScenarioAnimation,
    TransitionState,
    EasingFunctions,
    PriceAnimator,
    PortfolioAnimator,
    ScenarioAnimator,
    MarketTickerAnimator,
    FinVerseAnimationService,
    create_fin_animation_service
)

from .fin_reasoning_engine import (
    ProblemDifficulty,
    SolutionStatus,
    SolutionStep,
    ConceptualAnalysis,
    FinancialSolution,
    TimeValueSolver,
    RiskAnalysisSolver,
    TechnicalAnalysisSolver,
    ScenarioPlanningSolver,
    FinVerseReasoningEngine,
    create_fin_reasoning_engine
)


# Factory functions for service creation
def create_fin_concept_service(config: dict = None) -> FinVerseConceptService:
    """
    Create a FinVerseConceptService instance.
    
    Args:
        config: Optional configuration dictionary
        
    Returns:
        Configured FinVerseConceptService instance
    """
    service = FinVerseConceptService(config)
    return service


def create_fin_visual_service(config: dict = None) -> FinVerseVisualService:
    """
    Create a FinVerseVisualService instance.
    
    Args:
        config: Optional configuration dictionary
        
    Returns:
        Configured FinVerseVisualService instance
    """
    service = FinVerseVisualService(config)
    return service


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


def create_fin_reasoning_engine(config: dict = None) -> FinVerseReasoningEngine:
    """
    Create a FinVerseReasoningEngine instance.
    
    Args:
        config: Optional configuration dictionary
        
    Returns:
        Configured FinVerseReasoningEngine instance
    """
    engine = FinVerseReasoningEngine(config)
    return engine


__all__ = [
    # Core Module
    "AssetClass",
    "TransactionType",
    "ChartType",
    "TimeFrame",
    "IndicatorType",
    "PriceQuote",
    "OHLCV",
    "Security",
    "Position",
    "Transaction",
    "Portfolio",
    "CashFlow",
    "AmortizationSchedule",
    "FinancialCalculator",
    "RiskAnalyzer",
    "TechnicalIndicator",
    "ScenarioInputs",
    "ScenarioResult",
    "ScenarioPlanner",
    "ChartConfig",
    "PortfolioVisualConfig",
    
    # Concept Service
    "FinanceDomain",
    "DifficultyLevel",
    "FormulaDefinition",
    "FinanceConcept",
    "LessonContent",
    "MarketTerm",
    "FormulaRepository",
    "ConceptRepository",
    "FinVerseConceptService",
    "create_fin_concept_service",
    
    # Visual Service
    "ChartStyle",
    "ColorPalette",
    "DataPoint",
    "ChartSeries",
    "CandlestickData",
    "AxisConfig",
    "LegendConfig",
    "TooltipConfig",
    "FinancialChart",
    "PortfolioAllocation",
    "PerformanceData",
    "RiskMetricsDisplay",
    "TechnicalIndicatorDisplay",
    "ChartFactory",
    "PortfolioVisualizer",
    "CorrelationHeatmap",
    "FinVerseVisualService",
    "create_fin_visual_service",
    
    # Animation Service
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
    "create_fin_animation_service",
    
    # Reasoning Engine
    "ProblemDifficulty",
    "SolutionStatus",
    "SolutionStep",
    "ConceptualAnalysis",
    "FinancialSolution",
    "TimeValueSolver",
    "RiskAnalysisSolver",
    "TechnicalAnalysisSolver",
    "ScenarioPlanningSolver",
    "FinVerseReasoningEngine",
    "create_fin_reasoning_engine"
]

__version__ = "1.0.0"
__author__ = "MiniMax Agent"
