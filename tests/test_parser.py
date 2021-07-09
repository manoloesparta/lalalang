from unittest import TestCase
from lalalang.parser import Parser
from lalalang.lexer import Lexer
from mocks.parser import (
    LET_STATEMENTS,
    RETURN_STATEMENTS,
)


class TestParser(TestCase):
    def test_let_statements(self):
        lex = Lexer(LET_STATEMENTS)
        par = Parser(lex)
        program = par.parse_program()

    def test_return_statements(self):
        pass

    def compare_results(self, source_code, expected_ast):
        pass
