"""
booking.py — logique métier de réservation, inspirée d'EventFlow.

Ce module ne contient AUCUN test. Il contient les règles métier que vous allez
apprendre à tester avec PyTest : prix, promotions, quantités, disponibilité,
création d'une commande et remboursement.

Deux dépendances externes (paiement, e-mail) sont passées en argument aux
fonctions qui en ont besoin : c'est ce qui permettra de les remplacer par des
mocks en test, sans jamais appeler les vrais services.
"""

from payment import PaymentError

# --- Règles métier constantes ---------------------------------------------

MAX_TICKETS_PER_ORDER = 6  # RM3 EventFlow : 6 billets maximum par commande

TICKET_PRICES_CENTS = {
    "early_bird": 2495,
    "standard": 3500,
    "vip": 7500,
}


# --- Fonctions "pures" (sans dépendance externe) ---------------------------

def ticket_price(category):
    """Prix unitaire d'une catégorie de billet, en centimes.

    Lève ValueError si la catégorie n'existe pas.
    """
    if category not in TICKET_PRICES_CENTS:
        raise ValueError(f"Catégorie de billet inconnue : {category!r}")
    return TICKET_PRICES_CENTS[category]


def line_total(category, quantity):
    """Prix total pour une catégorie et une quantité, en centimes.

    Lève ValueError si la quantité n'est pas strictement positive.
    """
    if quantity <= 0:
        raise ValueError("La quantité doit être strictement positive")
    return ticket_price(category) * quantity


def apply_promo(total_cents, promo):
    """Applique un code promo à un total (en centimes) et renvoie le nouveau total.

    `promo` est None (aucune remise) ou un dict :
        {"code": str, "percent_off": int, "active": bool,
         "max_uses": int, "used_count": int}

    Règles :
    - promo None                     -> total inchangé
    - promo inactive                 -> ValueError
    - quota d'utilisations atteint   -> ValueError
    - percent_off hors de 1..100     -> ValueError
    La remise est calculée en centimes entiers (arrondi vers le bas).
    """
    if promo is None:
        return total_cents
    if not promo.get("active", False):
        raise ValueError("Code promo inactif")
    if promo["used_count"] >= promo["max_uses"]:
        raise ValueError("Code promo épuisé")
    percent = promo["percent_off"]
    if percent < 1 or percent > 100:
        raise ValueError("Pourcentage de remise invalide")
    discount = total_cents * percent // 100
    return total_cents - discount


def order_total(items, promo=None):
    """Total d'une commande en centimes, promo éventuelle appliquée.

    `items` est une liste de dicts : {"category": str, "quantity": int}.

    Règles :
    - commande vide (0 billet)                 -> ValueError
    - plus de MAX_TICKETS_PER_ORDER billets    -> ValueError
    - chaque ligne est validée par line_total (quantité > 0, catégorie connue)
    """
    total_quantity = sum(item["quantity"] for item in items)
    if total_quantity <= 0:
        raise ValueError("Une commande doit contenir au moins un billet")
    if total_quantity > MAX_TICKETS_PER_ORDER:
        raise ValueError(
            f"Maximum {MAX_TICKETS_PER_ORDER} billets par commande"
        )
    subtotal = sum(line_total(item["category"], item["quantity"]) for item in items)
    return apply_promo(subtotal, promo)


def check_availability(available, requested):
    """Vérifie qu'on peut réserver `requested` places parmi `available`.

    Lève ValueError si la demande est <= 0 ou dépasse le stock disponible.
    """
    if requested <= 0:
        raise ValueError("Le nombre de places demandé doit être positif")
    if requested > available:
        raise ValueError("Stock insuffisant")


# --- Fonctions avec dépendances externes (paiement, e-mail) ----------------

def create_order(event, items, user, payment_gateway, email_service, promo=None):
    """Crée une commande : valide, calcule, encaisse, notifie.

    Args:
        event: dict avec au moins {"id": int, "title": str, "available": int}
        items: liste de dicts {"category": str, "quantity": int}
        user: dict avec au moins {"email": str, "active": bool, "payment_token": str}
        payment_gateway: objet avec .charge(amount_cents, token) -> {"success": bool, "transaction_id": str | None}
        email_service: objet avec .send(to, subject, body)
        promo: dict optionnel {"code": str, "percent_off": int, "active": bool, "max_uses": int, "used_count": int}

    Règles :
        - utilisateur inactif                 -> ValueError (aucun paiement, aucun e-mail)
        - stock insuffisant / quantités        -> ValueError (via check_availability / order_total)
        - paiement refusé (success == False)   -> PaymentError, et AUCUN e-mail n'est envoyé
        - succès                               -> e-mail de confirmation, puis dict commande
    """
    if not user.get("active", False):
        raise ValueError("Utilisateur inactif")

    total_quantity = sum(item["quantity"] for item in items)
    check_availability(event["available"], total_quantity)

    amount = order_total(items, promo)

    charge_result = payment_gateway.charge(amount, user["payment_token"])
    if not charge_result["success"]:
        raise PaymentError("Paiement refusé")

    email_service.send(
        user["email"],
        "Confirmation de votre commande",
        f"Votre commande de {total_quantity} billet(s) est confirmée. "
        f"Montant : {amount} centimes.",
    )

    return {
        "status": "confirmed",
        "total_cents": amount,
        "tickets": total_quantity,
        "user_email": user["email"],
        "transaction_id": charge_result["transaction_id"],
    }


def process_refund(order, payment_gateway, email_service, hours_before_event):
    """Rembourse une commande confirmée si les règles le permettent.

    Dépendances injectées :
    - payment_gateway.refund(amount_cents, transaction_id) -> {"success": bool}
    - email_service.send(to, subject, body)

    Règles (inspirées de RM6 EventFlow) :
    - commande non "confirmed"                  -> ValueError
    - moins de 48h avant l'événement            -> ValueError (48h pile = autorisé)
    - remboursement refusé par la passerelle    -> PaymentError, aucun e-mail
    - succès                                    -> e-mail, puis dict remboursement
    """
    if order["status"] != "confirmed":
        raise ValueError("Seule une commande confirmée peut être remboursée")
    if hours_before_event < 48:
        raise ValueError("Remboursement impossible à moins de 48h de l'événement")

    refund_result = payment_gateway.refund(order["total_cents"], order["transaction_id"])
    if not refund_result["success"]:
        raise PaymentError("Remboursement refusé")

    email_service.send(
        order["user_email"],
        "Remboursement effectué",
        f"Votre commande a été remboursée de {order['total_cents']} centimes.",
    )

    return {"status": "refunded", "amount_cents": order["total_cents"]}
