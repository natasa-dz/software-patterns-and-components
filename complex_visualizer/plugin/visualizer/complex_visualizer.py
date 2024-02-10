import json
from core.services.visualizing import VisualizingService
from django.template import engines


class ComplexVisualizer(VisualizingService):

    def id(self):
        return "Complex graph"

    @property
    def name(self):
        return "Complex Visualizer"

    def url(self):
        return 'complex_visualization_data_processing'

    def visualize(self, graph, request):
        vertices = {}
        edges = []
        for vertex_id, vertex in graph.vertices.items():
            attributes = "\n"
            for attribute in vertex.attributes.keys():
                attributes += attribute + ": " + str(vertex.attributes[attribute]) + "\n"
            vertices[vertex.id] = {
                "id": vertex_id,
                "attributes": attributes
            }

        for edge in graph.edges:
            current_edge = {
                "source": edge.start,
                "target": edge.end
            }
            edges.append(current_edge)

        visualization_data = {
            "nodes": list(vertices.values()),
            "edges": edges
        }
        return visualization_data
