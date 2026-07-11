"""Regenerate Data/AllCombos.csv from Data/Pals.csv using Palworld's real breeding formula.

Formula (reverse-engineered from the game's DataTables; used identically by every
current community breeding calculator):
    child_target_rank = floor((parent1.combi_rank + parent2.combi_rank) / 2)
    child = the Pal (across the full current roster) whose own combi_rank is
            closest to child_target_rank (ties broken by the LOWER combi_rank).
    EXCEPT: breeding a Pal with itself always returns that same Pal (verified
            against every self-breed diagonal cell in the pre-Feybreak AllCombos.csv:
            0 mismatches out of 138), and a fixed list of "unique breed" parent
            pairs (mostly used to obtain elemental/regional variants) override the
            formula whenever both parents match, in either order.

combi_rank and work_suitability come from palworld-save-pal (actively maintained,
tracks the current live roster including Feybreak-update Pals):
    https://raw.githubusercontent.com/oMaN-Rod/palworld-save-pal/main/data/json/pals.json
    https://raw.githubusercontent.com/oMaN-Rod/palworld-save-pal/main/data/json/l10n/en/pals.json

The old 28 unique-breed overrides came from blaynem/paldex's unique_breeds.json
(https://raw.githubusercontent.com/blaynem/paldex/main/data-provider/baked-data/en/unique_breeds.json).
That repo has not been updated with the ~40 elemental/regional variants added since,
so those overrides (29 confirmed as of this writing) were researched individually
via web search and cross-checked against a second source (paldb.cc). Three new
variants (Blazamut Ryu, Bellanoir Libero, Shroomer Noct) were confirmed to have NO
distinct-species override -- they're reached via the rank formula / self-breed only.

Katress Ignis and Wixen Noct are BOTH bred from Katress + Wixen, with the real
in-game result depending on which parent is male vs female -- a mechanic this
app's single-outcome-per-pair CSV schema cannot represent. We map that pair to
"Katress Ignis"; "Wixen Noct" is not reachable via override in this table.
"""
import csv
import json
import subprocess

import pandas as pd

pals = pd.read_csv(r'../Pals.csv', header=None)[0].tolist()

# Name mismatches between our Pals.csv display names and the source dataset's
# localized_name.
ALIASES = {
    'Gumoss (Special)': 'Gumoss',
    'Ribunny': 'Ribbuny',
    'Ice Reptyro': 'Reptyro Cryst',
    'Ice Kingpaca': 'Kingpaca Cryst',
    'Ribunny Botan': 'Ribbuny Botan',
}

def fetch_json(url):
    # Uses curl instead of urllib: some sandboxed environments have a broken/missing
    # local CA bundle for Python's ssl module while the system curl works fine.
    # Capture raw bytes (not text=True): the response is UTF-8 and json.loads
    # decodes bytes directly, whereas text mode uses the platform locale
    # (cp1252 on Windows) and chokes on non-Latin localized names.
    out = subprocess.run(["curl", "-s", "--max-time", "30", url], capture_output=True)
    return json.loads(out.stdout)


print("Downloading pal data (palworld-save-pal)..")
DATA_URL = "https://raw.githubusercontent.com/oMaN-Rod/palworld-save-pal/main/data/json/pals.json"
L10N_URL = "https://raw.githubusercontent.com/oMaN-Rod/palworld-save-pal/main/data/json/l10n/en/pals.json"
data = fetch_json(DATA_URL)
l10n = fetch_json(L10N_URL)


def dedupe_score(item):
    """Prefer the 'real' dev-key among duplicate reskins of the same Pal."""
    key, entry = item
    bad = 0
    if '_Oilrig' in key:
        bad += 10
    if key.startswith('SUMMON_'):
        bad += 10
    if entry.get('combi_rank') == 9999:
        bad += 5
    if key.startswith('Quest_'):
        bad += 1
    if '_Flower' in key:
        bad += 1
    return bad


by_localized_name = {}
for key, entry in data.items():
    if not entry.get('is_pal'):
        continue
    try:
        idx = int(entry.get('pal_deck_index'))
    except (TypeError, ValueError):
        continue
    if idx <= 0:
        continue
    loc = l10n.get(key, {}).get('localized_name')
    if not loc:
        continue
    existing = by_localized_name.get(loc)
    if existing is None or dedupe_score((key, entry)) < dedupe_score(existing):
        by_localized_name[loc] = (key, entry)

