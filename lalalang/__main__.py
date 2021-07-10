import sys
import signal
import pretty_errors
from .lexer import Lexer, TokenType, Token


def main():
    print("Welcome to the city of stars!🌟")
    print("This is the La La Lang Programming Language!")
    start_repl(lexing)


def lexing(line):
    lex = Lexer(line)
    token = Token.empty()
    while token.token_type != TokenType.EOF:
        token = lex.next_token()
        print(token)


def start_repl(fun):
    while line := input("♪♪ > "):
        fun(line)


def ctrlc_handler(sig, fram):
    print("\nSee you at Seb's 😉")
    sys.exit(0)


signal.signal(signal.SIGINT, ctrlc_handler)


if __name__ == "__main__":
    main()
