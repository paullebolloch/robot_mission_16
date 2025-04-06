#agents.py

import mesa
from objects import WasteDisposalZone, RadioactivityAgent, Waste



class MyAgent(mesa.Agent):
    """An agent with fixed initial knowledge."""

    def __init__(self, model):
        super().__init__(model)
        self.knowledge = {"grid_size": (self.model.grid.width, self.model.grid.height),
            "position": self.pos,
            "possible_steps": [],
            "neighbor_waste_disposal_zone": [],
            "neighbor_radioactivity_agent": [],
            "neighbor_waste": [],
            "neighbor_robot": [],
            "neighbors": []}
        self.next_action = []

    def perceive(self, percepts):
        """Update agent's perception of its environment using Von Neumann neighborhood."""
        self.knowledge["neighbors"] = percepts

        # Reset memory
        self.knowledge["possible_steps"] = []
        self.knowledge["neighbor_waste_disposal_zone"] = []
        self.knowledge["neighbor_radioactivity_agent"] = []
        self.knowledge["neighbor_waste"] = []
        self.knowledge["neighbor_robot"] = []

        for agent in self.knowledge["neighbors"]:
            if isinstance(agent, WasteDisposalZone):
                self.knowledge["neighbor_waste_disposal_zone"].append([agent, agent.pos, agent.radioactivity])
            if isinstance(agent, RadioactivityAgent):
                self.knowledge["neighbor_radioactivity_agent"].append([agent, agent.pos, agent.radioactivity])
            if isinstance(agent, Waste):
                self.knowledge["neighbor_waste"].append([agent, agent.color])
            if isinstance(agent, MyAgent):
                self.knowledge["neighbor_robot"].append([agent, agent.pos])


    def deliberate(self):

        # Determine possible steps (only cells that are not occupied by other MyAgent)
        impossible_steps = []
        for agent in self.knowledge["neighbor_robot"]:
            impossible_steps.append(agent[1])
        
        for position in self.model.grid.get_neighborhood(self.pos, moore=False):
            if position not in impossible_steps:
                self.knowledge["possible_steps"].append(position)

        self.next_action.append("move_random")


    def do(self):
        """Execute the decided action."""
        return self.next_action[-1]
        
    def step(self):
        """Execute the agent's step."""
        
        self.deliberate()
        action = self.do()
        percepts = self.model.do(self, action)
        self.perceive(percepts)

'''

from mesa import Agent

action_list = ["move_up", "move_down", "move_forward", "move_backward", "pick_up", "transform", "put_down"]
cell_range = {'green' : [], 'blue' : [], 'yellow' : []}

class greenAgent(Agent):
    def __init__(self, model):
        super().__init__(model)
        self.knowledge = {
            'position' : None,
            'perception' : None,
            'target' : None,
            'actions_history' : [],  
        }
        self.hold_waste = False
        self.cell_range = cell_range['green']
        
    def update(self, knowledge, percepts):
        knowledge['perception'] = percepts

    def deliberate(self, knowledge):

        (current_pos, percepts, target, history) = tuple(knowledge.values())
        
        if 'waste' in percepts[current_pos] and not self.hold_waste:
            return 'pick_up'
        
        possible_steps = self.model.grid.get_neighborhood(
            current_pos, moore=False, include_center=False
            )
        
        (x, y) = current_pos
        right_to_move = [cell for cell in possible_steps if percepts[cell] != 'robot' and cell in cell_range]
        to_take_waste = [cell for cell, content in percepts.items() if content == 'waste' and cell[0]<x]

        if self.hold_waste:
                if (x+1, y) in right_to_move:
                    return 'move_forward'
                elif (x+1, y) not in cell_range:
                    return 'put_down'
                else:
                    if (x, y+1) in right_to_move and target[1]>y:
                        return 'move_up'
                    elif (x, y-1) in right_to_move and target[1]<y:
                        return 'move_down'
                    else :
                        return 'wait'
           
        if len(to_take_waste)>0:
            return 'move_left'
        
        if (x-1, y) in right_to_move and (x-1, y) in cell_range:
            return 'move_backward'
    


        

    def step_agent(self, percepts):
        self.update(self.knowledge, percepts)
        action = self.deliberate(self.knowledge)
        percepts = self.model.do(self, action)



    '''