from typing import Dict, Any


class Vertex:
    _id_counter = 0

    def __init__(self, id=None):
        self._attributes = {}
        self._id = id or self._generate_unique_id()
        self._edges = []

    @property
    def attributes(self):
        return self._attributes

    @attributes.setter
    def attributes(self, attributes):
        self._attributes = attributes

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @property
    def edges(self):
        return self._edges

    def degree(self):
        return len(self._edges)

    def add_attribute(self, key, value):
        self._attributes[key] = value

    def add_edge(self, e):
        already_existing = self.contains_edge(e)
        if already_existing:
            self._edges[self._edges.index(already_existing)] = e
        else:
            self._edges.append(e)

    def contains_edge(self, e):
        for edge in self._edges:
            if e == edge:
                return edge
        return None


    def get_adjacent_vertices(self):
        return [edge.get_end() for edge in self._edges]

    def get_outgoing_edges(self):
        return [edge for edge in self._edges]

    def get_incoming_edges(self):
        return [edge for edge in self._edges if edge.get_end() == self._id]

    def is_adjacent(self, other_vertex):
        return any(edge.get_end() == other_vertex.id for edge in self._edges)

    def is_outgoing_edge(self, edge):
        return edge in self._edges

    def is_incoming_edge(self, edge):
        return edge in self.get_incoming_edges()

    def _generate_unique_id(self):
        current_id = Vertex._id_counter
        Vertex._id_counter += 1
        return current_id


class Edge:
    def __init__(self, start: int, end: int):
        self.start = start
        self.end = end
        self.label=label


    def get_start(self) -> int:
        return self.start

    def get_end(self) -> int:
        return self.end

    def equals(self, other_edge) -> bool:
        return (
            self.start == other_edge.get_start()
            and self.end == other_edge.get_end()
        )

class Graph:
    def __init__(self):
        self.vertices = {}
        self.edges = []

    def add_vertex(self, vertex: 'Vertex'):
        self.vertices[vertex.id] = vertex
    def get_vertex(self, key):
        return self.vertices.get(key)

    def add_edge(self, start: int, end: int):
        # Check if the edge already exists
        if not any(edge.equals(Edge(start, end)) for edge in self.edges):
            self.edges.append(Edge(start, end))

    def add_bidirectional_edge(self, vertex1: Vertex, vertex2: Vertex):
        # Create an edge from vertex1 to vertex2
        self.add_edge(vertex1.id, vertex2.id)

        # Create a bidirectional edge
        self.add_edge(vertex2.id, vertex1.id)

    def isBiDirectional(self, vertex1: Vertex, vertex2: Vertex):
        edge1 = Edge(vertex1.id, vertex2.id)
        edge2 = Edge(vertex2.id, vertex1.id)

        return edge1 in self.edges and edge2 in self.edges


    def print_graph(self):
        print("Nodes:")
        for vertex_id, vertex in self.vertices.items():
            print(f"Node {vertex_id}: {vertex.attributes}")

        print("\nEdges:")
        for edge in self.edges:
            print(f"Edge: {edge.start} -> {edge.end}")

# # Example usage:
# graph = Graph()
#
# # Adding vertices
# graph.add_vertex("A")
# graph.add_vertex("B")
# graph.add_vertex("C")
#
# # Adding edges
# graph.add_edge("A", "B", 3)
# graph.add_edge("B", "C", 5)
# graph.add_edge("A", "C", 2)
#
# # Accessing vertices and edges
# print("Vertices:", graph.get_vertices())
# print("Edges:", [(edge.start, edge.end, edge.weight) for edge in graph.get_edges()])
