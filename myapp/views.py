from django.shortcuts import render

from django.http import Http404


from .analysis import plot_containers_11

import myapp

def dashboard(request):
    return render(request,"myapp/dashboard.html",{"plots": plot_containers_11})

def project_report(request):
    return render(request, "myapp/report.html")

def graph_detail(request, graph_id):
    if graph_id < 0 or graph_id >= len(plot_containers_11):
        raise Http404("Graph Not Found")
    plot = plot_containers_11[graph_id]
    return render(request, "myapp/graph_id.html", {"plot":plot})