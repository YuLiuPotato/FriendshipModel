import mesa
import random
import numpy as np

class Payoff_f():
    def __init__(self,T=1.5,R=1.1,P=0.8,S=0.5):
        self.T = T
        self.R = R
        self.P = P
        self.S = S

class PeopleAgent(mesa.Agent):
    """An agent with fixed initial wealth."""

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.social = 0.5  # scoial preference s, the initial value is 0.5 or 50% probability of being social or non-social
        self.make_friend = 1 # the actural behavior [0,1] isolated vs outgoing
        self.utility_social = 0 #
        self.utility_not_social = 0 #
        self.payoff_f = Payoff_f()
        '''
        T = 1.5 # temptation
        R = 1.1  # reward
        P = 0.8  # punishment
        S = 0.5  # sucker's payoff, the above four values are subject to change

        '''
    def init_property(self,social=0.5,make_friend=1,utility_social=0,utility_not_social=0):
        self.social = social  # scoial preference s, the initial value is 0.5 or 50% probability of being social or non-social
        self.make_friend = make_friend # the actural behavior [0,1] isolated vs outgoing
        self.utility_social = utility_social #
        self.utility_not_social = utility_not_social #

    # currently assuming agents do not move - however, the move of some agents with mutation of their "s" can be seen as dying out of those agents and the reproduction of the new ones; consider in the later stage
    # def move(self):
    #     possible_steps = self.model.grid.get_neighborhood(
    #         self.pos, moore=True, include_center=False
    #     )
    #     new_position = self.random.choice(possible_steps)
    #     self.model.grid.move_agent(self, new_position)

    def payoff(self):
        cellmates = self.model.grid.get_neighbors(self.pos,moore=True)
        if cellmates == None:
            self.utility_not_social = 0
            self.utility_social =1
            self.make_friend =1
            return
        _utility_not_social =0
        _utility_social =0
        for i in cellmates:
            #social_preference_to_i = np.random.choice((social,nonsocial),(self.wealth,1-self.wealth))
            #doesn't work
            if(i.make_friend ==1):
                _utility_not_social += (1-self.social)*self.payoff_f.T + self.social * self.payoff_f.S
                _utility_social += (1-self.social)*self.payoff_f.R + self.social * self.payoff_f.R
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


    def step(self):
        self.payoff() # update the behavior
        #print(min(self.utility_social, self.utility_not_social))
        if(min(self.utility_social,self.utility_not_social)<4):
            self.move()
        self.change_social()
    ## move the agent to random place
    def move(self):
        possible_space = self.model.grid.get_neighborhood(self.pos,moore=True,include_center=False)
        new_position = self.random.choice(possible_space)
        self.model.grid.move_agent(self,new_position)
    ##TODO: what happen if he is unhappy
    def change_social(self):
        return
class PeopleModel(mesa.Model):

    def __init__(self,N,width,height):
        self.num_agents = N
        self.grid = mesa.space.MultiGrid(width,height,True)
        self.schedule = mesa.time.RandomActivation(self)
        self.init_agent()
    def init_agent(self):
        for i in range(self.num_agents):
            a = PeopleAgent(i,self)
            self.schedule.add(a)

            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a,(x,y))
    def step(self):
        self.schedule.step()
