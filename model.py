#model.py

from itertools import product

import mesa

from agents import greenAgent, redAgent, yellowAgent
from objects import RadioactivityAgent, Waste, WasteDisposalZone
from utils import next_waste_color


class MyModel(mesa.Model):
    """A model with some number of agents."""

    def __init__(self, n_green_agents=3, n_yellow_agents=0, n_red_agents=0, n_green_waste=10, n_yellow_waste=10, n_red_waste=10, width=10, height=10, seed=None):
        """Initialize a MoneyModel instance.

        Args:
            N: The number of agents.
            width: width of the grid.
            height: Height of the grid.
        """
        # SolaraViz envoie un dict pour n → on le transforme
        if isinstance(n_green_agents, dict):
            n_green_agents = n_green_agents.get("value", 10)
        if isinstance(n_yellow_agents, dict):
            n_yellow_agents = n_yellow_agents.get("value", 10)
        if isinstance(n_red_agents, dict):
            n_red_agents = n_red_agents.get("value", 10)

        if isinstance(n_green_waste, dict):
            n_green_waste = n_green_waste.get("value", 10)
        if isinstance(n_yellow_waste, dict):
            n_yellow_waste = n_yellow_waste.get("value", 10)
        if isinstance(n_red_waste, dict):
            n_red_waste = n_red_waste.get("value", 10)

        super().__init__(seed=seed)
        self.num_green_agents = n_green_agents
        self.num_yellow_agents = n_yellow_agents
        self.num_red_agents = n_red_agents
        self.grid = mesa.space.MultiGrid(width, height, torus=False)
        self.percepts = None

        # Create agents
        green_agents = greenAgent.create_agents(model=self, n=n_green_agents)
        yellow_agents = yellowAgent.create_agents(model=self, n=n_yellow_agents)
        red_agents = redAgent.create_agents(model=self, n=n_red_agents)

        # Create objects
        green_waste = Waste.create_agents(model=self, n=n_green_waste, color = "green")
        yellow_waste = Waste.create_agents(model=self,n=n_yellow_waste, color = "yellow")
        red_waste = Waste.create_agents(model=self, n=n_red_waste, color = "red")

        z1 = RadioactivityAgent.create_agents(model=self, n=width//3 * height, zone = "z1")
        z2 = RadioactivityAgent.create_agents(model=self, n=width//3 * height, zone = "z2")
        z3 = RadioactivityAgent.create_agents(model=self, n=width//3 * height, zone = "z3")

        waste_disposal_zone = WasteDisposalZone.create_agents(model=self, n=1, zone = "z3")

        # Create x and y positions for green agents
        x = self.rng.integers(0, self.grid.width//3, size=(n_green_agents,))
        y = self.rng.integers(0, self.grid.height, size=(n_green_agents,))
        for a, i, j in zip(green_agents, x, y):
            # Add the agent to a random grid cell
            self.grid.place_agent(a, (i, j))

        # Create x and y positions for yellow agents
        x = self.rng.integers(0, 2*self.grid.width//3, size=(n_yellow_agents,))
        y = self.rng.integers(0, self.grid.height, size=(n_yellow_agents,))
        for a, i, j in zip(yellow_agents, x, y):
            # Add the agent to a random grid cell
            self.grid.place_agent(a, (i, j))

        # Create x and y positions for red agents
        x = self.rng.integers(0, self.grid.width, size=(n_red_agents,))
        y = self.rng.integers(0, self.grid.height, size=(n_red_agents,))
        for a, i, j in zip(red_agents, x, y):
            # Add the agent to a random grid cell
            self.grid.place_agent(a, (i, j))


        # Positionner la disposal zone
        self.grid.place_agent(waste_disposal_zone[0], (width-1,height//2))


        # Positionner les déchets
        x_z1 = self.rng.integers(0, width//3, size=(n_green_waste,))
        x_z2 = self.rng.integers(width//3, 2*width//3, size=(n_yellow_waste,))
        x_z3 = self.rng.integers(2*width//3, width, size=(n_red_waste,))
        y = self.rng.integers(0, height, size=(n_green_waste+n_yellow_waste+n_red_waste,))

        for a, i, j in zip(green_waste, x_z1, y):
            self.grid.place_agent(a, (i, j))

        for a, i, j in zip(yellow_waste, x_z2, y):
            self.grid.place_agent(a, (i, j))

        for a, i, j in zip(red_waste, x_z3, y):
            self.grid.place_agent(a, (i, j))



        # Positioner les zones (green: toutes les lignes entre 0 et height//3, yellow: entre height//3 et 2*height//3, red: entre 2*height//3 et height)
        # Je ne veux pas de random, ces cases sont fixées
        # Zone z1 (verte)
        z1_coords = list(product(range(0, width // 3), range(height)))
        for a, (i, j) in zip(z1, z1_coords):
            self.grid.place_agent(a, (i, j))

        # Zone z2 (jaune)
        z2_coords = list(product(range(width // 3, 2 * width // 3), range(height)))
        for a, (i, j) in zip(z2, z2_coords):
            self.grid.place_agent(a, (i, j))

        # Zone z3 (rouge)
        z3_coords = list(product(range(2 * width // 3, width), range(height)))
        for a, (i, j) in zip(z3, z3_coords):
            self.grid.place_agent(a, (i, j))


            
    def do(self, agent, action):
        percepts = {}

        # Positions que l'agent croit possible
        possible_steps = agent.knowledge.get("possible_steps", [])

        # Positions occupées par d'autres agents mobiles
        mobile_agent_types = (greenAgent, yellowAgent, redAgent)
        occupied_positions = {other_agent.pos for other_agent in self.agents 
        if isinstance(other_agent, mobile_agent_types) and other_agent!= agent}

        # Supprimer les positions occupées par d'autres agents mobiles
        possible_steps = [pos for pos in possible_steps if pos not in occupied_positions]

        if action == "move_random" and possible_steps:
            self.grid.move_agent_to_one_of(agent, possible_steps)
            percepts = self.grid.get_neighbors(agent.pos, moore=False, include_center=True)
                
        elif action == "drop":
            waste = agent.get_waste(agent.pos)[0]  # find is there is already a waste in the cell
            if waste is None:
                # if its free move the waste held by the agent to this place
                if isinstance(agent, greenAgent):
                    coord = agent.pos
                    self.grid.place_agent(agent.has_waste, coord)
                    agent.has_waste = None # the agent has no waste anymore
                    agent.hold[1] = 0
                elif isinstance(agent, yellowAgent):
                    coord = agent.pos
                    self.grid.place_agent(agent.has_waste, coord)
                    agent.has_waste = None
                    agent.hold[2] = 0
                elif isinstance(agent, redAgent):
                    coord = agent.pos
                    self.grid.place_agent(agent.has_waste, coord)
                    waste_to_remove = agent.has_waste
                    self.grid.remove_agent(waste_to_remove)
                    #waste.remove()
                    agent.has_waste = None
                    agent.hold[2] = 0

                
        elif action == 'merge':
            # no risk of being unable to do the merge action
            if agent.get_waste(agent.pos)[0] is not None:
                waste = agent.get_waste(agent.pos)[0]
                # the agent merge the waste with the existing held, means he creates a new waste agent
                new_waste_color = next_waste_color(waste.color)
                # new_waste = Waste(self, new_waste_color)
                new_waste = Waste.create_agents(model=self,n=1, color = new_waste_color)[0] # bien prendre le premier élément car renvoie une liste d'agents
                
                old_waste = agent.has_waste         
                
                old_waste.remove()
                agent.has_waste = new_waste

                if isinstance(agent, greenAgent):
                    agent.hold = [0,1,0]
                elif isinstance(agent, yellowAgent):
                    agent.hold = [0,0,1]
            
                # code for removing the waste from the grid
                self.grid.remove_agent(waste)
                waste.remove()


        elif action == 'pick':
            # no risk of being unable to do the pick action
            if agent.get_waste(agent.pos)[0] is not None:
                waste = agent.get_waste(agent.pos)[0]
                
                # code for removing the waste from the grid
                self.grid.remove_agent(waste)          
                # the agent take the waste 
                agent.has_waste = waste

                if isinstance(agent, greenAgent):
                    agent.hold = [1, 0, 0]
                elif isinstance(agent, yellowAgent):
                    agent.hold = [0, 1, 0]
                elif isinstance(agent, redAgent):
                    agent.hold = [0, 0, 1]
                
        #percepts = self.grid.get_neighbors(agent.pos, moore=False, include_center=True)
        
        elif action == "move_toward" and possible_steps:
            # Stratégie pour l'agent vert
            if isinstance(agent, greenAgent):
                moved = False

                # Priorité : aller à droite

                for pos in possible_steps:
                    radio = 0
                    for agent_radio in self.grid.get_cell_list_contents(pos):
                        if isinstance(agent_radio,RadioactivityAgent):
                            radio = agent_radio.radioactivity
                    if pos[0] == agent.pos[0] + 1 and radio < 0.33:
                        self.grid.move_agent(agent, pos)
                        moved = True
                        break

                # Sinon : aller en haut ou en bas
                if not moved:
                    for pos in possible_steps:
                        if pos[1] in (agent.pos[1] + 1, agent.pos[1] - 1):
                            self.grid.move_agent(agent, pos)
                            moved = True
                            break

                # Sinon : déplacement aléatoire
                if not moved:
                    self.grid.move_agent_to_one_of(agent, possible_steps)

        percepts = self.grid.get_neighbors(agent.pos, moore=False, include_center=True)
        
        return percepts
        



    def step(self):
        """One step of the model: ask each agent what they want to do, and execute it."""
        self.agents.shuffle_do("step")





