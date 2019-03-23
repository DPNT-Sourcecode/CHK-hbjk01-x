from lib.solutions.SUM import sum_solution
from pytest import mark, raises

@mark.parametrize("x,y,expected", [
    (1, 2, 3),
    (0, 0, 0),
    (0, 1, 1),
    (100, 100, 200)
])
def test_sum_positive_cases(x, y, expected):
    assert sum_solution.compute(x, y) == expected

@mark.parametrize("x,y", [
    (-1, 2),
    (0, -3),
    (1, 101),
    ("sup", ""),
    (None, None)
])
def test_sum_negative_cases(x, y):
    with raises(Exception):
        sum_solution.compute(x, y)