missing = [p for p in pals if ALIASES.get(p, p) not in by_localized_name]
if missing:
    raise SystemExit(f"Cannot find combi_rank data for: {missing}")

rank_of = {p: by_localized_name[ALIASES.get(p, p)][1]['combi_rank'] for p in pals}

# --- Unique-breed overrides ---
overrides = {}


def add_override(p1, p2, child):
    if p1 not in rank_of or p2 not in rank_of or child not in rank_of:
        print(f"WARNING: override references unknown Pal: {p1} + {p2} -> {child}")
        return
    key = tuple(sorted([p1, p2]))
    if key in overrides and overrides[key] != child:
        print(f"WARNING: conflicting override for {key}: {overrides[key]} vs {child}")
    overrides[key] = child


# 28 pairs from blaynem/paldex unique_breeds.json (pre-Feybreak roster).
OLD_28 = [
    ("Relaxaurus", "Sparkit", "Relaxaurus Lux"),
    ("Incineram", "Maraith", "Incineram Noct"),
    ("Mau", "Pengullet", "Mau Cryst"),
    ("Vanwyrm", "Foxcicle", "Vanwyrm Cryst"),
    ("Eikthyrdeer", "Hangyu", "Eikthyrdeer Terra"),
    ("Elphidran", "Surfent", "Elphidran Aqua"),
    ("Pyrin", "Katress", "Pyrin Noct"),
    ("Mammorest", "Wumpo", "Mammorest Cryst"),
    ("Mossanda", "Grizzbolt", "Mossanda Lux"),
    ("Dinossom", "Rayhound", "Dinossom Lux"),
    ("Jolthog", "Pengullet", "Jolthog Cryst"),
    ("Frostallion", "Helzephyr", "Frostallion Noct"),
    ("Kingpaca", "Reindrix", "Ice Kingpaca"),
    ("Lyleen", "Menasting", "Lyleen Noct"),
    ("Leezpunk", "Flambelle", "Leezpunk Ignis"),
    ("Blazehowl", "Felbat", "Blazehowl Noct"),
    ("Robinquill", "Fuddler", "Robinquill Terra"),
    ("Broncherry", "Fuack", "Broncherry Aqua"),
    ("Surfent", "Dumud", "Surfent Terra"),
    ("Gobfin", "Rooby", "Gobfin Ignis"),
    ("Suzaku", "Jormuntide", "Suzaku Aqua"),
    ("Reptyro", "Foxcicle", "Ice Reptyro"),
    ("Hangyu", "Swee", "Hangyu Cryst"),
    ("Mossanda", "Petallia", "Lyleen"),
    ("Vanwyrm", "Anubis", "Faleris"),
    ("Mossanda", "Rayhound", "Grizzbolt"),
    ("Grizzbolt", "Relaxaurus", "Orserk"),
    ("Kitsun", "Astegon", "Shadowbeak"),
]

# 29 pairs researched via web search for post-Feybreak elemental/regional variants,
# cross-checked against a second source (paldb.cc) as of 2026-07.
NEW_29 = [
    ("Foxparks", "Foxcicle", "Foxparks Cryst"),
    ("Fuack", "Flambelle", "Fuack Ignis"),
    ("Pengullet", "Sparkit", "Pengullet Lux"),
    ("Penking", "Rayhound", "Penking Lux"),
    ("Killamari", "Ribunny", "Killamari Primo"),
    ("Celaray", "Univolt", "Celaray Lux"),
    ("Caprity", "Tarantriss", "Caprity Noct"),
    ("Ribunny", "Bristla", "Ribunny Botan"),
    ("Dumud", "Eikthyrdeer Terra", "Dumud Gild"),
    ("Loupmoon", "Sweepa", "Loupmoon Cryst"),
    ("Gorirat", "Kikit", "Gorirat Terra"),
    ("Chillet", "Arsox", "Chillet Ignis"),
    ("Kitsun", "Nyafia", "Kitsun Noct"),
    ("Dazzi", "Omascul", "Dazzi Noct"),
    ("Bushi", "Sootseer", "Bushi Noct"),
    ("Katress", "Wixen", "Katress Ignis"),
    ("Azurobe", "Frostplume", "Azurobe Cryst"),
    ("Cryolinx", "Dazemu", "Cryolinx Terra"),
    ("Warsect", "Digtoise", "Warsect Terra"),
    ("Fenglope", "Azurmane", "Fenglope Lux"),
    ("Quivern", "Lullu", "Quivern Botan"),
    ("Helzephyr", "Beakon", "Helzephyr Lux"),
    ("Menasting", "Knocklem", "Menasting Terra"),
    ("Faleris", "Jormuntide", "Faleris Aqua"),
    ("Croajiro", "Bushi Noct", "Croajiro Noct"),
    ("Turtacle", "Digtoise", "Turtacle Terra"),
    ("Finsider", "Gobfin Ignis", "Finsider Ignis"),
    ("Ghangler", "Sootseer", "Ghangler Ignis"),
    ("Whalaska", "Chillet Ignis", "Whalaska Ignis"),
]

