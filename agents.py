
from communication.agent.CommunicatingAgent import CommunicatingAgent
from communication.message.Message import Message
from objects import RadioactivityAgent, Waste, WasteDisposalZone
from utils import choose_move_to_target, map_waste_color


class CleaningAgent(CommunicatingAgent):
    def __init__(self, model, name=None):
        agent_name = name or f"agent-{id(self)}"
        super().__init__(model, name=agent_name)
        self.has_waste = None
        self.hold = [0, 0, 0]
        self.knowledge = {
            "grid_size": (self.model.grid.width, self.model.grid.height),
            "position": self.pos,
            "possible_steps": [],
            "neighbor_waste_disposal_zone": [],
            "neighbor_radioactivity_agent": [],
            "neighbor_waste": [],
            "neighbor_robot": [],
            "neighbors": []
        }
        self.next_action = []
        self.agent_color = None
        self.target = None

    def get_radioactivity(self, position) -> float:
        (x, y) = position
        for agent in self.knowledge["neighbor_radioactivity_agent"]:
            if agent.pos == (x, y):
                return agent.radioactivity
        return -1

    def get_waste(self, position) -> list:
        (x, y) = position
        for agent in self.knowledge["neighbor_waste"]:
            if agent.pos == (x, y):
                return [agent, map_waste_color(agent.color)]
        return [None, [0, 0, 0]]

    def perceive(self, percepts):
        self.knowledge["neighbors"] = percepts
        self.knowledge["possible_steps"] = []
        self.knowledge["neighbor_waste_disposal_zone"] = []
        self.knowledge["neighbor_radioactivity_agent"] = []
        self.knowledge["neighbor_waste"] = []
        self.knowledge["neighbor_robot"] = []

        for agent in percepts:
            if isinstance(agent, WasteDisposalZone):
                self.knowledge["neighbor_waste_disposal_zone"].append(agent)
            elif isinstance(agent, RadioactivityAgent):
                self.knowledge["neighbor_radioactivity_agent"].append(agent)
            elif isinstance(agent, Waste):
                self.knowledge["neighbor_waste"].append(agent)
            elif isinstance(agent, CleaningAgent):
                self.knowledge["neighbor_robot"].append(agent)

    def do(self):
        return self.next_action[-1]

    #def step(self):
    #    print(f"STEP START — {self.get_name()}")
    #    super().step()
    #   self.deliberate()
    #    action = self.do()
    #    percepts = self.model.do(self, action)
    #    self.perceive(percepts)
    #    print(f"STEP END — {self.get_name()}")
    def step_messages_only(self):
        super().step()  # permet à CommunicatingAgent de traiter les messages

    def step_logic_only(self):
        self.deliberate()
        action = self.do()
        percepts = self.model.do(self, action)
        self.perceive(percepts)


class greenAgent(CleaningAgent):
    def __init__(self, model):
        super().__init__(model, name=f"green-{id(self)}")
        self.agent_color = "green"

    def deliberate(self):
        x, y = self.pos
        right_cell = (x + 1, y)

        # Si l'agent est sur la frontière, qu'il porte un déchet jaune et qu'il n'y a pas de déchet déjà sur la case...
        if self.get_radioactivity(right_cell) >= 0.33 and self.hold == [0, 1, 0] and self.get_waste(self.pos)[0] is None:
            # ... il drop et envoie un message à l'agent jaune
            self.next_action.append("drop")
            for other_agent in self.model.agents:
                if isinstance(other_agent, yellowAgent) and other_agent != self:
                    msg = Message(
                        from_agent=self.get_name(),
                        to_agent=other_agent.get_name(),
                        message_performative=107,
                        content={"type": "drop", "position": self.pos}
                    )
                    self.send_message(msg)

            return

        # Si l'agent est sur une case de déchet vert et qu'il n'a pas de déchet jaune...
        if self.get_waste(self.pos)[1] == [1, 0, 0] and self.hold != [0, 1, 0]:
            # ...il merge s'il a déjà un déchet vert et pick s'il n'a rien
            self.next_action.append("merge" if self.hold == [1, 0, 0] else "pick")
            return
       
        # Un agent mobile ne peut pas se déplacer sur une case occupée par un autre agent mobile
        # Un agent vert doit rester dans une case avec une radioactivité inférieure à 0.33
        impossible_steps = [
            agent.pos for agent in self.knowledge["neighbor_robot"]
        ] + [
            agent.pos for agent in self.knowledge["neighbor_radioactivity_agent"]
            if agent.radioactivity >= 0.33
        ]

        self.knowledge["possible_steps"] = [
            p for p in self.model.grid.get_neighborhood(self.pos, moore=False)
            if p not in impossible_steps
        ]

        # Si l'agent vert a un déchet jaune, il doit se déplacer vers la frontière
        if self.hold == [0, 1, 0]:
            if self.get_radioactivity(right_cell) >= 0.33 and self.get_waste(self.pos)[0] is not None:
                if (x,y+1) in self.knowledge["possible_steps"]:
                    self.next_action.append("move_up")
                    return
                elif (x,y-1) in self.knowledge["possible_steps"]:
                    self.next_action.append("move_down")
                    return
            self.next_action.append("move_right")
            return

        # Action par défault : se déplacer en random      
        self.next_action.append("move_random")


