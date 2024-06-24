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
    def __init__(self, edge_id: int, source: Node, destination: Node, directed: bool):
        self.edge_id = edge_id
        self.source = source
        self.destination = destination
        self.directed = directed

    def __str__(self):
        return str(self.edge_id) + "   source: " + str(
            self.source) + "   destination: " + str(self.destination)

    def __eq__(self, other) -> bool:
        return self.source == other.source and self.destination == other.destination


class Graph:
    def __init__(self, name: str, edges: list[Edge], nodes: list[Node]):
        self.name = name
        self.edges = edges
        self.nodes = nodes

    # def add_node(self, data: dict) -> Node:
    #     if len(self.nodes) != 0:
    #         new_node = Node(self.nodes[-1].node_id + 1, data)
    #         for node in self.nodes:
    #             if new_node == node:
    #                 return node
    #     else:
    #         new_node = Node(1, data)
    #
    #     self.nodes.append(new_node)
    #     return new_node

    def add_node(self, data: dict, node_id) -> Node:
        if len(self.nodes) != 0:
            new_node = Node(node_id, data)
            for node in self.nodes:
                if node_id == node.node_id:
                    return node
        else:
            new_node = Node(node_id, data)

        self.nodes.append(new_node)
        return new_node

    def add_edge(self, source: Node, destination: Node) -> Edge:
        if len(self.edges) != 0:
            new_edge = Edge(self.edges[-1].edge_id + 1, source, destination, False)
            for edge in self.edges:
                if edge == new_edge:
                    return edge
        else:
            new_edge = Edge(1, source, destination, False)

        self.edges.append(new_edge)
        return new_edge

    def get_node_count(self) -> int:
        return len(self.nodes)

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
        return "Name: " + self.name + '\n' + "Nodes: \t\t" + nodes_str + "Edges: \t\t" + edges_str

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
