# door-tests

![tests](https://github.com/petsob33/door-tests/actions/workflows/tests.yml/badge.svg)

Ukázkový projekt automatizovaných testů v **Pytestu** nad zjednodušenou logikou dveří tramvaje.
Ukazuje techniky návrhu testů: rozhodovací tabulku, hraniční hodnoty, ekvivalentní třídy a přechody stavů.

## Co testujeme

Pravidlo: dveře se smí otevřít, jen když **vozidlo stojí** (0 km/h), **je v zastávce** a **řidič dveře uvolnil**.
Vozidlo se nesmí rozjet s otevřenými dveřmi a překážka ve dveřích zabrání zavření.

## Struktura

```
door-tests/
├── src/door.py                    # testovaný kód (to by psal vývojář)
├── tests/
│   ├── conftest.py                # sdílené fixtures (příprava dat pro testy)
│   ├── test_can_open_door.py      # rozhodovací tabulka, hraniční hodnoty, neplatné vstupy
│   └── test_door_controller.py    # stavový automat dveří, bezpečnostní scénáře
├── pytest.ini                     # nastavení pytestu a markerů
├── requirements.txt
├── .gitlab-ci.yml                 # automatické spuštění testů v GitLab CI
└── .github/workflows/tests.yml    # totéž na GitHubu (GitHub Actions)
```

## Spuštění (Fedora / Linux)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

pytest                     # všechny testy
pytest -m smoke            # jen smoke testy
pytest -k boundaries       # jen testy s "boundaries" v názvu
pytest --cov=src           # pokrytí kódu
```

Výsledek: 33 testů prošlo, 1 očekávaně selhává (`xfail`), pokrytí kódu 100 %.

## Použité techniky

| Technika | Kde | Co ověřuje |
| --- | --- | --- |
| Rozhodovací tabulka | `test_decision_table` | všech 8 kombinací tří podmínek |
| Hraniční hodnoty | `test_speed_boundaries` | 0 / 0,1 km/h a horní hranici 80 km/h |
| Ekvivalentní třídy | `test_out_of_range_speed_raises`, `test_non_numeric_speed_raises` | záporné, příliš vysoké a nečíselné vstupy |
| Přechody stavů | `test_door_controller.py` | povolené i zakázané přechody CLOSED ↔ OPEN |
| Negativní / bezpečnostní testy | `test_cannot_depart_with_open_door`, `test_obstacle_keeps_door_open` | rozjezd s otevřenými dveřmi, překážka |

## Použité funkce Pytestu

- `assert` místo `assertEqual`
- `@pytest.mark.parametrize` – jeden test, mnoho vstupů
- `pytest.raises` – testování výjimek
- fixtures v `conftest.py` – `door` a `open_door`
- markery `smoke` a `xfail`
- `pytest-cov` – měření pokrytí kódu
- `.gitlab-ci.yml` a `.github/workflows/tests.yml` – testy běží automaticky po každém pushi (GitLab CI i GitHub Actions)
