import numpy as np

class MatrixProcessor:
    def __init__(self, adjacency_matrix):
        self.adjacency_matrix = adjacency_matrix
        self.specific_column = None
        self.rows_with_ones = None

    def find_rows_with_ones(self, specific_column):
        self.specific_column = specific_column
        self.rows_with_ones = np.where(self.adjacency_matrix[:, self.specific_column] == 1)[0]
        print("Indices of rows with values 1 for column", self.specific_column, "are:", self.rows_with_ones)

    def process_rows_with_ones(self):
        while sum(self.rows_with_ones) != 0:
            for i in range(len(self.rows_with_ones)):
                if self.rows_with_ones[i] != 0:
                    new_values = np.where(self.adjacency_matrix[:, self.rows_with_ones[i]] == 1)[0]
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