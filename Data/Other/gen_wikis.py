"""Generate Data/Wikis.csv -- fandom wiki page URLs, keyed by roster name.
Roster-only (no PalCalc needed): the URL is built from the display name."""
import _paldata as pd_

# Our display name -> fandom article title, where they differ.
FANDOM_TITLE = {
    'Gumoss (Special)': 'Gumoss',
    'Ribunny': 'Ribbuny',
    'Ribunny Botan': 'Ribbuny Botan',
}


def _title(pal):
    return FANDOM_TITLE.get(pal, pal).replace(' ', '_')


def generate(roster):
    rows = [[pal, f"https://palworld.fandom.com/wiki/{_title(pal)}"] for pal in roster]
    pd_.write_csv('Wikis.csv', rows)
    print(f"Wikis.csv: {len(rows)} urls")


if __name__ == '__main__':
    generate(pd_.read_roster())
