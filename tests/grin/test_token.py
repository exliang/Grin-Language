
# Unit tests for the provided grin.token module.


from grin.token import GrinTokenKind, GrinToken
import unittest



class GrinTokenKindTest(unittest.TestCase):
    def test_indexes_are_unique(self):
        indexes = set(kind.index() for kind in GrinTokenKind.__members__.values())
        self.assertEqual(len(indexes), len(GrinTokenKind.__members__))
