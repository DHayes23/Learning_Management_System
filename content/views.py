from django.shortcuts import render, get_object_or_404
from .models import Path

def path_detail(request, pk):
    path = get_object_or_404(Path, pk=pk)
    return render(request, 'content/path_detail.html', {'path': path})
