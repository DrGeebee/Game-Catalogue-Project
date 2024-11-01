import xml.etree.ElementTree as ET

game_collection = []

def load_games_from_launchbox_xml(file_path):
    global game_collection  # Ensure we're modifying the global collection
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()

        for game in root.findall('Game'):
            title = game.find('Title').text if game.find('Title') is not None else "Unknown Title"
            release_date = game.find('ReleaseDate').text if game.find('ReleaseDate') is not None else "Unknown Release Date"
            developer = game.find('Developer').text if game.find('Developer') is not None else "Unknown Developer"
            publisher = game.find('Publisher').text if game.find('Publisher') is not None else "Unknown Publisher"
            platform = game.find('Platform').text if game.find('Platform') is not None else "Unknown Platform"

            game_info = {
                'Title': title,
                'Release Date': release_date,
                'Publisher': publisher,
                'Developer': developer,
                'Platform': platform  # Ensure this line is included
            }
            game_collection.append(game_info)

        print("Games loaded into collection successfully.")

    except Exception as e:
        print(f"Error loading XML file: {e}")

def load_games_from_excel(file_path):
    # Your existing code for loading games from Excel
    pass

def add_game():
    game_title = input("Enter the game title: ")
    game_year = input("Enter the release year: ")
    game_publisher = input("Enter the publisher: ")
    
    game_info = {
        'Title': game_title,
        'Year': game_year,
        'Publisher': game_publisher
    }
    game_collection.append(game_info)
    print(f"Added '{game_title}' to your collection.")
