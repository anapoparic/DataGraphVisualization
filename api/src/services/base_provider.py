from abc import abstractmethod
from api.src.services.base_service import ServiceBase
from api.src.types.config import Config


class SourcePlugin(ServiceBase):
    @abstractmethod
    def load(self, config: dict):
        pass

    @abstractmethod
    def config(self) -> list[Config]:
        pass
