import copy
from typing import Dict, Any, List, Set


class Vertex:
    _id_counter = 0

    def __init__(self, id=None):
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

    @edges.setter
    def edges(self, edges):
        self._edges = edges

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

    @id.setter
    def id(self, id):
        self._id = id

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
    def __init__(self, start: int, end: int, label=None):
        self.start = start
        self.end = end
        self.label = label

    def get_start(self) -> int:
        return self.start

    def get_end(self) -> int:
        return self.end

    def equals(self, other_edge) -> bool:
        return (
                self.start == other_edge.get_start()
                and self.end == other_edge.get_end()
        )


class Graph(object):
    def __init__(self):
        self.vertices: Dict[int, Vertex] = {}
        self.edges = []

    def add_vertex(self, vertex: 'Vertex'):
        self.vertices[vertex.id] = vertex

    def get_vertex(self, key):
        return self.vertices.get(key)

    def contains_vertex(self, attributes: Dict[str, Any]):
        for vertex in self.vertices.values():
            if vertex.attributes.keys() == attributes.keys() and vertex.attributes.values() == attributes.values():
                return True
        return False

    def add_edge(self, start: int, end: int):
        # Check if the edge already exists
        if not any(edge.equals(Edge(start, end)) for edge in self.edges):
            self.edges.append(Edge(start, end))

    def add_bidirectional_edge(self, vertex1: Vertex, vertex2: Vertex):
        # Create an edge from vertex1 to vertex2
        self.add_edge(vertex1.id, vertex2.id)

        # Create a bidirectional edge
        self.add_edge(vertex2.id, vertex1.id)

    def add_bidirectional_edge(self, vertex1: Vertex, vertex2: Vertex):
        # Create an edge from vertex1 to vertex2
        self.add_edge(vertex1.id, vertex2.id)

        # Create a bidirectional edge
        self.add_edge(vertex2.id, vertex1.id)

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

    def print_graph(self):
        print("Nodes:")
        for vertex_id, vertex in self.vertices.items():
            print(f"Node {vertex_id}: {vertex.attributes}")

        print("\nEdges:")
        for edge in self.edges:
            print(f"Edge: {edge.start} -> {edge.end}")

    def handle_duplicate(self, duplicate: Vertex):
        if duplicate in self.edges.keys():
            pass


class Node(object):
    # class Vertex:
    # _id_counter = 0
    # def __init__(self, id=None):
    #     self._attributes = {}
    #     self._id = id or self._generate_unique_id()
    #     self._edges = []
    def __init__(self, vertex: Vertex, recursive=False):
        self.attributes = vertex.attributes
        self.id = vertex.id
        self.children = []
        self.recursive = recursive

    def add_child(self, child_node):
        self.children.append(child_node)


class Tree:
    list_of_vertices: List[Vertex]
    root: Node
    containing_node_ids: Set[int]

    def __init__(self, vertices_to_manage):
        self.list_of_vertices = vertices_to_manage
        self.containing_node_ids = set()
        self.create_from_graph()

    def create_from_graph(self):
        self.root = Node(self.list_of_vertices[0])

        current_vertex = self.list_of_vertices[0]
        self.remove_vertex_by_id(current_vertex.id)

        self.create_subtree(current_vertex.edges, self.root)

    def create_subtree(self, list_of_edges, parent_node):
        for edge in list_of_edges:
            if edge.end not in self.containing_node_ids:

                end_vertex = self.find_vertex_by_id(edge.get_end())
                # if end_vertex is None:  #this if is added for logic when having recursion
                #     child = Node(Vertex(edge.start), True)
                # else:
                child = Node(end_vertex)
                self.remove_vertex_by_id(child.id)

                parent_node.add_child(child)

                # if len(end_vertex.edges) != 0 and not child.recursive:
                if len(end_vertex.edges) != 0:
                    self.create_subtree(end_vertex.edges, child)
            else:
                child = Node(Vertex(edge.get_end()), True)
                parent_node.add_child(child)

    def find_vertex_by_id(self, lookup_id) -> Vertex:
        for vertex in self.list_of_vertices:
            if vertex.id == lookup_id:
                return vertex

    def remove_vertex_by_id(self, lookup_id):
        vertex_to_remove = self.find_vertex_by_id(lookup_id)
        self.list_of_vertices.remove(vertex_to_remove)
        self.containing_node_ids.add(vertex_to_remove.id)

    def add_node(self, node):
        if not self.root:
            self.root = node
        else:
            self.root.add_child(node)


class Forest:
    graph: Graph
    list_of_graph_vertices: List[Vertex]
    trees: List[Tree]

    def __init__(self, graph):
        self.trees = []
        self.graph = graph
        self.list_of_graph_vertices = list(copy.deepcopy(graph.vertices))
        self.create_forest()

    def create_forest(self):
        while len(self.list_of_graph_vertices) != 0:
            t = Tree(self.list_of_graph_vertices)
            self.add_tree(t)

    def add_tree(self, tree):
        self.trees.append(tree)

# # Example usage:
#
# # Create nodes with custom attributes
# node1 = Node({"name": "Node 1", "value": 10})
# node2 = Node({"name": "Node 2", "value": 20})
# node3 = Node({"name": "Node 3", "value": 30})
#
# # Create a tree and add nodes
# tree1 = Tree()
# tree1.add_node(node1)
# tree1.add_node(node2)
#
# # Create another tree and add nodes
# tree2 = Tree()
# tree2.add_node(node3)
#
# # Create a forest and add trees
# forest = Forest()
# forest.add_tree(tree1)
# forest.add_tree(tree2)


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
