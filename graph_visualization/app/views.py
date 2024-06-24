import os
import sys

from django.http import HttpResponse
from django.shortcuts import render

from core.src.use_cases.loader import Loader

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
sys.path.append(BASE_DIR)

loader = Loader()
loader.initialize_loader()
source_id = -1
visualizer_id = -1
workspace_id = 1


def index(request):
    return render(request, 'index.html', {"sources": loader.sources,
                                          "visualizers": loader.visualizers})

def generate(request):
    pass
    # global visualizer_id, source_id, plugin_config, workspace_id
    # plugin_settings = loader.get_settings(source_id)
    # plugin_config = {}
    # for setting in plugin_settings:
    #     try:
    #         plugin_config[setting.key] = setting.data_type(request.POST.get(setting.key))
    #     except Exception as e:
    #         print(e)
    #         return render(request, 'index.html',
    #                       {"sources": loader.sources, "visualizers": loader.visualizers, "modal_opened": True,
    #                        "modal_error": True,
    #                        "settings": plugin_settings, "source_id": source_id, "visualizer_id": visualizer_id})
    # loader.load_graph(source_id, plugin_config)
    # return render_new_graph(request)

def config(request):
    global visualizer_id, source_id, workspace_id
    visualizer_id = int(request.POST.get("visualizers"))
    source_id = int(request.POST.get("sources"))
    print(visualizer_id, source_id)
    # if 'show' in request.POST:
    #     if main_view.is_workspace_loaded(workspace_id):
    #         if loader.is_graph_loaded(source_id, main_view.get_workspace_config(workspace_id)):
    #             return change_visualizer(request, visualizer_id)
    #     else:
    #         if loader.is_graph_loaded(source_id, plugin_config):
    #             return render_new_graph(request)

    return render(request, 'index.html',
                  {"sources": loader.sources, "visualizers": loader.visualizers, "modal_opened": True,
                   "settings": loader.get_settings(source_id), "source_id": source_id, "visualizer_id": visualizer_id})

def search(request):
    pass
    # global plugin_config, workspace_id, visualizer_id, source_id
    # search_text: str = str(request.POST.get("query"))
    # main_view_html = main_view.generate_with_filter(search_text, workspace_id)
    # tree_view = TreeView(main_view.get_workspace_graph(workspace_id))
    # return render(request, 'index.html', {"sources": loader.sources, "visualizers": loader.visualizers,
    #                                       "tree_view_html": tree_view.generate_tree_view(),
    #                                       "visualization_html": main_view_html, "source_id": source_id,
    #                                       "visualizer_id": visualizer_id})

def clear_filters(request):
    pass
    # main_view_html = main_view.clear_filters(workspace_id)
    # tree_view = TreeView(main_view.get_workspace_graph(workspace_id))
    # return render(request, 'index.html', {"sources": loader.sources, "visualizers": loader.visualizers,
    #                                       "visualization_html": main_view_html,
    #                                       "tree_view_html": tree_view.generate_tree_view(), "source_id": source_id,
    #                                       "visualizer_id": visualizer_id})

def set_workspace(request, number: int):
    pass
    # global workspace_id
    # workspace_id = number
    # if main_view.is_workspace_loaded(workspace_id):
    #     return render_existing_graph(request)
    # else:
    #     return index(request)

# def index(request):
#     return HttpResponse("Hello, world. You're at the app index.")
