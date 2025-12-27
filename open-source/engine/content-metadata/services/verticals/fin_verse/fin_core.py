"""
FinVerse Core Module

This module provides the mathematical foundations and data structures for financial
computations in the VisualVerse learning platform. It includes classes for securities,
portfolios, market data, time value of money calculations, and risk analysis.

Author: MiniMax Agent
Version: 1.0.0
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple, Callable
from enum import Enum
from decimal import Decimal
import math
from datetime import datetime, date


class AssetClass(str, Enum):
    """Asset classification for securities."""
    EQUITY = "equity"
    FIXED_INCOME = "fixed_income"
    ETF = "etf"
    MUTUAL_FUND = "mutual_fund"
    COMMODITY = "commodity"
    REAL_ESTATE = "real_estate"
    CRYPTO = "crypto"
    CASH = "cash"
    DERIVATIVE = "derivative"


class TransactionType(str, Enum):
    """Types of portfolio transactions."""
    BUY = "buy"
    SELL = "sell"
    DIVIDEND = "dividend"
    INTEREST = "interest"
    FEE = "fee"
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"
    TRANSFER_IN = "transfer_in"
    TRANSFER_OUT = "transfer_out"


class ChartType(str, Enum):
    """Types of financial charts."""
    LINE = "line"
    CANDLESTICK = "candlestick"
    BAR = "bar"
    AREA = "area"
    SCATTER = "scatter"
    PIE = "pie"
    GAUGE = "gauge"
    HEATMAP = "heatmap"


class TimeFrame(str, Enum):
    """Time frames for market data."""
    INTRADAY = "intraday"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    YEARLY = "yearly"


class IndicatorType(str, Enum):
    """Technical analysis indicators."""
    SMA = "sma"
    EMA = "ema"
    RSI = "rsi"
    MACD = "macd"
    BOLLINGER_BANDS = "bollinger_bands"
    ATR = "atr"
    STOCHASTIC = "stochastic"


@dataclass
class PriceQuote:
    """Represents a single price quote."""
    symbol: str
    price: float
    change: float = 0.0
    change_percent: float = 0.0
    bid: float = 0.0
    ask: float = 0.0
    volume: int = 0
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


@dataclass
class OHLCV:
    """Open-High-Low-Close-Volume data for a time period."""
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: int = 0
    
    @property
    def is_bullish(self) -> bool:
        """Check if the period was bullish (close > open)."""
        return self.close >= self.open
    
    @property
    def body_size(self) -> float:
        """Get the size of the candle body."""
        return abs(self.close - self.open)
    
    @property
    def wick_size(self) -> float:
        """Get the size of the wick (high - low)."""
        return self.high - self.low
    
    @property
    def range_percent(self) -> float:
        """Get the price range as a percentage."""
        if self.open == 0:
            return 0
        return ((self.high - self.low) / self.open) * 100


@dataclass
class Security:
    """Represents a financial security."""
    symbol: str
    name: str
    asset_class: AssetClass
    currency: str = "USD"
    exchange: str = ""
    sector: str = ""
    industry: str = ""
    
    # Pricing data
    current_price: float = 0.0
    previous_close: float = 0.0
    day_high: float = 0.0
    day_low: float = 0.0
    volume: int = 0
    
    # Company metrics
    market_cap: float = 0.0
    pe_ratio: float = 0.0
    dividend_yield: float = 0.0
    eps: float = 0.0
    
    def get_price_change(self) -> float:
        """Get the price change from previous close."""
        return self.current_price - self.previous_close
    
    def get_price_change_percent(self) -> float:
        """Get the price change percentage."""
        if self.previous_close == 0:
            return 0
        return (self.get_price_change() / self.previous_close) * 100


@dataclass
class Position:
    """Represents a position in a portfolio."""
    security: Security
    quantity: float
    average_cost: float
    current_value: float = 0.0
    unrealized_pnl: float = 0.0
    unrealized_pnl_percent: float = 0.0
    realized_pnl: float = 0.0
    
    def update_market_value(self, current_price: float) -> None:
        """Update position value based on current market price."""
        self.current_value = self.quantity * current_price
        cost_basis = self.quantity * self.average_cost
        self.unrealized_pnl = self.current_value - cost_basis
        if cost_basis > 0:
            self.unrealized_pnl_percent = (self.unrealized_pnl / cost_basis) * 100
    
    def get_weight(self, portfolio_value: float) -> float:
        """Get position weight in portfolio."""
        if portfolio_value == 0:
            return 0
        return (self.current_value / portfolio_value) * 100


@dataclass
class Transaction:
    """Represents a portfolio transaction."""
    id: str
    security_symbol: str
    transaction_type: TransactionType
    quantity: float
    price_per_unit: float
    fees: float = 0.0
    timestamp: datetime = None
    notes: str = ""
    
    @property
    def total_value(self) -> float:
        """Get the total transaction value."""
        return self.quantity * self.price_per_unit
    
    @property
    def net_value(self) -> float:
        """Get the net transaction value including fees."""
        if self.transaction_type in [TransactionType.BUY, TransactionType.FEE, TransactionType.WITHDRAWAL]:
            return self.total_value + self.fees
        else:
            return self.total_value - self.fees


@dataclass
class Portfolio:
    """Represents an investment portfolio."""
    id: str
    name: str
    cash_balance: float = 0.0
    currency: str = "USD"
    positions: List[Position] = field(default_factory=list)
    transactions: List[Transaction] = field(default_factory=list)
    
    def get_total_value(self) -> float:
        """Get the total portfolio value including cash."""
        position_value = sum(pos.current_value for pos in self.positions)
        return position_value + self.cash_balance
    
    def get_total_cost_basis(self) -> float:
        """Get the total cost basis of all positions."""
        return sum(pos.quantity * pos.average_cost for pos in self.positions)
    
    def get_total_unrealized_pnl(self) -> float:
        """Get total unrealized profit/loss."""
        return sum(pos.unrealized_pnl for pos in self.positions)
    
    def get_total_unrealized_pnl_percent(self) -> float:
        """Get total unrealized P&L as percentage."""
        cost_basis = self.get_total_cost_basis()
        if cost_basis == 0:
            return 0
        return (self.get_total_unrealized_pnl() / cost_basis) * 100
    
    def get_allocation(self) -> Dict[str, float]:
        """Get asset allocation as percentages."""
        total_value = self.get_total_value()
        allocation = {}
        for pos in self.positions:
            weight = pos.get_weight(total_value)
            asset_class = pos.security.asset_class.value
            allocation[asset_class] = allocation.get(asset_class, 0) + weight
        return allocation
    
    def add_transaction(self, transaction: Transaction) -> None:
        """Add a transaction to the portfolio."""
        self.transactions.append(transaction)


@dataclass
class CashFlow:
    """Represents a cash flow for TVM calculations."""
    amount: float
    timing: int  # Period number
    is_inflow: bool = True
    
    def present_value(self, rate: float) -> float:
        """Calculate present value of this cash flow."""
        if rate == 0:
            return self.amount if self.is_inflow else -self.amount
        discount_factor = (1 + rate) ** (-self.timing)
        if self.is_inflow:
            return self.amount * discount_factor
        return -self.amount * discount_factor


@dataclass
class AmortizationSchedule:
    """Represents a loan amortization schedule entry."""
    period: int
    payment: float
    interest_payment: float
    principal_payment: float
    remaining_balance: float


class FinancialCalculator:
    """Core financial calculation functions."""
    
    @staticmethod
    def calculate_npv(rate: float, cash_flows: List[float]) -> float:
        """
        Calculate Net Present Value.
        
        Args:
            rate: Discount rate (as decimal)
            cash_flows: List of cash flows (negative for outflows)
            
        Returns:
            Net Present Value
        """
        npv = 0.0
        for i, cf in enumerate(cash_flows):
            npv += cf / (1 + rate) ** i
        return npv
    
    @staticmethod
    def calculate_irr(cash_flows: List[float], guess: float = 0.1) -> float:
        """
        Calculate Internal Rate of Return using Newton-Raphson method.
        
        Args:
            cash_flows: List of cash flows
            guess: Initial guess for IRR
            
        Returns:
            Internal Rate of Return as decimal
        """
        def npv_func(rate):
            return FinancialCalculator.calculate_npv(rate, cash_flows)
        
        def npv_derivative(rate):
            if rate == -1:
                return float('inf')
            return sum(-i * cf * (1 + rate) ** (-i - 1) for i, cf in enumerate(cash_flows))
        
        max_iterations = 100
        tolerance = 1e-7
        rate = guess
        
        for _ in range(max_iterations):
            npv = npv_func(rate)
            derivative = npv_derivative(rate)
            
            if abs(derivative) < tolerance:
                break
            
            new_rate = rate - npv / derivative
            
            if abs(new_rate - rate) < tolerance:
                return new_rate
            
            rate = new_rate
        
        return rate
    
    @staticmethod
    def calculate_pmt(principal: float, rate: float, periods: int) -> float:
        """
        Calculate periodic payment for a loan.
        
        Args:
            principal: Loan principal
            rate: Periodic interest rate
            periods: Number of payments
            
        Returns:
            Periodic payment amount
        """
        if rate == 0:
            return principal / periods
        
        return principal * (rate * (1 + rate) ** periods) / ((1 + rate) ** periods - 1)
    
    @staticmethod
    def calculate_fv(rate: float, periods: int, pmt: float, pv: float = 0) -> float:
        """
        Calculate Future Value.
        
        Args:
            rate: Periodic interest rate
            periods: Number of periods
            pmt: Periodic payment
            pv: Present value
            
        Returns:
            Future Value
        """
        if rate == 0:
            return -pv - pmt * periods
        
        fv = pv * (1 + rate) ** periods
        fv += pmt * ((1 + rate) ** periods - 1) / rate
        return -fv
    
    @staticmethod
    def calculate_pv(rate: float, periods: int, pmt: float, fv: float = 0) -> float:
        """
        Calculate Present Value.
        
        Args:
            rate: Periodic interest rate
            periods: Number of periods
            pmt: Periodic payment
            fv: Future value
            
        Returns:
            Present Value
        """
        if rate == 0:
            return -fv - pmt * periods
        
        pv = fv / (1 + rate) ** periods
        pv -= pmt * ((1 + rate) ** periods - 1) / (rate * (1 + rate) ** periods)
        return -pv
    
    @staticmethod
    def calculate_amortization(
        principal: float,
        annual_rate: float,
        term_years: int,
        payments_per_year: int = 12
    ) -> List[AmortizationSchedule]:
        """
        Generate an amortization schedule.
        
        Args:
            principal: Loan principal
            annual_rate: Annual interest rate
            term_years: Loan term in years
            payments_per_year: Number of payments per year
            
        Returns:
            List of AmortizationSchedule entries
        """
        periods = term_years * payments_per_year
        periodic_rate = annual_rate / payments_per_year
        payment = FinancialCalculator.calculate_pmt(principal, periodic_rate, periods)
        
        schedule = []
        balance = principal
        
        for i in range(1, periods + 1):
            interest = balance * periodic_rate
            principal_payment = payment - interest
            balance -= principal_payment
            
            schedule.append(AmortizationSchedule(
                period=i,
                payment=payment,
                interest_payment=interest,
                principal_payment=principal_payment,
                remaining_balance=max(0, balance)
            ))
        
        return schedule
    
    @staticmethod
    def compound_interest(
        principal: float,
        annual_rate: float,
        years: int,
        compounds_per_year: int = 12
    ) -> float:
        """
        Calculate compound interest.
        
        Args:
            principal: Initial amount
            annual_rate: Annual interest rate
            years: Number of years
            compounds_per_year: Compounding frequency
            
        Returns:
            Final amount after compounding
        """
        if annual_rate == 0:
            return principal
        
        rate_per_period = annual_rate / compounds_per_year
        total_periods = years * compounds_per_year
        
        return principal * (1 + rate_per_period) ** total_periods


class RiskAnalyzer:
    """Risk analysis and portfolio metrics."""
    
    @staticmethod
    def calculate_returns(prices: List[float]) -> List[float]:
        """Calculate period-over-period returns."""
        if len(prices) < 2:
            return []
        
        returns = []
        for i in range(1, len(prices)):
            if prices[i-1] != 0:
                ret = (prices[i] - prices[i-1]) / prices[i-1]
                returns.append(ret)
        return returns
    
    @staticmethod
    def calculate_volatility(returns: List[float], annualize: bool = True) -> float:
        """Calculate return volatility (standard deviation)."""
        if len(returns) < 2:
            return 0.0
        
        mean_return = sum(returns) / len(returns)
        variance = sum((r - mean_return) ** 2 for r in returns) / (len(returns) - 1)
        volatility = math.sqrt(variance)
        
        if annualize:
            # Assuming daily returns, annualize by sqrt(252)
            volatility *= math.sqrt(252)
        
        return volatility
    
    @staticmethod
    def calculate_sharpe_ratio(
        returns: List[float],
        risk_free_rate: float = 0.02,
        annualize: bool = True
    ) -> float:
        """
        Calculate Sharpe Ratio.
        
        Args:
            returns: List of returns
            risk_free_rate: Annual risk-free rate
            annualize: Whether to annualize the ratio
            
        Returns:
            Sharpe Ratio
        """
        if len(returns) < 2:
            return 0.0
        
        mean_return = sum(returns) / len(returns)
        volatility = RiskAnalyzer.calculate_volatility(returns, annualize)
        
        if annualize:
            # Convert daily excess return to annual
            daily_rf = risk_free_rate / 252
            excess_return = mean_return - daily_rf
            return (excess_return * 252) / volatility if volatility != 0 else 0
        else:
            return (mean_return - risk_free_rate) / volatility if volatility != 0 else 0
    
    @staticmethod
    def calculate_beta(asset_returns: List[float], market_returns: List[float]) -> float:
        """Calculate beta relative to a benchmark."""
        if len(asset_returns) != len(market_returns) or len(asset_returns) < 2:
            return 1.0
        
        mean_asset = sum(asset_returns) / len(asset_returns)
        mean_market = sum(market_returns) / len(market_returns)
        
        covariance = sum(
            (ar - mean_asset) * (mr - mean_market)
            for ar, mr in zip(asset_returns, market_returns)
        ) / (len(asset_returns) - 1)
        
        market_variance = sum((mr - mean_market) ** 2 for mr in market_returns) / (len(market_returns) - 1)
        
        if market_variance == 0:
            return 1.0
        
        return covariance / market_variance
    
    @staticmethod
    def calculate_var(
        returns: List[float],
        confidence_level: float = 0.95,
        method: str = "historical"
    ) -> float:
        """
        Calculate Value at Risk.
        
        Args:
            returns: List of returns
            confidence_level: Confidence level (e.g., 0.95)
            method: Calculation method ('historical' or 'parametric')
            
        Returns:
            VaR as a percentage
        """
        if len(returns) < 2:
            return 0.0
        
        if method == "historical":
            sorted_returns = sorted(returns)
            index = int((1 - confidence_level) * len(sorted_returns))
            return -sorted_returns[index]
        else:  # parametric
            volatility = RiskAnalyzer.calculate_volatility(returns)
            from scipy import stats
            z_score = stats.norm.ppf(1 - confidence_level)
            return -volatility * z_score / math.sqrt(252)  # Daily VaR
    
    @staticmethod
    def calculate_correlation(asset1_returns: List[float], asset2_returns: List[float]) -> float:
        """Calculate correlation between two assets."""
        if len(asset1_returns) != len(asset2_returns) or len(asset1_returns) < 2:
            return 0.0
        
        mean1 = sum(asset1_returns) / len(asset1_returns)
        mean2 = sum(asset2_returns) / len(asset2_returns)
        
        numerator = sum(
            (r1 - mean1) * (r2 - mean2)
            for r1, r2 in zip(asset1_returns, asset2_returns)
        )
        
        denom1 = math.sqrt(sum((r - mean1) ** 2 for r in asset1_returns))
        denom2 = math.sqrt(sum((r - mean2) ** 2 for r in asset2_returns))
        
        if denom1 * denom2 == 0:
            return 0.0
        
        return numerator / (denom1 * denom2)
    
    @staticmethod
    def calculate_max_drawdown(values: List[float]) -> float:
        """Calculate maximum drawdown from a series of values."""
        if len(values) < 2:
            return 0.0
        
        max_drawdown = 0.0
        peak = values[0]
        
        for value in values[1:]:
            if value > peak:
                peak = value
            drawdown = (peak - value) / peak
            if drawdown > max_drawdown:
                max_drawdown = drawdown
        
        return max_drawdown * 100  # As percentage


class TechnicalIndicator:
    """Technical analysis indicators calculator."""
    
    @staticmethod
    def calculate_sma(prices: List[float], period: int) -> List[float]:
        """Calculate Simple Moving Average."""
        if len(prices) < period:
            return []
        
        sma = []
        for i in range(period - 1, len(prices)):
            avg = sum(prices[i - period + 1:i + 1]) / period
            sma.append(avg)
        return sma
    
    @staticmethod
    def calculate_ema(prices: List[float], period: int) -> List[float]:
        """Calculate Exponential Moving Area."""
        if len(prices) < period:
            return []
        
        multiplier = 2 / (period + 1)
        ema = []
        
        # Start with SMA
        sma = sum(prices[:period]) / period
        ema.append(sma)
        
        # Calculate EMA for remaining prices
        for i in range(period, len(prices)):
            value = prices[i] * multiplier + ema[-1] * (1 - multiplier)
            ema.append(value)
        
        return ema
    
    @staticmethod
    def calculate_rsi(prices: List[float], period: int = 14) -> List[float]:
        """Calculate Relative Strength Index."""
        if len(prices) < period + 1:
            return []
        
        returns = RiskAnalyzer.calculate_returns(prices)
        rsi = []
        
        gains = [r for r in returns if r > 0]
        losses = [-r for r in returns if r < 0]
        
        avg_gain = sum(gains) / period if gains else 0
        avg_loss = sum(losses) / period if losses else 0
        
        for i in range(period, len(returns)):
            r = returns[i]
            if r > 0:
                avg_gain = (avg_gain * (period - 1) + r) / period
            else:
                avg_loss = (avg_loss * (period - 1) + (-r)) / period
            
            if avg_loss == 0:
                rsi.append(100)
            else:
                rs = avg_gain / avg_loss
                rsi.append(100 - (100 / (1 + rs)))
        
        return rsi
    
    @staticmethod
    def calculate_macd(
        prices: List[float],
        fast_period: int = 12,
        slow_period: int = 26,
        signal_period: int = 9
    ) -> Dict[str, List[float]]:
        """Calculate MACD (Moving Average Convergence Divergence)."""
        ema_fast = TechnicalIndicator.calculate_ema(prices, fast_period)
        ema_slow = TechnicalIndicator.calculate_ema(prices, slow_period)
        
        # MACD line
        macd = []
        start_idx = len(ema_slow) - len(ema_fast)
        for i in range(len(ema_fast)):
            if start_idx + i >= 0:
                macd.append(ema_fast[i] - ema_slow[start_idx + i])
        
        # Signal line
        signal = TechnicalIndicator.calculate_ema(macd, signal_period)
        
        # Histogram
        histogram = []
        hist_start = len(macd) - len(signal)
        for i in range(len(signal)):
            if hist_start + i >= 0:
                histogram.append(macd[hist_start + i] - signal[i])
        
        return {
            "macd": macd,
            "signal": signal,
            "histogram": histogram
        }
    
    @staticmethod
    def calculate_bollinger_bands(
        prices: List[float],
        period: int = 20,
        std_dev: float = 2.0
    ) -> Dict[str, List[float]]:
        """Calculate Bollinger Bands."""
        if len(prices) < period:
            return {"upper": [], "middle": [], "lower": []}
        
        middle = TechnicalIndicator.calculate_sma(prices, period)
        upper = []
        lower = []
        
        for i in range(len(middle)):
            start = i - period + 1
            end = i + 1
            subset = prices[start:end]
            std = math.sqrt(sum((p - middle[i]) ** 2 for p in subset) / period)
            upper.append(middle[i] + std_dev * std)
            lower.append(middle[i] - std_dev * std)
        
        return {
            "upper": upper,
            "middle": middle,
            "lower": lower
        }


@dataclass
class ScenarioInputs:
    """Inputs for scenario planning."""
    initial_investment: float
    monthly_contribution: float
    annual_return_rate: float
    inflation_rate: float = 0.02
    investment_horizon_years: int = 10
    tax_rate: float = 0.0


@dataclass
class ScenarioResult:
    """Results from scenario planning."""
    scenario_name: str
    final_value: float
    total_contributions: float
    total_earnings: float
    inflation_adjusted_value: float
    yearly_projections: List[Dict[str, float]]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "scenario_name": self.scenario_name,
            "final_value": self.final_value,
            "total_contributions": self.total_contributions,
            "total_earnings": self.total_earnings,
            "inflation_adjusted_value": self.inflation_adjusted_value,
            "yearly_projections": self.yearly_projections
        }


class ScenarioPlanner:
    """Scenario planning and forecasting."""
    
    @staticmethod
    def project_growth(inputs: ScenarioInputs) -> ScenarioResult:
        """
        Project investment growth over time.
        
        Args:
            inputs: Scenario input parameters
            
        Returns:
            ScenarioResult with projections
        """
        yearly_projections = []
        balance = inputs.initial_investment
        total_contributions = inputs.initial_investment
        
        real_return = (1 + inputs.annual_return_rate) / (1 + inputs.inflation_rate) - 1
        
        for year in range(1, inputs.investment_horizon_years + 1):
            # Add annual contributions
            annual_contribution = inputs.monthly_contribution * 12
            total_contributions += annual_contribution
            
            # Calculate returns (monthly compounding)
            for month in range(12):
                balance += inputs.monthly_contribution
                balance *= (1 + inputs.annual_return_rate / 12)
            
            # Inflation-adjusted value
            inflation_adjusted = balance / ((1 + inputs.inflation_rate) ** year)
            
            yearly_projections.append({
                "year": year,
                "balance": balance,
                "contributions": total_contributions,
                "earnings": balance - total_contributions,
                "inflation_adjusted": inflation_adjusted,
                "return_percent": ((balance - total_contributions) / total_contributions * 100) if total_contributions > 0 else 0
            })
        
        return ScenarioResult(
            scenario_name="Base Case",
            final_value=balance,
            total_contributions=total_contributions,
            total_earnings=balance - total_contributions,
            inflation_adjusted_value=yearly_projections[-1]["inflation_adjusted"] if yearly_projections else 0,
            yearly_projections=yearly_projections
        )
    
    @staticmethod
    def run_monte_carlo(
        initial_investment: float,
        annual_return: float,
        volatility: float,
        years: int,
        iterations: int = 1000
    ) -> List[Dict[str, Any]]:
        """
        Run Monte Carlo simulation for portfolio projection.
        
        Args:
            initial_investment: Starting investment amount
            annual_return: Expected annual return
            volatility: Annual volatility (standard deviation)
            years: Investment horizon
            iterations: Number of simulations
            
        Returns:
            List of simulation paths
        """
        import random
        
        simulations = []
        daily_return = annual_return / 252
        daily_vol = volatility / math.sqrt(252)
        
        for _ in range(iterations):
            path = [{"year": 0, "value": initial_investment}]
            value = initial_investment
            
            for day in range(years * 252):
                random_return = random.gauss(daily_return, daily_vol)
                value *= (1 + random_return)
                
                if day % 252 == 0 and day > 0:
                    path.append({
                        "year": day // 252,
                        "value": value
                    })
            
            simulations.append(path)
        
        return simulations


@dataclass
class ChartConfig:
    """Configuration for financial charts."""
    chart_type: ChartType = ChartType.LINE
    title: str = ""
    x_axis_label: str = ""
    y_axis_label: str = ""
    colors: List[str] = None
    show_grid: bool = True
    show_legend: bool = True
    width: int = 800
    height: int = 400
    
    def __post_init__(self):
        if self.colors is None:
            self.colors = ["#10B981", "#EF4444", "#3B82F6", "#F59E0B", "#8B5CF6"]


@dataclass
class PortfolioVisualConfig:
    """Configuration for portfolio visualization."""
    show_positions: bool = True
    show_pie_chart: bool = True
    show_performance: bool = True
    show_risk_metrics: bool = True
    color_scheme: str = "default"


__all__ = [
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
    "PortfolioVisualConfig"
]
