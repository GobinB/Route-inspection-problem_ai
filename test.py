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
    # Create a graph from the adjacency matrix
    G = nx.Graph()
    for i, row in enumerate(testdata):
        for j, weight in enumerate(row):
            if weight != 0:
                G.add_edge(i, j, weight=weight)

    # Compute and draw the Minimum Spanning Tree (MST) using Kruskal's algorithm
    mst = nx.minimum_spanning_tree(G, algorithm='kruskal')
    pos = nx.spring_layout(G)  # Node positions for all nodes
    
    # Drawing code for nodes, edges, labels, and MST
    nx.draw_networkx_nodes(G, pos, node_size=700)
    nx.draw_networkx_edges(G, pos, edgelist=G.edges(), width=6)
    nx.draw_networkx_edges(G, pos, edgelist=mst.edges(), width=6, edge_color="tab:red")
    nx.draw_networkx_labels(G, pos, font_size=20, font_family="sans-serif")
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    
    # Create a legend for the MST edges
    legend_elements = [Line2D([0], [0], color='red', lw=4, label='MST Edges')]
    plt.legend(handles=legend_elements, loc='upper left')
    plt.axis('off')
    
    # Save the graph as an image file and display it
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
