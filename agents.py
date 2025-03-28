import mesa

class MyAgent(mesa.Agent):
    """An agent with fixed initial wealth."""

    def __init__(self, model):
        """initialize a MoneyAgent instance.

        Args:
            model: A model instance
        """
        super().__init__(model)

    def move(self):
        """move to a random neighboring cell."""
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False
        )
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)


    def step(self):
        """do one step of the agent."""
        self.move()

