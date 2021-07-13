from unittest import TestCase
from lalalang.lexer import Lexer
from lalalang.parser import (
    Parser,
    Program,
    ExpressionStatement,
    Statement,
    Identifier,
    IntegerLiteral,
)
from mocks.parser import (
    LET_STATEMENTS,
    RETURN_STATEMENTS,
    LET_PROGRAM,
    IDENT_EXPRESSION,
    INT_LITERAL,
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

    def test_return_statements(self):
        program = self.create_program(RETURN_STATEMENTS)
        self.assertEqual(len(program.statements), 3)

    def create_program(self, source_code):
        lex = Lexer(source_code)
        par = Parser(lex)
        return par.parse_program()
