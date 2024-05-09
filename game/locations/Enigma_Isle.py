from game import location
from game import items
import game.config as config
from game.display import announce
from game.events import *
import random

class SubLocation(location.SubLocation):
    def __init__(self, m):
        super().__init__(m)
        self.verbs = {
            "beach": self,
            "mystic_grove": self,
            "hidden_temple": self,
            "riddle_peak": self,
            "sirens_cove": self,
            "captains_hideout": self,
            "leave": self
        }

    def process_verb(self, verb, cmd_list, nouns):
        next_loc = self.main_location.locations.get(verb)
        if next_loc:
            config.the_player.next_loc = next_loc
        else:
            announce("Invalid command. Please try again.")

class EnigmaIsle(location.Location):
    def __init__(self,x,y,w):
        super().__init__(x, y, w)
        self.name = "Enigma Isle"
        self.symbol = "E"
        self.visitable = True
        self.starting_location = EnigmaBeach(self)
        self.locations = {
            "beach": self.starting_location,
            "mystic_grove": MysticGrove(self),
            "hidden_temple": HiddenTemple(self),
            "riddle_peak": RiddlePeak(self),
            "sirens_cove": SirensCove(self),
            "captains_hideout": CaptainsHideout(self)
        }

    def enter(self, ship):
        announce("You've arrived at Enigma Isle, a place shrouded in mystery and wonder.")

    def visit(self):
        config.the_player.location = self.starting_location
        config.the_player.location.enter()
        super().visit()
        while config.the_player.visiting:
            self.start_turn ()
            self.process_turn ()
            self.end_turn ()
        # Reset to default after visiting
        config.the_player.location = config.the_player.ship
        config.the_player.next_loc = None

class EnigmaBeach(location.SubLocation):
    def __init__(self, m):
        super().__init__(m)
        self.name = "beach"
        self.verbs["beach"] = self
        self.verbs["mystic_grove"] = self
        self.verbs["hidden_temple"] = self
        self.verbs["riddle_peak"] = self
        self.verbs["sirens_cove"]=self
        self.verbs["captains_hideout"]=self
        self.verbs["leave"] = self

        self.treasure_collected = False
        self.treasure = items.TreasureItem("Enigmatic Pearl", 150)

    def collect_treasures(self):
        for treasure in self.treasures:
            announce(f"You found a {treasure.name}, a mystical artifact worth {treasure.value} points!")
            config.the_player.add_to_inventory([self.treasure])
            self.treasure_collected = True
        announce("You have discovered all the hidden treasures!")

    def enter(self):
        announce(
            "Welcome to Enigma Beach. Choose a path to explore: \nMystic Grove \nHidden Temple \nRiddle Peak \nSirens Cove \nCaptains Hideout \nLeave Enigma Isle\n"
        )
        if not self.treasure_collected:
            announce(
                "You spot something glimmering in the sand and pick up an Enigmatic Pearl."
            )
            config.the_player.collect_treasure(self.treasure)
            self.treasure_collected = True
        else:
            announce("You stroll along the serene shores of Enigma Beach.")
        if not self.treasure_collected:
            announce(
                "You find a mysterious scroll partially buried in the sand."
            )

    def process_verb(self, verb, cmd_list, nouns):
        if verb == "beach":
            config.the_player.next_loc = self.main_location.locations["beach"]
        elif verb == "mystic_grove":
            config.the_player.next_loc = self.main_location.locations["mystic_grove"]
        elif verb == "hidden_temple":
            config.the_player.next_loc = self.main_location.locations["hidden_temple"]
        elif verb == "riddle_peak":
            config.the_player.next_loc = self.main_location.locations["riddle_peak"]
        elif verb == "sirens_cove":
            config.the_player.next_loc = self.main_location.locations["sirens_cove"]
        elif verb == "captains_hideout":
            config.the_player.next_loc = self.main_location.locations["captains_hideout"]
        elif verb == "leave":
            announce("You return to your ship.")
            config.the_player.next_loc = config.the_player.ship
            config.the_player.visiting = False

