import mesa
import random
import numpy as np
import pandas as pd
from itertools import islice
from statistics import mean
from enum import Enum


def take(n, iterable):
    """Return the first n items of the iterable as a list."""
    return list(islice(iterable, n))
def count_make_friend(model):  # counts how many agents chooses make friend strategy in a round
    make_friend_list = [i.make_friend for i in model.schedule.agents]
    make_friend_yes_counts = len([i for i in make_friend_list if i == 1])
    return make_friend_yes_counts


def average_social_utility(model):  # calculate the average utility of each agent in a round
    every_utility_list = [i.utility_social for i in model.schedule.agents]
    average_utility = mean(every_utility_list)
    return average_utility
def average_non_soc_utility(model):  # calculate the average utility of each agent in a round
    every_utility_list = [i.utility_not_social for i in model.schedule.agents]
    average_utility = mean(every_utility_list)
    return average_utility


def average_social(model):  # calculate the average social of each agent in a round
    every_social_list = [i.social for i in model.schedule.agents]
    average_social = mean(every_social_list)
    return average_social
def friendship(model):
    friendship_bet = [i.friendship for i in model.schedule.agents]
    return average_social
class Payoff_f():
    def __init__(self,_T=1.5,_R=1.1,_P=0.8,_S=0.5):
        self.init(_T, _R, _P, _S)
    # friendship_level affect payoff function
    def friend_change(self,value):
        self.T += value/2
        self.R += value/2
        self.P += value/4
        self.S -= value/4
    def init(self,T=1.5,R=1.1,P=0.8,S=0.5):
        self.T = T
        self.R = R
        self.P = P
        self.S = S
class Monte_Carlo():
    def __init__(self,seed =0):
        self._random = random
        #self._random.seed(seed)
    def __call__(self, x):
        if(self._random.random()>x):
            return 1
        else:
            return 0
# configurator the parameter inside the file
class configurator():
    def __init__(self):
        self.init()
    def init(self):
        self.social_initial =0.2 # initial value of social
        self.payoff = Payoff_f() #initial payoff function
        self.level_of_hurt =4 # utilization boundary for bahavior change
        self.unhappy_move_barrier = 0.05
        self.happy_move_barrier = 0.8
        self.makefriend_hurt = 0.05
        self.alone_hurt = 0.03
