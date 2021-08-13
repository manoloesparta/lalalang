from __future__ import annotations
from lalalang.lexer.token import TokenType, Token
from lalalang.parser.nodes import Node, Statement, Expression


class Program(Node):
    """
    This class is the root node of every abstract
    syntax tree
    """

    @staticmethod
    def with_statements(statements: list[Statement]) -> Program:
        program: Program = Program()
        program.statements = statements
        return program

    def __init__(self):
        self.statements: list[Statement] = []

    def __repr__(self):
        conversion: list[str] = [repr(i) for i in self.statements]
        return "\n".join(conversion)

    def __str__(self):
        conversion: list[str] = [str(i) for i in self.statements]
        return "".join(conversion)

    def token_literal(self) -> str:
        if len(self.statements) > 0:
            return self.statements[0].token_literal()
        return ""

    def add_statement(self, statement: Statement):
        self.statements.append(statement)


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
        return "Identifier(%s, %s)" % (repr(self.token), self.value)

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
            repr(self.token),
            repr(self.name),
            repr(self.value),
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
        return "ReturnStatement(%s, %s)" % (repr(self.token), repr(self.return_value))

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
        return "ExpressionStatement(%s, %s)" % (repr(self.token), repr(self.expression))

    def __str__(self):
        if not self.expression:
            return ""
        return str(self.expression)

    def token_literal(self) -> str:
        return self.token.literal

    def statement_node(self) -> None:
        pass


class IntegerLiteral(Expression):
    """
    This is for representing the actual numbers, it is
    a expression so that they can return themselves as the
    value represented.
    """

    @staticmethod
    def empty():
        return IntegerLiteral(None, None)

    def __init__(self, token: Token, value: int):
        self.token: Token = token
        self.value: int = value

    def __repr__(self):
        return "IntegerLiteral(%s,%s)" % (repr(self.token), self.value)

    def __str__(self):
        return str(self.value)

    def token_literal(self) -> str:
        return self.token.literal

    def expression_node(self):
        pass


class PrefixExpression(Expression):
    """
    This is any expression that has an operator before the
    operand for now we only have two prefix operators - and !.
    """

    @staticmethod
    def empty():
        return PrefixExpression(None, None, None)

    def __init__(self, token: Token, operator: str, right: Expression):
        self.token: Token = token
        self.operator: str = operator
        self.right: Expression = right

    def __repr__(self):
        return "PrefixExpression(%s,%s,%s)" % (
            repr(self.token),
            self.operator,
            repr(self.right),
        )

    def __str__(self):
        return "(%s %s)" % (self.operator, str(self.right))

    def token_literal(self) -> str:
        return self.token.literal

    def expression_node(self):
        pass


class InfixExpression(Expression):
    """
    This is any expression that has an operator sitting between
    its operands, here are most arithmetic operations
    """

    @staticmethod
    def empty():
        return InfixExpression(None, None, None, None)

    def __init__(
        self, token: Token, left: Expression, operator: str, right: Expression
    ):
        self.token: Token = token
        self.left: Expression = left
        self.operator: str = operator
        self.right: Expression = right

    def __repr__(self):
        return "InfixExpression(%s,%s,%s,%s)" % (
            repr(self.token),
            repr(self.left),
            repr(self.operator),
            repr(self.right),
        )

    def __str__(self):
        return "(%s %s %s)" % (str(self.left), self.operator, str(self.right))

    def token_literal(self) -> str:
        return self.token.literal

    def expression_node(self):
        pass


class BooleanLiteral(Expression):
    """
    Here we only store the simplest for of data, a boolean they
    are represented with the literals 'true' or 'false'
    """

    def __init__(self, token: Token, value: bool):
        self.token: Token = token
        self.value: bool = value

    def __repr__(self):
        return "BooleanLiteral(%s, %s)" % (repr(self.token), self.value)

    def __str__(self):
        return str(self.token.literal)

    def token_literal(self):
        return self.token.literal

    def expression_node(self):
        pass


class IfExpression(Expression):
    """
    This are conditionals which has an expression that evaluates to
    a boolean (also known as predicate), a consequence or alternative
    that executes depending the condition
    """

    @staticmethod
    def empty():
        return IfExpression(None, None, None, None)

    def __init__(
        self,
        token: Token,
        condition: Expression,
        consequence: BlockStatement,
        alternative: BlockStatement,
    ):
        self.token: Token = token
        self.condition: Expression = condition
        self.consequence: BlockStatement = consequence
        self.alternative: BlockStatement = alternative

    def __repr__(self):
        return "IfExpression(%s, %s, %s, %s)" % (
            repr(self.token),
            repr(self.condition),
            repr(self.consequence),
            repr(self.alternative),
        )

    def __str__(self):
        if self.alternative:
            return "if %s %s else %s" % (
                str(self.condition),
                str(self.consequence),
                str(self.alternative),
            )
        return "if %s %s" % (str(self.condition), str(self.consequence))

    def token_literal(self) -> str:
        return self.token.literal

    def expression_node(self):
        pass


class BlockStatement(Statement):
    """
    This is a construct for storing various statements that for
    example is the body of an if expression or function literal
    """

    @staticmethod
    def empty():
        return BlockStatement(None, None)

    def __init__(self, token: Token, statements: list[Statement]):
        self.token: Token = token
        self.statements: list[Statement] = statements

    def __repr__(self):
        conv_stmnts = [repr(i) for i in self.statements]
        return "BlockStatement(%s, %s)" % (str(self.token), "".join(conv_stmnts))

    def __str__(self):
        conv_stmnts = [str(i) for i in self.statements]
        return "".join(conv_stmnts)

    def token_literal(self) -> str:
        return self.token.literal

    def statement_node(self):
        pass


class FunctionLiteral(Expression):
    """
    This is fore storing the a function, with its name and parameters
    (also known as signature) and the body, which is a BlockStatement
    """

    @staticmethod
    def empty():
        return FunctionLiteral(None, None, None)

    def __init__(
        self, token: Token, parameters: list[Identifier], body: BlockStatement
    ):
        self.token: Token = token
        self.parameters: list[Identifier] = parameters
        self.body: BlockStatement = body

    def __repr__(self):
        convs_params = [repr(i) for i in self.parameters]
        return "FunctionLiteral(%s, %s, %s)" % (
            repr(self.token),
            "".join(convs_params),
            repr(self.body),
        )

    def __str__(self):
        convs_params = [str(i) for i in self.parameters]
        return "%s(%s) %s" % (
            self.token_literal(),
            ",".join(convs_params),
            str(self.body),
        )

    def token_literal(self) -> str:
        return self.token.literal

    def expression_node(self):
        pass


class CallExpression(Expression):
    """
    Here are the expressions that are using our declared function
    literals, we only store a the funcion used with its arguments
    """

    @staticmethod
    def empty():
        return CallExpression(None, None, None)

    def __init__(self, token: Token, function: Expression, arguments: list[Expression]):
        self.token: Token = token
        self.function: Expression = function
        self.arguments: list[Expression] = arguments

    def __repr__(self):
        convs_args = [repr(i) for i in self.arguments]
        return "CallExpression(%s, %s, %s)" % (
            repr(self.token),
            repr(self.function),
            ", ".join(convs_args),
        )

    def __str__(self):
        convs_args = [str(i) for i in self.arguments]
        return "%s(%s)" % (str(self.function), ", ".join(convs_args))

    def token_literal(self) -> str:
        return self.token.literal

    def expression_node(self):
        pass
