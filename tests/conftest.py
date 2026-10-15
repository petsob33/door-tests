"""Sdílené fixtures - pytest tento soubor najde automaticky."""
import pytest

from src.door import DoorController


@pytest.fixture
def door():
    """Nové dveře v zavřeném stavu pro každý test zvlášť."""
    return DoorController()


@pytest.fixture
def open_door(door):
    """Dveře, které už jsou otevřené (vozidlo stojí v zastávce)."""
    door.request_open(speed_kmh=0, at_stop=True, released=True)
    return door
