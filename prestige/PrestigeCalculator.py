import numpy as np


class PrestigeCalculator:
    @staticmethod
    def normalize_matrix(matrix):
        result = []
        for row in matrix:
            row_sum = sum(row)
            normalized_row = [element/row_sum if row_sum != 0 else 0 for element in row]
            result.append(normalized_row)
        return np.array(result)

    @staticmethod
    def poweriteration(matrix, websites):
        transposed_matrix = np.transpose(matrix)
        eigenvalues, eigenvectors = np.linalg.eig(transposed_matrix)

        index_of_max_eigenvalue = np.argmax(eigenvalues)
        max_eigenvector = eigenvectors[:, index_of_max_eigenvalue]

        prestige_values = np.abs(np.real(max_eigenvector))
        prestige_dict = {website: f"Poweriteration: {prestige_values[i]}" for i, website in enumerate(websites)}

        return prestige_dict
    @staticmethod
    def pagerank(matrix, websites):
        matrix1 = PrestigeCalculator.normalize_matrix(matrix)
        transposed_matrix = np.transpose(matrix1)
        eigenvalues, eigenvectors = np.linalg.eig(transposed_matrix)

        index_of_max_eigenvalue = np.argmax(eigenvalues)
        max_eigenvector = eigenvectors[:, index_of_max_eigenvalue]

        ranks_ev = max_eigenvector / max_eigenvector.sum()
        ranks_ev = np.nan_to_num(ranks_ev, nan=0)
        prestige_values = np.real(ranks_ev)
        prestige_dict = {website: f"Pagerank: {prestige_values[i]}" for i, website in enumerate(websites)}

        return prestige_dict
    
