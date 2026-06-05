import streamlit as st
import pandas as pd
import os
import xlxswriter
from datetime import timedelta, datetime

# Open excel file
#df = pd.read_excel('./PythonServer/files/cleaned.xlsx')

item = st.file_uploader("**Transaction File** - Upload cleaned transcation file in xlsx format.",type=["xlsx", "xls", "csv"])

if item is not None:
    file = pd.read_excel(item)
    
    # Seperate USER ID from DATETIME in the 'DATETIME' column
    df['USER'] = df['DATETIME'].where(df['DATETIME'].apply(lambda x: isinstance(x, str)))
    df['DATE'] = df['DATETIME'].where(df['DATETIME'].apply(lambda x: isinstance(x, datetime)))
    
    # Reorder columns in dataframe
    df = df[['USER', 'DATE', 'ITEMID', 'TRANSACTION', 'SOURCEBIN', 'DESTBIN', 'QUANTITY', 'JOB']]
    df['PACKAGEQTY'] = ""
    df['AVGPERPACKAGE'] = ""
    df['30MINGAPS'] = ""
    df['15MINGAPS'] = ""
    df['10MINGAPS'] = ""
    df['5MINGAPS'] = ""
    
    df['5MINGAPS'] = df['5MINGAPS'].astype(str)
    df['10MINGAPS'] = df['10MINGAPS'].astype(str)
    df['15MINGAPS'] = df['15MINGAPS'].astype(str)
    df['30MINGAPS'] = df['30MINGAPS'].astype(str)
    
    df['USER'] = df['USER'].ffill()
    for index, row in df.iterrows():
        if row['TRANSACTION'] == "Clock Out":
            df.loc[index, 'USER'] = ""
    
    i = 0
    cols = ['DATE', 'ITEMID', 'TRANSACTION', 'SOURCEBIN', 'DESTBIN', 'QUANTITY', 'JOB']
    u = ""
    # Varialbe - set of all users
    users = ("AJB002", "ALH002", "AXG004", "AXG006", "BBN001", "BJH001", "CXH003", "CXP001", "DLJ001", "DVA001", "DXN001", "DXK001", "EAY001", "JJS001", "JXA001", "KAN001", "LJM001", "MDL001", "NXP003", "PXL001", "SC303", "SC304", "SC306", "SPN001", "SXD001", "TXF001")
    packages = [0, "", False]
    
    df.loc[i:, cols] = df.loc[i:, cols].shift(-1)
    
    df.to_excel('./PythonServer/files/result.xlsx', index=False)
    df = pd.read_excel('./PythonServer/files/result.xlsx')
    
    for index, row in df.iterrows():
        index2 = index + 1
    
        if index2 >= len(df) - 1:
            break
    
        if df.loc[index2, 'DATE'] == "" or df.loc[index2, 'DATE'] == "nan":
            index2 = index + 2
            index = index + 1
        else:
            t = df.loc[index2, 'DATE'] - df.loc[index, 'DATE']
            t = t.total_seconds()
    
            if t > 899 and t < 1799:
                t = t / 60
                df.loc[index2, '15MINGAPS'] = str(f"{t:.2f} minutes")
            if t > 1799:
                t = t / 60
                df.loc[index2, '30MINGAPS'] = str(f"{t:.2f} minutes")
            if t > 599 and t < 899:
                t = t / 60
                df.loc[index2, '10MINGAPS'] = str(f"{t:.2f} minutes")
            if t > 299 and t < 599:
                t = t / 60
                df.loc[index2, '5MINGAPS'] = str(f"{t:.2f} minutes")
    
            if row['TRANSACTION'] == "LOAD.STAGE" and row['SOURCEBIN'] == "PICK" and row['DESTBIN'] == "PACK":
                packages[2] = True
                if packages[1] == "" or packages[1] == row['JOB']:
                    packages[1] = row['JOB']
                    packages[0] += 1
                else:
                    index2 = index - 1
                    df.loc[index2, 'PACKAGEQTY'] = packages[0]
                    packages[0] = 1
                    packages[1] = row['JOB']
            else:
                if packages[2] == True:
                    index2 = index - 1
                    df.loc[index2, 'PACKAGEQTY'] = packages[0]
                    packages[0] = str("")
                    packages[1] = row['JOB']
                    packages[2] = False
    
    # Save file
    df.to_excel('./PythonServer/files/result.xlsx', index=False)

    st.write(df)
