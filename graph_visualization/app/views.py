import os
import sys

from django.http import HttpResponse
from django.shortcuts import render

from django.views.decorators.csrf import csrf_exempt

from core.src.use_cases import tree_view
from core.src.use_cases.loader import Loader
from core.src.use_cases.tree_view import TreeView

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
sys.path.append(BASE_DIR)

loader = Loader()
# breakpoint()
loader.initialize_loader()
source_id = -1
visualizer_id = -1
workspace_id = 1


def index(request):
    return render(request, 'index.html', {"sources": loader.sources,
                                          "visualizers": loader.visualizers})


@csrf_exempt
def generate(request):
    return render_new_graph(request)


def config(request):
    pass


def search(request):
    pass


def clear_filters(request):
    pass


def set_workspace(request, number: int):
    pass


def render_new_graph(request):
    global workspace_id, source_id, visualizer_id
    visualizer_id = int(request.POST.get("visualizers"))
    source_id = int(request.POST.get("sources"))

    graph = loader.get_loaded_graph(source_id)
    tree_view = TreeView(graph)
    visualization_html = loader.visualizers[visualizer_id].plugin.visualize(graph)

    return render(request, 'index.html', {
        "sources": loader.sources,
        "visualizers": loader.visualizers,
        "visualization_html": visualization_html,
        "tree_view_html": tree_view.generate_tree_view()
    })
