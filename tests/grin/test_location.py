# Unit tests for the provided grin.location module.


from grin import GrinLocation
import unittest



class TestGrinLocation(unittest.TestCase):
    def test_cannot_create_with_non_positive_line(self):
        for invalid_line in (0, -1, -11):
            with self.subTest(invalid_line = invalid_line):
                with self.assertRaises(ValueError):
                    GrinLocation(invalid_line, 1)


    def test_cannot_create_with_non_positive_column(self):
        for invalid_column in (0, -1, -11):
            with self.subTest(invalid_column = invalid_column):
                with self.assertRaises(ValueError):
                    GrinLocation(1, invalid_column)


    def test_can_create_with_positive_line_and_column(self):
        for line, column in ((1, 1), (18, 11), (11, 7)):
            with self.subTest(line = line, column = column):
                location = GrinLocation(line, column)
                self.assertEqual(location.line(), line)
                self.assertEqual(location.column(), column)


    def test_can_format_with_str(self):
        location = GrinLocation(11, 7)
        self.assertEqual(str(location), 'Line 11 Column 7')


    def test_can_format_with_repr(self):
        location = GrinLocation(11, 7)
        self.assertEqual(repr(location), 'GrinLocation(11, 7)')



if __name__ == '__main__':
    unittest.main()
