"""
VerseScript DSL Parser - Main Parser Implementation

This module provides the core VerseScript parser that converts source code
written in the VerseScript DSL into an Abstract Syntax Tree (AST).

Author: MiniMax Agent
Version: 1.0.0
"""

import re
from typing import Optional, List, Dict, Any, Tuple
from pathlib import Path
from dataclasses import dataclass

from .lexer import (
    Position,
    Program,
    SceneDirective,
    EntityDefinition,
    VariableAssignment,
    FunctionDefinition,
    FunctionCall,
    IfStatement,
    ForLoop,
    WhileLoop,
    AnimationBlock,
    Literal,
    Identifier,
    PropertyAccess,
    BinaryOperation,
    UnaryOperation,
    ListLiteral,
    DictLiteral,
    Comment,
    ImportStatement,
    ReturnStatement,
    ASTNodeType,
    BinaryOperator,
    UnaryOperator
)


class ParseError(Exception):
    """Exception raised during parsing errors."""
    
    def __init__(self, message: str, position: Optional[Position] = None):
        self.message = message
        self.position = position
        super().__init__(self._format_message())
    
    def _format_message(self) -> str:
        if self.position:
            return f"{self.message} at line {self.position.line}, column {self.position.column}"
        return self.message


class TokenType:
    """Token types for the VerseScript lexer."""
    # Keywords
    SCENE = "SCENE"
    ENTITY = "ENTITY"
    DEF = "DEF"
    IF = "IF"
    ELIF = "ELIF"
    ELSE = "ELSE"
    FOR = "FOR"
    WHILE = "WHILE"
    RETURN = "RETURN"
    IMPORT = "IMPORT"
    AS = "AS"
    TRUE = "TRUE"
    FALSE = "FALSE"
    NONE = "NONE"
    
    # Operators
    PLUS = "+"
    MINUS = "-"
    STAR = "*"
    SLASH = "/"
    PERCENT = "%"
    STAR_STAR = "**"
    EQUAL = "="
    EQUAL_EQUAL = "=="
    NOT_EQUAL = "!="
    LESS = "<"
    GREATER = ">"
    LESS_EQUAL = "<="
    GREATER_EQUAL = ">="
    AND = "and"
    OR = "or"
    NOT = "not"
    
    # Delimiters
    LEFT_PAREN = "("
    RIGHT_PAREN = ")"
    LEFT_BRACKET = "["
    RIGHT_BRACKET = "]"
    LEFT_BRACE = "{"
    RIGHT_BRACE = "}"
    COMMA = ","
    COLON = ":"
    DOT = "."
    AT = "@"
    HASH = "#"
    
    # Literals
    NUMBER = "NUMBER"
    STRING = "STRING"
    IDENTIFIER = "IDENTIFIER"
    
    # Special
    NEWLINE = "NEWLINE"
    INDENT = "INDENT"
    DEDENT = "DEDENT"
    EOF = "EOF"
    COMMENT = "COMMENT"


@dataclass
class Token:
    """Token representation."""
    type: str
    value: str
    position: Optional[Position] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.type,
            "value": self.value,
            "position": self.position.to_dict() if self.position else None
        }


