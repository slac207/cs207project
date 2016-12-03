from pytest import raises
from lazy import lazy_add, lazy_mul, LazyOperation, lazy


def test_type():
    assert isinstance(lazy_add(2, 3), LazyOperation) is True
    assert isinstance(lazy_mul(2, 3), LazyOperation) is True


def test_operation():
    assert lazy_add(3, 4).eval() == 7
    assert lazy_mul(3, 4).eval() == 12


def test_composition():
    assert lazy_add(3, lazy_add(3, 2)).eval() == 8
    assert lazy_mul(3, lazy_mul(2, 5)).eval() == 30
    assert lazy_add(4, lazy_mul(3, -1)).eval() == 1
    assert lazy_mul(3, lazy_add(-1, 3)).eval() == 6


@lazy
def lazy_add_kw(x, y, z=0):
    if z == 0:
        return -99
    return x + y


def test_kw():
    assert lazy_add_kw(2, 3).eval() == -99
    assert lazy_add_kw(2, 3, z=0).eval() == -99
    assert lazy_add_kw(2, 3, z=1).eval() == 5


def test_kw_composition():
    assert lazy_add_kw(2, 3, z=lazy_add_kw(2, 3, z=1)).eval() == 5
    assert lazy_add_kw(2, 3, z=lazy_add_kw(2, -2, z=1)).eval() == -99
