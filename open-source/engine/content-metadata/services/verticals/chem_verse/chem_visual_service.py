"""
ChemVerse Visual Service

This module provides molecular visualization and rendering services for the
VisualVerse chemistry learning platform. It handles 3D rendering, structure
display, and visual configuration for chemical compounds.

Author: MiniMax Agent
Version: 1.0.0
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any
from enum import Enum
from .chem_core import (
    Atom, Bond, Molecule, Vector3D, BondType, Phase,
    ElementData, MoleculeVisualConfig
)


class RenderStyle(str, Enum):
    """Styles for rendering molecules."""
    BALL_AND_STICK = "ball_and_stick"
    SPACE_FILLING = "space_filling"
    WIREFRAME = "wireframe"
    LINE = "line"
    CARTOON = "cartoon"


class ColorScheme(str, Enum):
    """Color schemes for molecular visualization."""
    CPK = "cpk"
    RAMA = "rama"
    CHARGE = "charge"
    ELEMENT = "element"
    CUSTOM = "custom"


class VectorDisplayStyle(str, Enum):
    """Styles for displaying vectors."""
    ARROW = "arrow"
    LINE = "line"
    CONE = "cone"


@dataclass
class AtomVisual:
    """Visual representation of an atom."""
    atom: Atom
    radius: float
    color: Tuple[int, int, int]
    opacity: float = 1.0
    label: str = ""
    is_highlighted: bool = False
    
    @classmethod
    def from_atom(
        cls,
        atom: Atom,
        style: RenderStyle = RenderStyle.BALL_AND_STICK,
        custom_radius: float = None
    ) -> 'AtomVisual':
        """Create atom visual from atom data."""
        # Set radius based on style
        if custom_radius:
            radius = custom_radius
        elif style == RenderStyle.SPACE_FILLING:
            # Van der Waals radius
            data = ElementData.get_data(atom.element_symbol)
            radius = (data["van_der_waals_radius"] / 100 if data else 1.2)
        else:
            # Covalent radius (scaled for ball-and-stick)
            data = ElementData.get_data(atom.element_symbol)
            radius = (data["covalent_radius"] / 200 if data else 0.4)
        
        return cls(
            atom=atom,
            radius=radius,
            color=atom.color_rgb,
            label=atom.element_symbol
        )


@dataclass
class BondVisual:
    """Visual representation of a bond."""
    bond: Bond
    start_position: Vector3D
    end_position: Vector3D
    thickness: float
    color: Tuple[int, int, int]
    order: int = 1
    is_highlighted: bool = False
    
    @classmethod
    def from_bond(
        cls,
        bond: Bond,
        atom1_pos: Vector3D,
        atom2_pos: Vector3D,
        style: RenderStyle = RenderStyle.BALL_AND_STICK
    ) -> 'BondVisual':
        """Create bond visual from bond data."""
        # Set thickness based on bond order and style
        base_thickness = 0.1 if style == RenderStyle.BALL_AND_STICK else 0.05
        thickness = base_thickness * (1 + bond.order * 0.3)
        
        # Set color based on bond type
        if bond.bond_type == BondType.IONIC:
            color = (255, 255, 0)  # Yellow for ionic
        elif bond.bond_type == BondType.HYDROGEN:
            color = (200, 200, 200)  # Light gray for hydrogen
        else:
            color = (150, 150, 150)  # Gray for covalent
        
        return cls(
            bond=bond,
            start_position=atom1_pos,
            end_position=atom2_pos,
            thickness=thickness,
            color=color,
            order=bond.order
        )


@dataclass
class MoleculeVisual:
    """Complete visual representation of a molecule."""
    molecule: Molecule
    atom_visuals: List[AtomVisual] = field(default_factory=list)
    bond_visuals: List[BondVisual] = field(default_factory=list)
    center: Vector3D = field(default_factory=lambda: Vector3D(0, 0, 0))
    scale: float = 1.0
    bounding_box: Tuple[Vector3D, Vector3D] = (
        Vector3D(0, 0, 0), Vector3D(0, 0, 0)
    )
    
    @classmethod
    def from_molecule(
        cls,
        molecule: Molecule,
        style: RenderStyle = RenderStyle.BALL_AND_STICK,
        config: MoleculeVisualConfig = None
    ) -> 'MoleculeVisual':
        """Create molecule visual from molecule data."""
        atom_visuals = []
        bond_visuals = []
        
        # Create atom visuals
        for atom in molecule.atoms:
            atom_visuals.append(AtomVisual.from_atom(atom, style))
        
        # Create bond visuals
        for bond in molecule.bonds:
            atom1 = molecule.get_atom_by_id(bond.atom1_id)
            atom2 = molecule.get_atom_by_id(bond.atom2_id)
            if atom1 and atom2:
                bond_visuals.append(BondVisual.from_bond(
                    bond, atom1.position, atom2.position, style
                ))
        
        # Calculate center
        center = molecule.get_center_of_mass()
        
        # Calculate bounding box
        if molecule.atoms:
            min_pos = Vector3D(
                min(a.position.x for a in molecule.atoms),
                min(a.position.y for a in molecule.atoms),
                min(a.position.z for a in molecule.atoms)
            )
            max_pos = Vector3D(
                max(a.position.x for a in molecule.atoms),
                max(a.position.y for a in molecule.atoms),
                max(a.position.z for a in molecule.atoms)
            )
            bounding_box = (min_pos, max_pos)
        else:
            bounding_box = (Vector3D(0, 0, 0), Vector3D(0, 0, 0))
        
        return cls(
            molecule=molecule,
            atom_visuals=atom_visuals,
            bond_visuals=bond_visuals,
            center=center,
            bounding_box=bounding_box
        )
    
    def get_rotation_matrix(self) -> List[List[float]]:
        """Get rotation matrix for the molecule."""
        # Returns identity matrix - actual rotation handled by renderer
        return [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    
    def get_view_transform(self) -> Dict[str, Any]:
        """Get transformation data for viewing."""
        return {
            "center": {"x": self.center.x, "y": self.center.y, "z": self.center.z},
            "scale": self.scale,
            "bounding_box": [
                {"x": self.bounding_box[0].x, "y": self.bounding_box[0].y, "z": self.bounding_box[0].z},
                {"x": self.bounding_box[1].x, "y": self.bounding_box[1].y, "z": self.bounding_box[1].z}
            ]
        }


@dataclass
class VectorField:
    """Represents a vector field for force or field visualization."""
    vectors: Dict[str, Tuple[Vector3D, Vector3D]] = field(default_factory=dict)
    color: Tuple[int, int, int] = (255, 100, 100)
    scale: float = 1.0
    arrow_head_size: float = 0.2
    
    def add_vector(
        self,
        position: Vector3D,
        direction: Vector3D,
        label: str = ""
    ) -> None:
        """Add a vector to the field."""
        self.vectors[label] = (position, direction)
    
    def get_vector_data(self) -> List[Dict[str, Any]]:
        """Get vector data for rendering."""
        result = []
        for label, (start, end) in self.vectors.items():
            result.append({
                "label": label,
                "start": {"x": start.x, "y": start.y, "z": start.z},
                "end": {"x": end.x, "y": end.y, "z": end.z},
                "color": list(self.color),
                "scale": self.scale,
                "arrow_head_size": self.arrow_head_size
            })
        return result


@dataclass
class ElectronOrbital:
    """Represents an electron orbital for visualization."""
    orbital_type: str  # s, p, d, f
    quantum_numbers: Dict[str, int]
    position: Vector3D
    phase_color_positive: Tuple[int, int, int] = (255, 100, 100)
    phase_color_negative: Tuple[int, int, int] = (100, 100, 255)
    opacity: float = 0.6
    
    def get_orbital_shape(self) -> Dict[str, Any]:
        """Get orbital shape data for rendering."""
        return {
            "type": self.orbital_type,
            "quantum_numbers": self.quantum_numbers,
            "position": {"x": self.position.x, "y": self.position.y, "z": self.position.z},
            "colors": [self.phase_color_positive, self.phase_color_negative],
            "opacity": self.opacity
        }


@dataclass
class ReactionCoordinateDiagram:
    """Represents an energy diagram for reaction progress."""
    reaction_name: str
    reactant_energy: float
    product_energy: float
    activation_energy: float
    intermediate_energy: Optional[float] = None
    labels: Dict[str, str] = field(default_factory=dict)
    
    def get_diagram_data(self) -> Dict[str, Any]:
        """Get diagram data for rendering."""
        data = {
            "reaction_name": self.reaction_name,
            "reactant_energy": self.reactant_energy,
            "product_energy": self.product_energy,
            "activation_energy": self.activation_energy,
            "labels": self.labels
        }
        if self.intermediate_energy:
            data["intermediate_energy"] = self.intermediate_energy
        return data


class MoleculeRenderer:
    """Handles the rendering of molecular structures."""
    
    def __init__(self, config: MoleculeVisualConfig = None):
        """Initialize the renderer with configuration."""
        self.config = config or MoleculeVisualConfig()
    
    def render(
        self,
        molecule: Molecule,
        style: RenderStyle = RenderStyle.BALL_AND_STICK
    ) -> MoleculeVisual:
        """Render a molecule with the specified style."""
        return MoleculeVisual.from_molecule(molecule, style, self.config)
    
    def render_multiple(
        self,
        molecules: List[Molecule],
        style: RenderStyle = RenderStyle.BALL_AND_STICK
    ) -> List[MoleculeVisual]:
        """Render multiple molecules."""
        return [self.render(mol, style) for mol in molecules]
    
    def get_render_data(self, visual: MoleculeVisual) -> Dict[str, Any]:
        """Get complete render data for a molecule visual."""
        atoms_data = []
        for atom_visual in visual.atom_visuals:
            atoms_data.append({
                "id": atom_visual.atom.id,
                "element": atom_visual.atom.element_symbol,
                "position": {
                    "x": atom_visual.atom.position.x,
                    "y": atom_visual.atom.position.y,
                    "z": atom_visual.atom.position.z
                },
                "radius": atom_visual.radius,
                "color": list(atom_visual.color),
                "opacity": atom_visual.opacity,
                "label": atom_visual.label,
                "is_highlighted": atom_visual.is_highlighted
            })
        
        bonds_data = []
        for bond_visual in visual.bond_visuals:
            bonds_data.append({
                "id": bond_visual.bond.id,
                "atom1": bond_visual.bond.atom1_id,
                "atom2": bond_visual.bond.atom2_id,
                "start": {
                    "x": bond_visual.start_position.x,
                    "y": bond_visual.start_position.y,
                    "z": bond_visual.start_position.z
                },
                "end": {
                    "x": bond_visual.end_position.x,
                    "y": bond_visual.end_position.y,
                    "z": bond_visual.end_position.z
                },
                "thickness": bond_visual.thickness,
                "color": list(bond_visual.color),
                "order": bond_visual.order,
                "is_highlighted": bond_visual.is_highlighted
            })
        
        return {
            "molecule_id": visual.molecule.id,
            "molecule_name": visual.molecule.name,
            "formula": visual.molecule.get_formula(),
            "molecular_weight": visual.molecule.get_molecular_weight(),
            "atoms": atoms_data,
            "bonds": bonds_data,
            "center": {"x": visual.center.x, "y": visual.center.y, "z": visual.center.z},
            "bounding_box": [
                {"x": visual.bounding_box[0].x, "y": visual.bounding_box[0].y, "z": visual.bounding_box[0].z},
                {"x": visual.bounding_box[1].x, "y": visual.bounding_box[1].y, "z": visual.bounding_box[1].z}
            ],
            "scale": visual.scale
        }
    
    def highlight_atoms(
        self,
        visual: MoleculeVisual,
        atom_ids: List[str],
        color: Tuple[int, int, int] = (255, 255, 0)
    ) -> MoleculeVisual:
        """Highlight specific atoms in the visual."""
        for atom_visual in visual.atom_visuals:
            if atom_visual.atom.id in atom_ids:
                atom_visual.is_highlighted = True
                atom_visual.color = color
                atom_visual.opacity = 1.0
        return visual
    
    def highlight_bonds(
        self,
        visual: MoleculeVisual,
        bond_ids: List[str],
        color: Tuple[int, int, int] = (255, 255, 0)
    ) -> MoleculeVisual:
        """Highlight specific bonds in the visual."""
        for bond_visual in visual.bond_visuals:
            if bond_visual.bond.id in bond_ids:
                bond_visual.is_highlighted = True
                bond_visual.color = color
        return visual
    
    def focus_on_atom(
        self,
        visual: MoleculeVisual,
        atom_id: str,
        padding: float = 2.0
    ) -> Dict[str, Any]:
        """Get camera focus data for a specific atom."""
        atom_visual = None
        for av in visual.atom_visuals:
            if av.atom.id == atom_id:
                atom_visual = av
                break
        
        if not atom_visual:
            return {"error": "Atom not found"}
        
        atom_pos = atom_visual.atom.position
        return {
            "target": {"x": atom_pos.x, "y": atom_pos.y, "z": atom_pos.z},
            "padding": padding,
            "radius": atom_visual.radius + padding
        }
    
    def get_2d_projection(
        self,
        visual: MoleculeVisual,
        projection_type: str = "perspective"
    ) -> List[Dict[str, Any]]:
        """Get 2D projection data for the molecule."""
        projected_atoms = []
        for atom_visual in visual.atom_visuals:
            pos = atom_visual.atom.position
            projected_atoms.append({
                "id": atom_visual.atom.id,
                "element": atom_visual.atom.element_symbol,
                "x_2d": pos.x,
                "y_2d": pos.y,
                "z_depth": pos.z,
                "radius": atom_visual.radius,
                "color": list(atom_visual.color)
            })
        return projected_atoms


class StructureComparator:
    """Compares and analyzes molecular structures."""
    
    @staticmethod
    def compare_structures(
        mol1: Molecule,
        mol2: Molecule
    ) -> Dict[str, Any]:
        """Compare two molecular structures."""
        formula1 = mol1.get_formula()
        formula2 = mol2.get_formula()
        
        atoms1 = mol1.get_atom_count()
        atoms2 = mol2.get_atom_count()
        
        bond_count1 = len(mol1.bonds)
        bond_count2 = len(mol2.bonds)
        
        return {
            "formulas_match": formula1 == formula2,
            "formula1": formula1,
            "formula2": formula2,
            "atom_counts_match": atoms1 == atoms2,
            "atoms1": atoms1,
            "atoms2": atoms2,
            "bond_count1": bond_count1,
            "bond_count2": bond_count2,
            "molecular_weight1": mol1.get_molecular_weight(),
            "molecular_weight2": mol2.get_molecular_weight(),
            "isomers": formula1 == formula2 and mol1.id != mol2.id
        }
    
    @staticmethod
    def find_similarities(
        mol1: Molecule,
        mol2: Molecule
    ) -> Dict[str, Any]:
        """Find structural similarities between molecules."""
        common_elements = set(mol1.get_atom_count().keys()) & \
                         set(mol2.get_atom_count().keys())
        
        return {
            "common_elements": list(common_elements),
            "similarity_score": len(common_elements) / max(
                len(mol1.get_atom_count()),
                len(mol2.get_atom_count())
            )
        }


class ChemVerseVisualService:
    """
    Service for molecular visualization and rendering.
    
    This service provides comprehensive visualization capabilities for
    chemical structures, including 3D rendering, style options, and
    interactive display features.
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        """Initialize the visual service."""
        self.config = config or {}
        self.renderer = MoleculeRenderer()
        self._molecule_cache: Dict[str, MoleculeVisual] = {}
    
    def configure(self, config: Dict[str, Any]) -> None:
        """Configure the service with custom settings."""
        self.config.update(config)
        if "default_style" in config:
            self._default_style = RenderStyle(config["default_style"])
    
    def render_molecule(
        self,
        molecule: Molecule,
        style: str = "ball_and_stick"
    ) -> Dict[str, Any]:
        """Render a molecule and return visualization data."""
        render_style = RenderStyle(style)
        visual = self.renderer.render(molecule, render_style)
        self._molecule_cache[molecule.id] = visual
        return self.renderer.get_render_data(visual)
    
    def render_multiple_molecules(
        self,
        molecules: List[Molecule],
        style: str = "ball_and_stick"
    ) -> List[Dict[str, Any]]:
        """Render multiple molecules."""
        render_style = RenderStyle(style)
        visuals = self.renderer.render_multiple(molecules, render_style)
        return [self.renderer.get_render_data(v) for v in visuals]
    
    def create_vector_field(
        self,
        positions: List[Vector3D],
        directions: List[Vector3D],
        labels: List[str] = None
    ) -> VectorField:
        """Create a vector field for visualization."""
        field = VectorField()
        labels = labels or [f"vec_{i}" for i in range(len(positions))]
        for pos, direction, label in zip(positions, directions, labels):
            field.add_vector(pos, direction, label)
        return field
    
    def create_orbital(
        self,
        orbital_type: str,
        position: Vector3D,
        n: int = 1,
        l: int = 0,
        m: int = 0
    ) -> ElectronOrbital:
        """Create an electron orbital for visualization."""
        return ElectronOrbital(
            orbital_type=orbital_type,
            quantum_numbers={"n": n, "l": l, "m": m},
            position=position
        )
    
    def create_reaction_energy_diagram(
        self,
        reactant_energy: float,
        product_energy: float,
        activation_energy: float,
        reaction_name: str = "Reaction",
        intermediate_energy: float = None
    ) -> ReactionCoordinateDiagram:
        """Create a reaction coordinate diagram."""
        return ReactionCoordinateDiagram(
            reaction_name=reaction_name,
            reactant_energy=reactant_energy,
            product_energy=product_energy,
            activation_energy=activation_energy,
            intermediate_energy=intermediate_energy,
            labels={
                "reactants": "Reactants",
                "products": "Products",
                "activation": "Activation Energy"
            }
        )
    
    def compare_structures(
        self,
        molecule1: Molecule,
        molecule2: Molecule
    ) -> Dict[str, Any]:
        """Compare two molecular structures."""
        return StructureComparator.compare_structures(molecule1, molecule2)
    
    def highlight_substructure(
        self,
        molecule: Molecule,
        atom_ids: List[str],
        bond_ids: List[str] = None,
        color: Tuple[int, int, int] = (255, 200, 50)
    ) -> Dict[str, Any]:
        """Highlight a substructure within a molecule."""
        render_style = RenderStyle(self.config.get("default_style", "ball_and_stick"))
        visual = self.renderer.render(molecule, render_style)
        self.renderer.highlight_atoms(visual, atom_ids, color)
        if bond_ids:
            self.renderer.highlight_bonds(visual, bond_ids, color)
        return self.renderer.get_render_data(visual)
    
    def get_camera_settings(
        self,
        molecule: Molecule,
        atom_id: str = None
    ) -> Dict[str, Any]:
        """Get camera settings for viewing a molecule."""
        render_style = RenderStyle(self.config.get("default_style", "ball_and_stick"))
        visual = self.renderer.render(molecule, render_style)
        
        if atom_id:
            return self.renderer.focus_on_atom(visual, atom_id)
        
        return {
            "target": {"x": visual.center.x, "y": visual.center.y, "z": visual.center.z},
            "padding": 5.0,
            "radius": 10.0
        }
    
    def export_visual_data(
        self,
        molecule: Molecule,
        format: str = "json"
    ) -> str:
        """Export visualization data in the specified format."""
        render_style = RenderStyle(self.config.get("default_style", "ball_and_stick"))
        visual = self.renderer.render(molecule, render_style)
        data = self.renderer.get_render_data(visual)
        
        if format == "json":
            return json.dumps(data, indent=2)
        elif format == "dict":
            return data
        else:
            return str(data)


def create_chem_visual_service(config: dict = None) -> ChemVerseVisualService:
    """
    Create a ChemVerseVisualService instance.
    
    Args:
        config: Optional configuration dictionary
        
    Returns:
        Configured ChemVerseVisualService instance
    """
    service = ChemVerseVisualService(config)
    return service


__all__ = [
    "RenderStyle",
    "ColorScheme",
    "VectorDisplayStyle",
    "AtomVisual",
    "BondVisual",
    "MoleculeVisual",
    "VectorField",
    "ElectronOrbital",
    "ReactionCoordinateDiagram",
    "MoleculeRenderer",
    "StructureComparator",
    "ChemVerseVisualService",
    "create_chem_visual_service"
]
