# A lexer for the Grin language, whose job is to take a string containing one
# line of Grin code and generate a sequence of GrinTokens from it.

from collections import defaultdict
from grin.location import GrinLocation
from grin.token import GrinTokenCategory, GrinTokenKind, GrinToken
from typing import Iterable, NoReturn



class GrinLexError(Exception):
    """Raised when lexing fails, with an error message explaining the issue
    and a GrinLocation specifying where the error was detected."""

    def __init__(self, message: str, location: GrinLocation):
        formatted = f'Error during lexing: {str(location)}: {message}'
        super().__init__(formatted)
        self._message = message
        self._location = location


    def location(self) -> GrinLocation:
        """Returns the location where the error was detected"""
        return self._location



_TOKEN_KIND_MAP = defaultdict(
    lambda: GrinTokenKind.IDENTIFIER,
    [(kind.name, kind)
     for kind in GrinTokenKind.__members__.values()
     if kind.category() == GrinTokenCategory.KEYWORD])


KEYWORDS = frozenset(_TOKEN_KIND_MAP.keys())



def to_tokens(line: str, line_number: int) -> Iterable[GrinToken]:
    """Given a line of Grin code and its line number, generates a sequence of
    GrinTokens corresponding to each of the lexemes found on the line.

    Raises a GrinLexError when there is a lexical error on the line."""

    index = 0
    start = 0


    def _make_token(kind: GrinTokenKind, value: object = None) -> GrinToken:
        return GrinToken(
            kind = kind, text = line[start:index],
            location = GrinLocation(line_number, start + 1), value = value)


    def _raise_error(message: str) -> NoReturn:
        raise GrinLexError(message, GrinLocation(line_number, index + 1))


    while True:
        while index < len(line) and line[index].isspace():
            index += 1

        if index == len(line):
            break

        start = index

        if line[index].isalpha():
            index += 1

            while index < len(line) and line[index].isalnum():
                index += 1

            yield _make_token(_TOKEN_KIND_MAP[line[start:index]], line[start:index])
        elif line[index] == '"':
            index += 1

            while index < len(line) and line[index] != '"':
                index += 1

            if index == len(line):
                _raise_error('Newline in string literal')
            else:
                index += 1
                yield _make_token(GrinTokenKind.LITERAL_STRING, line[(start + 1):(index - 1)])
        elif line[index] == '-' or line[index].isdigit():
            is_negated = line[index] == '-'
            index += 1
            digits = 0 if is_negated else 1

            while index < len(line) and line[index].isdigit():
                index += 1
                digits += 1

            if is_negated and digits == 0:
                _raise_error('Negation must be followed by at least one digit')
            elif index < len(line) and line[index] == '.':
                index += 1

                while index < len(line) and line[index].isdigit():
                    index += 1

                yield _make_token(GrinTokenKind.LITERAL_FLOAT, float(line[start:index]))
            else:
                yield _make_token(GrinTokenKind.LITERAL_INTEGER, int(line[start:index]))
        elif line[index] == ':':
            index += 1
            yield _make_token(GrinTokenKind.COLON)
        elif line[index] == '.':
            index += 1
            yield _make_token(GrinTokenKind.DOT)
        elif line[index] == '=':
            index += 1
            yield _make_token(GrinTokenKind.EQUAL)
        elif line[index] == '<':
            index += 1

            if index < len(line) and line[index] == '>':
                index += 1
                yield _make_token(GrinTokenKind.NOT_EQUAL)
            elif index < len(line) and line[index] == '=':
                index += 1
                yield _make_token(GrinTokenKind.LESS_THAN_OR_EQUAL)
            else:
                yield _make_token(GrinTokenKind.LESS_THAN)
        elif line[index] == '>':
            index += 1

            if index < len(line) and line[index] == '=':
                index += 1
                yield _make_token(GrinTokenKind.GREATER_THAN_OR_EQUAL)
            else:
                yield _make_token(GrinTokenKind.GREATER_THAN)
        else:
            _raise_error('Invalid character')



__all__ = [
    'KEYWORDS',
    to_tokens.__name__,
    GrinLexError.__name__
]
