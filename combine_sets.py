import os
import json
import re

# -------------------------------- Helper Functions -------------------------------- #

# Generates a special key for each card
def get_card_key(card):
    return (card["number"], card["name"], card["setName"])

# Adds imgSrc to each card
def generate_img_src(card):

    name = str(card.get("name", "")) # Just ensures the name is a string
    number = str(card.get("number", "")) # Just ensures the number is a string

    cleaned_name = re.sub(r'[^a-zA-Z0-9]', '', name) # Removes everything that isn't a letter or number, including spaces and punctuation
    match = re.match(r".*([a-zA-Z])$", number)
    version_suffix = ""

    if match: # For cards like the Promotional House Points
        letter = match.group(1).lower()
        version_number = ord(letter) - ord('a') + 1  # a → 1, b → 2, etc.
        version_suffix = f"V{version_number}"

    return f"{cleaned_name}{version_suffix}.png" # Joins the modified text with .png at the end

# Cleans up Adventure type cards of toSolve and reward, removing them from effect
def clean_adventure_cards(cards):
    changes_made = 0 # Keeps track of how many adventure cards are being modified, starts at 0
    for card in cards: # Creates a loop that runs through each card in the cards array
        if "Adventure" in card.get("type", []): # Checks if any of the types of card is adventure
            if "effect" in card and isinstance(card["effect"], list): # Checks if there is an effect key and if it is an array/list of strings
                # This deletes any strings that begin with "to solve:" or "reward:"
                new_effect = [
                    line for line in card["effect"]
                    if not re.match(r"^\s*(to solve:|reward:)", line, re.IGNORECASE)
                ]
                # If it cleaned the card, this will print out which card was cleaned and then add 1 to the changes_made to keep track
                if len(new_effect) != len(card["effect"]):
                    print(f"Cleaning Adventure card: {card["name"]}")
                    card["effect"] = new_effect
                    changes_made +=1
    print(f"Cleaned {changes_made} Adventure cards") # Prints out how many adventure cards were cleaned

# -------------------------------- Setting Paths -------------------------------- #

base_dir = os.path.dirname(__file__)
all_sets = os.path.join(base_dir, "sets")
rulings_file = os.path.join(base_dir, "rules", "rules.json")

# -------------------------------- Loading Rulings -------------------------------- #

rulings_by_card = {} # Creates an array/dictionary of each card with an array of rulings that apply to them instead of current rulings with an array of cards they apply to
try:
    try:
        with open(rulings_file, "r", encoding='utf-8') as f: # Opens ruling file for reading with utf-8 encoding
            rulings_data = json.load(f) # Loads rulings as an object
    except UnicodeDecodeError: # if utf-8 doesn't work try cp1252
        with open(rulings_file, "r", encoding='cp1252') as f: # Opens ruling file for reading with cp1252 encoding (seems to work better)
            rulings_data = json.load(f) # Loads rulings as an object
        
    for entry in rulings_data: # Checks every ruling in the ruling object
        for card_name in entry.get("cards", []): # Will run for each card in each ruling
            if card_name not in rulings_by_card:
                rulings_by_card[card_name] = [] # If the card being read isn't already in rulings_by_card, add it
            ruling_copy = {k: v for k, v in entry.items() if k != "cards"} # Ignore the 'cards' field from each ruling when appending, we only want the actual ruling and date of ruling
            rulings_by_card[card_name].append(ruling_copy) # Takes the data of ruling and date and adds it to the current card being processed 
except Exception as e:
    print(f"Error loading rulings for {e}") # Print an error if the ruling file can't be read/loaded


# -------------------------------- Joining All of the cards -------------------------------- #

all_cards = [] # Creates an empty array for cards from cards.json and any new cards to be added to