class MysticGrove(location.SubLocation):
    def __init__(self, m):
        super().__init__(m)
        self.name = "mystic_grove"
        self.verbs["beach"] = self
        self.verbs["mystic_grove"] = self
        self.verbs["hidden_temple"] = self
        self.verbs["riddle_peak"] = self
        self.verbs["sirens_cove"]=self
        self.verbs["captains_hideout"]=self
        self.verbs["leave"] = self

        self.riddle_solved = False
        self.treasures = [
            items.TreasureItem("Mystic Amulet", 200),
            items.TreasureItem("Ancient Relic", 150),
            items.TreasureItem("Enchanted Flower", 100),
        ]
        self.treasures_collected = False
    def collect_treasures(self):
        for treasure in self.treasures:
            announce(f"You found a {treasure.name}, a mystical artifact worth {treasure.value} points!")
            config.the_player.add_to_inventory([self.treasure])
            self.treasure_collected = True
        announce("You have discovered all the hidden treasures within Mystic Grove!")

    def enter(self):
        if not self.treasures_collected and not self.riddle_solved:
            announce(
                "You enter the Mystic Grove, surrounded by whispering trees and hidden treasures."
            )
            self.collect_treasures()
            self.treasures_collected = True
            self.start_riddle()
        elif not self.riddle_solved:
            announce(
                "The Mystic Grove exudes an aura of ancient magic, yet the enigmatic riddle remains unsolved."
            )
            self.start_riddle()
        else:
            announce(
                "The Mystic Grove is serene, its mysteries unlocked and treasures claimed."
            )
    def collect_treasures(self):
        for treasure in self.treasures:
            announce(f"You found a {treasure.name}, a mystical artifact worth {treasure.value} points!")
            config.the_player.add_to_inventory([self.treasure])
            self.treasure_collected = True
        announce("You have discovered all the hidden treasures within the Mystic Grove!")

    def process_verb(self, verb, cmd_list, nouns):
        if verb == "beach":
            config.the_player.next_loc = self.main_location.locations["beach"]
        elif verb == "mystic_grove":
            config.the_player.next_loc = self.main_location.locations["mystic_grove"]
        elif verb == "hidden_temple":
            config.the_player.next_loc = self.main_location.locations["hidden_temple"]
        elif verb == "riddle_peak":
            config.the_player.next_loc = self.main_location.locations["riddle_peak"]
        elif verb == "sirens_cove":
            config.the_player.next_loc = self.main_location.locations["sirens_cove"]
        elif verb == "captains_hideout":
            config.the_player.next_loc = self.main_location.locations["captains_hideout"]
        elif verb == "leave":
            announce("You return to your ship.")
            config.the_player.next_loc = config.the_player.ship
            config.the_player.visiting = False

    def collect_treasures(self):
        for treasure in self.treasures:
            announce(f"You found a {treasure.name}, a mystical artifact worth {treasure.value} points!")
            config.the_player.add_to_inventory(self.treasures)
            self.treasure_collected = True
        announce("You have discovered all the hidden treasures within the Mystic Grove!")

    def start_riddle(self):
        announce(
            "A spectral voice echoes through the trees: 'What has keys but can't open locks?'\n"
        )
        self.solve_riddle()

    def solve_riddle(self):
        player_answer = input("Your answer: ").strip().lower()
        if player_answer == "piano":
            announce("Correct! The forest spirits rejoice, granting you passage.")
            self.riddle_solved = True
            # Add a path to the hidden temple
            announce(
                "A path materializes, leading to the Hidden Temple."
            )
        else:
            announce("Incorrect! The enigma persists, try again.")
            self.start_riddle()

class HiddenTemple(location.SubLocation):
    def __init__(self, m):
        super().__init__(m)
        self.name = "hidden_temple"
        self.verbs["beach"] = self
        self.verbs["mystic_grove"] = self
        self.verbs["hidden_temple"] = self
        self.verbs["riddle_peak"] = self
        self.verbs["sirens_cove"]=self
        self.verbs["captains_hideout"]=self
        self.verbs["leave"] = self

        self.treasure = items.TreasureItem("Lost Scroll", 250)
        # config.the_player.add_to_inventory([self.treasure])
        self.treasure_collected = False

    def collect_treasures(self):
        for treasure in self.treasures:
            announce(f"You found a {treasure.name} worth {treasure.value} points!")
            config.the_player.collect_treasure(treasure)
        announce("You have collected all the scattered treasures in the forest!")
    

    def enter(self):
        if not self.treasure_collected:
            announce(
                "You step into the Hidden Temple, its ancient walls adorned with forgotten wisdom."
            )
            config.the_player.collect_treasure(self.treasure)
            self.treasure_collected = True
            # Add an event or puzzle related to the hidden treasure
            self.start_puzzle_event()
            announce(
                "A mysterious altar beckons, its secrets waiting to be uncovered."
            )
        else:
            announce(
                "The Hidden Temple remains silent, its secrets now revealed and treasures claimed."
            )
    def start_puzzle_event(self):
        # Word jumble puzzle
        word_bank = ["TEMPLE", "ANCIENT", "WISDOM", "MYSTERY"]
        secret_word = random.choice(word_bank)
        scrambled_word = ''.join(random.sample(secret_word, len(secret_word)))

        announce("You encounter a mysterious puzzle at the altar.")
        announce(f"Unscramble the word: {scrambled_word}")

        attempts = 3
        while attempts > 0:
            player_guess = input("Enter your guess: ").strip().upper()
            if player_guess == secret_word:
                announce("Congratulations! You've solved the puzzle.")
                # Provide rewards or progress the game
                break
            else:
                announce("Incorrect guess. Try again.")
                attempts -= 1
                announce(f"You have {attempts} attempts remaining.")
        else:
            announce("You've run out of attempts. The puzzle remains unsolved.")

    def process_verb(self, verb, cmd_list, nouns):
        if verb == "beach":
            config.the_player.next_loc = self.main_location.locations["beach"]
        elif verb == "mystic_grove":
            config.the_player.next_loc = self.main_location.locations["mystic_grove"]
        elif verb == "hidden_temple":
            config.the_player.next_loc = self.main_location.locations["hidden_temple"]
        elif verb == "riddle_peak":
            config.the_player.next_loc = self.main_location.locations["riddle_peak"]
        elif verb == "sirens_cove":
            config.the_player.next_loc = self.main_location.locations["sirens_cove"]
        elif verb == "captains_hideout":
            config.the_player.next_loc = self.main_location.locations["captains_hideout"]
        elif verb == "leave":
            announce("You return to your ship.")
            config.the_player.next_loc = config.the_player.ship
            config.the_player.visiting = False

