import mesa
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from itertools import islice
from statistics import mean
from enum import Enum
import networkx as nx

class Mode(Enum):
    def __init__(self):
        self.TIME = 0

class Analyzer():
    def __init__(self):
        self.Mode = Mode
    def load(self,csv_file):
        self.df = pd.read_csv(csv_file)
    def plot_network(self,step):
        filtered_names_ = self.df.loc[self.df['Step'] == step]
        Agent = filtered_names_['AgentID'].values
        friend_people = []
        for i in filtered_names_['friendship_people']:
            i = i.strip('[]').split(', ')
            list = [k for k in i]
            friend_people.append(list)
        friend_value = []
        for i in filtered_names_['friendship_value']:
            if (i == "[]"):
                friend_value.append('')
            else:
                i = i.strip('[]').split(', ')
                list = [float(k) for k in i]

                friend_value.append(list)
        G = nx.DiGraph()
        #print(f'Agent:{Agent},friend_people:{friend_people},friend_value:{friend_value},')
        for i in Agent:
            G.add_node(i)
        for i in range(len(Agent)):
            for k in range(len(friend_people[i])):
                if(friend_people[i][k]!=""):
                    G.add_edge(Agent[i],friend_people[i][k],weight=friend_value[i][k])
        pos = nx.spring_layout(G)  # Specify the layout algorithm

        # Draw the nodes
        #nx.draw_networkx_nodes(G.subgraph(['30','50']), pos, node_color='lightblue', node_size=50,alpha=0.7)

        # Draw the edges
        #nx.draw_networkx_edges(G.subgraph(['30','50']), pos, arrowstyle='->', arrowsize=1)

        # Add labels to the edges with weights
        labels = nx.get_edge_attributes(G, 'weight')
        #nx.draw_networkx_edge_labels(G, pos, edge_labels=labels,font_size=2)
        nodes =[30,50]
        neighbors_30 = G.neighbors(nodes[0])
        neighbors_50 = G.neighbors(nodes[1])

        for i in neighbors_30:
            nodes.append(i)
        for i in neighbors_50:
            nodes.append(i)

        subgraph_nodes = nodes
        subgraph = G.subgraph(subgraph_nodes)
        labels = nx.get_edge_attributes(subgraph, 'weight')
        # Draw node labels
        #nx.draw_networkx_labels(G, pos, font_size=12, font_color='black')
        #nx.draw(subgraph, with_labels=True, node_color='lightblue', node_size=500, edge_color='gray')
        # Display the graph
        #plt.axis('off')
        #plt.savefig('graph/' +"30_50_steps_"+ str(step) + ".png")
        #plt.show()
        #plt.savefig('graph/'+str(step)+"steps_30_50.png")
        #plt.clf()

        num_nodes = G.number_of_nodes()
        num_edges = G.number_of_edges()
        average_degree = sum(dict(G.degree()).values()) / num_nodes
#        average_shortest_path_length = nx.average_shortest_path_length(G)
        node_cluster_coefficients = nx.clustering(G.to_undirected())
        average_cluster_coefficient = sum(node_cluster_coefficients.values()) / len(node_cluster_coefficients)
       # clustering_coefficient = nx.average_clustering(G)

        print("Number of nodes:", num_nodes)
        print("Number of edges:", num_edges)
        print("Average degree:", average_degree)
        #print("Average shortest path length:", average_shortest_path_length)
        print("Clustering coefficient:", average_cluster_coefficient)

        degrees = [G.degree(node) for node in G.nodes()]
        plt.hist(degrees, bins=range(min(degrees), max(degrees) + 2, 1), align='left', alpha=0.7, color='lightblue')
        plt.xlabel('Degree (Number of Edges)')
        plt.ylabel('Frequency')
        plt.title('Distribution of Edges')
        plt.xticks(range(min(degrees), max(degrees) + 1))
        plt.savefig('graph/friend_ship_net/' +"steps_node_distribution_"+ str(step) + ".png")
        plt.show()
        plt.clf()

        weights = [d['weight'] for u, v, d in G.edges(data=True)]
        plt.hist(weights,bins=100, edgecolor='black')
        plt.xlabel('Weight')
        plt.ylabel('Frequency')
        #plt.xticks([1.0,1.2,1.4,1.6,1.8,2.0])
        plt.title('Weighted Edges Distribution')
        plt.show()

    def Plot(self,ID):
        filtered_names_ = self.df.loc[self.df['AgentID'] == ID]
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
a.load('/Users/michael/Documents/ETh/Sem2/fpga for quantum engineering/FriendshipModel/result_agent_model.csv')
a.Plot(60)
a.plot_network(60)
#for i in range(5,700):
    #a.plot_network(i)