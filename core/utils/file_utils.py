import pandas as pd


def read_excel_file(file):
    if file.name.endswith(".csv"):
        return pd.read_csv(file).where(pd.notnull, None)
    elif file.name.endswith(".xlsx"):
        return pd.read_excel(file, engine="openpyxl").where(pd.notnull, None)
    raise ValueError("Sadece .csv ve .xlsx dosyaları kabul edilir.")
