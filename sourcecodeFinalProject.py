import numpy as np
import pandas as pd
import random
import networkx as nx
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import itertools

def read_txt_file_to_graph(filename):
    # Read the adjacency matrix from a .txt file into a graph
    with open(filename, 'r') as file:
        lines = file.readlines()
    matrix = [list(map(int, line.strip().split())) for line in lines]
    graph = nx.from_numpy_array(np.array(matrix))
    return graph



def find_odd_degree_vertices(graph):
    # Find all vertices in the graph with odd degree
    odd_degree_vertices = [v for v, d in graph.degree() if d % 2 == 1]
    return odd_degree_vertices

def add_edges_to_make_eulerian(graph, odd_degree_vertices):
    # Create a complete graph over the odd degree vertices with the shortest path distances as weights
    odd_graph = nx.complete_graph(len(odd_degree_vertices))
    for i, u in enumerate(odd_degree_vertices):
        for j, v in enumerate(odd_degree_vertices):
            if i < j:
                # Check if both u and v exist in the graph
                if u in graph.nodes and v in graph.nodes:
                    try:
                        # Attempt to find the shortest path
                        path = nx.shortest_path(graph, source=u, target=v, weight='weight')
                        weight = sum(graph[path[k]][path[k + 1]]['weight'] for k in range(len(path) - 1))
                        odd_graph.add_edge(u, v, weight=weight)
                    except nx.NetworkXNoPath:
                        # Handle the case where no path exists between u and v
                        print(f"No path between {u} and {v}. Skipping.")
                        continue
                else:
                    print(f"One or both of the nodes {u} and {v} are not in the graph. Skipping.")

    # Find the minimum weight perfect matching on the odd_graph
    min_matching = nx.algorithms.matching.max_weight_matching(odd_graph)

    # Add the edges in the original graph as per the matching
    for u, v in min_matching:
        path = nx.shortest_path(graph, source=u, target=v, weight='weight')
        for i in range(len(path) - 1):
            if path[i] != path[i + 1]:  # Check if the path is non-trivial
                # Increase the weight of the edge if it already exists, otherwise add a new edge
                if graph.has_edge(path[i], path[i + 1]):
                    graph[path[i]][path[i + 1]]['weight'] += graph[path[i]][path[i + 1]]['weight']
                else:
                    graph.add_edge(path[i], path[i + 1], weight=graph[path[i]][path[i - 1]]['weight'])

    # After adding edges, check if the graph is now Eulerian
    if not nx.is_eulerian(graph):
        raise nx.NetworkXError("The graph is not Eulerian after adding edges.")

    return graph



def create_eulerian_circuit(graph, starting_node=None):
    # Create an Eulerian circuit from an Eulerian graph
    if starting_node is None:
        starting_node = random.choice(list(graph.nodes))
    eulerian_circuit = list(nx.eulerian_circuit(graph, source=starting_node))
    return eulerian_circuit

def cpp_fitness(eulerian_circuit, graph):
    # Fitness is the total weight of the Eulerian circuit
    return sum(graph[u][v]['weight'] for u, v in eulerian_circuit)

def initialize_population(graph, pop_size):
    # Initialize the population as a list of random Eulerian circuits
    population = []
    for _ in range(pop_size):
        eulerian_circuit = create_eulerian_circuit(graph)
        population.append(eulerian_circuit)
    return population

def tournament_selection(population, graph, tournament_size=3):
    # Select the best circuit from a random sample of the population
    sample = random.sample(population, tournament_size)
    best_circuit = min(sample, key=lambda circuit: cpp_fitness(circuit, graph))
    return best_circuit

def validate_eulerian_circuit(circuit, graph):
    """
    Validates and, if necessary, corrects the sequence of edges to ensure it is an Eulerian circuit.
    This is a placeholder function for illustrative purposes.
    """
    try:
        # Check if the circuit is Eulerian
        if nx.is_eulerian(graph):
            return True, circuit
        else:
            # If not, try to correct the circuit (this is non-trivial and will need a proper implementation)
            return False, circuit  # Returning the unmodified circuit for now
    except nx.NetworkXError as e:
        print(f"Error during Eulerian validation: {e}")
        return False, circuit
    

def ordered_crossover(parent1, parent2, graph):
    """
    Perform an ordered crossover that respects the Eulerian circuit.
    This is a complex operation, so we will perform a simple edge swap
    between two circuits instead of a traditional crossover.
    """
    # Find a random edge in parent1 and replace it with an edge from parent2
    edge_to_replace = random.choice(parent1)
    
    # Ensure the replacement edge is not in parent1
    available_edges = [edge for edge in parent2 if edge not in parent1]
    
    if not available_edges:
        # If no suitable replacement edge is found, return parent1 as is
        return parent1
    
    replacement_edge = random.choice(available_edges)
    
    # Make the new offspring
    offspring = parent1[:]
    offspring.remove(edge_to_replace)
    offspring.append(replacement_edge)
   
    is_valid, corrected_offspring = validate_eulerian_circuit(offspring, graph)
    return corrected_offspring if is_valid else parent1  # Fallback to parent1 if not valid


