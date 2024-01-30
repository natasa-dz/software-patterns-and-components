import pkg_resources
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
