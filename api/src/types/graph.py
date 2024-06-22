
class Node:
    def __init__(self, node_id: int, data: dict):
        self.node_id = node_id
        self.data = data

    def __ne__(self, other):
        return self.node_id != other.node_id

    def __eq__(self, other):
        return self.node_id == other.node_id

    def __str__(self):
        return str(self.node_id)


class Edge:
    def __init__(self, edge_id: int, data: dict, source: Node, destination: Node, directed: bool):
        self.edge_id = edge_id
        self.data = data
        self.source = source
        self.destination = destination
        self.directed = directed

    def __str__(self):
        return str(self.edge_id) + "{  " + str(self.data) + "  }" + "   source: " + str(
            self.source) + "   destination: " + str(self.destination)


class Graph:
    def __init__(self, name: str, root: Node, edges: list[Edge], nodes: list[Node]):
        self.name = name
        self.root = root
        self.edges = edges
        self.nodes = nodes

    def set_root(self, root: Node):
        self.root = root

    def add_node(self, node: Node):
        if node not in self.nodes:
            self.nodes.append(node)

    def get_node(self, node_id):
        for node in self.nodes:
            if node.node_id == node_id:
                return node

    def add_edge(self, edge: Edge):
        self.edges.append(edge)

    def get_node_count(self) -> int:
        return len(self.nodes)

    def add_edges(self, edges: list[Edge]):
        pass

    def get_neighbours(self, node: Node):
        neighbours = []
        for edge in self.edges:
            if edge.directed:
                if node == edge.source:
                    neighbours.append(edge.destination)
            else:
                if node == edge.source:
                    neighbours.append(edge.destination)
                if node == edge.destination:
                    neighbours.append(edge.source)
        return neighbours



    def __str__(self):
        nodes_str = ""
        edges_str = ""
        for node in self.nodes:
            nodes_str += str(node) + '\n'
        for edge in self.edges:
            edges_str += str(edge) + '\n'
        return "Name: " + self.name + "\nRoot: " + str(
            self.root) + '\n' + "Nodes: \t\t" + nodes_str + "Edges: \t\t" + edges_str

    def dfs(self, visited: list[Node], node: Node):  # function for dfs
        if node not in visited:
            visited.append(node)
            for neighbour in self.get_neighbours(node):
                self.dfs(visited, neighbour)

    def get_neighbours_undirected(self, node: Node):
        neighbours = []
        for edge in self.edges:
            if node == edge.source:
                neighbours.append(edge.destination)
            if node == edge.destination:
                neighbours.append(edge.source)
        return neighbours

    def dfs_undirected(self, visited: list[Node], node: Node):  # function for dfs
        if node not in visited:
            visited.append(node)
            for neighbour in self.get_neighbours_undirected(node):
                self.dfs_undirected(visited, neighbour)
