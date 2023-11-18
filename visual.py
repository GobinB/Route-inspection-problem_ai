import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx
import numpy as np
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from test2 import Graph

def calculate_fitness(circuit, graph_matrix):
    total_cost = 0
    for i, j in circuit:
        total_cost += graph_matrix[i][j]
    # Fitness is the inverse of cost, we add a small constant to avoid division by zero.
    fitness = 1 / (total_cost + 1e-6)
    return fitness, total_cost
def draw_graph(filename):
    # Read adjacency matrix from file
    graph_matrix = np.loadtxt(filename, dtype=int)

    # Create a Graph instance
    G = Graph(graph_matrix)

    # Find Eulerian circuit and total cost
    circuit, total_cost = G.find_eulerian_circuit()

    # Create a graph from the adjacency matrix
    G = nx.Graph()
    for i in range(len(graph_matrix)):
        for j in range(len(graph_matrix[i])):
            if graph_matrix[i][j] != 0:
                G.add_edge(i, j, weight=graph_matrix[i][j])

    # Create a Tkinter window
    root = tk.Tk()
    root.title("Graph Visualization")

    # Create a Matplotlib figure
    fig = Figure(figsize=(8, 6))
    ax = fig.add_subplot(111)

    # Draw the graph
    pos = nx.spring_layout(G)  # positions for all nodes
    nx.draw(G, pos, with_labels=True, ax=ax)

    # Edge labels
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax)

    ax.set_title('Graph Representation with Edge Costs')

    # Embed the Matplotlib figure into a Tkinter canvas
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack()

    # Calculate fitness
    fitness, _ = calculate_fitness(circuit, graph_matrix)

    # Print circuit, total cost, and fitness
    circuit_str = " -> ".join([f"{i}->{j}" for i, j in circuit])
    fitness_label = tk.Label(root, text=f"Eulerian Circuit: {circuit_str}")
    total_cost_label = tk.Label(root, text=f"Total Cost: {total_cost}")
    fitness_label.pack()
    total_cost_label.pack()

    fitness_label = tk.Label(root, text=f"Fitness: {fitness}")
    fitness_label.pack()

    root.mainloop()