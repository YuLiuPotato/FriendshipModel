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
def average_bias_utility(model):  # calculate the average utility of each agent in a round
    every_utility_list = [i.bias for i in model.schedule.agents]
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
        self.T += value/2*random.random()
        self.R += value/2*random.random()
        self.P += value/4*random.random()
        self.S -= value*5/4
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
class Configurator():
    def __init__(self):
        self.init()
    def init(self):
        self.social_initial =0.2 # initial value of social
        self.payoff = Payoff_f() #initial payoff function
        self.level_of_hurt =6 # utilization boundary for bahavior change
        self.unhappy_move_barrier = 0.05
        self.happy_move_barrier = 0.8
        self.makefriend_hurt = 0.05
        self.alone_hurt = 0.03
        self.thershold_hurt= 2
class PeopleAgent(mesa.Agent):
    """An agent with fixed initial wealth."""

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.social = 0.5*random.random()  # scoial preference s, the initial value is 0.5 or 50% probability of being social or non-social
        self.make_friend = random.randint(0,1) # the actural behavior [0,1] isolated vs outgoing
        self.utility_social = 0 #
        self.utility_not_social = 0 #
        self.bias =0 # bad mood / good mod affect his utilization
        self.threshold_of_hurt =4
        self.payoff_f = Payoff_f()
        self.friendship = {} # this is the friends list
        self.potential_friendship ={}
        self.internet_friends =[]
        self.monte_carlo = Monte_Carlo()
        self.configurator = Configurator()

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
        #to be modified. which is not true
        def no_cellmates(self):
            self.utility_not_social *= 0.9
            self.utility_social *=0.9
            if (self.utility_social > self.utility_not_social):
                if (self.monte_carlo(0.2)):
                    self.make_friend = 1
                else:
                    self.make_friend = 0
                self.make_friend = 1
            elif (self.utility_social < self.utility_not_social):
                if (self.monte_carlo(0.2)):
                    self.make_friend = 0
                else:
                    self.make_friend = 1
            else:
                self.make_friend = random.randint(0, 1)
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
        '''
        if(len(self.internet_friends)>0):
            for x in self.internet_friends:
                cellmates.append(x)
        print(f'cellmates length: {len(cellmates)}')
        '''

        for i in cellmates:
            #social_preference_to_i = np.random.choice((social,nonsocial),(self.wealth,1-self.wealth))
            #doesn't work
            #change friendship
            is_friend = False
            if(self.friendship.get(str(i.unique_id)) is not None):
                self.payoff_f.init()
                self.payoff_f.friend_change(self.friendship.get(str(i.unique_id)))
                is_friend =True

            if(i.make_friend ==1):
                _utility_not_social += (1-self.social)*self.payoff_f.T + self.social * self.payoff_f.S
                _utility_social_single = (1-self.social)*self.payoff_f.R + self.social * self.payoff_f.R
                _utility_social +=  _utility_social_single
                if(i.social>0.5 or self.monte_carlo(i.social) ):
                    self.potential_friendship[str(i.unique_id)] =  _utility_social_single
                    if(len(i.internet_friends) != 0):
                        i_friend = random.choice(i.internet_friends)
                        self.internet_friends.append(i_friend) # take friends' friend
                    self.internet_friends.append(i)
            else:
                _utility_not_social += (1 - self.social) * self.payoff_f.P + self.social * self.payoff_f.P
                _utility_social += (1 - self.social) * self.payoff_f.S + self.social * self.payoff_f.T
                if(is_friend and self.monte_carlo(0.2) or i.social<0):
                    self.potential_friendship[str(i.unique_id)] =  -1

        for i in self.internet_friends:
            is_friend=False
            friend_of_other = False
            if(self.friendship.get(str(i.unique_id)) is not None):
                self.payoff_f.init()
                self.payoff_f.friend_change(self.friendship.get(str(i.unique_id))/2) # 1/2 of change
                is_friend = True
            if(i.friendship.get(str(self.unique_id)) is not None):
                #self.payoff_f.init()
                self.payoff_f.friend_change(i.friendship.get(str(self.unique_id))/2) # 1/2 of change
                friend_of_other = True

            if(i.make_friend ==1):
                _utility_not_social += (1-self.social)*self.payoff_f.T + self.social * self.payoff_f.S
                _utility_social_single = (1-self.social)*self.payoff_f.R + self.social * self.payoff_f.R
                _utility_social +=  _utility_social_single
                #if(len(self.potential_friendship)<15):
                #    self.potential_friendship[str(i.unique_id)] =  _utility_social_single
            else:
                _utility_not_social += (1 - self.social) * self.payoff_f.P + self.social * self.payoff_f.P
                _utility_social += (1 - self.social) * self.payoff_f.S + self.social * self.payoff_f.T
                if(is_friend and self.monte_carlo(0.2) or i.social<0):
                    self.potential_friendship[str(i.unique_id)] =  -1
            if(is_friend and not friend_of_other):
                self.potential_friendship[str(i.unique_id)] -= 0.2
        self.utility_social = _utility_social +5*self.bias*random.random()
        self.utility_not_social = _utility_not_social -5*self.bias*random.random()
        # update the behavior
        if(self.utility_social>self.utility_not_social):
            if(self.monte_carlo(0.2)):
                self.make_friend = 1
            else:
                self.make_friend = 0
            self.make_friend = 1
        elif (self.utility_social<self.utility_not_social ):
            if(self.monte_carlo(0.2)):
                self.make_friend = 0
            else:
                self.make_friend = 1
        else:
            self.make_friend = random.randint(0, 1)

    # take the 10 best friendship in list
    def update_friendship(self):
        friendship_temp = dict(sorted(self.potential_friendship.items(), key=lambda item: item[1],reverse=True))
        self.friendship = dict([i for i in take(20,friendship_temp.items()) if i[1] >1])
        #self.friendship = {}
        list = []
        for i in self.internet_friends:
            id = str(i.unique_id)
            fri_u = friendship_temp.get(id)
            if(fri_u != None):
                if(friendship_temp.get(id) > 1.3):
                    list.append(i)
                if(len(list)>15):
                    break
        #list =[]
        self.internet_friends = list


    def step(self):
        self.payoff() # update the behavior
        bias_level = 5
        bias_memory = 0.7
        #print(min(self.utility_social, self.utility_not_social))
        max_uti = max(self.utility_social,self.utility_not_social)
        max_uti_diff = max_uti - self.threshold_of_hurt
        if(max_uti<self.threshold_of_hurt):
            if self.monte_carlo(0.05):
                self.move()
            self.change_social("Hurt")
            if(self.make_friend==1):
                self.bias =(bias_memory+0.1)*self.bias+ self.monte_carlo(0.2) *bias_level* max_uti_diff * 0.1 * (random.random() - 0.25)
            else:
                self.bias =(bias_memory+0.1)*self.bias -self.monte_carlo(0.2) *bias_level* max_uti_diff * 0.1 * (random.random() - 0.25)

        else:
            if self.monte_carlo(0.8):
                self.move()
            if(self.make_friend ==1):
                self.update_friendship()
                self.bias = (bias_memory)*self.bias+ self.monte_carlo(0.8)*bias_level*max_uti_diff*(random.random()-0.25)
            else:
                self.bias = (bias_memory)*self.bias- self.monte_carlo(0.8)*bias_level*max_uti_diff*(random.random()-0.25)
        self.threshold_of_hurt = 0.2*self.threshold_of_hurt+ max(self.utility_social,self.utility_not_social)
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
                #self.social-=0.02
                self.bias -= 0.05
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
                self.social -= 0.1
            else:
                self.social +=0.05
