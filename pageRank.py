import numpy as np
class PageRankCalculator:
    def __init__(self, adjacency_matrix):
        self.adjacency_matrix = adjacency_matrix
        self.num_pages = adjacency_matrix.shape[0]

    def calculate_pagerank(self, damping_factor=0.85, epsilon=1e-8, max_iterations=100):
        # Inicjalizacja rankingu
        pagerank = np.ones(self.num_pages) / self.num_pages

        for _ in range(max_iterations):
            prev_pagerank = pagerank.copy()

            # Obliczenia nowego rankingu
            for i in range(self.num_pages):
                incoming_links = np.where(self.adjacency_matrix[:, i] > 0)[0]
                pagerank[i] = (1 - damping_factor) / self.num_pages + \
                              damping_factor * np.sum(prev_pagerank[j] / np.sum(self.adjacency_matrix[j]) 
                                                      for j in incoming_links)

            # Warunek stopu
            if np.sum(np.abs(pagerank - prev_pagerank)) < epsilon:
                break

        return pagerank

# Przykładowa macierz sąsiedztwa (graf skierowany)
adjacency_matrix = np.array([
    [0, 1, 1, 0],
    [0, 0, 1, 1],
    [1, 0, 0, 0],
    [0, 1, 0, 0],
], dtype=float)

# Stworzenie instancji kalkulatora PageRank
pagerank_calculator = PageRankCalculator(adjacency_matrix)

# Obliczenie PageRank
pagerank = pagerank_calculator.calculate_pagerank()

# Wyświetlenie wyników
print("PageRank:", pagerank)