class VerseScriptLexer:
    """
    Lexical analyzer for VerseScript.
    
    Converts raw source code into a stream of tokens for parsing.
    """
    
    KEYWORDS = {
        "scene": TokenType.SCENE,
        "entity": TokenType.ENTITY,
        "def": TokenType.DEF,
        "if": TokenType.IF,
        "elif": TokenType.ELIF,
        "else": TokenType.ELSE,
        "for": TokenType.FOR,
        "while": TokenType.WHILE,
        "return": TokenType.RETURN,
        "import": TokenType.IMPORT,
        "as": TokenType.AS,
        "true": TokenType.TRUE,
        "false": TokenType.FALSE,
        "null": TokenType.NONE,
        "and": TokenType.AND,
        "or": TokenType.OR,
        "not": TokenType.NOT,
    }
    
    OPERATORS = {
        "**": TokenType.STAR_STAR,
        "==": TokenType.EQUAL_EQUAL,
        "!=": TokenType.NOT_EQUAL,
        "<=": TokenType.LESS_EQUAL,
        ">=": TokenType.GREATER_EQUAL,
        "+=": TokenType.PLUS,
        "-=": TokenType.MINUS,
    }
    
    SINGLE_OPERATORS = {
        "+": TokenType.PLUS,
        "-": TokenType.MINUS,
        "*": TokenType.STAR,
        "/": TokenType.SLASH,
        "%": TokenType.PERCENT,
        "=": TokenType.EQUAL,
        "<": TokenType.LESS,
        ">": TokenType.GREATER,
        "(": TokenType.LEFT_PAREN,
        ")": TokenType.RIGHT_PAREN,
        "[": TokenType.LEFT_BRACKET,
        "]": TokenType.RIGHT_BRACKET,
        "{": TokenType.LEFT_BRACE,
        "}": TokenType.RIGHT_BRACE,
        ",": TokenType.COMMA,
        ":": TokenType.COLON,
        ".": TokenType.DOT,
        "@": TokenType.AT,
        "#": TokenType.HASH,
    }
    
    def __init__(self, source: str, filename: str = None):
        self.source = source
        self.filename = filename
        self.pos = 0
        self.line = 1
        self.column = 0
        self.tokens: List[Token] = []
        self.current_line_start = 0
    
    def tokenize(self) -> List[Token]:
        """Convert source code to tokens."""
        while not self._is_at_end():
            self._skip_whitespace()
            
            if self._is_at_end():
                break
            
            char = self._peek()
            
            # Handle comments
            if char == "#":
                self._read_comment()
                continue
            
            # Handle multi-character operators
            two_char = self.source[self.pos:self.pos + 2]
            if two_char in self.OPERATORS:
                self._add_token(self.OPERATORS[two_char], two_char)
                self.pos += 2
                continue
            
            # Handle single-character operators
            if char in self.SINGLE_OPERATORS:
                self._add_token(self.SINGLE_OPERATORS[char], char)
                self.pos += 1
                continue
            
            # Handle string literals
            if char in ('"', "'"):
                self._read_string()
                continue
            
            # Handle numbers
            if self._is_digit(char):
                self._read_number()
                continue
            
            # Handle identifiers and keywords
            if self._is_alpha(char):
                self._read_identifier()
                continue
            
            raise ParseError(f"Unexpected character: {char}", self._current_position())
        
        self._add_token(TokenType.EOF, "")
        return self.tokens
    
    def _is_at_end(self) -> bool:
        return self.pos >= len(self.source)
    
    def _peek(self) -> str:
        return self.source[self.pos] if self.pos < len(self.source) else ""
    
    def _peek_next(self) -> str:
        return self.source[self.pos + 1] if self.pos + 1 < len(self.source) else ""
    
    def _current_position(self) -> Position:
        return Position(
            line=self.line,
            column=self.column,
            file=self.filename
        )
    
    def _skip_whitespace(self):
        while not self._is_at_end():
            char = self._peek()
            
            if char == "\n":
                self.line += 1
                self.column = 0
                self.pos += 1
                self._add_token(TokenType.NEWLINE, "\n")
                continue
            
            if char in " \t":
                self.pos += 1
                self.column += 1
                continue
            
            break
    
    def _read_comment(self):
        start_pos = self._current_position()
        self.pos += 1
        
        while not self._is_at_end() and self._peek() != "\n":
            self.pos += 1
        
        comment_text = self.source[start_pos.pos:self.pos]
        self._add_token(TokenType.COMMENT, comment_text, start_pos)
    
    def _read_string(self):
        start_pos = self._current_position()
        quote_char = self._peek()
        self.pos += 1
        self.column += 1
        
        value = ""
        
        while not self._is_at_end() and self._peek() != quote_char:
            char = self._peek()
            
            if char == "\\" and self._peek_next() != "":
                self.pos += 1
                escaped = self._peek()
                escape_map = {
                    "n": "\n",
                    "t": "\t",
                    "r": "\r",
                    '"': '"',
                    "'": "'",
                    "\\": "\\"
                }
                value += escape_map.get(escaped, escaped)
            else:
                value += char
            
            self.pos += 1
            self.column += 1
        
        # Skip closing quote
        if not self._is_at_end():
            self.pos += 1
            self.column += 1
        
        self._add_token(TokenType.STRING, value, start_pos)
    
    def _read_number(self):
        start_pos = self._current_position()
        value = ""
        has_decimal = False
        
        while not self._is_at_end():
            char = self._peek()
            
            if char == ".":
                if has_decimal:
                    break
                has_decimal = True
                value += char
                self.pos += 1
                self.column += 1
                continue
            
            if self._is_digit(char):
                value += char
                self.pos += 1
                self.column += 1
                continue
            
            break
        
        self._add_token(TokenType.NUMBER, value, start_pos)
    
    def _read_identifier(self):
        start_pos = self._current_position()
        value = ""
        
        while not self._is_at_end():
            char = self._peek()
            
            if self._is_alpha_numeric(char) or char == "_":
                value += char
                self.pos += 1
                self.column += 1
                continue
            
            break
        
        # Check if it's a keyword
        token_type = self.KEYWORDS.get(value.lower(), TokenType.IDENTIFIER)
        self._add_token(token_type, value, start_pos)
    
    def _is_digit(self, char: str) -> bool:
        return char >= "0" and char <= "9"
    
    def _is_alpha(self, char: str) -> bool:
        return (char >= "a" and char <= "z") or (char >= "A" and char <= "Z") or char == "_"
    
    def _is_alpha_numeric(self, char: str) -> bool:
        return self._is_alpha(char) or self._is_digit(char)
    
    def _add_token(self, token_type: str, value: str, position: Position = None):
        token = Token(
            type=token_type,
            value=value,
            position=position or self._current_position()
        )
        self.tokens.append(token)


