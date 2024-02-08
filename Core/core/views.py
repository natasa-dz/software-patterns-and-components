import pkg_resources
from django.apps import apps
from django.shortcuts import render


def base(request):
    title = apps.get_app_config('core').verbose_name
    files = apps.get_app_config('core').data
    loaders = apps.get_app_config('core').loaders
    print("[Debug] files that are going to html: ", files)
    return render(request, 'base.html', {'title': title, 'data': files, 'loaders': loaders})


def parse(request):
    files = apps.get_app_config('core').data
    loaders = apps.get_app_config('core').loaders
    print("[Debug] uslo je u parse funkciju za tree!!!")
    return render(request, 'tree.html', {'data':files, 'loaders':loaders})


def index(request):
    print("[Debug] uslo je u parse funkciju za index!!!")
    return render(request, 'index.html', {})
