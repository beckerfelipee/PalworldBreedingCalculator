"""Generate Data/Images.csv -- infobox image URLs, keyed by roster name.

The slowest step: one MediaWiki API call per pal. We hit the fandom API
(action=query&prop=pageimages) rather than scraping HTML, because fandom's HTML
pages are Cloudflare-blocked in some sandboxes while the API is not. Pals with no
usable page image are simply omitted; the app falls back to the "No Image" row.
"""
import json
import subprocess
import urllib.parse

import _paldata as pd_

NO_IMAGE = ["No Image", "https://consultix.radiantthemes.com/demo-nine/wp-content/"
            "themes/consultix/images/no-image-found-360x250.png"]

# Our display name -> fandom article title, where they differ.
FANDOM_TITLE = {
    'Gumoss (Special)': 'Gumoss',
    'Ribunny': 'Ribbuny',
    'Ribunny Botan': 'Ribbuny Botan',
}

# Pals whose wiki page has no usable pageimage (or needs a specific known-good src).
MANUAL_SRC = {
    'Yakumo': 'https://static.wikia.nocookie.net/palworld/images/b/ba/Yakumo.png',
}


def fetch_image(title):
    query = urllib.parse.quote(title.replace(' ', '_'))
    url = (
        f"https://palworld.fandom.com/api.php?action=query&titles={query}"
        "&prop=pageimages&piprop=original&format=json"
    )
    try:
        out = subprocess.run(
            ["curl", "-s", "--max-time", "15", url], capture_output=True, timeout=20
        )
        pages = json.loads(out.stdout).get("query", {}).get("pages", {})
        for page in pages.values():
            if "original" in page:
                src = page["original"]["source"]
                # Strip the "/revision/latest?cb=..." suffix for a stable, clean URL.
                for ext in (".png", ".webp"):
                    if ext in src:
                        return src.split(ext)[0] + ext
                return src
    except Exception as exc:  # noqa: BLE001
        print(f"  error fetching image for {title}: {exc}")
    return None


def generate(roster):
    rows, missing = [], []
    for pal in roster:
        if pal in MANUAL_SRC:
            rows.append([pal, MANUAL_SRC[pal]])
            continue
        src = fetch_image(FANDOM_TITLE.get(pal, pal))
        if src:
            rows.append([pal, src])
        else:
            missing.append(pal)
    if missing:
        print("  WARNING no image found for:", missing)
    rows.append(NO_IMAGE)
    pd_.write_csv('Images.csv', rows)
    print(f"Images.csv: {len(rows) - 1} pals"
          + (f" ({len(missing)} missing)" if missing else ""))
    return missing


if __name__ == '__main__':
    generate(pd_.read_roster())
