import mesa
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from itertools import islice
from statistics import mean
from enum import Enum

class Mode(Enum):
    def __init__(self):
        self.TIME = 0

class Analyzer():
    def __init__(self):
        self.Mode = Mode

    def Plot(self,csv_file):
        df = pd.read_csv(csv_file)
        filtered_names_ = df.loc[df['AgentID'] == 12]
        bias = filtered_names_['bias']
        threshold = filtered_names_['threshold']
        make_friend = filtered_names_['make_friend']
        social = filtered_names_['social']
        step = filtered_names_['Step']
        utility_not_social = filtered_names_['utility_not_social']
        utility_social = filtered_names_['utility_social']
        friend_people = []
        for i in filtered_names_['friendship_people']:
            i = i.strip('[]').split(', ')

            friend_people.append(len(i))
        print(friend_people)
        friend_value = []
        for i in filtered_names_['friendship_value']:
            if(i=="[]"):
                friend_value.append(0)
            else:
                i = i.strip('[]').split(', ')
                list = [float(k) for k in i]

                friend_value.append(mean(list))
        fig, axes = plt.subplots(nrows=4, ncols=2, figsize=(10, 8))

        axes[0, 0].plot(step,threshold)
        axes[0, 0].set_title("threshold")

        axes[0, 1].plot(step, social)
        axes[0, 1].set_title("social")

        axes[1, 0].plot(step, make_friend)
        axes[1, 0].set_title("make_friend")

        axes[1, 1].plot(step, bias)
        axes[1, 1].set_title("bias")

        axes[2, 0].plot(step, friend_people)
        axes[2, 0].set_title("friend_people")

        axes[2, 1].plot(step, friend_value)
        axes[2, 1].set_title("friend_value")

        axes[3, 0].plot(step, utility_not_social)
        axes[3, 0].set_title("utility_not_social")

        axes[3, 1].plot(step, utility_social)
        axes[3, 1].set_title("utility_social")
        plt.tight_layout()
        plt.show()
a =Analyzer()
a.Plot('/Users/michael/Documents/ETh/Sem2/fpga for quantum engineering/FriendshipModel/result_agent_model.csv')