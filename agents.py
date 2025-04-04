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