class yellowAgent(CleaningAgent):
    def __init__(self, model):
        super().__init__(model, name=f"yellow-{id(self)}")
        self.agent_color = "yellow"

    def deliberate(self):
        x, y = self.pos
        if self.target == self.pos:
            self.target = None

        for message in self.get_new_messages():
            if message.get_performative() == 107:
                content = message.get_content()
                if content.get("type") == "drop" and self.target is None:
                    self.target = content.get("position")
        
        
        right_cell = (x + 1, y)
        if self.get_radioactivity(right_cell) >= 0.66 and self.hold == [0, 0, 1] and self.get_waste(self.pos)[0] is None:
            self.next_action.append("drop")
            for other_agent in self.model.agents:
                if isinstance(other_agent, redAgent) and other_agent != self:
                    msg = Message(
                        from_agent=self.get_name(),
                        to_agent=other_agent.get_name(),
                        message_performative=107,
                        content={"type": "drop", "position": self.pos}
                    )
                    self.send_message(msg)
            return

        if self.get_waste(self.pos)[1] == [0, 1, 0] and self.hold != [0, 0, 1]:
            self.next_action.append("merge" if self.hold == [0, 1, 0] else "pick")
            return

        impossible_steps = [
            agent.pos for agent in self.knowledge["neighbor_robot"]
        ] + [
            agent.pos for agent in self.knowledge["neighbor_radioactivity_agent"]
            if agent.radioactivity >= 0.66
        ]

        self.knowledge["possible_steps"] = [
            p for p in self.model.grid.get_neighborhood(self.pos, moore=False)
            if p not in impossible_steps
        ]

        if self.target and self.hold != [0, 0, 1] :
            move = choose_move_to_target(self.target, self.pos, self.knowledge["possible_steps"])
            self.next_action.append(f"move_{move}")         
            return
        
        
        # Si l'agent jaune a un déchet rouge, il doit se déplacer vers la frontière
        if self.hold == [0, 0, 1]:
            if self.get_radioactivity(right_cell) >= 0.66 and self.get_waste(self.pos)[0] is not None:
                if (x,y+1) in self.knowledge["possible_steps"]:
                    self.next_action.append("move_up")
                    return
                elif (x,y-1) in self.knowledge["possible_steps"]:
                    self.next_action.append("move_down")
                    return
            self.next_action.append("move_right")
            return
        
        self.next_action.append("move_random")


class redAgent(CleaningAgent):
    def __init__(self, model):
        super().__init__(model, name=f"red-{id(self)}")
        self.agent_color = "red"

    def deliberate(self):
        x, y = self.pos
        if self.target == self.pos:
            self.target = None

        if self.get_radioactivity((x, y)) == -1 and self.hold == [0, 0, 1]:
            self.next_action.append("drop")
            return

        if self.get_waste(self.pos)[1] == [0, 0, 1] and self.hold == [0, 0, 0]:
            self.next_action.append("pick")
            return

        for message in self.get_new_messages():
            if message.get_performative() == 107:
                content = message.get_content()
                if content.get("type") == "drop" and self.target is None:
                    self.target = content.get("position")
        print(f"yellow message: {self.get_new_messages()}")

        impossible_steps = [agent.pos for agent in self.knowledge["neighbor_robot"]]

        self.knowledge["possible_steps"] = [
            p for p in self.model.grid.get_neighborhood(self.pos, moore=False)
            if p not in impossible_steps
        ]

        print(f"yellow target: {self.target}")
        if self.target and self.hold != [0, 0, 1]:
            move = choose_move_to_target(self.target, self.pos, self.knowledge["possible_steps"])
            self.next_action.append(f"move_{move}")
            print(f"red move: {move}")
            return
        
        # Si l'agent rouge a un déchet rouge, il doit se déplacer vers la frontière
        if self.hold == [0, 0, 1]:
            if self.get_radioactivity(self.pos) == -1 and self.get_waste(self.pos)[0] is not None:
                if (x,y+1) in self.knowledge["possible_steps"]:
                    self.next_action.append("move_up")
                    return
                elif (x,y-1) in self.knowledge["possible_steps"]:
                    self.next_action.append("move_down")
                    return
            self.next_action.append("move_right")
            return
        
        self.next_action.append("move_random")