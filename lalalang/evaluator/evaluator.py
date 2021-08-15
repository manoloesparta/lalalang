from lalalang.parser.ast import *
from lalalang.evaluator.object import Object, Integer, Boolean, Null

# References
TRUE: Boolean = Boolean(True)
FALSE: Boolean = Boolean(False)
NULL: Null = Null()


def eval_3lang(node: Node) -> Object:
    """
    This is executing a tree walk interpreter, doing a
    postorder traverse over the ast
    """

    # Statements
    if isinstance(node, Program):
        return eval_statements(node.statements)

    # Expressions
    elif isinstance(node, ExpressionStatement):
        return eval_3lang(node.expression)

    # Internal objects
    elif isinstance(node, IntegerLiteral):
        return Integer(node.value)
    elif isinstance(node, BooleanLiteral):
        return boolean_reference(node.value)

    return None


def eval_statements(statements: list[Statement]) -> Object:
    """
    The root of every program is a list of statements, not
    the ast nodes, we need to start from the root
    """
    for statement in statements:
        result: Object = eval_3lang(statement)
    return result


def boolean_reference(value: bool) -> Boolean:
    """Return the Boolean reference instead of creating new value"""
    if value:
        return TRUE
    return FALSE
