
from communication.agent.CommunicatingAgent import CommunicatingAgent
from communication.message.Message import Message
from objects import RadioactivityAgent, Waste, WasteDisposalZone
from utils import choose_move_to_target, map_waste_color

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


class greenAgent(CommunicatingAgent):
    """An agent with fixed initial knowledge."""

    def __init__(self, model):
        super().__init__(model, name=f"green-{id(self)}")
        self.has_waste = None # object agent waste
        self.hold = [0,0,0]
        self.knowledge = {"grid_size": (self.model.grid.width, self.model.grid.height),
            "position": self.pos,
            "possible_steps": [],
            "neighbor_waste_disposal_zone": [],
            "neighbor_radioactivity_agent": [],
            "neighbor_waste": [],
            "neighbor_robot": [],
            "neighbors": []
            
        }
        self.next_action = []
        self.agent_color = "green"

    def get_radioactivity(self, position) -> float:
        (x,y) = position
        for agent in self.knowledge["neighbor_radioactivity_agent"]:
            if agent.pos == (x,y):
                return agent.radioactivity
        print("information undisclosed")
        return -1

        
    def get_waste(self, position) -> list[bool]:
        (x,y) = position
        for agent in self.knowledge["neighbor_waste"]:
            if agent.pos == (x,y):
                return [agent, map_waste_color(agent.color)]
        return [None, [0,0,0]]


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
                self.knowledge["neighbor_waste_disposal_zone"].append(agent)
            if isinstance(agent, RadioactivityAgent):
                self.knowledge["neighbor_radioactivity_agent"].append(agent)
            if isinstance(agent, Waste):
                self.knowledge["neighbor_waste"].append(agent)
            if isinstance(agent, greenAgent) or isinstance(agent, yellowAgent) or isinstance(agent, redAgent):
                self.knowledge["neighbor_robot"].append(agent)


    def deliberate(self):
        # Get current position
        x, y = self.pos[0], self.pos[1]


        # Using the speaking model to get information

    




        # is it on the target ? (i.e. the radioactivity at the right is 0.33 < . < 0.66)
        right_cell = (x+1, y)
        if self.get_radioactivity(right_cell) >=0.33 and self.hold == [0,1,0]:
            self.next_action.append("drop")

            for other_agent in self.model.agents:
                if isinstance(other_agent, yellowAgent) and other_agent != self:
                    message = Message(
                        from_agent=self.get_name(),
                        to_agent=other_agent.get_name(),
                        message_performative=107,
                        content={"type": "drop", "position": self.pos}
                    )
                    self.send_message(message)

            return 

        
        # looking at the current position if a waste is available and what color is it 
        if self.get_waste(self.pos)[1] == [1,0,0]:
        
        # looking at the has_waste variable to know
            # is there another waste already in hand, same colour
            if self.hold == [1,0,0]:          
                self.next_action.append("merge")
                return 
            else :
                self.next_action.append('pick')
                return

        else: 

            # Determine possible steps (only cells that are not occupied by other MyAgent)
            impossible_steps = []

            # Agent don't want to be in the same cell as another agent
            for agent in self.knowledge["neighbor_robot"]:
                impossible_steps.append(agent.pos)
            
            # Agent want to be in the good zone
            for agent in self.knowledge["neighbor_radioactivity_agent"]:
                if agent.radioactivity >= 0.33:
                    impossible_steps.append(agent.pos)

            for position in self.model.grid.get_neighborhood(self.pos, moore=False):
                if position not in impossible_steps:
                    self.knowledge["possible_steps"].append(position)

            self.next_action.append("move_random")

            return 


    def do(self):
        """Execute the decided action."""
        return self.next_action[-1]
        
    
    def step(self):
        """Execute the agent's step."""
        
        self.deliberate()
        action = self.do()
        percepts = self.model.do(self, action)
        self.perceive(percepts)




