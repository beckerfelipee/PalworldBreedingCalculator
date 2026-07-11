import csv
import json
import subprocess
import urllib.parse

import pandas as pd

pals = pd.read_csv(r'../Pals.csv', header=None)

print("Getting images sources..")

csv_data = []

# Exceptions
no_image_src = ["No Image", "https://consultix.radiantthemes.com/demo-nine/wp-content/"
                    "themes/consultix/images/no-image-found-360x250.png"]

# Name mismatches between our Pals.csv display names and the fandom wiki article titles.
ALIASES = {
    "Gumoss (Special)": "Gumoss",
    "Ribunny": "Ribbuny",
    "Ribunny Botan": "Ribbuny Botan",
}

# Manual overrides for pals whose wiki page has no usable pageimage (or needs a
# specific known-good source).
MANUAL_SRC = {
    "Hangyu": "https://www.paldeck.xyz/_next/image?url=https%3A%2F%2Fres.cloudinary.com%2Fdierlpbxm%2Fimage%2Fupload"
              "%2Fv1705439180%2Fhangyu_8e2e97eccd.png&w=640&q=75 ",
    "Yakumo": "https://static.wikia.nocookie.net/palworld/images/b/ba/Yakumo.png",
    # These two pages have no MediaWiki "page image" property set, so the API's
    # prop=pageimages lookup returns nothing even though the file exists.
    "Ice Reptyro": "https://static.wikia.nocookie.net/palworld/images/5/57/Ice_Reptyro.png",
    "Ice Kingpaca": "https://static.wikia.nocookie.net/palworld/images/b/bd/Ice_Kingpaca.png",
}

# NOTE: palworld.fandom.com's HTML pages are Cloudflare-blocked in some sandboxed
# environments (both curl and requests get blocked), but the MediaWiki API is not.
# We use action=query&prop=pageimages to fetch the canonical infobox image URL
# directly, instead of scraping HTML.


def fetch_image(title: str):
    q = urllib.parse.quote(title.replace(" ", "_"))
    url = (
        f"https://palworld.fandom.com/api.php?action=query&titles={q}"
        "&prop=pageimages&piprop=original&format=json"
    )
    try:
        out = subprocess.run(
            ["curl", "-s", "--max-time", "15", url],
            capture_output=True, timeout=20,
        )
        data = json.loads(out.stdout)
        pages = data.get("query", {}).get("pages", {})
        for page in pages.values():
            if "original" in page:
                src = page["original"]["source"]
                # Strip the "/revision/latest?cb=..." suffix for a stable, clean URL.
                if ".png" in src:
                    src = src.split(".png")[0] + ".png"
                return src
    except Exception as exc:  # noqa: BLE001
        print(f"Error fetching image for {title}: {exc}")
    return None


missing = []
for pal in pals[0]:
    if pal in MANUAL_SRC:
        csv_data.append([pal, MANUAL_SRC[pal]])
        continue

    title = ALIASES.get(pal, pal)
    src = fetch_image(title)
    if src:
        csv_data.append([pal, src])
    else:
        missing.append(pal)

if missing:
    print("Warning, no image found for:", missing)

print("Image sources successfully obtained.")

with open('../Images.csv', 'w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerows(csv_data)
    writer.writerow(no_image_src)

print("CSV file created successfully.")
