from lalalang.lexer import Lexer
from lalalang.parser import Parser
from lalalang.evaluator import eval_3lang
from lalalang.evaluator.environment import Environment
from lalalang.evaluator.object import Null


def run(code):
    """Run source code directly with this function"""
    lex = Lexer(code)
    tokens = lex.create_tokens()
    par = Parser(tokens)
    program = par.parse_program()

    if len(par.errors) > 0:
        [print(i) for i in par.errors]
        return

    env = Environment.empty()
    evaluated = eval_3lang(program, env)
    if evaluated and not isinstance(evaluated, Null):
        return evaluated.inspect()
