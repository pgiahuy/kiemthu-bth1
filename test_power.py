import time

from utils import power
import pytest


def test_0():
    assert power(88, 0) == 1


def test_mu_duong_1():
    assert power(2, 1) == 2


def test_mu_duong_2():
    assert power(2, 3) == 8


def test_mu_am():
    assert power(2, -1) == 0.5
    assert power(2, -2) == 0.25


@pytest.mark.parametrize("x,n,expected", [
    (2, 0, 1),
    (3, 1, 3),
    (5, 2, 25),
    (2, -1, 0.5),
    (4, -2, 0.0625),
])
def test_others(x, n, expected):
    assert power(x, n) == expected


def test_x_0():
    with pytest.raises(ZeroDivisionError):
        power(0, -5)



@pytest.mark.timeout(2)
def test_timeout():
    time.sleep(3)