import threading
from importlib.metadata import entry_points

from api.src.types.graph import Graph
from core.src.models.plugin import Plugin
import os
import pickle


class Loader:
    data_source_eps = entry_points(group='graph.sources')
    visualizer_eps = entry_points(group='graph.visualizers')
    sources: dict[str, Plugin] = {}
    visualizers: dict[int, Plugin] = {}
    loaded_graphs: dict[int, Graph] = {}
    __singleton_lock = threading.Lock()
    __singleton_instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__singleton_instance is None:
            with cls.__singleton_lock:
                if cls.__singleton_instance is None:
                    cls.__singleton_instance = super(Loader, cls).__new__(cls)
        return cls.__singleton_instance

    def initialize_loader(self):
        # breakpoint()
        # id = 0
        # for entry_point in self.data_source_eps:
        #     print(entry_point)
        #     plugin = entry_point.load()
        #     plugin_instance = Plugin(plugin.DataSource(), id)
        #     print("NAME " + str(plugin.DataSource().name))
        #     self.sources[plugin.DataSource().name] = plugin_instance
        #
        #     id += 1
        id = 0
        print("Loading data sources:")
        for entry_point in self.data_source_eps:
            print(f"Found entry point: {entry_point}")
            plugin = entry_point.load()
            plugin_instance = Plugin(plugin.DataSource(), id)
            print(f"Plugin instance created: {plugin.DataSource().name()}")
            self.sources[plugin.DataSource().name()] = plugin_instance
            id += 1

        id = 0
        for entry_point in self.visualizer_eps:
            plugin = entry_point.load()
            plugin_instance = Plugin(plugin.GraphVisualizer(), id)
            self.visualizers[id] = plugin_instance
            id += 1

    def load_graph(self, source_plugin_id: int, source_name: str) -> Graph:
        print(source_name)
        print("KEYS AND VALUES:")
        for key, value in self.sources.items():
            print(f"Key: {key}, Value: {value}")
        graph = self.sources["api_football_datasource"].plugin.load({})
        print(graph)
        return graph

        # key = hash(str(source_plugin_id))
        # # config_copy.pop("graph_name")
        # file_name = self.create_file_name(source_name)
        # file_path = os.path.join("saved_graphs", str(file_name))
        # if os.path.exists(file_path):
        #     with open(file_path, 'rb') as file:
        #         self.loaded_graphs[key] = pickle.load(file)
        # else:
        #     os.makedirs("saved_graphs", exist_ok=True)
        #     with open(file_path, 'wb') as file:
        #         print("RECNIK " + self.sources.keys())
        #         graph = self.sources[source_name].plugin.load({})
        #         self.loaded_graphs[key] = graph
        #         pickle.dump(graph, file)
        # return self.loaded_graphs[key]

    def get_sources(self) -> dict[int, Plugin]:
        return self.sources

    def get_visualizers(self) -> dict[int, Plugin]:
        return self.visualizers

    def is_graph_loaded(self, source_plugin_id: int, config: dict) -> bool:
        return hash(str(source_plugin_id) + str(config)) in self.loaded_graphs.keys()

    def get_loaded_graph(self, plugin_id: int, source_name: str) -> Graph:
        key = hash(str(plugin_id))
        if key in self.loaded_graphs.keys():
            return self.loaded_graphs[key]
        else:
            return self.load_graph(plugin_id, source_name)

    def get_settings(self, plugin: int):
        return self.sources[plugin].plugin.params()

    def create_file_name(self, source_name) -> str:
        file_name: str = source_name[:3]
        # for value in config.values():
        #     file_name += str(value)
        # file_name += ".pkl"
        return file_name
