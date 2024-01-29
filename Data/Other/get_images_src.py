import csv
import pandas as pd
import requests
from bs4 import BeautifulSoup

pals = pd.read_csv(r'../Pals.csv', header=None)

print("Getting images sources..")

csv_data = []

# Exceptions
no_image_src = ["No Image", "https://consultix.radiantthemes.com/demo-nine/wp-content/"
                    "themes/consultix/images/no-image-found-360x250.png"]

for pal in pals[0]:
    # Variable Declaration
    url_pal = pal
    alt_pal = pal

    # Exceptions
    if pal == "Gumoss (Special)":
        url_pal = "Gumoss"
        alt_pal = "Gumoss"
    elif pal == "Ribunny":
        url_pal = "Ribbuny"
        alt_pal = "Ribbuny"
    elif " " in pal:
        url_pal = pal.replace(" ", "_")

    url = f"https://palworld.fandom.com/wiki/{url_pal}?file={url_pal}.png"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "lxml")
        src = soup.find("img", {"alt": alt_pal}).get("src")
        src = src.split(".png")[0] + ".png"
        csv_data.append([pal, src])

print("Image sources successfully obtained.")

with open('../Images.csv', 'w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerows(csv_data)
    writer.writerow(no_image_src)

print("CSV file created successfully.")
