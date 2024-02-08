from abc import ABC

from rdflib import URIRef, RDF, RDFS, BNode, OWL, Graph as RdfGraph
from core.models import Graph as CoreGraph, Vertex, Edge

from core.services.loading import LoadingService

class RdfParser(LoadingService, ABC):

    def __init__(self):
        self.rdf_graph = None
        self.vertices = {}
        self.edges = set()

    def load(self, file_path):
        self.load_from_file(file_path)

    def name(self):
        return "RDF Data Loading"

    def id(self):
        return 1

    def load_from_file(self, file_path, format="turtle"):
        self.rdf_graph = RdfGraph()
        self.rdf_graph.parse(file_path, format=format)

    def create_graph(self):
        core_graph = CoreGraph()
        for subject, predicate, obj in self.rdf_graph:
            self.process_subject(subject, predicate, obj, core_graph)
        self.add_vertex_edges(core_graph)  # Add edges to vertices

        return core_graph

    def process_subject(self, subject, predicate, obj, core_graph, parent_label=None):
        start_vertex = self.create_or_get_vertex(subject, core_graph)
        end_vertex = self.create_or_get_vertex(obj, core_graph)

        if start_vertex and end_vertex and start_vertex != end_vertex:
            # If neither start nor end vertex is a blank node and they are not the same, create an edge
            edge_label = str(predicate) if predicate else None
            core_graph.edges.append(Edge(start_vertex, end_vertex, label=edge_label))


        if isinstance(obj, BNode):
            # If the object is a blank node, process the nested structure
            self.process_nested_structure(obj, core_graph, end_vertex, parent_label)

    def process_nested_structure(self, blank_node, core_graph, parent_vertex, parent_label):
        # Recursive function to process nested structure
        nested_objects = list(self.rdf_graph.predicate_objects(blank_node))
        for nested_predicate, nested_subject in nested_objects:
            nested_end_vertex = self.create_or_get_vertex(nested_subject, core_graph)
            # Only create an edge if both start and end vertices exist, and the predicate is not rdf:type
            if parent_vertex and nested_end_vertex and nested_predicate != RDF.type:
                edge_label = f"{parent_label} - {nested_predicate}" if parent_label else str(nested_predicate)
                core_graph.edges.append(Edge(parent_vertex, nested_end_vertex, label=edge_label))
                parent_vertex.add_edge(Edge(parent_vertex, nested_end_vertex, label=edge_label))  # Add edge to parent vertex

                # Recursively process nested structures
                self.process_subject(nested_subject, None, nested_subject, core_graph, parent_label=edge_label)

    def create_or_get_vertex(self, identifier, core_graph):
        if not isinstance(identifier, BNode):
            # Skip blank nodes
            if identifier not in core_graph.vertices:
                new_vertex = Vertex(id=identifier)
                core_graph.vertices[identifier] = new_vertex
                return new_vertex
            else:
                return core_graph.vertices[identifier]
        return None

    def count_nodes_and_edges(self, core_graph):
        node_count = len(core_graph.vertices)
        edge_count = len(core_graph.edges)
        return node_count, edge_count

    def add_vertex_edges(self, core_graph):
        # Add edges to vertices based on relationships in the graph
        for edge in core_graph.edges:
            edge.start.add_edge(edge)

if __name__ == '__main__':
    rdf_parser = RdfParser()
    rdf_parser.load_from_file("C://SIIT//SIIT-treca godina//Zimski semestar//Softverski obrasci i komponente//Software-patterns-and-components//data//cyclicRDF200Nodes.nt")
    parsed_graph = rdf_parser.create_graph()
    rdf_nodes, rdf_edges=rdf_parser.count_nodes_and_edges(parsed_graph)
    # print("Counted nodes: ", rdf_nodes)
    # print("Counted edges:", rdf_edges)


    # Iterate over the parsed graph's vertices
    print("\nVertices with edges:")
    for vertex_id, vertex in parsed_graph.vertices.items():
        print(f"Vertex ID: {vertex_id}")
        print("Edges:")
        for edge in vertex.edges:
            print(f"Start: {edge.start.id}, End: {edge.end.id}, Label: {edge.label}")


