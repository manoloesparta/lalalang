from enum import Enum


class Token:
    """
    This class is for representing the object the
    lexer is producing
    """

    def __init__(self, token_type: str, literal: str):
        self.token_type = token_type
        self.literal = literal

    def __str__(self):
        return 'Token(%s, "%s")' % (self.token_type, self.literal)

    @staticmethod
    def empty_token():
        return Token(None, None)


class TokenType(Enum):
    """
    This are all the token types available in an
    enumeration
    """

    # Control
    ILLEGAL = "ILLEGAL"
    EOF = "EOF"

    # Identifiers and literals
    IDENT = "IDENT"
    INT = "INT"

    # Operators
    ASSIGN = "="
    PLUS = "+"

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


KEYWORDS = {"fun": TokenType.FUNCTION, "let": TokenType.LET}


def lookup_identifier(key: str):
    """
    This function is for getting the token type of an alpha name,
    so we can't confuse between keywords and identifiers
    """
    if key in KEYWORDS:
        return KEYWORDS[key]
    return TokenType.IDENT
