from collections import Counter, OrderedDict
from random import randrange, uniform

import matplotlib.pyplot as plt
import networkx as nx

colors = {
    "RED": '#ff0000',
    "ORANGE": '#ff5500',
    "YELLOW": '#fce500',
    "LIGHT_GREEN": '#b9ff00',
    "GREEN": '#46ff00',
    "COREAL": '#00ff78',
    "LIGHT_BLUE": '#00ffff',
    "BLUE": '#0074ff',
    "DARK_BLUE": '#0013ff',
    "DARK_PURPLE": '#7b00b5',
    "LIGHT_PURPLE": '#d500ff',
    "PINK": '#e800ff',
    "DARK_PINK": '#7e005f',
    "LIGHT_PINK": '#ff0683',
    "DARK_ORANGE": '#8c4600',
    "LIGHT_ORANGE": '#fc9e3f',
    "DARK_GREEN": '#2d7300',
    "BLACK": '#000000',
    "DARK_RED": '#4a0200',
    "LIGHT_RED": '#fc645f',
    "GREY": '#858585'
}

colors_dict = OrderedDict(colors)

NUMBER_OF_NODES = 8192
COEF = 8


def find_neighbour(graph, new_node_color):
    def fitness_coefficient(node):
        if new_node_color == colors['GREY']:
            return 1

        if new_node_color == node['node_color']:
            return COEF

        return round(uniform(0.1, 0.99), 2)

    coeffs = {node: fitness_coefficient(graph.nodes[node]) for node in graph.nodes}

    if all(coeff == 1 for coeff in coeffs.values()):
        neighbour = sorted(coeffs, key=lambda node: coeffs[node], reverse=True)[randrange(len(coeffs.keys()))]
    else:
        neighbour = sorted(coeffs, key=lambda node: coeffs[node], reverse=True)[0]

    return neighbour


def build_degree_frequency_plot(grey_degree_sequence, degree_sequence):
    degree_count = Counter(degree_sequence)
    deg, cnt = zip(*degree_count.items())

    grey_degree_count = Counter(grey_degree_sequence)
    grey_deg, grey_cnt = zip(*grey_degree_count.items())

    plt.loglog(grey_deg, 'r-', marker='o')
    plt.loglog(deg, 'b-', marker='o')

    plt.title("Degree Histogram")
    plt.ylabel("Count")
    plt.xlabel("Degree")

    plt.figure(figsize=(20, 100))

    plt.show()


def build_degree_rank_plot(grey_degree_sequence, degree_sequence):
    grey = sorted(grey_degree_sequence.values(), reverse=True)
    colored = sorted(degree_sequence.values(), reverse=True)

    plt.loglog(grey, 'r-', marker='o')
    plt.loglog(colored, 'b-', marker='o')
    plt.title("Degree rank plot")
    plt.ylabel("degree")
    plt.xlabel("rank")

    plt.figure(figsize=(20, 20))

    plt.show()


from collections import defaultdict

graph = nx.Graph()
graph.add_node(0, node_color='GREY')
graph.add_node(1, node_color='GREY')

fitness_coef = dict(graph.degree)

colors_list = list(colors_dict.keys())
color_map = defaultdict(list)

for new_node in range(graph.size() + 1, NUMBER_OF_NODES + 1):
    random_value = randrange(100)
    if (random_value > 19):
        color = colors['GREY']
    else:
        color = colors[colors_list[random_value]]

    node_neighbour = find_neighbour(graph, color)

    graph.add_node(new_node, node_color=color)
    graph.add_edge(new_node, node_neighbour)

    color_map[color].append(new_node)

grey_degree_sequence = {node: graph.degree[node] for node in graph.nodes if
                        graph.nodes[node]['node_color'] == colors['GREY']}
degree_sequence = {node: graph.degree[node] for node in graph.nodes if
                   graph.nodes[node]['node_color'] != colors['GREY']}

build_degree_frequency_plot(grey_degree_sequence, degree_sequence)
build_degree_rank_plot(grey_degree_sequence, degree_sequence)

# plt.figure(figsize=(20, 20))
#
# for color, node_list in color_map.items():
#     nx.draw_networkx_nodes(graph, pos=nx.kamada_kawai_layout(graph), nodelist=node_list, node_color=color)
#
# nx.draw_networkx_edges(graph, pos=nx.kamada_kawai_layout(graph), width=1.0, alpha=0.5)
# plt.show()
