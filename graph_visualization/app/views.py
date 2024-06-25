import os
import sys

from django.http import HttpResponse
from django.shortcuts import render

from django.views.decorators.csrf import csrf_exempt

from core.src.use_cases import tree_view
from core.src.use_cases.loader import Loader
from core.src.use_cases.main_view import MainWorkspace
from core.src.use_cases.tree_view import TreeView

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
sys.path.append(BASE_DIR)

loader = Loader()
# breakpoint()
loader.initialize_loader()
workspace_id = 1
source_id = -1
visualizer_id = -1

mainView = MainWorkspace()


def load_index_page(request):
    return render(request, 'index.html',
                  {"sources": loader.sources,
                   "visualizers": loader.visualizers,
                   'workspace_id': workspace_id})


def clear_search_filter_input(request):
    main_display = mainView.clear_filters(workspace_id)
    tree_view = TreeView(mainView.get_current_workspace_graph(workspace_id))
    return render(request, 'index.html',
                  {"visualization_html": main_display,
                   "source_id": source_id,
                   "visualizer_id": visualizer_id,
                   "sources": loader.sources,
                   "visualizers": loader.visualizers,
                   "tree_view_html": tree_view.generate_tree_view(),
                   "workspace_id": workspace_id})


def load_workspace(request, wsc_id: int):
    request.session['workspace_id'] = wsc_id  # Koristimo session za čuvanje workspace_id
    global workspace_id
    workspace_id = wsc_id

    if mainView.load_current_workspace(wsc_id):
        tree_view = TreeView(mainView.get_current_workspace_graph(wsc_id))
        main_workspace = mainView.get_workspace(wsc_id)
        return render(request, 'index.html',
                      {"visualization_html": mainView.show_workspace_graph(wsc_id),
                       "source_id": main_workspace.data_source_id,
                       "visualizer_id": main_workspace.visualizer_id,
                       "sources": loader.sources,
                       "visualizers": loader.visualizers,
                       "tree_view_html": tree_view.generate_tree_view(),
                       'workspace_id': wsc_id})
    else:
        return load_index_page(request)


@csrf_exempt
def render_graph(request):
    global workspace_id, source_id, visualizer_id
    visualizer_id = int(request.POST.get("visualizers"))
    source_id = int(request.POST.get("sources"))

    graph = loader.load_graph(source_id)
    tree_view = TreeView(graph)

    return render(request, 'index.html',
                  {"visualization_html": mainView.init(workspace_id, source_id, visualizer_id),
                           "sources": loader.sources,
                           "visualizers": loader.visualizers,
                           "tree_view_html": tree_view.generate_tree_view(),
                           'workspace_id': workspace_id})


@csrf_exempt
def search_filter_graph(request):
    global workspace_id, source_id, visualizer_id
    search_filter_word: str = str(request.POST.get("query"))
    main_display = mainView.search_filter(search_filter_word, workspace_id)
    graph = mainView.get_current_workspace_graph(workspace_id)
    tree_view = TreeView(graph)
    return render(request, 'index.html',
                  {"visualization_html": main_display,
                           "source_id": source_id,
                           "visualizer_id": visualizer_id,
                           "sources": loader.sources,
                           "visualizers": loader.visualizers,
                           "tree_view_html": tree_view.generate_tree_view(),
                           "workspace_id": workspace_id})
