import re
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
        self.create_nodes(tree)
        return self._graph




if __name__ == '__main__':
    loader = JSONGraphLoader()
    with open("/Users/uros/Software-patterns-and-components/data/test2.json") as file:
        data = loader.load(file)
    graph = loader.create_graph(data)
    graph.print_graph()
#    loader.display_graph(graph)