def mutate(eulerian_circuit, graph, mutation_rate):
    """
    Mutate an Eulerian circuit by swapping two edges.
    """
    if random.random() < mutation_rate:
        edge1, edge2 = random.sample(eulerian_circuit, 2)
        eulerian_circuit.remove(edge1)
        eulerian_circuit.remove(edge2)
        eulerian_circuit.append(edge1[::-1])  # Reverse edge1 and append
        eulerian_circuit.append(edge2[::-1])  # Reverse edge2 and append
        
    # Ensure the mutated circuit is still Eulerian
    is_valid, corrected_circuit = validate_eulerian_circuit(eulerian_circuit, graph)
    return corrected_circuit if is_valid else eulerian_circuit  # Fallback to the original if not valid

def genetic_algorithm(graph, pop_size, num_generations, mutation_rate):
    """
    The main genetic algorithm loop for the CPP.
    """
    # Initialize population
    population = initialize_population(graph, pop_size)
    
    # Track the best solution
    best_circuit = min(population, key=lambda circuit: cpp_fitness(circuit, graph))
    best_fitness = cpp_fitness(best_circuit, graph)
    
    for generation in range(num_generations):
        new_population = []
        for _ in range(pop_size):
            # Selection
            parent1 = tournament_selection(population, graph)
            parent2 = tournament_selection(population, graph)
            
            # Crossover
            offspring = ordered_crossover(parent1, parent2, graph)
            
            # Mutation
            offspring = mutate(offspring, graph, mutation_rate)
            
            new_population.append(offspring)
        
        # Evaluate new population
        population = new_population
        current_best = min(population, key=lambda circuit: cpp_fitness(circuit, graph))
        current_best_fitness = cpp_fitness(current_best, graph)
        
        # Update the best solution
        if current_best_fitness < best_fitness:
            best_circuit = current_best
            best_fitness = current_best_fitness
        
        # (Optional) Print out some information every few generations
        if generation % 10 == 0:
            print(f"Generation {generation}: Best Fitness = {best_fitness}")
    
    return best_circuit, best_fitness

def visualize_cpp_solution(solution, graph):
    """
    Visualize the CPP solution using matplotlib and integrate it into a Tkinter GUI.
    """
    root = tk.Tk()
    root.title("Chinese Postman Problem Solution Visualization")

    # Create a matplotlib figure
    fig, ax = plt.subplots()

    # Draw the graph
    pos = nx.spring_layout(graph)
    nx.draw(graph, pos, with_labels=True, ax=ax)

    # Draw the Eulerian circuit
    edge_colors = ['black' if edge in solution else 'red' for edge in graph.edges()]
    nx.draw_networkx_edges(graph, pos, edgelist=solution, edge_color=edge_colors, width=2, ax=ax)

    # Highlight the Eulerian circuit
    for u, v in solution:
        ax.annotate("",
                    xy=pos[v], xycoords='data',
                    xytext=pos[u], textcoords='data',
                    arrowprops=dict(arrowstyle="->", color="green",
                                    shrinkA=5, shrinkB=5,
                                    patchA=None, patchB=None,
                                    connectionstyle="arc3,rad=rrr".replace('rrr', str(random.random() * 0.5 - 0.25)),
                                    ),
                    )

    # Place the matplotlib figure in a Tkinter canvas
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    # Run the Tkinter loop
    tk.mainloop()


def main():
    # File selection dialog
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    filename = filedialog.askopenfilename(title="Select a .txt file for CPP", filetypes=[("Text files", "*.txt")])
    root.destroy()

    if filename:
        graph = read_txt_file_to_graph(filename)

        # Process the graph to find odd degree vertices and make the graph Eulerian
        odd_vertices = find_odd_degree_vertices(graph)
        eulerian_graph = add_edges_to_make_eulerian(graph, odd_vertices)

        # Run the genetic algorithm to find the best Eulerian circuit
        best_circuit, best_fitness = genetic_algorithm(eulerian_graph, pop_size=100, num_generations=1000, mutation_rate=0.05)

        # Visualize the best solution found
        visualize_cpp_solution(best_circuit, eulerian_graph)

        # Output the best solution details
        print(f"Best fitness: {best_fitness}")
        print(f"Best Eulerian circuit: {best_circuit}")

# Ensure the script can be run directly
if __name__ == "__main__":
    main()
