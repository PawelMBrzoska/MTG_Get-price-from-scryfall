import json
import sys
import os
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import json
import requests
import urllib.request
from PIL import Image                                                                                


os.chdir(os.path.dirname(sys.argv[0]))

def clean(name, set_name):
    name = name.replace(" ", "_")
    set_name = set_name.replace(" ", "_")
    set_name = set_name.replace("_(M15)","")
    set_name = set_name.replace("_(M14)","")
    set_name = set_name.replace("_(M13)","")
    set_name = set_name.replace("_(M12)","")
    set_name = set_name.replace("_(M11)","")
    set_name = set_name.replace("_(M10)","")
    set_name = set_name.replace("10th_Edition", "Tenth_Edition")
    set_name = set_name.replace("9th_Edition", "Ninth_Edition")
    set_name = set_name.replace(":", "")
    set_name = set_name.replace("Commander_Streets_of_New_Capenna", "New_Capenna_Commander")
    set_name = set_name.replace("Modern_Horizons_2_Extras", "Modern_Horizons_1_Timeshifts")
    set_name = set_name.replace("Mystery_Booster_Cards", "Mystery_Booster")
    name = name.replace("_(Showcase)", "")
    name = name.replace("_(Extended_Art)", "")
    if "_(Retro_Frame)_(Foil_Etched)" in name:
        bonus = "+finishes:['foil','etched']"
        name = name.replace("_(Retro_Frame)_(Foil_Etched)", "")
        set_name = "Modern_Horizons_1_Timeshifts"

    return(name, set_name)

df = pd.read_excel("inventory.xlsx")
bonus = ""
Eurosy = []

for index, row in df.iterrows():
    name = row["Card"]
    set_name = row["Set"]
    bonus = ""
    name, set_name = clean(name,set_name)
    try:
        # Try to recover data using stryfall ID. 
        if row["ID"] == row["ID"]:
            print(row["ID"])
            request = requests.get("https://api.scryfall.com/cards/"+row["ID"]) # sometimes something crashes here making type error. Mainly badly saved ID
            if row["Foil"] == "No": 
                price_eu = request.json()['prices']['eur']
                price_us = request.json()['prices']['usd']
            if row["Foil"] == "Yes":
                price_eu = request.json()['prices']['eur_foil']
                price_us = request.json()['prices']['usd_foil']
            df['Eurosy'][index] = price_eu
            df['Dolary'][index] = price_us
            df['ID'][index] = f"{request.json()['set']}/{request.json()['collector_number']}"
            df.to_excel("inventory.xlsx")
        else: 
            i = 1 - "string" # Lazy way to make a Type error xD

    except TypeError:
        # TypeError occure when there is no ID. Then use name and set.
        try:
            request = requests.get("https://api.scryfall.com/cards/search?order=set&q=name="+name+"+set="+set_name+bonus)

            if row["Foil"] == "No": 
                price_eu = request.json()['data'][0]['prices']['eur']
                price_us = request.json()['data'][0]['prices']['usd']
            if row["Foil"] == "Yes":
                price_eu = request.json()['data'][0]['prices']['eur_foil']
                price_us = request.json()['data'][0]['prices']['usd_foil']
            df['Eurosy'][index] = price_eu
            df['Dolary'][index] = price_us
            # Save the ID
            df['ID'][index] = f"{request.json()['data'][0]['set']}/{request.json()['data'][0]['collector_number']}"
            df.to_excel("inventory.xlsx")
            #print(name+price)
        except KeyError:
            # But sometimes there are error in set name - most commonly - then get all the card version and...
            request = requests.get("https://api.scryfall.com/cards/search?order=set&q=name="+name+"+unique:prints")
            print(row)
            for i in request.json()["data"]:
                print(f"card set (to use in cleaning) = {i['set_name']}")
                print(f"cardid = {i['set']}/{i['collector_number']}")
                urllib.request.urlretrieve(i['image_uris']['normal'],"a.png")                                                                          
                img = Image.open('a.png')
                img.show()                    
            
            # Choose which one to use. 
            card_id=str(input("Past the ID e.g.[hmm/32] here:"))
            # And use this ID to retrieve info normally
            request = requests.get("https://api.scryfall.com/cards/"+card_id)
            if row["Foil"] == "No": 
                price_eu = request.json()['prices']['eur']
                price_us = request.json()['prices']['usd']
            if row["Foil"] == "Yes":
                price_eu = request.json()['prices']['eur_foil']
                price_us = request.json()['prices']['usd_foil']
            df['Eurosy'][index] = price_eu
            df['Dolary'][index] = price_us
            # Save the ID
            df['ID'][index] = f"{request.json()['set']}/{request.json()['collector_number']}"
            df.to_excel("inventory.xlsx")



    






