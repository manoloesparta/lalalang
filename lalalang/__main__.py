import sys
import click
import signal
from .lexer import Lexer, TokenType, Token
from .parser import Parser


@click.command()
@click.option("--mode", default="parser", help="REPL mode (lexer|parser)")
def cli(mode):
    print("Welcome to the city of stars!🌟")
    print("This is the La La Lang Programming Languag v0.2!")
    if mode == "parser":
        repl(parsing)
    elif mode == "lexer":
        repl(lexing)


def lexing(line):
    lex = Lexer(line)
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


def repl(fun):
    while line := input("♪♪ > "):
        fun(line)


def ctrlc_handler(sig, fram):
    print("\nSee you at Seb's 😉")
    sys.exit(0)


signal.signal(signal.SIGINT, ctrlc_handler)


if __name__ == "__main__":
    cli()
