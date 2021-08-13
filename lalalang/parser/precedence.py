from __future__ import annotations
from enum import Enum
from lalalang.lexer.token import TokenType


class ExpressionPrecedence(Enum):
    """
    These are the operator of la la lang, we assing them to a
    value in order to denote precedence
    """

    def __repr__(self):
        return "ExpressionPrecedence(%s)" % self.value

    def __str__(self):
        return str(self.value)

    def __lt__(self, other: ExpressionPrecedence):
        return self.value - other.value < 0

    LOWEST = 0
    EQUALS = 1
    LESS_GREATER = 2
    SUM = 3
    PRODUCT = 4
    PREFIX = 5
    CALL = 6


PRECEDENCES: dict[TokenType, ExpressionPrecedence] = {
    TokenType.EQ: ExpressionPrecedence.EQUALS,
    TokenType.NOT_EQ: ExpressionPrecedence.EQUALS,
    TokenType.LT: ExpressionPrecedence.LESS_GREATER,
    TokenType.GT: ExpressionPrecedence.LESS_GREATER,
    TokenType.PLUS: ExpressionPrecedence.SUM,
    TokenType.MINUS: ExpressionPrecedence.SUM,
    TokenType.SLASH: ExpressionPrecedence.PRODUCT,
    TokenType.ASTERISK: ExpressionPrecedence.PRODUCT,
    TokenType.LPAREN: ExpressionPrecedence.CALL,
}
