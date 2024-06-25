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

    def get_sources(self) -> dict[str, Plugin]:
        return self.sources

    def get_visualizers(self) -> dict[int, Plugin]:
        return self.visualizers

    def __new__(cls, *args, **kwargs):
        if cls.__singleton_instance is None:
            with cls.__singleton_lock:
                if cls.__singleton_instance is None:
                    cls.__singleton_instance = super(Loader, cls).__new__(cls)
        return cls.__singleton_instance

    def initialize_loader(self):
        id = 0
        for entry_point in self.data_source_eps:
            plugin = entry_point.load()
            plugin_instance = Plugin(plugin.DataSource(), id)
            self.sources[plugin.DataSource().name()] = plugin_instance
            id += 1

        id = 0
        for entry_point in self.visualizer_eps:
            plugin = entry_point.load()
            plugin_instance = Plugin(plugin.GraphVisualizer(), id)
            self.visualizers[id] = plugin_instance
            id += 1

    def load_graph(self, source_id: int) -> Graph:
        global data
        data = None
        for key, val in self.sources.items():
            if source_id == val.id:
                data = self.sources[key]
                break

        if data is not None:
            graph = data.plugin.load({})
            return graph
        else:
            raise ValueError(f"No data source found for source_id {source_id}")

    def is_graph_loaded(self, source_plugin_id: int, config: dict) -> bool:
        return hash(str(source_plugin_id) + str(config)) in self.loaded_graphs.keys()

    def get_loaded_graph(self, source_id: int) -> Graph:
        key = hash(str(source_id))
        if key in self.loaded_graphs.keys():
            return self.loaded_graphs[key]
        else:
            return self.load_graph(source_id)
