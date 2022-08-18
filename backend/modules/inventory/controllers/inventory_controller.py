from io import BytesIO
import pandas as pd
from modules.inventory.services.interfaces.inventory_service import InventoryService

class InventoryController:

    __service__: InventoryService

    def __init__(self, service: InventoryService):
        self.__service__ = service
    
    def read(self, data: BytesIO, tag: str) -> pd.DataFrame:
        return self.__service__.readInventory(data, tag)
