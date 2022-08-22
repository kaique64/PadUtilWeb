import uuid
import pandas as pd
from pandas import DataFrame

def create_and_save_xls_file(file, dataframe: DataFrame):
    filename = str(uuid.uuid4()) + file.filename + '_RESULT.xlsx'
    path = 'uploads/' + filename
    writer = pd.ExcelWriter(path, engine='xlsxwriter')
    dataframe.to_excel(writer, sheet_name='Example', index=False)

    writer.save()

    results = dict()
    results['path'] = path
    results['filename'] = filename

    return results