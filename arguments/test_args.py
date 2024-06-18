import unittest
from args import *

class ArgsTest(unittest.TestCase):
    def test_matching_amount_of_arguments_goes_correctly(self):
        Args('a,b', "-a true -b false")

    def test_mismatching_amount_of_arguments_gives_parse_exception(self):
        with self.assertRaises(ParseException):
            Args('a,b', "-a true")

    def test_parse_and_retrieve_boolean(self):
        sut = Args('a', "-a true")
        self.assertEqual(True, sut.getB('a'))

    def test_parse_and_retrieve_two_booleans(self):
        sut = Args('a,b', "-a true -b false")
        self.assertEqual(True, sut.getB('a'))
        self.assertEqual(False, sut.getB('b'))

    def test_parse_and_retrieve_boolean_invalid_boolean(self):
        with self.assertRaises(ParseException):
            Args('a', "-a 12")

    def test_parse_and_retrieve_string(self):
        sut = Args('hallo*', '-hallo "Hello World"')
        self.assertEqual("Hello World", sut.getS('hallo'))

    def test_parse_and_retrieve_two_strings(self):
        sut = Args('hallo*,b*', '-hallo "Hello World" -b "Bob"')
        self.assertEqual("Hello World", sut.getS('hallo'))
        self.assertEqual("Bob", sut.getS('b'))

    def test_parse_and_retrieve_string_invalid_string(self):
        with self.assertRaises(ParseException):
            Args('hallo*,b*', '-hallo "Hello World" -b Bob')

    def test_parse_and_retrieve_two_types(self):
        sut = Args('hello,b*', '-hello false -b "Bob"')
        self.assertEqual(False, sut.getB('hello'))
        self.assertEqual("Bob", sut.getS('b'))


if __name__ == '__main__':
    unittest.main()
