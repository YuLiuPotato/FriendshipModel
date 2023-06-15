import mesa
from peoplemodel_random import *
def agent_portrayal(agent):
    portrayal = {
        "Shape": "circle",
        "Filled": "true",
        "Layer": 0,
        "Color": "red",
        "r": 0.5,
    }
    if agent.utility_social > agent.utility_not_social :
        portrayal["Color"] = "red"
        portrayal["Layer"] = 0
    else:
        portrayal["Color"] = "grey"
        portrayal["Layer"] = 1
    if(agent.social>0.01):
        portrayal["r"] = agent.social
    else:
        portrayal["r"] = 0.01
    #portrayal['text'] = agent.unique_id
    return portrayal


grid = mesa.visualization.CanvasGrid(agent_portrayal, 30, 30, 500, 500)
server = mesa.visualization.ModularServer(
    PeopleModel, [grid], "Money Model", {"N": 200, "width": 30, "height": 30}
)
server.port = 8521  # The default
server.launch()