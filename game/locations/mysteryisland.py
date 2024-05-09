from game import location
import game.config as config
from game.display import announce
from game.events import *
import game.items as items



class MysteryIsland(location.Location):
    def __init__(self,x,y,w):
        super().__init__(x, y, w)
        self.name = "Mystery Island"
        self.symbol = "I"
        self.visitable = True
        self.starting_location = MysteryBeach(self)
        self.locations = {
            "beach": self.starting_location,
            "forest": MysteryForest(self),
            "cave": MysteryCave(self),
            "cliff": MysteryCliff(self),
            "ruins": MysteryRuins(self)
        }

    def enter(self, ship):
        announce("You've arrived at the Mysterious Island.")

    def visit(self):
        config.the_player.location = self.starting_location
        config.the_player.location.enter()
        super().visit()


class MysteryBeach(location.SubLocation):
    def __init__(self, m):
        super().__init__(m)
        self.name = "beach"  #"forest" to "beach"
        self.verbs["beach"] = self
        self.verbs["forest"] = self
        self.verbs["cave"] = self
        self.verbs["cliff"] = self
        self.verbs["ruins"] = self
        self.verbs["leave"] = self

        self.treasure_collected = False
        self.treasure = items.Treasure("Mystery Diamond", 100)

    def enter(self):
        announce(
            " Choose a location to visit: \nMystery Beach \nMystery Forest  \nMystery Cave  \nMystery Cliff \nMystery Ruins \nLeave Mystery Island\n"
        )
        if self.treasure_collected== False:
            announce(
                "You step onto the sandy shores of the Mystery Beach, noticing something hidden in the sand."
            )
            self.treasure = items.Treasure("Unique Crystal", 50)
            #config.the_player.add_to_inventory(self.treasure)
            self.treasure_collected = True
        else:
            announce("You walk along the familiar sandy shores of the Mystery Beach.")

        announce(
            "You are on the Mystery Beach. Choose a location to explore: \nForest  \nCave  \nCliff \nRuins\n"
        )

    def process_verb(self, verb, cmd_list, nouns):
        if verb == "beach":
            config.the_player.next_loc = self.main_location.locations["beach"]
        if verb == "forest":
            config.the_player.next_loc = self.main_location.locations["forest"]
        if verb == "cave":
            config.the_player.next_loc = self.main_location.locations["cave"]
        if verb == "cliff":
            config.the_player.next_loc = self.main_location.locations["cliff"]
        if verb == "ruins":
            config.the_player.next_loc = self.main_location.locations["ruins"]
        if verb == "leave":
            announce("You return to your ship.")
            config.the_player.next_loc = config.the_player.ship
            config.the_player.visiting = False




class MysteryForest(location.SubLocation):
    def __init__(self, m):
        super().__init__(m)
        self.name = "forest"
        self.verbs["beach"] = self
        self.verbs["forest"] = self
        self.verbs["cave"] = self
        self.verbs["cliff"] = self
        self.verbs["ruins"] = self
        self.verbs["leave"] = self
        self.event_chance = 25
        self.events.append (seagull.Seagull())
        self.events.append(drowned_pirates.DrownedPirates())

        self.riddle_solved = False
        self.treasures = [
            items.Treasure("Diamond", 100),
            items.Treasure("Crystal", 100),
        ]
        self.treasures_collected = False

    def enter(self):
        if not self.treasures_collected and not self.riddle_solved:
            announce(
                "You venture into the dense, mysterious forest, sensing hidden treasures and a wise old parrot awaiting with a challenge."
            )
            self.collect_treasures()
            self.treasures_collected = True
            self.start_encounter()
        elif not self.riddle_solved:
            announce(
                "The dense forest seems less mysterious now, but the wise old parrot still awaits with its unsolved riddle."
            )
            self.start_encounter()
        else:
            announce(
                "The forest is peaceful, and the wise old parrot nods in respect, its riddle now a memory."
            )

    def process_verb(self, verb, cmd_list, nouns):
        if verb == "beach":
            config.the_player.next_loc = self.main_location.locations["beach"]
        if verb == "forest":
            config.the_player.next_loc = self.main_location.locations["forest"]
        if verb == "cave":
            config.the_player.next_loc = self.main_location.locations["cave"]
        if verb == "cliff":
            config.the_player.next_loc = self.main_location.locations["cliff"]
        if verb == "ruins":
            config.the_player.next_loc = self.main_location.locations["ruins"]
        if verb == "leave":
            announce("You return to your ship.")
            config.the_player.next_loc = config.the_player.ship
            config.the_player.visiting = False
        

    def collect_treasures(self):
        for treasure in self.treasures:
            announce(f"You found a {treasure.name} worth {treasure.value} points!")
            config.the_player.add_to_inventory(self.treasure)
        announce("You have collected all the scattered treasures in the forest!")

    def start_encounter(self):
        announce(
            "A squirrel asks: 'Solve my riddle to pass: What gets wet while drying?'"
        )
        self.solve_riddle()

    def solve_riddle(self):
        player_answer = input("Your answer: ").strip().lower()
        if player_answer == "towel":
            announce("Correct! The parrot squawks in approval and allows you to pass.")
            self.riddle_solved = True
            # Add a friendly squirrel that offers to guide you deeper into the forest
            announce(
                "The friendly squirrel offers to guide you deeper into the forest."
            )
        else:
            announce("Incorrect! The squirrel says Try again.")
            self.start_encounter()