class RiddlePeak(location.SubLocation):
    def __init__(self, m):
        super().__init__(m)
        self.name = "riddle_peak"
        self.verbs["beach"] = self
        self.verbs["mystic_grove"] = self
        self.verbs["hidden_temple"] = self
        self.verbs["riddle_peak"] = self
        self.verbs["sirens_cove"]=self
        self.verbs["captains_hideout"]=self
        self.verbs["leave"] = self

        self.puzzle_solved = False

    def enter(self):
        if not self.puzzle_solved:
            announce(
                "You ascend Riddle Peak, its summit wreathed in clouds and enigmatic puzzles."
            )
            self.start_puzzle()
        else:
            announce(
                "Riddle Peak stands silent, its mysteries solved and challenges conquered."
            )

    def process_verb(self, verb, cmd_list, nouns):
        if verb == "beach":
            config.the_player.next_loc = self.main_location.locations["beach"]
        elif verb == "mystic_grove":
            config.the_player.next_loc = self.main_location.locations["mystic_grove"]
        elif verb == "hidden_temple":
            config.the_player.next_loc = self.main_location.locations["hidden_temple"]
        elif verb == "riddle_peak":
            config.the_player.next_loc = self.main_location.locations["riddle_peak"]
        elif verb == "sirens_cove":
            config.the_player.next_loc = self.main_location.locations["sirens_cove"]
        elif verb == "captains_hideout":
            config.the_player.next_loc = self.main_location.locations["captains_hideout"]
        elif verb == "leave":
            announce("You return to your ship.")
            config.the_player.next_loc = config.the_player.ship
            config.the_player.visiting = False

    def start_puzzle(self):
        announce("You encounter a series of cryptic puzzles, each more perplexing than the last.")
        self.solve_puzzle()

    def display_grid(self, grid):
        for row in grid:
            print(" ".join(row))

    def solve_puzzle(self):
        announce("You encounter a mysterious puzzle. You see a grid of buttons labeled with letters.")
        announce("The goal is to arrange the letters to form a secret word.")

        # Define the puzzle solution
        secret_word = "treasure"

        # Define the initial grid
        grid = [
            ['t', 'r', 'e', 'a'],
            ['s', 'u', 'r', 'e'],
            ['a', 't', 's', 'r'],
            ['e', 'u', 't', 'r']
        ]

        # Initialize variables to track user progress
        solved = False
        attempts = 3

        # Loop until the puzzle is solved or the player runs out of attempts
        while not solved and attempts > 0:
            # Display the current grid
            announce("Current Grid:")
            self.display_grid(grid)

            # Prompt the player for input
            player_input = input("Enter your guess: ").strip().lower()

            # Check if the player's guess matches the secret word
            if player_input == secret_word:
                announce("Congratulations! You've solved the puzzle and unlocked the treasure!")
                solved = True
            else:
                announce("Incorrect guess. Try again.")
                attempts -= 1
                announce(f"You have {attempts} attempts remaining.")

        # If the player runs out of attempts without solving the puzzle
        if not solved:
            announce("You've run out of attempts. The puzzle remains unsolved.")

