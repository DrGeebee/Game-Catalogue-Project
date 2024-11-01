from user_input import game_collection

def view_collection():
    if game_collection:
        sorted_collection = sorted(game_collection, key=lambda x: x['Title'])
        print("Your game collection:")
        for game in sorted_collection:
            print(f"- {game['Title']} ({game['Year']}) - {game['Publisher']}")
    else:
        print("Your collection is empty.")

def view_games_by_platform():
    # Function to view games by platform as before
    pass
