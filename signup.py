"""
signup.py — inscription d'un utilisateur.

Contrairement à booking.create_order, cette fonction NE reçoit PAS son service
d'e-mail en argument : elle le crée elle-même en interne. On ne peut donc pas
lui injecter un mock. C'est le cas typique où l'on utilise patch : on remplace
l'EmailService LÀ OÙ signup va le chercher.
"""
from notifications import EmailService


def register_user(email):
    if "@" not in email:
        raise ValueError("Email invalide")
    service = EmailService()          # dépendance créée en interne
    service.send(email, "Bienvenue", "Votre compte est créé.")
    return {"email": email, "status": "registered"}
