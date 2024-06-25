import os
import sys

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie

from django.views.decorators.csrf import csrf_exempt

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
    global source_id
    source_id = 0
    graph = loader.get_loaded_graph(source_id, "api_football_datasource")
    tree_view = TreeView(graph)
    return render(request, 'index.html', {
        "sources": loader.sources,
        "visualizers": loader.visualizers,
        "visualization_html": loader.visualizers[0].plugin.visualize(graph),
        "tree_view_html": tree_view.generate_tree_view()

    })
