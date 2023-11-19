import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import tkinter as tk
from tkinter import filedialog
import random
# Define global variable to hold test data
testdata = []

# Function to open a file dialog and load test data
def open_file():
    global testdata
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, "r") as file:
            testdata = [list(map(int, line.split())) for line in file.readlines()]
           
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


# Function to create and draw the graph based on a solution
def draw_graph(graph, solution=None, show=True):
    # Draw the graph using the solution if provided, else draw the original graph
    pos = nx.spring_layout(graph)
    nx.draw_networkx_nodes(graph, pos, node_size=700)
    nx.draw_networkx_edges(graph, pos, edgelist=graph.edges(), width=6)
    
    if solution:
        # Highlight the solution path
        path_edges = list(zip(solution, solution[1:] + [solution[0]]))
        nx.draw_networkx_edges(graph, pos, edgelist=path_edges, width=6, edge_color="tab:red")
        
    nx.draw_networkx_labels(graph, pos, font_size=20, font_family="sans-serif")
    edge_labels = nx.get_edge_attributes(graph, 'weight')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)
    
    legend_elements = [Line2D([0], [0], color='red', lw=4, label='Solution Path' if solution else 'Eulerian Circuit')]
    plt.legend(handles=legend_elements, loc='upper left')
    plt.axis('off')
    plt.title(f"Total Distance: {calculate_fitness(graph, solution) if solution else 'N/A'}")
    plt.savefig('output.png')
    
    if show:
        plt.show()


def initialize_population(graph, population_size):
    population = []
    for _ in range(population_size):
        # Create a random solution (a sequence of node indices)
        solution = list(graph.nodes())
        random.shuffle(solution)
        population.append(solution)
    return population

def calculate_fitness(graph, solution):
    weight_sum = 0
    for i in range(len(solution) - 1):
        u, v = solution[i], solution[i+1]
        if graph.has_edge(u, v):
            weight_sum += graph[u][v]['weight']
        else:
            weight_sum += 200 # Penalize the fitness for invalid edges
    # Include the edge from the last to the first node to complete the circuit
    if graph.has_edge(solution[-1], solution[0]):
        weight_sum += graph[solution[-1]][solution[0]]['weight']
    else:
        weight_sum += 200
    return weight_sum



def select_parents(population, graph):
    # Tournament selection
    tournament_size = 5
    parents = []
    for _ in range(2):  # Select two parents
        tournament = random.sample(population, tournament_size)
        tournament.sort(key=lambda x: calculate_fitness(graph, x))
        parents.append(tournament[0])
    return parents

def crossover(parent1, parent2):
    # Single-point crossover
    crossover_point = random.randint(1, len(parent1) - 2)
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]
    return child1, child2

def mutate(solution, mutation_rate):
    # Swap mutation
    for i in range(len(solution)):
        if random.random() < mutation_rate:
            swap_with = random.randint(0, len(solution) - 1)
            solution[i], solution[swap_with] = solution[swap_with], solution[i]
    return solution

def genetic_algorithm(graph, population_size, generations, mutation_rate):
    population = initialize_population(graph, population_size)
    
    for g in range(generations):
        new_population = []
        for _ in range(population_size // 2):
            parent1, parent2 = select_parents(population, graph)
            child1, child2 = crossover(parent1, parent2)
            new_population.append(mutate(child1, mutation_rate))
            new_population.append(mutate(child2, mutation_rate))
        
        # Evaluate the fitness of the new population
        population.sort(key=lambda x: calculate_fitness(graph, x))
        # Replace the worst half with new solutions
        population = population[:population_size // 2] + new_population[:population_size // 2]
        
        # The following line has been removed from here
        # draw_graph(graph, population[0], show=True)
        
    # Draw the best solution found after all generations
    draw_graph(graph, population[0], show=True)
    
    return population[0]  # Return the best solution found

def run_ga():
    global testdata
    G = nx.Graph()
    for i, row in enumerate(testdata):
        for j, weight in enumerate(row):
            if weight != 0:
                G.add_edge(i, j, weight=weight)
    
    # Run the genetic algorithm to find the best solution
    best_solution = genetic_algorithm(G, population_size=50, generations=100, mutation_rate=0.3)
    
    # Draw the graph with the best solution found by the GA, only showing the final result
    draw_graph(G, best_solution, show=True)


# Modify the Tkinter setup to include a button to run the GA
ga_button = tk.Button(root, text="Run Genetic Algorithm", command=run_ga)
ga_button.pack()

root.mainloop()