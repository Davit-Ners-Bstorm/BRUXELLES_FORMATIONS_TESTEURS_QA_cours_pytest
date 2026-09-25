"""
conftest.py — fixtures partagées entre plusieurs fichiers de test.

Vide au départ : vous y déplacerez vos fixtures au Bloc 5, quand plusieurs
fichiers auront besoin des mêmes données ou des mêmes mocks.
Pytest découvre ce fichier automatiquement : aucune importation nécessaire.
"""

from unittest.mock import Mock

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
