from abc import ABC, abstractmethod, abstractproperty

class Message(ABC):
    @abstractmethod
    def __init__(self, content, sender, receiver):
        pass