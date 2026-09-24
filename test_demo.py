import pytest

def my_sum(a, b):
    return a + b


def my_sub(a, b):
    return a - b

def my_div(a, b):
    return a / b

def fonction_au_pif(value):
    if type(value) == str:
        raise TypeError("Le type ne peut pas être string!!!")
    if type(value) == bool:
        raise TypeError("Le type ne peut pas être bool!!!")
    return True

# print(my_sum(5, 6) == 11)

def test_my_sum():
    assert my_sum(5, 6) == 11
    assert my_sum(5, -5) == 0


def test_my_sub():
    assert my_sub(8, 5) == 3
    assert my_sub(10, 0) == 10

def test_my_div():
    assert my_div(8, 2) == 4
    assert my_div(9, 3) == 3


def test_my_div_zero_error():
    with pytest.raises(ZeroDivisionError):
        my_div(8, 0)

def test_pif_string():
    with pytest.raises(TypeError, match="Le type ne peut pas être string!!!"):
        fonction_au_pif("hello je suis un string")

def test_pif_bool():
    with pytest.raises(TypeError, match="bool"):
        fonction_au_pif(True)
