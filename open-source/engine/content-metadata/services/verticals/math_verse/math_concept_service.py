"""
MathVerse Concept Service

This module provides the MathVerse-specific concept service implementation,
extending the base concept service with mathematical domain functionality
including formula processing, mathematical validation, and concept relationship
handling for algebraic, calculus, linear algebra, probability, and proof concepts.

Licensed under the Apache License, Version 2.0
"""

from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from datetime import datetime
import re
import logging

from ..extensions.service_extension_base import (
    ConceptServiceExtension,
    ExtensionContext
)

logger = logging.getLogger(__name__)


@dataclass
class MathConceptMetadata:
    """Additional metadata for mathematical concepts."""
    formula: Optional[str] = None
    formula_latex: Optional[str] = None
    variables: List[str] = None
    domain: str = "general"
    subdomain: Optional[str] = None
    proof_type: Optional[str] = None
    difficulty_score: float = 0.5
    prerequisites_math: List[str] = None
    related_formulas: List[str] = None
    visual_types_preferred: List[str] = None
    calculation_procedure: Optional[str] = None
    example_problems: List[Dict[str, Any]] = None


class MathVerseConceptService:
    """
    MathVerse-specific concept service.
    
    This service handles mathematical concept processing including:
    - Formula parsing and validation
    - Mathematical relationship detection
    - Proof structure analysis
    - Difficulty scoring for mathematical concepts
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the MathVerse concept service.
        
        Args:
            config: Optional configuration dictionary
        """
        self.config = config or {}
        self._formula_patterns = self._compile_formula_patterns()
        self._operator_precedence = self._build_operator_precedence()
        
    def _compile_formula_patterns(self) -> Dict[str, re.Pattern]:
        """Compile regex patterns for formula analysis."""
        return {
            'fraction': re.compile(r'\\frac\{[^}]+\}\{[^}]+\}'),
            'integral': re.compile(r'\\int_[a-zA-Z0-9]+(\^[a-zA-Z0-9]+)?\s*[a-zA-Z]'),
            'derivative': re.compile(r'\\frac\{d[a-zA-Z]\}\{d[a-zA-Z]\}'),
            'sqrt': re.compile(r'\\sqrt\[[^\]]*\]?\{[^}]+\}'),
            'sum': re.compile(r'\\sum_\{[^}]+\}(\^[^\}]+)?'),
            'limit': re.compile(r'\\lim_\{[^}]+\}'),
            'matrix': re.compile(r'\\begin\{[a-zA-Z]+\}.*?\\end\{[a-zA-Z]+\}', re.DOTALL),
            'greek': re.compile(r'\\[a-zA-Z]+'),
            'variable': re.compile(r'\\?[a-zA-Z][a-zA-Z0-9]*'),
            'exponent': re.compile(r'\^[0-9+-]+'),
            'subscript': re.compile(r'_[0-9]+'),
        }
    
    def _build_operator_precedence(self) -> Dict[str, int]:
        """Build operator precedence for mathematical expressions."""
        return {
            '+': 1,
            '-': 1,
            '*': 2,
            '/': 2,
            '^': 3,
            'sqrt': 4,
            'fraction': 4,
            'integral': 5,
            'derivative': 5,
        }
    
    def process_concept(
        self,
        concept: Dict[str, Any],
        context: Optional[ExtensionContext] = None
    ) -> Dict[str, Any]:
        """
        Process a mathematical concept with domain-specific logic.
        
        Args:
            concept: The concept to process
            context: Optional execution context
            
        Returns:
            Processed concept with enhanced mathematical metadata
        """
        # Create a copy to avoid modifying original
        processed = concept.copy()
        
        # Add mathematical metadata
        math_metadata = MathConceptMetadata(
            variables=self._extract_variables(concept),
            formula=concept.get('formula'),
            formula_latex=self._render_latex(concept.get('formula')),
            domain=concept.get('math_domain', 'general'),
            subdomain=concept.get('math_subdomain'),
            difficulty_score=concept.get('difficulty_score', 0.5),
            visual_types_preferred=concept.get('visualization_preferences', []),
            example_problems=concept.get('example_problems', [])
        )
        
        # Process based on concept type
        concept_type = concept.get('concept_type', 'definition')
        
        if concept_type == 'formula':
            math_metadata.calculation_procedure = self._describe_procedure(concept)
        elif concept_type == 'proof':
            math_metadata.proof_type = self._determine_proof_type(concept)
        
        # Add processed metadata to concept
        processed['_math_metadata'] = {
            'formula': math_metadata.formula,
            'formula_latex': math_metadata.formula_latex,
            'variables': math_metadata.variables,
            'domain': math_metadata.domain,
            'subdomain': math_metadata.subdomain,
            'proof_type': math_metadata.proof_type,
            'difficulty_score': math_metadata.difficulty_score,
            'prerequisites_math': math_metadata.prerequisites_math,
            'visual_types': math_metadata.visual_types_preferred,
            'calculation_procedure': math_metadata.calculation_procedure,
            'example_problems': math_metadata.example_problems
        }
        
        # Generate display representation
        processed['_display'] = self._generate_display_representation(concept)
        
        # Validate mathematical content
        processed['_validation'] = self._validate_math_content(concept)
        
        return processed
    
    def validate_concept(self, concept: Dict[str, Any]) -> List[str]:
        """
        Validate a mathematical concept against domain rules.
        
        Args:
            concept: The concept to validate
            
        Returns:
            List of validation errors (empty if valid)
        """
        errors = []
        
        # Check for required fields based on concept type
        concept_type = concept.get('concept_type', 'definition')
        
        if concept_type == 'formula':
            if not concept.get('formula') and not concept.get('description'):
                errors.append("Formula concepts must have either a formula or description")
            if concept.get('formula'):
                if not self._validate_formula_syntax(concept['formula']):
                    errors.append("Formula has invalid syntax")
        
        elif concept_type == 'proof':
            if not concept.get('proof_structure'):
                errors.append("Proof concepts must have proof_structure defined")
            if concept.get('proof_type') not in ['direct', 'induction', 'contradiction', 'counterexample', 'construction']:
                errors.append("Invalid proof_type specified")
        
        elif concept_type == 'definition':
            if not concept.get('description'):
                errors.append("Definition concepts must have a description")
        
        # Check difficulty score range
        if 'difficulty_score' in concept:
            if not 0 <= concept['difficulty_score'] <= 1:
                errors.append("Difficulty score must be between 0 and 1")
        
        # Validate mathematical expressions in description
        if 'description' in concept:
            math_errors = self._check_math_expression_errors(concept['description'])
            errors.extend(math_errors)
        
        # Check for circular prerequisites
        prerequisites = concept.get('prerequisites', [])
        if concept.get('id') in prerequisites:
            errors.append("Concept cannot be a prerequisite of itself")
        
        return errors
    
    def get_related_concepts(
        self,
        concept_id: str,
        relationship_type: str
    ) -> List[str]:
        """
        Get related concepts with domain-specific relationships.
        
        Args:
            concept_id: The source concept
            relationship_type: Type of relationship
            
        Returns:
            List of related concept IDs
        """
        # This would typically query a knowledge graph
        # For now, return common mathematical relationships
        relationships = {
            'prerequisite_for': [
                'linear-equations' for 'variables',
                'quadratic-equations' for 'linear-equations',
                'systems-equations' for 'quadratic-equations',
            ],
            'uses': [
                'variables' for 'expressions',
                'expressions' for 'equations',
                'functions' for 'derivatives',
            ],
            'generalizes': [
                'functions' for 'linear-functions',
                'functions' for 'quadratic-functions',
            ],
            'specializes': [
                'linear-functions' for 'functions',
                'quadratic-functions' for 'functions',
            ],
            'related_theorems': [
                'fundamental-theorem' for 'derivatives',
                'fundamental-theorem' for 'integrals',
            ],
        }
        
        return relationships.get(relationship_type, [])
    
    def analyze_difficulty(
        self,
        concept: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Analyze the difficulty of a mathematical concept.
        
        Args:
            concept: The concept to analyze
            
        Returns:
            Difficulty analysis results
        """
        factors = []
        base_score = 0.5
        
        # Factor 1: Concept type
        concept_type = concept.get('concept_type', 'definition')
        type_scores = {
            'definition': 0.0,
            'formula': 0.1,
            'procedure': 0.15,
            'proof': 0.25,
            'theorem': 0.2,
        }
        base_score += type_scores.get(concept_type, 0.0)
        
        # Factor 2: Mathematical complexity
        formula = concept.get('formula', '')
        formula_complexity = self._assess_formula_complexity(formula)
        base_score += formula_complexity * 0.3
        
        # Factor 3: Number of prerequisites
        prerequisites = len(concept.get('prerequisites', []))
        base_score += min(prerequisites * 0.05, 0.2)
        
        # Factor 4: Domain-specific factors
        domain = concept.get('math_domain', 'general')
        domain_factors = {
            'algebra': 0.0,
            'calculus': 0.1,
            'linear-algebra': 0.15,
            'probability': 0.05,
            'proofs': 0.15,
        }
        base_score += domain_factors.get(domain, 0.0)
        
        return {
            'overall_score': min(base_score, 1.0),
            'factors': factors,
            'level': self._score_to_level(min(base_score, 1.0)),
            'estimated_hours': self._score_to_hours(base_score)
        }
    
    def decompose_proof(
        self,
        proof_concept: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Decompose a proof concept into steps.
        
        Args:
            proof_concept: The proof concept to decompose
            
        Returns:
            List of proof steps with analysis
        """
        steps = []
        proof_type = proof_concept.get('proof_type', 'direct')
        structure = proof_concept.get('proof_structure', {})
        
        if proof_type == 'direct':
            steps = self._decompose_direct_proof(structure)
        elif proof_type == 'induction':
            steps = self._decompose_induction_proof(structure)
        elif proof_type == 'contradiction':
            steps = self._decompose_contradiction_proof(structure)
        elif proof_type == 'counterexample':
            steps = self._decompose_counterexample_proof(structure)
        
        return steps
    
    def _extract_variables(self, concept: Dict[str, Any]) -> List[str]:
        """Extract variables from a concept."""
        variables = set()
        
        # Extract from formula
        formula = concept.get('formula', '')
        var_pattern = self._formula_patterns['variable']
        matches = var_pattern.findall(formula)
        for match in matches:
            clean_var = match.lstrip('\\')
            if clean_var not in ['frac', 'sqrt', 'int', 'sum', 'lim', 'frac', 'partial', 'nabla']:
                variables.add(clean_var)
        
        # Extract from description
        description = concept.get('description', '')
        for word in description.split():
            if len(word) == 1 and word.isalpha():
                variables.add(word)
        
        return list(variables)
    
    def _render_latex(self, formula: Optional[str]) -> Optional[str]:
        """Render formula to LaTeX if not already in that format."""
        if not formula:
            return None
        if formula.startswith('$$') or formula.startswith('\\'):
            return formula
        return f"$${formula}$$"
    
    def _describe_procedure(self, concept: Dict[str, Any]) -> str:
        """Generate a description of the calculation procedure."""
        formula = concept.get('formula', '')
        description = concept.get('description', '')
        
        # Generate procedural description
        procedure = f"Apply the formula {formula} to calculate the result."
        
        return procedure
    
    def _determine_proof_type(self, concept: Dict[str, Any]) -> str:
        """Determine the type of proof."""
        description = concept.get('description', '').lower()
        
        if 'induction' in description:
            return 'induction'
        elif 'contradiction' in description or 'assume the opposite' in description:
            return 'contradiction'
        elif 'counterexample' in description:
            return 'counterexample'
        elif 'construct' in description or 'existence' in description:
            return 'construction'
        else:
            return 'direct'
    
    def _generate_display_representation(self, concept: Dict[str, Any]) -> Dict[str, Any]:
        """Generate display representation for a concept."""
        return {
            'title': concept.get('name', 'Untitled'),
            'formula': concept.get('formula'),
            'latex': self._render_latex(concept.get('formula')),
            'type': concept.get('concept_type', 'definition'),
            'difficulty': concept.get('difficulty_score', 0.5),
            'domain': concept.get('math_domain', 'general')
        }
    
    def _validate_math_content(self, concept: Dict[str, Any]) -> Dict[str, Any]:
        """Validate mathematical content in a concept."""
        return {
            'is_valid': len(self.validate_concept(concept)) == 0,
            'errors': self.validate_concept(concept),
            'warnings': self._generate_warnings(concept)
        }
    
    def _generate_warnings(self, concept: Dict[str, Any]) -> List[str]:
        """Generate warnings for potential issues."""
        warnings = []
        
        formula = concept.get('formula', '')
        if formula and len(formula) > 200:
            warnings.append("Formula is very long, consider breaking it into steps")
        
        if concept.get('concept_type') == 'proof':
            if not concept.get('example_proofs'):
                warnings.append("Consider adding example proofs")
        
        return warnings
    
    def _validate_formula_syntax(self, formula: str) -> bool:
        """Validate formula syntax."""
        try:
            # Basic syntax checks
            open_braces = formula.count('{') - formula.count('}')
            if open_braces != 0:
                return False
            
            open_parens = formula.count('(') - formula.count(')')
            if open_parens != 0:
                return False
            
            open_brackets = formula.count('[') - formula.count(']')
            if open_brackets != 0:
                return False
            
            return True
        except Exception:
            return False
    
    def _check_math_expression_errors(self, text: str) -> List[str]:
        """Check for common mathematical expression errors in text."""
        errors = []
        
        # Check for unbalanced delimiters
        if text.count('(') != text.count(')'):
            errors.append("Unbalanced parentheses in description")
        
        if text.count('[') != text.count(']'):
            errors.append("Unbalanced brackets in description")
        
        # Check for common mistakes
        if '=' in text and text.count('=') > 1:
            if '≤' not in text and '≥' not in text and '!=' not in text:
                # Multiple equals might indicate equation chain
                pass
        
        return errors
    
    def _assess_formula_complexity(self, formula: str) -> float:
        """Assess the complexity of a formula."""
        if not formula:
            return 0.0
        
        complexity = 0.0
        
        # Count nested fractions
        complexity += formula.count('\\frac') * 0.15
        
        # Count integrals and derivatives
        complexity += formula.count('\\int') * 0.2
        complexity += formula.count('\\frac{d') * 0.2
        complexity += formula.count('\\partial') * 0.2
        
        # Count limits and sums
        complexity += formula.count('\\lim') * 0.15
        complexity += formula.count('\\sum') * 0.15
        complexity += formula.count('\\prod') * 0.15
        
        # Count matrices
        if '\\begin{' in formula:
            complexity += 0.3
        
        # Check for nested structures
        depth = self._calculate_nesting_depth(formula)
        complexity += depth * 0.1
        
        return min(complexity, 1.0)
    
    def _calculate_nesting_depth(self, formula: str) -> int:
        """Calculate maximum nesting depth in a formula."""
        max_depth = 0
        current_depth = 0
        
        for char in formula:
            if char in '{[(':
                current_depth += 1
                max_depth = max(max_depth, current_depth)
            elif char in '}])':
                current_depth -= 1
        
        return max_depth
    
    def _score_to_level(self, score: float) -> str:
        """Convert difficulty score to level name."""
        if score < 0.3:
            return 'foundational'
        elif score < 0.5:
            return 'developing'
        elif score < 0.7:
            return 'proficient'
        elif score < 0.85:
            return 'advanced'
        else:
            return 'expert'
    
    def _score_to_hours(self, score: float) -> float:
        """Convert difficulty score to estimated study hours."""
        return round(1 + score * 10, 1)
    
    def _decompose_direct_proof(self, structure: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Decompose a direct proof into steps."""
        return [
            {'step': 1, 'type': 'hypothesis', 'description': 'State given conditions'},
            {'step': 2, 'type': 'derivation', 'description': 'Apply definitions and axioms'},
            {'step': 3, 'type': 'deduction', 'description': 'Logical deduction steps'},
            {'step': 4, 'type': 'conclusion', 'description': 'State final result'}
        ]
    
    def _decompose_induction_proof(self, structure: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Decompose an induction proof into steps."""
        return [
            {'step': 1, 'type': 'base_case', 'description': 'Prove for initial value (n=0 or n=1)'},
            {'step': 2, 'type': 'inductive_hypothesis', 'description': 'Assume true for n=k'},
            {'step': 3, 'type': 'inductive_step', 'description': 'Prove true for n=k+1'},
            {'step': 4, 'type': 'conclusion', 'description': 'Conclude true for all n'}
        ]
    
    def _decompose_contradiction_proof(self, structure: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Decompose a proof by contradiction into steps."""
        return [
            {'step': 1, 'type': 'negation', 'description': 'Assume the negation of the statement'},
            {'step': 2, 'type': 'derivation', 'description': 'Derive consequences'},
            {'step': 3, 'type': 'contradiction', 'description': 'Reach a contradiction'},
            {'step': 4, 'type': 'conclusion', 'description': 'Original statement must be true'}
        ]
    
    def _decompose_counterexample_proof(self, structure: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Decompose a counterexample proof into steps."""
        return [
            {'step': 1, 'type': 'statement', 'description': 'State the universal claim'},
            {'step': 2, 'type': 'counterexample', 'description': 'Present specific counterexample'},
            {'step': 3, 'type': 'verification', 'description': 'Verify counterexample satisfies conditions'},
            {'step': 4, 'type': 'conclusion', 'description': 'Claim is false'}
        ]


def create_math_concept_service(config: Optional[Dict[str, Any]] = None) -> MathVerseConceptService:
    """
    Factory function to create a MathVerse concept service.
    
    Args:
        config: Optional configuration dictionary
        
    Returns:
        Configured MathVerseConceptService instance
    """
    return MathVerseConceptService(config)
