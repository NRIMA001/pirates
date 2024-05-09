from game import event
from game.player import Player
from game.context import Context
import game.config as config
import random

class Shark(Context, event.Event):
    '''Encounter with a dangerous shark while exploring the ocean.'''
    def __init__(self):
        super().__init__()
        self.name = "shark encounter"
        self.sharks = 1
        self.verbs['swim away'] = self
        self.verbs['attack'] = self
        self.verbs['hide'] = self
        self.result = {}
        self.go = False

    def process_verb(self, verb, cmd_list, nouns):
        if verb == "swim away":
            self.go = True
            r = random.randint(1, 10)
            if r < 5:
                self.result["message"] = "You manage to swim away from the shark."
                if self.sharks > 1:
                    self.sharks -= 1
            else:
                c = random.choice(config.the_player.get_pirates())
                if c.isLucky():
                    self.result["message"] = "Luckily, the shark loses interest and swims away."
                else:
                    self.result["message"] = c.get_name() + " is attacked by the shark."
                    if c.inflict_damage(self.sharks, "Bitten by a shark"):
                        self.result["message"] = ".. " + c.get_name() + " is bitten to death by the shark!"

        elif verb == "attack":
            self.go = True
            c = random.choice(config.the_player.get_pirates())
            if c.isLucky():
                self.result["message"] = "You manage to fend off the shark and escape."
            else:
                self.result["message"] = c.get_name() + " is attacked by the shark."
                if c.inflict_damage(self.sharks, "Bitten by a shark"):
                    self.result["message"] = ".. " + c.get_name() + " is bitten to death by the shark!"
        
        elif verb == "hide":
            self.go = True
            self.result["message"] = "You find a hiding spot and wait for the shark to pass."
        
        else:
            print("Your options are to 'swim away', 'attack', or 'hide'.")
            self.go = False

    def process(self, world):
        self.go = False
        self.result = {}
        self.result["newevents"] = [self]
        self.result["message"] = "A shark has appeared! What do you want to do?"
        
        while not self.go:
            print(str(self.sharks) + " shark(s) has appeared. What do you want to do?")
            Player.get_interaction([self])

        return self.result
