import mesa
import solara
import pandas as pd
import matplotlib.pyplot as plt
from mesa.visualization import make_space_component, make_plot_component, SolaraViz
from model import MyModel
from objects import Waste, RadioactivityAgent, WasteDisposalZone
from agents import greenAgent, yellowAgent, redAgent
from mesa.datacollection import DataCollector
from mesa.visualization.utils import update_counter

def compute_gini(model):
    agent_wealths = [agent.pos for agent in model.agents]
    x = sorted(agent_wealths)
    n = model.num_agents
    B = sum(xi * (n - i) for i, xi in enumerate(x)) / (n * sum(x))
    return 1 + (1 / n) - 2 * B


model_params = {
    "n_green_agents": {
        "type": "SliderInt",
        "value": 1,
        "label": "Number of green agents:",
        "min": 0,
        "max": 20,
        "step": 1,
    },
    "n_yellow_agents": {
        "type": "SliderInt",
        "value": 1,
        "label": "Number of yellow agents:",
        "min": 0,
        "max": 20,
        "step": 1,
    },
    "n_red_agents": {
        "type": "SliderInt",
        "value": 1,
        "label": "Number of red agents:",
        "min": 0,
        "max": 20,
        "step": 1,
    },
    "n_green_waste": {
        "type": "SliderInt",
        "value": 16,
        "label": "Number of green waste:",
        "min": 0,
        "max": 20,
        "step": 1,
    },
    "n_yellow_waste": {
        "type": "SliderInt",
        "value": 0,
        "label": "Number of yellow waste:",
        "min": 0,
        "max": 20,
        "step": 1,
    },
    "n_red_waste": {
        "type": "SliderInt",
        "value": 0,
        "label": "Number of red waste:",
        "min": 0,
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
        "size": 200,         # taille standard pour agents (mobiles)
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
            portrayal["color"] = "honeydew"
            portrayal["size"] = 100
            portrayal["marker"] = "s"
            portrayal["zorder"] = 0
        elif agent.zone == "z2":
            portrayal["color"] = "lemonchiffon"
            portrayal["size"] = 100
            portrayal["marker"] = "s"
            portrayal["zorder"] = 0
        elif agent.zone == "z3":
            portrayal["color"] = "mistyrose"
            portrayal["size"] = 100
            portrayal["marker"] = "s"
            portrayal["zorder"] = 0

    elif isinstance(agent, Waste):
        # Waste
        if agent.color == "green":
            portrayal["color"] = "green"
        elif agent.color == "yellow":
            portrayal["color"] = "goldenrod"
        elif agent.color == "red":
            portrayal["color"] = "firebrick"
        portrayal["size"] = 30  # légèrement plus petit que les agents
        portrayal["marker"] = "^"
        portrayal["zorder"] = 3

    elif isinstance(agent, yellowAgent):
        portrayal["color"] = "gold"
    
    elif isinstance(agent, redAgent):
        portrayal["color"] = "orangered"

    return portrayal


@solara.component
def WastePlot(model):
    update_counter.get()
    if model is None:
        return

    df = model.datacollector.get_model_vars_dataframe()
    if df.empty:
        return solara.Text("Pas encore de données. Cliquez sur 'Step' ou 'Run' pour démarrer la simulation.")

    fig, ax = plt.subplots()
    if "Green Waste" in df.columns:
        ax.plot(df.index, df["Green Waste"], label="Green Waste", color="green")
    if "Yellow Waste" in df.columns:
        ax.plot(df.index, df["Yellow Waste"], label="Yellow Waste", color="gold")
    if "Red Waste" in df.columns:
        ax.plot(df.index, df["Red Waste"], label="Red Waste", color="red")

    ax.set_title("Évolution des types de déchets")
    ax.set_xlabel("Step")
    ax.set_ylabel("Nombre")
    ax.legend()

    solara.FigureMatplotlib(fig)


@solara.component
def Page():
    """
    This function is used to define the SolaraViz page.
    """
    money_model = MyModel(**model_params)

    SpaceGraph = make_space_component(agent_portrayal)

    page = SolaraViz(
        money_model,
        components=[SpaceGraph,
                    WastePlot],
        model_params=model_params,
        name="Robot Mission",
    )
    return page




#solara run server.py