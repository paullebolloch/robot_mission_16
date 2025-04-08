#agents.py

import mesa
from objects import WasteDisposalZone, RadioactivityAgent, Waste



'''class MyAgent(mesa.Agent):
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


class greenAgent(mesa.Agent):
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
        self.agent_color = "green"

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
                self.knowledge["neighbor_waste_disposal_zone"].append({"agent": agent,"pos": agent.pos,"radioactivity": agent.radioactivity})
            if isinstance(agent, RadioactivityAgent):
                self.knowledge["neighbor_radioactivity_agent"].append({"agent": agent, "pos": agent.pos,"radioactivity": agent.radioactivity})
            if isinstance(agent, Waste):
                self.knowledge["neighbor_waste"].append({"agent": agent,"pos": agent.pos, "color": agent.color})
            if isinstance(agent, greenAgent) or isinstance(agent, yellowAgent) or isinstance(agent, redAgent):
                self.knowledge["neighbor_robot"].append({"agent": agent,"pos": agent.pos, "agent_color": agent.agent_color})


    def deliberate(self):

        # Determine possible steps (only cells that are not occupied by other MyAgent)
        impossible_steps = []

        # Agent don't want to be in the same cell as another agent
        for agent in self.knowledge["neighbor_robot"]:
            impossible_steps.append(agent["pos"])
        
        # Agent want to be in the good zone
        for agent in self.knowledge["neighbor_radioactivity_agent"]:
            if agent["radioactivity"] >= 0.33:
                impossible_steps.append(agent["pos"])

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




class yellowAgent(mesa.Agent):
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
        self.agent_color = "yellow"

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
                self.knowledge["neighbor_waste_disposal_zone"].append({"agent": agent,"pos": agent.pos,"radioactivity": agent.radioactivity})
            if isinstance(agent, RadioactivityAgent):
                self.knowledge["neighbor_radioactivity_agent"].append({"agent": agent, "pos": agent.pos,"radioactivity": agent.radioactivity})
            if isinstance(agent, Waste):
                self.knowledge["neighbor_waste"].append({"agent": agent,"pos": agent.pos, "color": agent.color})
            if isinstance(agent, greenAgent) or isinstance(agent, yellowAgent) or isinstance(agent, redAgent):
                self.knowledge["neighbor_robot"].append({"agent": agent,"pos": agent.pos, "agent_color": agent.agent_color})


    def deliberate(self):

        # Determine possible steps (only cells that are not occupied by other MyAgent)
        impossible_steps = []

        # Agent don't want to be in the same cell as another agent
        for agent in self.knowledge["neighbor_robot"]:
            impossible_steps.append(agent["pos"])
        
        # Agent want to be in the good zone
        for agent in self.knowledge["neighbor_radioactivity_agent"]:
            if agent["radioactivity"] >= 0.66:
                impossible_steps.append(agent["pos"])

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





class redAgent(mesa.Agent):
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
        self.agent_color = "red"

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
                self.knowledge["neighbor_waste_disposal_zone"].append({"agent": agent,"pos": agent.pos,"radioactivity": agent.radioactivity})
            if isinstance(agent, RadioactivityAgent):
                self.knowledge["neighbor_radioactivity_agent"].append({"agent": agent, "pos": agent.pos,"radioactivity": agent.radioactivity})
            if isinstance(agent, Waste):
                self.knowledge["neighbor_waste"].append({"agent": agent,"pos": agent.pos, "color": agent.color})
            if isinstance(agent, greenAgent) or isinstance(agent, yellowAgent) or isinstance(agent, redAgent):
                self.knowledge["neighbor_robot"].append({"agent": agent,"pos": agent.pos, "agent_color": agent.agent_color})


    def deliberate(self):

        # Determine possible steps (only cells that are not occupied by other MyAgent)
        impossible_steps = []

        # Agent don't want to be in the same cell as another agent
        for agent in self.knowledge["neighbor_robot"]:
            impossible_steps.append(agent["pos"])
        
        # Agent want to be in the good zone (red can go anywhere)

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
