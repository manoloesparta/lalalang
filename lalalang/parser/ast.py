from lalalang.lexer.token import TokenType, Token
from .nodes import Node, Statement, Expression


class Program(Node):
    """
    This class is the root node of every abstract
    syntax tree
    """

    @staticmethod
    def with_statements(statements: list):
        program = Program()
        program.statements = statements
        return program

    def __init__(self):
        self.statements: list = []

    def __repr__(self):
        conversion = [str(i) for i in self.statements]
        return "\n".join(conversion)

    def __str__(self):
        conversion = [str(i) for i in self.statements]
        return "".join(conversion)

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

    def __repr__(self):
        return "Identifier(%s, %s)" % (str(self.token), self.value)

    def __str__(self):
        return self.value

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
        return LetStatement(None, None, None)

    def __init__(self, token: Token, name: Identifier, value: Expression):
        self.token: Token = token
        self.name: Identifier = name
        self.value: Expression = value

    def __repr__(self):
        return "LetStatement(%s, %s, %s)" % (
            str(self.token),
            str(self.name),
            str(self.value),
        )

    def __str__(self):
        if not self.value:
            return "%s %s = ;" % (self.token_literal(), str(self.name))
        return "%s %s = %s;" % (self.token_literal(), str(self.name), str(self.value))

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

    def __init__(self, token: Token, return_value: Expression):
        self.token: Token = token
        self.return_value: Expression = return_value

    def __repr__(self):
        return "ReturnStatement(%s, %s)" % (str(self.token), str(self.return_value))

    def __str__(self):
        return "%s %s;" % (self.token_literal(), str(self.return_value))

    def token_literal(self) -> str:
        return self.token.literal

    def statement_node(self) -> None:
        pass


class ExpressionStatement(Statement):
    """
    This is for every line of code that returns a value,
    this is necessary to have simpler expressions to print
    the result
    """

    @staticmethod
    def empty():
        return ExpressionStatement(None, None)

    def __init__(self, token: Token, expression: Expression):
        self.token: Token = token
        self.expression: Expression = expression

    def __repr__(self):
        return "ExpressionStatement(%s, %s)" % (str(self.token), str(self.expression))

    def __str__(self):
        if not self.expression:
            return ""
        return str(self.expression)

    def token_literal(self) -> str:
        return self.token.literal

    def statement_node(self) -> None:
        pass

class IntegerLiteral:
    
    @staticmethod
    def empyt():
        return IntegerLiteral(None, None)
    
    def __init__(self, token: Token, value: int):
        self.token: Token = token
        self.value: int = value

    def expression_node(self):
        pass

    def token_literal(self) -> str:
        return self.token.literal
    