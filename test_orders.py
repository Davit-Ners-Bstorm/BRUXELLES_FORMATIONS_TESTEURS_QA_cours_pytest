"""
Exercices 5 & 6 — voir J3_exercices_eleves.md.
Lancez : pytest test_orders.py -v

Exercice 5 (fixtures) : create_order a besoin d'un utilisateur, d'un événement
et de deux services externes (paiement, e-mail). Les deux faux services sont
fournis ci-dessous, prêts à l'emploi. Pour l'instant, considérez-les comme des
boîtes noires : on comprendra leur fonctionnement au bloc mocks (exercice 6).

Votre travail ici : écrire le cas nominal de create_order, repérer la répétition
du setup, l'extraire en fixtures, en déplacer dans conftest.py, écrire une
fixture avec yield.

Exercice 6 (mocks) : ensuite seulement, concevez la vraie suite des interactions
de create_order avec ses dépendances (voir énoncé).
"""
from unittest.mock import Mock
from booking import create_order

payment = Mock()
payment.charge.return_value = {
    "success": True,
    "transaction_id": "tx_1"
}
email = Mock()

# À vous d'écrire le cas nominal puis de travailler les fixtures.
