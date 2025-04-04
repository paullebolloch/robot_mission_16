import mesa
import solara
from mesa.visualization import make_space_component, make_plot_component, SolaraViz
from model import MyModel


model_params = {
    "n": {
        "type": "SliderInt",
        "value": 10,
        "label": "Number of agents:",
        "min": 10,
        "max": 100,
        "step": 1,
    },
    "width": 15,
    "height": 15,
}

def agent_portrayal(agent):
    # Valeurs par défaut (pour les agents mobiles)
    portrayal = {
        "color": "blue",
        "size": 50,         # taille standard pour agents (mobiles)
        "marker": "o",      # cercle
        "zorder": 2
    }

    if hasattr(agent, "radioactivity"):
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

    elif hasattr(agent, "color"):
        # Waste
        portrayal["color"] = agent.color
        portrayal["size"] = 30  # légèrement plus petit que les agents
        portrayal["marker"] = "o"
        portrayal["zorder"] = 3

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