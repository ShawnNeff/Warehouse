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

# st.sidebar.image('logo.png', width=260)

# st.sidebar.page_link("main.py", label="Home")
# st.sidebar.page_link("Pages/inboundreports.py", label="Inventory Reports")
# st.sidebar.page_link("Pages/nobinzerolist.py", label="NOBIN / ZERO Lists")
# st.sidebar.page_link("Pages/3dayold.py", label="3 Day old ASN's")
# st.sidebar.page_link("Pages/zeroprogram.py", label="Zero Program")
# st.sidebar.page_link("Pages/itemclasssize.py", label="Calculate Item Class Size")

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
