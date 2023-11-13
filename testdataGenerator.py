import random

def generate_valid_cpp_graph(num_nodes, max_edge_weight=10):
    # Initialize an empty adjacency matrix
    matrix = [[0] * num_nodes for _ in range(num_nodes)]

    # Create a connected graph
    for i in range(num_nodes - 1):
        weight = random.randint(1, max_edge_weight)
        matrix[i][i + 1] = matrix[i + 1][i] = weight

    # Connect the last node to the first node to ensure connectivity
    matrix[num_nodes - 1][0] = matrix[0][num_nodes - 1] = random.randint(1, max_edge_weight)

    # Make sure all nodes have even degrees (except for the start and end nodes)
    for i in range(num_nodes):
        # Calculate the current degree of the node
        degree = sum(1 for j in range(num_nodes) if matrix[i][j] > 0)

        # If the degree is odd and the node is not the start or end node, connect it to another random node
        if degree % 2 == 1 and i != 0 and i != num_nodes - 1:
            j = random.randint(0, num_nodes - 1)
            while j == i or degree % 2 == 0:
                j = random.randint(0, num_nodes - 1)
            weight = random.randint(1, max_edge_weight)
            matrix[i][j] = matrix[j][i] = weight

    return matrix

def print_matrix(matrix):
    for row in matrix:
        print(" ".join(map(str, row)))

def save_matrix_to_txt(matrix, filename):
    with open(filename, 'w') as file:
        for row in matrix:
            file.write(" ".join(map(str, row)) + "\n")
    print(f"Matrix saved to {filename}")

# Parameters
num_nodes = 8  # Number of nodes in the graph
max_edge_weight = 120  # Maximum weight for the edges
filename = "test01.txt"  # Filename to save the adjacency matrix in .txt format

# Generate a valid CPP graph and adjacency matrix
matrix = generate_valid_cpp_graph(num_nodes, max_edge_weight)

# Print the matrix
print_matrix(matrix)

# Save the matrix to a .txt file
save_matrix_to_txt(matrix, filename)
