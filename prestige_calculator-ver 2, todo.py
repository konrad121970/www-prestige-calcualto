import numpy as np

class MatrixProcessor:
    def __init__(self, adjacency_matrix):
        self.adjacency_matrix = adjacency_matrix
        self.specific_column = None
        self.rows_with_ones = None

    def find_rows_with_ones(self, specific_column):
        self.specific_column = specific_column
        self.rows_with_ones = np.where(self.adjacency_matrix[:, self.specific_column] >0 )[0]
        print("Indices of rows with values 1 for column", self.specific_column, "are:", self.rows_with_ones)

    def process_rows_with_ones(self):
        prestige = 0
        while sum(self.rows_with_ones) != 0:
            for i in range(len(self.rows_with_ones)):
                if self.rows_with_ones[i] != 0:
                    for col_index in self.rows_with_ones:
                        value = self.adjacency_matrix[col_index, i]
                        print(f"Value at ({col_index}, {i}): {value}")
                    new_values = np.where(self.adjacency_matrix[:, self.rows_with_ones[i]] >0)[0]
                    
                
                    array1 = self.rows_with_ones[:i]
                    array2 = self.rows_with_ones[i + 1:]
                    self.rows_with_ones = np.concatenate((array1, new_values, array2))
                    print(self.rows_with_ones)

    def calculate_prestige(self, specific_column):

        self.find_rows_with_ones(specific_column)
        self.process_rows_with_ones()

        prestige = len(self.rows_with_ones)
        print("Prestige:", prestige)
        return prestige
# Funkcja do generowania nowej macierzy
    
def generate_new_matrix(matrix):
    new_matrix = np.zeros_like(matrix, dtype=float)
    
    # Iteracja po wierszach
    for i in range(matrix.shape[0]):
        # Suma jedynek w danym wierszu
        row_sum = np.sum(matrix[i])
        
        # Ustawienie wartości 1/x w miejscach jedynek
        if row_sum > 0:
            new_matrix[i] = matrix[i] / row_sum
    
    return new_matrix
matrix = np.array([
    [0, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0],
    [0, 1, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0]
], dtype=float)
# Generowanie nowej macierzy
result_matrix = generate_new_matrix(matrix)
print(result_matrix)
# Create a MatrixProcessor instance
processor = MatrixProcessor(result_matrix)

# Calculate prestige for a specific column
specific_column = 1
prestige = processor.calculate_prestige(specific_column)


