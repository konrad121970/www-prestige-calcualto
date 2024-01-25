import numpy as np

class PageRankCalculator:
    def __init__(self, adjacency_matrix, node_names):
        self.adjacency_matrix = adjacency_matrix
        self.num_pages = adjacency_matrix.shape[0]
        self.node_names = node_names

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

        # Zwróć PageRank razem z prawdziwymi nazwami stron
        page_rank_with_names = [(self.node_names[i], pagerank[i]) for i in range(self.num_pages)]
        page_rank_with_names.sort(key=lambda x: x[1], reverse=True)  # Sortuj malejąco wg PageRank
        return page_rank_with_names

# Przykładowa macierz sąsiedztwa (graf skierowany)
adjacency_matrix = np.array([
    [0, 1, 1, 0],
    [0, 0, 1, 1],
    [1, 0, 0, 0],
    [0, 1, 0, 0],
], dtype=float)

# Prawdziwe nazwy stron
node_names = ["strona A", "strona B", "strona C", "strona D"]

# Stworzenie instancji kalkulatora PageRank
pagerank_calculator = PageRankCalculator(adjacency_matrix, node_names)

# Obliczenie PageRank
pagerank_with_names = pagerank_calculator.calculate_pagerank()

# Wyświetlenie wyników
print("PageRank with names:", pagerank_with_names)
