import tkinter as tk
from tkinter import ttk
import networkx as nx
import matplotlib.pyplot as plt

class Graph:
    def __init__(self, sommet):   
        self.S = sommet
        self.graph = []
        self.sommets = []

    def add_art(self, s, d, p):
        self.graph.append([s, d, p])

    def addSommet(self, valeur):
        self.sommets.append(valeur)

    def bellmanFord(self, src):
        dist = {i: float("Inf") for i in self.sommets}
        dist[src] = 0

        for _ in range(self.S - 1):
            for s, d, p in self.graph:
                if dist[s] != float("Inf") and dist[s] + p < dist[d]:
                    dist[d] = dist[s] + p

        for s, d, p in self.graph:
            if dist[s] != float("Inf") and dist[s] + p < dist[d]:
                return "Circuit absorbant"

        return f"Distances les plus courtes de la source à tous les sommets :\n{dist}"

    def visualize_graph(self):
        G = nx.DiGraph()

        for s, d, p in self.graph:
            G.add_edge(s, d, weight=p)

        pos = nx.spring_layout(G)
        labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_nodes(G, pos)
        nx.draw_networkx_edges(G, pos)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
        nx.draw_networkx_labels(G, pos)
        plt.title('Graph Visualization')
        plt.show()


g = None

def submit_button_click():
    global g
    vertices_value = vertices_entry.get()
    edges_value = edges_entry.get("1.0", tk.END)  

    vertices_list = vertices_value.split()
    edges_list = [tuple(edge.split()) for edge in edges_value.splitlines()]

    g = Graph(len(vertices_list))

    for vertex in vertices_list:
        g.addSommet(vertex)

    for edge in edges_list:
        g.add_art(edge[0], edge[1], int(edge[2]))

    result = g.bellmanFord(vertices_list[0])
    output_label.config(text=result)

def visualize_graph_button_click():
    if g is not None:
        g.visualize_graph()
    else:
        output_label.config(text="Créez d'abord un graphe.")

root = tk.Tk()
root.title("Bellman-Ford Algorithm")

vertices_label = ttk.Label(root, text="Sommets (séparés par des espaces):")
vertices_label.grid(row=0, column=0, padx=10, pady=10)
vertices_entry = ttk.Entry(root)
vertices_entry.grid(row=0, column=1, padx=10, pady=10)

edges_label = ttk.Label(root, text="Arêtes (une par ligne, format : 'source destination poids'):")
edges_label.grid(row=1, column=0, padx=10, pady=10)
edges_entry = tk.Text(root, height=5, width=30)
edges_entry.grid(row=1, column=1, padx=10, pady=10)

submit_button = ttk.Button(root, text="Exécuter Bellman-Ford", command=submit_button_click)
submit_button.grid(row=2, column=0, columnspan=2, pady=10)

visualize_button = ttk.Button(root, text="Visualiser le graphe", command=visualize_graph_button_click)
visualize_button.grid(row=3, column=0, columnspan=2, pady=10)

output_label = ttk.Label(root, text="")
output_label.grid(row=4, column=0, columnspan=2, pady=10)

root.mainloop()
