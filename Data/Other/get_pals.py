"""Regenerate Data/Pals.csv (the roster) from the live palworld-save-pal dataset,
ordered by pal_deck_index. Run this first after a game update; every other CSV
(AllCombos, Images, Wikis, WorkSuitability) is generated from Pals.csv, so the
roster must be refreshed before the others.

Source (same as get_all_combos.py / get_work_suitability.py):
    https://raw.githubusercontent.com/oMaN-Rod/palworld-save-pal/main/data/json/pals.json
    https://raw.githubusercontent.com/oMaN-Rod/palworld-save-pal/main/data/json/l10n/en/pals.json
"""
import csv
import json
import subprocess

# localized_name -> the display name this app has always used for it.
DISPLAY_OVERRIDES = {
    'Ribbuny': 'Ribunny',
    'Ribbuny Botan': 'Ribunny Botan',
}

# Gumoss and its reskin (PlantSlime / PlantSlime_Flower) share the localized
# name "Gumoss"; dedupe collapses them to one entry, but the app has always
# listed both. Emit "Gumoss (Special)" right after "Gumoss".
GUMOSS = 'Gumoss'
GUMOSS_SPECIAL = 'Gumoss (Special)'


def fetch_json(url):
    # curl instead of urllib: some sandboxed environments have a broken/missing
    # local CA bundle for Python's ssl module while system curl works fine.
    # Capture raw bytes (not text=True): the response is UTF-8 and json.loads
    # decodes bytes directly, whereas text mode would use the platform locale
    # (cp1252 on Windows) and choke on non-Latin localized names.
    out = subprocess.run(["curl", "-s", "--max-time", "30", url], capture_output=True)
    return json.loads(out.stdout)


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


print("Downloading pal data (palworld-save-pal)..")
DATA_URL = "https://raw.githubusercontent.com/oMaN-Rod/palworld-save-pal/main/data/json/pals.json"
L10N_URL = "https://raw.githubusercontent.com/oMaN-Rod/palworld-save-pal/main/data/json/l10n/en/pals.json"
data = fetch_json(DATA_URL)
l10n = fetch_json(L10N_URL)

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

roster = sorted(by_localized_name.items(), key=lambda kv: kv[1][1]['pal_deck_index'])

rows = []
for loc, (key, entry) in roster:
    rows.append([DISPLAY_OVERRIDES.get(loc, loc)])
    if loc == GUMOSS:
        rows.append([GUMOSS_SPECIAL])

with open('../Pals.csv', 'w', newline='', encoding='utf-8') as csv_file:
    csv.writer(csv_file).writerows(rows)

print(f"Wrote {len(rows)} pals to ../Pals.csv")
