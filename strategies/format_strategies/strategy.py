from abc import ABC, abstractmethod
import strategies


class FormatStrategy(ABC):
    def __init__(self, strategy):
        self.strategy = strategy
        
    @abstractmethod
    def append_market(self, caller, parsed_market):
        pass
