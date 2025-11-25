import requests
from bs4 import BeautifulSoup
import time
import csv

BASE = "https://www.d20pfsrd.com"
START_URL = BASE + "/bestiary/monster-listings/"


#  Get all monster  pages

response = requests.get(START_URL)
response.raise_for_status()
soup = BeautifulSoup(response.text, "lxml")


monster_type_links = []

# Monster types appear as <li><a href="...">Aberrations</a></li>
for page_ref in soup.select("li a"):

    href = page_ref.get("href", "")
    #print("With href:", href)
    if href.__contains__("/bestiary/monster-listings/"): # fix here --- look into a.get("href", "")
        monster_type_links.append({
            "name": page_ref.text.strip(),
            "url": href
        })

print("Monster types found:", len(monster_type_links))
print(monster_type_links)

