from typing import Dict, Any
from Core.core.models import Vertex, Edge, Graph
import json
import networkx as nx
import matplotlib.pyplot as plt

from Core.core.services.loading import LoadingService


class JSONGraphLoader(LoadingService):
    def __init__(self):
        super().__init__()
        self._id_counter = 0
        self._key = "id"
        self._graph = Graph()
        self._last_created_vertex = None  # Add this line to initialize _last_created_vertex

    def name(self):  # Implement abstract method
        return "JsonGraphLoader"

    def id(self):  # Implement abstract method
        return 2

    def load(self, file, unique_key="id"):
        if unique_key:
            self._key = unique_key
        json_object = json.load(file)
        return json_object

    def create_graph(self, tree):
        self._graph = Graph()
        self.create_vertices(tree)
        return self._graph

    def create_vertices(self, data, parent_vertex=None):
        current_vertex = Vertex()

        # If 'id' is not present in the data, generate a unique ID
        if 'id' not in data:
            current_vertex.id = self.generate_id()
            current_vertex.add_attribute("id", current_vertex.id)
        else:
            current_vertex.id = data['id']

        # Connect to the parent vertex with a bidirectional edge
        if parent_vertex:
            print(f"Adding bidirectional edge between {parent_vertex.id} and {current_vertex.id}")
            self._graph.add_bidirectional_edge(parent_vertex, current_vertex)

        # Handle dictionaries
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, (dict, list)):
                    # If the value is a nested structure, recursively call create_vertices
                    nested_vertex = self.create_vertices(value, current_vertex)
                    self.alter_existing_vertex(nested_vertex)
                else:
                    # If the value is a leaf node, add it as an attribute
                    current_vertex.add_attribute(key, value)

        # Handle lists
        elif isinstance(data, list):
            for item in data:
                if isinstance(item, (dict, list)):
                    # If the item is a nested structure, recursively call create_vertices
                    nested_vertex = self.create_vertices(item, current_vertex)
                    self.alter_existing_vertex(nested_vertex)

        self.alter_existing_vertex(current_vertex)
        self._last_created_vertex = current_vertex
        return current_vertex

    def add_edge(self, child_vertex, parent_vertex):
        # Create an edge from parent to child
        e_parent_to_child = Edge(parent_vertex.id, child_vertex.id)
        parent_vertex.add_edge(e_parent_to_child)

        # Create a bidirectional edge
        e_child_to_parent = Edge(child_vertex.id, parent_vertex.id)
        child_vertex.add_edge(e_child_to_parent)

    def alter_existing_vertex(self, vertex):
        already_in_graph = self._graph.get_vertex(vertex.id)
        if already_in_graph:
            vertex.attributes.update(already_in_graph.attributes)
        self._graph.add_vertex(vertex)
    def generate_id(self):
        current_id = self._id_counter
        self._id_counter += 1
        return current_id

    def display_graph(self, graph):
        G = nx.Graph()

        # Add vertices to the graph
        for vertex_id, vertex in graph.vertices.items():
            G.add_node(vertex_id, **vertex.attributes)

        # Add edges to the graph
        for edge in graph.edges:
            G.add_edge(edge.start, edge.end)

        # Display the graph
        pos = nx.spring_layout(G)  # You can use different layout algorithms
        nx.draw(G, pos, with_labels=True)
        plt.show()

if __name__ == '__main__':
    loader = JSONGraphLoader()
    with open("C://SIIT//SIIT-treca godina//Zimski semestar//Softverski obrasci i komponente//Software-patterns-and-components//data//test2.json") as file:
        data = loader.load(file)
    graph = loader.create_graph(data)
    graph.print_graph()
#    loader.display_graph(graph)
