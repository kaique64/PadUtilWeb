from abc import ABC, abstractmethod
from io import BytesIO
from typing import Any
import pandas as pd

class InventoryService(ABC):
    @abstractmethod
    def __updateColumnsNames__(columns) -> dict[str]:
        pass
    
    @abstractmethod
    def __getEanCodeBySeriesNumber__(series_number: str) -> str:
        pass
    
    @abstractmethod
    def readInventory(self, data: BytesIO, tag: str) -> Any:
        pass
