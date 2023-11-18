import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import tkinter as tk
from tkinter import filedialog

# Define global variable to hold test data
testdata = []

# Function to open a file dialog and load test data
def open_file():
    global testdata
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, "r") as file:
            testdata = [list(map(int, line.split())) for line in file.readlines()]
            draw_graph()  # Call the function to draw the graph once data is loaded

# Function to create and draw the graph
def draw_graph():
    global testdata
    G = nx.Graph()
    for i, row in enumerate(testdata):
        for j, weight in enumerate(row):
            if weight != 0:
                G.add_edge(i, j, weight=weight)
    
    # Find nodes with odd degrees
    odd_nodes = [node for node in G.nodes() if G.degree(node) % 2 == 1]
    
    # Create a complete graph among odd-degree nodes and find the minimum-weight perfect matching
    complete_graph = nx.complete_graph(odd_nodes)
    min_weight_matching = nx.min_weight_matching(complete_graph, weight='weight')
    
    # Duplicate edges in the original graph to create an Eulerian graph
    eulerian_graph = G.copy()
    for u, v in min_weight_matching:
        shortest_path = nx.shortest_path(G, source=u, target=v, weight='weight')
        for i in range(len(shortest_path) - 1):
            eulerian_graph.add_edge(shortest_path[i], shortest_path[i + 1], weight=G[shortest_path[i]][shortest_path[i + 1]]['weight'])
    
    # Find the Eulerian circuit in the augmented graph
    eulerian_circuit = list(nx.eulerian_circuit(eulerian_graph))
    
    # Calculate the total distance of the circuit
    total_distance = sum([eulerian_graph[u][v]['weight'] for u, v in eulerian_circuit])
    
    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos, node_size=700)
    nx.draw_networkx_edges(G, pos, edgelist=G.edges(), width=6)
    nx.draw_networkx_edges(G, pos, edgelist=eulerian_circuit, width=6, edge_color="tab:red")
    nx.draw_networkx_labels(G, pos, font_size=20, font_family="sans-serif")
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    
    legend_elements = [Line2D([0], [0], color='red', lw=4, label='Eulerian Circuit')]
    plt.legend(handles=legend_elements, loc='upper left')
    plt.axis('off')
    
    plt.title(f"Total Distance: {total_distance}")
    plt.savefig('output.png')
    plt.show()

# Create a Tkinter window
root = tk.Tk()
root.title("Minimum Spanning Tree")

# Create a button to open the file dialog
open_button = tk.Button(root, text="Open File", command=open_file)
open_button.pack()

# Function to find the vertex with the minimum key value
def min_key(key, mst_set):
    min_value = float('inf')
    min_index = -1
    for v in range(len(testdata)):
        if key[v] < min_value and not mst_set[v]:
            min_value = key[v]
            min_index = v
    return min_index

# Prim's algorithm for MST
def prims_algorithm(graph):
    num_vertices = len(graph)
    selected = [False] * num_vertices
    key = [float('inf')] * num_vertices
    parent = [-1] * num_vertices
    key[0] = 0
    
    for _ in range(num_vertices):
        u = min_key(key, selected)
        selected[u] = True
        
        for v in range(num_vertices):
            if graph[u][v] > 0 and not selected[v] and key[v] > graph[u][v]:
                key[v] = graph[u][v]
                parent[v] = u
    
    return parent

# Placeholder for Prim's MST result; will be populated when file is loaded and Prim's algorithm is executed
mst_parents = []

# Main loop of the Tkinter window
root.mainloop()
