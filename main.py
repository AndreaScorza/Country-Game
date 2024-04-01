import random
import time
import json
from threading import Timer

# Function to load country names from an external JSON file
def load_countries(filename):
    with open(filename, 'r') as file:
        return json.load(file)

# Function to get the number of players and their names
def get_player_details():
    players = []
    num_players = int(input("Enter the number of players (1-5): "))
    for i in range(num_players):
        name = input(f"Enter player {i+1} name: ")
        players.append({"name": name, "score": 0})
    return players

# Function to randomly select a country and ensure it's not repeated
def select_country(countries, already_guessed):
    country = random.choice([c for c in countries if c not in already_guessed])
    already_guessed.add(country)
    return country

# Function for a player's turn, including the timer
def player_turn(player, country, already_guessed):
    def time_up():
        print("\nTime's up!")
        already_guessed.add(country)  # Ensure the country is marked as guessed even if time runs out

    print(f"{player['name']}, your country to locate is: {country}")
    print("You have 30 seconds. Press Enter when ready...")
    
    timer = Timer(30.0, time_up)
    timer.start()
    input()  # Wait for player to press Enter
    timer.cancel()  # Stop the timer if the player presses Enter before time is up
    
    if timer.is_alive():
        print("Correct! +1 point")
        player['score'] += 1
    else:
        print("Moving to the next player...")

# Function to display scores
def display_scores(players):
    print("\n--- Current Scores ---")
    for player in players:
        print(f"{player['name']}: {player['score']}")

# Main function to run the game
def game_rounds(players, countries, already_guessed, rounds):
    for round in range(rounds):
        print(f"\n--- Round {round+1} ---")
        for player in players:
            if len(already_guessed) == len(countries):
                print("Congratulations! All countries have been guessed. Game over.")
                return True
            country = select_country(countries, already_guessed)
            player_turn(player, country, already_guessed)
    return False

def main():
    countries = load_countries("countries.json")  # Load countries from JSON
    players = get_player_details()
    already_guessed = set()

    while True:
        rounds = int(input("\nEnter the number of rounds: "))
        game_finished = game_rounds(players, countries, already_guessed, rounds)
        display_scores(players)  # Display scores after each set of rounds

        if game_finished:
            break

        continue_game = input("Do you want to continue the game? (yes/no): ")
        if continue_game.lower() != "yes":
            break

    print("\n--- Game Over ---\nFinal scores:")
    for player in players:
        print(f"{player['name']}: {player['score']}")

if __name__ == "__main__":
    main()
