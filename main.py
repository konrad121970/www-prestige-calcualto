import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import filedialog
from incidence_list_reader import IncidenceListReader

class MainApplication:
    def __init__(self, root):
        self.G = nx.DiGraph()

        self.incidence_text = tk.Text(root, height=5, width=50)
        self.incidence_text.grid(row=0, column=0, padx=10, pady=10)

        self.update_button = tk.Button(root, text="Update Graph and Matrix", command=self.update_graph_and_matrix)
        self.update_button.grid(row=1, column=0, pady=5, padx=5)

        self.load_button = tk.Button(root, text="Load from File", command=self.load_file)
        self.load_button.grid(row=2, column=0, pady=5, padx=5)

        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.grid(row=3, column=0, padx=10, pady=10)

        self.adjacency_text = tk.Text(root, height=20, width=40)
        self.adjacency_text.grid(row=3, column=2, padx=10, pady=10)

        self.incidence_text.bind("<KeyRelease>", self.on_text_edit)

    def update_graph(self):
        incidents = IncidenceListReader.read_incidents_from_text_widget(self.incidence_text, tk)

        # Update DataFrame
        df = pd.DataFrame(incidents, columns=['source', 'target'])

        # Update directed graph from data
        self.G.clear()
        self.G.add_edges_from([(row.source, target) for row in df.itertuples(index=False) for target in row.target if target])

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

    def on_text_edit(self, event):
        self.update_graph_and_matrix()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Graph and Adjacency Matrix Viewer")
    root.geometry("1200x600")

    app = MainApplication(root)

    root.mainloop()
