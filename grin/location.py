# Defines a class called GrinLocation, whose objects describe a location within
# the text of a Grin program (i.e., a line number and a column number).

class GrinLocation:
    """Describes a location within the text of a Grin program"""

    def __init__(self, line, column):
        if int(line) < 1:
            raise ValueError(f'Line in location cannot be non-positive, was {line}')

        if int(column) < 1:
            raise ValueError(f'Column in location cannot be non-positive, was {column}')

        self._line = line
        self._column = column


    def line(self) -> int:
        return self._line


    def column(self) -> int: # call this (LET A 4 works but LET 4 A doesn't)
        return self._column


    def __str__(self) -> str:
        return f'Line {self._line} Column {self._column}'


    def __repr__(self) -> str:
        return f'GrinLocation({self._line}, {self._column})'


    def __eq__(self, other):
        return isinstance(other, GrinLocation) \
                and self._line == other._line \
                and self._column == other._column



__all__ = [GrinLocation.__name__]
