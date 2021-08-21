from unittest import TestCase
from tests.mocks.evaluator import *
from lalalang.lexer.lexer import Lexer
from lalalang.parser.parser import Parser
from lalalang.evaluator.evaluator import eval_3lang


class TestEvaluator(TestCase):
    def test_eval_integer(self):
        for io in INTEGER:
            source = io.get("input")
            internal = self.build_object(source)
            expected = io.get("expected")
            self.assertEqual(internal.inspect(), expected)

    def test_eval_boolean(self):
        for bo in BOOLEAN:
            source = bo.get("input")
            internal = self.build_object(source)
            expected = bo.get("expected")
            self.assertEqual(internal.inspect(), expected)

    def test_eval_prefix(self):
        for po in PREFIX:
            source = po.get("input")
            internal = self.build_object(source)
            expected = po.get("expected")
            self.assertEqual(internal.inspect(), expected)

    def test_eval_infix(self):
        for io in INFIX:
            source = io.get("input")
            internal = self.build_object(source)
            expected = io.get("expected")
            self.assertEqual(internal.inspect(), expected)

    def test_eval_conditionals(self):
        for co in CONDITIONALS:
            source = co.get("input")
            internal = self.build_object(source)
            expected = co.get("expected")
            self.assertEqual(internal.inspect(), expected)

    def build_object(self, source):
        lex = Lexer(source)
        par = Parser(lex)
        program = par.parse_program()
        return eval_3lang(program)
