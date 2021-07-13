from __future__ import annotations
from enum import Enum
from lalalang.lexer import Lexer, Token, TokenType
from .ast import (
    Program,
    Statement,
    Expression,
    Identifier,
    LetStatement,
    IntegerLiteral,
    ReturnStatement,
    ExpressionStatement,
)


class Parser:
    def __init__(self, lexer: Lexer):
        self.lexer: Lexer = lexer
        self.current_token: Token = Token.empty()
        self.peek_token: Token = Token.empty()
        self.statements: list = []
        self.errors: list = []
        self.prefix_parse_funs = dict({})
        self.infix_parse_funs = dict({})
        self.setup()

    def setup(self):
        """
        Some stuff that needs to be ready at the construction of
        this class
        """
        self.register_prefix_fun(TokenType.IDENT, self._parse_identifier)
        self.register_prefix_fun(TokenType.INT, self._parse_integer_literal)
        self._next_token()
        self._next_token()

    def __str__(self):
        return "".join(self.statements)

    def parse_program(self) -> Program:
        """
        This is the main method that will traverse the tokens
        and generate an abstract syntax tree
        """
        program = Program()
        while not self._current_token_is(TokenType.EOF):
            statement = self._parse_statement()
            if statement != None:
                program.statements.append(statement)
            self._next_token()
        return program

    def register_prefix_fun(self, token_type: TokenType, fun: PrefixParseFun) -> None:
        """
        Associate a token type with a function for the
        prefix statements
        """
        self.prefix_parse_funs[token_type] = fun

    def register_infix_fun(self, token_type: TokenType, fun: InfixParseFun) -> None:
        """
        Associate a token type with a function for the
        infix statements
        """
        self.infix_parse_funs[token_type] = fun

    def errors() -> list:
        """
        Returns all errors detected while parsing
        """
        return self.errors

    def _peek_error(self, token_type: TokenType) -> None:
        """
        Add error message of unexpected tokens
        """
        message = "Expected type %s, got %s" % (token_type, self.peek_token.token_type)
        self.errors.append(message)

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
        raise Exception("Unable to handle statement")

    def _parse_integer_literal(self) -> Expression:
        literal = IntegerLiteral(self.current_token)
        try:
            number = int(self.current_token.literal)
        except ValueError:
            self.errors.append()
        literal.value = number
        return literal


    def _parse_expression_statement(self) -> ExpressionStatement:
        """
        Here we extract expression statements from the code
        """
        statement = ExpressionStatement.empty()
        statement.expression = self._parse_expression(ExpressionType.LOWEST)

        if self._peek_token_is(TokenType.SEMICOLON):
            self._next_token()

        return statement

    def _parse_expression(self, precedence: ExpressionType) -> Expresssion:
        """
        Here we ensure we are using the correct precedence
        with the corresponding function
        """
        weight = precedence.value

        prefix = self.prefix_parse_funs[self.current_token.token_type]
        if not prefix:
            return None

        left_expression = prefix()
        return left_expression

    def _parse_identifier(self):
        """
        We return the identifier of on our current position
        """
        return Identifier(self.current_token, self.current_token.literal)

    def _parse_let_statement(self) -> LetStatement:
        """
        Handling the specific case of a let statement
        """
        statement = LetStatement.empty()
        statement.token = self.current_token

        if not self._expected_peek(TokenType.IDENT):
            raise Exception("Could not parse let statement")

        statement.name = Identifier(self.current_token, self.current_token.literal)

        while not self._current_token_is(TokenType.SEMICOLON):
            self._next_token()

        return statement

    def _parse_return_statement(self) -> ReturnStatement:
        """
        Handling the other case of return statement
        """
        statement = ReturnStatement.empty()
        statement.token = self.current_token

        self._next_token()

        while not self._current_token_is(TokenType.SEMICOLON):
            self._next_token()

        return statement

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

    def _expected_peek(self, token_type: TokenType) -> bool:
        """
        This helper method is for checking if next token has the
        expected TokenType
        """
        if self._peek_token_is(token_type):
            self._next_token()
            return True
        else:
            self._peek_error(token_type)
            return False

    def _next_token(self) -> None:
        """
        This helps us moving arround the lexer to watch one
        token ahead
        """
        self.current_token = self.peek_token
        self.peek_token = self.lexer.next_token()


class PrefixParseFun:
    def run(self):
        pass


class InfixParseFun:
    def run(self):
        pass


class ExpressionType(Enum):
    """
    These are the operator of la la lang, we assing them to a
    value in order to denote precedence
    """

    def __str__(self):
        return str(self.value)

    LOWEST = 0
    EQUALS = 1
    LESS_GREATER = 2
    SUM = 3
    PRODUCT = 4
    PREFIX = 5
    CALL = 6
