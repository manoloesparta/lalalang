from lalalang.lexer import Lexer, Token, TokenType
from .ast import Program, Statement, LetStatement


class Parser:

    current_token: Token = Token.empty_token()
    peek_token: Token = Token.empty_token()

    def __init__(self, lexer: Lexer):
        self.lexer = lexer
        self._next_token()
        self._next_token()

    def parse_program(self) -> Program:
        """
        This is the main method that will traverse the tokens
        and generate an abstract syntax tree
        """
        program = Program()
        while self.current_token.token_type != TokenType.EOF:
            statement = self._parse_statement()
            if statement != None:
                program.statements.append(statement)
            self._next_token()
        return program

    def _parse_statement(self) -> Statement:
        if self.current_token.token_type == TokenType.LET:
            return self._parse_let_statement()
        return None

    def _parse_let_statement(self) -> LetStatement:
        statement = LetStatement(self.current_token)

        if not self._expected_peek(TokenType.IDENT):
            return None

        while not self._current_token_is(TokenType.SEMICOLON):
            self._next_token()

        return statement

    def _current_token_is(self, token_type: TokenType) -> bool:
        return self.current_token.token_type == token_type

    def _peek_token_is(self, token_type: TokenType) -> bool:
        return self.peek_token.token_type == token_type

    def _expected_peek(self, token_type: TokenType) -> bool:
        if self._peek_token_is(token_type):
            self._next_token()
            return True
        return False

    def _next_token(self) -> None:
        """
        This helps us moving arround the lexer to watch one
        token ahead
        """
        self.current_token = self.peek_token
        self.peek_token = self.lexer.next_token()
