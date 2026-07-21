"""Shared data layer for the CSV generators in this folder.

Single source of truth for the roster and game-data fields: PalCalc's datamined
dataset, extracted straight from the live game .pak files
(https://github.com/tylercamp/palcalc). Roster & order, work suitability and
breeding results all come from here, so a game patch only needs a fresh PalCalc
dump (check the printed version). Image and wiki links can't come from PalCalc --
they don't exist in that dataset -- so they're sourced from the fandom wiki,
keyed by the roster names produced here.

Folder layout:
    _paldata.py    -- this module: download + roster + name mapping + validation
    update_data.py -- orchestrator: regenerates every CSV in dependency order
    gen_pals.py    -- Pals.csv            (PalCalc db)
    gen_work.py    -- WorkSuitability.csv (PalCalc db)
    gen_combos.py  -- AllCombos.csv       (PalCalc breeding table)
    gen_wikis.py   -- Wikis.csv           (fandom URLs)
    gen_images.py  -- Images.csv          (fandom MediaWiki API)

Every gen_*.py exposes a generate(...) function and also runs standalone.
"""
import csv
import json
import os
import subprocess

# --- source & output locations -------------------------------------------------
PALCALC_RAW = "https://raw.githubusercontent.com/tylercamp/palcalc/main/PalCalc.Model"
DB_URL = f"{PALCALC_RAW}/db.json"
BREEDING_URL = f"{PALCALC_RAW}/breeding.json"

_HERE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.normpath(os.path.join(_HERE, ".."))


def data_path(name):
    return os.path.join(DATA_DIR, name)


# --- naming reconciliation ------------------------------------------------------
# Our display names vs PalCalc's English "Name", where they differ.
ALIASES = {
    'Ribunny': 'Ribbuny',
    'Ribunny Botan': 'Ribbuny Botan',
}
_REV_ALIASES = {v: k for k, v in ALIASES.items()}

# Gumoss and Gumoss (Special) share the English name "Gumoss" (the base PlantSlime
# and the Flower variant PlantSlime_Flower), so the name alone is ambiguous -- pin
# them straight to internal names.
INTERNAL_OVERRIDES = {
    'Gumoss': 'PlantSlime',
    'Gumoss (Special)': 'PlantSlime_Flower',
}
_INTERNAL_TO_DISPLAY = {v.lower(): k for k, v in INTERNAL_OVERRIDES.items()}

# Work-suitability columns, in the exact order the app's CSV expects. These are
# PalCalc's WorkSuitability dict keys (OilExtraction, the 13th type, is unused).
WORK_FIELDS = [
    'Kindling', 'Watering', 'Planting', 'GenerateElectricity', 'Handiwork',
    'Gathering', 'Lumbering', 'Mining', 'MedicineProduction', 'Cooling',
    'Transporting', 'Farming',
]

# Breeding pairs whose result depends on parent gender collapse to a single stored
# outcome (the app shows a gender-exception toast for these). If PalCalc ever adds
# more gendered pairs, gen_combos raises so this list can be reviewed.
GENDER_PREFERENCE = ['Katress Ignis']


def _is_event_only(entry):
    """Event-only pals we never list (Terraria crossover monsters)."""
    return entry['InternalName'].lower().startswith('yakushima')


def fetch_json(url):
    # curl (not urllib): some sandboxes ship a broken/missing CA bundle for
    # Python's ssl module while system curl works. Raw bytes (not text=True) so
    # json.loads decodes UTF-8 directly rather than via the platform locale
    # (cp1252 on Windows chokes on non-Latin localized names).
    out = subprocess.run(["curl", "-sL", "--max-time", "60", url], capture_output=True)
    return json.loads(out.stdout)


def load_db():
    print("Downloading PalCalc pal database (db.json)..")
    return fetch_json(DB_URL)


def load_breeding():
    print("Downloading PalCalc breeding table (breeding.json)..")
    return fetch_json(BREEDING_URL)


def display_name(entry):
    """Our display name for a PalCalc pal entry."""
    internal = entry['InternalName'].lower()
    if internal in _INTERNAL_TO_DISPLAY:
        return _INTERNAL_TO_DISPLAY[internal]
    return _REV_ALIASES.get(entry['Name'], entry['Name'])


def build_roster(db):
    """Ordered list of display names: every breedable pal, base before variant, in
    pal-dex order. Excludes event-only pals; PalCalc already omits pals that can't
    be bred at all (e.g. Astralym)."""
    pals = [p for p in db['Pals'] if not _is_event_only(p)]
    pals.sort(key=lambda p: (p['Id']['PalDexNo'], p['Id']['IsVariant'], p['InternalIndex']))
    return [display_name(p) for p in pals]


def read_roster():
    """The committed roster (Pals.csv) -- the contract every other CSV aligns to.
    Generators besides gen_pals read this so a manual roster tweak propagates."""
    with open(data_path('Pals.csv'), newline='', encoding='utf-8-sig') as f:
        return [row[0] for row in csv.reader(f) if row]


def pal_index(db):
    """display name -> PalCalc pal entry, for every non-event pal."""
    return {display_name(p): p for p in db['Pals'] if not _is_event_only(p)}


def require_all(index, roster):
    """Fail loudly if the roster references a pal PalCalc doesn't know -- e.g. a
    rename or a manual Pals.csv edit that outpaced the dataset."""
    missing = [p for p in roster if p not in index]
    if missing:
        raise SystemExit(
            f"Roster entries with no PalCalc match: {missing}\n"
            "Update the dataset, or the aliases/overrides in _paldata."
        )


def write_csv(name, rows, bom=False, delimiter=','):
    """Write a Data/*.csv. Matches the repo convention: CRLF line endings, and (for
    AllCombos.csv) a ';' delimiter plus a UTF-8 BOM."""
    encoding = 'utf-8-sig' if bom else 'utf-8'
    with open(data_path(name), 'w', newline='', encoding=encoding) as f:
        csv.writer(f, delimiter=delimiter).writerows(rows)
