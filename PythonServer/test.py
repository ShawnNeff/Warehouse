import os
import pandas as pd
import openpyxl as op
import xlsxwriter

file = pd.read_excel('Transactions.xls')

file.dropna(subset=['Unnamed: 0'], inplace=True)
file.to_excel('result.xlsx', index=False)