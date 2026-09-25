"""
Exercices Bloc 1 & 3 — voir J3_exercices_eleves.md.
Lancez : pytest test_pricing.py -v
"""
import pytest
from pytest import raises
from booking import MAX_TICKETS_PER_ORDER
from pytest import mark as m
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

def test_ticket_price_cat_error():
    with pytest.raises(ValueError):
        ticket_price('vipp')

def test_line_total_quant_error():
    with pytest.raises(ValueError):
        line_total('vip', 0)

def test_line_total_quant_error():
    with pytest.raises(ValueError):
        line_total('vip', -1)

codes_test = {
    "valide_code": {
        "code": "VALID",
        "percent_off": 10,
        "active": True,
        "max_uses": 10,
        "used_count": 1
    },
    "invalide": {
        "code": "INVALID",
        "percent_off": 10,
        "active": False,
        "max_uses": 10,
        "used_count": 1
    },
    "max_used": {
        "code": "USED",
        "percent_off": 10,
        "active": True,
        "max_uses": 10,
        "used_count": 10
    },
    "low_percent": {
        "code": "LOW",
        "percent_off": 0,
        "active": True,
        "max_uses": 10,
        "used_count": 1
    },
    "high_percent": {
        "code": "HIGH",
        "percent_off": 101,
        "active": True,
        "max_uses": 10,
        "used_count": 1
    }
}

def test_apply_promo():
    assert apply_promo(100, None) == 100
    assert apply_promo(100, codes_test["valide_code"]) == 100 - (100 * 10 // 100)

def test_apply_promo_inactive():
    with pytest.raises(ValueError, match=r"(?i).*inactif"):
        apply_promo(100, codes_test["invalide"])

def test_apply_promo_used():
    with pytest.raises(ValueError, match=r"(?i).*épuisé"):
        apply_promo(100, codes_test["max_used"])

def test_apply_promo_low_percent():
    with pytest.raises(ValueError, match=r"(?i).*invalide"):
        apply_promo(100, codes_test["low_percent"])

def test_apply_promo_high_percent():
    with pytest.raises(ValueError, match=r"(?i).*invalide"):
        apply_promo(100, codes_test["high_percent"])

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# ATTENTION CE CODE EN BAS N'EST PAS ECRIT PAR MOI (cc Noé)
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

def test_order_total_ok() :
    i = [
        {
            "category" : "vip",
            "quantity" : 6
        }
    ]
    assert order_total(i, None) == 6*7500

def test_order_total_tropdetickets() :
    i = [
        {
            "category" : "vip",
            "quantity" : 7
        }
    ]
    with raises(ValueError, match=f"Maximum {MAX_TICKETS_PER_ORDER}"):
        order_total(i,None)

def test_order_total_pasassédetiquets() :
    i = [
        {
            "category" : "vip",
            "quantity" : 0
        }
    ]
    with raises( ValueError, match= "contenir au moins un"):
        order_total(i,None)

def test_order_total_ticket_negatif() :
    i = [
        {
            "category" : "vip",
            "quantity" : -5
        }
    ]
    with raises( ValueError, match= "contenir au moins un"):
        order_total(i,None)


#Exercice 04
@pytest.mark.parametrize("category, quantity, expected", [
    ("vip", 1, 7500),
    ("standard", 1, 3500),
    ("early_bird", 3, 2495*3)
], ids=["CAS_VIP", "CAS_STANDARD", "CAS_EARLY"])
def test_line_total(category, quantity, expected):
    assert line_total(category, quantity) == expected

@pytest.mark.parametrize("items, expected", [
    ([
        {"category": "vip", "quantity": 2},
        {"category": "standard", "quantity": 1}
    ], 18500),
    ([
            {"category": "vip", "quantity": 3},
            {"category": "early_bird", "quantity": 1}
        ], 24995)
])
def test_param_order_total(items, expected):
    assert order_total(items, None) == expected

    [(1, 2)]

order_total_dict = {
    "no_ticket": {
        "category": "vip",
        "quantity": 0
    },
    "tickets_5": {
        "category": "standard",
        "quantity": 5
    },
    "negative_ticket": {
        "category": "early_bird",
        "quantity": -1
    },
    "tickets_7": {
        "category": "vip",
        "quantity": 7
    },
    "tickets_6": {
        "category": "standard",
        "quantity": 6
    },
}

# @pytest.mark.parametrize === même chose qu'en bas
@m.parametrize("ticket_dict, expected, sorted_error", [
    (order_total_dict["negative_ticket"], None, r"(?i).*doit contenir"),
    (order_total_dict["no_ticket"], None, r"(?i).*au moins un"),
    (order_total_dict["tickets_5"], (3500 * 5), None),
    (order_total_dict["tickets_6"], (3500 * 6), None),
    (order_total_dict["tickets_7"], None, r"(?i).*maximum")
], ids=["negative ticket", "no tickets", "5 tickets", "6 tickets", "7 tickets"])
def test_p_order_total(ticket_dict, expected, sorted_error):
    cart = [ticket_dict]
    if sorted_error:
        with raises(ValueError, match=sorted_error):
            order_total(cart)
    else:
        assert order_total(cart) == expected