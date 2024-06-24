import threading
from importlib.metadata import entry_points

from api.src.types.graph import Graph
from core.src.models.plugin_model import Plugin
import os
import pickle


class Loader():
    data_source_eps = entry_points(group='graph.sources')
    visualizer_eps = entry_points(group='graph.visualizers')
    sources: dict[int, Plugin] = {}
    visualizers: dict[int, Plugin] = {}
    __singleton_lock = threading.Lock()
    __singleton_instance = None

    def instance(cls):

        # check for the singleton instance
        if not cls.__singleton_instance:
            with cls.__singleton_lock:
                if not cls.__singleton_instance:
                    cls.__singleton_instance = cls()

        # return the singleton instance
        return cls.__singleton_instance

    def initialize_loader(self):
        plugin_id = 0
        for entry_point in self.data_source_eps:
            plugin = entry_point.load()
            plugin_instance = Plugin(plugin.DataSource(), plugin_id, name=plugin.DataSource().name())
            print("NAMEEE " + plugin_instance.name);
            self.sources[plugin_id] = plugin_instance
            plugin_id+=1

        plugin_id = 0
        for entry_point in self.visualizer_eps:
            plugin = entry_point.load()
            plugin_instance = Plugin(plugin.GraphVisualizer(), plugin_id, name=plugin.GraphVisualizer().name())
            self.visualizers[plugin_id] = plugin_instance
            plugin_id+=1

    def load_graph(self, source_plugin_id: int, config) -> Graph:
        key = hash(str(source_plugin_id) + str(config))
        config_copy = config.copy()
        config_copy.pop("graph_name")
        file_name = self.create_file_name(source_plugin_id, config_copy)
        file_path = os.path.join("saved_graphs", str(file_name))
        if os.path.exists(file_path):
            with open(file_path, 'rb') as file:
                self.loaded_graphs[key] = pickle.load(file)
        else:
            os.makedirs("saved_graphs", exist_ok=True)
            with open(file_path, 'wb') as file:
                graph = self.sources[source_plugin_id].plugin.load(config)
                self.loaded_graphs[key] = graph
                pickle.dump(graph, file)
        return self.loaded_graphs[key]
