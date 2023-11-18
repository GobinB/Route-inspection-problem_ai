from collections import defaultdict
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

class Graph:
    def __init__(self, graph_matrix):
        self.graph = defaultdict(list)
        for i, row in enumerate(graph_matrix):
            for j, cost in enumerate(row):
                if cost != 0:
                    self.graph[i].append((j, cost))

    def remove_edge(self, u, v):
        for index, (vertex, cost) in enumerate(self.graph[u]):
            if vertex == v:
                self.graph[u].pop(index)
                break
        for index, (vertex, cost) in enumerate(self.graph[v]):
            if vertex == u:
                self.graph[v].pop(index)
                break

    def find_min_cost_edge(self, u):
        if not self.graph[u]:
            return (None, None)
        min_cost_edge = min(self.graph[u], key=lambda x: x[1])
        return (u, min_cost_edge[0], min_cost_edge[1])  # (from, to, cost)

    def find_eulerian_circuit(self):
        if not self.graph:
            return []

        current_vertex = list(self.graph.keys())[0]
        circuit = []
        total_cost = 0

        while True:
            next_edge = self.find_min_cost_edge(current_vertex)
            if next_edge[1] is None:
                break
            circuit.append((next_edge[0], next_edge[1]))
            total_cost += next_edge[2]
            self.remove_edge(next_edge[0], next_edge[1])
            current_vertex = next_edge[1]

            if not any(self.graph.values()):
                break

        return circuit, total_cost
def calculate_fitness(circuit, graph_matrix):
    total_cost = 0
    for i, j in circuit:
        total_cost += graph_matrix[i][j]
    # Fitness is the inverse of cost, we add a small constant to avoid division by zero.
    fitness = 1 / (total_cost + 1e-6)
    return fitness, total_cost




# Define the adjacency matrix
graph_matrix = np.array([
    [0, 37, 0, 0, 0, 0, 0, 68],
    [37, 0, 77, 0, 0, 0, 0, 0],
    [0, 77, 0, 88, 0, 0, 0, 0],
    [0, 0, 88, 0, 115, 0, 0, 0],
    [0, 0, 0, 115, 0, 42, 0, 0],
    [0, 0, 0, 0, 42, 0, 88, 0],
    [0, 0, 0, 0, 0, 88, 0, 43],
    [68, 0, 0, 0, 0, 0, 43, 0]
])

# Create a Graph instance
G = Graph(graph_matrix)

# Find Eulerian circuit and total cost
circuit, total_cost = G.find_eulerian_circuit()

# Calculate fitness
fitness, _ = calculate_fitness(circuit, graph_matrix)

# Print circuit, total cost, and fitness
print("Eulerian Circuit:", circuit)
print("Total Cost:", total_cost)
print("Fitness:", fitness)

# Create a graph from the adjacency matrix
G = nx.Graph()
for i in range(len(graph_matrix)):
    for j in range(len(graph_matrix[i])):
        if graph_matrix[i][j] != 0:
            G.add_edge(i, j, weight=graph_matrix[i][j])

# Draw the graph
pos = nx.spring_layout(G)  # positions for all nodes
nx.draw(G, pos, with_labels=True)

# Edge labels
edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

plt.title('Graph Representation with Edge Costs')
plt.show()
