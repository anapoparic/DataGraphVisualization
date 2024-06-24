from api.src.services.base_visualizer import VisualizerPlugin
from jinja2 import Environment, FileSystemLoader

from api.src.types.graph import Graph


def transform_nodes(nodes):
    return [{"node_id": node.node_id, "data": node.data} for node in nodes]


def transform_edges(edges):
    return [{"source": edge.source.node_id, "target": edge.destination.node_id} for edge in edges]


def prepare_context(graph):
    nodes = transform_nodes(graph.nodes)
    edges = transform_edges(graph.edges)
    context = {
        "nodes": nodes,
        "edges": edges,
    }
    return context


class GraphVisualizer(VisualizerPlugin):
    def visualize(self, graph: Graph):
        context = prepare_context(self, graph)
        template_dir = "../simple_visualizer/src/plugin"
        env = Environment(loader=FileSystemLoader(template_dir))
        template = env.get_template("mainView.html")
        return template.render(context)

    def identifier(self):
        return "Simple_Graph_Visualizer"

    def name(self):
        return "Simple Visualizer"
