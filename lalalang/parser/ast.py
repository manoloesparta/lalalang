from lalalang.lexer.token import TokenType, Token
from .nodes import Node, Statement, Expression


class Program(Node):
    """
    This class is the root node of every abstract
    syntax tree
    """

    def __init__(self):
        self.statements: list = []

    def __str__(self):
        conversion = [str(i) for i in self.statements]
        return "\n".join(conversion)

    def token_literal(self) -> str:
        if len(self.statements) > 0:
            return self.statements[0].token_literal()
        return ""


class Identifier(Expression):
    """
    This is the class for dealing with the names or
    identifier of a let expression
    """

    @staticmethod
    def empty():
        return Identifier(None, None)

    def __init__(self, token: Token, value: str):
        self.token: Token = token
        self.value: str = value

    def __str__(self):
        return "Identifier(%s, %s)" % (str(self.token), self.value)

    def token_literal(self) -> str:
        return self.token.literal

    def expression_node(self) -> None:
        pass


class LetStatement(Statement):
    """
    This is for let statements, binding names or
    identifiers to values
    """

    @staticmethod
    def empty():
        return LetStatement(None, None)

    def __init__(self, token: Token, name: Identifier):
        self.token: Token = token
        self.name: Identifier = name

    def __str__(self):
        return "LetStatement(%s, %s)" % (str(self.token), str(self.name))

    def token_literal(self) -> str:
        return self.token.literal

    def statement_node(self) -> None:
        pass


class ReturnStatement(Statement):
    """
    This is for return statements, for reusing
    values made inside functions
    """

    @staticmethod
    def empty():
        return ReturnStatement(None, None)

    def __str__(self):
        return "ReturnStatement(%s, %s)" % (str(self.token), str(self.return_value))

    def __init__(self, token: Token, return_value: Expression):
        self.token: Token = token
        self.return_value: Expression = return_value

    def token_literal(self) -> str:
        return self.token.literal

    def statement_node(self) -> None:
        pass
