"""
conftest.py — fixtures partagées entre plusieurs fichiers de test.

Vide au départ : vous y déplacerez vos fixtures au Bloc 5, quand plusieurs
fichiers auront besoin des mêmes données ou des mêmes mocks.
Pytest découvre ce fichier automatiquement : aucune importation nécessaire.
"""

from unittest.mock import Mock
from pytest import fixture as fixture
import pytest


@pytest.fixture
def get_user():
    fixture_user =  {"name": "Leslie", "formation": "QA test"}
    return fixture_user

@pytest.fixture
def get_confirm():
    return {"result": True}

@pytest.fixture
def db(base_donne):
    db = base_donne.open()
    print("Conexion")
    yield db
    print('Deconexion')


@pytest.fixture(scope="session")
def email_mock_service():
    mock_email = Mock()
    mock_email.error.side_effect = ValueError("hehe je suis une erreure")
    mock_email.send.return_value = {"ok": True}
    mock_email.display.return_value = {"ok": True}

    return mock_email


@fixture
def no_ticket_item_dict():
    return [
        {
        "category": "vip",
        "quantity": 0
        }
    ]

@fixture
def ticket5_item_dict():
    return [
        {
        "category": "standard",
        "quantity": 5
        }
    ]


@fixture
def ticket6_item_dict():
    return [
        {
            "category": "early_bird",
            "quantity": 6
        }
    ]


@fixture
def over_ticket_item_dict():
    return [
        {
            "category": "vip",
        "quantity": 7
        }
    ]


@fixture
def active_user_dict():
    return {
        "active": True,
        "email": "raph@eventflow.com",
        "payment_token": "magielol156"
    }

@fixture
def inactive_user_dict():
    return {
        "active": False,
        "email": "sign@eventflow.com",
        "payment_token": "ftg5541"
    }


@fixture
def event1_dict():
    return {
        "available": 6
    }


@fixture
def event2_dict():
    return {
        "available": 2
    }


@fixture
def event3_dict():
    return {
        "available": 6
    }


@fixture
def yield_example():
    print("Test before yield")

    yield

    print("Test after yield")

