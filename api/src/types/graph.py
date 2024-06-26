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


from operator import eq, gt, ge, lt, le, ne
import re


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
    def __init__(self, name: str, edges: list[Edge], nodes: list[Node], root: Node):
        self.name = name
        self.edges = edges
        self.nodes = nodes
        self.root = root

    def set_root(self, root: Node):
        self.root = root

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

    def search_graph(self):
        search_word = input("Unesite rec za pretragu: ")
        result_graph: Graph = Graph("Graph", [], [], None)
        visited_nodes = set()
        for node in self.nodes:
            if self.is_search_successful(search_word, node):
                result_graph.add_node(node.data, node.node_id)
                visited_nodes.add(node.node_id)  # Dodajemo node_id umesto samog node-a

                # Pronalaženje i dodavanje susednih čvorova
                neighbours = self.get_neighbours(node)
                for neighbour in neighbours:
                    if neighbour.node_id not in visited_nodes:
                        result_graph.add_node(neighbour.data, neighbour.node_id)
                        visited_nodes.add(neighbour.node_id)
        # add edges
        if result_graph.get_node_count() > 0:
            root = result_graph.nodes[0]
            result_graph.set_root(root)
            for edge in self.edges:
                if edge.source in result_graph.nodes and edge.destination in result_graph.nodes:
                    result_graph.add_edge(edge.source, edge.destination)
        print(result_graph);

    def is_search_successful(self, search_word, node: Node):
        if search_word in str(node.node_id):
            return True
        for value in node.data.values():
            if search_word in str(value):
                return True
        return False

    def filter_graph(self):
        search_word = input("Unesite query za filtriranje: ")

        pattern = r'(\w+)\s*(==|>=?|<=?|!=)\s*(.+)'
        match = re.match(pattern, search_word)

        if match:
            attribute = match.group(1)
            operator = match.group(2)
            value = match.group(3)

            result_graph = Graph("Graph", [], [], None)

            for node in self.nodes:
                if self.is_filter_successful(node, attribute, operator, value):
                    result_graph.add_node(node.data, node.node_id)

            # Dodavanje grana u rezultujući graf
            if result_graph.get_node_count() > 0:
                root = result_graph.nodes[0]
                result_graph.set_root(root)
                for edge in self.edges:
                    if edge.source in result_graph.nodes and edge.destination in result_graph.nodes:
                        result_graph.add_edge(edge.source, edge.destination)

            print(result_graph)
        else:
            print("Unos nije u validnom formatu.")

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


operators = {
    '==': eq,
    '>': gt,
    '>=': ge,
    '<': lt,
    '<=': le,
    '!=': ne
}
