import streamlit as st
import os
import pandas as pd
import openpyxl as op
import io
import xlsxwriter
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

st.set_page_config(layout="wide")
st.title("Coming Soon")
st.sidebar.success("Reliable Parts")
with st.sidebar:
    st.page_link('./main.py', label="Home")
    st.page_link('./pages/2_Inventory_History.py', label="Inventory History")
    st.page_link('./pages/3_Inventory_Reports.py', label="Inbound Reports")
    st.page_link('./pages/4_Nobin_Zero_Lists.py', label="Nobin / Zero Reports")
    st.page_link('./pages/5_Three_Day_Old_ASN_Reports.py', label="ASN 3 Day Old Report")
    st.page_link('./pages/6_Bin_Change_Log.py', label="Item Bin Size Change")
    st.page_link('./pages/7_Calculate_Item_Class_Size.py', label="Calculate Item Class Size")
