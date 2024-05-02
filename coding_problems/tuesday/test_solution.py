import codewars_test as test
from solution import longest_palindrome


def dotest(s, expected):
    test.assert_equals(longest_palindrome(s), expected, f"With s = \"{s}\"")


@test.describe("Tests")
def test_group():
    @test.it("Sample tests")
    def test_case():
        for s, expected in (
            ("a", 1),
            ("aa", 2),
            ("baa", 2),
            ("aab", 2),
            ("abcdefghba", 1),
            ("baablkj12345432133d", 9),
        ):
            dotest(s, expected)
