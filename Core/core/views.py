import os
from datetime import time

import pkg_resources
from core.models import Forest
from django.apps import apps
from django.http import JsonResponse
from django.shortcuts import render, redirect

from plugin.loader.rdf_loader import RdfParser

from core.models import Graph


from plugin.xml_loader.loader import XMLLoader

def index(request):
    title = apps.get_app_config('core').verbose_name
    return render(request, 'index.html', {'title': title})


def base(request):

    title = apps.get_app_config('core').verbose_name
    files = apps.get_app_config('core').data
    visualizers = apps.get_app_config('core').visualizers
    loaders = apps.get_app_config('core').loaders
    return render(request, 'base.html', {'title': title, 'data': files, 'visualizers': visualizers, 'loaders': loaders})


def get_visualizer(visualizer_name):
    global chosen_visualizer
    visualizers = apps.get_app_config('core').visualizers
    for v in visualizers:
        if v.name == visualizer_name:
            chosen_visualizer = v.name
            return v
    return None


def get_loader(loader_name):
    loaders = apps.get_app_config('core').loaders
    for l in loaders:
        print("L name: ", l.name)
        if l.name() == loader_name:
            return l
    return None


current_graph = None
chosen_visualizer = None


def get_graph(loader, file_name):
    global current_graph
    if are_parser_and_file_type_matching(loader, file_name):
        if loader.name() == "RdfGraphLoading":
            parser = RdfParser()
            parser.load_from_file(file_name)
            graph = parser.create_graph()
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
        graph = get_graph(loader, file_path)

        if file_path.endswith(".nt"):
            if visualizer and graph:
                # Assuming 'visualizer.visualize' returns the visualization data
                visualization_data = visualizer.visualize(graph, request)
                print("Visualization data rendered! ")
                return JsonResponse({'visualization_data': visualization_data})
        else:
            forest = Forest(graph)
            # Render the visualization
            if visualizer and graph:
                # Assuming 'visualizer.visualize' returns the visualization data
                visualization_data = visualizer.visualize(graph, request)
                print("Visualization data rendered! ")
                return JsonResponse({'visualization_data': visualization_data,
                                     'forest': forest.to_dict()})

    # Handle invalid requests or errors
    return JsonResponse({'error': 'Invalid request'})


def are_parser_and_file_type_matching(loader, file):
    if loader and file:
        if loader.name() == "RdfGraphLoading" and file.endswith('.nt'):
            print("Returned true")
            return True
        elif file.endswith('.xml') and loader.name() == "XML Loader":
            return True
    return False


def complex_visualization_data_processing(request):
    if request.method == 'POST':
        visualizer_name = request.POST.get('visualizer')
        visualizer = get_visualizer(visualizer_name)
        loader_name = request.POST.get('loader')
        loader = get_loader(loader_name)

        file_name = request.POST.get('file')
        file_path = "..//data/" + file_name

        graph = get_graph(loader, file_path)

        if file_path.endswith(".nt"):
            if visualizer and graph:
                # Assuming 'visualizer.visualize' returns the visualization data
                visualization_data = visualizer.visualize(graph, request)
                print("Visualization data rendered! ")
                return JsonResponse({'visualization_data': visualization_data})
        else:
            forest = Forest(graph)
            # Render the visualization
            if visualizer and graph:
                # Assuming 'visualizer.visualize' returns the visualization data
                visualization_data = visualizer.visualize(graph, request)
                print("Visualization data rendered! ")
                return JsonResponse({'visualization_data': visualization_data,
                                     'forest': forest.to_dict()})

    return JsonResponse({'error': 'Invalid request'})


def evaluate_query(node, attribute, operator, value):
    if attribute not in node.attributes:
        return False

    node_value = node.attributes[attribute]

    if operator == '==':
        return node_value == value
    elif operator == '!=':
        return node_value != value
    elif operator == '>':
        return node_value > value
    elif operator == '>=':
        return node_value >= value
    elif operator == '<':
        return node_value < value
    elif operator == '<=':
        return node_value <= value
    else:
        return False


def apply_query(request):
    global chosen_visualizer
    global current_graph
    if request.method == 'POST':
        query = request.POST.get('query')

        if query:
            try:
                attribute, operator, value = query.split(' ')
            except ValueError:
                return JsonResponse({'error': 'Invalid query format. Use format: attribute operator value'})

            filtered_vertices = {}
            filtered_edges = []

            for node_id, node in current_graph.vertices.items():
                if evaluate_query(node, attribute, operator, value):
                    filtered_vertices[node_id] = node

            # Collect edges associated with filtered vertices
            for edge in current_graph.edges:
                if edge.start.id in filtered_vertices and edge.end.id in filtered_vertices:
                    filtered_edges.append(edge)

            # Construct a new graph with filtered vertices and edges
            filtered_graph = Graph()
            filtered_graph.vertices = filtered_vertices
            filtered_graph.edges = filtered_edges
            current_graph = filtered_graph

            if chosen_visualizer == "Simple Visualizer":
                return simple_visualization_data_processing(request)
            # elif current_visualizer == "Complex Visualizer":
            #     return complex_visualization_data_processing(request, filtered_graph)
            else:
                return redirect('base')

    return JsonResponse({'error': 'Invalid request'})
