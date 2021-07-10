from unittest import TestCase
from lalalang.parser import Parser, Program, Statement
from lalalang.lexer import Lexer
from mocks.parser import (
    LET_STATEMENTS,
    RETURN_STATEMENTS,
    PROGRAM_STRING,
)


class TestParserStatements(TestCase):
    def test_let_statements(self):
        program = self.create_program(LET_STATEMENTS)
        expected_idents = ["x", "y", "foobar", "mia"]
        stms = program.statements
        for i, idents in enumerate(expected_idents):
            current = stms[i].name.value
            self.assertEqual(idents, current)

    def test_return_statements(self):
        program = self.create_program(RETURN_STATEMENTS)
        expected_returns = 3 * ["return"]
        self.assertEqual(len(program.statements), 3)

    def create_program(self, source_code):
        lex = Lexer(source_code)
        par = Parser(lex)
        return par.parse_program()


class TestParserExpressions(TestCase):
    pass
