# Data Sources & Updating

How the calculator's data is produced, and how to refresh it when Palworld gets a new version.

---

## TL;DR

```
cd Data/Other
python update_data.py        # regenerates every CSV, then validates
```

That one command updates everything. Read on for what it pulls and what to do if it complains.

---

## Where the data comes from

We use **two** sources. All game facts come from a datamined dataset; only the pictures and wiki links come from the wiki.

| Data | File | Source | Why |
|------|------|--------|-----|
| Roster + order | `Pals.csv` | **PalCalc** | datamined from the game files |
| Work suitability | `WorkSuitability.csv` | **PalCalc** | datamined from the game files |
| Breeding results | `AllCombos.csv` | **PalCalc** | datamined from the game files |
| Wiki links | `Wikis.csv` | Palworld **Fandom** wiki | built from the pal name |
| Images | `Images.csv` | Palworld **Fandom** wiki (API) | the dataset has no images |

### PalCalc (the game-data source)

- Repo: <https://github.com/tylercamp/palcalc>
- It extracts breeding results **directly from the game's `.pak` files**, so it matches the real in-game behavior — including the special/unique combos and the changes each patch brings.
- We read two files from it: `db.json` (the pal list, work suitability, names) and `breeding.json` (the full parent + parent → child table).
- It is **versioned** (e.g. `v26`). The updater prints this version so you know which game build the data reflects.

> ⚠️ We do **not** compute breeding with a formula. Palworld's real breeding math isn't a simple "average of the two parents", so a formula gets ~57% of pairs wrong. We use PalCalc's datamined results instead.

---

## How the pieces fit together

```text
┌───────────────────────────────┐   ┌───────────────────────────────┐
│            PalCalc            │   │          Fandom wiki          │
│     (datamined game data)     │   │     (images & wiki links)     │
├───────────────────────────────┤   ├───────────────────────────────┤
│ • Pals.csv  (roster)          │   │ • Wikis.csv                   │
│ • WorkSuitability.csv         │   │ • Images.csv                  │
│ • AllCombos.csv               │   │                               │
└───────────────────────────────┘   └───────────────────────────────┘
                └─────────────────┬─────────────────┘
                                  ▼
                         ┌─────────────────┐
                         │ App  (build.py) │
                         └─────────────────┘
```

**`Pals.csv` is the backbone.** It's generated first; every other file lines up with its list of pals, in the same order. Wiki links and images are matched to those names.

---

## The scripts

All live in `Data/Other/`:

| Script | Makes | Runs alone? |
|--------|-------|-------------|
| `update_data.py` | **everything** (the orchestrator) | — |
| `_paldata.py` | shared helpers (download, names, validation) | no (library) |
| `gen_pals.py` | `Pals.csv` | yes |
| `gen_work.py` | `WorkSuitability.csv` | yes |
| `gen_combos.py` | `AllCombos.csv` | yes |
| `gen_wikis.py` | `Wikis.csv` | yes |
| `gen_images.py` | `Images.csv` | yes |

- **Normal use:** just run `update_data.py`.
- **Reprocess one file** (e.g. images failed): run its generator, like `python gen_images.py`.

---

## Updating for a new game version

```text
   Wait for PalCalc to publish the new version
       │
       ▼
   Run:  python update_data.py  ◄───────────────┐
       │                                        │
       ▼                                        │
   Finished OK?                                 │
       ├── no ──►  fix _paldata.py, then run ───┘
       │
       ▼ yes
   Review the diff & commit
```

### Steps

1. **Wait for PalCalc to update.** We depend on their data, not the game directly. Run the updater and check the printed `PalCalc data version:` — if it didn't go up after a patch, they haven't datamined it yet.
2. **Run it:**
   ```
   cd Data/Other
   python update_data.py
   ```
   New pals are picked up **automatically** — the roster is rebuilt from PalCalc, so you don't hand-edit `Pals.csv`.
3. **If it stops with an error**, it's protecting you from bad data. See below.
4. **Review the diff and commit** once it finishes and validation passes.

> 💡 `python update_data.py --skip-images` skips the slow wiki image step (~2 min) while you're iterating.
