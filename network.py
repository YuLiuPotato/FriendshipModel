import mesa
import random
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


class Payoff_f():
    def __init__(self, t=1.5, r=0.9, p=0.7,
                 s=0.5):  # s between (T-R)/(T-S) and (P-S)/(T-S) for conditional social choice of the agent
        self.t = t
        self.r = r
        self.p = p
        self.s = s

    # the payoff the agent i gets when i interacts with j, depending on the social decisions of the both
    def payoff_i_with_j(self, make_friend_i, make_friend_j):
        payoff_of_i = None
        if make_friend_i == 1 and make_friend_j == 1:
            payoff_of_i = self.r
        elif make_friend_i == 1 and make_friend_j == 0:
            payoff_of_i = self.s
        elif make_friend_i == 0 and make_friend_j == 1:
            payoff_of_i = self.t
        elif make_friend_i == 0 and make_friend_j == 0:
            payoff_of_i = self.p
        else:
            print("invalid social decision input")
        return payoff_of_i

    # utility function of i when i interacts with j
    def utility_i_with_j(self, social, payoff_i, payoff_j):
        utility = (1 - social) * payoff_i + social * payoff_j
        return utility


class PeopleAgent(mesa.Agent):
    """An agent with fixed initial wealth."""

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.social = 0.5  # scoial preference s, the initial value is 0.5 or a person is "half-half" for being "other-regarding"
        self.make_friend = 0  # the actual behavior [0,1] isolated vs outgoing. Assuming at the beginning everyone is isolated.
        self.payoff_f = Payoff_f()

    def payoff(self):

        '''Here the agent has two choices:
        keep using its strategy in the last round (e.g. make friend), or change into an alternative one (e.g. not make friend);
        The decision is based on maximizing its utility function, by comparing the values of both cases and choose;
        In the end, the agent will update to the new strategy and get its utility for the current round'''

        cellmates_id = self.model.grid.get_neighbors(self.pos)
        cellmates = self.model.grid.get_cell_list_contents(cellmates_id)
        # below calculates the default (the same as last round) social strategy of the agent and its utility
        total_utility_of_the_agent = 0
        for cellmate_j in cellmates:
            payoff_of_the_agent_by_interacting_with_the_cellmate_j = self.payoff_f.payoff_i_with_j(self.make_friend,
                                                                                                   cellmate_j.make_friend)
            payoff_of_the_cellmate_j = self.payoff_f.payoff_i_with_j(cellmate_j.make_friend, self.make_friend)
            utility_of_the_agent_by_interacting_with_the_cellmate_j = self.payoff_f.utility_i_with_j(self.social,
                                                                                                     payoff_of_the_agent_by_interacting_with_the_cellmate_j,
                                                                                                     payoff_of_the_cellmate_j)
            total_utility_of_the_agent += utility_of_the_agent_by_interacting_with_the_cellmate_j
        # below calculates alternative social strategy of the agent and its utility
        alternative_total_utility_of_the_agent = 0
        if self.make_friend == 0:
            alternative_make_friend = 1
        else:
            alternative_make_friend = 0
        for cellmate_j in cellmates:
            alternative_payoff_of_the_agent_by_interacting_with_the_cellmate_j = self.payoff_f.payoff_i_with_j(
                alternative_make_friend,
                cellmate_j.make_friend)
            alternative_payoff_of_the_cellmate_j = self.payoff_f.payoff_i_with_j(cellmate_j.make_friend,
                                                                                 alternative_make_friend)
            alternative_utility_of_the_agent_by_interacting_with_the_cellmate_j = self.payoff_f.utility_i_with_j(
                self.social,
                alternative_payoff_of_the_agent_by_interacting_with_the_cellmate_j,
                alternative_payoff_of_the_cellmate_j)
            alternative_total_utility_of_the_agent += alternative_utility_of_the_agent_by_interacting_with_the_cellmate_j
        # below the agent decides which social strategy to choose by optimizing its utility
        if alternative_total_utility_of_the_agent > total_utility_of_the_agent:
            self.make_friend = alternative_make_friend
            total_utility_of_the_agent = alternative_total_utility_of_the_agent
        else:
            pass
        return [self.make_friend, total_utility_of_the_agent, self.social, self.unique_id]
        # # print (self.pos, self.make_friend)

    ## move the agent to random place
    def move(self):
        possible_space = self.model.grid.get_neighborhood(self.pos)
        possible_free_space = []
        for i in possible_space:
            if self.model.grid.is_cell_empty(i) is True:
                possible_free_space.append(i)
        if not possible_free_space:  # if all the neighbour sites are occupied, then move it to a random empty space
            pass
        else:  # move randomly the agent to a neighbouring empty site
            new_position = self.random.choice(possible_free_space)
            self.model.grid.move_agent(self, new_position)

    def change_social(self):
        self.social = self.social + random.choice([-0.05, 0.05])  # change other-regarding social preference randomly plus or minus 0.05
        return

    ## In the end, an agent will do 2 things at each step (as written in the "step" function below):
    ## 1. choose to be outgoing or not by maximizing its utility; 2. 5% of the agents move to neighbouring sites and changing their other-regarding preferences.
    def step(self):
        self.payoff()
        agent_info_i = self.payoff()  # update the behavior
        # print (agent_info_i)
        # return agent_info_i

        # chance_of_move = random.random()  # generate a number randomly between 0 - 1, choose a chance of 5%, if yes, move the agent and change its other-regarding prefernece
        # if chance_of_move <= 0.05:
        #     self.move()
        #     self.change_social()
        # else:
        #     pass


class PeopleModel(mesa.Model):

    def __init__(self, N):
        self.num_agents = N
        self.network = nx.barabasi_albert_graph(20, 10)
        self.grid = mesa.space.NetworkGrid(self.network)
        self.schedule = mesa.time.RandomActivation(self)
        self.init_agent()

        subax1 = plt.subplot()
        nx.draw(self.network, with_labels=True, font_weight='bold')
        subax2 = plt.subplot()
        nx.draw_shell(self.network, nlist=[range(0, 20), range(20)], with_labels=True, font_weight='bold')
        plt.show()

    def init_agent(self):
        for i in range(self.num_agents):
            a = PeopleAgent(i, self)
            self.schedule.add(a)
            self.grid.place_agent(a, random.choice(range(20)))

    def step(self):
        self.schedule.step()