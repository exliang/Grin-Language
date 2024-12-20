# Classes used to describe tokens in a Grin program.
# * GrinToken, which describes one token in its entirety.
# * GrinTokenKind, which identifies a type of token, such as a literal integer
#   or the keyword SUB.
# * GrinTokenCategory, which kinds of tokens into broader categories.

from enum import Enum
from grin.location import GrinLocation
from typing import Any



class GrinTokenCategory(Enum):
    """A categorization of Grin tokens, which combines multiple kinds of
    Grin tokens together when they serve similar purposes."""
    COMPARISON_OPERATOR = 1
    IDENTIFIER = 2
    KEYWORD = 3
    LITERAL_VALUE = 4
    PUNCTUATION = 5



class GrinTokenKind(Enum):
    """Identifies a kind of Grin token."""
    ADD = (1, GrinTokenCategory.KEYWORD)
    COLON = (2, GrinTokenCategory.PUNCTUATION)
    DIV = (3, GrinTokenCategory.KEYWORD)
    DOT = (4, GrinTokenCategory.PUNCTUATION)
    END = (5, GrinTokenCategory.KEYWORD)
    EQUAL = (6, GrinTokenCategory.COMPARISON_OPERATOR)
    GOSUB = (7, GrinTokenCategory.KEYWORD)
    GOTO = (8, GrinTokenCategory.KEYWORD)
    GREATER_THAN = (9, GrinTokenCategory.COMPARISON_OPERATOR)
    GREATER_THAN_OR_EQUAL = (10, GrinTokenCategory.COMPARISON_OPERATOR)
    IDENTIFIER = (11, GrinTokenCategory.IDENTIFIER)
    IF = (12, GrinTokenCategory.KEYWORD)
    INNUM = (13, GrinTokenCategory.KEYWORD)
    INSTR = (14, GrinTokenCategory.KEYWORD)
    LESS_THAN = (15, GrinTokenCategory.COMPARISON_OPERATOR)
    LESS_THAN_OR_EQUAL = (16, GrinTokenCategory.COMPARISON_OPERATOR)
    LET = (17, GrinTokenCategory.KEYWORD)
    LITERAL_FLOAT = (18, GrinTokenCategory.LITERAL_VALUE)
    LITERAL_INTEGER = (19, GrinTokenCategory.LITERAL_VALUE)
    LITERAL_STRING = (20, GrinTokenCategory.LITERAL_VALUE)
    MULT = (21, GrinTokenCategory.KEYWORD)
    NOT_EQUAL = (22, GrinTokenCategory.COMPARISON_OPERATOR)
    PRINT = (23, GrinTokenCategory.KEYWORD)
    RETURN = (24, GrinTokenCategory.KEYWORD)
    SUB = (25, GrinTokenCategory.KEYWORD)


    def __init__(self, index: int, category: GrinTokenCategory):
        self._index = index
        self._category = category


    def index(self) -> int: #identities the token, 1, 2, etc.
        """An index associated with this kind of token, mainly to differentiate
        it from all the others."""
        return self._index


    def category(self) -> GrinTokenCategory:
        """How this kind of token is categorized."""
        return self._category



class GrinToken:
    """A single token in a Grin program"""
    def __init__(
            self, *,
            kind: GrinTokenKind,
            text: str,
            location: GrinLocation,
            value: Any = None):
        self._kind = kind
        self._text = text
        self._location = location
        self._value = value


    def kind(self) -> GrinTokenKind: # might need to call this
        return self._kind


    def text(self) -> str: # might need to call this
        return self._text


    def location(self) -> GrinLocation: # might need to call this
        return self._location


    def value(self) -> Any: # might need to call this
        return self._value


    def __eq__(self, other):
        return isinstance(other, GrinToken) \
                and self._kind == other._kind \
                and self._text == other._text \
                and self._location == other._location \
                and self._value == other._value



__all__ = [
    GrinToken.__name__,
    GrinTokenCategory.__name__,
    GrinTokenKind.__name__
]
