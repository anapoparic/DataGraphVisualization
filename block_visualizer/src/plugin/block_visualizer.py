from api.src.services.base_visualizer import VisualizerPlugin
from api.src.types.graph import Graph
from jinja2 import Environment, FileSystemLoader


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
    def visualize(self, graph):
        context = prepare_context(graph)
        template_dir = "../block_visualizer/src/plugin"
        env = Environment(loader=FileSystemLoader(template_dir))
        template = env.get_template("visualization.html")
        return template.render(context)

    def identifier(self):
        return "graph_block-visualizer"

    def name(self):
        return "Block Visualizer"
