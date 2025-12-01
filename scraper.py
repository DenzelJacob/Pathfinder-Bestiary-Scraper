import requests
from bs4 import BeautifulSoup
import time
import csv

BASE = "https://www.d20pfsrd.com"

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


#  Get all monster pages individually by type
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
        if href.__contains__("/bestiary/monster-listings/"+type_url.split("/")[-2]): 
            monster_type_lists[index].append({
            "name": text,
            "url": href,
            "type": type_url.split("/")[-2]  # Extract type from URL    
        })


for monster_type_list in monster_type_lists: #O(1) 13 times

    for monster in monster_type_list:

        print("Scraping monster:", monster["name"], "from", monster["url"])

        response = requests.get(monster["url"])
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "lxml")

        # Extract CR from the monster page
        cr = None

        for tag in soup.find_all(["b", "strong", "p", "h1" ,"span",'title', "th" ,"td"]):

            txt = tag.get_text().strip()
           
            if txt.startswith("CR "): 
                cr = txt.replace("CR", "")[:4].strip() # fix for mythic levels etc.  
                break

            elif "CR" in txt:
                parts = txt.split("CR")
                
                cr_part = parts[1].strip()
                cr = cr_part[:4].strip()  # Take up to 4 characters after "CR"
                break

        if not cr:
            
            cr = "UNKNOWN" 

        monster["cr"] = cr
        

# Print summary of results
print("\nDONE. Summary of monsters scraped:")

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


# Save results to CSV
with open("pathfinder_monsters_raw.csv", "w", newline='', encoding='utf-8') as csvfile:
    fieldnames = ["name", "url", "type", "cr"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for monster_list in monster_type_lists:
        for monster in monster_list:
            writer.writerow(monster)

print("\nData saved to pathfinder_monsters_raw.csv")