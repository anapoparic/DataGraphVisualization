from api.src.types.graph import Graph, Node, Edge
from operator import eq, gt, ge, lt, le, ne
import re

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
        self.configuration = {}
        self.current_graph: Graph = current_graph;
        self.entire_graph: Graph = entire_graph;

    def set_visualizer_id(self, visualizer_id: int):
        self.visualizer_id = visualizer_id

    def set_data_source_id(self, data_source_id: int):
        self.data_source_id = data_source_id

    def set_configuration(self, configuration):
        self.configuration = configuration

    def set_current_graph(self, graph: Graph):
        self.current_graph = graph

    def set_entire_graph(self, graph: Graph):
        self.entire_graph = graph

    def has_current_graph(self) -> bool:
        return self.current_graph is not None


class MainView(object):
    def __init__(self):
        self.workspaces: dict[int, Workspace] = {i: Workspace() for i in range(1, 4)}
        self.current_workspace_id = 1;
        # ucitati Loader klasu
        self.data_sources = []
        self.visualizers = []

    def show_workspace_graph(self, workspace_id: int):
        return self.visualizers[self.workspaces[workspace_id].visualizer_id].plugin.show(
            self.workspaces[workspace_id].current_graph)

    def get_current_workspace_graph(self, workspace_id: int):
        return self.workspaces[workspace_id].current_graph

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
        pass



    def search_graph(self, search_word: str, workspace: Workspace, result_graph: Graph):
        pass


