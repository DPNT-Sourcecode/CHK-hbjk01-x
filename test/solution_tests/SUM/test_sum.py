from solutions.SUM import sum_solution
from pytest import mark

@mark.parametrize("x,y,expected" [
    (1, 2, 3),
    (0, 0, 0),
    (0, 1, 1),
    (100, 100, 200)
])
def test_sum_positive_cases(self, x, y, expected):
    assert sum_solution.compute(x, y) == expected


