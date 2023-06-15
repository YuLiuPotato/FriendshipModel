import mesa
import random
from statistics import mean
import numpy as np


def count_make_friend(model):  # counts how many agents chooses make friend strategy in a round
    make_friend_list = [i.make_friend for i in model.schedule.agents]
    make_friend_yes_counts = len([i for i in make_friend_list if i == 1])
    return make_friend_yes_counts


def average_utility(model):  # calculate the average utility of each agent in a round
    every_utility_list = [i.agent_utility for i in model.schedule.agents]
    average_utility = mean(every_utility_list)
    return average_utility


def average_social(model):  # calculate the average social of each agent in a round
    every_social_list = [i.social for i in model.schedule.agents]
    average_social = mean(every_social_list)
    return average_social


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
        self.social = random.random()  # social preference of other-regarding or self-regarding, randomly distributed between 0-1
        # self.social = 0.5
        # self.make_friend = 0  # the actual behavior [0,1] isolated vs outgoing. Assuming at the beginning everyone is isolated.
        self.make_friend = random.choice([0,1])  # the actual behavior [0,1] isolated vs outgoing. Assuming at the beginning everyone is isolated.
        self.payoff_f = Payoff_f()

    def payoff(self):

        '''Here the agent has two choices:
        keep using its strategy in the last round (e.g. make friend), or change into an alternative one (e.g. not make friend);
        The decision is based on maximizing its utility function, by comparing the values of both cases and choose;
        In the end, the agent will update to the new strategy and get its utility for the current round'''

        cellmates = self.model.grid.get_neighbors(self.pos, moore=True)
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
        if not len(cellmates) == 0:
            total_utility_of_the_agent = total_utility_of_the_agent / len(cellmates)
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
        if not len(cellmates) == 0:
            alternative_total_utility_of_the_agent = alternative_total_utility_of_the_agent / len(cellmates)

        # below the agent decides which social strategy to choose by optimizing its utility
        if alternative_total_utility_of_the_agent > total_utility_of_the_agent:
            self.make_friend = alternative_make_friend
            total_utility_of_the_agent = alternative_total_utility_of_the_agent
        else:
            pass
        self.agent_utility = total_utility_of_the_agent
        return {self.unique_id: [total_utility_of_the_agent, self.social, self.make_friend]}
        # # print (self.pos, self.make_friend)

    ## move the agent to random place
    def move(self):
        possible_space = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
        possible_free_space = []
        for i in possible_space:
            if self.model.grid.is_cell_empty(i) is True:
                possible_free_space.append(i)
        if not possible_free_space:  # if all the neighbour sites are occupied, then move it to a random empty space
            self.model.grid.move_to_empty(self)
        else:  # move randomly the agent to a neighbouring empty site
            new_position = self.random.choice(possible_free_space)
            self.model.grid.move_agent(self, new_position)

    def change_social(self):
        self.social = self.social + random.choice(
            [-0.1, 0.1])  # change other-regarding social preference randomly plus or minus 0.1
        # self.social = self.social + 0.05  # change other-regarding social preference by increasing 0.05
        # self.social = self.social - 0.05  # change other-regarding social preference by decreasing 0.05
        return

    ## In the end, an agent will do 2 things at each step (as written in the "step" function below):
    ## 1. choose to be outgoing or not by maximizing its utility; 2. 5% of the agents move to neighbouring sites and changing their other-regarding preferences.
    def step(self):
        agent_info_i = self.payoff()  # update the behavior
        self.model.agents_info(agent_info_i)  # gather all agents' info by updating every agent's info in a round
        if self.unique_id in self.model.choose_agents():  # in the second round, if the agent belongs to the last 5% group of the first round, then it does the followings
            self.move()
            self.change_social()
        else:
            pass


class PeopleModel(mesa.Model):

    def __init__(self, N, width, height):
        self.num_agents = N
        self.grid = mesa.space.MultiGrid(width, height, True)
        self.schedule = mesa.time.RandomActivation(self)
        self.init_agent()
        self.all_agents_info = {}
        self.agents_chosen = []

    def init_agent(self):
        for i in range(self.num_agents):
            a = PeopleAgent(i, self)
            self.schedule.add(a)
            self.grid.place_agent(a, self.grid.find_empty())  # Good change Yu :)

        self.datacollector = mesa.DataCollector(
            model_reporters={"average_utility": average_utility, "average_social": average_social,
                             "count_make_friend": count_make_friend},
            agent_reporters={"utility": "agent_utility", "social": "social", "make_friend": "make_friend"})

    def agents_info(self, new_agent_info):
        self.all_agents_info.update(new_agent_info)

    def choose_agents(self):
        return self.agents_chosen

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)
        self.agents_chosen = list((dict(sorted(self.all_agents_info.items(), key=lambda item: item[1][0]))))[
                             :5]  # identify the id of 5 agents with the lowest utility values
