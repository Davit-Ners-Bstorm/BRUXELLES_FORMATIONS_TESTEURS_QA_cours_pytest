"""
conftest.py — fixtures partagées entre plusieurs fichiers de test.

Vide au départ : vous y déplacerez vos fixtures au Bloc 5, quand plusieurs
fichiers auront besoin des mêmes données ou des mêmes mocks.
Pytest découvre ce fichier automatiquement : aucune importation nécessaire.
"""

import pytest


@pytest.fixture
def get_user():
    fixture_user =  {"name": "Leslie", "formation": "QA test"}
    yield fixture_user
    print('Fermer connexion BD')

@pytest.fixture
def db(base_donne):
    db = base_donne.open()
    print("Conexion")
    yield db
    print('Deconexion')

