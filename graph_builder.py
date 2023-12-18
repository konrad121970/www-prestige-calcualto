import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

class GraphBuilder:
    def __init__(self, incidence_list):
        self.df = pd.DataFrame(incidence_list, columns=['source', 'target'])
        self.G = nx.DiGraph()
        self.adjacency_matrix = None
        self.nodes = None

    def build_directed_graph(self):
        for row in self.df.itertuples(index=False):
            source = row.source
            targets = row.target
            for target in targets:
                if target != '':
                    self.G.add_edge(source, target)

    def get_nodes(self):
        self.nodes = list(self.G.nodes())

    def build_adjacency_matrix(self):
        self.adjacency_matrix = np.zeros((len(self.nodes), len(self.nodes)))

        for i, node in enumerate(self.nodes):
            neighbors = list(self.G.neighbors(node))
            for neighbor in neighbors:
                j = self.nodes.index(neighbor)
                self.adjacency_matrix[i, j] = 1

    def display_adjacency_matrix(self):
        print("Macierz sąsiedztwa:")
        print(self.adjacency_matrix)

    def draw_graph(self):
        self.build_directed_graph()
        self.get_nodes()
        self.build_adjacency_matrix()
        self.display_adjacency_matrix()

        pos = nx.spring_layout(self.G)
        nx.draw(self.G, pos, with_labels=True, arrowsize=20, node_size=700, node_color="skyblue", font_size=10,
                font_color="black", font_weight="bold", font_family="sans-serif")
        plt.title("Graf na podstawie DataFrame")
        plt.show()
