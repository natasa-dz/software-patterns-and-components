import json
from Core.core.services.visualizing import VisualizingService
from django.template import engines


class ComplexVisualizer(VisualizingService):

    def id(self):
        return "Complex graph"

    def name(self):
        return "Complex Visualizer"

    def url(self):
        return 'complex_visualization_data_processing'

    def visualize(self, graph, request):
        vertices = {}
        edges = []
        for vertex in graph.vertices:
            attributes = []
            for attribute in vertex.attributes.keys():
                attributes.append(attribute + ": " + str(vertex.attributes[attribute]))
            vertices[vertex.id] = {
                "id": "Vertex " + str(vertex.id),
                "attributes": attributes
            }
            for edge in vertex.edges():
                current_edge = {
                    "start": edge.start.id,
                    "end": edge.end.id,
                    "label": edge.label if edge.label else "Edge"
                }
                edges.append(current_edge)

        visualization_data = {
            "nodes": list(vertices.values()),
            "edges": edges
        }
        return visualization_data
