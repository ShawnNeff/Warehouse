import streamlit as st
import os
import pandas as pd
import openpyxl as op
import io
import xlsxwriter

st.set_page_config(layout="wide")
st.title("Slotting Reports")
# st.sidebar.success("Reliable Parts")
# with st.sidebar:
#     st.page_link('./main.py', label="Home")
#     st.page_link('./pages/2_Inventory_History.py', label="Inventory History")
#     st.page_link('./pages/3_Inventory_Reports.py', label="Inbound Reports")
#     st.page_link('./pages/4_Nobin_Zero_Lists.py', label="Nobin / Zero Reports")
#     st.page_link('./pages/5_Three_Day_Old_ASN_Reports.py', label="ASN 3 Day Old Report")
#     st.page_link('./pages/6_Bin_Change_Log.py', label="Slotting Reports")
#     st.page_link('./pages/7_Calculate_Item_Class_Size.py', label="Calculate Item Class Size")

file1 = st.file_uploader("**Inventory File** - Upload inventory excel file in xlsx format.",type="xlsx")
# file2 = st.file_uploader("**Bin Change Log** - Upload bin change log excel file in xlsx format.",type="xlsx")
# file3 = st.file_uploader("**Size Class Log** - Upload LAT_US_Missing_Item_Size_Class excel file in xlsx format.",type="xlsx")

# if file1 is not None and file2 is not None and file3 is not None:
#     f1 = pd.read_excel(file1)
#     f2 = pd.read_excel(file2)
#     f3 = pd.read_excel(file3)

#     f1.drop(f1.columns[[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 28, 29, 30, 31, 32, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 62, 63, 64]], axis=1, inplace=True)

    # TODO: if lat us missing item size class in bin change log delete line in bin change long
    # TODO: if primary bin = "NOBIN" delete in bin change log
    # TODO: go line by lin in bin change log and check to see if new bin size changed in inventory file (if not, delete line)
    # TODO: remove and duplicate values


if file1 is not None:
    file = pd.read_excel(file1)
    file2 = pd.read_excel(file1)

    # Drop garbage columns
    file.drop(file.columns[[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 28, 29, 30, 31, 32, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 62, 63, 64]], axis=1, inplace=True)
    file2.drop(file2.columns[[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 28, 29, 30, 31, 32, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 62, 63, 64]], axis=1, inplace=True)

    i_db = len(file) - 1

    while i_db >= 0:
        if file.loc[i_db, 'ItemSizeClassID'] == file.loc[i_db, 'BinSizeClassID']:
            file = file.drop(i_db)
        i_db -= 1

    i_db = len(file2) - 1

    while i_db >= 0:
        if file2.loc[i_db, 'ItemVelocityClassID'] == file2.loc[i_db, 'BinVelocityClassID']:
            file2 = file2.drop(i_db)
        i_db -= 1

    st.subheader("Bin and Size Class Mismatch")
    st.write(file)
    st.subheader("Velocity Mismatch")
    st.write(file2)
