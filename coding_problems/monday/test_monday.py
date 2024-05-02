import codewars_test as test
from solution import light_bulbs

sample_test_cases = [
    ([0, 1, 1, 0, 1, 1], 2,  [1, 0, 1, 1, 0, 1]),
    ([0, 0, 1, 1, 1], 5,  [1, 1, 1, 0, 1]),
    ([1, 0, 1, 1, 0, 1, 1, 0, 1], 10,  [0, 1, 1, 0, 1, 1, 0, 1, 1]),
    ([1, 1, 0, 0, 0, 1, 1, 1, 1, 1], 20,  [1, 0, 0, 0, 0, 0, 1, 1, 0, 1]),
    ([1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1], 50,
     [0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0]),
]


@test.describe('Sample tests')
def sample_tests():
    @test.it('')
    def _():
        for lights, n, expected in sample_test_cases:
            msg = f'light_bulbs({lights}, {n})'
            test.assert_equals(light_bulbs(lights, n), expected, msg)
