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

@pytest.mark.parametrize("a, b, expected", [
    (5, 6, 11),
    (5, -5, 0),
    (8, 0, 8)
])
def test_param_somme(a, b, expected):
    assert somme(a, b) == expected


# Parametrize avec message erreur
@pytest.mark.parametrize("value, expected_match", [
    (0, r"(?i)zero"),
    (42, r"(?i)nombre"),
    (777, "Bingo")
], ids=["CAS_ZERO", "CAS_42", "BINGOOOOO"])
def test_param_pl_type(value, expected_match):
    with pytest.raises(ValueError, match=expected_match):
        pl_type_error(value)

# Parametrize avec levée ou pas
@pytest.mark.parametrize("value, should_raise", [
    (42, True),
    (0, True),
    (777, True),
    (10, False),
    (648, False),
    (625, False)
], ids=["CAS_42_SHOULD", "CAS_0_SHOULD", "CAS_777_SHOULD", "CAS_10_NOT", "CAS_648_NOT", "CAS_625_NOT"])
def test_should(value, should_raise):
    if should_raise:
        with pytest.raises(ValueError):
            pl_type_error(value)
    else:
        assert pl_type_error(value) == True


# !!!!!!!!!!!!!!!!!!!!!!!!!!
# !!!!!!!!ATTENTION!!!!!!!!!
# !!!!!!!!!!!!!!!!!!!!!!!!!!
# Voir à quel point on peut aller loin avec le parametrize, mais attention à ne pas perdre en lisibilité, il vaut mieux ne pas tout parametrer pour avoir des foncitons de tests plus lisible et facile à comprendre
@pytest.mark.parametrize("value, potential_match, error", [
    (42, r"(?i)nombre", ValueError),
    (0, r"(?i)zero", ValueError),
    (777, r"(?i)bingo", ValueError),
    ('777', r"(?i)er+eur", TypeError),
    (5, r"(?i)bruno", BrunoError),
    (10, None, None),
    (648, None, None),
    (625, None, None)
], ids=["CAS_42_SHOULD", "CAS_0_SHOULD", "CAS_777_SHOULD", "CAS_777_string_SHOULD", "CAS_5_SHOULD", "CAS_10_NOT", "CAS_648_NOT", "CAS_625_NOT"])
def test_should_OVER_KILL(value, potential_match, error):
    if error:
        with pytest.raises(error, match=potential_match):
            pl_type_error(value)
    else:
        assert pl_type_error(value) == True
