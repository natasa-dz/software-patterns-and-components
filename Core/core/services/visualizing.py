from abc import abstractmethod

from core.services.base import BaseService

class VisualizingService(BaseService):
    @abstractmethod
    def visualize(self, graph, request):
        pass