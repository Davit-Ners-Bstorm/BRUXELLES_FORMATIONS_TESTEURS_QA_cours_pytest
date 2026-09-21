"""
notifications.py — service d'envoi d'e-mails (simulé).

Comme la passerelle de paiement, l'envoi réel n'est pas disponible : on ne
veut pas spammer une vraie boîte mail depuis un test. En test, on remplace
ce service par un mock et on vérifie COMMENT il a été appelé.
"""


class EmailService:
    def send(self, to, subject, body):
        raise NotImplementedError("Envoi d'e-mail réel indisponible en formation")
