from lalalang.lexer.token import TokenType, Token
from .nodes import Node, Statement, Expression


class Program(Node):
    """
    This class is the root node of every abstract
    syntax tree
    """

    statements: list = []

    def token_literal(self) -> str:
        if len(self.statements) > 0:
            return self.statements[0].token_literal()
        return ""


class Identifier(Expression):
    """
    This is the class for dealing with the names or
    identifier of a let expression
    """

    token: Token = Token.empty_token()
    value: str = ""

    def token_literal(self) -> str:
        return self.token.literal

    def expression_node(self) -> None:
        pass


class LetStatement(Statement):
    """
    This is for let statements, binding names or
    identifiers to values
    """

    token: Token = Token.empty_token()
    name: Identifier = Identifier()

    def __init__(self, token: Token):
        self.token = token

    @staticmethod
    def empty_let_statement():
        return LetStatement(None)

    def token_literal(self) -> str:
        return self.token.literal

    def statement_node(self) -> None:
        pass
