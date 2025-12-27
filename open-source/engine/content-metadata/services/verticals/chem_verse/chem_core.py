"""
ChemVerse Core Module

This module provides the mathematical foundations and data structures for chemistry
computations in the VisualVerse learning platform. It includes classes for atomic
structure, molecular composition, chemical reactions, and thermodynamic calculations.

Author: MiniMax Agent
Version: 1.0.0
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Tuple, Any
from decimal import Decimal
import math


class ElementSymbol(str, Enum):
    """Standard chemical element symbols."""
    H = "H"
    HE = "He"
    LI = "Li"
    BE = "Be"
    B = "B"
    C = "C"
    N = "N"
    O = "O"
    F = "F"
    NE = "Ne"
    NA = "Na"
    MG = "Mg"
    AL = "Al"
    SI = "Si"
    P = "P"
    S = "S"
    CL = "Cl"
    AR = "Ar"
    K = "K"
    CA = "Ca"
    FE = "Fe"
    CU = "Cu"
    ZN = "Zn"
    AG = "Ag"
    AU = "Au"
    HG = "Hg"
    PB = "Pb"
    U = "U"


class BondType(str, Enum):
    """Types of chemical bonds."""
    COVALENT_SINGLE = "covalent_single"
    COVALENT_DOUBLE = "covalent_double"
    COVALENT_TRIPLE = "covalent_triple"
    COVALENT_AROMATIC = "covalent_aromatic"
    IONIC = "ionic"
    METALLIC = "metallic"
    HYDROGEN = "hydrogen"
    COORDINATE = "coordinate"


class HybridizationType(str, Enum):
    """Orbital hybridization types."""
    SP = "sp"
    SP2 = "sp2"
    SP3 = "sp3"
    SP3D = "sp3d"
    SP3D2 = "sp3d2"
    NONE = "none"


class ReactionType(str, Enum):
    """Types of chemical reactions."""
    SYNTHESIS = "synthesis"
    DECOMPOSITION = "decomposition"
    SINGLE_REPLACEMENT = "single_replacement"
    DOUBLE_REPLACEMENT = "double_replacement"
    COMBUSTION = "combustion"
    ACID_BASE = "acid_base"
    REDOX = "redox"
    PRECIPITATION = "precipitation"


class Phase(str, Enum):
    """Physical phases of matter."""
    SOLID = "solid"
    LIQUID = "liquid"
    GAS = "gas"
    AQUEOUS = "aqueous"
    PLASMA = "plasma"


class ElementData:
    """Comprehensive data for a chemical element."""
    
    _element_database: Dict[str, Dict[str, Any]] = {
        "H": {
            "name": "Hydrogen",
            "atomic_number": 1,
            "atomic_mass": 1.008,
            "electronegativity": 2.20,
            "valence_electrons": 1,
            "covalent_radius": 31,
            "van_der_waals_radius": 120,
            "group": 1,
            "period": 1,
            "category": "nonmetal",
            "color_rgb": (255, 255, 255)
        },
        "C": {
            "name": "Carbon",
            "atomic_number": 6,
            "atomic_mass": 12.011,
            "electronegativity": 2.55,
            "valence_electrons": 4,
            "covalent_radius": 76,
            "van_der_waals_radius": 170,
            "group": 14,
            "period": 2,
            "category": "nonmetal",
            "color_rgb": (100, 100, 100)
        },
        "N": {
            "name": "Nitrogen",
            "atomic_number": 7,
            "atomic_mass": 14.007,
            "electronegativity": 3.04,
            "valence_electrons": 5,
            "covalent_radius": 71,
            "van_der_waals_radius": 155,
            "group": 15,
            "period": 2,
            "category": "nonmetal",
            "color_rgb": (0, 0, 255)
        },
        "O": {
            "name": "Oxygen",
            "atomic_number": 8,
            "atomic_mass": 15.999,
            "electronegativity": 3.44,
            "valence_electrons": 6,
            "covalent_radius": 66,
            "van_der_waals_radius": 152,
            "group": 16,
            "period": 2,
            "category": "nonmetal",
            "color_rgb": (255, 0, 0)
        },
        "F": {
            "name": "Fluorine",
            "atomic_number": 9,
            "atomic_mass": 18.998,
            "electronegativity": 3.98,
            "valence_electrons": 7,
            "covalent_radius": 57,
            "van_der_waals_radius": 147,
            "group": 17,
            "period": 2,
            "category": "halogen",
            "color_rgb": (0, 255, 0)
        },
        "NA": {
            "name": "Sodium",
            "atomic_number": 11,
            "atomic_mass": 22.990,
            "electronegativity": 0.93,
            "valence_electrons": 1,
            "covalent_radius": 154,
            "van_der_waals_radius": 227,
            "group": 1,
            "period": 3,
            "category": "alkali_metal",
            "color_rgb": (170, 0, 170)
        },
        "CL": {
            "name": "Chlorine",
            "atomic_number": 17,
            "atomic_mass": 35.45,
            "electronegativity": 3.16,
            "valence_electrons": 7,
            "covalent_radius": 102,
            "van_der_waals_radius": 175,
            "group": 17,
            "period": 3,
            "category": "halogen",
            "color_rgb": (0, 255, 0)
        },
        "FE": {
            "name": "Iron",
            "atomic_number": 26,
            "atomic_mass": 55.845,
            "electronegativity": 1.83,
            "valence_electrons": 2,
            "covalent_radius": 132,
            "van_der_waals_radius": 194,
            "group": 8,
            "period": 4,
            "category": "transition_metal",
            "color_rgb": (255, 165, 0)
        },
        "CU": {
            "name": "Copper",
            "atomic_number": 29,
            "atomic_mass": 63.546,
            "electronegativity": 1.90,
            "valence_electrons": 1,
            "covalent_radius": 132,
            "van_der_waals_radius": 163,
            "group": 11,
            "period": 4,
            "category": "transition_metal",
            "color_rgb": (184, 115, 51)
        },
        "AG": {
            "name": "Silver",
            "atomic_number": 47,
            "atomic_mass": 107.868,
            "electronegativity": 1.93,
            "valence_electrons": 1,
            "covalent_radius": 145,
            "van_der_waals_radius": 172,
            "group": 11,
            "period": 5,
            "category": "transition_metal",
            "color_rgb": (192, 192, 192)
        },
        "AU": {
            "name": "Gold",
            "atomic_number": 79,
            "atomic_mass": 196.967,
            "electronegativity": 2.54,
            "valence_electrons": 1,
            "covalent_radius": 136,
            "van_der_waals_radius": 166,
            "group": 11,
            "period": 6,
            "category": "transition_metal",
            "color_rgb": (255, 215, 0)
        }
    }
    
    @classmethod
    def get_data(cls, symbol: str) -> Optional[Dict[str, Any]]:
        """Get element data by symbol."""
        return cls._element_database.get(symbol.upper())
    
    @classmethod
    def get_atomic_mass(cls, symbol: str) -> float:
        """Get atomic mass for an element."""
        data = cls.get_data(symbol)
        return data["atomic_mass"] if data else 0.0
    
    @classmethod
    def get_electronegativity(cls, symbol: str) -> float:
        """Get electronegativity for an element."""
        data = cls.get_data(symbol)
        return data["electronegativity"] if data else 0.0


@dataclass
class Vector3D:
    """3D position vector for atomic coordinates."""
    x: float
    y: float
    z: float
    
    def __add__(self, other: 'Vector3D') -> 'Vector3D':
        return Vector3D(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other: 'Vector3D') -> 'Vector3D':
        return Vector3D(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def __mul__(self, scalar: float) -> 'Vector3D':
        return Vector3D(self.x * scalar, self.y * scalar, self.z * scalar)
    
    def magnitude(self) -> float:
        """Calculate the magnitude of the vector."""
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)
    
    def distance_to(self, other: 'Vector3D') -> float:
        """Calculate distance to another vector."""
        return (self - other).magnitude()
    
    def normalize(self) -> 'Vector3D':
        """Return a unit vector in the same direction."""
        mag = self.magnitude()
        if mag == 0:
            return Vector3D(0, 0, 0)
        return Vector3D(self.x / mag, self.y / mag, self.z / mag)


@dataclass
class Atom:
    """Represents a single atom in a molecule."""
    id: str
    element_symbol: str
    position: Vector3D
    charge: int = 0
    hybridization: HybridizationType = HybridizationType.NONE
    formal_charge: int = 0
    implicit_hydrogens: int = 0
    
    @property
    def atomic_number(self) -> int:
        """Get the atomic number."""
        data = ElementData.get_data(self.element_symbol)
        return data["atomic_number"] if data else 0
    
    @property
    def atomic_mass(self) -> float:
        """Get the atomic mass."""
        return ElementData.get_atomic_mass(self.element_symbol)
    
    @property
    def electronegativity(self) -> float:
        """Get the electronegativity."""
        return ElementData.get_electronegativity(self.element_symbol)
    
    @property
    def valence_electrons(self) -> int:
        """Get the number of valence electrons."""
        data = ElementData.get_data(self.element_symbol)
        return data["valence_electrons"] if data else 0
    
    @property
    def total_electrons(self) -> int:
        """Get total electrons (atomic number minus charge)."""
        return self.atomic_number - self.charge
    
    @property
    def element_name(self) -> str:
        """Get the full element name."""
        data = ElementData.get_data(self.element_symbol)
        return data["name"] if data else "Unknown"
    
    @property
    def color_rgb(self) -> Tuple[int, int, int]:
        """Get the standard CPK color for this element."""
        data = ElementData.get_data(self.element_symbol)
        return tuple(data["color_rgb"]) if data else (128, 128, 128)
    
    def get_oxidation_state(self) -> int:
        """Calculate oxidation state based on electronegativity."""
        return self.formal_charge


@dataclass
class Bond:
    """Represents a chemical bond between two atoms."""
    id: str
    atom1_id: str
    atom2_id: str
    bond_type: BondType
    order: int = 1
    length: float = 1.5  # Angstroms
    is_aromatic: bool = False
    
    @property
    def is_single(self) -> bool:
        """Check if this is a single bond."""
        return self.bond_type == BondType.COVALENT_SINGLE and not self.is_aromatic
    
    @property
    def is_double(self) -> bool:
        """Check if this is a double bond."""
        return self.bond_type == BondType.COVALENT_DOUBLE
    
    @property
    def is_triple(self) -> bool:
        """Check if this is a triple bond."""
        return self.bond_type == BondType.COVALENT_TRIPLE
    
    def get_bond_energy(self) -> float:
        """Get approximate bond energy in kJ/mol."""
        bond_energies = {
            (BondType.COVALENT_SINGLE, "C", "C"): 347,
            (BondType.COVALENT_SINGLE, "C", "H"): 413,
            (BondType.COVALENT_SINGLE, "C", "O"): 358,
            (BondType.COVALENT_SINGLE, "O", "H"): 463,
            (BondType.COVALENT_SINGLE, "N", "H"): 391,
            (BondType.COVALENT_SINGLE, "H", "H"): 436,
            (BondType.COVALENT_DOUBLE, "C", "C"): 614,
            (BondType.COVALENT_DOUBLE, "C", "O"): 745,
            (BondType.COVALENT_DOUBLE, "O", "O"): 146,
            (BondType.COVALENT_TRIPLE, "C", "C): 839,
            (BondType.COVALENT_TRIPLE, "C", "N"): 615,
            (BondType.COVALENT_TRIPLE, "N", "N"): 418
        }
        return bond_energies.get((self.bond_type, self.atom1_symbol, self.atom2_symbol), 200)


@dataclass
class Molecule:
    """Represents a chemical molecule with atoms and bonds."""
    id: str
    name: str
    formula: str = ""
    atoms: List[Atom] = field(default_factory=list)
    bonds: List[Bond] = field(default_factory=list)
    smiles: str = ""
    charge: int = 0
    phase: Phase = Phase.AQUEOUS
    
    def get_atom_by_id(self, atom_id: str) -> Optional[Atom]:
        """Get an atom by its ID."""
        for atom in self.atoms:
            if atom.id == atom_id:
                return atom
        return None
    
    def get_bond_between(self, atom1_id: str, atom2_id: str) -> Optional[Bond]:
        """Get the bond between two atoms."""
        for bond in self.bonds:
            if (bond.atom1_id == atom1_id and bond.atom2_id == atom2_id) or \
               (bond.atom1_id == atom2_id and bond.atom2_id == atom1_id):
                return bond
        return None
    
    def get_molecular_weight(self) -> float:
        """Calculate the molecular weight in g/mol."""
        total_mass = 0.0
        for atom in self.atoms:
            total_mass += atom.atomic_mass
        return total_mass
    
    def get_atom_count(self) -> Dict[str, int]:
        """Get a count of each element in the molecule."""
        counts = {}
        for atom in self.atoms:
            counts[atom.element_symbol] = counts.get(atom.element_symbol, 0) + 1
        return counts
    
    def get_formula(self) -> str:
        """Generate the chemical formula."""
        counts = self.get_atom_count()
        formula_parts = []
        # Carbon first
        if "C" in counts:
            formula_parts.append(f"C{counts['C']}" if counts["C"] > 1 else "C")
            del counts["C"]
        # Hydrogen second
        if "H" in counts:
            formula_parts.append(f"H{counts['H']}" if counts["H"] > 1 else "H")
            del counts["H"]
        # Remaining elements alphabetically
        for symbol in sorted(counts.keys()):
            count = counts[symbol]
            formula_parts.append(f"{symbol}{count}" if count > 1 else symbol)
        return "".join(formula_parts)
    
    def get_center_of_mass(self) -> Vector3D:
        """Calculate the center of mass of the molecule."""
        total_mass = 0.0
        weighted_pos = Vector3D(0, 0, 0)
        for atom in self.atoms:
            mass = atom.atomic_mass
            total_mass += mass
            weighted_pos = weighted_pos + atom.position * mass
        if total_mass == 0:
            return Vector3D(0, 0, 0)
        return Vector3D(
            weighted_pos.x / total_mass,
            weighted_pos.y / total_mass,
            weighted_pos.z / total_mass
        )
    
    def get_coordination_number(self, atom_id: str) -> int:
        """Get the coordination number for an atom."""
        count = 0
        for bond in self.bonds:
            if bond.atom1_id == atom_id or bond.atom2_id == atom_id:
                count += bond.order
        return count
    
    def is_valid(self) -> bool:
        """Validate the molecule structure."""
        # Check that all bonds reference valid atoms
        atom_ids = {atom.id for atom in self.atoms}
        for bond in self.bonds:
            if bond.atom1_id not in atom_ids or bond.atom2_id not in atom_ids:
                return False
        # Check valence rules for common elements
        for atom in self.atoms:
            coord = self.get_coordination_number(atom.id)
            valence = atom.valence_electrons
            if atom.element_symbol == "C" and coord > 4:
                return False
            if atom.element_symbol in ("N", "P") and coord > 3:
                return False
            if atom.element_symbol in ("O", "S") and coord > 2:
                return False
        return True


@dataclass
class ChemicalReaction:
    """Represents a chemical reaction with reactants and products."""
    id: str
    reaction_type: ReactionType
    reactants: List[Molecule] = field(default_factory=list)
    products: List[Molecule] = field(default_factory=list)
    catalysts: List[Molecule] = field(default_factory=list)
    coefficients: List[int] = field(default_factory=list)
    
    # Reaction conditions
    temperature: float = 298.15  # Kelvin
    pressure: float = 1.0  # atm
    ph: float = 7.0
    
    # Thermodynamic data
    delta_h: float = 0.0  # Enthalpy change (kJ/mol)
    delta_s: float = 0.0  # Entropy change (J/mol·K)
    delta_g: float = 0.0  # Gibbs free energy change (kJ/mol)
    equilibrium_constant: float = 0.0
    activation_energy: float = 0.0  # kJ/mol
    
    def get_reactant_formula(self) -> str:
        """Get the combined reactant formula."""
        if not self.reactants:
            return ""
        parts = []
        for i, mol in enumerate(self.reactants):
            coeff = self.coefficients[i] if i < len(self.coefficients) else 1
            if coeff > 1:
                parts.append(f"{coeff}{mol.get_formula()}")
            else:
                parts.append(mol.get_formula())
        return " + ".join(parts)
    
    def get_product_formula(self) -> str:
        """Get the combined product formula."""
        if not self.products:
            return ""
        parts = []
        offset = len(self.reactants)
        for i, mol in enumerate(self.products):
            idx = offset + i
            coeff = self.coefficients[idx] if idx < len(self.coefficients) else 1
            if coeff > 1:
                parts.append(f"{coeff}{mol.get_formula()}")
            else:
                parts.append(mol.get_formula())
        return " + ".join(parts)
    
    def get_equation_string(self) -> str:
        """Get the full reaction equation string."""
        return f"{self.get_reactant_formula()} → {self.get_product_formula()}"
    
    def calculate_delta_g(self) -> float:
        """Calculate Gibbs free energy from enthalpy and entropy."""
        self.delta_g = self.delta_h - self.temperature * self.delta_s / 1000
        return self.delta_g
    
    def calculate_equilibrium_constant(self) -> float:
        """Calculate equilibrium constant from delta G."""
        if self.delta_g == 0:
            self.calculate_delta_g()
        R = 8.314  # J/mol·K
        self.equilibrium_constant = math.exp(-self.delta_g * 1000 / (R * self.temperature))
        return self.equilibrium_constant
    
    def is_balanced(self) -> bool:
        """Check if the reaction is balanced."""
        # Count atoms on each side
        reactant_counts = {}
        product_counts = {}
        
        for i, mol in enumerate(self.reactants):
            coeff = self.coefficients[i] if i < len(self.coefficients) else 1
            for atom_count in mol.get_atom_count().items():
                symbol, count = atom_count
                reactant_counts[symbol] = reactant_counts.get(symbol, 0) + count * coeff
        
        offset = len(self.reactants)
        for i, mol in enumerate(self.products):
            idx = offset + i
            coeff = self.coefficients[idx] if idx < len(self.coefficients) else 1
            for atom_count in mol.get_atom_count().items():
                symbol, count = atom_count
                product_counts[symbol] = product_counts.get(symbol, 0) + count * coeff
        
        return reactant_counts == product_counts


class ChemicalConstants:
    """Physical constants used in chemistry calculations."""
    
    AVOGADRO_NUMBER = 6.02214076e23
    PLANCK_CONSTANT = 6.62607015e-34
    BOLTZMANN_CONSTANT = 1.380649e-23
    GAS_CONSTANT = 8.314462618  # J/mol·K
    FARADAY_CONSTANT = 96485.33212  # C/mol
    IDEAL_GAS_VOLUME = 22.414  # L/mol at STP
    SPEED_OF_LIGHT = 2.99792458e8  # m/s
    ELEMENTARY_CHARGE = 1.602176634e-19  # C
    
    @classmethod
    def moles_to_particles(cls, moles: float) -> float:
        """Convert moles to number of particles."""
        return moles * cls.AVOGADRO_NUMBER
    
    @classmethod
    def particles_to_moles(cls, particles: float) -> float:
        """Convert number of particles to moles."""
        return particles / cls.AVOGADRO_NUMBER
    
    @classmethod
    def molarity_to_parts_per_million(cls, molarity: float, molar_mass: float) -> float:
        """Convert molarity to ppm."""
        return molarity * molar_mass * 1000


class UnitConverter:
    """Unit conversion utilities for chemistry."""
    
    @staticmethod
    def celsius_to_kelvin(celsius: float) -> float:
        """Convert Celsius to Kelvin."""
        return celsius + 273.15
    
    @staticmethod
    def kelvin_to_celsius(kelvin: float) -> float:
        """Convert Kelvin to Celsius."""
        return kelvin - 273.15
    
    @staticmethod
    def atm_to_pascal(atm: float) -> float:
        """Convert atm to Pascal."""
        return atm * 101325
    
    @staticmethod
    def joules_to_kilojoules(joules: float) -> float:
        """Convert joules to kilojoules."""
        return joules / 1000
    
    @staticmethod
    def kcal_to_kilojoules(kcal: float) -> float:
        """Convert kilocalories to kilojoules."""
        return kcal * 4.184
    
    @staticmethod
    def liters_to_cubic_meters(liters: float) -> float:
        """Convert liters to cubic meters."""
        return liters / 1000
    
    @staticmethod
    def amu_to_grams(amu: float) -> float:
        """Convert atomic mass units to grams."""
        return amu * 1.66054e-24


class StoichiometryCalculator:
    """Calculator for stoichiometric calculations."""
    
    @staticmethod
    def calculate_moles(mass: float, molar_mass: float) -> float:
        """Calculate moles from mass and molar mass."""
        return mass / molar_mass if molar_mass > 0 else 0
    
    @staticmethod
    def calculate_mass(moles: float, molar_mass: float) -> float:
        """Calculate mass from moles and molar mass."""
        return moles * molar_mass
    
    @staticmethod
    def calculate_molar_mass(formula: str) -> float:
        """Calculate molar mass from chemical formula."""
        # Simple parser for formulas like H2O, C6H12O6
        total_mass = 0.0
        i = 0
        while i < len(formula):
            if formula[i].isupper():
                # Element symbol
                symbol = formula[i]
                i += 1
                # Check for lowercase letter
                if i < len(formula) and formula[i].islower():
                    symbol += formula[i]
                    i += 1
                # Check for count
                count = 1
                if i < len(formula) and formula[i].isdigit():
                    count_str = ""
                    while i < len(formula) and formula[i].isdigit():
                        count_str += formula[i]
                        i += 1
                    count = int(count_str)
                total_mass += ElementData.get_atomic_mass(symbol) * count
            else:
                i += 1
        return total_mass
    
    @staticmethod
    def calculate_limiting_reagent(
        mole_ratios: List[float],
        available_moles: List[float]
    ) -> Tuple[int, float]:
        """
        Identify the limiting reagent.
        
        Returns:
            Tuple of (index of limiting reagent, excess moles of others)
        """
        if len(mole_ratios) != len(available_moles) or not mole_ratios:
            return (-1, 0)
        
        # Calculate how many reactions each reagent can support
        max_reactions = []
        for ratio, available in zip(mole_ratios, available_moles):
            if ratio > 0:
                max_reactions.append(available / ratio)
            else:
                max_reactions.append(float('inf'))
        
        limiting_index = max_reactions.index(min(max_reactions))
        return (limiting_index, min(max_reactions))
    
    @staticmethod
    def calculate_percent_yield(actual_yield: float, theoretical_yield: float) -> float:
        """Calculate percent yield."""
        if theoretical_yield == 0:
            return 0
        return (actual_yield / theoretical_yield) * 100
    
    @staticmethod
    def calculate_theoretical_yield(
        limiting_moles: float,
        mole_ratio_product: float,
        molar_mass_product: float
    ) -> float:
        """Calculate theoretical yield in grams."""
        moles_product = limiting_moles * mole_ratio_product
        return moles_product * molar_mass_product


class PHCalculator:
    """Calculator for acid-base calculations."""
    
    @staticmethod
    def calculate_ph(concentration: float) -> float:
        """Calculate pH from concentration."""
        if concentration <= 0:
            return 7.0
        return -math.log10(concentration)
    
    @staticmethod
    def calculate_poh(concentration: float) -> float:
        """Calculate pOH from concentration."""
        if concentration <= 0:
            return 7.0
        return -math.log10(concentration)
    
    @staticmethod
    def calculate_ph_from_poh(poh: float) -> float:
        """Calculate pH from pOH."""
        return 14.0 - poh
    
    @staticmethod
    def calculate_concentration_from_ph(ph: float) -> float:
        """Calculate [H+] from pH."""
        return 10 ** (-ph)
    
    @staticmethod
    def calculate_ka_from_ph(ph: float, acid_concentration: float) -> float:
        """Calculate Ka from pH and acid concentration."""
        h_conc = PHCalculator.calculate_concentration_from_ph(ph)
        return h_conc ** 2 / (acid_concentration - h_conc)
    
    @staticmethod
    def calculate_oh_concentration_from_ph(ph: float) -> float:
        """Calculate [OH-] from pH."""
        return 10 ** (ph - 14)


class ElectrochemistryCalculator:
    """Calculator for electrochemical cells."""
    
    @staticmethod
    def calculate_cell_potential(
        reduction_potential_anode: float,
        reduction_potential_cathode: float
    ) -> float:
        """Calculate cell potential."""
        return reduction_potential_cathode - reduction_potential_anode
    
    @staticmethod
    def calculate_gibbs_free_energy(
        cell_potential: float,
        moles_of_electrons: int
    ) -> float:
        """Calculate Gibbs free energy from cell potential."""
        return -moles_of_electrons * ChemicalConstants.FARADAY_CONSTANT * cell_potential / 1000
    
    @staticmethod
    def calculate_nernst_equation(
        cell_potential_standard: float,
        reaction_quotient: float,
        temperature: float,
        moles_of_electrons: int
    ) -> float:
        """Calculate cell potential using Nernst equation."""
        R = ChemicalConstants.GAS_CONSTANT
        E = cell_potential_standard - (R * temperature / (moles_of_electrons * ChemicalConstants.FARADAY_CONSTANT)) * math.log(reaction_quotient)
        return E


@dataclass
class ReactionAnimationConfig:
    """Configuration for reaction animations."""
    duration_ms: int = 2000
    easing_function: str = "ease_in_out"
    show_transition_state: bool = True
    show_energy_diagram: bool = True
    particle_effects: bool = True
    color_highlighting: bool = True


@dataclass
class MoleculeVisualConfig:
    """Configuration for molecular visualization."""
    render_style: str = "ball_and_stick"
    atom_scale: float = 1.0
    bond_thickness: float = 0.1
    show_hydrogens: bool = True
    show_bond_orders: bool = True
    background_color: str = "#1a1a2e"
    ambient_light_intensity: float = 0.5
    point_light_intensity: float = 1.0


__all__ = [
    "ElementSymbol",
    "BondType",
    "HybridizationType",
    "ReactionType",
    "Phase",
    "ElementData",
    "Vector3D",
    "Atom",
    "Bond",
    "Molecule",
    "ChemicalReaction",
    "ChemicalConstants",
    "UnitConverter",
    "StoichiometryCalculator",
    "PHCalculator",
    "ElectrochemistryCalculator",
    "ReactionAnimationConfig",
    "MoleculeVisualConfig"
]