class PeopleModel(mesa.Model):

    def __init__(self,N,width,height):
        self.num_agents = N
        self.grid = mesa.space.SingleGrid(width,height,True)
        #self.grid = mesa.space.MultiGrid(width, height, True)
        self.schedule = mesa.time.RandomActivation(self)
        self.init_agent()
        self.step_num = 0
        self.datacollector = mesa.DataCollector(
            model_reporters={"average_social_utility": average_social_utility, "average_non_soc_utility":average_non_soc_utility,
                             "average_social": average_social,"count_make_friend": count_make_friend,"bias":average_bias_utility},
            agent_reporters={"utility_not_social": "utility_not_social","utility_social": "utility_social" ,
                             "social": lambda m:m.social, "make_friend": "make_friend","friendship_people":lambda m: [float(i) for i in m.friendship.keys()],"friendship_value":lambda m: [float(i) for i in m.friendship.values()],
                             "bias":"bias","threshold":"threshold_of_hurt" },

            tables = {"friend_net":["unique_id"]}
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
        self.output_csv(0, "/Users/michael/Documents/ETh/Sem2/fpga for quantum engineering/FriendshipModel/result_agent_model.csv")
        self.output_csv(1,"/Users/michael/Documents/ETh/Sem2/fpga for quantum engineering/FriendshipModel/result_model.csv")
        self.output_csv(2,"/Users/michael/Documents/ETh/Sem2/fpga for quantum engineering/FriendshipModel/result_table.csv")
    def output_csv(self,data,path):
        #result = self.datacollector.get_model_vars_dataframe()
        if(data==0):
            result = self.datacollector.get_agent_vars_dataframe()
        elif(data==1):
            result = self.datacollector.get_model_vars_dataframe()
        else:
            result = self.datacollector.get_table_dataframe("friend_net")
        result.to_csv(path)
