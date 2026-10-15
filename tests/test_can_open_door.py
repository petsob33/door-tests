"""Testy funkce can_open_door - techniky návrhu testů v praxi."""
import pytest

from src.door import DoorError, can_open_door


# --- 1) Základní testy: obyčejný assert -----------------------------------

@pytest.mark.smoke
def test_opens_when_all_conditions_met():
    assert can_open_door(0, at_stop=True, released=True) is True


def test_stays_closed_while_moving():
    assert can_open_door(30, at_stop=True, released=True) is False


# --- 2) Rozhodovací tabulka: 3 podmínky = 2^3 = 8 kombinací ---------------

@pytest.mark.parametrize(
    "speed, at_stop, released, expected",
    [
        (0, True, True, True),     # jen tahle kombinace otevře dveře
        (0, True, False, False),   # řidič neuvolnil
        (0, False, True, False),   # mimo zastávku
        (0, False, False, False),
        (10, True, True, False),   # jede
        (10, True, False, False),
        (10, False, True, False),
        (10, False, False, False),
    ],
)
def test_decision_table(speed, at_stop, released, expected):
    assert can_open_door(speed, at_stop, released) == expected


# --- 3) Hraniční hodnoty kolem 0 a 80 km/h --------------------------------

@pytest.mark.parametrize(
    "speed, expected",
    [
        (0, True),       # přesně na hranici - smí otevřít
        (0.1, False),    # nejmenší kladná rychlost - nesmí
        (1, False),
        (79, False),
        (80, False),     # horní hranice rozsahu - platný vstup, ale jede
    ],
)
def test_speed_boundaries(speed, expected):
    assert can_open_door(speed, at_stop=True, released=True) == expected


# --- 4) Ekvivalentní třídy neplatných vstupů -> výjimka -------------------

@pytest.mark.parametrize("bad_speed", [-1, -0.1, 80.1, 81, 200])
def test_out_of_range_speed_raises(bad_speed):
    with pytest.raises(DoorError):
        can_open_door(bad_speed, at_stop=True, released=True)


@pytest.mark.parametrize("bad_speed", ["abc", None, "0", True])
def test_non_numeric_speed_raises(bad_speed):
    with pytest.raises(DoorError, match="číslo"):
        can_open_door(bad_speed, at_stop=True, released=True)


def test_negative_speed_message():
    with pytest.raises(DoorError, match="záporná"):
        can_open_door(-5, at_stop=True, released=True)
