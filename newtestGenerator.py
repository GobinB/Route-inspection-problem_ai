import random

def generate_test_data(num_nodes, max_weight, filename="test_04.txt", undirected=True):
    matrix = [[0 for _ in range(num_nodes)] for _ in range(num_nodes)]

    for i in range(num_nodes):
        for j in range(i+1, num_nodes):
            weight = random.randint(1, max_weight)
            matrix[i][j] = weight
            if undirected:
                matrix[j][i] = weight

    with open(filename, "w") as file:
        for row in matrix:
            file.write(" ".join(map(str, row)) + "\n")

    print(f"Test data generated and saved in {filename}")

num_nodes = 7  # Number of nodes in the graph
max_weight = 7  # Maximum weight of an edge

generate_test_data(num_nodes, max_weight)
