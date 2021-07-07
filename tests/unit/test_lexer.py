from unittest.mock import patch
from unittest import TestCase
from lalalang.lexer.lexer import Lexer
from lalalang.lexer.token import TokenType, Token


class TestLexer(TestCase):
    def test_lexer_with_source_code(self):
        source_code = """
            let pi = 314;
            fun area(ratio) {
                pi * ratio * ratio + 0;
            }

            13 / 3 > 16;

            if(10 - 8 < 16) {
                return true;
            } else {
                return false;
            }

            10 == 10;
            10 != 9;
        """
        expected_tokens = [
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
        self.compare_results(source_code, expected_tokens)

    def test_lexer_delimeters(self):
        source_code = "(){},;"
        expected_tokens = [
            Token(TokenType.LPAREN, "("),
            Token(TokenType.RPAREN, ")"),
            Token(TokenType.LBRACE, "{"),
            Token(TokenType.RBRACE, "}"),
            Token(TokenType.COMMA, ","),
            Token(TokenType.SEMICOLON, ";"),
            Token(TokenType.EOF, ""),
        ]
        self.compare_results(source_code, expected_tokens)

    def test_lexer_control(self):
        source_code = "~`^"
        expected_tokens = [
            Token(TokenType.ILLEGAL, "~"),
            Token(TokenType.ILLEGAL, "`"),
            Token(TokenType.ILLEGAL, "^"),
            Token(TokenType.EOF, ""),
        ]
        self.compare_results(source_code, expected_tokens)

    def test_lexer_operators(self):
        source_code = "+=-!*/<>"
        expected_tokens = [
            Token(TokenType.PLUS, "+"),
            Token(TokenType.ASSIGN, "="),
            Token(TokenType.MINUS, "-"),
            Token(TokenType.BANG, "!"),
            Token(TokenType.ASTERISK, "*"),
            Token(TokenType.SLASH, "/"),
            Token(TokenType.LT, "<"),
            Token(TokenType.GT, ">"),
        ]
        self.compare_results(source_code, expected_tokens)

    def test_lexer_identifiers(self):
        source_code = "someone in the crowd"
        expected_tokens = [
            Token(TokenType.IDENT, "someone"),
            Token(TokenType.IDENT, "in"),
            Token(TokenType.IDENT, "the"),
            Token(TokenType.IDENT, "crowd"),
        ]
        self.compare_results(source_code, expected_tokens)

    def test_lexer_numbers(self):
        source_code = "314 217 161"
        expected_tokens = [
            Token(TokenType.INT, "314"),
            Token(TokenType.INT, "217"),
            Token(TokenType.INT, "161"),
        ]
        self.compare_results(source_code, expected_tokens)

    def test_lexer_keywords(self):
        source_code = "let fun"
        expected_tokens = [
            Token(TokenType.LET, "let"),
            Token(TokenType.FUNCTION, "fun"),
        ]
        self.compare_results(source_code, expected_tokens)

    def test_correct_string_format(self):
        token = Token(TokenType.EOF, "")
        self.assertEqual(str(token), 'Token(TokenType.EOF, "")')

    def compare_results(self, source_code, expected_tokens):
        lex = Lexer(source_code)
        for token in expected_tokens:
            current = lex.next_token()
            self.assertEqual(token.token_type, current.token_type)
            self.assertEqual(token.literal, current.literal)