class SirensCove(location.SubLocation):
    def __init__(self, m):
        super().__init__(m)
        self.name = "sirens_cove"
        self.verbs["beach"] = self
        self.verbs["mystic_grove"] = self
        self.verbs["hidden_temple"] = self
        self.verbs["riddle_peak"] = self
        self.verbs["sirens_cove"]=self
        self.verbs["captains_hideout"]=self
        self.verbs["leave"] = self
        self.verbs["sirens"] = self
        self.verbs["leave"] = self
        self.sequence = ['A', 'B', 'C', 'D']  # Example musical notes
        self.attempts = 3
        self.song_solved = False

    def enter(self):
        announce("You've entered the Siren's Cove. A mysterious melody fills the air.")
        if not self.song_solved:
            self.play_melody()

    def process_verb(self, verb, cmd_list, nouns):
        if verb == "beach":
            config.the_player.next_loc = self.main_location.locations["beach"]
        elif verb == "mystic_grove":
            config.the_player.next_loc = self.main_location.locations["mystic_grove"]
        elif verb == "hidden_temple":
            config.the_player.next_loc = self.main_location.locations["hidden_temple"]
        elif verb == "riddle_peak":
            config.the_player.next_loc = self.main_location.locations["riddle_peak"]
        elif verb == "sirens_cove":
            config.the_player.next_loc = self.main_location.locations["sirens_cove"]
        elif verb == "captains_hideout":
            config.the_player.next_loc = self.main_location.locations["captains_hideout"]
        elif verb == "leave":
            announce("You return to your ship.")
            config.the_player.next_loc = config.the_player.ship
            config.the_player.visiting = False

    def play_melody(self):
        for i in range(1, 4):
            announce(f"Round {i}: Memorize the sequence!")
            self.display_sequence(i)
            player_input = input("Repeat the sequence: ").strip().upper()
            if player_input == ''.join(self.sequence[:i]):
                announce("Correct! The sirens are pleased.")
            else:
                announce("Incorrect sequence. The sirens are displeased.")
                self.attempts -= 1
                if self.attempts == 0:
                    announce("The sirens have cast you out!")
                    return
        announce("You've calmed the sirens and earned the mystical trident.")
        self.song_solved = True

    def display_sequence(self, length):
        announce(' '.join(self.sequence[:length]))



class CaptainsHideout(location.SubLocation):
    def __init__(self, m):
        super().__init__(m)
        self.name = "captains_hideout"
        self.verbs["beach"] = self
        self.verbs["mystic_grove"] = self
        self.verbs["hidden_temple"] = self
        self.verbs["riddle_peak"] = self
        self.verbs["sirens_cove"]=self
        self.verbs["captains_hideout"]=self
        self.verbs["leave"] = self
        self.verbs["explore"] = self
        self.verbs["leave"] = self
        self.lever_order = ['Skull', 'Anchor', 'Ship', 'Treasure']
        self.map_found = False

    def enter(self):
        announce("You've discovered the Captain's Hideout, filled with old maps and pirate relics.")
        if not self.map_found:
            self.play_memory_game()

    def play_memory_game(self):
        announce("A wall of levers appears, each marked with different symbols.")
        self.show_sequence()
        player_input = input("Enter the correct order of symbols: ").strip().title()
        if player_input == ' '.join(self.lever_order):
            announce("Correct! A hidden compartment opens revealing a treasure map and other relics.")
            self.map_found = True
        else:
            announce("Incorrect. The levers reset ominously.")
    def process_verb(self, verb, cmd_list, nouns):
        if verb == "beach":
            config.the_player.next_loc = self.main_location.locations["beach"]
        elif verb == "mystic_grove":
            config.the_player.next_loc = self.main_location.locations["mystic_grove"]
        elif verb == "hidden_temple":
            config.the_player.next_loc = self.main_location.locations["hidden_temple"]
        elif verb == "riddle_peak":
            config.the_player.next_loc = self.main_location.locations["riddle_peak"]
        elif verb == "sirens_cove":
            config.the_player.next_loc = self.main_location.locations["sirens_cove"]
        elif verb == "captains_hideout":
            config.the_player.next_loc = self.main_location.locations["captains_hideout"]
        elif verb == "leave":
            announce("You return to your ship.")
            config.the_player.next_loc = config.the_player.ship
            config.the_player.visiting = False
        

        

    def show_sequence(self):
        # Display the sequence of symbols to the player
        announce("The sequence of symbols:")
        for symbol in self.lever_order:
            announce(symbol)


if __name__ == "__main__":
    # Initialize game configuration
    config.initialize()

    enigma_isle = EnigmaIsle(0, 0, config.world)
    enigma_isle.enter(None)

    # Visit the main location
    enigma_isle.visit()
