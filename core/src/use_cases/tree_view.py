import os

from django.template.loader import render_to_string
from jinja2 import Environment, FileSystemLoader

from api.src.types.graph import Graph
from core.src.models.tree import Tree
from core.src.use_cases.loader import Loader


class TreeView(object):
    def __init__(self, graph: Graph):
        self.graph = graph
        self.tree = None

    def generate_tree_view(self):
        if self.graph.get_node_count() <= 0:
            return ''
        self.tree = Tree(self.graph)
        context = {
            "input_tree": self.tree.get_json(),
        }
        path = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'graph_visualization', 'app', 'templates')
        jinja_env = Environment(loader=FileSystemLoader(path))
        template = jinja_env.get_template('tree_template.html')
        return template.render(context)