from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from io import BytesIO
import pandas as pd
import uuid
import os
from modules.inventory.services.inventory_service_xls import InventoryServiceXLS
from modules.inventory.controllers.inventory_controller import InventoryController

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

inventoryServiceXLS = InventoryServiceXLS()
inventoryControllerXLS = InventoryController(inventoryServiceXLS)

@app.post('/files/xls/upload', response_class=FileResponse)
def upload_file(file: UploadFile = File(...)):
    content = file.file.read()
    data = BytesIO(content)
    result = inventoryControllerXLS.read(data, "TAG")

    path = 'uploads/' + str(uuid.uuid4()) + file.filename + '_RESULT.xlsx'
    writer = pd.ExcelWriter(path, engine='xlsxwriter')
    result.to_excel(writer, sheet_name='Example', index=False)

    writer.save()

    file.file.close()

    if os.path.isfile(path):
        return FileResponse(path=path, filename=file.filename)
    return None
