import colorsys
import numpy as np
import ast
import csv
import tkinter as tk
from tkinter import ttk, filedialog
import numpy as np
import networkx as nx

from prestige.InputProcessor import InputProcessor
from prestige.PrestigeCalculator import PrestigeCalculator


class GraphGUI:
    websites = None

    def __init__(self, master):
        self.websites = None
        self.master = master
        self.master.title("Graph Visualization and Incidence Matrix")
        self.master.geometry("800x600")

        self.text_input = tk.Text(self.master, height=10, width=60)
        self.text_input.grid(row=0, column=0, padx=10, pady=10)

        self.canvas = tk.Canvas(self.master, width=600, height=400, bg="white")
        self.canvas.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        self.load_button = tk.Button(self.master, text="Load from File", command=self.load_from_file)
        self.load_button.grid(row=1, column=1, pady=5, padx=5)

        self.poweriteration_button = tk.Button(self.master, text="Power Iteration Prestige", command=self.calculate_poweriteration_prestige)
        self.poweriteration_button.grid(row=2, column=0, pady=5, padx=5)

        self.pagerank_button = tk.Button(self.master, text="PageRank Prestige", command=self.calculate_pagerank_prestige)
        self.pagerank_button.grid(row=2, column=1, pady=5, padx=5)

        self.adjacency_text = tk.Text(root, height=20, width=40)
        self.adjacency_text.grid(row=3, column=2, padx=10, pady=10)

        self.prestige_window = tk.Toplevel(self.master)
        self.prestige_window.title("Prestige Values")
        self.prestige_window.geometry("400x300")

        self.prestige_text = tk.Text(self.prestige_window, height=10, width=40)
        self.prestige_text.pack(padx=10, pady=10)

        self.save_button = tk.Button(self.master, text="Save to CSV", command=self.save_to_csv)
        self.save_button.grid(row=2, column=2, pady=5, padx=5)

        self.process_button = tk.Button(self.master, text="Process Input", command=self.process_input)
        self.process_button.grid(row=1, column=0, pady=5, padx=5)
    def calculate_poweriteration_prestige(self):
        input_str = self.text_input.get("1.0", "end-1c")
        relationships_dict = InputProcessor.transform_input_to_dict(input_str)
        self.websites, matrix = self.create_adjacency_matrix(relationships_dict)
        array = np.array(matrix)
        prestige_dict = PrestigeCalculator.poweriteration(array, self.websites)
        self.display_prestige(prestige_dict)

    def calculate_pagerank_prestige(self):
        input_str = self.text_input.get("1.0", "end-1c")
        relationships_dict = InputProcessor.transform_input_to_dict(input_str)
        self.websites, matrix = self.create_adjacency_matrix(relationships_dict)
        array = np.array(matrix)
        A_normalized = PrestigeCalculator.normalize_matrix(array)
        prestige_dict = PrestigeCalculator.pagerank(A_normalized, self.websites)
        self.display_prestige(prestige_dict)

    def display_prestige(self, prestige_dict):

        self.prestige_text.delete(1.0, tk.END)
        sorted_prestige = sorted(prestige_dict.items(), key=lambda x: (x[1].split(":")[-1]), reverse=True)


        for website, prestige_info in sorted_prestige:
            prestige_value = float(prestige_info.split(":")[-1])
            formatted_prestige = "{:.3f}".format(prestige_value)
            self.prestige_text.insert(tk.END, f"{website}: {formatted_prestige}\n")

        input_str = self.text_input.get("1.0", "end-1c")
        relationships_dict = InputProcessor.transform_input_to_dict(input_str)
        websites, matrix = self.create_adjacency_matrix(relationships_dict)
        self.draw_graph(self.websites, matrix,sorted_prestige)
        self.prestige_window.deiconify()

    def save_to_csv(self):
        adjacency_matrix_str = self.adjacency_text.get("1.0", tk.END)

        adjacency_matrix = [ast.literal_eval(row) for row in adjacency_matrix_str.strip().split('\n')]

        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])

        if file_path:
            with open(file_path, 'w', newline='') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerows(adjacency_matrix)


    def process_input(self):
        input_str = self.text_input.get("1.0", "end-1c")
        relationships_dict = InputProcessor.transform_input_to_dict(input_str)

        websites, matrix = self.create_adjacency_matrix(relationships_dict)
        self.websites = websites

        self.adjacency_text.delete(1.0, tk.END)
        for row in matrix:
            self.adjacency_text.insert(tk.END, str(row) + "\n")

        self.draw_graph(websites, matrix)


    def load_from_file(self):
        file_path = filedialog.askopenfilename(title="Select File", filetypes=[("Text Files", "*.txt")])

        if file_path:
            with open(file_path, 'r') as file:
                incidence_list = file.read()

            self.text_input.delete(1.0, tk.END)
            self.text_input.insert(tk.END, incidence_list)

            self.process_input()


    def draw_graph(self, websites, matrix, pagerank_values=None):
        self.canvas.delete("all")

        G = nx.DiGraph()

        for website in websites:
            G.add_node(website)

        for i in range(len(websites)):
            for j in range(len(websites)):
                if matrix[i][j] == 1:
                    G.add_edge(websites[i], websites[j])

        pos = nx.spring_layout(G)

        node_radius = 20
        for website, (x, y) in pos.items():
            x = 300 + x * 200  
            y = 200 + y * 150 
            if(pagerank_values != None):
                pagerank_value = next((float(value.split(': ')[1]) for name, value in pagerank_values if name == website), 0.0)
                node_color = self.get_color_based_on_pagerank(pagerank_value)
                self.canvas.create_oval(x - node_radius, y - node_radius, x + node_radius, y + node_radius,
                                        fill=node_color)
                self.canvas.create_text(x, y, text=website)
            elif(pagerank_values ==None):
                node_color = "lightblue"
                self.canvas.create_oval(x - node_radius, y - node_radius, x + node_radius, y + node_radius,
                                        fill=node_color)
                self.canvas.create_text(x, y, text=website)

        for edge in G.edges():
            x1, y1 = pos[edge[0]]
            x2, y2 = pos[edge[1]]
            x1 = 300 + x1 * 200
            y1 = 200 + y1 * 150
            x2 = 300 + x2 * 200
            y2 = 200 + y2 * 150

            dx = x2 - x1
            dy = y2 - y1

            length = np.sqrt(dx ** 2 + dy ** 2)
            if length != 0:
                dx /= length
                dy /= length

            x1 += dx * node_radius
            y1 += dy * node_radius
            x2 -= dx * node_radius
            y2 -= dy * node_radius

            self.canvas.create_line(x1, y1, x2, y2, arrow=tk.LAST)


    def to_rgb(self, r, g, b):
        return int(r * 255), int(g * 255), int(b * 255)

    def get_color_based_on_pagerank(self, pagerank_value):
        
        red = 1-pagerank_value
        green = pagerank_value
        rgb_color = self.to_rgb(red, green, 0)
        return "#{:02x}{:02x}{:02x}".format(*rgb_color)

    def create_adjacency_matrix(self, relationships):
        websites = sorted(
            set(website for connection in relationships.values() for website in connection) | set(
                relationships.keys()))

        website_indices = {website: index for index, website in enumerate(websites)}
        matrix_size = len(websites)
        adjacency_matrix = [[0] * matrix_size for _ in range(matrix_size)]

        for source, targets in relationships.items():
            source_index = website_indices[source]
            for target in targets:
                target_index = website_indices[target]
                adjacency_matrix[source_index][target_index] = 1

        return websites, adjacency_matrix

root = tk.Tk()
app = GraphGUI(root)
root.mainloop()