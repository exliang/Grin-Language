# A parser for the Grin language, which takes a sequence of strings containing
# lines of Grin code and returns a corresponding sequence in which every
# element is a list of GrinTokens.  Importantly, though, this only succeeds
# if there are no parse errors (e.g., a statement that doesn't start with a
# keyword, a GOTO statement that's missing a target, etc.) on the line.  When
# a parse error is detected, a GrinParseError is raised instead.

from typing import Callable, Iterable, NoReturn
from grin.lexing import to_tokens
from grin.location import GrinLocation
from grin.token import GrinTokenKind, GrinToken

# parsing puts all the tokens in list

class GrinParseError(Exception):
    """Raised when a parse error is found during parsing, with an error message
    describing the issue, along with the location where the error was detected."""

    def __init__(self, message: str, location: GrinLocation):
        formatted = f'Error during parsing: {str(location)}: {message}'
        super().__init__(formatted)
        self._location = location


    def location(self) -> GrinLocation:
        """Returns the location where the error was detected"""
        return self._location



def parse(lines: Iterable[str]) -> Iterable[list[GrinToken]]:
    """Given a sequence of strings containing lines of Grin code, generates a
    corresponding sequence of lists of GrinTokens, each being the tokens
    found on the corresponding line of input code.

    Raises a GrinParseError when there is a parse error on a line, so that
    you'll only ever receive valid lists of GrinTokens from this function."""

    for line_number, line in enumerate(lines, start = 1):
        tokens = _parse_line(line, line_number)

        if len(tokens) == 1 and tokens[0].kind() == GrinTokenKind.DOT:
            return

        yield tokens


def _parse_line(line: str, line_number: int) -> list[GrinToken]:
    tokens = list(to_tokens(line, line_number))
    index = 0


    def _raise_error_on_token(message: str, token: GrinToken) -> NoReturn:
        raise GrinParseError(message, token.location())


    def _raise_error_at_end_of_line(message: str) -> NoReturn:
        raise GrinParseError(message, GrinLocation(line_number, len(line) + 1))


    def _token_is(*kinds: GrinTokenKind) -> bool:
        return index < len(tokens) and tokens[index].kind() in kinds


    def _expect(*kinds: GrinTokenKind) -> None:
        if not _token_is(*kinds):
            message = ', '.join(str(kind) for kind in kinds)

            if index >= len(tokens):
                _raise_error_at_end_of_line(message)
            else:
                _raise_error_on_token(message, tokens[index])


    def _parse_label() -> None:
        nonlocal index

        if _token_is(GrinTokenKind.IDENTIFIER):
            index += 1
            _expect(GrinTokenKind.COLON)
            index += 1


    def _parse_variable_update() -> None:
        nonlocal index
        _expect(GrinTokenKind.IDENTIFIER)
        index += 1
        _parse_value()


    def _parse_print() -> None:
        nonlocal index
        _parse_value()


    def _parse_input() -> None:
        nonlocal index
        _expect(GrinTokenKind.IDENTIFIER)
        index += 1


    def _parse_jump() -> None:
        nonlocal index
        _parse_jump_target()

        if _token_is(GrinTokenKind.IF):
            index += 1
            _parse_value()
            _parse_comparison_operator()
            _parse_value()


    def _parse_empty() -> None:
        pass


    _BODY_PARSERS: dict[GrinTokenKind, Callable[[], None]] = {
        GrinTokenKind.LET: _parse_variable_update,
        GrinTokenKind.PRINT: _parse_print,
        GrinTokenKind.INNUM: _parse_input,
        GrinTokenKind.INSTR: _parse_input,
        GrinTokenKind.ADD: _parse_variable_update,
        GrinTokenKind.SUB: _parse_variable_update,
        GrinTokenKind.MULT: _parse_variable_update,
        GrinTokenKind.DIV: _parse_variable_update,
        GrinTokenKind.GOTO: _parse_jump,
        GrinTokenKind.GOSUB: _parse_jump,
        GrinTokenKind.RETURN: _parse_empty,
        GrinTokenKind.END: _parse_empty
    }


    def _parse_body() -> None:
        nonlocal index

        if tokens[index].kind() in _BODY_PARSERS:
            kind = tokens[index].kind()
            index += 1
            _BODY_PARSERS[kind]()
        else:
            _raise_error_on_token('Statement keyword expected', tokens[index])


    def _parse_jump_target() -> None:
        nonlocal index

        _expect(
            GrinTokenKind.LITERAL_INTEGER, GrinTokenKind.LITERAL_STRING,
            GrinTokenKind.IDENTIFIER)

        index += 1


    def _parse_value() -> None:
        nonlocal index

        _expect(
            GrinTokenKind.LITERAL_INTEGER, GrinTokenKind.LITERAL_FLOAT,
            GrinTokenKind.LITERAL_STRING, GrinTokenKind.IDENTIFIER)

        index += 1


    def _parse_comparison_operator() -> None:
        nonlocal index

        _expect(
            GrinTokenKind.EQUAL, GrinTokenKind.NOT_EQUAL,
            GrinTokenKind.LESS_THAN, GrinTokenKind.LESS_THAN_OR_EQUAL,
            GrinTokenKind.GREATER_THAN, GrinTokenKind.GREATER_THAN_OR_EQUAL)

        index += 1


    if len(tokens) == 0:
        _raise_error_at_end_of_line('Program lines cannot be empty')
    elif len(tokens) == 1 and tokens[0].kind() == GrinTokenKind.DOT:
        return tokens

    _parse_label()

    if index >= len(tokens):
        _raise_error_at_end_of_line('Statement body expected')

    _parse_body()

    if index < len(tokens):
        _raise_error_on_token('Extra tokens after statement end', tokens[index])

    return tokens



__all__ = [parse.__name__, GrinParseError.__name__]
