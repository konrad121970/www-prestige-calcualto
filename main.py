import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import filedialog, scrolledtext
from prestige.incidence_list_reader import IncidenceListReader
from prestige.pageRank import PageRankCalculator


class MainApplication:
    def __init__(self, root):
        self.G = nx.DiGraph()
        # Incidence Text
        self.incidence_text = tk.Text(root, height=5, width=50)
        self.incidence_text.grid(row=0, column=0, padx=10, pady=10)

        # Calculate PageRank Button
        self.page_rank_button = tk.Button(root, text="Calculate PageRank", command=self.calculate_pagerank)
        self.page_rank_button.grid(row=0, column=1, padx=10, pady=10)

        # Save Matrix to CSV Button
        self.save_csv_button = tk.Button(root, text="Save Matrix to CSV", command=self.save_matrix_to_csv)
        self.save_csv_button.grid(row=1, column=1, padx=10, pady=10)

        # Update Graph and Matrix Button
        self.update_button = tk.Button(root, text="Update Graph and Matrix", command=self.update_graph_and_matrix)
        self.update_button.grid(row=1, column=0, pady=5, padx=5)

        # Load from File Button
        self.load_button = tk.Button(root, text="Load from File", command=self.load_file)
        self.load_button.grid(row=2, column=0, pady=5, padx=5)

        # Matplotlib Plot
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        # Adjacency Text
        self.adjacency_text = tk.Text(root, height=20, width=40)
        self.adjacency_text.grid(row=3, column=2, padx=10, pady=10)
        self.adjacency_text.bind("<KeyRelease>", self.on_text_edit)

        # Bind KeyRelease Event for Incidence Text
        self.incidence_text.bind("<KeyRelease>", self.on_text_edit)

    def calculate_pagerank(self):
        adjacency_matrix = nx.linalg.graphmatrix.adjacency_matrix(self.G).todense()
        node_names = list(self.G.nodes)
        page_rank_calculator = PageRankCalculator(adjacency_matrix, node_names)
        pagerank = page_rank_calculator.calculate_pagerank()

        # Create a new window for displaying PageRank results
        rank_window = tk.Toplevel(root)
        rank_window.title("PageRank Results")

        # Create a scrolled text widget for displaying results
        result_text = scrolledtext.ScrolledText(rank_window, width=30, height=10)
        result_text.grid(row=0, column=0, padx=10, pady=10)

        # Display the ranked pages
        result_str = "Ranked Pages:\n"
        for i, (page_name, prestige) in enumerate(pagerank):
            result_str += f"{i + 1}. {page_name} (Prestige: {prestige:.4f})\n"

        result_text.insert(tk.END, result_str)

    def update_graph(self):
        incidents = IncidenceListReader.read_incidents_from_text_widget(self.incidence_text, tk)

        # Update DataFrame
        df = pd.DataFrame(incidents, columns=['source', 'target'])

        # Update directed graph from data
        self.G.clear()
        self.G.add_edges_from(
            [(row.source, target) for row in df.itertuples(index=False) for target in row.target if target])

        # Update Matplotlib plot
        pos = nx.spring_layout(self.G)
        self.ax.clear()
        nx.draw(self.G, pos, with_labels=True, arrowsize=20, node_size=700, node_color="skyblue",
                font_size=10, font_color="black", font_weight="bold", font_family="sans-serif")
        plt.title("Graph based on DataFrame")
        self.canvas.draw()

    def update_matrix(self):
        # Update Text widget with adjacency matrix
        adjacency_matrix = nx.linalg.graphmatrix.adjacency_matrix(self.G).todense()
        self.adjacency_text.delete(1.0, tk.END)
        self.adjacency_text.insert(tk.END, str(adjacency_matrix))

    def update_graph_and_matrix(self):
        self.update_graph()
        self.update_matrix()

    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            incidents = IncidenceListReader.read_incidents_from_file(file_path)
            self.incidence_text.delete(1.0, tk.END)
            self.incidence_text.insert(tk.END, "\n".join([f"{item[0]}: {', '.join(item[1])}" for item in incidents]))
            self.update_graph_and_matrix()

    def save_matrix_to_csv(self):
        adjacency_matrix = nx.linalg.graphmatrix.adjacency_matrix(self.G).todense()
        node_names = list(self.G.nodes)
        df = pd.DataFrame(adjacency_matrix, index=node_names, columns=node_names)
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])

        if file_path:
            df.to_csv(file_path)
            print(f"Adjacency matrix saved to: {file_path}")


    def on_text_edit(self, event):
        self.update_graph_and_matrix()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Graph and Adjacency Matrix Viewer")
    root.geometry("1200x600")

    app = MainApplication(root)

    root.mainloop()
