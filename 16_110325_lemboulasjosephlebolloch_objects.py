#%%
import numpy as np
import random as rd

#%%
class RadioactivityAgent:
    def __init__ (self,pos,zone):
        self.pos = pos
        self.zone = zone
        self.radioactivity = self.compute_radioactivity()
    
    def compute_radioactivity(self):
        if self.zone == "z3":
            return rd.uniform(0.66,1)
        elif self.zone == "z2":
            return rd.uniform(0.33,0.66)
        else:
            return rd.uniform(0,0.33)
# %%
class WasteDisposalZone(RadioactivityAgent):
    def __init__(self,pos,zone):
        super().__init__(self,pos,zone)
        self.radioactivity = -1
# %%
class Waste:
    def __init__(self, pos, color):
        self.pos = pos
        self.color = color

# %%