class MysteryCliff(location.SubLocation):
    def __init__(self, m):
        super().__init__(m)
        self.name = "cliff"
        self.verbs["beach"] = self
        self.verbs["forest"] = self
        self.verbs["cave"] = self
        self.verbs["cliff"] = self
        self.verbs["ruins"] = self
        self.verbs["leave"] = self

        self.event_chance = 20
        self.treasure = items.Treasure("Ancient Coin", 200)
        self.treasure_collected = False
        self.events.append (seagull.Seagull())
        self.events.append(drowned_pirates.DrownedPirates())

    def enter(self):
        if not self.treasure_collected:
            announce(
                "You stand at the edge of a high cliff, a glint from the ground catching your eye."
            )
            #config.the_player.collect_treasures(self.treasure)
            self.treasure_collected = True
            #paragliding
            announce(
                "You notice a paragliding kit nearby. Would you like to try paragliding from the cliff? (yes/no)"
            )
            choice = input().strip().lower()
            if choice == "yes":
                announce(
                    "You take the leap and experience a paragliding adventure!"
                )
            elif choice == "no":
                announce(
                    "You decide to enjoy the view from the cliff."
                )
        else:
            announce(
                "The cliff offers a breathtaking view of the sea, the mystery of the hidden treasure now solved."
            )

    def process_verb(self, verb, cmd_list, nouns):
        if verb == "beach":
            config.the_player.next_loc = self.main_location.locations["beach"]
        if verb == "forest":
            config.the_player.next_loc = self.main_location.locations["forest"]
        if verb == "cave":
            config.the_player.next_loc = self.main_location.locations["cave"]
        if verb == "cliff":
            config.the_player.next_loc = self.main_location.locations["cliff"]
        if verb == "ruins":
            config.the_player.next_loc = self.main_location.locations["ruins"]
        if verb == "leave":
            announce("You return to your ship.")
            config.the_player.next_loc = config.the_player.ship
            config.the_player.visiting = False            



class MysteryCave(location.SubLocation):
    def __init__(self, m):
        super().__init__(m)
        self.name = "cave"
        self.verbs["beach"] = self
        self.verbs["forest"] = self
        self.verbs["cave"] = self
        self.verbs["cliff"] = self
        self.verbs["ruins"] = self
        self.verbs["leave"] = self
        

        self.special_item = None
        self.item_collected = False
        self.puzzle_solved = False

    def enter(self):
        if not self.item_collected and not self.puzzle_solved:
            announce(
                "You enter a dark cave, and you are provided with a puzzle to solve."
            )
            #config.the_player.collect_treasures(self.treasure)
            self.item_collected = True
            self.start_puzzle()
        elif not self.puzzle_solved:
            announce(
                "The cave, now less intimidating with the special item in your possession, still holds the unsolved puzzle."
            )
            self.start_puzzle()
        else:
            announce(
                "The cave is silent now and everything here is explored."
            )

    def process_verb(self, verb, cmd_list, nouns):
        if verb == "beach":
            config.the_player.next_loc = self.main_location.locations["beach"]
        if verb == "forest":
            config.the_player.next_loc = self.main_location.locations["forest"]
        if verb == "cave":
            config.the_player.next_loc = self.main_location.locations["cave"]
        if verb == "cliff":
            config.the_player.next_loc = self.main_location.locations["cliff"]
        if verb == "ruins":
            config.the_player.next_loc = self.main_location.locations["ruins"]
        if verb == "leave":
            announce("You return to your ship.")
            config.the_player.next_loc = config.the_player.ship
            config.the_player.visiting = False


    def start_puzzle(self):
        announce("Five people were eating apples, A finished before B, but behind C. D finished before E, but behind B.")
        self.solve_puzzle()

    def solve_puzzle(self):
        max_guess = 3
        while max_guess != 0:
            announce(f"You have {max_guess} chance to solve it")
            player_answer = input("What was the finishing order?").strip().lower()
            if player_answer == "cabde":
                announce("Correct! CABDE")
                self.puzzle_solved = True
                max_guess = 0
                # Add a mysterious figure that reveals a hidden passage deeper into the cave
                announce(
                    "A mysterious figure appears and reveals a hidden passage deeper into the cave."
                )
                announce("You go inside there and find a treasure and leave the cave.")
            else:
                announce("That's not right. Think carefully and try again.")
                max_guess -= 1
                announce(f"{max_guess} chances left. Do you think you can do it !!!!!!")
                if max_guess == 0:
                    announce("YOUU LOSTTTT !!! LEAVE THE ISLAND!!!!")
                


    


class MysteryRuins(location.SubLocation):
    def __init__(self, m):
        super().__init__(m)
        self.name = "ruins"  
        self.verbs["beach"] = self
        self.verbs["forest"] = self
        self.verbs["cave"] = self
        self.verbs["cliff"] = self
        self.verbs["leave"] = self

        self.treasure_collected = False

    def enter(self):
        if not self.treasure_collected:
            announce(
                "You step into a big castle ruin. You explore around and find dead skeletons of animals. You get attacked by zombies of dead pirates."
            )
            self.treasures = items.Treasure("Ruby", 100)
            self.treasure_collected = True
            announce("You have found a big amount of gold and silver to rennovate your ship. Your ship is going to look luxurious.")
            self.events.append(drowned_pirates.DrownedPirates())
        else:
            announce("You have been to the ruins and fought the dead pirates. You probably wouldn't want to go there.")

    def process_verb(self, verb, cmd_list, nouns):
        if verb == "beach":
            config.the_player.next_loc = self.main_location.locations["beach"]
        if verb == "forest":
            config.the_player.next_loc = self.main_location.locations["forest"]
        if verb == "cave":
            config.the_player.next_loc = self.main_location.locations["cave"]
        if verb == "cliff":
            config.the_player.next_loc = self.main_location.locations["cliff"]
        if verb == "ruins":
            config.the_player.next_loc = self.main_location.locations["ruins"]
        if verb == "leave":
            announce("You return to your ship.")
            config.the_player.next_loc = config.the_player.ship
            config.the_player.visiting = False
