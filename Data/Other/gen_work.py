"""Generate Data/WorkSuitability.csv -- 12 work-type ratings per pal -- from
PalCalc's db. Columns follow _paldata.WORK_FIELDS, the order the app expects."""
import _paldata as pd_


def generate(db, roster):
    index = pd_.pal_index(db)
    pd_.require_all(index, roster)
    rows = []
    for pal in roster:
        ws = index[pal]['WorkSuitability']
        rows.append([pal] + [ws[field] for field in pd_.WORK_FIELDS])
    pd_.write_csv('WorkSuitability.csv', rows)
    print(f"WorkSuitability.csv: {len(rows)} pals x {len(pd_.WORK_FIELDS)} work types")


if __name__ == '__main__':
    generate(pd_.load_db(), pd_.read_roster())
