from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseSecurityModule(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def scan(self, file_path: str) -> Dict[str, Any]:
        pass