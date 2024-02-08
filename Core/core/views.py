import pkg_resources
import os
from django.apps import apps
from django.shortcuts import render


def index(request):
    title = apps.get_app_config('core').verbose_name
    return render(request, 'index.html', {'title': title})


def base(request):
    title = apps.get_app_config('core').verbose_name
    files = apps.get_app_config('core').data
    print("[Debug] files that are going to html: ", files)
    return render(request, 'base.html', {'title': title, 'data': files})


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