class PeopleAgent(mesa.Agent):
    """An agent with fixed initial wealth."""

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.social = 0.2  # scoial preference s, the initial value is 0.5 or 50% probability of being social or non-social
        self.make_friend = 1 # the actural behavior [0,1] isolated vs outgoing
        self.utility_social = 0 #
        self.utility_not_social = 0 #
        self.bias =0 # bad mood / good mod affect his utilization
        self.threshold_of_hurt =4
        self.payoff_f = Payoff_f()
        self.friendship = {} # this is the friends list
        self.potential_friendship ={}
        self.monte_carlo = Monte_Carlo()

        '''
        T = 1.5 # temptation
        R = 1.1  # reward
        P = 0.8  # punishment
        S = 0.5  # sucker's payoff, the above four values are subject to change
        '''
    def init_property(self,social=0.5,make_friend=1,utility_social=0,utility_not_social=0,friendship ={}):
        self.social = social  # scoial preference s, the initial value is 0.5 or 50% probability of being social or non-social
        self.make_friend = make_friend # the actural behavior [0,1] isolated vs outgoing
        self.utility_social = utility_social #
        self.utility_not_social = utility_not_social #
        self.friendship = friendship


    # currently assuming agents do not move - however, the move of some agents with mutation of their "s" can be seen as dying out of those agents and the reproduction of the new ones; consider in the later stage
    # def move(self):
    #     possible_steps = self.model.grid.get_neighborhood(
    #         self.pos, moore=True, include_center=False
    #     )
    #     new_position = self.random.choice(possible_steps)
    #     self.model.grid.move_agent(self, new_position)

    def payoff(self):
        def no_cellmates(self):
            self.utility_not_social = 0
            self.utility_social =1
            self.make_friend =1
            return
        #compatability with multiGrid
        try:
            cellmates = self.model.grid.get_neighbors(self.pos,moore=True,include_center=False)
        except TypeError:
            cellmates = None
            no_cellmates(self)
            return
        finally:
            if(cellmates==None):
                no_cellmates(self)
                return
        _utility_not_social =0
        _utility_social =0
        for i in cellmates:
            #social_preference_to_i = np.random.choice((social,nonsocial),(self.wealth,1-self.wealth))
            #doesn't work
            #change friendship
            if(self.friendship.get(str(i.unique_id)) is not None):
                self.payoff_f.friend_change(self.friendship.get(str(i.unique_id)))

            if(i.make_friend ==1):
                _utility_not_social += (1-self.social)*self.payoff_f.T + self.social * self.payoff_f.S
                _utility_social_single = (1-self.social)*self.payoff_f.R + self.social * self.payoff_f.R
                _utility_social +=  _utility_social_single
                self.potential_friendship[str(i.unique_id)] =  _utility_social_single
            else:
                _utility_not_social += (1 - self.social) * self.payoff_f.P + self.social * self.payoff_f.P
                _utility_social += (1 - self.social) * self.payoff_f.S + self.social * self.payoff_f.T

        self.utility_social = _utility_social
        self.utility_not_social = _utility_not_social
        # update the behavior
        if(self.utility_social>self.utility_not_social):
            self.make_friend = 1
        elif (self.utility_social<self.utility_not_social):
            self.make_friend = 0
        else:
            self.make_friend = random.randint(0, 1)

    # take the 10 best friendship in list
    def update_friendship(self):
        friendship_temp = dict(sorted(self.potential_friendship.items(), key=lambda item: item[1],reverse=True))
        self.friendship = dict(take(10,friendship_temp.items()))

    def step(self):
        self.payoff() # update the behavior
        #print(min(self.utility_social, self.utility_not_social))
        if(min(self.utility_social,self.utility_not_social)<4):
            if self.monte_carlo(0.05):
                self.move()
            self.change_social("Hurt")
        else:
            if self.monte_carlo(0.8):
                self.move()
            if(self.make_friend ==1):
                self.update_friendship()
    ## move the agent to random place
    def move(self):
        possible_space = self.model.grid.get_neighborhood(self.pos,moore=True,include_center=False)
        empty = [i for i in possible_space if self.model.grid.is_cell_empty(i)]
        if isinstance(self.model.grid, mesa.space.SingleGrid):
            if len(empty) != 0:
                new_position = self.random.choice(empty)
                self.model.grid.move_agent(self, new_position)
            else:
                # if one fail to move, he become unfriendly/ he accumulate bias
                self.social-=0.02
        elif isinstance(self.model.grid, mesa.space.MultiGrid):
            new_position = self.random.choice(possible_space)
            self.model.grid.move_agent(self, new_position)

        # try if it is not empty for singleGrid
        '''
        while not self.model.grid.is_cell_empty(new_position) and isinstance(self.model.grid, mesa.space.SingleGrid):
            new_position = self.random.choice(possible_space)
            print(new_position)
        '''


    ##TODO: what happen if he is unhappy
    def change_social(self,mode):
        if(mode =="No_change"):
            return
        elif(mode =="Random"):
            self.social = random.random()
        # people got negative reward
        elif(mode =="Hurt"):
            if(self.make_friend >0.5):
                self.social -= 0.05
            else:
                self.social +=0.03
class PeopleModel(mesa.Model):

    def __init__(self,N,width,height):
        self.num_agents = N
        #self.grid = mesa.space.SingleGrid(width,height,True)
        self.grid = mesa.space.MultiGrid(width, height, True)
        self.schedule = mesa.time.RandomActivation(self)
        self.init_agent()
        self.step_num = 0
        self.datacollector = mesa.DataCollector(
            model_reporters={"average_social_utility": average_social_utility, "average_non_soc_utility":average_non_soc_utility,
                             "average_social": average_social,"count_make_friend": count_make_friend},
            agent_reporters={"utility_not_social": "utility_not_social","utility_social": "utility_social" ,
                             "social": "social", "make_friend": "make_friend"},
            tables = {"friend_net":["unique_id","friendship"]}
        )
    def init_agent(self):
        for i in range(self.num_agents):
            a = PeopleAgent(i,self)
            self.schedule.add(a)
            self.grid.place_agent(a, self.grid.find_empty()) # find a empty cell
    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)
        self.step_num+=1
        if(self.step_num %10 ==1):
            self.output_csv("/Users/michael/Documents/ETh/Sem2/fpga for quantum engineering/FriendshipModel/result.csv")
    def output_csv(self,path):
        result = self.datacollector.get_model_vars_dataframe()
        result.to_csv(path)
