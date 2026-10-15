"""Zjednodušená logika dveří tramvaje.

Tohle je "testovaný kód" - v reálné firmě by ho napsal vývojář.
My k němu píšeme testy.
"""

MAX_SPEED_KMH = 80


class DoorError(Exception):
    """Neplatný vstup (např. záporná rychlost)."""


def can_open_door(speed_kmh: float, at_stop: bool, released: bool) -> bool:
    """Smí se dveře otevřít?

    Pravidlo: vozidlo stojí (rychlost 0), je v zastávce a řidič dveře uvolnil.
    """
    if not isinstance(speed_kmh, (int, float)) or isinstance(speed_kmh, bool):
        raise DoorError("Rychlost musí být číslo")
    if speed_kmh < 0:
        raise DoorError("Rychlost nemůže být záporná")
    if speed_kmh > MAX_SPEED_KMH:
        raise DoorError(f"Rychlost nad {MAX_SPEED_KMH} km/h je mimo rozsah")
    return speed_kmh == 0 and at_stop and released


class DoorController:
    """Stavový automat dveří: CLOSED <-> OPEN."""

    CLOSED = "CLOSED"
    OPEN = "OPEN"

    def __init__(self):
        self.state = self.CLOSED

    def request_open(self, speed_kmh: float, at_stop: bool, released: bool) -> bool:
        """Požadavek na otevření. Vrací True, pokud se dveře otevřely."""
        if self.state == self.OPEN:
            return True
        if can_open_door(speed_kmh, at_stop, released):
            self.state = self.OPEN
            return True
        return False

    def request_close(self, obstacle: bool = False) -> bool:
        """Požadavek na zavření. Při překážce ve dveřích zůstanou otevřené."""
        if obstacle:
            return False
        self.state = self.CLOSED
        return True

    def can_depart(self) -> bool:
        """Vozidlo se smí rozjet jen se zavřenými dveřmi."""
        return self.state == self.CLOSED
