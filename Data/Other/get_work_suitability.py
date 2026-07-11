import csv
import json
import subprocess

import pandas as pd

pals = pd.read_csv(r'../Pals.csv', header=None)[0].tolist()

# Name mismatches between our Pals.csv display names and the source dataset's
# localized_name (see get_all_combos.py for the full reconciliation notes).
ALIASES = {
    'Gumoss (Special)': 'Gumoss',
    'Ribunny': 'Ribbuny',
    'Ice Reptyro': 'Reptyro Cryst',
    'Ice Kingpaca': 'Kingpaca Cryst',
    'Ribunny Botan': 'Ribbuny Botan',
}

# Field order matches the 12 work types used across the app (Kindling,
# Watering, Planting, Eletricity, Handiwork, Gathering, Lumbering, Mining,
# Medicine, Cooling, Transporting, Farming). "OilExtraction" is skipped
# since the app never tracked that 13th work type.
FIELDS = [
    'EmitFlame', 'Watering', 'Seeding', 'GenerateElectricity', 'Handcraft',
    'Collection', 'Deforest', 'Mining', 'ProductMedicine', 'Cool',
    'Transport', 'MonsterFarm',
]

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

csv_data = []
missing = []
for pal in pals:
    lookup = ALIASES.get(pal, pal)
    found = by_localized_name.get(lookup)
    if not found:
        missing.append(pal)
        csv_data.append([pal] + [0] * len(FIELDS))
        continue
    ws = found[1]['work_suitability']
    csv_data.append([pal] + [ws[f] for f in FIELDS])

if missing:
    print("Warning, no data found for:", missing)

with open('../WorkSuitability.csv', 'w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerows(csv_data)

print("CSV file created successfully.")
