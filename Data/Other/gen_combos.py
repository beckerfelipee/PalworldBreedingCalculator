"""Generate Data/AllCombos.csv -- the full breeding matrix -- from PalCalc's
datamined breeding table.

Why datamined results, not the old rank formula: Palworld 1.0's real breeding
algorithm is NOT a simple "closest average combi_rank" pick. The ranks are right,
but the game's rounding + tie-break plus dozens of unique-combo overrides diverge
from the naive formula on ~57% of cells. We consume PalCalc's RESULT table, which
is read straight from the game .pak (cross-checked vs paldb.cc: Orserk / Faleris /
Shadowbeak are self-breed-only in 1.0; Grizzbolt + Relaxaurus now yields Reptyro).

Katress + Wixen is gender-dependent (Katress Ignis vs Wixen Noct); the single
outcome per pair is resolved via _paldata.GENDER_PREFERENCE, matching the app's
gender-exception toast.
"""
import _paldata as pd_


def generate(db, breeding, roster):
    index = pd_.pal_index(db)
    pd_.require_all(index, roster)

    internal_of = {pal: index[pal]['InternalName'].lower() for pal in roster}
    # Invert to label results with the exact roster name; injective by design.
    display_of = {}
    for pal, internal in internal_of.items():
        if internal in display_of:
            raise SystemExit(f"{pal} and {display_of[internal]} share internal '{internal}'")
        display_of[internal] = pal

    # (frozenset of the two parent internals) -> set of possible child names,
    # keeping only children in our roster (drops event-only children like the
    # Terraria crossover monsters).
    combos = {}
    for entry in breeding['Breeding']:
        key = frozenset([entry['Parent1InternalName'].lower(),
                         entry['Parent2InternalName'].lower()])
        child = display_of.get(entry['ChildInternalName'].lower())
        if child is not None:
            combos.setdefault(key, set()).add(child)

    def child_of(parent_a, parent_b):
        kids = combos.get(frozenset([internal_of[parent_a], internal_of[parent_b]]))
        if not kids:
            raise SystemExit(f"PalCalc has no breeding result for {parent_a} + {parent_b}")
        if len(kids) > 1:
            preferred = [k for k in pd_.GENDER_PREFERENCE if k in kids]
            if not preferred:
                raise SystemExit(
                    f"Unhandled gender-dependent pair {parent_a} + {parent_b} -> "
                    f"{sorted(kids)}. Add the intended outcome to GENDER_PREFERENCE."
                )
            return preferred[0]
        return next(iter(kids))

    # cell[row][col] = child of roster[col] bred with roster[row] (symmetric except
    # the gender pair, which resolves to one value in both directions).
    matrix = [[child_of(col, row) for col in roster] for row in roster]
    pd_.write_csv('AllCombos.csv', matrix, bom=True, delimiter=';')
    print(f"AllCombos.csv: {len(roster)}x{len(roster)}")


if __name__ == '__main__':
    generate(pd_.load_db(), pd_.load_breeding(), pd_.read_roster())
