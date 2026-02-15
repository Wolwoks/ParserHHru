import os
import pandas as pd


def excel(columns: list, filename: str, sheet_name: str = 'Sheet1'):
    df = pd.DataFrame(columns=columns)

    if not os.path.exists('excel_files'):
        os.makedirs('excel_files')

    filepath = os.path.join('excel_files', filename)
    excel_writer = pd.ExcelWriter(filepath, engine='xlsxwriter')
    df.to_excel(excel_writer, sheet_name=sheet_name)
    excel_writer._save()

    return filepath
