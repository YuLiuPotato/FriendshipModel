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
        filtered_names_ = df.loc[df['AgentID'] == 30]
        bias = filtered_names_['bias']
        threshold = filtered_names_['threshold']
        make_friend = filtered_names_['make_friend']
        social = filtered_names_['social']
        step = filtered_names_['Step']
        fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(10, 8))

        axes[0, 0].plot(step,threshold)
        axes[0, 0].set_title("threshold")

        axes[0, 1].plot(step, social)
        axes[0, 1].set_title("social")

        axes[1, 0].plot(step, make_friend)
        axes[1, 0].set_title("make_friend")

        axes[1, 1].plot(step, bias)
        axes[1, 1].set_title("bias")

        plt.show()
a =Analyzer()
a.Plot('/Users/michael/Documents/ETh/Sem2/fpga for quantum engineering/FriendshipModel/result_agent_model.csv')