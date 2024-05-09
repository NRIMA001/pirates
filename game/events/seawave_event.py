from game import event
from game.player import Player
from game.context import Context
import game.config as config
import random

class  Seawaves(Context, event.Event):
    '''Encounter with seawaves approaching, which results in ship imbalance'''
    def __init__ (self):
        super().__init__()
        self.name = "seawaves"
        self.seawaves= 1
        self.result = {}

    def process_verb (self, verb, cmd_list, nouns):
        self.go = True
        r = random.randint(1,10)
        if (r < 5):
            self.result["message"] = "the seawave calms down."
            if (self.seagulls > 1):
                self.seawaves = self.seawaves - 1
        else:
            c = random.choice(config.the_player.get_pirates())
            if (c.isLucky() == True):
                self.result["message"] = "luckily, the seawave doesn't harm anyone."
            else:
                self.result["message"] = c.get_name() + " is getting harmed by the seawaves."
                if (c.inflict_damage (self.seawaves, "Harmed by seawave")):
                    self.result["message"] = ".. " + c.get_name() + " is thrown off the ship by the seawave!"

    
    def process (self, world):
        self.go = False
        self.result = {}
        self.result["newevents"] = [ self ]
        self.result["message"] = "default message"

        
        print ("A big seawave has occured.")
           

        return self.result
