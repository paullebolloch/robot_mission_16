#model.py

import mesa
from objects import WasteDisposalZone, Waste, RadioactivityAgent
from agents import MyAgent
from itertools import product



class MyModel(mesa.Model):
    """A model with some number of agents."""

    def __init__(self, n=10, width=10, height=10, seed=None):
        """Initialize a MoneyModel instance.

        Args:
            N: The number of agents.
            width: width of the grid.
            height: Height of the grid.
        """
        # SolaraViz envoie un dict pour n → on le transforme
        if isinstance(n, dict):
            n = n.get("value", 50)

        super().__init__(seed=seed)
        self.num_agents = n
        self.grid = mesa.space.MultiGrid(width, height, torus=False)
        self.percepts = None

        # Create agents
        agents = MyAgent.create_agents(model=self, n=n)

        # Create objects
        green_waste = Waste.create_agents(model=self, n=n, color = "green")
        yellow_waste = Waste.create_agents(model=self,n=n, color = "yellow")
        red_waste = Waste.create_agents(model=self, n=n, color = "red")

        z1 = RadioactivityAgent.create_agents(model=self, n=width//3 * height, zone = "z1")
        z2 = RadioactivityAgent.create_agents(model=self, n=width//3 * height, zone = "z2")
        z3 = RadioactivityAgent.create_agents(model=self, n=width//3 * height, zone = "z3")

        waste_disposal_zone = WasteDisposalZone.create_agents(model=self, n=1, zone = "z3")

        # Create x and y positions for agents
        x = self.rng.integers(0, self.grid.width, size=(n,))
        y = self.rng.integers(0, self.grid.height, size=(n,))
        for a, i, j in zip(agents, x, y):
            # Add the agent to a random grid cell
            self.grid.place_agent(a, (i, j))


        # Positionner la disposal zone
        self.grid.place_agent(waste_disposal_zone[0], (width-1,height//2))


        # Positionner les déchets
        x_z1 = self.rng.integers(0, width//3, size=(n,))
        x_z2 = self.rng.integers(width//3, 2*width//3, size=(n,))
        x_z3 = self.rng.integers(2*width//3, width, size=(n,))
        y = self.rng.integers(0, height, size=(n,))

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

        if action == "move_random":
            possible_steps = agent.knowledge.get("possible_steps", [])
            if possible_steps:
                self.grid.move_agent_to_one_of(agent, possible_steps)
                percepts = self.grid.get_neighbors(agent.pos, moore=False, include_center=True)

        # Ajouter d'autres actions ici plus tard

        return percepts
        

    def step(self):
        """One step of the model: ask each agent what they want to do, and execute it."""
        self.agents.shuffle_do("step")





