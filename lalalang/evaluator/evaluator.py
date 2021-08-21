from lalalang.parser.ast import *
from lalalang.evaluator.object import *

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
    elif isinstance(node, ExpressionStatement):
        return eval_3lang(node.expression)
    elif isinstance(node, BlockStatement):
        return eval_block_statement(node)
    elif isinstance(node, ReturnStatement):
        value = eval_3lang(node.return_value)
        return ReturnValue(value)

    # Expressions
    elif isinstance(node, PrefixExpression):
        right = eval_3lang(node.right)
        return eval_prefix_expression(node.operator, right)
    elif isinstance(node, InfixExpression):
        left = eval_3lang(node.left)
        right = eval_3lang(node.right)
        return eval_infix_expression(node.operator, left, right)
    elif isinstance(node, IfExpression):
        return eval_if_expression(node)

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
        if isinstance(result, ReturnValue):
            return result.value
    return result


def eval_block_statement(block: BlockStatement) -> Object:
    """
    This is somewhat similar to eval_statements except that is
    looking for any value to return and stop in the statement
    """
    for statement in block.statements:
        result: Object = eval_3lang(statement)
        if not result and isinstance(result, ReturnValue):
            return result
    return result


def eval_prefix_expression(operator: str, right: Object) -> Object:
    """We support evaluating the two only prefix operators"""
    if operator == "!":
        return eval_bang_operator_expression(right)
    elif operator == "-":
        return eval_minus_operator_expression(right)
    return NULL


def eval_bang_operator_expression(right: Object) -> Object:
    """
    If the object is null or false, it should evaluate to true, any
    othe expression or object should be false
    """
    if right in [FALSE, NULL]:
        return TRUE
    return FALSE


def eval_minus_operator_expression(right: Object) -> Object:
    """Just reverse the value is already in the object"""
    if isinstance(right, Integer):
        return Integer(-right.value)

    if right.object_type() != ObjectType.INTEGER:
        return NULL

    return NULL


def eval_infix_expression(operator: str, left: Object, right: Object) -> Object:
    """Main method for evaluating infix expression"""
    if (
        left.object_type() == ObjectType.INTEGER
        and right.object_type() == ObjectType.INTEGER
    ):
        return eval_integer_infix_expression(operator, left, right)
    elif operator == "==":
        return boolean_reference(left == right)
    elif operator == "!=":
        return boolean_reference(left != right)

    return NULL


def eval_integer_infix_expression(operator: str, left: Object, right: Object) -> Object:
    """
    Here we evaulate relational and arithmetic operations
    with integers
    """
    if not (isinstance(left, Integer) and isinstance(right, Integer)):
        return NULL

    left_value: int = left.value
    right_value: int = right.value

    # Arithmetic
    if operator == "+":
        return Integer(left_value + right_value)
    elif operator == "-":
        return Integer(left_value - right_value)
    elif operator == "*":
        return Integer(left_value * right_value)
    elif operator == "/":
        return Integer(left_value // right_value)

    # Relational
    elif operator == "<":
        return boolean_reference(left_value < right_value)
    elif operator == ">":
        return boolean_reference(left_value > right_value)
    elif operator == "==":
        return boolean_reference(left_value == right_value)
    elif operator == "!=":
        return boolean_reference(left_value != right_value)

    return NULL


def eval_if_expression(expression: IfExpression) -> Object:
    """
    Here we parse the condition and depending on the result we
    execute the consequence or alternative
    """
    predicate: Object = eval_3lang(expression.condition)

    if is_truthy(predicate):
        return eval_3lang(expression.consequence)
    elif expression.alternative is not None:
        return eval_3lang(expression.alternative)

    return NULL


def is_truthy(obj: Object) -> bool:
    """Here we check which kind of objects evaluate to true or false"""
    if obj in [NULL, FALSE]:
        return False
    return True


def boolean_reference(value: bool) -> Boolean:
    """Return the Boolean reference instead of creating new value"""
    if value:
        return TRUE
    return FALSE
