import sys
import click
import signal
from lalalang.parser.parser import Parser
from lalalang.lexer.lexer import Lexer
from lalalang.lexer.token import TokenType, Token
from lalalang.evaluator.evaluator import eval_3lang


@click.command()
@click.option("--mode", default="eval", help="REPL mode (lex|parse|eval)")
@click.option("--src", default=None, help="Input file with 3lang code")
def cli(mode, src):

    code = None
    if not src:
        print("Welcome to the city of stars!🌟")
        print("This is the La La Lang Programming Languag v0.3.5!")
    else:
        with open(src, "r") as f:
            code = f.read().replace("\n", "")

    if mode == "lex":
        repl(lexing, code)
    elif mode == "parse":
        repl(parsing, code)
    elif mode == "eval":
        repl(evaluating, code)


def lexing(code):
    lex = Lexer(code)
    token = Token.empty()
    while token.token_type != TokenType.EOF:
        token = lex.next_token()
        print(repr(token))


def parsing(code):
    lex = Lexer(code)
    par = Parser(lex)
    program = par.parse_program()

    if len(par.errors) == 0:
        print(program)
    else:
        [print("\t %s" % err) for err in par.errors]


def evaluating(code):
    lex = Lexer(code)
    par = Parser(lex)
    program = par.parse_program()

    if len(par.errors) > 0:
        [print(i) for i in par.errors]
        return

    evaluated = eval_3lang(program)
    if evaluated:
        print(evaluated.inspect())


def repl(fun, source):
    if not source:
        while line := input("♪♪ > "):
            fun(line)
    fun(source)


def ctrlc_handler(sig, fram):
    print("\nSee you at Seb's 😉")
    sys.exit(0)


signal.signal(signal.SIGINT, ctrlc_handler)


if __name__ == "__main__":
    cli()
