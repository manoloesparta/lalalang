from unittest import TestCase
from tests.mocks.evaluator import *
from lalalang.lexer.lexer import Lexer
from lalalang.parser.parser import Parser
from lalalang.evaluator.evaluator import eval_3lang


class TestEvaluator(TestCase):
    def test_integer(self):
        self.check_evaluation(INTEGER)

    def test_boolean(self):
        self.check_evaluation(BOOLEAN)

    def test_prefix(self):
        self.check_evaluation(PREFIX)

    def test_infix(self):
        self.check_evaluation(INFIX)

    def test_conditionals(self):
        self.check_evaluation(CONDITIONALS)

    def test_return(self):
        self.check_evaluation(RETURN)

    def test_errors(self):
        self.check_evaluation(ERRORS)

    def check_evaluation(self, cases):
        for case in cases:
            source = case.get("input")
            internal = self.build_object(source)
            expected = case.get("expected")
            self.assertEqual(internal.inspect(), expected)

    def build_object(self, source):
        lex = Lexer(source)
        par = Parser(lex)
        program = par.parse_program()
        return eval_3lang(program)
