"""
FinVerse Concept Service

This module provides the concept management and educational content services for
the VisualVerse financial learning platform. It handles curriculum mapping, lesson
content, formula definitions, and financial concept explanations.

Author: MiniMax Agent
Version: 1.0.0
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple
from enum import Enum
import json


class FinanceDomain(str, Enum):
    """Finance domains for curriculum organization."""
    GENERAL = "general"
    TIME_VALUE_OF_MONEY = "time_value_of_money"
    PORTFOLIO_MANAGEMENT = "portfolio_management"
    RISK_MANAGEMENT = "risk_management"
    TECHNICAL_ANALYSIS = "technical_analysis"
    FUNDAMENTAL_ANALYSIS = "fundamental_analysis"
    FIXED_INCOME = "fixed_income"
    DERIVATIVES = "derivatives"
    FINANCIAL_PLANNING = "financial_planning"
    INVESTMENT_STRATEGIES = "investment_strategies"


class DifficultyLevel(str, Enum):
    """Difficulty levels for finance concepts."""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


@dataclass
class FormulaDefinition:
    """Represents a financial formula with metadata."""
    id: str
    name: str
    latex_formula: str
    description: str
    variables: Dict[str, Dict[str, str]] = field(default_factory=dict)  # variable -> {name, unit}
    example: str = ""
    applications: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "latex_formula": self.latex_formula,
            "description": self.description,
            "variables": self.variables,
            "example": self.example,
            "applications": self.applications
        }


@dataclass
class FinanceConcept:
    """Represents a financial concept with educational content."""
    id: str
    name: str
    domain: FinanceDomain
    difficulty: DifficultyLevel
    definition: str
    explanation: str
    key_points: List[str] = field(default_factory=list)
    formulas: List[str] = field(default_factory=list)  # Formula IDs
    examples: List[str] = field(default_factory=list)
    related_concepts: List[str] = field(default_factory=list)
    visual_aids: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "domain": self.domain.value,
            "difficulty": self.difficulty.value,
            "definition": self.definition,
            "explanation": self.explanation,
            "key_points": self.key_points,
            "formulas": self.formulas,
            "examples": self.examples,
            "related_concepts": self.related_concepts,
            "visual_aids": self.visual_aids
        }


@dataclass
class LessonContent:
    """Represents a finance lesson with structured content."""
    id: str
    title: str
    domain: FinanceDomain
    difficulty: DifficultyLevel
    objectives: List[str] = field(default_factory=list)
    prerequisites: List[str] = field(default_factory=list)
    sections: List[Dict[str, Any]] = field(default_factory=list)
    practice_problems: List[Dict[str, Any]] = field(default_factory=list)
    summary_points: List[str] = field(default_factory=list)
    estimated_minutes: int = 30
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "title": self.title,
            "domain": self.domain.value,
            "difficulty": self.difficulty.value,
            "objectives": self.objectives,
            "prerequisites": self.prerequisites,
            "sections": self.sections,
            "practice_problems": self.practice_problems,
            "summary_points": self.summary_points,
            "estimated_minutes": self.estimated_minutes
        }


@dataclass
class MarketTerm:
    """Represents a financial market term or jargon."""
    term: str
    definition: str
    example_usage: str = ""
    related_terms: List[str] = field(default_factory=list)
    category: str = "general"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "term": self.term,
            "definition": self.definition,
            "example_usage": self.example_usage,
            "related_terms": self.related_terms,
            "category": self.category
        }


class FormulaRepository:
    """Repository for financial formulas."""
    
    _formulas: Dict[str, FormulaDefinition] = {}
    
    @classmethod
    def register_formula(cls, formula: FormulaDefinition) -> None:
        """Register a new formula."""
        cls._formulas[formula.id] = formula
    
    @classmethod
    def get_formula(cls, formula_id: str) -> Optional[FormulaDefinition]:
        """Get a formula by ID."""
        return cls._formulas.get(formula_id)
    
    @classmethod
    def get_all_formulas(cls) -> List[FormulaDefinition]:
        """Get all formulas."""
        return list(cls._formulas.values())
    
    @classmethod
    def search_formulas(cls, query: str) -> List[FormulaDefinition]:
        """Search formulas by name."""
        query_lower = query.lower()
        return [f for f in cls._formulas.values() if query_lower in f.name.lower()]


class ConceptRepository:
    """Repository for financial concepts and educational content."""
    
    _concepts: Dict[str, FinanceConcept] = {}
    _lessons: Dict[str, LessonContent] = {}
    _terms: Dict[str, MarketTerm] = {}
    
    @classmethod
    def register_concept(cls, concept: FinanceConcept) -> None:
        """Register a new finance concept."""
        cls._concepts[concept.id] = concept
    
    @classmethod
    def get_concept(cls, concept_id: str) -> Optional[FinanceConcept]:
        """Get a concept by ID."""
        return cls._concepts.get(concept_id)
    
    @classmethod
    def get_concepts_by_domain(cls, domain: FinanceDomain) -> List[FinanceConcept]:
        """Get all concepts in a domain."""
        return [c for c in cls._concepts.values() if c.domain == domain]
    
    @classmethod
    def register_lesson(cls, lesson: LessonContent) -> None:
        """Register a new lesson."""
        cls._lessons[lesson.id] = lesson
    
    @classmethod
    def get_lesson(cls, lesson_id: str) -> Optional[LessonContent]:
        """Get a lesson by ID."""
        return cls._lessons.get(lesson_id)
    
    @classmethod
    def get_lessons_by_domain(cls, domain: FinanceDomain) -> List[LessonContent]:
        """Get all lessons in a domain."""
        return [l for l in cls._lessons.values() if l.domain == domain]
    
    @classmethod
    def register_term(cls, term: MarketTerm) -> None:
        """Register a market term."""
        cls._terms[term.term.lower()] = term
    
    @classmethod
    def get_term(cls, term: str) -> Optional[MarketTerm]:
        """Get a market term."""
        return cls._terms.get(term.lower())
    
    @classmethod
    def search_terms(cls, query: str) -> List[MarketTerm]:
        """Search market terms."""
        query_lower = query.lower()
        return [t for t in cls._terms.values() if query_lower in t.term.lower()]


class FinVerseConceptService:
    """
    Service for managing financial educational content and curriculum.
    
    This service provides access to concepts, lessons, formulas, and
    market terminology for the financial learning platform.
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        """Initialize the concept service with optional configuration."""
        self.config = config or {}
        self._initialize_default_content()
    
    def _initialize_default_content(self) -> None:
        """Initialize with default finance content."""
        # Register formulas
        FormulaRepository.register_formula(FormulaDefinition(
            id="npv",
            name="Net Present Value",
            latex_formula="NPV = \\sum_{t=0}^{n} \\frac{CF_t}{(1+r)^t}",
            description="The present value of all cash flows associated with an investment",
            variables={
                "CF_t": {"name": "Cash flow at time t", "unit": "$"},
                "r": {"name": "Discount rate", "unit": "%"},
                "n": {"name": "Number of periods", "unit": "periods"}
            },
            example="NPV = $10,000 / (1.10)^1 + $10,000 / (1.10)^2 = $17,355",
            applications=["Capital budgeting", "Investment evaluation", "Project selection"]
        ))
        
        FormulaRepository.register_formula(FormulaDefinition(
            id="irr",
            name="Internal Rate of Return",
            latex_formula="0 = \\sum_{t=0}^{n} \\frac{CF_t}{(1+IRR)^t}",
            description="The discount rate at which NPV equals zero",
            variables={
                "CF_t": {"name": "Cash flow at time t", "unit": "$"},
                "n": {"name": "Number of periods", "unit": "periods"}
            },
            example="For an investment with cash flows [-1000, 500, 600], IRR ≈ 6.6%",
            applications=["Comparing investments", "Project evaluation"]
        ))
        
        FormulaRepository.register_formula(FormulaDefinition(
            id="sharpe_ratio",
            name="Sharpe Ratio",
            latex_formula="\\frac{R_p - R_f}{\\sigma_p}",
            description="Risk-adjusted return measure",
            variables={
                "R_p": {"name": "Portfolio return", "unit": "%"},
                "R_f": {"name": "Risk-free rate", "unit": "%"},
                "\\sigma_p": {"name": "Portfolio standard deviation", "unit": "%"}
            },
            example="Sharpe Ratio = (15% - 3%) / 10% = 1.2",
            applications=["Performance evaluation", "Risk-adjusted comparison"]
        ))
        
        FormulaRepository.register_formula(FormulaDefinition(
            id="pmt",
            name="Loan Payment",
            latex_formula="PMT = \\frac{P \\cdot r \\cdot (1+r)^n}{(1+r)^n - 1}",
            description="Calculate periodic loan payment",
            variables={
                "P": {"name": "Principal", "unit": "$"},
                "r": {"name": "Periodic interest rate", "unit": "%"},
                "n": {"name": "Number of payments", "unit": "payments"}
            },
            example="PMT = ($200,000 × 0.00417 × 360) / (360 - 1) = $973",
            applications=["Mortgage calculations", "Loan amortization"]
        ))
        
        FormulaRepository.register_formula(FormulaDefinition(
            id="compound_interest",
            name="Compound Interest",
            latex_formula="A = P \\left(1 + \\frac{r}{n}\\right)^{nt}",
            description="Calculate compound interest growth",
            variables={
                "A": {"name": "Final amount", "unit": "$"},
                "P": {"name": "Principal", "unit": "$"},
                "r": {"name": "Annual interest rate", "unit": "%"},
                "n": {"name": "Compounding periods per year", "unit": "periods"},
                "t": {"name": "Time in years", "unit": "years"}
            },
            example="$10,000 at 5% compounded monthly for 10 years = $16,470",
            applications=["Savings growth", "Investment projections"]
        ))
        
        # Register concepts
        ConceptRepository.register_concept(FinanceConcept(
            id="time-value-money",
            name="Time Value of Money",
            domain=FinanceDomain.TIME_VALUE_OF_MONEY,
            difficulty=DifficultyLevel.INTERMEDIATE,
            definition="The concept that money available today is worth more than the same amount in the future due to its potential earning capacity.",
            explanation="The time value of money is a fundamental financial principle. A dollar today is worth more than a dollar tomorrow because of the opportunity to invest and earn returns. This concept underlies NPV, IRR, and many other financial calculations.",
            key_points=[
                "Money has time value due to earning potential",
                "Discounting brings future cash flows to present value",
                "Compounding grows present values into the future",
                "Higher discount rates reduce present value"
            ],
            examples=["$100 invested at 5% for 1 year becomes $105"],
            formulas=["npv", "compound_interest"],
            related_concepts=["discounting", "compounding", "present-value"]
        ))
        
        ConceptRepository.register_concept(FinanceConcept(
            id="net-present-value",
            name="Net Present Value (NPV)",
            domain=FinanceDomain.TIME_VALUE_OF_MONEY,
            difficulty=DifficultyLevel.INTERMEDIATE,
            definition="The difference between the present value of cash inflows and the present value of cash outflows over a period of time.",
            explanation="NPV is used in capital budgeting to analyze the profitability of an investment. A positive NPV indicates the investment is profitable, while a negative NPV suggests it should be rejected.",
            key_points=[
                "NPV > 0 means profitable investment",
                "Higher discount rates reduce NPV",
                "Compare NPV across projects with similar risk"
            ],
            examples=["Project with $100,000 investment and $150,000 returns has positive NPV at 10% discount rate"],
            formulas=["npv"],
            related_concepts=["discount-rate", "cash-flow", "capital-budgeting"]
        ))
        
        ConceptRepository.register_concept(FinanceConcept(
            id="sharpe-ratio",
            name="Sharpe Ratio",
            domain=FinanceDomain.RISK_MANAGEMENT,
            difficulty=DifficultyLevel.ADVANCED,
            definition="The average return earned in excess of the risk-free rate per unit of volatility or total risk.",
            explanation="The Sharpe Ratio measures risk-adjusted performance. A higher ratio indicates better return per unit of risk. Ratios above 1 are considered good, above 2 are very good.",
            key_points=[
                "Higher Sharpe Ratio = better risk-adjusted performance",
                "Use consistent time periods for comparison",
                "Risk-free rate is typically Treasury bill yield"
            ],
            examples=["Portfolio returning 15% with 10% volatility and 3% risk-free rate has Sharpe = 1.2"],
            formulas=["sharpe_ratio"],
            related_concepts=["risk-adjusted-return", "volatility", "standard-deviation"]
        ))
        
        ConceptRepository.register_concept(FinanceConcept(
            id="diversification",
            name="Diversification",
            domain=FinanceDomain.PORTFOLIO_MANAGEMENT,
            difficulty=DifficultyLevel.BEGINNER,
            definition="A risk management strategy that mixes a wide variety of investments within a portfolio to reduce exposure to any single asset.",
            explanation="Diversification works because different assets respond differently to market conditions. When some investments decline, others may rise, offsetting losses.",
            key_points=[
                "Don't put all eggs in one basket",
                "Correlated assets provide less diversification benefit",
                "Diversification reduces unsystematic risk"
            ],
            examples=["Holding stocks, bonds, and real estate reduces portfolio volatility"],
            related_concepts=["correlation", "asset-allocation", "risk-management"]
        ))
        
        ConceptRepository.register_concept(FinanceConcept(
            id="moving-averages",
            name="Moving Averages",
            domain=FinanceDomain.TECHNICAL_ANALYSIS,
            difficulty=DifficultyLevel.INTERMEDIATE,
            definition="A technical indicator that smooths out price data by calculating the average price over a specified number of periods.",
            explanation="Moving averages help identify trends and reduce noise. The Simple Moving Average (SMA) gives equal weight to all periods, while the Exponential Moving Average (EMA) gives more weight to recent prices.",
            key_points=[
                "SMA: Equal-weighted average of prices",
                "EMA: Weighted toward recent prices",
                "Golden Cross: 50-day crosses above 200-day",
                "Death Cross: 50-day crosses below 200-day"
            ],
            examples=["50-day SMA of a stock shows its medium-term trend"],
            formulas=["sma", "ema"],
            related_concepts=["trend", "technical-indicators", "support-resistance"]
        ))
        
        # Register market terms
        ConceptRepository.register_term(MarketTerm(
            term="bull market",
            definition="A market condition in which prices are rising or are expected to rise",
            example_usage="We're in a bull market, with the S&P 500 up 20% this year",
            category="market-conditions"
        ))
        
        ConceptRepository.register_term(MarketTerm(
            term="bear market",
            definition="A market condition in which prices are falling or expected to fall",
            example_usage="The bear market erased $2 trillion in market value",
            category="market-conditions"
        ))
        
        ConceptRepository.register_term(MarketTerm(
            term="P/E ratio",
            definition="Price-to-Earnings ratio, the ratio of a company's share price to its earnings per share",
            example_usage="With a P/E ratio of 20, the stock trades at 20x earnings",
            category="valuation"
        ))
        
        ConceptRepository.register_term(MarketTerm(
            term="volatility",
            definition="A statistical measure of the dispersion of returns for a given security or market index",
            example_usage="High volatility in crypto markets led to large price swings",
            category="risk"
        ))
        
        ConceptRepository.register_term(MarketTerm(
            term="dividend yield",
            definition="The ratio of a company's annual dividend compared to its share price",
            example_usage="The 3% dividend yield provides steady income",
            category="income"
        ))
        
        # Register lessons
        ConceptRepository.register_lesson(LessonContent(
            id="lesson-tvm-basics",
            title="Time Value of Money Basics",
            domain=FinanceDomain.TIME_VALUE_OF_MONEY,
            difficulty=DifficultyLevel.BEGINNER,
            objectives=[
                "Understand why money has time value",
                "Calculate present and future values",
                "Apply discounting and compounding"
            ],
            prerequisites=[],
            sections=[
                {
                    "title": "Why Money Has Time Value",
                    "content": "Money available today is worth more than the same amount in the future because it can be invested to earn returns.",
                    "type": "text"
                },
                {
                    "title": "Present Value",
                    "content": "The current value of a future cash flow, discounted at an appropriate rate.",
                    "type": "text"
                },
                {
                    "title": "Future Value",
                    "content": "The value of an asset at a specific date in the future based on an assumed growth rate.",
                    "type": "text"
                }
            ],
            practice_problems=[
                {
                    "question": "What is the future value of $1,000 invested at 5% for 10 years?",
                    "answer": "$1,628.89",
                    "hint": "Use the compound interest formula: FV = PV × (1 + r)^n"
                }
            ],
            summary_points=[
                "Money has time value due to earning potential",
                "Present value = future value / (1 + r)^n",
                "Future value = present value × (1 + r)^n"
            ],
            estimated_minutes=30
        ))
    
    def get_formula(self, formula_id: str) -> Optional[FormulaDefinition]:
        """Get a formula by ID."""
        return FormulaRepository.get_formula(formula_id)
    
    def get_all_formulas(self) -> List[FormulaDefinition]:
        """Get all available formulas."""
        return FormulaRepository.get_all_formulas()
    
    def search_formulas(self, query: str) -> List[FormulaDefinition]:
        """Search formulas by name."""
        return FormulaRepository.search_formulas(query)
    
    def get_concept(self, concept_id: str) -> Optional[FinanceConcept]:
        """Get a concept by ID."""
        return ConceptRepository.get_concept(concept_id)
    
    def get_concepts_by_domain(self, domain: FinanceDomain) -> List[FinanceConcept]:
        """Get all concepts in a domain."""
        return ConceptRepository.get_concepts_by_domain(domain)
    
    def get_lesson(self, lesson_id: str) -> Optional[LessonContent]:
        """Get a lesson by ID."""
        return ConceptRepository.get_lesson(lesson_id)
    
    def get_lessons_by_domain(self, domain: FinanceDomain) -> List[LessonContent]:
        """Get all lessons in a domain."""
        return ConceptRepository.get_lessons_by_domain(domain)
    
    def get_market_term(self, term: str) -> Optional[MarketTerm]:
        """Get a market term definition."""
        return ConceptRepository.get_term(term)
    
    def search_market_terms(self, query: str) -> List[MarketTerm]:
        """Search market terms."""
        return ConceptRepository.search_terms(query)
    
    def get_curriculum_map(
        self, domain: Optional[FinanceDomain] = None
    ) -> List[Dict[str, Any]]:
        """Get a curriculum map showing concepts and their prerequisites."""
        curriculum = []
        concepts = (ConceptRepository.get_concepts_by_domain(domain)
                   if domain else list(ConceptRepository._concepts.values()))
        
        for concept in concepts:
            curriculum.append({
                "id": concept.id,
                "name": concept.name,
                "domain": concept.domain.value,
                "difficulty": concept.difficulty.value,
                "formulas": concept.formulas,
                "estimated_time": f"{len(concept.key_points) * 5} minutes"
            })
        
        return curriculum
    
    def explain_concept_with_formulas(
        self, concept_id: str
    ) -> Dict[str, Any]:
        """Get a concept with its associated formulas."""
        concept = self.get_concept(concept_id)
        if not concept:
            return {"error": "Concept not found"}
        
        formulas = []
        for formula_id in concept.formulas:
            formula = self.get_formula(formula_id)
            if formula:
                formulas.append(formula.to_dict())
        
        return {
            "concept": concept.to_dict(),
            "formulas": formulas
        }
    
    def configure(self, config: Dict[str, Any]) -> None:
        """Configure the service with custom settings."""
        if "custom_content_path" in config:
            pass  # Load custom content from the specified path


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


__all__ = [
    "FinanceDomain",
    "DifficultyLevel",
    "FormulaDefinition",
    "FinanceConcept",
    "LessonContent",
    "MarketTerm",
    "FormulaRepository",
    "ConceptRepository",
    "FinVerseConceptService",
    "create_fin_concept_service"
]
