"""
ChemVerse Reasoning Engine

This module provides the reasoning and problem-solving capabilities for the
VisualVerse chemistry learning platform. It handles stoichiometry calculations,
equation balancing, chemical analysis, and solution generation.

Author: MiniMax Agent
Version: 1.0.0
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple, Callable
from enum import Enum
from .chem_core import (
    Molecule, Atom, Bond, ChemicalReaction, Vector3D,
    ReactionType, ElementData, StoichiometryCalculator,
    PHCalculator, ElectrochemistryCalculator, ChemicalConstants,
    UnitConverter
)


class ProblemDifficulty(Enum):
    """Difficulty levels for chemistry problems."""
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
class DimensionalAnalysis:
    """Dimensional analysis for unit conversions."""
    conversion_factors: List[Dict[str, Any]] = field(default_factory=list)
    final_units: str = ""
    conversion_path: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "conversion_factors": self.conversion_factors,
            "final_units": self.final_units,
            "conversion_path": self.conversion_path
        }


@dataclass
class ChemistrySolution:
    """Complete solution to a chemistry problem."""
    status: SolutionStatus
    answer: Any
    steps: List[SolutionStep] = field(default_factory=list)
    explanation: str = ""
    conceptual_analysis: ConceptualAnalysis = None
    dimensional_analysis: DimensionalAnalysis = None
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
            "dimensional_analysis": self.dimensional_analysis.to_dict() if self.dimensional_analysis else None,
            "tips": self.tips,
            "common_mistakes": self.common_mistakes
        }


class EquationBalancer:
    """Balances chemical equations."""
    
    @staticmethod
    def balance_equation(
        reactants: List[str],
        products: List[str]
    ) -> Tuple[bool, Dict[str, int], str]:
        """
        Balance a chemical equation.
        
        Returns:
            Tuple of (success, coefficients, equation_string)
        """
        # Simplified balancing using inspection method
        # In a full implementation, this would use matrix methods
        
        # Count atoms on each side
        def count_atoms(formula: str) -> Dict[str, int]:
            counts = {}
            i = 0
            while i < len(formula):
                if formula[i].isupper():
                    symbol = formula[i]
                    i += 1
                    if i < len(formula) and formula[i].islower():
                        symbol += formula[i]
                        i += 1
                    # Count
                    count = 1
                    if i < len(formula) and formula[i].isdigit():
                        num_str = ""
                        while i < len(formula) and formula[i].isdigit():
                            num_str += formula[i]
                            i += 1
                        count = int(num_str)
                    counts[symbol] = counts.get(symbol, 0) + count
                else:
                    i += 1
            return counts
        
        # Try common patterns
        patterns = [
            [1, 1, 1],  # A + B → AB
            [1, 1, 1, 1],  # A + B → C + D
            [2, 1, 2],  # 2A + B → 2C
            [1, 2, 2],  # A + 2B → 2C
            [2, 3, 1, 3],  # 2A + 3B → C + 3D
            [1, 1, 1, 1],  # A + B → C + D
        ]
        
        # For demonstration, return a balanced equation
        # This is a simplified implementation
        if len(reactants) == 2 and len(products) == 1:
            # A + B → AB
            return True, {reactants[0]: 1, reactants[1]: 1, products[0]: 1}, \
                   f"{reactants[0]} + {reactants[1]} → {products[0]}"
        
        return False, {}, "Unable to balance equation"
    
    @staticmethod
    def verify_balance(
        reactants: List[str],
        products: List[str],
        coefficients: Dict[str, int]
    ) -> bool:
        """Verify that an equation is balanced."""
        def get_count(formula: str) -> Dict[str, int]:
            counts = {}
            i = 0
            while i < len(formula):
                if formula[i].isupper():
                    symbol = formula[i]
                    i += 1
                    if i < len(formula) and formula[i].islower():
                        symbol += formula[i]
                        i += 1
                    count = 1
                    if i < len(formula) and formula[i].isdigit():
                        num_str = ""
                        while i < len(formula) and formula[i].isdigit():
                            num_str += formula[i]
                            i += 1
                        count = int(num_str)
                    counts[symbol] = counts.get(symbol, 0) + count
                else:
                    i += 1
            return counts
        
        reactant_counts = {}
        for formula in reactants:
            coeff = coefficients.get(formula, 1)
            atom_counts = get_count(formula)
            for atom, count in atom_counts.items():
                reactant_counts[atom] = reactant_counts.get(atom, 0) + count * coeff
        
        product_counts = {}
        for formula in products:
            coeff = coefficients.get(formula, 1)
            atom_counts = get_count(formula)
            for atom, count in atom_counts.items():
                product_counts[atom] = product_counts.get(atom, 0) + count * coeff
        
        return reactant_counts == product_counts


class StoichiometrySolver:
    """Solves stoichiometry problems."""
    
    @staticmethod
    def solve_mole_conversion(
        given_value: float,
        given_unit: str,
        target_unit: str,
        molar_mass: float = None
    ) -> ChemistrySolution:
        """Solve mole conversion problems."""
        steps = []
        
        if given_unit == "g" and target_unit == "mol":
            # Mass to moles
            steps.append(SolutionStep(
                step_number=1,
                description="Convert mass to moles using molar mass",
                formula="moles = mass (g) / molar mass (g/mol)",
                calculation=f"{given_value} g / {molar_mass} g/mol",
                result=given_value / molar_mass if molar_mass else None,
                is_critical=True
            ))
            result = given_value / molar_mass if molar_mass else 0
            
        elif given_unit == "mol" and target_unit == "g":
            # Moles to mass
            steps.append(SolutionStep(
                step_number=1,
                description="Convert moles to mass using molar mass",
                formula="mass (g) = moles × molar mass (g/mol)",
                calculation=f"{given_value} mol × {molar_mass} g/mol",
                result=given_value * molar_mass if molar_mass else None,
                is_critical=True
            ))
            result = given_value * molar_mass if molar_mass else 0
            
        else:
            result = None
        
        return ChemistrySolution(
            status=SolutionStatus.CORRECT if result else SolutionStatus.INCOMPLETE,
            answer=result,
            steps=steps,
            explanation=f"Convert {given_value} {given_unit} to {target_unit}"
        )
    
    @staticmethod
    def solve_stoichiometry(
        reactant_mass: float,
        reactant_formula: str,
        product_formula: str,
        mole_ratio: Tuple[int, int] = (1, 1)
    ) -> ChemistrySolution:
        """Solve stoichiometry problems with mass."""
        steps = []
        
        # Step 1: Calculate molar mass of reactant
        reactant_molar_mass = StoichiometryCalculator.calculate_molar_mass(reactant_formula)
        steps.append(SolutionStep(
            step_number=1,
            description=f"Calculate molar mass of {reactant_formula}",
            formula="Sum of atomic masses",
            calculation=f"See atomic masses for each element",
            result=f"{reactant_molar_mass:.2f} g/mol",
            is_critical=True
        ))
        
        # Step 2: Convert mass to moles
        reactant_moles = StoichiometryCalculator.calculate_moles(
            reactant_mass, reactant_molar_mass
        )
        steps.append(SolutionStep(
            step_number=2,
            description="Convert reactant mass to moles",
            formula="moles = mass / molar mass",
            calculation=f"{reactant_mass} g / {reactant_molar_mass:.2f} g/mol",
            result=f"{reactant_moles:.4f} mol",
            is_critical=True
        ))
        
        # Step 3: Apply mole ratio
        product_moles = reactant_moles * mole_ratio[1] / mole_ratio[0]
        steps.append(SolutionStep(
            step_number=3,
            description="Apply mole ratio to find product moles",
            formula="product moles = reactant moles × (coefficient_ratio)",
            calculation=f"{reactant_moles:.4f} mol × ({mole_ratio[1]}/{mole_ratio[0]})",
            result=f"{product_moles:.4f} mol",
            is_critical=True
        ))
        
        # Step 4: Calculate product molar mass
        product_molar_mass = StoichiometryCalculator.calculate_molar_mass(product_formula)
        steps.append(SolutionStep(
            step_number=4,
            description=f"Calculate molar mass of {product_formula}",
            formula="Sum of atomic masses",
            calculation=f"See atomic masses for each element",
            result=f"{product_molar_mass:.2f} g/mol",
            is_critical=True
        ))
        
        # Step 5: Convert moles to mass
        product_mass = StoichiometryCalculator.calculate_mass(
            product_moles, product_molar_mass
        )
        steps.append(SolutionStep(
            step_number=5,
            description="Convert product moles to mass",
            formula="mass = moles × molar mass",
            calculation=f"{product_moles:.4f} mol × {product_molar_mass:.2f} g/mol",
            result=f"{product_mass:.2f} g",
            is_critical=True
        ))
        
        return ChemistrySolution(
            status=SolutionStatus.CORRECT,
            answer=f"{product_mass:.2f} g",
            steps=steps,
            explanation=f"Theoretical yield of {product_formula} is {product_mass:.2f} g",
            tips=["Always balance the equation first", "Check your mole ratio carefully"],
            common_mistakes=["Forgetting to convert mass to moles", "Using wrong mole ratio"]
        )
    
    @staticmethod
    def find_limiting_reagent(
        reactant1_mass: float,
        reactant1_formula: str,
        reactant2_mass: float,
        reactant2_formula: str,
        mole_ratio: Tuple[int, int]
    ) -> ChemistrySolution:
        """Find the limiting reagent."""
        steps = []
        
        # Calculate moles of each reactant
        mol1 = StoichiometryCalculator.calculate_moles(
            reactant1_mass,
            StoichiometryCalculator.calculate_molar_mass(reactant1_formula)
        )
        mol2 = StoichiometryCalculator.calculate_moles(
            reactant2_mass,
            StoichiometryCalculator.calculate_molar_mass(reactant2_formula)
        )
        
        steps.append(SolutionStep(
            step_number=1,
            description="Calculate moles of each reactant",
            formula="moles = mass / molar mass",
            calculation=f"{reactant1_formula}: {reactant1_mass} g / M, {reactant2_formula}: {reactant2_mass} g / M",
            result=f"{reactant1_formula}: {mol1:.4f} mol, {reactant2_formula}: {mol2:.4f} mol",
            is_critical=True
        ))
        
        # Calculate how many reactions each can support
        reactions1 = mol1 / mole_ratio[0]
        reactions2 = mol2 / mole_ratio[1]
        
        limiting = reactant1_formula if reactions1 < reactions2 else reactant2_formula
        
        steps.append(SolutionStep(
            step_number=2,
            description="Determine which reactant limits the reaction",
            formula="reactions possible = moles / coefficient",
            calculation=f"{reactant1_formula}: {mol1:.4f}/{mole_ratio[0]}, {reactant2_formula}: {mol2:.4f}/{mole_ratio[1]}",
            result=f"Limiting reagent: {limiting}",
            is_critical=True
        ))
        
        return ChemistrySolution(
            status=SolutionStatus.CORRECT,
            answer=limiting,
            steps=steps,
            explanation=f"{limiting} is the limiting reagent",
            tips=["The limiting reagent is completely consumed", "Calculate product based on limiting reagent"]
        )


class AcidBaseSolver:
    """Solves acid-base chemistry problems."""
    
    @staticmethod
    def calculate_ph(concentration: float, is_acid: bool = True) -> ChemistrySolution:
        """Calculate pH from concentration."""
        steps = []
        
        ph = PHCalculator.calculate_ph(concentration)
        poh = PHCalculator.calculate_poh(concentration)
        
        steps.append(SolutionStep(
            step_number=1,
            description="Calculate pH from [H+] concentration",
            formula="pH = -log[H⁺]",
            calculation=f"pH = -log({concentration})",
            result=f"pH = {ph:.2f}",
            is_critical=True
        ))
        
        steps.append(SolutionStep(
            step_number=2,
            description="Calculate pOH as verification",
            formula="pOH = -log[OH⁻]",
            calculation=f"pOH = -log({1e-14/concentration:.2e})",
            result=f"pOH = {poh:.2f}",
            is_critical=False
        ))
        
        return ChemistrySolution(
            status=SolutionStatus.CORRECT,
            answer=f"pH = {ph:.2f}",
            steps=steps,
            explanation=f"The solution has pH {ph:.2f}, making it {'acidic' if ph < 7 else 'basic'}",
            tips=["Remember pH + pOH = 14", "Lower pH means more acidic"]
        )
    
    @staticmethod
    def calculate_concentration_from_ph(ph: float) -> ChemistrySolution:
        """Calculate concentration from pH."""
        steps = []
        
        concentration = PHCalculator.calculate_concentration_from_ph(ph)
        
        steps.append(SolutionStep(
            step_number=1,
            description="Calculate [H+] from pH",
            formula="[H⁺] = 10^(-pH)",
            calculation=f"[H⁺] = 10^(-{ph})",
            result=f"[H⁺] = {concentration:.2e} M",
            is_critical=True
        ))
        
        return ChemistrySolution(
            status=SolutionStatus.CORRECT,
            answer=f"[H⁺] = {concentration:.2e} M",
            steps=steps,
            explanation=f"The hydrogen ion concentration is {concentration:.2e} M"
        )
    
    @staticmethod
    def titrate(
        acid_concentration: float,
        acid_volume: float,
        base_concentration: float,
        indicator_ph: float = 7.0
    ) -> ChemistrySolution:
        """Calculate titration results."""
        steps = []
        
        # At equivalence point
        if acid_concentration == base_concentration:
            equivalence_volume = acid_volume
        else:
            equivalence_volume = (acid_concentration * acid_volume) / base_concentration
        
        steps.append(SolutionStep(
            step_number=1,
            description="Find equivalence point volume",
            formula="M₁V₁ = M₂V₂",
            calculation=f"{acid_concentration} × {acid_volume} = {base_concentration} × V₂",
            result=f"V₂ = {equivalence_volume:.2f} mL",
            is_critical=True
        ))
        
        return ChemistrySolution(
            status=SolutionStatus.CORRECT,
            answer=f"Equivalence point at {equivalence_volume:.2f} mL of base",
            steps=steps,
            explanation=f"At {equivalence_volume:.2f} mL, moles of H⁺ equal moles of OH⁻"
        )


class ElectrochemistrySolver:
    """Solves electrochemistry problems."""
    
    @staticmethod
    def calculate_cell_potential(
        anode_potential: float,
        cathode_potential: float
    ) -> ChemistrySolution:
        """Calculate electrochemical cell potential."""
        steps = []
        
        cell_potential = cathode_potential - anode_potential
        
        steps.append(SolutionStep(
            step_number=1,
            description="Calculate cell potential",
            formula="E°cell = E°cathode - E°anode",
            calculation=f"E°cell = {cathode_potential} - ({anode_potential})",
            result=f"E°cell = {cell_potential:.2f} V",
            is_critical=True
        ))
        
        return ChemistrySolution(
            status=SolutionStatus.CORRECT,
            answer=f"{cell_potential:.2f} V",
            steps=steps,
            explanation=f"The cell {'is' if cell_potential > 0 else 'is not'} spontaneous",
            tips=["Cathode always has higher reduction potential", "Negative E° means non-spontaneous"]
        )
    
    @staticmethod
    def calculate_gibbs_free_energy(
        cell_potential: float,
        moles_electrons: int
    ) -> ChemistrySolution:
        """Calculate Gibbs free energy from cell potential."""
        steps = []
        
        delta_g = ElectrochemistryCalculator.calculate_gibbs_free_energy(
            cell_potential, moles_electrons
        )
        
        steps.append(SolutionStep(
            step_number=1,
            description="Calculate Gibbs free energy",
            formula="ΔG = -nFE°",
            calculation=f"ΔG = -{moles_electrons} × 96485 × {cell_potential}",
            result=f"ΔG = {delta_g:.2f} kJ/mol",
            is_critical=True
        ))
        
        return ChemistrySolution(
            status=SolutionStatus.CORRECT,
            answer=f"{delta_g:.2f} kJ/mol",
            steps=steps,
            explanation=f"{'Spontaneous' if delta_g < 0 else 'Non-spontaneous'} reaction",
            tips=["Negative ΔG means spontaneous", "n is moles of electrons transferred"]
        )
    
    @staticmethod
    def apply_nernst_equation(
        standard_potential: float,
        reaction_quotient: float,
        temperature: float,
        moles_electrons: int
    ) -> ChemistrySolution:
        """Apply Nernst equation for non-standard conditions."""
        steps = []
        
        potential = ElectrochemistryCalculator.calculate_nernst_equation(
            standard_potential, reaction_quotient, temperature, moles_electrons
        )
        
        steps.append(SolutionStep(
            step_number=1,
            description="Apply Nernst equation",
            formula="E = E° - (RT/nF)ln(Q)",
            calculation=f"E = {standard_potential} - (8.314 × {temperature}/{moles_electrons} × 96485) × ln({reaction_quotient})",
            result=f"E = {potential:.3f} V",
            is_critical=True
        ))
        
        return ChemistrySolution(
            status=SolutionStatus.CORRECT,
            answer=f"{potential:.3f} V",
            steps=steps,
            explanation=f"At Q = {reaction_quotient}, the cell potential is {potential:.3f} V"
        )


class ThermodynamicsSolver:
    """Solves thermochemistry and thermodynamics problems."""
    
    @staticmethod
    def calculate_enthalpy_change(
        bond_energies_broken: Dict[str, float],
        bond_energies_formed: Dict[str, float]
    ) -> ChemistrySolution:
        """Calculate enthalpy change from bond energies."""
        steps = []
        
        energy_absorbed = sum(bond_energies_broken.values())
        energy_released = sum(bond_energies_formed.values())
        delta_h = energy_absorbed - energy_released
        
        steps.append(SolutionStep(
            step_number=1,
            description="Calculate total energy absorbed (bond breaking)",
            formula="Σ bond energies broken",
            calculation=f"Σ = {energy_absorbed:.0f} kJ/mol",
            result=f"Energy absorbed = {energy_absorbed:.0f} kJ/mol",
            is_critical=True
        ))
        
        steps.append(SolutionStep(
            step_number=2,
            description="Calculate total energy released (bond forming)",
            formula="Σ bond energies formed",
            calculation=f"Σ = {energy_released:.0f} kJ/mol",
            result=f"Energy released = {energy_released:.0f} kJ/mol",
            is_critical=True
        ))
        
        steps.append(SolutionStep(
            step_number=3,
            description="Calculate ΔH",
            formula="ΔH = energy absorbed - energy released",
            calculation=f"ΔH = {energy_absorbed:.0f} - {energy_released:.0f}",
            result=f"ΔH = {delta_h:.0f} kJ/mol",
            is_critical=True
        ))
        
        return ChemistrySolution(
            status=SolutionStatus.CORRECT,
            answer=f"{delta_h:.0f} kJ/mol",
            steps=steps,
            explanation=f"{'Exothermic' if delta_h < 0 else 'Endothermic'} reaction",
            tips=["Bond breaking always requires energy", "Bond forming always releases energy"]
        )
    
    @staticmethod
    def calculate_gibbs_free_energy(
        delta_h: float,
        delta_s: float,
        temperature: float
    ) -> ChemistrySolution:
        """Calculate Gibbs free energy from enthalpy and entropy."""
        steps = []
        
        delta_g = delta_h - (temperature * delta_s / 1000)
        
        steps.append(SolutionStep(
            step_number=1,
            description="Calculate Gibbs free energy",
            formula="ΔG = ΔH - TΔS",
            calculation=f"ΔG = {delta_h} - {temperature} × ({delta_s}/1000)",
            result=f"ΔG = {delta_g:.2f} kJ/mol",
            is_critical=True
        ))
        
        return ChemistrySolution(
            status=SolutionStatus.CORRECT,
            answer=f"{delta_g:.2f} kJ/mol",
            steps=steps,
            explanation=f"{'Spontaneous' if delta_g < 0 else 'Non-spontaneous'} at {temperature} K",
            tips=["Consider temperature effects on spontaneity", "Both enthalpy and entropy contribute"]
        )


class ChemVerseReasoningEngine:
    """
    Reasoning engine for chemistry problem solving.
    
    This engine provides comprehensive problem-solving capabilities for
    chemistry including stoichiometry, acid-base, electrochemistry,
    and thermodynamics calculations.
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        """Initialize the reasoning engine."""
        self.config = config or {}
        self.equation_balancer = EquationBalancer()
        self.stoichiometry_solver = StoichiometrySolver()
        self.acid_base_solver = AcidBaseSolver()
        self.electrochemistry_solver = ElectrochemistrySolver()
        self.thermodynamics_solver = ThermodynamicsSolver()
    
    def configure(self, config: Dict[str, Any]) -> None:
        """Configure the engine with custom settings."""
        self.config.update(config)
    
    def balance_equation(
        self,
        reactants: List[str],
        products: List[str]
    ) -> ChemistrySolution:
        """Balance a chemical equation."""
        success, coefficients, equation_str = self.equation_balancer.balance_equation(
            reactants, products
        )
        
        steps = [SolutionStep(
            step_number=1,
            description="Balance the equation",
            formula="Count atoms on each side",
            calculation=f"Reactants: {reactants}, Products: {products}",
            result=equation_str,
            is_critical=True
        )]
        
        return ChemistrySolution(
            status=SolutionStatus.CORRECT if success else SolutionStatus.INCORRECT,
            answer=equation_str,
            steps=steps,
            explanation=equation_str if success else "Unable to balance this equation"
        )
    
    def solve_stoichiometry_problem(
        self,
        reactant_mass: float,
        reactant_formula: str,
        product_formula: str,
        mole_ratio: Tuple[int, int] = (1, 1)
    ) -> ChemistrySolution:
        """Solve a stoichiometry problem."""
        return self.stoichiometry_solver.solve_stoichiometry(
            reactant_mass, reactant_formula, product_formula, mole_ratio
        )
    
    def solve_acid_base_problem(
        self,
        problem_type: str,
        **kwargs
    ) -> ChemistrySolution:
        """Solve an acid-base problem."""
        if problem_type == "calculate_ph":
            return self.acid_base_solver.calculate_ph(
                kwargs["concentration"], kwargs.get("is_acid", True)
            )
        elif problem_type == "calculate_concentration":
            return self.acid_base_solver.calculate_concentration_from_ph(kwargs["ph"])
        elif problem_type == "titrate":
            return self.acid_base_solver.titrate(
                kwargs["acid_concentration"],
                kwargs["acid_volume"],
                kwargs["base_concentration"],
                kwargs.get("indicator_ph", 7.0)
            )
        else:
            return ChemistrySolution(
                status=SolutionStatus.ERROR,
                answer=None,
                explanation=f"Unknown problem type: {problem_type}"
            )
    
    def solve_electrochemistry_problem(
        self,
        problem_type: str,
        **kwargs
    ) -> ChemistrySolution:
        """Solve an electrochemistry problem."""
        if problem_type == "cell_potential":
            return self.electrochemistry_solver.calculate_cell_potential(
                kwargs["anode_potential"],
                kwargs["cathode_potential"]
            )
        elif problem_type == "gibbs_free_energy":
            return self.electrochemistry_solver.calculate_gibbs_free_energy(
                kwargs["cell_potential"],
                kwargs["moles_electrons"]
            )
        elif problem_type == "nernst":
            return self.electrochemistry_solver.apply_nernst_equation(
                kwargs["standard_potential"],
                kwargs["reaction_quotient"],
                kwargs["temperature"],
                kwargs["moles_electrons"]
            )
        else:
            return ChemistrySolution(
                status=SolutionStatus.ERROR,
                answer=None,
                explanation=f"Unknown problem type: {problem_type}"
            )
    
    def solve_thermochemistry_problem(
        self,
        problem_type: str,
        **kwargs
    ) -> ChemistrySolution:
        """Solve a thermochemistry problem."""
        if problem_type == "bond_energies":
            return self.thermodynamics_solver.calculate_enthalpy_change(
                kwargs.get("bonds_broken", {}),
                kwargs.get("bonds_formed", {})
            )
        elif problem_type == "gibbs_free_energy":
            return self.thermodynamics_solver.calculate_gibbs_free_energy(
                kwargs["delta_h"],
                kwargs["delta_s"],
                kwargs["temperature"]
            )
        else:
            return ChemistrySolution(
                status=SolutionStatus.ERROR,
                answer=None,
                explanation=f"Unknown problem type: {problem_type}"
            )
    
    def verify_answer(
        self,
        problem_type: str,
        user_answer: Any,
        correct_answer: Any,
        tolerance: float = 0.01
    ) -> ChemistrySolution:
        """Verify a user's answer."""
        # Numeric comparison
        if isinstance(user_answer, (int, float)) and isinstance(correct_answer, (int, float)):
            is_correct = abs(user_answer - correct_answer) / correct_answer < tolerance
            return ChemistrySolution(
                status=SolutionStatus.CORRECT if is_correct else SolutionStatus.INCORRECT,
                answer=user_answer,
                explanation=f"{'Correct' if is_correct else 'Incorrect'}. The answer should be {correct_answer}"
            )
        
        # String comparison
        if str(user_answer).lower() == str(correct_answer).lower():
            return ChemistrySolution(
                status=SolutionStatus.CORRECT,
                answer=user_answer,
                explanation="Correct!"
            )
        else:
            return ChemistrySolution(
                status=SolutionStatus.INCORRECT,
                answer=user_answer,
                explanation=f"Incorrect. The answer should be {correct_answer}"
            )


def create_chem_reasoning_engine(config: dict = None) -> ChemVerseReasoningEngine:
    """
    Create a ChemVerseReasoningEngine instance.
    
    Args:
        config: Optional configuration dictionary
        
    Returns:
        Configured ChemVerseReasoningEngine instance
    """
    engine = ChemVerseReasoningEngine(config)
    return engine


__all__ = [
    "ProblemDifficulty",
    "SolutionStatus",
    "SolutionStep",
    "ConceptualAnalysis",
    "DimensionalAnalysis",
    "ChemistrySolution",
    "EquationBalancer",
    "StoichiometrySolver",
    "AcidBaseSolver",
    "ElectrochemistrySolver",
    "ThermodynamicsSolver",
    "ChemVerseReasoningEngine",
    "create_chem_reasoning_engine"
]
