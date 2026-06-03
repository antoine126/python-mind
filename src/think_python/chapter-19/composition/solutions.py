"""Chapitre 19 — Composition, délégation et mixins : corrigés."""

from __future__ import annotations

from typing import Protocol


# ---------------------------------------------------------------------------
# Exercice 1 — Refaire : d'héritage à composition
# ---------------------------------------------------------------------------
class StripePayment:
    def __init__(self) -> None:
        self.charged: list[int] = []

    def charge(self, amount: int) -> None:
        self.charged.append(amount)


class Checkout:
    """Checkout A-UN moteur de paiement (composition), il n'EN EST PAS un."""

    def __init__(self, payment: StripePayment) -> None:
        self._payment = payment

    def pay(self, amount: int) -> None:
        self._payment.charge(amount)   # délégation


# ---------------------------------------------------------------------------
# Exercice 2 — Comprendre : pourquoi recombiner
# ---------------------------------------------------------------------------
EXERCICE_2 = """\
Par héritage, « sérialiser en JSON » est SOUDÉ à chaque classe via sa
hiérarchie ; ajouter le XML imposerait un second parent (MRO…) ou de la
duplication, et le format serait figé à la définition de la classe.
Par composition, le sérialiseur est un collaborateur INJECTÉ :
Report(JsonSerializer()) ou Report(XmlSerializer()), décidé à la création.
Ajouter un format = ajouter une classe de sérialiseur, sans toucher à Report.
C'est la recombinaison (en germe, le pattern Strategy).
"""


# ---------------------------------------------------------------------------
# Exercice 3 — Concevoir : un système de notifications (composition + délégation)
# ---------------------------------------------------------------------------
class Channel(Protocol):
    def send(self, user: str, msg: str) -> None: ...


class _Recorder:
    def __init__(self) -> None:
        self.sent: list[tuple[str, str, str]] = []


class EmailChannel(_Recorder):
    def send(self, user: str, msg: str) -> None:
        self.sent.append(("email", user, msg))


class SmsChannel(_Recorder):
    def send(self, user: str, msg: str) -> None:
        self.sent.append(("sms", user, msg))


class SlackChannel(_Recorder):       # ajouté SANS modifier Notifier
    def send(self, user: str, msg: str) -> None:
        self.sent.append(("slack", user, msg))


class Notifier:
    def __init__(self, channels: list[Channel]) -> None:
        self._channels = channels

    def notify(self, user: str, msg: str) -> None:
        for channel in self._channels:   # délègue à chaque canal
            channel.send(user, msg)


def _checks() -> None:
    payment = StripePayment()
    Checkout(payment).pay(42)
    assert payment.charged == [42]

    email, sms, slack = EmailChannel(), SmsChannel(), SlackChannel()
    Notifier([email, sms, slack]).notify("ada", "hi")
    assert email.sent == [("email", "ada", "hi")]
    assert sms.sent and slack.sent       # tous les canaux notifiés


if __name__ == "__main__":
    _checks()
    print("chapitre 19 — corrigés OK")
