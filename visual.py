import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx
import numpy as np
from matplotlib.figure import Figure

def edges_to_adjacency_matrix(edges, num_nodes):
    adjacency_matrix = np.zeros((num_nodes, num_nodes))

    # Update the adjacency matrix for each edge
    for u, v in edges:
        adjacency_matrix[u][v] = 1  # Set to 1 for edge u-v
        adjacency_matrix[v][u] = 1  # Set to 1 for edge v-u as the graph is undirected

    return adjacency_matrix


def draw_graph(adjacency_matrix, best_circuit):
    G = nx.Graph(adjacency_matrix)
    pos = nx.circular_layout(G)

    figure = Figure(figsize=(6, 4), dpi=100)
    plot = figure.add_subplot(1, 1, 1)
    
    nx.draw_networkx_nodes(G, pos, node_size=700, node_color="lightblue", ax=plot)
    
    # Draw all edges with default color first
    nx.draw_networkx_edges(G, pos, width=2, ax=plot)
    
    # Now draw the best circuit with green color
    best_path_edges = [(best_circuit[i], best_circuit[i + 1]) for i in range(len(best_circuit) - 1)]
    
    # Ensure that best_path_edges exist in the graph
    best_path_edges = [(u, v) for u, v in best_path_edges if G.has_edge(u, v)]
    
    nx.draw_networkx_edges(G, pos, edgelist=best_path_edges, width=2, edge_color="green", ax=plot)
    
    edge_labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=plot)
    nx.draw_networkx_labels(G, pos, font_size=20, font_family="sans-serif", ax=plot)
    
    plot.set_title('Network Graph of Chinese Postman Problem')
    plot.axis('off')

    return figure


def plot_data(best_circuit, best_fitness, frame):
    # Determine the number of nodes
    # num_nodes = max(max(u, v) for u, v in best_circuit) + 1
    best_path_edges = [(best_circuit[i], best_circuit[i + 1]) for i in range(len(best_circuit) - 1)]
    num_nodes = max(best_circuit) + 1  # Since best_circuit is a list of nodes, we can simply take the max
    adjacency_matrix = edges_to_adjacency_matrix(best_path_edges, num_nodes)

    # Convert the Eulerian circuit to an adjacency matrix
    # adjacency_matrix = edges_to_adjacency_matrix(best_circuit, num_nodes)
    # figure = draw_graph(adjacency_matrix, best_circuit)
    figure = draw_graph(adjacency_matrix, best_path_edges)


    # figure = draw_graph(adjacency_matrix)

    # Clear previous figure
    for widget in frame.winfo_children():
        widget.destroy()

    # Create canvas and add the plot to the GUI
    canvas = FigureCanvasTkAgg(figure, master=frame)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    canvas.draw()
