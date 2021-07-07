#!venv/bin/python
import sys
import signal
from lalalang.lexer import Lexer, TokenType, Token


def main():
    print("Welcome to the city of stars!🌟")
    print("This is the La La Lang Programming Language!")
    start_repl()


def start_repl():
    while line := input("♪♪ > "):
        lex = Lexer(line)
        token = Token.empty_token()
        while token.token_type != TokenType.EOF:
            token = lex.next_token()
            print(token)


def ctrlc_handler(sig, fram):
    print("\nSee you at Seb's 😉")
    sys.exit(0)


signal.signal(signal.SIGINT, ctrlc_handler)


if __name__ == "__main__":
    main()
