from django.shortcuts import render, get_object_or_404
from .models import Path, Module

def path_detail(request, pk):
    path = get_object_or_404(Path, pk=pk)
    return render(request, 'content/path_detail.html', {'path': path})

def module_detail(request, pk):
    module = get_object_or_404(Module, pk=pk)
    lessons = module.lessons.all()
    return render(request, 'content/module_detail.html', {'module': module, 'lessons': lessons})
