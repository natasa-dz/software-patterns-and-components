import os
from datetime import time

import pkg_resources
from core.models import Forest
from django.apps import apps
from django.http import JsonResponse
from django.shortcuts import render

from plugin.loader.rdf_loader import RdfParser


from plugin.xml_loader.loader import XMLLoader

#TODO:Solve the problem with the edges!
def index(request):
    title = apps.get_app_config('core').verbose_name
    return render(request, 'index.html', {'title': title})


def base(request):
    title = apps.get_app_config('core').verbose_name
    files = apps.get_app_config('core').data
    visualizers = apps.get_app_config('core').visualizers
    loaders = apps.get_app_config('core').loaders
    # print("Outgoing loaders: ", loaders)
    # print("Outgoing visualizers: ", visualizers)
    # print("[Debug] files that are going to html: ", files)
    return render(request, 'base.html', {'title': title, 'data': files, 'visualizers': visualizers, 'loaders': loaders})


def get_visualizer(visualizer_name):
    visualizers = apps.get_app_config('core').visualizers
    for v in visualizers:
        print("V name: ", v.name)
        if v.name == visualizer_name:
            return v
    return None


def get_loader(loader_name):
    loaders = apps.get_app_config('core').loaders
    for l in loaders:
        print("L name: ", l.name)
        if l.name() == loader_name:
            return l
    return None


def get_graph(loader, file_name):
    if are_parser_and_file_type_matching(loader, file_name):
        if loader.name() == "RdfGraphLoading":
            parser = RdfParser()
            parser.load_from_file(file_name)
            graph = parser.create_graph()
            print("Number of edges: ", len(graph.edges))
            return graph
        else:
            parser = XMLLoader()
            root = parser.load(file_name)
            graph = parser.create_graph(root)
            return graph

    return None


def simple_visualization_data_processing(request):
    if request.method == 'POST':

        visualizer_name = request.POST.get('visualizer')
        visualizer = get_visualizer(visualizer_name)

        loader_name = request.POST.get('loader')
        loader = get_loader(loader_name)

        file_name = request.POST.get('file')
        file_path = "..//data/" + file_name

        print("---------------- SIMPLE VISUALIZATION ------------------------")
        graph = get_graph(loader, file_path)
        forest = Forest(graph)
        print("Graph edges from Graph itself: ")
        for e in graph.edges:
            print(e)
        print("-------------------------------------------------------------")
        for vertex_id, vertex in graph.vertices.items():
            print(f"Vertex ID: {vertex_id}")
        print("Edges:")
        for edge in graph.edges:
            print(f"Start: {edge.start.id}, End: {edge.end.id}, Label: {edge.label}")

        # Render the visualization
        if visualizer and graph:
            # Assuming 'visualizer.visualize' returns the visualization data
            visualization_data = visualizer.visualize(graph, request)
            print("Visualization data rendered! ")
            return JsonResponse({'visualization_data': visualization_data,
                                 'forest': forest.to_dict()})

    # Handle invalid requests or errors
    return JsonResponse({'error': 'Invalid request'})

# def parse_tree(request):
#     return render(request, 'tree.html')

def are_parser_and_file_type_matching(loader, file):
    if loader and file:
        if loader.name() == "RdfGraphLoading" and file.endswith('.nt'):
            print("Returned true")
            return True
        elif file.endswith('.xml') and loader.name() == "XML Loader":
            return True
    return False
