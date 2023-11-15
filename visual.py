import tkinter as tk
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx
import numpy as np
from matplotlib.figure import Figure

from solverccp import main_genetic_algorithm

def edges_to_adjacency_matrix(edges):
    # Determine the number of nodes by finding the max node index in edges
    num_nodes = max(max(e[0], e[1]) for e in edges) + 1
    adjacency_matrix = np.zeros((num_nodes, num_nodes))

    # Update the adjacency matrix for each edge
    for i, j in edges:
        adjacency_matrix[i][j] = 1  # If the graph is undirected, set to 1 for both [i][j] and [j][i]
        # Uncomment the next line if the graph is undirected
        # adjacency_matrix[j][i] = 1

    return adjacency_matrix

def draw_graph(adjacency_matrix):
    # Create a graph from the adjacency matrix
    G = nx.from_numpy_matrix(adjacency_matrix, create_using=nx.DiGraph())
    pos = nx.circular_layout(G)  # positions for all nodes in a circular layout

    figure = Figure(figsize=(6, 4), dpi=100)
    plot = figure.add_subplot(1, 1, 1)
    
    # Draw the nodes
    nx.draw_networkx_nodes(G, pos, node_size=700, node_color="lightblue", ax=plot)
    
    # Draw the edges with the weights as labels
    nx.draw_networkx_edges(G, pos, arrowstyle='-|>', arrowsize=20, width=2, ax=plot)
    edge_labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=plot)
    
    # Draw the labels
    nx.draw_networkx_labels(G, pos, font_size=20, font_family="sans-serif", ax=plot)
    
    plot.set_title('Network Graph of Chinese Postman Problem')
    plot.axis('off')  # Turn off the axis

    return figure

def plot_data():

    # edges, best_fitness, num_nodes = main_genetic_algorithm()  # Modify your function to also return num_nodes
    best_circuit, best_fitness = main_genetic_algorithm()

    # adjacency_matrix, best_fitness = main_genetic_algorithm()
    # adjacency_matrix = edges_to_adjacency_matrix(edges, num_nodes)
    adjacency_matrix = edges_to_adjacency_matrix(best_circuit)
    


    figure = draw_graph(adjacency_matrix)

    # Clear previous figure
    for widget in frame.winfo_children():
        widget.destroy()

    # Create canvas and add the plot to the GUI
    canvas = FigureCanvasTkAgg(figure, master=frame)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    canvas.draw()

root = tk.Tk()
root.title("Genetic Algorithm for Chinese Postman Problem")

frame = tk.Frame(root)
frame.pack(fill=tk.BOTH, expand=1)

plot_data()
root.mainloop()
