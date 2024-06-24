from api.src.services.base_visualizer import VisualizerPlugin
from api.src.types.graph import Graph
from jinja2 import Environment, FileSystemLoader

def transform_nodes(nodes):
    result = []
    for node in nodes:
        result.append({
            "node_id": node.node_id,
            "data": node.data
        })
    return result

def transform_edges(edges):
    result = []
    for edge in edges:
        result.append({
            "source": edge.source.node_id,
            "destination": edge.destination.node_id
        })
    return result

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
        template_dir = "../block_visualizer/src/plugin"
        env = Environment(loader=FileSystemLoader(template_dir))
        template = env.get_template("visualization.html")
        return template.render(context)

    def identifier(self):
        return "graph_block-visualizer"

    def name(self):
        return "Block Visualizer"
