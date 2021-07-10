from lalalang.lexer import Lexer, Token, TokenType
from .ast import Program, Statement, LetStatement, Identifier, ReturnStatement


class Parser:
    def __init__(self, lexer: Lexer):
        self.lexer: Lexer = lexer
        self.current_token: Token = Token.empty()
        self.peek_token: Token = Token.empty()
        self.statements: list = []
        self.errors: list = []

        self._next_token()
        self._next_token()

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

    def errors() -> list:
        return self.errors

    def _peek_error(self, token_type: TokenType) -> None:
        message = "Expected type %s, got %s" % (token_type, self.peek_token.token_type)
        self.errors.append(message)

    def _parse_statement(self) -> Statement:
        """
        Here are the conditionals to handle any statement defined
        by us
        """
        if self._current_token_is(TokenType.LET):
            return self._parse_let_statement()
        elif self._current_token_is(TokenType.RETURN):
            return self._parse_return_statement()
        raise Exception("Unable to handle statement")

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
