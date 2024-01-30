from abc import abstractmethod, ABC

class BaseService(ABC):
    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def identifier(self):
        pass
