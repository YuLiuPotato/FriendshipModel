import mesa
from threading import Thread
import peoplemodel_zz,peoplemodel_random


def agent_portrayal(agent):
    portrayal = {
        "Shape": "circle",
        "Filled": "true",
        "Layer": 0,
        "Color": "red",
        "r": 0.5,
    }
    if agent.utility_social > agent.utility_not_social :
    #if agent.make_friend ==1:
        portrayal["Color"] = "red"
        portrayal["Layer"] = 0
    else:
        portrayal["Color"] = "grey"
        portrayal["Layer"] = 1

    if(agent.social>1):
        portrayal["r"] = 1
    elif(agent.social>0.05):
        portrayal["r"] = agent.social
    else:
        portrayal["r"] = 0.05
    #portrayal['text'] = agent.unique_id
    return portrayal


grid = mesa.visualization.CanvasGrid(agent_portrayal, 30, 30, 500, 500)
chart = mesa.visualization.ChartModule([{"Label": "average_social",
                      "Color": "Black"}],
                    data_collector_name='datacollector')
chart_1 = mesa.visualization.ChartModule([{"Label": "count_make_friend",
                      "Color": "Black"}],
                    data_collector_name='datacollector')
server = mesa.visualization.ModularServer(
    peoplemodel_random.PeopleModel, [grid,chart,chart_1], "Money Model", {"N": 200, "width": 30, "height": 30}
)

def listen_to_dump(server):
    print(server.model.step_num)
    if(server.model.step_num%10==1):
        server.model.output_csv(path="/Users/michael/Documents/ETh/Sem2/fpga for quantum engineering/FriendshipModel/result.csv")



server.port = 8521  # The default
server.launch()
t = Thread(target=listen_to_dump, args=[server])
t.run()