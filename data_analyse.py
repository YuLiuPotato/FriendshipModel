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
        result = pd.read_csv(csv_file)
        plt.plot(result["unique_id"],result[""])