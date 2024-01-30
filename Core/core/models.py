from typing import Dict, Any


class Vertex:   #declaration that id must be typeof int!!!!
    def __init__(self, attributes: Dict[str, Any]):
        self.attributes = attributes

    def get_id(self) -> int:
        return self.attributes['id']


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

class Graph:
    def __init__(self):
        self.vertices = {}
        self.edges = {}

    def add_vertex(self, data: Dict[str, Any]):
        new_vertex = Vertex(data)
        self.vertices[new_vertex.get_id()] = new_vertex
        return new_vertex

    def get_vertex(self, key):
        return self.vertices.get(key)

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
