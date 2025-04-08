import mesa
import solara
from mesa.visualization import make_space_component, make_plot_component, SolaraViz
from model import MyModel
from objects import Waste, RadioactivityAgent, WasteDisposalZone
from agents import greenAgent, yellowAgent, redAgent


model_params = {
    "n_green_agents": {
        "type": "SliderInt",
        "value": 10,
        "label": "Number of green agents:",
        "min": 1,
        "max": 20,
        "step": 1,
    },
    "n_yellow_agents": {
        "type": "SliderInt",
        "value": 10,
        "label": "Number of yellow agents:",
        "min": 1,
        "max": 20,
        "step": 1,
    },
    "n_red_agents": {
        "type": "SliderInt",
        "value": 10,
        "label": "Number of red agents:",
        "min": 1,
        "max": 20,
        "step": 1,
    },
    "n_green_waste": {
        "type": "SliderInt",
        "value": 10,
        "label": "Number of green waste:",
        "min": 1,
        "max": 20,
        "step": 1,
    },
    "n_yellow_waste": {
        "type": "SliderInt",
        "value": 10,
        "label": "Number of yellow waste:",
        "min": 1,
        "max": 20,
        "step": 1,
    },
    "n_red_waste": {
        "type": "SliderInt",
        "value": 10,
        "label": "Number of red waste:",
        "min": 1,
        "max": 20,
        "step": 1,
    },
    "width": 15,
    "height": 15,
}

def agent_portrayal(agent):
    # Valeurs par défaut (pour les agents mobiles)
    portrayal = {
        "color": "lightgreen",
        "size": 100,         # taille standard pour agents (mobiles)
        "marker": "o",      # cercle
        "zorder": 2
    }

    if isinstance(agent, RadioactivityAgent) or isinstance(agent, WasteDisposalZone):
        if agent.radioactivity == -1:
            # WasteDisposalZone
            portrayal["color"] = "black"
            portrayal["size"] = 100  # remplit la cellule
            portrayal["marker"] = "s"  # carré
            portrayal["zorder"] = 1
        elif agent.zone == "z1":
            portrayal["color"] = "mediumseagreen"
            portrayal["size"] = 100
            portrayal["marker"] = "s"
            portrayal["zorder"] = 0
        elif agent.zone == "z2":
            portrayal["color"] = "khaki"
            portrayal["size"] = 100
            portrayal["marker"] = "s"
            portrayal["zorder"] = 0
        elif agent.zone == "z3":
            portrayal["color"] = "lightcoral"
            portrayal["size"] = 100
            portrayal["marker"] = "s"
            portrayal["zorder"] = 0

    elif isinstance(agent, Waste):
        # Waste
        portrayal["color"] = agent.color
        portrayal["size"] = 30  # légèrement plus petit que les agents
        portrayal["marker"] = "o"
        portrayal["zorder"] = 3

    elif isinstance(agent, yellowAgent):
        portrayal["color"] = "gold"
    
    elif isinstance(agent, redAgent):
        portrayal["color"] = "red"

    return portrayal



@solara.component
def Page():
    """
    This function is used to define the SolaraViz page.
    """
    money_model = MyModel(**model_params)

    SpaceGraph = make_space_component(agent_portrayal)

    page = SolaraViz(
        money_model,
        components=[SpaceGraph],
        model_params=model_params,
        name="Robot Mission",
    )
    return page


#solara run server.py