# 25 variant pairs for the v1.0 (Sunreach / World Tree) roster, datamined from
# paldb.cc as of 2026-07 (one day post-launch, so worth re-verifying against a
# second source once more sites finish datamining). Child names use this app's
# display names -- notably "Ice Reptyro" where paldb writes "Reptyro Cryst".
# The brand-new base Pals (Ophydia, Sekhmet, the World Tree legendaries, etc.)
# have no unique combo -- they come from the rank formula -- so they're absent.
NEW_V1 = [
    ("Tanzee", "Flambelle", "Tanzee Ignis"),
    ("Woolipop", "Kikit", "Woolipop Terra"),
    ("Gloopie", "Valentail", "Gloopie Primo"),
    ("Polapup", "Surfent Terra", "Polapup Terra"),
    ("Elgrove", "Pierdon Cryst", "Elgrove Cryst"),
    ("Petallia", "Bushi", "Petallia Ignis"),
    ("Beakon", "Frostplume", "Beakon Cryst"),
    ("Rayhound", "Foxcicle", "Rayhound Cryst"),
    ("Needoll", "Prunelia", "Needoll Noct"),
    ("Moldron", "Ice Reptyro", "Moldron Cryst"),
    ("Sibelyx", "Lapure", "Sibelyx Primo"),
    ("Skutlass", "Gobfin Ignis", "Skutlass Ignis"),
    ("Starryon", "Celesdir", "Starryon Primo"),
    ("Pierdon", "Wumpo", "Pierdon Cryst"),
    ("Dualith", "Sootseer", "Dualith Noct"),
    ("Prixter", "Helzephyr Lux", "Prixter Lux"),
    ("Tetroise", "Celesdir", "Tetroise Primo"),
    ("Nitemary", "Petallia", "Nitemary Botan"),
    ("Smokie", "Munchill", "Smokie Cryst"),
    ("Celesdir", "Kitsun Noct", "Celesdir Noct"),
    ("Knocklem", "Ragnahawk", "Knocklem Ignis"),
    ("Snock", "Turtacle Terra", "Snock Lux"),
    ("Solmora", "Slowatt", "Solmora Lux"),
    ("Eidrolon", "Suzaku", "Eidrolon Ignis"),
    ("Univolt", "Frostplume", "Univolt Cryst"),
]

for p1, p2, child in OLD_28 + NEW_29 + NEW_V1:
    add_override(p1, p2, child)

print(f"Loaded {len(overrides)} unique-breed overrides.")


def child_of(p1, p2):
    if p1 == p2:
        return p1
    key = tuple(sorted([p1, p2]))
    if key in overrides:
        return overrides[key]
    target = (rank_of[p1] + rank_of[p2]) // 2
    best, best_dist, best_rank = None, None, None
    for pal in pals:
        r = rank_of[pal]
        d = abs(r - target)
        if best is None or d < best_dist or (d == best_dist and r < best_rank):
            best, best_dist, best_rank = pal, d, r
    return best


print("Computing breeding matrix..")
# cell[row][col] = child of pals[col] bred with pals[row]
matrix = [[child_of(col_pal, row_pal) for col_pal in pals] for row_pal in pals]

with open('../AllCombos.csv', 'w', newline='', encoding='utf-8-sig') as csv_file:
    writer = csv.writer(csv_file, delimiter=';')
    writer.writerows(matrix)

print("CSV file created successfully.")
