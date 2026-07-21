"""Generate Data/Pals.csv -- the roster, in pal-dex order -- from PalCalc's db.

Run this first: it writes the roster that every other CSV aligns to. Astralym and
other non-breedable pals are absent from PalCalc's dataset, so they are naturally
left out; the Terraria event monsters are filtered in _paldata.build_roster.
"""
import _paldata as pd_


def generate(db):
    roster = pd_.build_roster(db)
    pd_.write_csv('Pals.csv', [[name] for name in roster])
    print(f"Pals.csv: {len(roster)} pals")
    return roster


if __name__ == '__main__':
    generate(pd_.load_db())
