"""
payment.py — passerelle de paiement externe (simulée).

En formation, l'appel réel n'est pas disponible : toute tentative lève
NotImplementedError. C'est VOULU. Pour tester du code qui dépend du paiement,
on ne l'appelle pas pour de vrai : on le remplace par un mock.
"""


class PaymentError(Exception):
    """Levée quand un paiement ou un remboursement est refusé."""


class PaymentGateway:
    def charge(self, amount_cents, token):
        raise NotImplementedError("Paiement réel indisponible en formation")

    def refund(self, amount_cents, transaction_id):
        raise NotImplementedError("Remboursement réel indisponible en formation")
