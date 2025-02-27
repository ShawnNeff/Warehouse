import streamlit as st
import os
import pandas as pd
import openpyxl as op
import io
import xlsxwriter

def fill_lists(i, imax, dfloc):
    dflist = []
    while i < imax:
        dflist.append(dfloc['ASN'][i])
        i += 1
    return dflist

st.set_page_config(layout="wide")
st.title("ASN Three Day Old Reports")
# st.sidebar.success("Reliable Parts")
# with st.sidebar:
#     st.page_link('./main.py', label="Home")
#     st.page_link('./pages/2_Inventory_History.py', label="Inventory History")
#     st.page_link('./pages/3_Inventory_Reports.py', label="Inbound Reports")
#     st.page_link('./pages/4_Nobin_Zero_Lists.py', label="Nobin / Zero Reports")
#     st.page_link('./pages/5_Three_Day_Old_ASN_Reports.py', label="ASN 3 Day Old Report")
#     st.page_link('./pages/6_Bin_Change_Log.py', label="Item Bin Size Change")
#     st.page_link('./pages/7_Calculate_Item_Class_Size.py', label="Calculate Item Class Size")
    
file = st.file_uploader("**Today's ASN File** - Upload today's open ASN file.",type="xlsx")
file2 = st.file_uploader("**Yesterday's ASN File** - Upload yesterday's open ASN file.", type="xlsx")

if file is not None and file2 is not None:

    df = pd.read_excel(file2)
    df2 = pd.read_excel(file)

    df.drop(df.columns[[
        0, 1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21,
        22, 23, 24, 25
    ]],
            axis=1,
            inplace=True)

    df.columns = ['ASN']

    df2.drop(df2.columns[[
        0, 1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21,
        22, 23, 24, 25
    ]],
            axis=1,
            inplace=True)

    df2.columns = ['ASN']

    i_df = len(df) - 1
    i_df2 = len(df2) - 1
    i = 0

    asn = fill_lists(i, i_df2, df2)

    while i_df >= 2:
        if df.loc[i_df, 'ASN'] in asn:
            df = df.drop(i_df)
        i_df -= 1

    st.write(df)
