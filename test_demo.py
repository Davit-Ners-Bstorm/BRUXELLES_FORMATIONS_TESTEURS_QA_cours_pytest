from unittest.mock import Mock

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

@pytest.mark.parametrize("a, b, expected", [
    (5, 6, 11),
    (-5, 5, 0),
    (0, 8, 8)
], ids=["cas_normal", "cas_zero", "cas_zero_2"])
def test_somme_param(a, b, expected):
    assert somme(a, b) == expected

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




def test_user_age(user):
    assert user["age"] == 254

def create_user(name, email_service):
    # ......... Creation User .........
    status = email_service.send(name)
    for i in range(5):
        email_service.salsa()
    return status["ok"]

def test_create_email_sent():
    mock_email_service = Mock()
    mock_email_service.send.return_value = {"ok": True}

    result = create_user("Maxime", mock_email_service)

    assert result is True

    mock_email_service.send.assert_called_once()
    mock_email_service.send.assert_called_once_with("Maxime")

    assert mock_email_service.salsa.call_count == 5

def payment(pay_service, result):
    if result:
        pay_service.pay_pas_error()
    else:
        pay_service.pay_error()

def test_pay():
    mock_pay = Mock()
    mock_pay.pay_error.side_effect = ConnectionError("Payment refusé, erreur de connexion")
    with pytest.raises(ConnectionError):
        payment(mock_pay, False)
