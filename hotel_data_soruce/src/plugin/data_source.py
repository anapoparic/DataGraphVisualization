import requests
from api.src.services.base_provider import SourcePlugin
from api.src.types.config import Config
from api.src.types.graph import Graph

headers = {
    "x-rapidapi-key": "4dc61e47e9msh1cde259b7972bdfp15706djsnc6fc2517cda6",
    "x-rapidapi-host": "priceline-com-provider.p.rapidapi.com"
}


def load_countries():
    url = "https://priceline-com-provider.p.rapidapi.com/v2/hotels/downloadCountries"
    querystring = {"limit": "300"}
    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()
    return data['getSharedBOF2.Downloads.Hotel.Countries']['results']['countries']


def load_cities():
    url = "https://priceline-com-provider.p.rapidapi.com/v2/hotels/downloadCities"
    querystring = {"limit": "500"}
    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()
    return data['getSharedBOF2.Downloads.Hotel.Cities']['results']['cities']


def load_hotels():
    url = "https://priceline-com-provider.p.rapidapi.com/v2/hotels/downloadHotels"
    querystring = {"limit": "500", "language": "fr-FR"}
    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()
    return data['getSharedBOF2.Downloads.Hotel.Hotels']['results']['hotels']


def add_node(graph, data, node_id):
    graph.add_node(data, node_id)


def add_edge(graph, source, destination):
    graph.add_edge(source, destination)


def load_graph():
    graph_name = "Film Graph"
    graph = Graph(name=graph_name, edges=[], nodes=[])

    countries = load_countries()
    cities = load_cities()
    hotels = load_hotels()

    country_nodes = {}
    city_nodes = {}
    hotel_nodes = {}

    # Function to check if a value is defined (not None and not an empty string)
    def is_defined(value):
        return value is not None and value != ""

    for country in countries:
        country_data = {
            "country": countries[str(country)]["country"] if is_defined(countries[str(country)]["country"]) else "",
            "country_code": countries[str(country)]["country_code_ppn"] if is_defined(countries[str(country)]["country_code_ppn"]) else ""
        }
        if is_defined(country_data["country"]) and is_defined(country_data["country_code"]):
            country_node = graph.add_node(country_data, countries[str(country)]["country_code_ppn"])
            country_nodes[countries[str(country)]["country_code_ppn"]] = country_node

    for city in cities:
        city_data = {
            "city": cities[str(city)]["city"] if is_defined(cities[str(city)]["city"]) else "",
            "state": cities[str(city)]["state"] if is_defined(cities[str(city)]["state"]) else "",
            "latitude": cities[str(city)]["latitude"] if is_defined(cities[str(city)]["latitude"]) else "",
            "longitude": cities[str(city)]["longitude"] if is_defined(cities[str(city)]["longitude"]) else "",
            "timezone": cities[str(city)]["timezone"] if is_defined(cities[str(city)]["timezone"]) else "",
            "hotel_count": cities[str(city)]["hotel_count"] if is_defined(cities[str(city)]["hotel_count"]) else "",
            "country_code": cities[str(city)]["country_code"] if is_defined(cities[str(city)]["country_code"]) else ""  # connection
        }
        if is_defined(city_data["city"]):
            city_node = graph.add_node(city_data, cities[str(city)]["cityid_ppn"])
            city_nodes[cities[str(city)]["cityid_ppn"]] = city_node

            country_id = cities[str(city)]["country_code"]
            if country_id in country_nodes.keys():
                graph.add_edge(city_node, country_nodes[country_id])

    for hotel in hotels:
        hotel_data = {
            "name": hotels[str(hotel)]["hotel_name"] if is_defined(hotels[str(hotel)]["hotel_name"]) else "",
            "hotel_type": hotels[str(hotel)]["hotel_type"] if is_defined(hotels[str(hotel)]["hotel_type"]) else "",
            "review_rating": hotels[str(hotel)]["review_rating"] if is_defined(hotels[str(hotel)]["review_rating"]) else "",
            "room_count": hotels[str(hotel)]["room_count"] if is_defined(hotels[str(hotel)]["room_count"]) else "",
            "check_in": hotels[str(hotel)]["check_in"] if is_defined(hotels[str(hotel)]["check_in"]) else "",
            "check_out": hotels[str(hotel)]["check_out"] if is_defined(hotels[str(hotel)]["check_out"]) else "",
        }
        if is_defined(hotel_data["name"]):
            hotel_node = graph.add_node(hotel_data, hotels[str(hotel)]["hotelid_ppn"])

            city_id = hotels[str(hotel)]["cityid_ppn"]
            country_id = hotels[str(hotel)]["country_code"]

            if city_id in city_nodes:
                graph.add_edge(hotel_node, city_nodes[city_id])

            # if country_id in country_nodes: # add?
            #     graph.add_edge(hotel_node, country_nodes[country_id])

    return graph



#
# graph = load_graph()
# print(graph)

class DataSource(SourcePlugin):
    def load(self, config: dict):
        return load_graph()

    def identifier(self):
        return "graph-hotel-datasource"

    def name(self):
        return "api_hotel_datasource"

    def config(self) -> list[Config]:
        return [Config("Graph name", "graph_name", str),
                Config("Depth", "depth", int),
                Config("Access token", "access_token", str)]
