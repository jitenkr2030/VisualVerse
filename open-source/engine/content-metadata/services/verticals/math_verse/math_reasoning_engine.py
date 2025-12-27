"""
MathVerse Reasoning Engine

This module provides the MathVerse-specific reasoning engine implementation,
extending the base reasoning engine with mathematical domain functionality
including proof step decomposition, logical reasoning strategies, and
explanation generation for mathematical proofs and derivations.

Licensed under the Apache License, Version 2.0
"""

from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import logging

from ....extensions.service_extension_base import (
    ReasoningEngineExtension,
    ExtensionContext
)

logger = logging.getLogger(__name__)


class ProofStrategy(str, Enum):
    """Mathematical proof strategies."""
    DIRECT = "direct"
    INDUCTION = "induction"
    CONTRADICTION = "contradiction"
    COUNTEREXAMPLE = "counterexample"
    CONSTRUCTION = "construction"
    CASES = "cases"
    CONTRAPOSITIVE = "contrapositive"
    COMPARISON = "comparison"
    EXHAUSTION = "exhaustion"


class ReasoningStepType(str, Enum):
    """Types of reasoning steps in mathematical proofs."""
    ASSUMPTION = "assumption"
    DEFINITION = "definition"
    AXIOM = "axiom"
    LEMMA = "lemma"
    DERIVATION = "derivation"
    CALCULATION = "calculation"
    SUBSTITUTION = "substitution"
    EQUALITY = "equality"
    INEQUALITY = "inequality"
    LOGICAL_INFERENCE = "logical_inference"
    CONCLUSION = "conclusion"


@dataclass
class ReasoningStep:
    """A single step in a mathematical reasoning process."""
    step_id: str
    step_type: ReasoningStepType
    content: str
    justification: str
    dependencies: List[str] = field(default_factory=list)
    logical_form: Optional[str] = None
    math_expression: Optional[str] = None
    confidence: float = 1.0
    alternatives: List[str] = field(default_factory=list)


@dataclass
class ProofStructure:
    """Structure of a mathematical proof."""
    proof_id: str
    theorem_name: str
    theorem_statement: str
    proof_type: ProofStrategy
    assumptions: List[str]
    steps: List[ReasoningStep]
    conclusion: str
    is_valid: bool
    difficulty: str
    techniques_used: List[str]


@dataclass
class ExplanationTemplate:
    """Template for generating explanations."""
    template_id: str
    proof_type: ProofStrategy
    description: str
    steps: List[str]


