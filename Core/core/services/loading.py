from abc import abstractmethod, ABC

from Core.core.services.base import BaseService


class LoadingService(BaseService):  #interface that will be used by parser (plugins that will be outside of django) to be sure they have these methods
    @abstractmethod
    def load(self, file):
        pass

    @abstractmethod
    def create_graph(self):
        pass