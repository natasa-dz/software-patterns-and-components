import os

from django.apps import AppConfig
import pkg_resources


class CoreConfig(AppConfig):
    name = 'core'
    verbose_name = 'Root of whole app for graph visualization'
    visualizers: []
    loaders: []
    data = []
    #kad pritisnem isparsiram neki fajl, onda ovde mogu da upisem instancu grafa koji je trenutno kreiran
    def ready(self):
        self.data = load_files_from_directory("D:\\FAKS\\SOFT. OBRASCI I KOMPONENTE\\Projekat 2023\\Software-patterns-and-components\\data")
        self.visualizers = load_visualizers()
        self.loaders = load_loaders()

def load_visualizers():
    oznaka = "plugin.visualizators"
    visualizators = load_plugins(oznaka)
    return visualizators

def load_loaders():
    oznaka = "plugin.loaders"
    loaders = load_plugins(oznaka)
    return loaders

def load_plugins(identifier):
    list_to_load = []
    for ep in pkg_resources.iter_entry_points(group=identifier):
        p = ep.load()
        plugin = p()
        list_to_load.append(plugin)
    return list_to_load


def load_files_from_directory(directory_path):
    try:
        # List all files in the directory
        files = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]
        return files
    except OSError as e:
        print(f"Error: {e}")
        return []
