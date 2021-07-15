from __future__ import annotations
from enum import Enum
from typing import Callable
from lalalang.lexer import Lexer, Token, TokenType
from .ast import (
    Statement,
    Program,
    ExpressionStatement,
    ReturnStatement,
    PrefixExpression,
    Expression,
    Identifier,
    InfixExpression,
    IntegerLiteral,
    LetStatement,
)


class Parser:
    def __init__(self, lexer: Lexer):
        self.lexer: Lexer = lexer
        self.current_token: Token = Token.empty()
        self.peek_token: Token = Token.empty()
        self.statements: list[Statement] = []
        self.errors: list[str] = []
        self.prefix_parse_funs: dict[TokenType, Callable] = dict({})
        self.infix_parse_funs: dict[TokenType, Callable] = dict({})
        self._setup()

    def __repr__(self):
        conversion: list[str] = [repr(i) for i in self.statements]
        return "\n".join(conversion)

    def __str__(self):
        conversion: list[str] = [str(i) for i in self.statements]
        return "".join(conversion)

    def parse_program(self) -> Program:
        """
        This is the main method that will traverse the tokens
        and generate an abstract syntax tree
        """
        program: Program = Program()
        while not self._current_token_is(TokenType.EOF):
            statement: Statement = self._parse_statement()
            if statement != None:
                program.add_statement(statement)
            self._next_token()
        return program

    def _setup(self) -> None:
        """
        Some stuff that needs to be ready at the construction of
        this class
        """
        self._register_prefix_fun(TokenType.IDENT, self._parse_identifier)
        self._register_prefix_fun(TokenType.INT, self._parse_integer_literal)
        self._register_prefix_fun(TokenType.BANG, self._parse_prefix_expression)
        self._register_prefix_fun(TokenType.MINUS, self._parse_prefix_expression)

        self._register_infix_fun(TokenType.PLUS, self._parse_infix_expression)
        self._register_infix_fun(TokenType.MINUS, self._parse_infix_expression)
        self._register_infix_fun(TokenType.SLASH, self._parse_infix_expression)
        self._register_infix_fun(TokenType.ASTERISK, self._parse_infix_expression)
        self._register_infix_fun(TokenType.EQ, self._parse_infix_expression)
        self._register_infix_fun(TokenType.NOT_EQ, self._parse_infix_expression)
        self._register_infix_fun(TokenType.LT, self._parse_infix_expression)
        self._register_infix_fun(TokenType.GT, self._parse_infix_expression)

        self._next_token()
        self._next_token()

    def _next_token(self) -> None:
        """
        This helps us moving arround the lexer to watch one
        token ahead
        """
        self.current_token = self.peek_token
        self.peek_token = self.lexer.next_token()

    def _parse_statement(self) -> Statement:
        """
        Here are the conditionals to handle any statements defined
        by us
        """
        if self._current_token_is(TokenType.LET):
            return self._parse_let_statement()
        elif self._current_token_is(TokenType.RETURN):
            return self._parse_return_statement()
        else:
            return self._parse_expression_statement()
        raise Exception("Unable to parse statement")

    def _parse_let_statement(self) -> LetStatement:
        """
        Handling the specific case of a let statement
        """
        statement: LetStatement = LetStatement.empty()
        statement.token = self.current_token

        if not self._peek_expected(TokenType.IDENT):
            raise Exception("Could not parse let statement")

        statement.name = Identifier(self.current_token, self.current_token.literal)

        while not self._current_token_is(TokenType.SEMICOLON):
            self._next_token()

        return statement

    def _parse_return_statement(self) -> ReturnStatement:
        """
        Handling the other case of return statement
        """
        statement: ReturnStatement = ReturnStatement.empty()
        statement.token = self.current_token

        self._next_token()

        while not self._current_token_is(TokenType.SEMICOLON):
            self._next_token()

        return statement

    def _parse_expression_statement(self) -> ExpressionStatement:
        """
        Here we extract expression statements from the code
        """
        statement: ExpressionStatement = ExpressionStatement.empty()
        statement.expression = self._parse_expression(ExpressionType.LOWEST)

        if self._peek_token_is(TokenType.SEMICOLON):
            self._next_token()

        return statement

    def _parse_expression(self, precedence: ExpressionType) -> Expression:
        """
        Here we ensure we are using the correct precedence
        with the corresponding function
        """
        prefix: Callable = self.prefix_parse_funs.get(self.current_token.token_type)
        if not prefix:
            self._no_prefix_parsing_error(self.current_token.token_type)
            return None

        left_expression: Expression = prefix()

        while (
            not self._peek_token_is(TokenType.SEMICOLON)
            and precedence < self._peek_precendence()
        ):
            infix: Callable = self.infix_parse_funs.get(self.peek_token.token_type)
            if not infix:
                return left_expression

            self._next_token()
            left_expression = infix(left_expression)

        return left_expression

    def _parse_identifier(self) -> Identifier:
        """
        We return the identifier of on our current position
        """
        return Identifier(self.current_token, self.current_token.literal)

    def _parse_integer_literal(self) -> IntegerLiteral:
        """
        Here we extract integers and convert them from str to int
        """
        literal: IntegerLiteral = IntegerLiteral.empty()
        literal.token = self.current_token
        try:
            number: int = int(self.current_token.literal)
        except ValueError:
            self.errors.append(
                "Could not parse %s as integer" % self.current_token.literal
            )
        literal.value = number
        return literal

    def _parse_prefix_expression(self) -> Expression:
        """
        We return the prefix expression of our current token
        """
        expression: PrefixExpression = PrefixExpression.empty()
        expression.token = self.current_token
        expression.operator = self.current_token.literal

        self._next_token()
        expression.right = self._parse_expression(ExpressionType.PREFIX)

        return expression

    def _parse_infix_expression(self, left: Expression):
        """
        We return the infix expression of our current token
        """
        expression: InfixExpression = InfixExpression.empty()
        expression.token = self.current_token
        expression.operator = self.current_token.literal
        expression.left = left

        precedence = self._current_precedence()
        self._next_token()
        expression.right = self._parse_expression(precedence)

        return expression

    def _no_prefix_parsing_error(self, token_type: TokenType) -> None:
        """
        Add this error message whenever a prefix expression is
        unrecognized
        """
        message = "No prefix function to parse %s" % token_type
        self.errors.append(message)

    def _current_precedence(self) -> ExpressionType:
        """
        Gets the precendence of the current token
        """
        precendence: ExpressionType = PRECEDENCES.get(self.current_token.token_type)
        if not precendence:
            return ExpressionType.LOWEST
        return precendence

    def _current_token_is(self, token_type: TokenType) -> bool:
        """
        Check if the current token is a specific TokenType
        """
        return self.current_token.token_type == token_type

    def _peek_token_is(self, token_type: TokenType) -> bool:
        """
        Check if the next token is a specific TokenType
        """
        return self.peek_token.token_type == token_type

    def _peek_error(self, token_type: TokenType) -> None:
        """
        Add error message of unexpected tokens
        """
        message: str = "Expected type %s, got %s" % (
            token_type,
            self.peek_token.token_type,
        )
        self.errors.append(message)

    def _peek_precendence(self) -> ExpressionType:
        """
        Gets the precedence of the peek token
        """
        precedence: ExpressionType = PRECEDENCES.get(self.peek_token.token_type)
        if not precedence:
            return ExpressionType.LOWEST
        return precedence

    def _peek_expected(self, token_type: TokenType) -> bool:
        """
        This helper method is for checking if next token has the
        expected TokenType
        """
        if self._peek_token_is(token_type):
            self._next_token()
            return True
        self._peek_error(token_type)
        return False

    def _register_prefix_fun(self, token_type: TokenType, fun: Callable) -> None:
        """
        Associate a token type with a function for the
        prefix statements
        """
        self.prefix_parse_funs[token_type] = fun

    def _register_infix_fun(self, token_type: TokenType, fun: Callable) -> None:
        """
        Associate a token type with a function for the
        infix statements
        """
        self.infix_parse_funs[token_type] = fun


class ExpressionType(Enum):
    """
    These are the operator of la la lang, we assing them to a
    value in order to denote precedence
    """

    def __repr__(self):
        return "ExpressionType(%s)" % self.value

    def __str__(self):
        return str(self.value)

    def __lt__(self, other: ExpressionType):
        return self.value - other.value < 0

    LOWEST = 0
    EQUALS = 1
    LESS_GREATER = 2
    SUM = 3
    PRODUCT = 4
    PREFIX = 5
    CALL = 6


PRECEDENCES: dict[TokenType, ExpressionType] = {
    TokenType.EQ: ExpressionType.EQUALS,
    TokenType.NOT_EQ: ExpressionType.EQUALS,
    TokenType.LT: ExpressionType.LESS_GREATER,
    TokenType.GT: ExpressionType.LESS_GREATER,
    TokenType.PLUS: ExpressionType.SUM,
    TokenType.MINUS: ExpressionType.SUM,
    TokenType.SLASH: ExpressionType.PRODUCT,
    TokenType.ASTERISK: ExpressionType.PRODUCT,
}
