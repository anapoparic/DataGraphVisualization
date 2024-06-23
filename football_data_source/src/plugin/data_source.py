from api.src.services.base_provider import SourcePlugin
from api.src.types.config import Config
import requests
from api.src.types.graph import Graph

headers = {
    'x-rapidapi-key': "695aff988dmsh646605d8f683a26p10b76ajsn51879da83914",
    'x-rapidapi-host': "euro-20242.p.rapidapi.com"
}


def load_players():
    url = "https://euro-20242.p.rapidapi.com/players"
    response = requests.get(url, headers=headers)
    data = response.json()
    return data


def load_groups():
    url = "https://euro-20242.p.rapidapi.com/groups"
    response = requests.get(url, headers=headers)
    data = response.json()
    return data


def add_node(graph, data, node_id):
    return graph.add_node(data, node_id)


def add_edge(graph, source, destination):
    return graph.add_edge(source, destination)


def load_graph():
    graph_name = "Football Graph"
    graph = Graph(name=graph_name, edges=[], nodes=[], root=None)

    players = load_players()
    groups = load_groups()

    groups_dict = {}

    for group in groups:
        group_data = {
            "name": group["name"],
            "number_of_teams": len(group["teams"]),
            "number_of_matches": len(group["matches"])
        }
        group_node = graph.add_node(group_data, group["_id"])
        groups_dict[group["_id"]] = group_node

    for player in players:
        player_data = {
            "name": player["name"],
            "team_name": player["team"]["name"],
            "position": player["position"],
            "dateOfBirth": player["dateOfBirth"],
            "club": player["club"],
            "goals": player["goals"],
            "minutesPlayed": player["minutesPlayed"]
        }
        team = player['team']
        team_data = {
            "name": team["name"],
            "coach": team["coach"],
            "captain": team["captain"],
            "championships": team["championships"],
            "number_of_players": len(team["players"])
        }

        player_node = graph.add_node(player_data, player["_id"])
        team_node = graph.add_node(team_data, team["_id"])

        graph.add_edge(player_node, team_node)
        graph.add_edge(groups_dict[team["group"]], team_node)

    return graph


graph2 = load_graph()
print(graph2)
# graph2.search_graph();
graph2.filter_graph();


class DataSource(SourcePlugin):
    def load(self, config: dict):
        return load_graph()

    def identifier(self):
        return "graph-football-datasource"

    def name(self):
        return "api_football_datasource"

    def config(self) -> list[Config]:
        return [Config("Graph name", "graph_name", str), Config("Depth", "depth", int),
                Config("Access token", "access_token", str)]
