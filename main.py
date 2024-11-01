import os
import json
import xml.etree.ElementTree as ET
from datetime import datetime
from user_input import add_game


# Default path to the XML file (can be changed by the user)
xml_file_path = ""
last_import_file = 'last_import.json'
game_collection = []  # Initialize the game collection
xml_path_file = 'xml_path.json'  # File to save the XML path

# Path to save last import time
last_import_file = 'last_import.json'

# Load last import time from file
def load_last_import_time():
    if os.path.exists(last_import_file):
        with open(last_import_file, 'r') as f:
            return datetime.fromisoformat(json.load(f))
    return None

# Save current import time to file
def save_current_import_time():
    with open(last_import_file, 'w') as f:
        json.dump(datetime.now().isoformat(), f)

# Load XML file path from file
def load_xml_file_path():
    global xml_file_path
    if os.path.exists(xml_path_file):
        with open(xml_path_file, 'r') as f:
            xml_file_path = json.load(f)

# Save XML file path to file
def save_xml_file_path():
    with open(xml_path_file, 'w') as f:
        json.dump(xml_file_path, f)

# Check if the XML file has been updated
def has_xml_file_updated(last_import_time):
    current_mod_time = datetime.fromtimestamp(os.path.getmtime(xml_file_path))
    return last_import_time is None or current_mod_time > last_import_time

# Function to load games from XML and save to JSON
def load_games_and_save_to_json(file_path, json_file_path):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()

        # Create a list to hold game info
        game_list = []

        for game in root.findall('Game'):
            title = game.find('Title').text if game.find('Title') is not None else "Unknown Title"
            release_date = game.find('ReleaseDate').text if game.find('ReleaseDate') is not None else "Unknown Release Date"
            developer = game.find('Developer').text if game.find('Developer') is not None else "Unknown Developer"
            publisher = game.find('Publisher').text if game.find('Publisher') is not None else "Unknown Publisher"
            platform = game.find('Platform').text if game.find('Platform') is not None else "Unknown Platform"

            # Create a dictionary for each game
            game_info = {
                'Title': title,
                'Release Date': release_date,
                'Developer': developer,
                'Publisher': publisher,
                'Platform': platform
            }
            game_list.append(game_info)

        # Save to JSON file
        with open(json_file_path, 'w') as json_file:
            json.dump(game_list, json_file, indent=4)

        print(f"Games loaded and saved to {json_file_path} successfully.")

    except Exception as e:
        print(f"Error loading XML file: {e}")

# Function to re-import the games
def reimport_games():
    last_import_time = load_last_import_time()
    if has_xml_file_updated(last_import_time):
        # Load and save each XML file to JSON
        xml_files = [f for f in os.listdir(xml_file_path) if f.endswith('.xml')]
        for xml_file in xml_files:
            file_path = os.path.join(xml_file_path, xml_file)
            json_file_path = os.path.join(xml_file_path, f"{os.path.splitext(xml_file)[0]}.json")
            load_games_and_save_to_json(file_path, json_file_path)
        save_current_import_time()  # Update last import time
        print("Games have been re-imported successfully.")
    else:
        print("No updates found. The XML file has not been modified since the last import.")

# Function to set the XML file path and load games
def set_xml_file_path():
    global xml_file_path  # Declare the variable as global
    new_path = input("Enter the full path to your LaunchBox XML folder: ")
    
    if os.path.isdir(new_path):  # Check if the path is a directory
        xml_file_path = new_path
        print(f"XML file path set to: {xml_file_path}")
        save_xml_file_path()  # Save the XML file path

        # Automatically load XML files found in the directory
        xml_files = [f for f in os.listdir(xml_file_path) if f.endswith('.xml')]
        
        if xml_files:
            for xml_file in xml_files:
                file_path = os.path.join(xml_file_path, xml_file)
                json_file_path = os.path.join(xml_file_path, f"{os.path.splitext(xml_file)[0]}.json")
                load_games_and_save_to_json(file_path, json_file_path)
                print(f"Loaded games from: {file_path}")
        else:
            print("No XML files found in the specified directory.")
    else:
        print("The specified path does not exist. Please check the path and try again.")

# Function to filter and view games by platform
def view_games_by_platform():
    if not game_collection:
        print("No games in the collection.")
        return
    
    # Get unique platforms from the game collection
    platforms = set(game['Platform'] for game in game_collection)
    
    if not platforms:
        print("No platforms available in the game collection.")
        return

    print("Available platforms:")
    for idx, platform in enumerate(sorted(platforms), start=1):
        print(f"{idx}. {platform}")

    choice = input("Select a platform number to view games: ")
    
    try:
        platform_index = int(choice) - 1
        selected_platform = sorted(platforms)[platform_index]

        # Display games for the selected platform
        print(f"\nGames for platform '{selected_platform}':")
        for game in sorted(game_collection, key=lambda x: x['Title']):
            if game['Platform'] == selected_platform:
                print(f"- {game['Title']} ({game['Release Date']}) by {game['Developer']}")

    except (ValueError, IndexError):
        print("Invalid selection. Please enter a valid platform number.")

# Function to load games from JSON
def load_games_from_json(json_file_path):
    global game_collection
    if os.path.exists(json_file_path):
        with open(json_file_path, 'r') as json_file:
            game_collection = json.load(json_file)
        print(f"Loaded games from {json_file_path} successfully.")
    else:
        print(f"No JSON file found at {json_file_path}.")

# Load XML file path at the start of the program
load_xml_file_path()

# Main program loop
while True:
    print("\nOptions:")
    print("1. Set XML file path")
    print("2. Add a game to the collection")
    print("3. View game collection")
    print("4. Load games from JSON")
    print("5. Re-import games from XML")
    print("6. Exit")
    
    # Get the user's choice
    choice = input("Enter the number of your choice: ")

    if choice == "1":
        set_xml_file_path()  # Allow user to set the XML file path
    elif choice == "2":
        add_game()  # Call your function for adding games (assume it's in user_input.py)
    elif choice == "3":
        view_games_by_platform()  # View games by platform
    elif choice == "4":
        json_file_path = input("Enter the path of the JSON file to load: ")
        load_games_from_json(json_file_path)  # Load games from JSON
    elif choice == "5":
        reimport_games()
    elif choice == "6":
        print("Goodbye!")
        break
    else:
        print("Invalid choice, please select 1, 2, 3, 4, 5, or 6.")
