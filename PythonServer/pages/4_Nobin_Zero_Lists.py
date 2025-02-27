import streamlit as st
import os
import pandas as pd
import openpyxl as op
import io
import xlsxwriter

# function to check for duplicates
def checkzero(file1, file2):
  file3 = file2['PrimaryBin'].isin(file1['PrimaryBin'])
  file2.drop(file2[file3].index, inplace=True)
  return file2

def checknobin(file1, file2):
  file3 = file2['BinID'].isin(file1['BinID'])
  file2.drop(file2[file3].index, inplace=True)
  return file2

st.set_page_config(layout="wide")
st.title("NOBIN / ZERO Lists")
# st.sidebar.success("Reliable Parts")
# with st.sidebar:
#     st.page_link('./main.py', label="Home")
#     st.page_link('./pages/2_Inventory_History.py', label="Inventory History")
#     st.page_link('./pages/3_Inventory_Reports.py', label="Inbound Reports")
#     st.page_link('./pages/4_Nobin_Zero_Lists.py', label="Nobin / Zero Reports")
#     st.page_link('./pages/5_Three_Day_Old_ASN_Reports.py', label="ASN 3 Day Old Report")
#     st.page_link('./pages/6_Bin_Change_Log.py', label="Item Bin Size Change")
#     st.page_link('./pages/7_Calculate_Item_Class_Size.py', label="Calculate Item Class Size")

file = st.file_uploader("**Nobin Master** - Upload nobin master file.",type="xlsx")
file2 = st.file_uploader("**Nobin List** - Upload nobin list file.", type="xlsx")
file3 = st.file_uploader("**Zero Master** - Upload zero master file", type="xlsx")
file4 = st.file_uploader("**Zero List** - Upload zero list file", type="xlsx")

if file is not None and file2 is not None and file3 is not None and file4 is not None:

    df = pd.read_excel(file)
    df2 = pd.read_excel(file2)
    df3 = pd.read_excel(file3)
    df4 = pd.read_excel(file4)
    
    # run checkfiles 
    dfzero = checkzero(df3, df4)
    dfnobin = checknobin(df, df2)

    st.subheader("Nobin List")
    st.write(dfnobin)
    st.subheader("Zero List")
    st.write(dfzero)
