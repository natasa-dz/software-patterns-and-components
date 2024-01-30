from typing import Dict, Any
from core.models import Vertex, Edge, Graph
import json

#TODO: Edge creation and bidirectional check?!
class JSONGraphLoader:
    def __init__(self):
        self._id_counter = 0
        self._key = "id"
        self._graph = None

    def get_identifier(self):
        return "JSONGraphLoader"

    def get_name(self):
        return "JSON Graph Loader"

    def load_data_from_file(self, file, unique_key="id"):
        if unique_key:
            self._key = unique_key
        json_object = json.load(file)
        return json_object

    #TODO: Dodaj metodu za kreiranje edges-a!
    def create_graph(self, tree):
        self._graph = Graph()
        self.create_vertices(tree)
        return self._graph

    def create_vertices(self, data, parent_vertex=None, relationship=None):
        current_vertex = Vertex(data)
        current_vertex.id = self.set_vertex_id(data)
        if parent_vertex:
            self.add_edge(current_vertex, parent_vertex, relationship)

        for nested_item, nested_value in data.items():
            if isinstance(nested_value, dict):
                nested_vertex = self.create_vertices(nested_value, current_vertex, nested_item)
                self.alter_existing_vertex(nested_vertex)
            else:
                current_vertex.add_attribute(nested_item, nested_value)

        self.alter_existing_vertex(current_vertex)
        return current_vertex

    def add_edge(self, child_vertex, parent_vertex, relationship):
        e = Edge(parent_vertex.get_id(), child_vertex.get_id(), relationship, 0, True)
        parent_vertex.add_edge(e)

    def alter_existing_vertex(self, vertex):
        already_in_graph = self._graph.get_vertex(vertex.id)
        if already_in_graph:
            vertex.attributes.update(already_in_graph.attributes)
        self._graph.add_vertex(vertex)

    def set_vertex_id(self, vertex_data=None):
        if vertex_data and self._key in vertex_data:
            vertex_id = vertex_data[self._key]
        else:
            vertex_id = self.generate_id()
        return vertex_id

    def generate_id(self):
        current_id = self._id_counter
        self._id_counter += 1
        return current_id



if __name__ == '__main__':
    loader = JSONGraphLoader()
    with open("C://SIIT//SIIT-treca godina//Zimski semestar//Softverski obrasci i komponente//Software-patterns-and-components//data//test2.json") as file:
        data = loader.load_data_from_file(file)
    graph = loader.create_graph(data)
