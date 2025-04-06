#objects.py

import numpy as np
import random as rd
import mesa

class RadioactivityAgent(mesa.Agent):
    def __init__ (self,model,zone):
        super().__init__(model)
        self.zone = zone
        self.radioactivity = self.compute_radioactivity()
    
    def compute_radioactivity(self):
        if self.zone == "z3":
            return rd.uniform(0.66,1)
        elif self.zone == "z2":
            return rd.uniform(0.33,0.66)
        else:
            return rd.uniform(0,0.33)

class WasteDisposalZone(RadioactivityAgent):
    def __init__(self,model,zone):
        super().__init__(model,zone)
        self.radioactivity = -1

class Waste(mesa.Agent):
    def __init__(self, model, color):
        super().__init__(model) 
        self.color = color

