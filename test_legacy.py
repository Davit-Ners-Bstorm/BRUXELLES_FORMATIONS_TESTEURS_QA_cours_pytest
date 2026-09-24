"""
Exercice Bloc 2 — Code hérité (voir énoncé).
Lisez la spécification dans legacy_pricing.py, concevez vos cas, écrivez vos
tests, lancez-les, et diagnostiquez tout écart avec la spécification.
Lancez : pytest test_legacy.py -v
"""
from legacy_pricing import loyalty_discount_percent, price_with_loyalty

# À vous d'écrire les tests.
def test_low_loyalty_discount_percent():
    assert loyalty_discount_percent(0) == 0
    assert loyalty_discount_percent(2) == 0

def test_medium_loyalty_discount_percent():
    assert loyalty_discount_percent(3) == 5
    assert loyalty_discount_percent(5) == 5
    assert loyalty_discount_percent(9) == 5

def test_high_loyalty_discount_percent():
    assert loyalty_discount_percent(10) == 10
    assert loyalty_discount_percent(11) == 10

def test_price_with_loyalty():
    assert price_with_loyalty(100, 10) == 90
    assert price_with_loyalty(147, 5) == 139

