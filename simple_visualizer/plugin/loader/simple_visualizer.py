import json
from django.template import *

from Core.core.services.visualizing import VisualizingService


class SimpleVisualizer(VisualizingService):

    def visualize(self, graph, request):
        vertices={}
        for v in graph.vertices:
            vertices[v.id]={
                "id":"ID_"+str(v.id)
            }
