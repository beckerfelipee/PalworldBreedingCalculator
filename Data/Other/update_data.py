"""Regenerate every Data/*.csv from scratch, in dependency order.

    python update_data.py                # everything
    python update_data.py --skip-images  # skip the slow fandom image fetch

Game data (Pals, WorkSuitability, AllCombos) comes from PalCalc; image and wiki
links come from the fandom wiki. Run this after a game patch -- once PalCalc has
datamined it (check the printed version).

The roster is rebuilt from PalCalc here, so new pals flow in automatically; no
manual Pals.csv edit is needed. The generators fail loudly rather than emit bad
data if something structural changed (a rename, a new name collision, or a new
gender-dependent pair) -- fix the aliases/overrides in _paldata and re-run.
"""
import csv
import sys

import _paldata as pd_
import gen_combos
import gen_images
import gen_pals
import gen_wikis
import gen_work


def main(skip_images=False):
    db = pd_.load_db()
    breeding = pd_.load_breeding()
    print(f"PalCalc data version: {db.get('Version')}\n")

    roster = gen_pals.generate(db)          # writes Pals.csv, the roster contract
    gen_work.generate(db, roster)
    gen_combos.generate(db, breeding, roster)
    gen_wikis.generate(roster)
    if skip_images:
        print("Images.csv: skipped (--skip-images)")
    else:
        gen_images.generate(roster)

    _validate(roster)
    print("\nDone.")


def _validate(roster):
    """Guard against silently shipping a broken breeding matrix."""
    n = len(roster)
    with open(pd_.data_path('AllCombos.csv'), newline='', encoding='utf-8-sig') as f:
        matrix = [row for row in csv.reader(f, delimiter=';')]

    problems = []
    if len(matrix) != n or any(len(row) != n for row in matrix):
        problems.append(f"AllCombos.csv is not {n}x{n}")
    else:
        roster_set = set(roster)
        for i, pal in enumerate(roster):
            if matrix[i][i] != pal:
                problems.append(f"self-breed wrong: {pal} + {pal} -> {matrix[i][i]}")
                break
        if any(matrix[i][j] != matrix[j][i] for i in range(n) for j in range(i + 1, n)):
            problems.append("matrix is not symmetric")
        strangers = {c for row in matrix for c in row} - roster_set
        if strangers:
            problems.append(f"results outside roster: {sorted(strangers)[:5]}")

    if problems:
        raise SystemExit("VALIDATION FAILED:\n  " + "\n  ".join(problems))
    print(f"\nValidation OK: {n} pals, {n * n} combos, symmetric, self-breed consistent.")


if __name__ == '__main__':
    main(skip_images='--skip-images' in sys.argv)
