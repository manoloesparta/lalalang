from unittest import TestCase
from lalalang.lexer.lexer import Lexer
from lalalang.lexer.token import TokenType
from lalalang.parser.parser import Parser
from lalalang.parser.ast import *
from tests.mocks.parser import *


class TestParserStatements(TestCase):
    def test_program_construction(self):
        result = "let myVar = anotherVar;"
        self.assertEqual(str(CONSTRUCTED_PROGRAM), result)

    def test_let_statements(self):
        for ls in LET_STATEMENTS:
            source = ls.get("input")
            program = self.create_program(source)

            output = ls.get("expected")
            self.assertEqual(len(program.statements), 1)

            statement = program.statements[0]
            self.assertIsInstance(statement, LetStatement)

            expression = statement.value
            self.assertIsInstance(expression, Expression)

            self.assertEqual(str(statement.name), output[0])
            self.assertEqual(str(expression), output[1])

    def test_return_statements(self):
        for rs in RETURN_STATEMENTS:
            source = rs.get("input")
            program = self.create_program(source)

            output = rs.get("expected")
            self.assertEqual(len(program.statements), 1)

            statement = program.statements[0]
            self.assertIsInstance(statement, ReturnStatement)

            expression = statement.return_value
            self.assertEqual(str(expression), output)

    def test_identifiers_expressions(self):
        for ie in IDENT_EXPRESSION:
            source = ie.get("input")
            program = self.create_program(source)

            output = ie.get("expected")
            self.assertEqual(str(program), output)
            self.assertEqual(len(program.statements), 1)

            statement = program.statements[0]
            self.assertIsInstance(statement, ExpressionStatement)

            expression = statement.expression
            self.assertIsInstance(expression, Identifier)

    def test_int_literal(self):
        for il in INT_LITERALS:
            source = il.get("input")
            program = self.create_program(source)

            output = il.get("expected")
            self.assertEqual(len(program.statements), 1)

            statement = program.statements[0]
            self.assertIsInstance(statement, ExpressionStatement)

            expression = statement.expression
            self.assertTrue(self.validate_integer_literal(expression, output))

    def test_prefix_expressions(self):
        for pe in PREFIX_EXPRESSIONS:
            source = pe.get("input")
            program = self.create_program(source)

            output = pe.get("expected")
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

            output = ie.get("expected")
            self.assertEqual(len(program.statements), 1)

            statement = program.statements[0]
            self.assertIsInstance(statement, ExpressionStatement)

            expression = statement.expression
            self.assertIsInstance(expression, InfixExpression)
            self.assertEqual(expression.operator, output[1])

            self.assertTrue(self.validate_integer_literal(expression.left, output[0]))
            self.assertEqual(expression.operator, output[1])
            self.assertTrue(self.validate_integer_literal(expression.right, output[2]))

    def test_precedence(self):
        for pe in PRECEDENCE_EXPRESSIONS:
            source = pe.get("input")
            program = self.create_program(source)

            expected = pe.get("expected")
            self.assertEqual(str(program), expected)

    def test_boolean_expressions(self):
        for be in BOOLEAN_EXPRESSION:
            source = be.get("input")
            program = self.create_program(source)

            expected = be.get("expected")
            self.assertEqual(str(program), expected)

            statement = program.statements[0]
            self.assertIsInstance(statement, ExpressionStatement)

            expression = statement.expression
            self.assertIsInstance(expression, BooleanLiteral)

    def test_grouped_expressions(self):
        for ge in GROUPED_EXPRESSIONS:
            source = ge.get("input")
            program = self.create_program(source)

            expected = ge.get("expected")
            self.assertEqual(str(program), expected)

    def test_if_expressions(self):
        for ie in IF_EXPRESSIONS:
            source = ie.get("input")
            program = self.create_program(source)

            expected = ie.get("expected")
            self.assertEqual(len(program.statements), 1)

            statement = program.statements[0]
            self.assertIsInstance(statement, ExpressionStatement)

            expression = statement.expression
            self.assertIsInstance(expression, IfExpression)

            consequence = expression.consequence
            self.assertIsInstance(consequence, BlockStatement)

            self.assertEqual(str(expression.condition), expected[0])
            self.assertEqual(str(expression.consequence), expected[1])
            self.assertEqual(str(expression.alternative), expected[2])

    def test_function_literals(self):
        for fl in FUNCTION_LITERALS:
            source = fl.get("input")
            program = self.create_program(source)

            expected = fl.get("expected")
            self.assertEqual(len(program.statements), 1)

            statement = program.statements[0]
            self.assertIsInstance(statement, ExpressionStatement)

            expression = statement.expression
            self.assertIsInstance(expression, FunctionLiteral)

            body = expression.body
            self.assertIsInstance(body, BlockStatement)

            self.assertEqual(str(expression), expected[0])
            self.assertEqual(str(body), expected[1])

    def test_call_expressions(self):
        for ce in CALL_EXPRESSIONS:
            source = ce.get("input")
            program = self.create_program(source)

            expected = ce.get("expected")
            self.assertEqual(len(program.statements), 1)

            statement = program.statements[0]
            self.assertIsInstance(statement, ExpressionStatement)

            expression = statement.expression
            self.assertIsInstance(expression, CallExpression)

            self.assertEqual(str(expression.function), expected[0])
            self.assertEqual(str(expression), expected[1])

    def create_program(self, source_code):
        lex = Lexer(source_code)
        par = Parser(lex)
        return par.parse_program()

    def validate_integer_literal(self, integer, value):
        correct_type = isinstance(integer, IntegerLiteral)
        correct_value = integer.value == value
        correct_literal = integer.token_literal() == "%s" % value
        return correct_type and correct_value and correct_literal
