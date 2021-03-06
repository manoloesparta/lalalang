from unittest import TestCase
from lalalang.lexer.lexer import Lexer
from lalalang.lexer.token import TokenType, Token
from tests.mocks.lexer import *


class TestLexer(TestCase):
    def test_lexer_with_source_code(self):
        expected_tokens = [
            Token(TokenType.AND, "&&"),
            Token(TokenType.OR, "||"),
            Token(TokenType.LET, "let"),
            Token(TokenType.IDENT, "pi"),
            Token(TokenType.ASSIGN, "="),
            Token(TokenType.INT, "314"),
            Token(TokenType.SEMICOLON, ";"),
            Token(TokenType.FUNCTION, "fun"),
            Token(TokenType.IDENT, "area"),
            Token(TokenType.LPAREN, "("),
            Token(TokenType.IDENT, "ratio"),
            Token(TokenType.RPAREN, ")"),
            Token(TokenType.LBRACE, "{"),
            Token(TokenType.IDENT, "pi"),
            Token(TokenType.ASTERISK, "*"),
            Token(TokenType.IDENT, "ratio"),
            Token(TokenType.ASTERISK, "*"),
            Token(TokenType.IDENT, "ratio"),
            Token(TokenType.PLUS, "+"),
            Token(TokenType.INT, "0"),
            Token(TokenType.SEMICOLON, ";"),
            Token(TokenType.RBRACE, "}"),
            Token(TokenType.INT, "13"),
            Token(TokenType.SLASH, "/"),
            Token(TokenType.INT, "3"),
            Token(TokenType.GT, ">"),
            Token(TokenType.INT, "16"),
            Token(TokenType.SEMICOLON, ";"),
            Token(TokenType.IF, "if"),
            Token(TokenType.LPAREN, "("),
            Token(TokenType.INT, "10"),
            Token(TokenType.MINUS, "-"),
            Token(TokenType.INT, "8"),
            Token(TokenType.LT, "<"),
            Token(TokenType.INT, "16"),
            Token(TokenType.RPAREN, ")"),
            Token(TokenType.LBRACE, "{"),
            Token(TokenType.RETURN, "return"),
            Token(TokenType.TRUE, "true"),
            Token(TokenType.SEMICOLON, ";"),
            Token(TokenType.RBRACE, "}"),
            Token(TokenType.ELSE, "else"),
            Token(TokenType.LBRACE, "{"),
            Token(TokenType.RETURN, "return"),
            Token(TokenType.FALSE, "false"),
            Token(TokenType.SEMICOLON, ";"),
            Token(TokenType.RBRACE, "}"),
            Token(TokenType.INT, "10"),
            Token(TokenType.EQ, "=="),
            Token(TokenType.INT, "10"),
            Token(TokenType.SEMICOLON, ";"),
            Token(TokenType.INT, "10"),
            Token(TokenType.NOT_EQ, "!="),
            Token(TokenType.INT, "9"),
            Token(TokenType.SEMICOLON, ";"),
            Token(TokenType.EOF, ""),
        ]
        self.compare_results(SOURCE_CODE, expected_tokens)

    def test_delimeters(self):
        expected_tokens = [
            Token(TokenType.LPAREN, "("),
            Token(TokenType.RPAREN, ")"),
            Token(TokenType.LBRACE, "{"),
            Token(TokenType.RBRACE, "}"),
            Token(TokenType.COMMA, ","),
            Token(TokenType.SEMICOLON, ";"),
            Token(TokenType.EOF, ""),
        ]
        self.compare_results(DELIMETERS, expected_tokens)

    def test_illegal(self):
        expected_tokens = [
            Token(TokenType.ILLEGAL, "~"),
            Token(TokenType.ILLEGAL, "`"),
            Token(TokenType.ILLEGAL, "^"),
            Token(TokenType.EOF, ""),
        ]
        self.compare_results(ILLEGAL, expected_tokens)

    def test_operators(self):
        expected_tokens = [
            Token(TokenType.PLUS, "+"),
            Token(TokenType.ASSIGN, "="),
            Token(TokenType.MINUS, "-"),
            Token(TokenType.NOT, "!"),
            Token(TokenType.ASTERISK, "*"),
            Token(TokenType.SLASH, "/"),
            Token(TokenType.LT, "<"),
            Token(TokenType.GT, ">"),
            Token(TokenType.MOD, "%"),
            Token(TokenType.EOF, ""),
        ]
        self.compare_results(OPERATORS, expected_tokens)

    def test_two_character_symbols(self):
        expected_tokens = [
            Token(TokenType.AND, "&&"),
            Token(TokenType.OR, "||"),
            Token(TokenType.NOT, "!"),
            Token(TokenType.EQ, "=="),
            Token(TokenType.NOT_EQ, "!="),
            Token(TokenType.ASSIGN, "="),
            Token(TokenType.EOF, ""),
        ]
        self.compare_results(TWO_CHARACTER_SYMBOLS, expected_tokens)

    def test_identifiers(self):
        expected_tokens = [
            Token(TokenType.IDENT, "someone"),
            Token(TokenType.IDENT, "in"),
            Token(TokenType.IDENT, "the"),
            Token(TokenType.IDENT, "crowd"),
            Token(TokenType.EOF, ""),
        ]
        self.compare_results(IDENTIFIERS, expected_tokens)

    def test_numbers(self):
        expected_tokens = [
            Token(TokenType.INT, "314"),
            Token(TokenType.INT, "217"),
            Token(TokenType.INT, "161"),
            Token(TokenType.EOF, ""),
        ]
        self.compare_results(NUMBERS, expected_tokens)

    def test_keywords(self):
        expected_tokens = [
            Token(TokenType.LET, "let"),
            Token(TokenType.FUNCTION, "fun"),
            Token(TokenType.TRUE, "true"),
            Token(TokenType.FALSE, "false"),
            Token(TokenType.NULL, "null"),
            Token(TokenType.IF, "if"),
            Token(TokenType.ELSE, "else"),
            Token(TokenType.RETURN, "return"),
            Token(TokenType.EOF, ""),
        ]
        self.compare_results(KEYWORDS, expected_tokens)

    def test_strings(self):
        expected_tokens = [
            Token(TokenType.STRING, "hello world"),
            Token(TokenType.STRING, "good morning"),
            Token(TokenType.STRING, "happy jueves"),
            Token(TokenType.EOF, ""),
        ]
        self.compare_results(STRINGS, expected_tokens)

    def compare_results(self, source_code, expected_tokens):
        lex = Lexer(source_code)
        generated_tokens = lex.create_tokens()
        for et, gt in zip(expected_tokens, generated_tokens):
            self.assertEqual(et.token_type, gt.token_type)
            self.assertEqual(et.literal, gt.literal)
