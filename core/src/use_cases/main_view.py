from api.src.types.graph import Graph, Node, Edge
from operator import eq, gt, ge, lt, le, ne
import re
import copy

from core.src.use_cases.loader import Loader

operators = {
    '==': eq,
    '>': gt,
    '>=': ge,
    '<': lt,
    '<=': le,
    '!=': ne
}


class Workspace(object):
    def __init__(self, current_graph: Graph = None, entire_graph: Graph = None):
        self.visualizer_id = -1;
        self.data_source_id = -1;
        # self.configuration = {}
        self.current_graph: Graph = current_graph;
        self.entire_graph: Graph = entire_graph;

    def set_visualizer_id(self, visualizer_id: int):
        self.visualizer_id = visualizer_id

    def set_data_source_id(self, data_source_id: int):
        self.data_source_id = data_source_id

    def set_current_graph(self, graph: Graph):
        self.current_graph = graph

    def set_entire_graph(self, graph: Graph):
        self.entire_graph = graph

    def has_current_graph(self) -> bool:
        return self.current_graph is not None


class MainWorkspace(object):
    def __init__(self):
        self.workspaces: dict[int, Workspace] = {i: Workspace() for i in range(1, 4)}
        self.current_workspace_id = 1
        self.loader = Loader()
        # ucitati Loader klasu
        self.data_sources = self.loader.sources
        self.visualizers = self.loader.visualizers

    def show_workspace_graph(self, workspace_id: int):
        workspace = self.workspaces[workspace_id]
        visualizer_id = workspace.visualizer_id
        visualizer = self.visualizers[visualizer_id]
        graph = workspace.current_graph
        return visualizer.plugin.visualize(graph)

    def get_current_workspace_graph(self, workspace_id: int):
        workspace = self.workspaces[workspace_id]
        return workspace.current_graph

    def load_current_workspace(self, id: int):
        current = self.workspaces[id]
        return current.has_current_graph()

    def get_workspace(self, id: int):
        return self.workspaces[id]

    def init(self, wsc_id: int, source_id: int, visualizer_id: int):
        workspace = self.workspaces[wsc_id]
        graph = self.loader.load_graph(source_id)
        workspace.set_current_graph(graph)

        workspace.set_entire_graph(copy.deepcopy(self.workspaces[wsc_id].current_graph))
        workspace.set_visualizer_id(visualizer_id)
        workspace.set_data_source_id(source_id)

        visualizer = self.visualizers[visualizer_id]

        return visualizer.plugin.visualize(workspace.current_graph)

    def search_filter(self, search_word: str, workspace_id: int):
        pattern = r'(\w+)\s*(==|>=?|<=?|!=)\s*(.+)'
        match = re.match(pattern, search_word)
        workspace = self.workspaces[workspace_id];
        if match:

            if workspace.current_graph is None:
                return ''
            result_graph: Graph = Graph(workspace.current_graph.name, [], [], None)
            return self.filter_graph(match.group(1), match.group(2), match.group(3), workspace, result_graph)
        else:

            if self.workspaces[workspace_id].current_graph is None:
                return ''
            result_graph: Graph = Graph(workspace.current_graph.name, [], [], None)
            return self.search_graph(search_word, workspace, result_graph)

    def filter_graph(self, attribute: str, operator: str, value: str, workspace: Workspace, result_graph: Graph):
        workspace_graph = workspace.current_graph
        for node in workspace_graph.nodes:
            if self.is_filter_successful(node, attribute, operator, value):
                result_graph.add_node(node.data, node.node_id)
        # add edges
        if result_graph.get_node_count() > 0:
            root = result_graph.nodes[0]
            result_graph.set_root(root)
            for edge in workspace_graph.edges:
                if edge.source in result_graph.nodes and edge.destination in result_graph.nodes:
                    result_graph.add_edge(edge.source, edge.destination)
        workspace.set_current_graph(result_graph)
        return self.visualizers[workspace.visualizer_id].plugin.visualize(result_graph)

    def compare(self, attribute_value: str, operator: str, value: str) -> bool:
        if operator in operators:
            return operators[operator](attribute_value, value)
        return False

    def is_filter_successful(self, node: Node, attribute: str, operator: str, value: str) -> bool:
        if attribute == "id":
            return self.compare(node.node_id, operator, value)
        else:
            try:
                data = node.data
                if attribute not in data:
                    return False  # Atribut nije prisutan u podacima čvora

                data_type = type(data[attribute])
                try:
                    converted_value = data_type(value)
                except ValueError:
                    return False  # Neuspešna konverzija vrednosti u očekivani tip

                return self.compare(data[attribute], operator, converted_value)
            except:
                return False

    def search_graph(self, search_word: str, workspace: Workspace, result_graph: Graph):
        workspace_graph = workspace.current_graph
        visited_nodes = set()
        for node in workspace_graph.nodes:
            if self.is_search_successful(search_word, node):
                result_graph.add_node(node.data, node.node_id)
                visited_nodes.add(node.node_id)  # Dodajemo node_id umesto samog node-a

                # Pronalaženje i dodavanje susednih čvorova
                neighbours = self.get_neighbours(node, workspace_graph.edges)
                for neighbour in neighbours:
                    if neighbour.node_id not in visited_nodes:
                        result_graph.add_node(neighbour.data, neighbour.node_id)
                        visited_nodes.add(neighbour.node_id)
        # add edges
        if result_graph.get_node_count() > 0:
            root = result_graph.nodes[0]
            result_graph.set_root(root)
            for edge in workspace_graph.edges:
                if edge.source in result_graph.nodes and edge.destination in result_graph.nodes:
                    result_graph.add_edge(edge.source, edge.destination)
        workspace.set_current_graph(result_graph)
        return self.visualizers[workspace.visualizer_id].plugin.visualize(result_graph)

    def get_neighbours(self, node: Node, edges: list[Edge]) -> list[Node]:
        neighbours = []
        for edge in edges:
            if edge.directed:
                if node == edge.source:
                    neighbours.append(edge.destination)
            else:
                if node == edge.source:
                    neighbours.append(edge.destination)
                if node == edge.destination:
                    neighbours.append(edge.source)
        return neighbours

    def is_search_successful(self, search_word, node: Node):
        if search_word in str(node.node_id):
            return True
        for value in node.data.values():
            if search_word in str(value):
                return True
        return False

    def clear_filters(self, wsc_id: int):
        workspace = self.workspaces[wsc_id]
        entire_graph = workspace.entire_graph
        visualizer = self.visualizers[workspace.visualizer_id]
        if workspace.entire_graph is None:
            return ''
        workspace.current_graph = copy.deepcopy(entire_graph)
        return visualizer.plugin.visualize(entire_graph)
