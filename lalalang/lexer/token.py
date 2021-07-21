from enum import Enum


class TokenType(Enum):
    """
    This are all the token types available in an
    enumeration
    """

    def __repr__(self):
        return str(self.name)

    def __str__(self):
        return str(self.value)

    # Control
    ILLEGAL = "ILLEGAL"
    EOF = "EOF"

    # Identifiers and literals
    IDENT = "IDENT"
    INT = "INT"

    # Operators
    ASSIGN = "="
    PLUS = "+"
    MINUS = "-"
    BANG = "!"
    ASTERISK = "*"
    SLASH = "/"
    LT = "<"
    GT = ">"
    EQ = "=="
    NOT_EQ = "!="

    # Delimeters
    COMMA = ","
    SEMICOLON = ";"
    LPAREN = "("
    RPAREN = ")"
    LBRACE = "{"
    RBRACE = "}"

    # Keywords
    FUNCTION = "FUNCTION"
    LET = "LET"
    TRUE = "TRUE"
    FALSE = "FALSE"
    IF = "IF"
    ELSE = "ELSE"
    RETURN = "RETURN"


class Token:
    """
    This class is for representing the object the
    lexer is producing
    """

    @staticmethod
    def empty():
        return Token(None, None)

    def __init__(self, token_type: TokenType, literal: str):
        self.token_type: TokenType = token_type
        self.literal: str = literal

    def __repr__(self):
        return "Token(%s, %s)" % (repr(self.token_type), self.literal)

    def __str__(self):
        return "Token(%s, %s)" % (self.token_type, self.literal)


KEYWORDS: dict[str, TokenType] = {
    "fun": TokenType.FUNCTION,
    "let": TokenType.LET,
    "true": TokenType.TRUE,
    "false": TokenType.FALSE,
    "if": TokenType.IF,
    "else": TokenType.ELSE,
    "return": TokenType.RETURN,
}


def lookup_identifier(key: str) -> TokenType:
    """
    This function is for getting the token type of an letters-name,
    so we can't confuse between keywords and identifiers
    """
    if key in KEYWORDS:
        return KEYWORDS[key]
    return TokenType.IDENT
