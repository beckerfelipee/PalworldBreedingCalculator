import csv
import pandas as pd

pals = pd.read_csv(r'../Pals.csv', header=None)

print("Getting wiki urls..")

csv_data = []

for pal in pals[0]:
    if " " in pal:
        url_pal = pal.replace(" ", "_")
    else:
        url_pal = pal

    # Exception
    if pal == "Gumoss (Special)":
        url_pal = "Gumoss"
    elif pal == "Ribunny":
        url_pal = "Ribbuny"

    url = f"https://palworld.fandom.com/wiki/{url_pal}"
    csv_data.append([pal, url])

print("Wikis successfully obtained.")

with open('../Wikis.csv', 'w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerows(csv_data)

print("CSV file created successfully.")
