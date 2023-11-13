import random
import pandas as pd

def generate_adjacency_matrix(num_nodes, max_edge_weight=10):
    matrix = [[0] * num_nodes for _ in range(num_nodes)]
    for i in range(num_nodes-1):
        weight = random.randint(1, max_edge_weight)
        matrix[i][i+1] = matrix[i+1][i] = weight
    matrix[num_nodes-1][0] = matrix[0][num_nodes-1] = random.randint(1, max_edge_weight)
    for i in range(num_nodes):
        for j in range(i+1, num_nodes):
            if matrix[i][j] == 0:
                if random.choice([True, False]):
                    weight = random.randint(1, max_edge_weight)
                    matrix[i][j] = matrix[j][i] = weight
    return matrix

def print_matrix(matrix):
    df = pd.DataFrame(matrix)
    df.columns = [chr(65+i) for i in range(len(matrix))]
    df.index = [chr(65+i) for i in range(len(matrix))]
    print(df)

def save_matrix_to_csv(matrix, filename):
    df = pd.DataFrame(matrix)
    df.columns = [chr(65+i) for i in range(len(matrix))]
    df.index = [chr(65+i) for i in range(len(matrix))]
    df.to_csv(filename)
    print(f"Matrix saved to {filename}")

def load_matrix_from_csv(filename):
    df = pd.read_csv(filename, index_col=0)
    return df.values.tolist()

# Parameters
num_nodes = 8  # Number of nodes in the graph
max_edge_weight = 120  # Maximum weight for the edges
filename = "adjacency_matrix.csv02"  # Filename to save the adjacency matrix

# Generate the adjacency matrix
matrix = generate_adjacency_matrix(num_nodes, max_edge_weight)

# Print the matrix
print_matrix(matrix)

# Save the matrix to a CSV file
save_matrix_to_csv(matrix, filename)

# Load and print the matrix to verify it's the same
loaded_matrix = load_matrix_from_csv(filename)
print("\nLoaded matrix:")
print(loaded_matrix)
