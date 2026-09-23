"""
Exercices Bloc 1 & 3 — voir J3_exercices_eleves.md.
Lancez : pytest test_pricing.py -v
"""
from booking import ticket_price, line_total, apply_promo, order_total

# À vous d'écrire les tests.


def test_ticket_price():
    assert ticket_price("early_bird") == 2495
    assert ticket_price("standard") == 3500
    assert ticket_price("vip") == 7500

def test_line_total():
    assert line_total("early_bird", 1) == 2495
    assert line_total("standard", 2) == 7000
    assert line_total("vip", 4) == 30000
    
