from unittest import TestCase
from lalalang.lexer import Lexer
from lalalang.parser import (
    Parser,
    Program,
    ExpressionStatement,
    Statement,
    Identifier,
    PrefixExpression,
    InfixExpression,
    IntegerLiteral,
)
from mocks.parser import (
    LET_STATEMENTS,
    RETURN_STATEMENTS,
    LET_PROGRAM,
    IDENT_EXPRESSION,
    INT_LITERAL,
    PREFIX_EXPRESSIONS,
    INFIX_EXPRESSIONS,
)


class TestParserStatements(TestCase):
    def test_let_statements(self):
        program = self.create_program(LET_STATEMENTS)
        expected_idents = ["x", "y", "foobar", "mia"]
        stms = program.statements
        for i, idents in enumerate(expected_idents):
            current = stms[i].name.value
            self.assertEqual(idents, current)

    def test_program_construction(self):
        result = "let myVar = anotherVar;"
        self.assertEqual(str(LET_PROGRAM), result)

    def test_ident_expression(self):
        program = self.create_program(IDENT_EXPRESSION)
        statement = program.statements[0]
        self.assertEqual(len(program.statements), 1)
        self.assertIsInstance(statement, ExpressionStatement)

        ident = statement.expression
        self.assertIsInstance(ident, Identifier)
        self.assertEqual(ident.value, "foobar")
        self.assertEqual(ident.token_literal(), "foobar")

    def test_int_literal(self):
        program = self.create_program(INT_LITERAL)
        statement = program.statements[0]
        self.assertEqual(len(program.statements), 1)
        self.assertIsInstance(statement, ExpressionStatement)

        literal = statement.expression
        self.assertIsInstance(literal, IntegerLiteral)
        self.assertEqual(literal.value, 5)
        self.assertEqual(literal.token_literal(), "5")

    def test_prefix_expressios(self):
        for pe in PREFIX_EXPRESSIONS:
            source = pe.get("input")
            program = self.create_program(source)

            output = pe.get("output")
            self.assertEqual(len(program.statements), 1)

            statement = program.statements[0]
            self.assertIsInstance(statement, ExpressionStatement)

            expression = statement.expression
            self.assertIsInstance(expression, PrefixExpression)
            self.assertEqual(expression.operator, output[0])
            self.assertTrue(self.validate_integer_literal(expression.right, output[1]))

    def test_infix_expressions(self):
        for ie in INFIX_EXPRESSIONS:
            source = ie.get("input")
            program = self.create_program(source)

            output = ie.get("output")
            self.assertEqual(len(program.statements), 1)

            statement = program.statements[0]
            self.assertIsInstance(statement, ExpressionStatement)

            expression = statement.expression
            self.assertIsInstance(expression, InfixExpression)
            self.assertEqual(expression.operator, output[1])

            self.assertTrue(self.validate_integer_literal(expression.left, output[0]))
            self.assertEqual(expression.operator, output[1])
            self.assertTrue(self.validate_integer_literal(expression.right, output[2]))

    def test_return_statements(self):
        program = self.create_program(RETURN_STATEMENTS)
        self.assertEqual(len(program.statements), 3)

    def create_program(self, source_code):
        lex = Lexer(source_code)
        par = Parser(lex)
        return par.parse_program()

    def validate_integer_literal(self, integer, value):
        correct_type = isinstance(integer, IntegerLiteral)
        correct_value = integer.value == value
        correct_literal = integer.token_literal() == "%s" % value

        return correct_type and correct_value and correct_literal
