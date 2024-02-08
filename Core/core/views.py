import os
from datetime import time
import pkg_resources
from django.apps import apps
from django.http import JsonResponse
from django.shortcuts import render
from plugin.loader.rdf_loader import RdfParser
#from plugin.xml_loader.loader import XmlLoader



def index(request):
    title = apps.get_app_config('core').verbose_name
    return render(request, 'index.html', {'title': title})


def base(request):
    title = apps.get_app_config('core').verbose_name
    files = apps.get_app_config('core').data
    visualizers = apps.get_app_config('core').visualizers
    loaders = apps.get_app_config('core').loaders
    print("Outgoing loaders: ", loaders)
    print("Outgoing visualizers: ", visualizers)
    print("[Debug] files that are going to html: ", files)
    return render(request, 'base.html', {'title': title, 'data': files, 'visualizers': visualizers, 'loaders': loaders})


def get_visualizer(visualizer_name):
    visualizers = apps.get_app_config('core').visualizers
    for v in visualizers:
        if v.name == visualizer_name:
            return v
    return None


def get_loader(loader_name):
    loaders = apps.get_app_config('core').loaders
    for l in loaders:
        if l.name == loader_name:
            return l
    return None


def get_graph(loader, file_name):

    if are_parser_and_file_type_matching(loader, file_name):
        if loader.name == "RdfGraphLoading":
            parser = RdfParser()
            parser.load_from_file(file_name)
            return parser.create_graph()

        #TODO: dodaj kada je xmlLoader
        # else:
        #     parser = XmlLoader()
    return None




def simple_visualization(request):
    if request.method == 'POST':

        visualizer = get_visualizer("Simple Visualizer")
        loader_name = request.POST.get('loader')
        loader = get_loader(loader_name)
        file_name = request.POST.get('file')
        print("---------------- SIMPLE VISUALIZATION ------------------------")
        print('VISUALIZER: ', visualizer)
        print('LOADER: ', loader)
        print('FILE NAME: ', file_name)

        graph = get_graph(loader, file_name)

        # Render the visualization
        if visualizer and graph:
            # Assuming 'visualizer.visualize' returns the visualization data
            visualization_data = visualizer.visualize(graph, request)
            print("Visualization data rendered! " )
            return JsonResponse({'visualization_data': visualization_data})

    # Handle invalid requests or errors
    return JsonResponse({'error': 'Invalid request'})


def are_parser_and_file_type_matching(loader, file):
    print("File extension loader: ", loader.name)
    print("File extension name: ", file.name)
    if loader.name == "RdfGraphLoading" and file.name.endswith('.nt'):
        return True
    elif file.name.endswith('.xml') and loader.name == "":
        return True

    return False


def complex_visualization(request):
    visualizers = apps.get_app_config('core').visualizers
    graph = apps.get_app_config('core').current_graph

    graph_missing = False
    if graph is None:
        graph_missing = True
    else:
        path = os.path.abspath(os.path.join(
            os.path.dirname(__file__), "templates", "mainView.html"))

        for visualizer in visualizers:
            if visualizer.identifier() == "complex-visualizer":
                apps.get_app_config(
                    'core').current_visualizer = "ComplexVisualizer"
                with open(path, 'w') as file:
                    file.write(visualizer.visualize(graph, request))

    visualizers = []
    for visualizer in apps.get_app_config('core').visualizers:
        visualizers.append({"name": visualizer.name(), "identifier": visualizer.identifier()})
    loaders = []
    for loader in apps.get_app_config('core').loaders:
        loaders.append({"name": loader.name(), "identifier": loader.identifier()})
    graph = apps.get_app_config('core').current_graph
    tree = apps.get_app_config('core').tree
    return render(request, "index.html", {'graph': graph, 'tree': tree, 'visualizers': visualizers, 'loaders': loaders,
                                          "graph_missing": graph_missing})
