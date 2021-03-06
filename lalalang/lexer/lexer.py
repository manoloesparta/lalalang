from lalalang.lexer.token import TokenType, Token, lookup_identifier


class Lexer:
    """
    This class recieves source code as input and returns the tokens
    that represent it
    """

    def __init__(self, source: str):
        self.source: str = source
        self.position: int = 0
        self.peek_position: int = 0
        self.char: str = ""

        self._read_char()

    def create_tokens(self) -> list[Token]:
        """This is for returning the tokens identified in the source code"""
        all_tokens: list[Token] = []

        while not self.position >= len(self.source) + 1:
            all_tokens.append(self._next_token())

        return all_tokens

    def _next_token(self) -> Token:
        """
        This is the main method that is traversing the source code and generating
        the tokens, this was made for being used multiple times
        """

        self._skip_whitespace()
        new_token: Token = Token.empty()

        # Comments
        if self.char == "#":
            self._skip_comment()
            return self._next_token()

        # One character symbols
        if self.char == ";":
            new_token = Token(TokenType.SEMICOLON, self.char)
        elif self.char == "(":
            new_token = Token(TokenType.LPAREN, self.char)
        elif self.char == ")":
            new_token = Token(TokenType.RPAREN, self.char)
        elif self.char == ",":
            new_token = Token(TokenType.COMMA, self.char)
        elif self.char == "{":
            new_token = Token(TokenType.LBRACE, self.char)
        elif self.char == "}":
            new_token = Token(TokenType.RBRACE, self.char)
        elif self.char == "+":
            new_token = Token(TokenType.PLUS, self.char)
        elif self.char == "-":
            new_token = Token(TokenType.MINUS, self.char)
        elif self.char == "*":
            new_token = Token(TokenType.ASTERISK, self.char)
        elif self.char == "/":
            new_token = Token(TokenType.SLASH, self.char)
        elif self.char == "%":
            new_token = Token(TokenType.MOD, self.char)
        elif self.char == "<":
            new_token = Token(TokenType.LT, self.char)
        elif self.char == ">":
            new_token = Token(TokenType.GT, self.char)
        elif self.char == '"':
            string: str = self._read_string()
            new_token = Token(TokenType.STRING, string)
        elif self.char == "":
            new_token = Token(TokenType.EOF, "")

        # Two different characters symbols
        elif self.char == "=":
            if self._peek_char() == "=":
                char = self.char
                self._read_char()
                new_token = Token(TokenType.EQ, char + self.char)
            else:
                new_token = Token(TokenType.ASSIGN, self.char)
        elif self.char == "!":
            if self._peek_char() == "=":
                char = self.char
                self._read_char()
                new_token = Token(TokenType.NOT_EQ, char + self.char)
            else:
                new_token = Token(TokenType.NOT, self.char)

        # Two equal characters symbols
        elif self.char == "&" and self._peek_char() == "&":
            char = self.char
            self._read_char()
            new_token = Token(TokenType.AND, char + self.char)
        elif self.char == "|" and self._peek_char() == "|":
            char = self.char
            self._read_char()
            new_token = Token(TokenType.OR, char + self.char)

        # Numbers and identifiers
        else:
            if self.char.isalpha():
                literal: str = self._read_identifier()
                new_token = Token(lookup_identifier(literal), literal)
                return new_token
            elif self.char.isdigit():
                new_token = Token(TokenType.INT, self._read_number())
                return new_token
            else:
                new_token = Token(TokenType.ILLEGAL, self.char)

        self._read_char()
        return new_token

    def _read_char(self) -> None:
        """This method is for traversing the source code character by character"""
        if self.peek_position >= len(self.source):
            self.char = ""
        else:
            self.char = self.source[self.peek_position]
        self.position = self.peek_position
        self.peek_position += 1

    def _read_identifier(self) -> str:
        """
        This helper method extracts any indentifier from the source code like
        variable or function names
        """
        start: int = self.position
        while self.char.isalpha():
            self._read_char()
        return self.source[start : self.position]

    def _read_number(self) -> str:
        """This helper method extracts integers from the source code"""
        start: int = self.position
        while self.char.isdigit():
            self._read_char()
        return self.source[start : self.position]

    def _read_string(self) -> str:
        """This helper method is for extracting strings from the source code"""
        start: int = self.position + 1
        self._read_char()
        while self.char not in ['"', ""]:
            self._read_char()
        return self.source[start : self.position]

    def _skip_whitespace(self) -> None:
        """
        This helper method advances the position until no whitespace is
        encountered
        """
        while self.char.isspace():
            self._read_char()

    def _skip_comment(self):
        """Advances the position until it found an end of line"""
        while self.char not in ["\n", ""]:
            self._read_char()

    def _peek_char(self) -> str:
        """
        This helper method is somewhat like _read_char() without the increment,
        it's for seeing what's next, not to move around
        """
        if self.peek_position >= len(self.source):
            return ""
        return self.source[self.peek_position]
