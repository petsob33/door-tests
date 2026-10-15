"""Testy stavového automatu dveří - přechody stavů a fixtures."""
import pytest

from src.door import DoorController


@pytest.mark.smoke
def test_new_door_is_closed(door):
    assert door.state == DoorController.CLOSED


# --- Povolené přechody ----------------------------------------------------

def test_closed_to_open_at_stop(door):
    assert door.request_open(0, at_stop=True, released=True) is True
    assert door.state == DoorController.OPEN


def test_open_to_closed(open_door):
    assert open_door.request_close() is True
    assert open_door.state == DoorController.CLOSED


def test_open_request_when_already_open(open_door):
    assert open_door.request_open(0, at_stop=True, released=True) is True
    assert open_door.state == DoorController.OPEN


# --- Zakázané přechody (bezpečnost) --------------------------------------

def test_cannot_open_while_moving(door):
    assert door.request_open(15, at_stop=False, released=True) is False
    assert door.state == DoorController.CLOSED


def test_cannot_depart_with_open_door(open_door):
    assert open_door.can_depart() is False


def test_can_depart_after_closing(open_door):
    open_door.request_close()
    assert open_door.can_depart() is True


# --- Událost ve špatnou chvíli -------------------------------------------

def test_obstacle_keeps_door_open(open_door):
    assert open_door.request_close(obstacle=True) is False
    assert open_door.state == DoorController.OPEN
    assert open_door.can_depart() is False


# --- Známý nedostatek: ukázka xfail ---------------------------------------

@pytest.mark.xfail(reason="Požadavek: ověřit, že zavření se zaloguje - logování zatím neexistuje")
def test_close_is_logged(open_door):
    open_door.request_close()
    assert hasattr(open_door, "log") and open_door.log[-1] == "CLOSED"