class VerseScriptParser:
    """
    Parser for VerseScript DSL.
    
    Converts token stream into an Abstract Syntax Tree (AST) that can be
    compiled into VisualVerse configuration objects.
    """
    
    def __init__(self, tokens: List[Token], filename: str = None):
        self.tokens = tokens
        self.filename = filename
        self.pos = 0
        self.current_token: Optional[Token] = None
        self.domain = "general"
        self.errors: List[ParseError] = []
    
    def parse(self) -> Program:
        """Parse the token stream into an AST."""
        self._advance()
        program = self._parse_program()
        
        if self.current_token and self.current_token.type != TokenType.EOF:
            self._error(f"Unexpected token: {self.current_token.type}")
        
        return program
    
    def _advance(self):
        """Move to the next token."""
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
            self.pos += 1
    
    def _peek(self, offset: int = 0) -> Optional[Token]:
        """Peek at a future token."""
        idx = self.pos + offset
        return self.tokens[idx] if idx < len(self.tokens) else None
    
    def _expect(self, expected_type: str) -> Token:
        """Expect a specific token type."""
        if not self.current_token:
            self._error(f"Expected {expected_type} but reached end of input")
        
        if self.current_token.type != expected_type:
            self._error(
                f"Expected {expected_type} but got {self.current_token.type}",
                self.current_token.position
            )
        
        token = self.current_token
        self._advance()
        return token
    
    def _error(self, message: str, position: Position = None):
        """Record a parse error."""
        error = ParseError(message, position or self.current_token.position)
        self.errors.append(error)
        raise error
    
    def _parse_program(self) -> Program:
        """Parse the root program node."""
        program = Program(domain=self.domain)
        
        while self.current_token and self.current_token.type != TokenType.EOF:
            try:
                # Handle imports
                if self.current_token.type == TokenType.IMPORT:
                    import_stmt = self._parse_import()
                    program.imports.append(import_stmt)
                    continue
                
                # Handle scene directive
                if self.current_token.type == TokenType.AT:
                    directive = self._parse_scene_directive()
                    program.directives.append(directive)
                    continue
                
                # Handle regular statements
                statement = self._parse_statement()
                if statement:
                    program.statements.append(statement)
            
            except ParseError:
                # Skip to next statement on error
                self._synchronize()
                if self.current_token and self.current_token.type == TokenType.NEWLINE:
                    self._advance()
        
        return program
    
    def _parse_import(self) -> ImportStatement:
        """Parse import statement."""
        self._expect(TokenType.IMPORT)
        
        module_parts = []
        while self.current_token and self.current_token.type == TokenType.IDENTIFIER:
            module_parts.append(self.current_token.value)
            self._advance()
            
            if self.current_token and self.current_token.type == TokenType.DOT:
                self._advance()
        
        module_path = ".".join(module_parts)
        alias = None
        items = []
        
        if self.current_token and self.current_token.type == TokenType.AS:
            self._advance()
            if self.current_token and self.current_token.type == TokenType.IDENTIFIER:
                alias = self.current_token.value
                self._advance()
        
        return ImportStatement(
            module_path=module_path,
            alias=alias,
            items=items
        )
    
    def _parse_scene_directive(self) -> SceneDirective:
        """Parse @scene directive."""
        self._expect(TokenType.AT)
        self._expect(TokenType.SCENE)
        
        attributes = {}
        
        if self.current_token and self.current_token.type == TokenType.LEFT_PAREN:
            self._advance()
            
            while self.current_token and self.current_token.type != TokenType.RIGHT_PAREN:
                if self.current_token.type == TokenType.IDENTIFIER:
                    key = self.current_token.value
                    self._advance()
                    
                    if self.current_token and self.current_token.type == TokenType.EQUAL:
                        self._advance()
                        value = self._parse_value()
                        attributes[key] = value
                
                if self.current_token and self.current_token.type == TokenType.COMMA:
                    self._advance()
            
            self._expect(TokenType.RIGHT_PAREN)
        
        # Extract domain from attributes if present
        if "type" in attributes:
            domain_attr = str(attributes["type"])
            if "math" in domain_attr:
                self.domain = "math"
            elif "physics" in domain_attr:
                self.domain = "physics"
            elif "chem" in domain_attr:
                self.domain = "chemistry"
            elif "algo" in domain_attr:
                self.domain = "algorithms"
            elif "fin" in domain_attr:
                self.domain = "finance"
        
        return SceneDirective(attributes=attributes)
    
    def _parse_statement(self) -> Optional:
        """Parse a statement."""
        if not self.current_token:
            return None
        
        # Skip newlines
        if self.current_token.type == TokenType.NEWLINE:
            self._advance()
            return None
        
        # Handle entity definitions
        if self.current_token.type == TokenType.ENTITY:
            return self._parse_entity_definition()
        
        # Handle function definitions
        if self.current_token.type == TokenType.DEF:
            return self._parse_function_definition()
        
        # Handle if statements
        if self.current_token.type == TokenType.IF:
            return self._parse_if_statement()
        
        # Handle for loops
        if self.current_token.type == TokenType.FOR:
            return self._parse_for_loop()
        
        # Handle while loops
        if self.current_token.type == TokenType.WHILE:
            return self._parse_while_loop()
        
        # Handle return statements
        if self.current_token.type == TokenType.RETURN:
            return self._parse_return_statement()
        
        # Handle variable assignments or function calls
        if self.current_token.type == TokenType.IDENTIFIER:
            next_token = self._peek()
            
            if next_token and next_token.type == TokenType.LEFT_PAREN:
                return self._parse_function_call()
            elif next_token and next_token.type == TokenType.EQUAL:
                return self._parse_assignment()
            elif next_token and next_token.type == TokenType.DOT:
                return self._parse_property_access_assignment()
        
        # Skip unknown tokens
        self._advance()
        return None
    
    def _parse_entity_definition(self) -> EntityDefinition:
        """Parse entity definition."""
        self._expect(TokenType.ENTITY)
        
        entity_type = ""
        if self.current_token and self.current_token.type == TokenType.DOT:
            self._advance()
            if self.current_token and self.current_token.type == TokenType.IDENTIFIER:
                entity_type = self.current_token.value
                self._advance()
        
        if not self.current_token or self.current_token.type != TokenType.IDENTIFIER:
            self._error("Expected entity name")
        
        name = self.current_token.value
        self._advance()
        
        properties = {}
        if self.current_token and self.current_token.type == TokenType.LEFT_PAREN:
            self._advance()
            properties = self._parse_property_list()
            self._expect(TokenType.RIGHT_PAREN)
        
        return EntityDefinition(
            entity_type=entity_type or "base",
            name=name,
            properties=properties
        )
    
    def _parse_property_list(self) -> Dict[str, Any]:
        """Parse property list in parentheses."""
        properties = {}
        
        while self.current_token and self.current_token.type != TokenType.RIGHT_PAREN:
            if self.current_token.type == TokenType.IDENTIFIER:
                key = self.current_token.value
                self._advance()
                
                if self.current_token and self.current_token.type == TokenType.EQUAL:
                    self._advance()
                    value = self._parse_value()
                    properties[key] = value
            
            if self.current_token and self.current_token.type == TokenType.COMMA:
                self._advance()
        
        return properties
    
    def _parse_function_definition(self) -> FunctionDefinition:
        """Parse function definition."""
        self._expect(TokenType.DEF)
        
        if not self.current_token or self.current_token.type != TokenType.IDENTIFIER:
            self._error("Expected function name")
        
        name = self.current_token.value
        self._advance()
        
        parameters = []
        if self.current_token and self.current_token.type == TokenType.LEFT_PAREN:
            self._advance()
            
            while self.current_token and self.current_token.type != TokenType.RIGHT_PAREN:
                if self.current_token.type == TokenType.IDENTIFIER:
                    parameters.append(self.current_token.value)
                    self._advance()
                
                if self.current_token and self.current_token.type == TokenType.COMMA:
                    self._advance()
            
            self._expect(TokenType.RIGHT_PAREN)
        
        self._expect(TokenType.COLON)
        
        body = []
        while self.current_token and self.current_token.type not in (TokenType.EOF, TokenType.NEWLINE):
            statement = self._parse_statement()
            if statement:
                body.append(statement)
        
        func = FunctionDefinition(name=name, parameters=parameters)
        func.body = body
        return func
    
    def _parse_if_statement(self) -> IfStatement:
        """Parse if statement."""
        self._expect(TokenType.IF)
        
        condition = self._parse_expression()
        self._expect(TokenType.COLON)
        
        if_stmt = IfStatement(condition=condition)
        
        # Parse then branch
        while self.current_token and self.current_token.type not in (
            TokenType.EOF, TokenType.NEWLINE, TokenType.ELIF, TokenType.ELSE
        ):
            statement = self._parse_statement()
            if statement:
                if_stmt.then_branch.append(statement)
        
        # Handle elif
        if self.current_token and self.current_token.type == TokenType.ELIF:
            self._advance()
            elif_condition = self._parse_expression()
            self._expect(TokenType.COLON)
            
            elif_body = []
            while self.current_token and self.current_token.type not in (
                TokenType.EOF, TokenType.NEWLINE, TokenType.ELIF, TokenType.ELSE
            ):
                statement = self._parse_statement()
                if statement:
                    elif_body.append(statement)
            
            # Convert to nested if-else
            nested_if = IfStatement(condition=elif_condition)
            nested_if.then_branch = elif_body
            if_stmt.then_branch.append(nested_if)
        
        # Handle else
        if self.current_token and self.current_token.type == TokenType.ELSE:
            self._advance()
            self._expect(TokenType.COLON)
            
            while self.current_token and self.current_token.type not in (
                TokenType.EOF, TokenType.NEWLINE
            ):
                statement = self._parse_statement()
                if statement:
                    if_stmt.else_branch.append(statement)
        
        return if_stmt
    
    def _parse_for_loop(self) -> ForLoop:
        """Parse for loop."""
        self._expect(TokenType.FOR)
        
        if not self.current_token or self.current_token.type != TokenType.IDENTIFIER:
            self._error("Expected loop variable")
        
        variable = self.current_token.value
        self._advance()
        
        self._expect(TokenType.IN) if self.current_token and self.current_token.type == TokenType.IN else None
        
        iterable = self._parse_expression()
        
        self._expect(TokenType.COLON)
        
        loop = ForLoop(variable=variable, iterable=iterable)
        
        while self.current_token and self.current_token.type not in (TokenType.EOF, TokenType.NEWLINE):
            statement = self._parse_statement()
            if statement:
                loop.body.append(statement)
        
        return loop
    
    def _parse_while_loop(self) -> WhileLoop:
        """Parse while loop."""
        self._expect(TokenType.WHILE)
        
        condition = self._parse_expression()
        self._expect(TokenType.COLON)
        
        loop = WhileLoop(condition=condition)
        
        while self.current_token and self.current_token.type not in (TokenType.EOF, TokenType.NEWLINE):
            statement = self._parse_statement()
            if statement:
                loop.body.append(statement)
        
        return loop
    
    def _parse_return_statement(self) -> ReturnStatement:
        """Parse return statement."""
        self._expect(TokenType.RETURN)
        
        value = None
        if self.current_token and self.current_token.type not in (TokenType.NEWLINE, TokenType.EOF):
            value = self._parse_expression()
        
        return ReturnStatement(value=value)
    
    def _parse_assignment(self) -> VariableAssignment:
        """Parse variable assignment."""
        if not self.current_token or self.current_token.type != TokenType.IDENTIFIER:
            self._error("Expected variable name")
        
        name = self.current_token.value
        self._advance()
        self._expect(TokenType.EQUAL)
        
        value = self._parse_expression()
        
        return VariableAssignment(name=name, value=value)
    
    def _parse_property_access_assignment(self) -> VariableAssignment:
        """Parse property access assignment (e.g., ball.position = (100, 300))."""
        if not self.current_token or self.current_token.type != TokenType.IDENTIFIER:
            self._error("Expected object name")
        
        object_name = self.current_token.value
        self._advance()
        self._expect(TokenType.DOT)
        
        if not self.current_token or self.current_token.type != TokenType.IDENTIFIER:
            self._error("Expected property name")
        
        property_name = self.current_token.value
        self._advance()
        self._expect(TokenType.EQUAL)
        
        value = self._parse_expression()
        
        # Create a function call that represents the property assignment
        func_call = FunctionCall(
            function_name="set_property",
            arguments=[
                Identifier(name=object_name),
                Literal(value=property_name, value_type="string"),
                value
            ]
        )
        
        return VariableAssignment(
            name=f"{object_name}.{property_name}",
            value=func_call
        )
    
    def _parse_function_call(self) -> FunctionCall:
        """Parse function call."""
        if not self.current_token or self.current_token.type != TokenType.IDENTIFIER:
            self._error("Expected function name")
        
        name = self.current_token.value
        self._advance()
        
        arguments = []
        if self.current_token and self.current_token.type == TokenType.LEFT_PAREN:
            self._advance()
            
            while self.current_token and self.current_token.type != TokenType.RIGHT_PAREN:
                arg = self._parse_expression()
                arguments.append(arg)
                
                if self.current_token and self.current_token.type == TokenType.COMMA:
                    self._advance()
            
            self._expect(TokenType.RIGHT_PAREN)
        
        return FunctionCall(function_name=name, arguments=arguments)
    
    def _parse_expression(self) -> ASTNode:
        """Parse an expression."""
        return self._parse_comparison()
    
    def _parse_comparison(self) -> ASTNode:
        """Parse comparison operators."""
        left = self._parse_addition()
        
        while self.current_token and self.current_token.type in (
            TokenType.EQUAL_EQUAL, TokenType.NOT_EQUAL,
            TokenType.LESS, TokenType.GREATER,
            TokenType.LESS_EQUAL, TokenType.GREATER_EQUAL
        ):
            op = self.current_token.value
            self._advance()
            right = self._parse_addition()
            
            op_map = {
                "==": BinaryOperator.EQUALS,
                "!=": BinaryOperator.NOT_EQUALS,
                "<": BinaryOperator.LESS_THAN,
                ">": BinaryOperator.GREATER_THAN,
                "<=": BinaryOperator.LESS_EQUALS,
                ">=": BinaryOperator.GREATER_EQUALS
            }
            
            left = BinaryOperation(
                left=left,
                operator=op_map.get(op, BinaryOperator.EQUALS),
                right=right
            )
        
        return left
    
    def _parse_addition(self) -> ASTNode:
        """Parse addition and subtraction."""
        left = self._parse_multiplication()
        
        while self.current_token and self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            op = self.current_token.value
            self._advance()
            right = self._parse_multiplication()
            
            left = BinaryOperation(
                left=left,
                operator=BinaryOperator.ADD if op == "+" else BinaryOperator.SUBTRACT,
                right=right
            )
        
        return left
    
    def _parse_multiplication(self) -> ASTNode:
        """Parse multiplication and division."""
        left = self._parse_power()
        
        while self.current_token and self.current_token.type in (
            TokenType.STAR, TokenType.SLASH, TokenType.PERCENT
        ):
            op = self.current_token.value
            self._advance()
            right = self._parse_power()
            
            op_map = {
                "*": BinaryOperator.MULTIPLY,
                "/": BinaryOperator.DIVIDE,
                "%": BinaryOperator.MODULO
            }
            
            left = BinaryOperation(
                left=left,
                operator=op_map.get(op, BinaryOperator.MULTIPLY),
                right=right
            )
        
        return left
    
    def _parse_power(self) -> ASTNode:
        """Parse power operator."""
        left = self._parse_unary()
        
        while self.current_token and self.current_token.type == TokenType.STAR_STAR:
            self._advance()
            right = self._parse_unary()
            
            left = BinaryOperation(
                left=left,
                operator=BinaryOperator.POWER,
                right=right
            )
        
        return left
    
    def _parse_unary(self) -> ASTNode:
        """Parse unary operators."""
        if self.current_token and self.current_token.type in (TokenType.MINUS, TokenType.NOT):
            op = self.current_token.value
            self._advance()
            operand = self._parse_unary()
            
            return UnaryOperation(
                operator=UnaryOperator.NEGATE if op == "-" else UnaryOperator.NOT,
                operand=operand
            )
        
        return self._parse_primary()
    
    def _parse_primary(self) -> ASTNode:
        """Parse primary (leaf) expressions."""
        if not self.current_token:
            self._error("Unexpected end of input")
        
        token = self.current_token
        
        # Number literal
        if token.type == TokenType.NUMBER:
            self._advance()
            value = float(token.value) if "." in token.value else int(token.value)
            return Literal(value=value, value_type="number")
        
        # String literal
        if token.type == TokenType.STRING:
            self._advance()
            return Literal(value=token.value, value_type="string")
        
        # Boolean literals
        if token.type == TokenType.TRUE:
            self._advance()
            return Literal(value=True, value_type="boolean")
        
        if token.type == TokenType.FALSE:
            self._advance()
            return Literal(value=False, value_type="boolean")
        
        if token.type == TokenType.NONE:
            self._advance()
            return Literal(value=None, value_type="null")
        
        # Identifier
        if token.type == TokenType.IDENTIFIER:
            self._advance()
            
            # Check for function call
            if self.current_token and self.current_token.type == TokenType.LEFT_PAREN:
                arguments = []
                self._advance()  # Skip '('
                
                while self.current_token and self.current_token.type != TokenType.RIGHT_PAREN:
                    arg = self._parse_expression()
                    arguments.append(arg)
                    
                    if self.current_token and self.current_token.type == TokenType.COMMA:
                        self._advance()
                
                self._expect(TokenType.RIGHT_PAREN)
                return FunctionCall(function_name=token.value, arguments=arguments)
            
            # Check for property access
            if self.current_token and self.current_token.type == TokenType.DOT:
                parts = [token.value]
                self._advance()
                
                while self.current_token and self.current_token.type == TokenType.DOT:
                    self._advance()
                    if self.current_token and self.current_token.type == TokenType.IDENTIFIER:
                        parts.append(self.current_token.value)
                        self._advance()
                
                if len(parts) == 2:
                    return PropertyAccess(
                        object_name=parts[0],
                        property_name=parts[1]
                    )
            
            return Identifier(name=token.value)
        
        # Parenthesized expression
        if token.type == TokenType.LEFT_PAREN:
            self._advance()
            expr = self._parse_expression()
            self._expect(TokenType.RIGHT_PAREN)
            return expr
        
        # List literal
        if token.type == TokenType.LEFT_BRACKET:
            self._advance()
            elements = []
            
            while self.current_token and self.current_token.type != TokenType.RIGHT_BRACKET:
                element = self._parse_expression()
                elements.append(element)
                
                if self.current_token and self.current_token.type == TokenType.COMMA:
                    self._advance()
            
            self._expect(TokenType.RIGHT_BRACKET)
            return ListLiteral(elements=elements)
        
        # Dictionary literal
        if token.type == TokenType.LEFT_BRACE:
            self._advance()
            pairs = {}
            
            while self.current_token and self.current_token.type != TokenType.RIGHT_BRACE:
                if self.current_token.type == TokenType.IDENTIFIER:
                    key = self.current_token.value
                    self._advance()
                    self._expect(TokenType.COLON)
                    value = self._parse_expression()
                    pairs[key] = value
                
                if self.current_token and self.current_token.type == TokenType.COMMA:
                    self._advance()
            
            self._expect(TokenType.RIGHT_BRACE)
            return DictLiteral(pairs=pairs)
        
        self._error(f"Unexpected token: {token.type}")
    
    def _parse_value(self) -> Any:
        """Parse a value (for attributes)."""
        if not self.current_token:
            return None
        
        if self.current_token.type == TokenType.NUMBER:
            value = float(self.current_token.value) if "." in self.current_token.value else int(self.current_token.value)
            self._advance()
            return value
        
        if self.current_token.type == TokenType.STRING:
            value = self.current_token.value
            self._advance()
            return value
        
        if self.current_token.type == TokenType.TRUE:
            self._advance()
            return True
        
        if self.current_token.type == TokenType.FALSE:
            self._advance()
            return False
        
        if self.current_token.type == TokenType.NONE:
            self._advance()
            return None
        
        return None
    
    def _synchronize(self):
        """Skip tokens until a synchronization point."""
        sync_tokens = {
            TokenType.NEWLINE, TokenType.EOF,
            TokenType.DEF, TokenType.IF, TokenType.FOR, TokenType.WHILE,
            TokenType.RETURN, TokenType.ENTITY
        }
        
        while self.current_token and self.current_token.type not in sync_tokens:
            self._advance()


def parse_verse_script(source: str, filename: str = None) -> Program:
    """
    Convenience function to parse VerseScript source code.
    
    Args:
        source: The VerseScript source code
        filename: Optional filename for error reporting
        
    Returns:
        Parsed Program AST
        
    Raises:
        ParseError: If there are parsing errors
    """
    lexer = VerseScriptLexer(source, filename)
    tokens = lexer.tokenize()
    parser = VerseScriptParser(tokens, filename)
    return parser.parse()


__all__ = [
    "TokenType",
    "Token",
    "VerseScriptLexer",
    "VerseScriptParser",
    "ParseError",
    "parse_verse_script"
]
