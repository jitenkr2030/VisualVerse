"""
FinVerse Visual Service

This module provides financial visualization and rendering services for the
VisualVerse learning platform. It handles financial charts, portfolio displays,
and technical analysis visualizations.

Author: MiniMax Agent
Version: 1.0.0
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any
from enum import Enum
from .fin_core import (
    Security, Portfolio, Position, OHLCV, ChartType, TimeFrame,
    IndicatorType, TechnicalIndicator, RiskAnalyzer, ChartConfig
)


class ChartStyle(str, Enum):
    """Styles for financial charts."""
    LINE = "line"
    CANDLESTICK = "candlestick"
    BAR = "bar"
    AREA = "area"
    DASHED = "dashed"
    POINTS = "points"


class ColorPalette(str, Enum):
    """Color palettes for financial charts."""
    DEFAULT = "default"
    GREEN_RED = "green_red"
    BLUE_ORANGE = "blue_orange"
    MONOCHROME = "monochrome"
    DARK = "dark"


@dataclass
class DataPoint:
    """A single data point for charting."""
    x: Any  # Can be datetime, number, or string
    y: float
    label: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        result = {"x": str(self.x) if hasattr(self.x, 'strftime') else self.x, "y": self.y}
        if self.label:
            result["label"] = self.label
        if self.metadata:
            result["metadata"] = self.metadata
        return result


@dataclass
class ChartSeries:
    """Represents a data series for charting."""
    name: str
    data: List[DataPoint]
    chart_type: ChartStyle = ChartStyle.LINE
    color: str = "#3B82F6"
    line_width: int = 2
    show_points: bool = True
    fill_area: bool = False
    fill_opacity: float = 0.1
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "data": [dp.to_dict() for dp in self.data],
            "type": self.chart_type.value,
            "color": self.color,
            "lineWidth": self.line_width,
            "showPoints": self.show_points,
            "fillArea": self.fill_area,
            "fillOpacity": self.fill_opacity
        }


@dataclass
class CandlestickData:
    """Candlestick chart data."""
    timestamp: Any
    open: float
    high: float
    low: float
    close: float
    volume: int = 0
    color: str = ""
    
    def __post_init__(self):
        self.color = "#10B981" if self.close >= self.open else "#EF4444"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "timestamp": str(self.timestamp) if hasattr(self.timestamp, 'strftime') else self.timestamp,
            "open": self.open,
            "high": self.high,
            "low": self.low,
            "close": self.close,
            "volume": self.volume,
            "color": self.color
        }


@dataclass
class AxisConfig:
    """Configuration for chart axes."""
    label: str = ""
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    format: str = "number"  # number, currency, percent, date
    decimal_places: int = 2
    show_grid: bool = True
    grid_color: str = "#E5E7EB"


@dataclass
class LegendConfig:
    """Configuration for chart legend."""
    show: bool = True
    position: str = "top"  # top, bottom, left, right
    alignment: str = "start"  # start, center, end


@dataclass
class TooltipConfig:
    """Configuration for chart tooltips."""
    show: bool = True
    format: str = "default"  # default, currency, percent
    decimal_places: int = 2
    show_indicators: bool = True


@dataclass
class FinancialChart:
    """Complete financial chart configuration."""
    config: ChartConfig
    series: List[ChartSeries] = field(default_factory=list)
    candlesticks: List[CandlestickData] = field(default_factory=list)
    x_axis: AxisConfig = field(default_factory=AxisConfig)
    y_axis: AxisConfig = field(default_factory=AxisConfig)
    legend: LegendConfig = field(default_factory=LegendConfig)
    tooltip: TooltipConfig = field(default_factory=TooltipConfig)
    annotations: List[Dict[str, Any]] = field(default_factory=list)
    time_range: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "title": self.config.title,
            "type": self.config.chart_type.value,
            "series": [s.to_dict() for s in self.series],
            "candlesticks": [c.to_dict() for c in self.candlesticks],
            "xAxis": self.x_axis.to_dict() if hasattr(self.x_axis, 'to_dict') else {
                "label": self.x_axis.label
            },
            "yAxis": self.y_axis.to_dict() if hasattr(self.y_axis, 'to_dict') else {
                "label": self.y_axis.label
            },
            "legend": {"show": self.legend.show, "position": self.legend.position},
            "tooltip": {"show": self.tooltip.show, "format": self.tooltip.format},
            "annotations": self.annotations,
            "timeRange": self.time_range
        }
    
    def _axis_to_dict(self, axis: AxisConfig) -> Dict[str, Any]:
        """Convert axis config to dictionary."""
        return {
            "label": axis.label,
            "min": axis.min_value,
            "max": axis.max_value,
            "format": axis.format,
            "decimalPlaces": axis.decimal_places,
            "showGrid": axis.show_grid,
            "gridColor": axis.grid_color
        }


@dataclass
class PortfolioAllocation:
    """Portfolio allocation data for pie/donut charts."""
    label: str
    value: float
    percentage: float
    color: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "label": self.label,
            "value": self.value,
            "percentage": self.percentage,
            "color": self.color
        }


@dataclass
class PerformanceData:
    """Portfolio performance data."""
    date: Any
    value: float
    change: float = 0.0
    change_percent: float = 0.0
    benchmark_value: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "date": str(self.date) if hasattr(self.date, 'strftime') else self.date,
            "value": self.value,
            "change": self.change,
            "changePercent": self.change_percent,
            "benchmarkValue": self.benchmark_value
        }


@dataclass
class RiskMetricsDisplay:
    """Risk metrics for visual display."""
    sharpe_ratio: float = 0.0
    beta: float = 0.0
    volatility: float = 0.0
    max_drawdown: float = 0.0
    var_95: float = 0.0
    var_99: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "sharpeRatio": self.sharpe_ratio,
            "beta": self.beta,
            "volatility": self.volatility,
            "maxDrawdown": self.max_drawdown,
            "var95": self.var_95,
            "var99": self.var_99
        }


@dataclass
class TechnicalIndicatorDisplay:
    """Technical indicator data for charting."""
    indicator_type: IndicatorType
    values: List[float]
    timestamps: List[Any] = field(default_factory=list)
    parameters: Dict[str, Any] = field(default_factory=dict)
    colors: Dict[str, str] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "type": self.indicator_type.value,
            "values": self.values,
            "timestamps": [str(t) for t in self.timestamps],
            "parameters": self.parameters,
            "colors": self.colors
        }


class ChartFactory:
    """Factory for creating financial charts."""
    
    COLORS = {
        "up": "#10B981",
        "down": "#EF4444",
        "primary": "#3B82F6",
        "secondary": "#8B5CF6",
        "tertiary": "#F59E0B",
        "neutral": "#6B7280",
        "grid": "#E5E7EB"
    }
    
    @staticmethod
    def create_price_chart(
        prices: List[float],
        timestamps: List[Any],
        chart_type: ChartType = ChartType.LINE,
        title: str = "Price Chart"
    ) -> FinancialChart:
        """Create a price chart from price data."""
        config = ChartConfig(
            chart_type=chart_type,
            title=title,
            colors=[ChartFactory.COLORS["primary"]]
        )
        
        chart = FinancialChart(config=config)
        
        if chart_type == ChartType.CANDLESTICK:
            # Create candlestick data from OHLCV
            for i, (ts, price) in enumerate(zip(timestamps, prices)):
                # In real implementation, this would use actual OHLCV data
                chart.candlesticks.append(CandlestickData(
                    timestamp=ts,
                    open=price * 0.99,
                    high=price * 1.02,
                    low=price * 0.98,
                    close=price
                ))
        else:
            # Create line/area chart
            series_data = [
                DataPoint(x=ts, y=price)
                for ts, price in zip(timestamps, prices)
            ]
            chart.series.append(ChartSeries(
                name="Price",
                data=series_data,
                chart_type=ChartStyle.LINE if chart_type == ChartType.LINE else ChartStyle.AREA,
                fill_area=chart_type == ChartType.AREA,
                color=ChartFactory.COLORS["primary"]
            ))
        
        chart.x_axis = AxisConfig(
            label="Date",
            format="date"
        )
        chart.y_axis = AxisConfig(
            label="Price",
            format="currency",
            decimal_places=2
        )
        
        return chart
    
    @staticmethod
    def create_portfolio_allocation_chart(
        portfolio: Portfolio,
        chart_type: ChartType = ChartType.PIE
    ) -> FinancialChart:
        """Create a portfolio allocation chart."""
        config = ChartConfig(
            chart_type=chart_type,
            title="Portfolio Allocation"
        )
        
        chart = FinancialChart(config=config)
        
        total_value = portfolio.get_total_value()
        allocations = []
        colors = ["#3B82F6", "#10B981", "#F59E0B", "#8B5CF6", "#EF4444", "#6B7280"]
        color_idx = 0
        
        for position in portfolio.positions:
            weight = position.get_weight(total_value)
            allocations.append(PortfolioAllocation(
                label=position.security.symbol,
                value=position.current_value,
                percentage=weight,
                color=colors[color_idx % len(colors)]
            ))
            color_idx += 1
        
        # Add cash allocation
        if portfolio.cash_balance > 0:
            cash_weight = (portfolio.cash_balance / total_value) * 100
            allocations.append(PortfolioAllocation(
                label="Cash",
                value=portfolio.cash_balance,
                percentage=cash_weight,
                color=colors[color_idx % len(colors)]
            ))
        
        # Store allocations in metadata for rendering
        chart.annotations = [{"type": "allocation", "data": [a.to_dict() for a in allocations]}]
        
        return chart
    
    @staticmethod
    def create_performance_chart(
        performance_data: List[PerformanceData],
        show_benchmark: bool = True
    ) -> FinancialChart:
        """Create a portfolio performance chart."""
        config = ChartConfig(
            chart_type=ChartType.AREA,
            title="Portfolio Performance"
        )
        
        chart = FinancialChart(config=config)
        
        series_data = [
            DataPoint(x=p.date, y=p.value)
            for p in performance_data
        ]
        chart.series.append(ChartSeries(
            name="Portfolio",
            data=series_data,
            chart_type=ChartStyle.AREA,
            fill_area=True,
            fill_opacity=0.2,
            color=ChartFactory.COLORS["primary"]
        ))
        
        if show_benchmark:
            benchmark_data = [
                DataPoint(x=p.date, y=p.benchmark_value)
                for p in performance_data
            ]
            chart.series.append(ChartSeries(
                name="Benchmark",
                data=benchmark_data,
                chart_type=ChartStyle.LINE,
                color=ChartFactory.COLORS["neutral"],
                line_width=1,
                show_points=False
            ))
        
        return chart
    
    @staticmethod
    def create_technical_indicator_chart(
        prices: List[float],
        timestamps: List[Any],
        indicator_type: IndicatorType,
        parameters: Dict[str, Any] = None
    ) -> Tuple[FinancialChart, TechnicalIndicatorDisplay]:
        """Create a chart with technical indicators."""
        params = parameters or {}
        
        if indicator_type == IndicatorType.SMA:
            period = params.get("period", 20)
            values = TechnicalIndicator.calculate_sma(prices, period)
            start_idx = len(prices) - len(values)
            indicator_data = TechnicalIndicatorDisplay(
                indicator_type=indicator_type,
                values=values,
                timestamps=timestamps[start_idx:],
                parameters={"period": period},
                colors={"sma": ChartFactory.COLORS["secondary"]}
            )
        elif indicator_type == IndicatorType.EMA:
            period = params.get("period", 20)
            values = TechnicalIndicator.calculate_ema(prices, period)
            start_idx = len(prices) - len(values)
            indicator_data = TechnicalIndicatorDisplay(
                indicator_type=indicator_type,
                values=values,
                timestamps=timestamps[start_idx:],
                parameters={"period": period},
                colors={"ema": ChartFactory.COLORS["secondary"]}
            )
        elif indicator_type == IndicatorType.RSI:
            period = params.get("period", 14)
            values = TechnicalIndicator.calculate_rsi(prices, period)
            start_idx = len(prices) - len(values)
            indicator_data = TechnicalIndicatorDisplay(
                indicator_type=indicator_type,
                values=values,
                timestamps=timestamps[start_idx:],
                parameters={"period": period},
                colors={"overbought": "#EF4444", "oversold": "#10B981"}
            )
        elif indicator_type == IndicatorType.MACD:
            result = TechnicalIndicator.calculate_macd(prices)
            indicator_data = TechnicalIndicatorDisplay(
                indicator_type=indicator_type,
                values=result["histogram"],
                timestamps=timestamps[len(prices) - len(result["histogram"]):],
                parameters={},
                colors={"macd": ChartFactory.COLORS["primary"], "signal": ChartFactory.COLORS["secondary"]}
            )
        else:
            indicator_data = TechnicalIndicatorDisplay(
                indicator_type=indicator_type,
                values=[],
                timestamps=[]
            )
        
        # Create the main price chart
        chart = ChartFactory.create_price_chart(prices, timestamps)
        
        return chart, indicator_data
    
    @staticmethod
    def create_risk_return_scatter(
        portfolios: List[Dict[str, float]]
    ) -> FinancialChart:
        """Create a risk-return scatter plot (e.g., for efficient frontier)."""
        config = ChartConfig(
            chart_type=ChartType.SCATTER,
            title="Risk vs Return Analysis"
        )
        
        chart = FinancialChart(config=config)
        
        series_data = [
            DataPoint(x=p["risk"], y=p["return"], label=p.get("name", ""))
            for p in portfolios
        ]
        chart.series.append(ChartSeries(
            name="Portfolios",
            data=series_data,
            chart_type=ChartStyle.POINTS,
            color=ChartFactory.COLORS["primary"],
            show_points=True
        ))
        
        chart.x_axis = AxisConfig(
            label="Risk (Std Dev %)",
            format="percent",
            decimal_places=1
        )
        chart.y_axis = AxisConfig(
            label="Return (%)",
            format="percent",
            decimal_places=1
        )
        
        return chart


class PortfolioVisualizer:
    """Visualizes portfolio data and metrics."""
    
    @staticmethod
    def visualize_portfolio(portfolio: Portfolio) -> Dict[str, Any]:
        """Get complete portfolio visualization data."""
        total_value = portfolio.get_total_value()
        
        positions_data = []
        for pos in portfolio.positions:
            positions_data.append({
                "symbol": pos.security.symbol,
                "name": pos.security.name,
                "quantity": pos.quantity,
                "price": pos.security.current_price,
                "value": pos.current_value,
                "costBasis": pos.quantity * pos.average_cost,
                "unrealizedPnl": pos.unrealized_pnl,
                "unrealizedPnlPercent": pos.unrealized_pnl_percent,
                "weight": pos.get_weight(total_value),
                "assetClass": pos.security.asset_class.value,
                "sector": pos.security.sector
            })
        
        allocation_data = []
        colors = ["#3B82F6", "#10B981", "#F59E0B", "#8B5CF6", "#EF4444", "#6B7280"]
        color_idx = 0
        allocation = portfolio.get_allocation()
        
        for asset_class, weight in allocation.items():
            allocation_data.append({
                "label": asset_class.replace("_", " ").title(),
                "value": total_value * weight / 100,
                "percentage": weight,
                "color": colors[color_idx % len(colors)]
            )
            color_idx += 1
        
        return {
            "summary": {
                "totalValue": total_value,
                "totalCostBasis": portfolio.get_total_cost_basis(),
                "totalUnrealizedPnl": portfolio.get_total_unrealized_pnl(),
                "totalUnrealizedPnlPercent": portfolio.get_total_unrealized_pnl_percent(),
                "cashBalance": portfolio.cash_balance,
                "positionCount": len(portfolio.positions)
            },
            "positions": positions_data,
            "allocation": allocation_data,
            "performance": {
                "daily": 0,
                "weekly": 0,
                "monthly": 0,
                "ytd": 0,
                "annual": 0
            }
        }
    
    @staticmethod
    def visualize_risk_metrics(
        returns: List[float],
        portfolio_value: float = 100000
    ) -> RiskMetricsDisplay:
        """Calculate and visualize risk metrics."""
        volatility = RiskAnalyzer.calculate_volatility(returns) * 100
        sharpe = RiskAnalyzer.calculate_sharpe_ratio(returns)
        max_dd = RiskAnalyzer.calculate_max_drawdown(
            [100 * (1 + r) for r in [0] + returns]
        )
        var_95 = RiskAnalyzer.calculate_var(returns, 0.95) * portfolio_value
        var_99 = RiskAnalyzer.calculate_var(returns, 0.99) * portfolio_value
        
        return RiskMetricsDisplay(
            sharpe_ratio=round(sharpe, 2),
            beta=1.0,  # Would need market returns for actual calculation
            volatility=round(volatility, 2),
            max_drawdown=round(max_dd, 2),
            var_95=round(var_95, 2),
            var_99=round(var_99, 2)
        )


class CorrelationHeatmap:
    """Generates correlation matrix heatmap data."""
    
    @staticmethod
    def generate_heatmap_data(
        assets: Dict[str, List[float]]
    ) -> Dict[str, Any]:
        """Generate correlation heatmap data from asset returns."""
        assets_returns = {}
        for symbol, prices in assets.items():
            returns = RiskAnalyzer.calculate_returns(prices)
            if returns:
                assets_returns[symbol] = returns
        
        symbols = list(assets_returns.keys())
        n = len(symbols)
        
        matrix = []
        for i, symbol1 in enumerate(symbols):
            row = []
            for j, symbol2 in enumerate(symbols):
                if i == j:
                    corr = 1.0
                else:
                    corr = RiskAnalyzer.calculate_correlation(
                        assets_returns[symbol1],
                        assets_returns[symbol2]
                    )
                row.append(round(corr, 3))
            matrix.append(row)
        
        return {
            "symbols": symbols,
            "matrix": matrix,
            "minColor": "#EF4444",
            "maxColor": "#10B981",
            "neutralColor": "#FFFFFF"
        }


class FinVerseVisualService:
    """
    Service for financial visualization and rendering.
    
    This service provides comprehensive visualization capabilities for
    financial data including charts, portfolios, and technical analysis.
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        """Initialize the visual service."""
        self.config = config or {}
        self.chart_factory = ChartFactory()
        self.portfolio_visualizer = PortfolioVisualizer()
    
    def configure(self, config: Dict[str, Any]) -> None:
        """Configure the service with custom settings."""
        self.config.update(config)
        if "default_chart_type" in config:
            self._default_chart_type = ChartType(config["default_chart_type"])
    
    def create_price_chart(
        self,
        prices: List[float],
        timestamps: List[Any],
        chart_type: str = "line"
    ) -> Dict[str, Any]:
        """Create a price chart."""
        chart = self.chart_factory.create_price_chart(
            prices, timestamps, ChartType(chart_type)
        )
        return chart.to_dict()
    
    def create_portfolio_chart(
        self,
        portfolio: Portfolio,
        chart_type: str = "pie"
    ) -> Dict[str, Any]:
        """Create a portfolio allocation chart."""
        chart = self.chart_factory.create_portfolio_allocation_chart(
            portfolio, ChartType(chart_type)
        )
        return chart.to_dict()
    
    def create_performance_chart(
        self,
        performance_data: List[PerformanceData],
        show_benchmark: bool = True
    ) -> Dict[str, Any]:
        """Create a portfolio performance chart."""
        chart = self.chart_factory.create_performance_chart(
            performance_data, show_benchmark
        )
        return chart.to_dict()
    
    def add_technical_indicators(
        self,
        prices: List[float],
        timestamps: List[Any],
        indicator: str,
        parameters: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Add technical indicators to price chart."""
        chart, indicator_data = self.chart_factory.create_technical_indicator_chart(
            prices, timestamps, IndicatorType(indicator), parameters
        )
        return {
            "chart": chart.to_dict(),
            "indicator": indicator_data.to_dict()
        }
    
    def get_portfolio_visualization(self, portfolio: Portfolio) -> Dict[str, Any]:
        """Get complete portfolio visualization."""
        return self.portfolio_visualizer.visualize_portfolio(portfolio)
    
    def get_risk_visualization(
        self,
        returns: List[float],
        portfolio_value: float = 100000
    ) -> Dict[str, Any]:
        """Get risk metrics visualization."""
        metrics = self.portfolio_visualizer.visualize_risk_metrics(
            returns, portfolio_value
        )
        return metrics.to_dict()
    
    def get_correlation_heatmap(
        self,
        assets: Dict[str, List[float]]
    ) -> Dict[str, Any]:
        """Get correlation heatmap data."""
        return CorrelationHeatmap.generate_heatmap_data(assets)
    
    def create_risk_return_plot(
        self,
        portfolios: List[Dict[str, float]]
    ) -> Dict[str, Any]:
        """Create a risk-return scatter plot."""
        chart = self.chart_factory.create_risk_return_scatter(portfolios)
        return chart.to_dict()
    
    def export_chart_data(
        self,
        chart: FinancialChart,
        format: str = "json"
    ) -> str:
        """Export chart data in the specified format."""
        data = chart.to_dict()
        
        if format == "json":
            return json.dumps(data, indent=2)
        elif format == "dict":
            return data
        else:
            return str(data)


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


__all__ = [
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
    "create_fin_visual_service"
]