class MathVerseReasoningEngine:
    """
    MathVerse-specific reasoning engine.
    
    This engine handles mathematical reasoning including:
    - Proof decomposition and analysis
    - Multiple proof strategy identification
    - Step-by-step explanation generation
    - Validation of proof logic
    - Gap detection in mathematical reasoning
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the MathVerse reasoning engine.
        
        Args:
            config: Optional configuration dictionary
        """
        self.config = config or {}
        self._templates = self._load_explanation_templates()
        self._axioms = self._load_common_axioms()
        self._definitions = self._load_common_definitions()
        
    def _load_explanation_templates(self) -> Dict[ProofStrategy, ExplanationTemplate]:
        """Load explanation templates for different proof types."""
        return {
            ProofStrategy.DIRECT: ExplanationTemplate(
                template_id="direct-proof",
                proof_type=ProofStrategy.DIRECT,
                description="A direct proof establishes the statement by logical deduction from axioms and definitions.",
                steps=[
                    "State the theorem clearly",
                    "List given conditions and definitions",
                    "Apply relevant axioms and previously proven results",
                    "Perform logical deductions step by step",
                    "Reach the conclusion"
                ]
            ),
            ProofStrategy.INDUCTION: ExplanationTemplate(
                template_id="induction-proof",
                proof_type=ProofStrategy.INDUCTION,
                description="Proof by mathematical induction proves a statement for all natural numbers by establishing a base case and an inductive step.",
                steps=[
                    "State the property P(n) to be proven",
                    "Prove the base case P(1) or P(0)",
                    "Assume P(k) is true (inductive hypothesis)",
                    "Prove P(k+1) follows from P(k)",
                    "Conclude P(n) is true for all n"
                ]
            ),
            ProofStrategy.CONTRADICTION: ExplanationTemplate(
                template_id="contradiction-proof",
                proof_type=ProofStrategy.CONTRADICTION,
                description="Proof by contradiction assumes the negation of the statement and derives a contradiction.",
                steps=[
                    "Assume the negation of the statement is true",
                    "Derive logical consequences from this assumption",
                    "Show that these consequences contradict known facts",
                    "Conclude the original statement must be true"
                ]
            ),
            ProofStrategy.COUNTEREXAMPLE: ExplanationTemplate(
                template_id="counterexample-proof",
                proof_type=ProofStrategy.COUNTEREXAMPLE,
                description="A counterexample disproves a universal claim by providing a specific case where it fails.",
                steps=[
                    "State the universal claim to be disproven",
                    "Present a specific counterexample",
                    "Verify the counterexample satisfies the hypothesis",
                    "Show the counterexample violates the conclusion",
                    "Conclude the original claim is false"
                ]
            ),
        }
    
    def _load_common_axioms(self) -> Dict[str, str]:
        """Load common mathematical axioms."""
        return {
            'peano': "Every natural number has a successor",
            'addition': "a + b = b + a",
            'multiplication': "a × b = b × a",
            'distributive': "a × (b + c) = a × b + a × c",
            'transitive': "If a = b and b = c, then a = c",
            'trichotomy': "For any two real numbers, exactly one of a < b, a = b, or a > b is true"
        }
    
    def _load_common_definitions(self) -> Dict[str, str]:
        """Load common mathematical definitions."""
        return {
            'prime': "A prime number is a natural number greater than 1 with no positive divisors other than 1 and itself",
            'function': "A function f from set A to set B assigns to each element of A exactly one element of B",
            'limit': "L is the limit of f(x) as x approaches a if for every ε > 0, there exists δ > 0 such that |f(x) - L| < ε whenever 0 < |x - a| < δ",
            'derivative': "The derivative of f at a is f'(a) = lim(h→0) [f(a+h) - f(a)]/h",
            'integral': "The definite integral of f from a to b is the net area under the curve",
            'convergence': "A sequence converges to L if for every ε > 0, there exists N such that |a_n - L| < ε for all n > N"
        }
    
    def get_reasoning_strategies(self) -> List[str]:
        """
        Get reasoning strategies provided by this engine.
        
        Returns:
            List of strategy identifiers
        """
        return [e.value for e in ProofStrategy]
    
    def decompose_step(
        self,
        step: Dict[str, Any],
        context: Optional[ExtensionContext] = None
    ) -> List[ReasoningStep]:
        """
        Decompose a reasoning step into sub-steps.
        
        Args:
            step: The step to decompose
            context: Optional execution context
            
        Returns:
            List of decomposed sub-steps
        """
        step_type = step.get('type', 'general')
        content = step.get('content', '')
        
        if step_type == 'proof-step':
            return self._decompose_proof_step(content)
        elif step_type == 'calculation':
            return self._decompose_calculation(content)
        elif step_type == 'definition':
            return self._decompose_definition(content)
        else:
            return [ReasoningStep(
                step_id="step-1",
                step_type=ReasoningStepType.GENERAL,
                content=content,
                justification="Given information"
            )]
    
    def generate_explanation(
        self,
        reasoning_type: str,
        data: Dict[str, Any],
        context: Optional[ExtensionContext] = None
    ) -> Dict[str, Any]:
        """
        Generate an explanation for a reasoning process.
        
        Args:
            reasoning_type: Type of reasoning
            data: Reasoning data
            context: Optional execution context
            
        Returns:
            Explanation data
        """
        try:
            proof_type = ProofStrategy(reasoning_type)
        except ValueError:
            proof_type = ProofStrategy.DIRECT
        
        template = self._templates.get(proof_type)
        
        if template:
            return {
                'type': reasoning_type,
                'description': template.description,
                'steps': template.steps,
                'proof_structure': self._generate_proof_structure(data, proof_type),
                'examples': self._get_examples_for_type(proof_type)
            }
        
        return {
            'type': reasoning_type,
            'explanation': "Mathematical reasoning step",
            'data': data
        }
    
    def analyze_proof(
        self,
        theorem: Dict[str, Any],
        proof: List[Dict[str, Any]]
    ) -> ProofStructure:
        """
        Analyze a mathematical proof for validity and structure.
        
        Args:
            theorem: The theorem being proven
            proof: List of proof steps
            
        Returns:
            ProofStructure with analysis results
        """
        # Determine proof type
        proof_type = self._identify_proof_type(theorem, proof)
        
        # Extract assumptions
        assumptions = self._extract_assumptions(proof)
        
        # Parse steps into structured format
        steps = self._parse_proof_steps(proof)
        
        # Extract conclusion
        conclusion = self._extract_conclusion(proof)
        
        # Validate proof logic
        validation = self._validate_proof_logic(steps, assumptions, conclusion)
        
        # Identify techniques used
        techniques = self._identify_techniques(steps)
        
        return ProofStructure(
            proof_id=f"proof-{theorem.get('id', 'unknown')}",
            theorem_name=theorem.get('name', 'Unknown Theorem'),
            theorem_statement=theorem.get('statement', ''),
            proof_type=proof_type,
            assumptions=assumptions,
            steps=steps,
            conclusion=conclusion,
            is_valid=validation['is_valid'],
            difficulty=validation['difficulty'],
            techniques_used=techniques
        )
    
    def suggest_proof_strategy(
        self,
        theorem: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Suggest proof strategies for a given theorem.
        
        Args:
            theorem: The theorem to prove
            
        Returns:
            List of suggested strategies with confidence scores
        """
        suggestions = []
        statement = theorem.get('statement', '').lower()
        theorem_type = theorem.get('type', 'unknown')
        
        # Check for induction indicators
        if any(word in statement for word in ['for all n', 'induction', 'every natural', 'positive integer']):
            suggestions.append({
                'strategy': 'induction',
                'confidence': 0.9,
                'reason': 'Statement appears to be universal over natural numbers',
                'difficulty': 'medium'
            })
        
        # Check for contradiction indicators
        if any(word in statement for word in ['prove that', 'impossible', 'cannot exist', 'does not']):
            suggestions.append({
                'strategy': 'contradiction',
                'confidence': 0.7,
                'reason': 'Statement is negative or existential',
                'difficulty': 'medium'
            })
        
        # Check for direct proof indicators
        if theorem_type in ['definition', 'formula', 'identity']:
            suggestions.append({
                'strategy': 'direct',
                'confidence': 0.8,
                'reason': 'Statement defines or computes a specific relationship',
                'difficulty': 'easy'
            })
        
        # Check for counterexample needs
        if 'false' in statement or 'not' in statement:
            suggestions.append({
                'strategy': 'counterexample',
                'confidence': 0.6,
                'reason': 'Statement claims falsity',
                'difficulty': 'easy'
            })
        
        # Sort by confidence
        suggestions.sort(key=lambda x: x['confidence'], reverse=True)
        
        return suggestions
    
    def validate_proof_step(
        self,
        step: ReasoningStep,
        previous_steps: List[ReasoningStep]
    ) -> Dict[str, Any]:
        """
        Validate a single proof step.
        
        Args:
            step: The step to validate
            previous_steps: Previous steps in the proof
            
        Returns:
            Validation results
        """
        # Check if dependencies are satisfied
        missing_deps = []
        for dep_id in step.dependencies:
            if not any(s.step_id == dep_id for s in previous_steps):
                missing_deps.append(dep_id)
        
        if missing_deps:
            return {
                'is_valid': False,
                'error': f'Missing dependencies: {missing_deps}',
                'type': 'dependency_error'
            }
        
        # Check logical consistency
        consistency_check = self._check_logical_consistency(step, previous_steps)
        
        return {
            'is_valid': len(missing_deps) == 0 and consistency_check['is_consistent'],
            'warnings': consistency_check.get('warnings', []),
            'type': 'step_validation'
        }
    
    def _decompose_proof_step(self, content: str) -> List[ReasoningStep]:
        """Decompose a proof step into sub-steps."""
        # Split by logical connectors
        connectors = ['therefore', 'hence', 'thus', 'so', 'it follows', 'this implies']
        
        for connector in connectors:
            if connector in content.lower():
                parts = content.split(connector, 1)
                if len(parts) == 2:
                    return [
                        ReasoningStep(
                            step_id="step-1",
                            step_type=ReasoningStepType.DERIVATION,
                            content=parts[0].strip(),
                            justification="Given"
                        ),
                        ReasoningStep(
                            step_id="step-2",
                            step_type=ReasoningStepType.CONCLUSION,
                            content=parts[1].strip(),
                            justification=f"Therefore, {connector}"
                        )
                    ]
        
        return [ReasoningStep(
            step_id="step-1",
            step_type=ReasoningStepType.DERIVATION,
            content=content,
            justification="Logical deduction"
        )]
    
    def _decompose_calculation(self, content: str) -> List[ReasoningStep]:
        """Decompose a calculation into steps."""
        return [
            ReasoningStep(
                step_id="calc-1",
                step_type=ReasoningStepType.SUBSTITUTION,
                content=f"Substitute values into: {content}",
                justification="Direct substitution"
            ),
            ReasoningStep(
                step_id="calc-2",
                step_type=ReasoningStepType.CALCULATION,
                content=f"Perform arithmetic operations",
                justification="Algebraic manipulation"
            ),
            ReasoningStep(
                step_id="calc-3",
                step_type=ReasoningStepType.EQUALITY,
                content=f"Final result",
                justification="Computation complete"
            )
        ]
    
    def _decompose_definition(self, content: str) -> List[ReasoningStep]:
        """Decompose a definition application."""
        return [
            ReasoningStep(
                step_id="def-1",
                step_type=ReasoningStepType.DEFINITION,
                content=f"Recall definition: {content}",
                justification="Definition reference"
            ),
            ReasoningStep(
                step_id="def-2",
                step_type=ReasoningStepType.LOGICAL_INFERENCE,
                content="Apply definition to current context",
                justification="Definition application"
            )
        ]
    
    def _generate_proof_structure(
        self,
        data: Dict[str, Any],
        proof_type: ProofStrategy
    ) -> Dict[str, Any]:
        """Generate a proof structure from data."""
        return {
            'type': proof_type.value,
            'premises': data.get('premises', []),
            'intermediate_steps': data.get('steps', []),
            'conclusion': data.get('conclusion', '')
        }
    
    def _get_examples_for_type(self, proof_type: ProofStrategy) -> List[str]:
        """Get example theorems for each proof type."""
        examples = {
            ProofStrategy.DIRECT: [
                "The sum of two even numbers is even",
                "If a|b and b|c, then a|c"
            ],
            ProofStrategy.INDUCTION: [
                "Sum of first n natural numbers = n(n+1)/2",
                "2^n > n for all n ≥ 1"
            ],
            ProofStrategy.CONTRADICTION: [
                "√2 is irrational",
                "There are infinitely many primes"
            ],
            ProofStrategy.COUNTEREXAMPLE: [
                "Not all continuous functions are differentiable",
                "Not all bounded sequences converge"
            ]
        }
        return examples.get(proof_type, [])
    
    def _identify_proof_type(
        self,
        theorem: Dict[str, Any],
        proof: List[Dict[str, Any]]
    ) -> ProofStrategy:
        """Identify the type of proof."""
        proof_text = ' '.join(str(step) for step in proof).lower()
        
        if 'base case' in proof_text or 'inductive' in proof_text:
            return ProofStrategy.INDUCTION
        elif 'assume' in proof_text and ('contradiction' in proof_text or 'false' in proof_text):
            return ProofStrategy.CONTRADICTION
        elif 'counterexample' in proof_text:
            return ProofStrategy.COUNTEREXAMPLE
        elif 'case' in proof_text and 'cases' in proof_text:
            return ProofStrategy.CASES
        
        return ProofStrategy.DIRECT
    
    def _extract_assumptions(self, proof: List[Dict[str, Any]]) -> List[str]:
        """Extract assumptions from a proof."""
        assumptions = []
        
        for step in proof:
            content = str(step.get('content', '')).lower()
            if 'assume' in content or 'given' in content:
                assumptions.append(step.get('content', ''))
        
        return assumptions
    
    def _parse_proof_steps(self, proof: List[Dict[str, Any]]) -> List[ReasoningStep]:
        """Parse proof steps into structured format."""
        steps = []
        
        for i, step in enumerate(proof):
            step_type = self._determine_step_type(step)
            
            steps.append(ReasoningStep(
                step_id=f"step-{i+1}",
                step_type=step_type,
                content=step.get('content', ''),
                justification=step.get('justification', ''),
                dependencies=step.get('dependencies', []),
                math_expression=step.get('expression'),
                confidence=step.get('confidence', 1.0)
            ))
        
        return steps
    
    def _determine_step_type(self, step: Dict[str, Any]) -> ReasoningStepType:
        """Determine the type of a reasoning step."""
        content = str(step.get('content', '')).lower()
        
        if 'assume' in content or 'given' in content:
            return ReasoningStepType.ASSUMPTION
        elif 'definition' in content:
            return ReasoningStepType.DEFINITION
        elif any(word in content for word in ['calculate', 'compute', 'evaluate']):
            return ReasoningStepType.CALCULATION
        elif any(word in content for word in ['therefore', 'thus', 'hence', 'conclude']):
            return ReasoningStepType.CONCLUSION
        elif '=' in content:
            return ReasoningStepType.EQUALITY
        else:
            return ReasoningStepType.DERIVATION
    
    def _extract_conclusion(self, proof: List[Dict[str, Any]]) -> str:
        """Extract the conclusion from a proof."""
        for step in reversed(proof):
            content = str(step.get('content', '')).lower()
            if any(word in content for word in ['therefore', 'thus', 'hence', 'conclude', 'shown']):
                return step.get('content', '')
        
        return proof[-1].get('content', '') if proof else ''
    
    def _validate_proof_logic(
        self,
        steps: List[ReasoningStep],
        assumptions: List[str],
        conclusion: str
    ) -> Dict[str, Any]:
        """Validate the logic of a proof."""
        # Check if all steps have justification
        unjustified = [s for s in steps if not s.justification]
        
        # Check logical flow
        valid_flow = True
        for i, step in enumerate(steps):
            if step.dependencies:
                for dep_id in step.dependencies:
                    dep_exists = any(s.step_id == dep_id for s in steps[:i])
                    if not dep_exists:
                        valid_flow = False
                        break
        
        # Estimate difficulty
        difficulty = 'easy'
        if len(steps) > 10:
            difficulty = 'medium'
        if len(steps) > 20:
            difficulty = 'hard'
        
        return {
            'is_valid': len(unjustified) == 0 and valid_flow,
            'unjustified_steps': len(unjustified),
            'warnings': ['Missing justifications' if unjustified else None],
            'difficulty': difficulty
        }
    
    def _identify_techniques(self, steps: List[ReasoningStep]) -> List[str]:
        """Identify techniques used in the proof."""
        techniques = set()
        
        for step in steps:
            if step.step_type == ReasoningStepType.ASSUMPTION:
                techniques.add('case_analysis')
            elif 'induction' in step.content.lower():
                techniques.add('mathematical_induction')
            elif step.step_type == ReasoningStepType.CALCULATION:
                techniques.add('algebraic_manipulation')
            elif 'contradiction' in step.content.lower():
                techniques.add('proof_by_contradiction')
        
        return list(techniques)
    
    def _check_logical_consistency(
        self,
        step: ReasoningStep,
        previous_steps: List[ReasoningStep]
    ) -> Dict[str, Any]:
        """Check if a step is logically consistent with previous steps."""
        # Simplified consistency check
        previous_content = ' '.join(s.content for s in previous_steps)
        
        # Check for obvious contradictions
        contradictions = [
            ('positive', 'negative'),
            ('greater', 'less'),
            ('equal', 'not equal'),
        ]
        
        warnings = []
        for pos, neg in contradictions:
            if pos in step.content.lower() and neg in previous_content.lower():
                warnings.append(f"Potential contradiction: {pos} vs {neg}")
        
        return {
            'is_consistent': len(warnings) == 0,
            'warnings': warnings
        }


def create_math_reasoning_engine(config: Optional[Dict[str, Any]] = None) -> MathVerseReasoningEngine:
    """
    Factory function to create a MathVerse reasoning engine.
    
    Args:
        config: Optional configuration dictionary
        
    Returns:
        Configured MathVerseReasoningEngine instance
    """
    return MathVerseReasoningEngine(config)
