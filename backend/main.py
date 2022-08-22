from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import uuid
import os
from utils.convert_bytes_io import convert_to_bytes_io
from utils.create_and_save_xls_file import create_and_save_xls_file
from modules.inventory.services.inventory_service_xls import InventoryServiceXLS
from modules.inventory.controllers.inventory_controller import InventoryController

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5173", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

inventoryServiceXLS = InventoryServiceXLS()
inventoryControllerXLS = InventoryController(inventoryServiceXLS)

@app.post('/files/xls/upload', response_class=FileResponse)
def upload_file(file: UploadFile = File(...), tag: str = ''):
    content = file.file.read()
    data = convert_to_bytes_io(content)
    result = inventoryControllerXLS.read(data, tag)

    XLSPathFile = create_and_save_xls_file(file, result)
    path = XLSPathFile['path']
    filename = XLSPathFile['filename']

    file.file.close()

    if os.path.isfile(path):
        return FileResponse(path=path, filename=filename)
    return None
