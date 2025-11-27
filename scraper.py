import requests
from bs4 import BeautifulSoup
import time
import csv

BASE = "https://www.d20pfsrd.com"
START_URL = BASE + "/bestiary/monster-listings/"

ABBERATIONS_URL = BASE + "/bestiary/monster-listings/aberrations/"
ANIMAL_URL = BASE + "/bestiary/monster-listings/animals/"
CONSTRUCTS_URL = BASE + "/bestiary/monster-listings/constructs/"
DRAGONS_URL = BASE + "/bestiary/monster-listings/dragons/"
FEY_URL = BASE + "/bestiary/monster-listings/fey/"
HUMANOIDS_URL = BASE + "/bestiary/monster-listings/humanoids/"
MAGICAL_BEASTS_URL = BASE + "/bestiary/monster-listings/magical-beasts/"
MONSTROUS_HUMANOIDS_URL = BASE + "/bestiary/monster-listings/monstrous-humanoids/"
OOZES_URL = BASE + "/bestiary/monster-listings/oozes/"
OUTSIDERS_URL = BASE + "/bestiary/monster-listings/outsiders/"
PLANTS_URL = BASE + "/bestiary/monster-listings/plants/"
UNDEAD_URL = BASE + "/bestiary/monster-listings/undead/"
VERMIN_URL = BASE + "/bestiary/monster-listings/vermin/"

monster_type_urls = [ABBERATIONS_URL, ANIMAL_URL, CONSTRUCTS_URL, DRAGONS_URL, FEY_URL,
                      HUMANOIDS_URL, MAGICAL_BEASTS_URL, MONSTROUS_HUMANOIDS_URL, OOZES_URL,
                      OUTSIDERS_URL, PLANTS_URL, UNDEAD_URL, VERMIN_URL]

# use enumerate(monster_type_urls)

abberations = []
animals = []
constructs = []
dragons = []
fey = []
humanoids = []
magical_beasts = []
monstrous_humanoids = []
oozes = []
outsiders = []
plants = []
undead = []
vermin = []

monster_type_lists = [abberations, animals, constructs, dragons, fey, humanoids,
                       magical_beasts, monstrous_humanoids, oozes, outsiders,
                       plants, undead, vermin]

print
#  Get all monster  pages individually by type

for index, type_url in enumerate(monster_type_urls):
    response = requests.get(type_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "lxml")
    print("Scraping type page:", type_url)
    # Extract monster entries from the type page
    for a in soup.select("a"):
        href = a.get("href", "")
        text = a.text.strip()

        # Only keep links to actual monster pages
        if href.__contains__("/bestiary/monster-listings/"): 
            monster_type_lists[index].append({
            "name": text,
            "url": href
        })
print(dragons)


print("Aberrations found:", len(abberations))
print("Animals found:", len(animals))
print("Constructs found:", len(constructs))
print("Dragons found:", len(dragons))
print("Fey found:", len(fey))
print("Humanoids found:", len(humanoids))
print("Magical Beasts found:", len(magical_beasts))
print("Monstrous Humanoids found:", len(monstrous_humanoids))
print("Oozes found:", len(oozes))
print("Outsiders found:", len(outsiders))
print("Plants found:", len(plants))
print("Undead found:", len(undead))
print("Vermin found:", len(vermin))
#print(abberations)
