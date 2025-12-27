"""
VerseScript DSL Parser - AST Node Definitions

This module defines the Abstract Syntax Tree (AST) node types used by the
VerseScript parser to represent content scripts in a structured format.

Author: MiniMax Agent
Version: 1.0.0
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Union
from enum import Enum
from abc import ABC, abstractmethod


class ASTNodeType(str, Enum):
    """Types of AST nodes in VerseScript."""
    PROGRAM = "program"
    SCENE_DIRECTIVE = "scene_directive"
    ENTITY_DEFINITION = "entity_definition"
    VARIABLE_ASSIGNMENT = "variable_assignment"
    FUNCTION_DEFINITION = "function_definition"
    FUNCTION_CALL = "function_call"
    IF_STATEMENT = "if_statement"
    FOR_LOOP = "for_loop"
    WHILE_LOOP = "while_loop"
    RETURN_STATEMENT = "return_statement"
    ANIMATION_BLOCK = "animation_block"
    COMMENT = "comment"
    IMPORT_STATEMENT = "import_statement"
    PROPERTY_ACCESS = "property_access"
    BINARY_OPERATION = "binary_operation"
    UNARY_OPERATION = "unary_operation"
    LITERAL = "literal"
    IDENTIFIER = "identifier"
    LIST_LITERAL = "list_literal"
    DICT_LITERAL = "dict_literal"


class BinaryOperator(str, Enum):
    """Binary operators in expressions."""
    ADD = "+"
    SUBTRACT = "-"
    MULTIPLY = "*"
    DIVIDE = "/"
    MODULO = "%"
    POWER = "**"
    EQUALS = "=="
    NOT_EQUALS = "!="
    LESS_THAN = "<"
    GREATER_THAN = ">"
    LESS_EQUALS = "<="
    GREATER_EQUALS = ">="
    AND = "and"
    OR = "or"


class UnaryOperator(str, Enum):
    """Unary operators in expressions."""
    NEGATE = "-"
    NOT = "not"


@dataclass
class Position:
    """Source code position for error reporting."""
    line: int
    column: int
    file: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "line": self.line,
            "column": self.column,
            "file": self.file
        }


class ASTNode(ABC):
    """Base class for all AST nodes."""
    
    def __init__(self, node_type: ASTNodeType, position: Optional[Position] = None):
        self.node_type = node_type
        self.position = position
        self.children: List[ASTNode] = []
        self.metadata: Dict[str, Any] = {}
    
    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """Convert node to dictionary representation."""
        pass
    
    def add_child(self, child: 'ASTNode') -> 'ASTNode':
        """Add a child node."""
        self.children.append(child)
        return self
    
    def set_metadata(self, key: str, value: Any) -> 'ASTNode':
        """Set metadata on this node."""
        self.metadata[key] = value
        return self


@dataclass
class Program(ASTNode):
    """Root node representing a complete VerseScript program."""
    directives: List[ASTNode] = field(default_factory=list)
    statements: List[ASTNode] = field(default_factory=list)
    imports: List[ASTNode] = field(default_factory=list)
    domain: str = "general"
    
    def __init__(self, domain: str = "general"):
        super().__init__(ASTNodeType.PROGRAM)
        self.directives = []
        self.statements = []
        self.imports = []
        self.domain = domain
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.node_type.value,
            "domain": self.domain,
            "imports": [imp.to_dict() for imp in self.imports],
            "directives": [d.to_dict() for d in self.directives],
            "statements": [s.to_dict() for s in self.statements],
            "position": self.position.to_dict() if self.position else None
        }


@dataclass
class SceneDirective(ASTNode):
    """Scene configuration directive (@scene)."""
    attributes: Dict[str, Any] = field(default_factory=dict)
    
    def __init__(self, attributes: Dict[str, Any] = None):
        super().__init__(ASTNodeType.SCENE_DIRECTIVE)
        self.attributes = attributes or {}
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.node_type.value,
            "attributes": self.attributes,
            "position": self.position.to_dict() if self.position else None
        }


@dataclass
class EntityDefinition(ASTNode):
    """Entity definition statement."""
    entity_type: str
    name: str
    properties: Dict[str, Any] = field(default_factory=dict)
    
    def __init__(self, entity_type: str, name: str, properties: Dict[str, Any] = None):
        super().__init__(ASTNodeType.ENTITY_DEFINITION)
        self.entity_type = entity_type
        self.name = name
        self.properties = properties or {}
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.node_type.value,
            "entityType": self.entity_type,
            "name": self.name,
            "properties": self.properties,
            "position": self.position.to_dict() if self.position else None
        }


@dataclass
class VariableAssignment(ASTNode):
    """Variable assignment statement."""
    name: str
    value: ASTNode
    is_constant: bool = False
    
    def __init__(self, name: str, value: ASTNode, is_constant: bool = False):
        super().__init__(ASTNodeType.VARIABLE_ASSIGNMENT)
        self.name = name
        self.value = value
        self.is_constant = is_constant
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.node_type.value,
            "name": self.name,
            "value": self.value.to_dict(),
            "isConstant": self.is_constant,
            "position": self.position.to_dict() if self.position else None
        }


@dataclass
class FunctionDefinition(ASTNode):
    """Function definition statement."""
    name: str
    parameters: List[str] = field(default_factory=list)
    body: List[ASTNode] = field(default_factory=list)
    return_type: Optional[str] = None
    
    def __init__(self, name: str, parameters: List[str] = None, return_type: str = None):
        super().__init__(ASTNodeType.FUNCTION_DEFINITION)
        self.name = name
        self.parameters = parameters or []
        self.body = []
        self.return_type = return_type
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.node_type.value,
            "name": self.name,
            "parameters": self.parameters,
            "body": [b.to_dict() for b in self.body],
            "returnType": self.return_type,
            "position": self.position.to_dict() if self.position else None
        }


@dataclass
class FunctionCall(ASTNode):
    """Function call expression."""
    function_name: str
    arguments: List[ASTNode] = field(default_factory=list)
    
    def __init__(self, function_name: str, arguments: List[ASTNode] = None):
        super().__init__(ASTNodeType.FUNCTION_CALL)
        self.function_name = function_name
        self.arguments = arguments or []
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.node_type.value,
            "functionName": self.function_name,
            "arguments": [arg.to_dict() for arg in self.arguments],
            "position": self.position.to_dict() if self.position else None
        }


@dataclass
class IfStatement(ASTNode):
    """If-else conditional statement."""
    condition: ASTNode
    then_branch: List[ASTNode] = field(default_factory=list)
    else_branch: List[ASTNode] = field(default_factory=list)
    
    def __init__(self, condition: ASTNode):
        super().__init__(ASTNodeType.IF_STATEMENT)
        self.condition = condition
        self.then_branch = []
        self.else_branch = []
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.node_type.value,
            "condition": self.condition.to_dict(),
            "thenBranch": [b.to_dict() for b in self.then_branch],
            "elseBranch": [b.to_dict() for b in self.else_branch],
            "position": self.position.to_dict() if self.position else None
        }


@dataclass
class ForLoop(ASTNode):
    """For loop statement."""
    variable: str
    iterable: ASTNode
    body: List[ASTNode] = field(default_factory=list)
    
    def __init__(self, variable: str, iterable: ASTNode):
        super().__init__(ASTNodeType.FOR_LOOP)
        self.variable = variable
        self.iterable = iterable
        self.body = []
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.node_type.value,
            "variable": self.variable,
            "iterable": self.iterable.to_dict(),
            "body": [b.to_dict() for b in self.body],
            "position": self.position.to_dict() if self.position else None
        }


@dataclass
class WhileLoop(ASTNode):
    """While loop statement."""
    condition: ASTNode
    body: List[ASTNode] = field(default_factory=list)
    
    def __init__(self, condition: ASTNode):
        super().__init__(ASTNodeType.WHILE_LOOP)
        self.condition = condition
        self.body = []
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.node_type.value,
            "condition": self.condition.to_dict(),
            "body": [b.to_dict() for b in self.body],
            "position": self.position.to_dict() if self.position else None
        }


@dataclass
class AnimationBlock(ASTNode):
    """Animation block for visual content."""
    animation_type: str
    target: str
    parameters: Dict[str, Any] = field(default_factory=dict)
    duration_ms: int = 1000
    easing: str = "ease-in-out"
    
    def __init__(self, animation_type: str, target: str, duration: int = 1000):
        super().__init__(ASTNodeType.ANIMATION_BLOCK)
        self.animation_type = animation_type
        self.target = target
        self.duration_ms = duration
        self.parameters = {}
        self.easing = "ease-in-out"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.node_type.value,
            "animationType": self.animation_type,
            "target": self.target,
            "parameters": self.parameters,
            "durationMs": self.duration_ms,
            "easing": self.easing,
            "position": self.position.to_dict() if self.position else None
        }


@dataclass
class Literal(ASTNode):
    """Literal value (number, string, boolean)."""
    value: Any
    value_type: str
    
    def __init__(self, value: Any, value_type: str):
        super().__init__(ASTNodeType.LITERAL)
        self.value = value
        self.value_type = value_type
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.node_type.value,
            "value": self.value,
            "valueType": self.value_type,
            "position": self.position.to_dict() if self.position else None
        }


@dataclass
class Identifier(ASTNode):
    """Identifier (variable or function name)."""
    name: str
    
    def __init__(self, name: str):
        super().__init__(ASTNodeType.IDENTIFIER)
        self.name = name
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.node_type.value,
            "name": self.name,
            "position": self.position.to_dict() if self.position else None
        }


@dataclass
class PropertyAccess(ASTNode):
    """Property access expression (e.g., ball.position)."""
    object_name: str
    property_name: str
    
    def __init__(self, object_name: str, property_name: str):
        super().__init__(ASTNodeType.PROPERTY_ACCESS)
        self.object_name = object_name
        self.property_name = property_name
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.node_type.value,
            "objectName": self.object_name,
            "propertyName": self.property_name,
            "position": self.position.to_dict() if self.position else None
        }


@dataclass
class BinaryOperation(ASTNode):
    """Binary operation expression."""
    left: ASTNode
    operator: BinaryOperator
    right: ASTNode
    
    def __init__(self, left: ASTNode, operator: BinaryOperator, right: ASTNode):
        super().__init__(ASTNodeType.BINARY_OPERATION)
        self.left = left
        self.operator = operator
        self.right = right
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.node_type.value,
            "left": self.left.to_dict(),
            "operator": self.operator.value,
            "right": self.right.to_dict(),
            "position": self.position.to_dict() if self.position else None
        }


@dataclass
class UnaryOperation(ASTNode):
    """Unary operation expression."""
    operator: UnaryOperator
    operand: ASTNode
    
    def __init__(self, operator: UnaryOperator, operand: ASTNode):
        super().__init__(ASTNodeType.UNARY_OPERATION)
        self.operator = operator
        self.operand = operand
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.node_type.value,
            "operator": self.operator.value,
            "operand": self.operand.to_dict(),
            "position": self.position.to_dict() if self.position else None
        }


@dataclass
class ListLiteral(ASTNode):
    """List literal expression."""
    elements: List[ASTNode] = field(default_factory=list)
    
    def __init__(self, elements: List[ASTNode] = None):
        super().__init__(ASTNodeType.LIST_LITERAL)
        self.elements = elements or []
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.node_type.value,
            "elements": [e.to_dict() for e in self.elements],
            "position": self.position.to_dict() if self.position else None
        }


@dataclass
class DictLiteral(ASTNode):
    """Dictionary literal expression."""
    pairs: Dict[str, ASTNode] = field(default_factory=dict)
    
    def __init__(self, pairs: Dict[str, ASTNode] = None):
        super().__init__(ASTNodeType.DICT_LITERAL)
        self.pairs = pairs or {}
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.node_type.value,
            "pairs": {k: v.to_dict() for k, v in self.pairs.items()},
            "position": self.position.to_dict() if self.position else None
        }


@dataclass
class Comment(ASTNode):
    """Comment node."""
    text: str
    is_block: bool = False
    
    def __init__(self, text: str, is_block: bool = False):
        super().__init__(ASTNodeType.COMMENT)
        self.text = text
        self.is_block = is_block
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.node_type.value,
            "text": self.text,
            "isBlock": self.is_block,
            "position": self.position.to_dict() if self.position else None
        }


@dataclass
class ImportStatement(ASTNode):
    """Import statement for external resources."""
    module_path: str
    alias: Optional[str] = None
    items: List[str] = field(default_factory=list)
    
    def __init__(self, module_path: str, alias: str = None, items: List[str] = None):
        super().__init__(ASTNodeType.IMPORT_STATEMENT)
        self.module_path = module_path
        self.alias = alias
        self.items = items or []
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.node_type.value,
            "modulePath": self.module_path,
            "alias": self.alias,
            "items": self.items,
            "position": self.position.to_dict() if self.position else None
        }


@dataclass
class ReturnStatement(ASTNode):
    """Return statement in functions."""
    value: Optional[ASTNode] = None
    
    def __init__(self, value: ASTNode = None):
        super().__init__(ASTNodeType.RETURN_STATEMENT)
        self.value = value
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.node_type.value,
            "value": self.value.to_dict() if self.value else None,
            "position": self.position.to_dict() if self.position else None
        }


__all__ = [
    "ASTNodeType",
    "BinaryOperator",
    "UnaryOperator",
    "Position",
    "ASTNode",
    "Program",
    "SceneDirective",
    "EntityDefinition",
    "VariableAssignment",
    "FunctionDefinition",
    "FunctionCall",
    "IfStatement",
    "ForLoop",
    "WhileLoop",
    "AnimationBlock",
    "Literal",
    "Identifier",
    "PropertyAccess",
    "BinaryOperation",
    "UnaryOperation",
    "ListLiteral",
    "DictLiteral",
    "Comment",
    "ImportStatement",
    "ReturnStatement"
]
