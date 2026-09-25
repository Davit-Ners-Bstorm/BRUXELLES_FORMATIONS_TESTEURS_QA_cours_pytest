import pytest

def somme(a, b):
    resultat = a + b
    return resultat

def my_min(a, b):
    return a - b

# TEST
# if somme(5, 6) == 11:
#     print('PASS')
# else:
#     print('FAIL')

# if somme(2, 6) == 8:
#     print('PASS')
# else:
#     print('FAIL')


def test_somme():
    assert somme(5, 6) == 11
    assert somme(-5, 5) == 0
    assert somme(0, 8) == 8

def test_somme_aaa():
    a = 5
    b = 7
    result = somme(a, b)
    assert result == 12

def test_my_min():
    assert my_min(8, 5) == 3
    assert my_min(8, 8) == 0
    assert my_min(10, 8) == 2


def my_div(a, b):
    return a / b

def test_my_div():
    assert my_div(8, 2) == 4
    assert my_div(9, 3) == 3

def test_my_div_zero_error():
    with pytest.raises(ZeroDivisionError, match="division by zero"):
        my_div(8, 0)

# print(my_div(8, 0))

# msg_error_pif.py
ERROR_WHILE_STRING = "La value ne peut pas être un string"



def function_au_pif(value):
    if type(value) == str:
        raise ValueError(ERROR_WHILE_STRING)
    if type(value) == bool:
        raise ValueError('La value ne peut pas être un bool')
    return True

def test_pif_str():
    with pytest.raises(ValueError, match=ERROR_WHILE_STRING):
        function_au_pif(True)



















# Revision 1-3
from booking import ticket_price

def test_nominal_ticket():
    assert ticket_price('vip') == 7500
    assert ticket_price('standard') == 3500
    assert ticket_price('early_bird') == 2495

def test_nominal_ticket_2():
    assert ticket_price('vip') == 7500
    assert ticket_price('standard') == 3500
    assert ticket_price('early_bird') == 2495

def test_ticket_error():
    with pytest.raises(ValueError):
        ticket_price("mauvais_categorie")

class BrunoError(Exception):
    pass


def pl_type_error(value):
    if value == 0:
        raise ValueError("ZERO ZERO ZERO")
    if value == 42:
        raise ValueError("Beau nombre")
    if value == 777:
        raise ValueError("Bingo")
    if type(value) == str:
        raise TypeError("errrrrreur")
    if value == 5:
        raise BrunoError("BRUNOOOOOOO")
    return True

def test_type_match_0():
    with pytest.raises(ValueError, match=r"(?i)zero"):
        pl_type_error(0)

def test_type_mauvais_type():
    with pytest.raises(TypeError):
        pl_type_error("hey je suis un string")

def test_bruno():
    with pytest.raises(BrunoError, match=r"(?i)bruno"):
        pl_type_error(5)




