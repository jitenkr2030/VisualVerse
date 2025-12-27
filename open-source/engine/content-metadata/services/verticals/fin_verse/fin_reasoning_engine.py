"""
FinVerse Reasoning Engine

This module provides the reasoning and calculation capabilities for the
VisualVerse financial learning platform. It handles financial analysis,
investment calculations, and scenario planning.

Author: MiniMax Agent
Version: 1.0.0
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple, Callable
from enum import Enum
from .fin_core import (
    Portfolio, Position, Security, OHLCV, FinancialCalculator,
    RiskAnalyzer, TechnicalIndicator, ScenarioInputs, ScenarioResult,
    ScenarioPlanner, Transaction, CashFlow, AssetClass
)


class ProblemDifficulty(Enum):
    """Difficulty levels for finance problems."""
    EASY = 1
    MEDIUM = 2
    HARD = 3
    EXPERT = 4


class SolutionStatus(Enum):
    """Status of a solution attempt."""
    CORRECT = "correct"
    INCORRECT = "incorrect"
    PARTIAL = "partial"
    INCOMPLETE = "incomplete"
    ERROR = "error"


@dataclass
class SolutionStep:
    """A single step in a solution process."""
    step_number: int
    description: str
    formula: str
    calculation: str
    result: Any
    is_critical: bool = True
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "step_number": self.step_number,
            "description": self.description,
            "formula": self.formula,
            "calculation": self.calculation,
            "result": self.result,
            "is_critical": self.is_critical
        }


@dataclass
class ConceptualAnalysis:
    """Analysis of conceptual understanding."""
    concepts_identified: List[str] = field(default_factory=list)
    concepts_mastered: List[str] = field(default_factory=list)
    misconceptions: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "concepts_identified": self.concepts_identified,
            "concepts_mastered": self.concepts_mastered,
            "misconceptions": self.misconceptions,
            "recommendations": self.recommendations
        }


@dataclass
class FinancialSolution:
    """Complete solution to a financial problem."""
    status: SolutionStatus
    answer: Any
    steps: List[SolutionStep] = field(default_factory=list)
    explanation: str = ""
    conceptual_analysis: ConceptualAnalysis = None
    tips: List[str] = field(default_factory=list)
    common_mistakes: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "status": self.status.value,
            "answer": self.answer,
            "steps": [step.to_dict() for step in self.steps],
            "explanation": self.explanation,
            "conceptual_analysis": self.conceptual_analysis.to_dict() if self.conceptual_analysis else None,
            "tips": self.tips,
            "common_mistakes": self.common_mistakes
        }


class TimeValueSolver:
    """Solves time value of money problems."""
    
    @staticmethod
    def solve_npv(
        cash_flows: List[float],
        discount_rate: float
    ) -> FinancialSolution:
        """Calculate Net Present Value."""
        steps = []
        
        npv = FinancialCalculator.calculate_npv(discount_rate, cash_flows)
        
        steps.append(SolutionStep(
            step_number=1,
            description="Calculate present value of each cash flow",
            formula="PV = CF / (1+r)^t",
            calculation="Calculating PV for each period",
            result=f"NPV = {npv:.2f}",
            is_critical=True
        ))
        
        return FinancialSolution(
            status=SolutionStatus.CORRECT if npv != 0 else SolutionStatus.INCOMPLETE,
            answer=npv,
            steps=steps,
            explanation=f"The NPV is ${npv:,.2f}. {'Positive NPV indicates a profitable investment.' if npv > 0 else 'Negative NPV indicates the investment should be rejected.'}",
            tips=["Use a discount rate that reflects the investment's risk", "Higher discount rates result in lower NPV"]
        )
    
    @staticmethod
    def solve_irr(cash_flows: List[float]) -> FinancialSolution:
        """Calculate Internal Rate of Return."""
        steps = []
        
        irr = FinancialCalculator.calculate_irr(cash_flows) * 100
        
        steps.append(SolutionStep(
            step_number=1,
            description="Find the discount rate where NPV equals zero",
            formula="0 = Σ CF / (1+IRR)^t",
            calculation="Using iterative method to find IRR",
            result=f"IRR = {irr:.2f}%",
            is_critical=True
        ))
        
        return FinancialSolution(
            status=SolutionStatus.CORRECT,
            answer=f"{irr:.2f}%",
            steps=steps,
            explanation=f"The IRR is {irr:.2f}%. Compare this to your required return to make investment decisions.",
            tips=["IRR assumes cash flows are reinvested at the IRR itself", "Use NPV for mutually exclusive projects"]
        )
    
    @staticmethod
    def solve_loan_payment(
        principal: float,
        annual_rate: float,
        years: int
    ) -> FinancialSolution:
        """Calculate loan payment."""
        steps = []
        
        rate = annual_rate / 12
        periods = years * 12
        payment = FinancialCalculator.calculate_pmt(principal, rate, periods)
        
        steps.append(SolutionStep(
            step_number=1,
            description="Convert annual rate to monthly rate",
            formula="r_monthly = r_annual / 12",
            calculation=f"{annual_rate:.4f} / 12 = {rate:.6f}",
            result=f"Monthly rate = {rate:.6f}",
            is_critical=True
        ))
        
        steps.append(SolutionStep(
            step_number=2,
            description="Calculate monthly payment",
            formula="PMT = P × r × (1+r)^n / ((1+r)^n - 1)",
            calculation=f"{principal} × {rate:.6f} × (1+{rate:.6f})^{periods} / ((1+{rate:.6f})^{periods} - 1)",
            result=f"Monthly payment = ${payment:.2f}",
            is_critical=True
        ))
        
        total_payment = payment * periods
        total_interest = total_payment - principal
        
        steps.append(SolutionStep(
            step_number=3,
            description="Calculate total interest paid",
            formula="Total Interest = Total Payments - Principal",
            calculation=f"(${payment:.2f} × {periods}) - ${principal} = ${total_interest:.2f}",
            result=f"Total interest = ${total_interest:.2f}",
            is_critical=False
        ))
        
        return FinancialSolution(
            status=SolutionStatus.CORRECT,
            answer=f"${payment:.2f}/month",
            steps=steps,
            explanation=f"Monthly payment is ${payment:.2f}. Total interest over the loan is ${total_interest:,.2f}.",
            tips=["Making extra payments reduces principal faster", "Shorter loan terms save on interest"]
        )
    
    @staticmethod
    def solve_future_value(
        present_value: float,
        annual_rate: float,
        years: int,
        compounds_per_year: int = 12
    ) -> FinancialSolution:
        """Calculate future value."""
        steps = []
        
        fv = FinancialCalculator.compound_interest(
            present_value, annual_rate, years, compounds_per_year
        )
        
        steps.append(SolutionStep(
            step_number=1,
            description="Calculate compound growth",
            formula="FV = PV × (1 + r/n)^(n×t)",
            calculation=f"FV = ${present_value} × (1 + {annual_rate}/{compounds_per_year})^{compounds_per_year × {years}}",
            result=f"Future Value = ${fv:,.2f}",
            is_critical=True
        ))
        
        return FinancialSolution(
            status=SolutionStatus.CORRECT,
            answer=f"${fv:,.2f}",
            steps=steps,
            explanation=f"${present_value} invested at {annual_rate*100}% for {years} years will grow to ${fv:,.2f}.",
            tips=["Start investing early to maximize compound growth", "Higher returns lead to exponential growth over time"]
        )


class RiskAnalysisSolver:
    """Solves portfolio risk and return problems."""
    
    @staticmethod
    def calculate_portfolio_risk_metrics(
        returns: List[float],
        risk_free_rate: float = 0.02,
        portfolio_value: float = 100000
    ) -> FinancialSolution:
        """Calculate comprehensive risk metrics."""
        steps = []
        
        volatility = RiskAnalyzer.calculate_volatility(returns) * 100
        sharpe = RiskAnalyzer.calculate_sharpe_ratio(returns, risk_free_rate)
        max_dd = RiskAnalyzer.calculate_max_drawdown(
            [100 * (1 + r) for r in [0] + returns]
        )
        var_95 = RiskAnalyzer.calculate_var(returns, 0.95) * portfolio_value
        
        steps.append(SolutionStep(
            step_number=1,
            description="Calculate portfolio volatility (standard deviation)",
            formula="σ = √(Σ(R - μ)² / (n-1)) × √252",
            calculation="Annualized volatility calculation",
            result=f"Volatility = {volatility:.2f}%",
            is_critical=True
        ))
        
        steps.append(SolutionStep(
            step_number=2,
            description="Calculate Sharpe Ratio",
            formula="Sharpe = (Rp - Rf) / σp",
            calculation=f"({sum(returns)/len(returns)*252:.2%} - {risk_free_rate:.2%}) / {volatility/100:.2%}",
            result=f"Sharpe Ratio = {sharpe:.2f}",
            is_critical=True
        ))
        
        steps.append(SolutionStep(
            step_number=3,
            description="Calculate Maximum Drawdown",
            formula="MDD = (Peak - Trough) / Peak",
            calculation="Peak-to-trough decline",
            result=f"Max Drawdown = {max_dd:.2f}%",
            is_critical=False
        ))
        
        return FinancialSolution(
            status=SolutionStatus.CORRECT,
            answer={
                "volatility": f"{volatility:.2f}%",
                "sharpe_ratio": f"{sharpe:.2f}",
                "max_drawdown": f"{max_dd:.2f}%",
                "var_95": f"${var_95:,.2f}"
            },
            steps=steps,
            explanation=f"Portfolio has {'good' if sharpe > 1 else 'acceptable' if sharpe > 0.5 else 'poor'} risk-adjusted returns.",
            tips=["Diversification can reduce portfolio volatility", "Higher Sharpe ratio indicates better risk-adjusted performance"]
        )
    
    @staticmethod
    def solve_diversification(
        asset_returns: Dict[str, List[float]]
    ) -> FinancialSolution:
        """Analyze diversification benefits."""
        steps = []
        
        results = {}
        for name, returns in asset_returns.items():
            volatility = RiskAnalyzer.calculate_volatility(returns) * 100
            results[name] = {"volatility": volatility}
        
        # Calculate portfolio if equal-weighted
        all_returns = list(asset_returns.values())
        if all_returns:
            combined = []
            min_len = min(len(r) for r in all_returns)
            for i in range(min_len):
                avg = sum(r[i] for r in all_returns) / len(all_returns)
                combined.append(avg)
            
            portfolio_vol = RiskAnalyzer.calculate_volatility(combined) * 100
            avg_individual = sum(r["volatility"] for r in results.values()) / len(results)
            
            diversification_benefit = avg_individual - portfolio_vol
            
            steps.append(SolutionStep(
                step_number=1,
                description="Calculate individual asset volatilities",
                formula="Individual asset standard deviations",
                calculation=f"Average individual volatility: {avg_individual:.2f}%",
                result=f"Individual volatilities: {results}",
                is_critical=True
            ))
            
            steps.append(SolutionStep(
                step_number=2,
                description="Calculate portfolio volatility",
                formula="σp = √(w'Σw)",
                calculation="Portfolio standard deviation",
                result=f"Portfolio volatility: {portfolio_vol:.2f}%",
                is_critical=True
            ))
            
            steps.append(SolutionStep(
                step_number=3,
                description="Calculate diversification benefit",
                formula="Benefit = Avg Individual - Portfolio",
                calculation=f"{avg_individual:.2f}% - {portfolio_vol:.2f}% = {diversification_benefit:.2f}%",
                result=f"Diversification benefit: {diversification_benefit:.2f}%",
                is_critical=False
            ))
        
        return FinancialSolution(
            status=SolutionStatus.CORRECT,
            answer={
                "individual_volatilities": results,
                "portfolio_volatility": f"{portfolio_vol:.2f}%",
                "diversification_benefit": f"{diversification_benefit:.2f}%"
            },
            steps=steps,
            explanation=f"Diversification reduces portfolio volatility by {diversification_benefit:.2f}%.",
            tips=["Add uncorrelated assets to maximize diversification", "Correlation is key - low correlation means more benefit"]
        )


class TechnicalAnalysisSolver:
    """Solves technical analysis problems."""
    
    @staticmethod
    def analyze_moving_averages(
        prices: List[float],
        short_period: int = 50,
        long_period: int = 200
    ) -> FinancialSolution:
        """Analyze moving average signals."""
        steps = []
        
        sma_short = TechnicalIndicator.calculate_sma(prices, short_period)
        sma_long = TechnicalIndicator.calculate_sma(prices, long_period)
        
        current_price = prices[-1]
        current_short_sma = sma_short[-1] if sma_short else 0
        current_long_sma = sma_long[-1] if sma_long else 0
        
        # Determine signal
        if current_price > current_short_sma > current_long_sma:
            signal = "BULLISH - Price above both MAs (Golden Cross setup)"
        elif current_price < current_short_sma < current_long_sma:
            signal = "BEARISH - Price below both MAs (Death Cross setup)"
        elif current_short_sma > current_long_sma:
            signal = "BULLISH - Short MA above long MA"
        else:
            signal = "BEARISH - Short MA below long MA"
        
        steps.append(SolutionStep(
            step_number=1,
            description="Calculate Short-term SMA",
            formula="SMA = (P1 + P2 + ... + Pn) / n",
            calculation=f"Average of last {short_period} prices",
            result=f"50-day SMA = {current_short_sma:.2f}" if short_period == 50 else f"SMA = {current_short_sma:.2f}",
            is_critical=True
        ))
        
        steps.append(SolutionStep(
            step_number=2,
            description="Calculate Long-term SMA",
            formula="SMA = (P1 + P2 + ... + Pn) / n",
            calculation=f"Average of last {long_period} prices",
            result=f"200-day SMA = {current_long_sma:.2f}" if long_period == 200 else f"SMA = {current_long_sma:.2f}",
            is_critical=True
        ))
        
        steps.append(SolutionStep(
            step_number=3,
            description="Generate trading signal",
            formula="Compare price and MAs",
            calculation=f"Current: {current_price:.2f}, Short: {current_short_sma:.2f}, Long: {current_long_sma:.2f}",
            result=signal,
            is_critical=True
        ))
        
        return FinancialSolution(
            status=SolutionStatus.CORRECT,
            answer=signal,
            steps=steps,
            explanation=f"Based on SMA analysis: {signal}",
            tips=["Use with other indicators for confirmation", "Golden cross (50-day crosses above 200-day) is bullish signal"]
        )
    
    @staticmethod
    def analyze_rsi(prices: List[float], period: int = 14) -> FinancialSolution:
        """Analyze RSI for overbought/oversold conditions."""
        steps = []
        
        rsi_values = TechnicalIndicator.calculate_rsi(prices, period)
        current_rsi = rsi_values[-1] if rsi_values else 50
        
        if current_rsi >= 70:
            condition = "OVERBOUGHT - Potential reversal or pullback"
        elif current_rsi <= 30:
            condition = "OVERSOLD - Potential bounce or recovery"
        else:
            condition = "NEUTRAL - No clear signal"
        
        steps.append(SolutionStep(
            step_number=1,
            description="Calculate price changes",
            formula="ΔP = Current Price - Previous Price",
            calculation="Calculate gains and losses",
            result="Gains and losses separated",
            is_critical=True
        ))
        
        steps.append(SolutionStep(
            step_number=2,
            description="Calculate average gain and loss",
            formula="Average = Sum of gains/losses / n",
            calculation=f"Using {period}-period lookback",
            result="RS values computed",
            is_critical=True
        ))
        
        steps.append(SolutionStep(
            step_number=3,
            description="Calculate RSI",
            formula="RSI = 100 - (100 / (1 + RS))",
            calculation=f"RS = Average Gain / Average Loss",
            result=f"RSI = {current_rsi:.2f}",
            is_critical=True
        ))
        
        return FinancialSolution(
            status=SolutionStatus.CORRECT,
            answer={
                "rsi": current_rsi,
                "condition": condition
            },
            steps=steps,
            explanation=f"RSI at {current_rsi:.2f} indicates {condition.lower()}",
            tips=["RSI above 70 may indicate overbought conditions", "RSI below 30 may indicate oversold conditions"]
        )


class ScenarioPlanningSolver:
    """Solves financial planning and scenario problems."""
    
    @staticmethod
    def plan_retirement(
        current_age: int,
        retirement_age: int,
        current_savings: float,
        monthly_contribution: float,
        expected_return: float = 0.07,
        desired_income: float = 50000,
        inflation_rate: float = 0.02
    ) -> FinancialSolution:
        """Calculate retirement readiness."""
        steps = []
        
        years_to_retirement = retirement_age - current_age
        years_in_retirement = 25  # Assume 25 years of retirement
        
        # Project savings at retirement
        inputs = ScenarioInputs(
            initial_investment=current_savings,
            monthly_contribution=monthly_contribution,
            annual_return_rate=expected_return,
            inflation_rate=inflation_rate,
            investment_horizon_years=years_to_retirement
        )
        
        result = ScenarioPlanner.project_growth(inputs)
        
        # Calculate sustainable withdrawal
        # Using 4% rule adjusted for inflation
        safe_withdrawal_rate = 0.04
        annual_income = result.final_value * safe_withdrawal_rate
        
        # Adjust desired income for inflation
        inflated_desire = desired_income * (1 + inflation_rate) ** years_to_retirement
        
        steps.append(SolutionStep(
            step_number=1,
            description="Project retirement savings",
            formula="FV = PV × (1+r)^n + PMT × [(1+r)^n - 1] / r",
            calculation=f"Savings at age {retirement_age}",
            result=f"Projected savings: ${result.final_value:,.2f}",
            is_critical=True
        ))
        
        steps.append(SolutionStep(
            step_number=2,
            description="Calculate sustainable annual income",
            formula="Income = Portfolio × Withdrawal Rate",
            calculation=f"${result.final_value:,.2f} × {safe_withdrawal_rate:.1%}",
            result=f"Annual income: ${annual_income:,.2f}",
            is_critical=True
        ))
        
        steps.append(SolutionStep(
            step_number=3,
            description="Compare to desired income (adjusted for inflation)",
            formula="Desired = Current × (1+inflation)^years",
            calculation=f"${desired_income:,} × (1+{inflation_rate:.1%})^{years_to_retirement} = ${inflated_desire:,.2f}",
            result=f"Desired (inflation-adjusted): ${inflated_desire:,.2f}",
            is_critical=True
        ))
        
        shortfall = inflated_desire - annual_income
        on_track = annual_income >= inflated_desire
        
        steps.append(SolutionStep(
            step_number=4,
            description="Determine if on track",
            formula="On Track = Projected Income >= Desired Income",
            calculation=f"${annual_income:,.2f} {'>=' if on_track else '<'} ${inflated_desire:,.2f}",
            result=f"{'ON TRACK' if on_track else 'SHORTFALL: $' + f'{shortfall:,.2f}/year'}",
            is_critical=True
        ))
        
        recommendations = []
        if not on_track:
            recommendations.append(f"Consider increasing monthly contribution by ${shortfall / 12 / expected_return:,.0f}")
            recommendations.append(f"Delay retirement by {int(shortfall / (annual_income * 0.1))} years")
        
        return FinancialSolution(
            status=SolutionStatus.CORRECT,
            answer={
                "projected_savings": result.final_value,
                "sustainable_income": annual_income,
                "desired_income": inflated_desire,
                "on_track": on_track,
                "shortfall": shortfall if not on_track else 0
            },
            steps=steps,
            explanation=f"Retirement analysis shows you are {'on track' if on_track else 'not on track'} for your retirement goals.",
            tips=["Start saving early for compound growth", "Review and adjust contributions annually"]
        )
    
    @staticmethod
    def compare_investment_options(
        options: List[Dict[str, Any]]
    ) -> FinancialSolution:
        """Compare different investment options."""
        steps = []
        
        comparison = []
        for option in options:
            result = ScenarioPlanner.project_growth(ScenarioInputs(
                initial_investment=option["initial"],
                monthly_contribution=option.get("monthly", 0),
                annual_return_rate=option["return_rate"] / 100,
                investment_horizon_years=option["years"]
            ))
            
            comparison.append({
                "name": option["name"],
                "final_value": result.final_value,
                "total_earnings": result.total_earnings,
                "roi_percent": (result.total_earnings / result.total_contributions) * 100
            })
        
        # Sort by final value
        comparison.sort(key=lambda x: x["final_value"], reverse=True)
        
        best = comparison[0] if comparison else None
        
        steps.append(SolutionStep(
            step_number=1,
            description="Project each option to maturity",
            formula="FV calculation for each scenario",
            calculation="Individual projections computed",
            result=f"Analyzed {len(options)} investment options",
            is_critical=True
        ))
        
        steps.append(SolutionStep(
            step_number=2,
            description="Compare final values and returns",
            formula="ROI = Earnings / Investment × 100%",
            calculation="Return on investment computed",
            result="Options ranked by performance",
            is_critical=True
        ))
        
        if best:
            steps.append(SolutionStep(
                step_number=3,
                description="Identify best option",
                formula="Highest final value wins",
                calculation=f"Best: {best['name']}",
                result=f"Recommended: {best['name']} with ${best['final_value']:,.2f}",
                is_critical=True
            ))
        
        return FinancialSolution(
            status=SolutionStatus.CORRECT,
            answer={
                "comparison": comparison,
                "recommended": best["name"] if best else None
            },
            steps=steps,
            explanation=f"After comparison, {best['name'] if best else 'N/A'} provides the best return."
        )


class FinVerseReasoningEngine:
    """
    Reasoning engine for financial problem solving.
    
    This engine provides comprehensive problem-solving capabilities for
    finance including time value of money, risk analysis, technical analysis,
    and financial planning.
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        """Initialize the reasoning engine."""
        self.config = config or {}
        self.tvm_solver = TimeValueSolver()
        self.risk_solver = RiskAnalysisSolver()
        self.tech_solver = TechnicalAnalysisSolver()
        self.scenario_solver = ScenarioPlanningSolver()
    
    def configure(self, config: Dict[str, Any]) -> None:
        """Configure the engine with custom settings."""
        self.config.update(config)
    
    def solve_tvm_problem(
        self,
        problem_type: str,
        **kwargs
    ) -> FinancialSolution:
        """Solve a time value of money problem."""
        if problem_type == "npv":
            return self.tvm_solver.solve_npv(
                kwargs["cash_flows"],
                kwargs["discount_rate"]
            )
        elif problem_type == "irr":
            return self.tvm_solver.solve_irr(kwargs["cash_flows"])
        elif problem_type == "loan_payment":
            return self.tvm_solver.solve_loan_payment(
                kwargs["principal"],
                kwargs["annual_rate"],
                kwargs["years"]
            )
        elif problem_type == "future_value":
            return self.tvm_solver.solve_future_value(
                kwargs["present_value"],
                kwargs["annual_rate"],
                kwargs["years"],
                kwargs.get("compounds_per_year", 12)
            )
        else:
            return FinancialSolution(
                status=SolutionStatus.ERROR,
                answer=None,
                explanation=f"Unknown TVM problem type: {problem_type}"
            )
    
    def solve_risk_problem(
        self,
        problem_type: str,
        **kwargs
    ) -> FinancialSolution:
        """Solve a risk analysis problem."""
        if problem_type == "portfolio_metrics":
            return self.risk_solver.calculate_portfolio_risk_metrics(
                kwargs["returns"],
                kwargs.get("risk_free_rate", 0.02),
                kwargs.get("portfolio_value", 100000)
            )
        elif problem_type == "diversification":
            return self.risk_solver.solve_diversification(kwargs["asset_returns"])
        else:
            return FinancialSolution(
                status=SolutionStatus.ERROR,
                answer=None,
                explanation=f"Unknown risk problem type: {problem_type}"
            )
    
    def solve_technical_problem(
        self,
        problem_type: str,
        **kwargs
    ) -> FinancialSolution:
        """Solve a technical analysis problem."""
        if problem_type == "moving_averages":
            return self.tech_solver.analyze_moving_averages(
                kwargs["prices"],
                kwargs.get("short_period", 50),
                kwargs.get("long_period", 200)
            )
        elif problem_type == "rsi":
            return self.tech_solver.analyze_rsi(
                kwargs["prices"],
                kwargs.get("period", 14)
            )
        else:
            return FinancialSolution(
                status=SolutionStatus.ERROR,
                answer=None,
                explanation=f"Unknown technical problem type: {problem_type}"
            )
    
    def solve_scenario_problem(
        self,
        problem_type: str,
        **kwargs
    ) -> FinancialSolution:
        """Solve a financial planning problem."""
        if problem_type == "retirement":
            return self.scenario_solver.plan_retirement(
                kwargs["current_age"],
                kwargs["retirement_age"],
                kwargs["current_savings"],
                kwargs["monthly_contribution"],
                kwargs.get("expected_return", 0.07),
                kwargs.get("desired_income", 50000),
                kwargs.get("inflation_rate", 0.02)
            )
        elif problem_type == "compare_options":
            return self.scenario_solver.compare_investment_options(kwargs["options"])
        else:
            return FinancialSolution(
                status=SolutionStatus.ERROR,
                answer=None,
                explanation=f"Unknown scenario problem type: {problem_type}"
            )
    
    def verify_answer(
        self,
        user_answer: Any,
        correct_answer: Any,
        tolerance: float = 0.01
    ) -> FinancialSolution:
        """Verify a user's answer."""
        if isinstance(user_answer, (int, float)) and isinstance(correct_answer, (int, float)):
            is_correct = abs(user_answer - correct_answer) / correct_answer < tolerance
            return FinancialSolution(
                status=SolutionStatus.CORRECT if is_correct else SolutionStatus.INCORRECT,
                answer=user_answer,
                explanation=f"{'Correct' if is_correct else 'Incorrect'}. The answer should be {correct_answer}"
            )
        
        if str(user_answer).lower() == str(correct_answer).lower():
            return FinancialSolution(
                status=SolutionStatus.CORRECT,
                answer=user_answer,
                explanation="Correct!"
            )
        else:
            return FinancialSolution(
                status=SolutionStatus.INCORRECT,
                answer=user_answer,
                explanation=f"Incorrect. The answer should be {correct_answer}"
            )


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
