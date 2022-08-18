from fastapi import FastAPI, File, UploadFile
from io import BytesIO
import pandas as pd
import uuid
from starlette.responses import FileResponse
from modules.inventory.services.inventory_service_xls import InventoryServiceXLS
from modules.inventory.controllers.inventory_controller import InventoryController

app = FastAPI()
inventoryServiceXLS = InventoryServiceXLS()
inventoryControllerXLS = InventoryController(inventoryServiceXLS)

@app.post('/files/xls/upload')
def upload_file(file: UploadFile = File(...)):
    content = file.file.read()
    data = BytesIO(content)
    result = inventoryControllerXLS.read(data, "TAG")

    path = 'results/' + str(uuid.uuid4()) + file.filename + '_RESULT.xlsx'
    writer = pd.ExcelWriter(path, engine='xlsxwriter')
    result.to_excel(writer, sheet_name='Example', index=False)

    writer.save()

    file.file.close()
    headers = {
        'Content-Disposition': 'attachment; filename="' + path + '"'
    }

    return FileResponse(path, headers=headers, media_type='application/octet-stream', filename=file.filename)
