from typing import Dict, Any


class Vertex(object):
    _id_counter = 0

    def __init__(self, id: int=None):
        self._attributes = {}
        self._id = id
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

    def __eq__(self, other):
        if isinstance(other, Vertex):
            if self._attributes.keys() != other._attributes.keys():
                return False
            for attr in self._attributes:
                if self.attributes[attr] != other._attributes[attr]:
                    return False
        else:
            return False
        return True



class Edge:
    def __init__(self, start: int, end: int):
        self.start = start
        self.end = end

    def get_start(self) -> int:
        return self.start

    def get_end(self) -> int:
        return self.end

    def equals(self, other_edge) -> bool:
        return self.start == other_edge.get_start() and self.end == other_edge.get_end()

class Graph(object):
    def __init__(self):
        self.vertices: Dict[int, Vertex] = {}
        self.edges = {}

    def add_vertex(self, vertex: Vertex):
        if vertex not in self.vertices.values():
            self.vertices[vertex.id] = vertex
            return vertex

    def get_vertex(self, key):
        return self.vertices.get(key)

    def contains_vertex(self, attributes: Dict[str, Any]):
        for vertex in self.vertices.values():
            if vertex.attributes.keys() == attributes.keys() and vertex.attributes.values() == attributes.values():
                return True
        return False

    def add_edge(self, start: int, end: int):
        #note: these two if cases will not happen, but i put it here so i can then later move it to somewhere where i will check for these errors
        # if start not in self.vertices:
        #     raise ValueError(f"Vertex {start} not found in the graph. Please chech that the data is not corrupt")
        # if end not in self.vertices:
        #     raise ValueError(f"Vertex {end} not found in the graph. Please check that the data is not corrupt")

        if start in self.edges.keys():
            self.edges[start].append(Edge(start, end))
        else:
            self.edges[start] = []
            self.edges[start].append(Edge(start, end))

    def isBiDirectional(self, vertex1: Vertex, vertex2: Vertex):
        edge1 = Edge(vertex1.get_id(), vertex2.get_id())
        edge2 = Edge(vertex2.get_id(), vertex1.get_id())
        edgesFromStart = self.edges.get(vertex1.get_id())
        edgesFromEnd = self.edges.get(vertex2.get_id())

        for temp in edgesFromStart:
            if temp.equals(edge1):
                for temp2 in edgesFromEnd:
                    if temp2.equals(edge2):
                        return True
        return False

    def handle_duplicate(self, duplicate: Vertex):
        if duplicate in self.edges.keys():
            pass


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