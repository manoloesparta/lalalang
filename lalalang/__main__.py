import sys
import click
import signal
from functools import wraps
from lalalang.parser.parser import Parser
from lalalang.lexer.lexer import Lexer
from lalalang.lexer.token import TokenType, Token
from lalalang.evaluator.object import Null
from lalalang.evaluator.evaluator import eval_3lang
from lalalang.evaluator.environment import Environment


@click.command()
@click.option("--mode", default="eval", help="REPL mode (lex|parse|eval)")
@click.option("--src", default=None, help="Input file with 3lang code")
def cli(mode, src):
    code = None
    if src:
        with open(src, "r") as f:
            code = f.read().replace("\n", "")
    else:
        print("Welcome to the city of stars!🌟")
        print("This is the La La Lang Programming Language v1.0.1!")

    if mode == "lex":
        lexing(code)

    elif mode == "parse":
        parsing(code)

    elif mode == "eval":
        env = Environment.empty()
        evaluating(code, env=env)


def read_eval_print_loop(func):
    def inner_function(code, **kwargs):
        if not code:
            while True:
                line = input("♪♪ > ")
                if line == "":
                    continue
                func(line, **kwargs)
        func(code, **kwargs)

    return inner_function


@read_eval_print_loop
def lexing(code):
    lex = Lexer(code)
    token = Token.empty()
    while token.token_type != TokenType.EOF:
        token = lex.next_token()
        print(repr(token))


@read_eval_print_loop
def parsing(code):
    lex = Lexer(code)
    par = Parser(lex)
    program = par.parse_program()

    if len(par.errors) == 0:
        print(program)

    [print("\t %s" % err) for err in par.errors]


@read_eval_print_loop
def evaluating(code, env):
    lex = Lexer(code)
    par = Parser(lex)
    program = par.parse_program()

    if len(par.errors) > 0:
        [print(i) for i in par.errors]
        return

    evaluated = eval_3lang(program, env)
    if evaluated and not isinstance(evaluated, Null):
        print(evaluated.inspect())


def ctrlc_handler(sig, fram):
    print("\nSee you at Seb's 😉")
    sys.exit(0)


signal.signal(signal.SIGINT, ctrlc_handler)


if __name__ == "__main__":
    cli()