# Loop through all of the set folders in "sets"
for setfolder in os.listdir(all_sets): # Looks only for objects in the "sets" folder
    set_path = os.path.join(all_sets, setfolder) # Creates a path that can be looped for each set folder

    if os.path.isdir(set_path): # As long as set_path is a folder run through following loop
        for filename in os.listdir(set_path):
            if filename.endswith(".json"): # Looks only for json files. If more json files are added in the folders, this can be modified to only look for "cards.json"
                file_path = os.path.join(set_path, filename)
                try:
                    try: # This is the same as the rulings, if utf-8 encoding doesn't work, use cp1252 encoding
                        with open(file_path, "r", encoding="utf-8") as f:
                            data = json.load(f) # Load the json file into data object with utf-8 encoding
                    except UnicodeDecodeError:
                        with open(file_path, "r", encoding="cp1252") as f:
                            data = json.load(f) # Load the json file into data object with cp1252 encoding

                    set_name = data.get("setName") # Creates an object for referencing setName to add to each card
                    release_date = data.get("releaseDate") # Creates an object for referencing releaseDate to add to each card
                    cards = data.get("cards", []) # Retrieves the cards array from the sets cards.json

                    for card in cards: # Runs a loop to add setName, releaseDate, imgSrc, rulings, and whether or not the card is horizontal to each card
                        card["setName"] = set_name # Adds the set name to the card
                        card["releaseDate"] = release_date # Adds the release date to the card

                        card["imgSrc"] = generate_img_src(card) # Adds the image source to the card. This will likely need fixing for some cards
                        if any (t.lower() == "spell" for t in card.get("type", [])): # Checks if the cards type is spell
                            card["horizontal"] = False # If the type is spell, set horizontal to false
                        else:
                            card["horizontal"] = True # If the type is not spell, set horizontal to true

                        # Attach rulings if applicable
                        if card["name"] in rulings_by_card: # Checks if the card has any rulings
                            card["rulings"] = rulings_by_card[card["name"]] # If it does, add it here
                        else:
                            card["rulings"] = []

                        all_cards.append(card) # Finally add the card to the all cards array
                except Exception as e:
                    print(f"Error reading {file_path}: {e}") # Print an error for any problems reading/loading any of the sets cards.json

# -------------------------------- Clean Adventure Cards -------------------------------- #

clean_adventure_cards(all_cards)

# -------------------------------- Merge New Cards with Existing json file -------------------------------- #

existing_cards = [] # Creates an empty array to add cards from main cards.json
existing_keys = set() # Creates an empty set to add the cards special keys to prevent duplication when reading sets cards.json files

if os.path.exists("cards.json"):
    try:
        try: # Same as previous, first attempt loading with utf-8 encoding and then cp1252 if unsuccessful
            with open("cards.json", "r", encoding="utf-8") as f:
                existing_cards = json.load(f) # Overrides empty array with full array of main cards.json
        except UnicodeDecodeError:
            with open("cards.json", "r", encoding="cp1252") as f:
                existing_cards = json.load(f) # Overrides empty array with full array of main cards.json
        existing_keys = {get_card_key(card) for card in existing_cards} #Overrides the empty set of special keys by creating a special key for each card in the main cards.json
    except Exception as e:
        print(f"Failed to read existing cards.json: {e}") # Print error if completely unable to read/load


existing_dict = {get_card_key(card): card for card in existing_cards}
new_cards = [] # Creates an empty array to append new cards that aren't already in the main cards.json
updated_cards = []

for card in all_cards: # Checks every card in all cards
    card_key = get_card_key(card) # Creates a special key for each card

    if card_key not in existing_keys: # If the special key is not in the existing keys of the main cards.json cards run this
        print(f"Found new card: {card["name"]} (from {card["setName"]})")
        new_cards.append(card) # Add new card to new cards array
        existing_dict[card_key] = card
    else:
        existing_card = existing_dict[card_key]
        if card != existing_card:
            print(f"Updated card: {card["name"]} (from {card["setName"]})")
            updated_cards.append(card)
            existing_dict[card_key] = card


existing_cards = list(existing_dict.values())
        

# -------------------------------- Saving new JSON and JS files -------------------------------- #

with open("cards.json", 'w', encoding='utf-8') as f: # Open the main cards.json file for writing
    json.dump(existing_cards, f, indent=4) # Replace with All cards, both already in cards.json and any new cards

# JS file will be the same as the JSON but with "export const cards = " before the array to make it usable as JS
cards_js_string = "export const cards = " + json.dumps(existing_cards, indent=2) # Set a new object to "export const cards = " followed by All cards, including both current and new cards
with open("cards.js", 'w', encoding='utf-8') as f: # Open the main cards.js file for writing
    f.write(cards_js_string) # Replace with the previoiusly made object of all cards made for JS


# -------------------------------- Confirmation -------------------------------- #


print(f"✅ Added {len(new_cards)} new cards.") # Prints how many new cards were added

print(f"✅ Updated {len(updated_cards)} existing cards.") # Prints how many new cards were added

print("Export complete, cards.js and cards.json") # Print out a line to notify of script completion