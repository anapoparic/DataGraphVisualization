from abc import abstractmethod
from api.src.services.base_service import ServiceBase
from api.src.types.graph import Graph


class VisualizerPlugin(ServiceBase):
    @abstractmethod
    def visualize(self, graph: Graph):
        pass