class yellowAgent(CommunicatingAgent):
    """An agent with fixed initial knowledge."""

    def __init__(self, model):
        super().__init__(model, name=f"yellow-{id(self)}")
        self.has_waste = None # object agent waste
        self.hold = [0,0,0]
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

        # Nouvel attribut pour savoir où aller pour récupérer le déchet 
        self.target = None


    def get_radioactivity(self, position) -> float:
        (x,y) = position
        for agent in self.knowledge["neighbor_radioactivity_agent"]:
            if agent.pos == (x,y):
                return agent.radioactivity
        print("information undisclosed")
        return -1

        
    def get_waste(self, position) -> list[bool]:
        (x,y) = position
        for agent in self.knowledge["neighbor_waste"]:
            if agent.pos == (x,y):
                return [agent, map_waste_color(agent.color)]
        return [None, [0,0,0]]

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
                self.knowledge["neighbor_waste_disposal_zone"].append(agent)
            if isinstance(agent, RadioactivityAgent):
                self.knowledge["neighbor_radioactivity_agent"].append(agent)
            if isinstance(agent, Waste):
                self.knowledge["neighbor_waste"].append(agent)
            if isinstance(agent, greenAgent) or isinstance(agent, yellowAgent) or isinstance(agent, redAgent):
                self.knowledge["neighbor_robot"].append(agent)

    def deliberate(self):

        # Get current position
        x, y = self.pos[0], self.pos[1]

        # Si il a atteint sa target il la supprime
        if self.target  == self.pos:
            self.target = None
        
        # Récupère la position par message quand un vert drop un déchet et le communique
        # Met à jour sa target si elle n'existe pas 
            
        for message in self.get_new_messages():
            if message.get_performative() == 107:
                content = message.get_content()
                if content.get("type") == "drop":
                    waste_pos = content.get("position")
                    if self.target is None:
                        self.target = waste_pos

        # is it on the target ? (i.e. the radioactivity at the right is 0.33 < . < 0.66)
        right_cell = (x+1, y)
        if self.get_radioactivity(right_cell) >=0.66 and self.hold == [0,0,1]:
            self.next_action.append("drop")

            for other_agent in self.model.agents:
                if isinstance(other_agent, redAgent) and other_agent != self:
                    message = Message(
                        from_agent=self.get_name(),
                        to_agent=other_agent.get_name(),
                        message_performative=107,
                        content={"type": "drop", "position": self.pos}
                    )
                    self.send_message(message)

            return 

        
        # looking at the current position if a waste is available and what color is it 
        if self.get_waste(self.pos)[1] == [0,1,0]:
        
        # looking at the has_waste variable to know
            # is there another waste already in hand, same colour
            if self.hold == [0,1,0]:          
                self.next_action.append("merge")
                return 
            else :
                self.next_action.append('pick')
                return

        else: 

            # Determine possible steps (only cells that are not occupied by other MyAgent)
            impossible_steps = []

            # Agent don't want to be in the same cell as another agent
            for agent in self.knowledge["neighbor_robot"]:
                impossible_steps.append(agent.pos)
            
            # Agent want to be in the good zone
            for agent in self.knowledge["neighbor_radioactivity_agent"]:
                if agent.radioactivity >= 0.66:
                    impossible_steps.append(agent.pos)

            for position in self.model.grid.get_neighborhood(self.pos, moore=False):
                if position not in impossible_steps:
                    self.knowledge["possible_steps"].append(position)

            if self.target is not None:
                next_move = choose_move_to_target(self.target, self.pos, self.knowledge["possible_steps"])
                self.next_action.append("move_"+next_move)
            else:
                self.next_action.append("move_random")

            return 



    def do(self):
        """Execute the decided action."""
        return self.next_action[-1]
        

    def step(self):
        """Execute the agent's step."""
        
        self.deliberate()
        action = self.do()
        percepts = self.model.do(self, action)
        self.perceive(percepts)





class redAgent(CommunicatingAgent):
    """An agent with fixed initial knowledge."""

    def __init__(self, model):
        super().__init__(model, name=f"red-{id(self)}")
        self.has_waste = None # object agent waste
        self.hold = [0,0,0]
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


        self.target = None

    def get_radioactivity(self, position) -> float:
        (x,y) = position
        for agent in self.knowledge["neighbor_radioactivity_agent"]:
            if agent.pos == (x,y):
                return agent.radioactivity
        print("information undisclosed")
        return -1

        
    def get_waste(self, position) -> list[bool]:
        (x,y) = position
        for agent in self.knowledge["neighbor_waste"]:
            if agent.pos == (x,y):
                return [agent, map_waste_color(agent.color)]
        return [None, [0,0,0]]
    

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
                self.knowledge["neighbor_waste_disposal_zone"].append(agent)
            if isinstance(agent, RadioactivityAgent):
                self.knowledge["neighbor_radioactivity_agent"].append(agent)
            if isinstance(agent, Waste):
                self.knowledge["neighbor_waste"].append(agent)
            if isinstance(agent, greenAgent) or isinstance(agent, yellowAgent) or isinstance(agent, redAgent):
                self.knowledge["neighbor_robot"].append(agent)

    def deliberate(self):

        # Get current position
        x, y = self.pos[0], self.pos[1]

        if self.get_radioactivity((x,y)) ==-1 and self.hold == [0,0,1]:
            self.next_action.append("drop")
            return 

        
        # looking at the current position if a waste is available and what color is it 
        if self.get_waste(self.pos)[1] == [0,0,1]:
        
        # looking at the has_waste variable to know
            # is there another waste already in hand, same colour
            if self.hold == [0,0,0]:          
                self.next_action.append("pick")
                return 

        # Récupère la position par message quand un vert drop un déchet et le communique
        # Met à jour sa target si elle n'existe pas 
            
        for message in self.get_new_messages():
            if message.get_performative() == 107:
                content = message.get_content()
                if content.get("type") == "drop":
                    waste_pos = content.get("position")
                    if self.target is None:
                        self.target = waste_pos

        # Determine possible steps (only cells that are not occupied by other MyAgent)
        impossible_steps = []

        # Agent don't want to be in the same cell as another agent
        for agent in self.knowledge["neighbor_robot"]:
            impossible_steps.append(agent.pos)
        
        # Agent want to be in the good zone (red can be anywhere)

        for position in self.model.grid.get_neighborhood(self.pos, moore=False):
            if position not in impossible_steps:
                self.knowledge["possible_steps"].append(position)

        if self.target is not None:
                next_move = choose_move_to_target(self.target, self.pos, self.knowledge["possible_steps"])
                self.next_action.append("move_"+next_move)
        else:
            self.next_action.append("move_random")


        return 


    def do(self):
        """Execute the decided action."""
        return self.next_action[-1]
        
    def step(self):
        """Execute the agent's step."""
        
        self.deliberate()
        action = self.do()
        percepts = self.model.do(self, action)
        self.perceive(percepts)
