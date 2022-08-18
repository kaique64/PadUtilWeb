from io import BytesIO
from typing import Any
import pandas as pd
from .interfaces.inventory_service import InventoryService

class InventoryServiceXLS(InventoryService):
    def __updateColumnsNames__(columns) -> dict[str]:
        updatedColumns = {columns[0]:'Placa', 
                        columns[1] : 'Modelo',
                        columns[2] : 'Numero_de_serie', 
                        columns[3] : "cod_de_produto", 
                        columns[4] : 'Serial', 
                        columns[5] : 'NE',
                        columns[6] : 'Slot',
                        columns[7] : 'PosicaoRack', 
                        columns[8] : 'Sub_Rack',  
                        columns[9] : 'Versao_Firmware', 
                        columns[10] : 'Versao_Hardware', 
                        columns[11] : 'Descricao', 
                        columns[12] : 'Chassi_Id', 
                        columns[13] : 'Inibido', 
                        columns[14] : 'Em_teste', 
                        columns[15] : 'Plataforma',}

        return updatedColumns
    
    def __getEanCodeBySeriesNumber__(series_number: str):
        return series_number.str.slice(4, 20)

    def readInventory(self, data: BytesIO, tag: str) -> Any:
        dataFromXLSFile = pd.read_excel(data)
        dataFromXLSFile = pd.DataFrame(dataFromXLSFile)

        quantityOfColumns = len(dataFromXLSFile.columns)
        quantityOfLines = len(dataFromXLSFile)
        
        if quantityOfColumns == 19:
            dataFromXLSFile = dataFromXLSFile.drop([0, 1, quantityOfLines-2, quantityOfLines-1], axis=0)

        if quantityOfColumns == 21:
            dataFromXLSFile = dataFromXLSFile.drop([0, 2, quantityOfLines-3, quantityOfLines-1], axis=0)

        dataFromXLSFile = dataFromXLSFile.dropna(axis=1, how="all")
        dataFromXLSFile = dataFromXLSFile.dropna(axis=0, how="all")
        
        actualColumnsNames = dataFromXLSFile.columns.values.tolist()
        
        updatedColumnsNames = InventoryServiceXLS.__updateColumnsNames__(actualColumnsNames)

        dataFromXLSFile.rename(columns=updatedColumnsNames, inplace = True)
        
        dataFromXLSFile['EAN'] = InventoryServiceXLS.__getEanCodeBySeriesNumber__(dataFromXLSFile['Numero_de_serie'])
        dataFromXLSFile['Região'] = tag

        dataFromXLSFile.sort_values(by=['NE', 'Chassi_Id', 'Modelo'])

        return dataFromXLSFile
