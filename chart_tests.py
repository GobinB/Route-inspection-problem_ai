import random
import networkx as nx
import matplotlib.pyplot as plt
from finalsourceCode import genetic_algorithm
import time

def run_logic(population_size, generations, mutation_rate, num_nodes):
    matrix = [[0 for _ in range(num_nodes)] for _ in range(num_nodes)]

    for i in range(num_nodes):
        for j in range(i+1, num_nodes):
            weight = random.randint(1, num_nodes)
            matrix[i][j] = weight
            if True:
                matrix[j][i] = weight

    G = nx.Graph()
    for i, row in enumerate(matrix):
        for j, weight in enumerate(row):
            if weight != 0:
                G.add_edge(i, j, weight=weight)

    # Add missing edges with zero weights
    for i in range(len(matrix)):
        for j in range(i + 1, len(matrix)):
            if not G.has_edge(i, j):
                G.add_edge(i, j, weight=0)

    start_time = time.time()
    genetic_algorithm(G, population_size, generations, mutation_rate, False)
    execution_time = time.time() - start_time
    return execution_time

def node_test():
    num_nodes_list = list(range(2, 51))
    execution_times = []

    for num_nodes in num_nodes_list:
        execution_time = run_logic(population_size=100, generations=100, mutation_rate=0.5, num_nodes=num_nodes)
        execution_times.append(execution_time)

    plt.plot(num_nodes_list, execution_times)
    plt.ticklabel_format(style='plain')
    plt.xlabel('Number of Nodes')
    plt.ylabel('Runtime (seconds)')
    plt.title('Runtime vs Number of Nodes')
    plt.savefig('node_output.png', bbox_inches='tight')

def population_test():
    population_list = list(range(10, 536, 25))
    execution_times = []

    for population_size in population_list:
        execution_time = run_logic(population_size=population_size, generations=100, mutation_rate=0.5, num_nodes=10)
        execution_times.append(execution_time)

    plt.plot(population_list, execution_times)
    plt.ticklabel_format(style='plain')
    plt.xlabel('Population Size')
    plt.ylabel('Runtime (seconds)')
    plt.title('Runtime vs Population Size')
    plt.savefig('population_output.png', bbox_inches='tight')

def generation_test():
    generation_list = list(range(10, 536, 25))
    execution_times = []

    for generations in generation_list:
        execution_time = run_logic(population_size=100, generations=generations, mutation_rate=0.5, num_nodes=10)
        execution_times.append(execution_time)

    plt.plot(generation_list, execution_times)
    plt.ticklabel_format(style='plain')
    plt.xlabel('Number of Generations')
    plt.ylabel('Runtime (seconds)')
    plt.title('Runtime vs Number of Generations')
    plt.savefig('generation_output.png', bbox_inches='tight')

def mutation_rate_test():
    mutation_rate_list = [round(rate, 2) for rate in list((i+1)/20 for i in range(19))]
    execution_times = []

    for mutation_rate in mutation_rate_list:
        execution_time = run_logic(population_size=100, generations=100, mutation_rate=mutation_rate, num_nodes=10)
        execution_times.append(execution_time)

    plt.plot(mutation_rate_list, execution_times)
    plt.ticklabel_format(style='plain')
    plt.xlabel('Mutation Rate')
    plt.ylabel('Runtime (seconds)')
    plt.title('Runtime vs Mutation Rate')
    plt.savefig('mutation_output.png', bbox_inches='tight')

def clear_fig():
    plt.cla()
    plt.clf()

node_test()
clear_fig()
population_test()
clear_fig()
generation_test()
clear_fig()
mutation_rate_test()
clear_fig()