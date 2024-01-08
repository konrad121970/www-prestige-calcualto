import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import filedialog

class IncidenceListReader:
    def __init__(self, file_path):
        self.file_path = file_path

    def read_incidents_from_file(self):
        with open(self.file_path, 'r') as file:
            incidents = [line.strip().split(':') for line in file]
        return [(left.strip(), [element.strip() for element in right.split(',')]) for left, right in incidents]

def update_graph_and_matrix():
    incidence_list = incidence_list_reader.read_incidents_from_file()

    # Update DataFrame
    df = pd.DataFrame(incidence_list, columns=['source', 'target'])

    # Update directed graph from data
    G.clear()
    G.add_edges_from([(row.source, target) for row in df.itertuples(index=False) for target in row.target if target])

    # Update Matplotlib plot
    pos = nx.spring_layout(G)
    ax.clear()
    nx.draw(G, pos, with_labels=True, arrowsize=20, node_size=700, node_color="skyblue",
            font_size=10, font_color="black", font_weight="bold", font_family="sans-serif")
    plt.title("Graph based on DataFrame")
    canvas.draw()

    # Update Text widget with adjacency matrix
    adjacency_matrix = nx.linalg.graphmatrix.adjacency_matrix(G).todense()
    adjacency_text.delete(1.0, tk.END)
    adjacency_text.insert(tk.END, str(adjacency_matrix))

def print_matrix_to_console():
    print("eh")

def load_incidence_list():
    incidence_list_path = filedialog.askopenfilename(title="Select Incidence List File", filetypes=[("Text files", "*.txt")])
    file_path_entry.delete(0, tk.END)
    file_path_entry.insert(0, incidence_list_path)
    incidence_list_reader.file_path = incidence_list_path
    update_graph_and_matrix()

# Create directed graph
G = nx.DiGraph()

# Create Tkinter window
root = tk.Tk()
root.title("Graph and Adjacency Matrix Viewer")
root.geometry("1200x600")

# Create Tkinter widgets
file_path_entry = tk.Entry(root, width=50)
file_path_entry.grid(row=0, column=0, padx=10, pady=10)

file_path_button = tk.Button(root, text="Load Incidence List", command=load_incidence_list)
file_path_button.grid(row=0, column=1, padx=10, pady=10)

update_button = tk.Button(root, text="Update Graph and Matrix", command=update_graph_and_matrix)
update_button.grid(row=1, column=0, columnspan=2, pady=10)

# Button to print matrix to console
print_matrix_button = tk.Button(root, text="Print Matrix to Console", command=print_matrix_to_console)
print_matrix_button.grid(row=1, column=1, padx=10, pady=10)

# Embed Matplotlib plot in Tkinter window
fig, ax = plt.subplots()
canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.grid(row=2, column=0, padx=10, pady=10)

# Text widget for displaying and editing adjacency matrix
adjacency_text = tk.Text(root, height=20, width=40)
adjacency_text.grid(row=2, column=1, padx=10, pady=10)

# Create incidence list reader instance
incidence_list_reader = IncidenceListReader("")

# Start the main event loop
root.mainloop()
