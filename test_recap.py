from unittest.mock import Mock

import pytest


class PaymentError(Exception):
    pass


class PaymentService:
    def pay(self, user, price):
        # pleins de truc de vrai payment
        # Debiter la carte bleu
        # une fois que c'est fait
        if not user.get('active'):
            raise PaymentError("Le payment n'as pas pu avoir lieu")
        # IF PAYMENT REUSSI
        return True


def payment_order(user, confirmation, payment_service, price):
    if not confirmation:
        return {"user": user, "result": False}

    payment_result = payment_service.pay(user, price)

    if payment_result:
        user["plan"] = 'PREMIUM'

    return {"user": user, "result": True}


@pytest.fixture
def user_payment():
    return {
        "name": "  No é   ",
        "plan": "FREE",
        "active": True
    }

@pytest.fixture
def user_payment_not_active():
    return {
        "name": "  No é   ",
        "plan": "FREE",
        "active": False
    }

def test_payment(user_payment):
    mock_payement = Mock()
    mock_payement.pay.return_value = True

    result = payment_order(user_payment, True, mock_payement, 25)

    # On teste que quand le payment est validé, le plan du user est bien passé à premium
    assert result.get('user').get('plan') == "PREMIUM"

    mock_payement.pay.assert_called_once()

def test_payment_not_done_when_no_confirmation(user_payment):
    mock_payement = Mock()
    mock_payement.pay.return_value = True

    result = payment_order(user_payment, False, mock_payement, 25)

    assert result.get('user').get('plan') == "FREE"

    mock_payement.pay.assert_not_called()

def test_payment_error(user_payment_not_active):
    mock_payement = Mock()
    mock_payement.pay.side_effect = PaymentError("Le payment n'as pas pu avoir lieu")

    with pytest.raises(PaymentError):
        payment_order(user_payment_not_active, True, mock_payement, 25)
