import streamlit as st
import os
import pandas as pd
import openpyxl as op
import io
import xlsxwriter


# def fill_lists(i, imax, dfloc):
#     dflist = []
#     while i < imax:
#         dflist.append(dfloc['BinID'][i])

#         i += 1
#     return dflist
st.set_page_config(layout="wide")

st.sidebar.image('logo.png', width=260)

st.sidebar.page_link("main.py", label="Home")
st.sidebar.page_link("Pages/inboundreports.py", label="Inventory Reports")
st.sidebar.page_link("Pages/nobinzerolist.py", label="NOBIN / ZERO Lists")
st.sidebar.page_link("Pages/3dayold.py", label="3 Day old ASN's")
st.sidebar.page_link("Pages/zeroprogram.py", label="Zero Program")
st.sidebar.page_link("Pages/itemclasssize.py", label="Calculate Item Class Size")

# file = st.file_uploader("**Inventory File** - Upload inventory excel file in xlsx format.",type="xlsx")
# file2 = st.file_uploader("**Multiple Bins** - Upload excel file with all multi-locations in xlsx format.", type="xlsx")

# if file is not None and file2 is not None:
#     df = pd.read_excel(file)
#     df2 = pd.read_excel(file2)

#     df.drop(df.columns[[
#     1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 23,
#     24, 25, 26, 28, 29, 30, 31, 32, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44,
#     45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63,
#     64
#     ]],
#         axis=1,
#         inplace=True)

#     #length of each file
#     i_df = len(df) - 1
#     i_df2 = len(df2) - 1

#     i = 0

#     duplicates = df.duplicated(subset=['ItemID'], keep=False)
#     duplicate_rows = df[duplicates]

#     duplicatebin = df.duplicated(subset=['PrimaryBin'], keep=False)
#     duplicate_bins = df[duplicatebin]
#     duplicate_bins.to_excel('bins.xlsx', index=False)

#     db = pd.read_excel('bins.xlsx')

#     dz = df[df['Quantity'] == 0]
#     dt = dz[dz['HostOnPurchaseOrder'] != 0]
#     dz = dz[dz['HostOnPurchaseOrder'] == 0]

#     itemnobin = df[df['PrimaryBin'] == "NOBIN"]
#     itemnone = df[df['PrimaryBin'] == "<NONE>"]

#     # fill multibin list
#     multi_loc = fill_lists(i, i_df2, df2)

#     i_db = len(db) - 1

#     while i_db >= 2:
#         if db.loc[i_db, 'PrimaryBin'] in multi_loc:
#             db = db.drop(i_db)
#         i_db -= 1

#     i_df -= 1

#     db = db.sort_values(by=['PrimaryBin'])
#     duplicate_rows = duplicate_rows.sort_values(by=['PrimaryBin'])

#     db.to_excel('doubleloc.xlsx', index=False)

#     #open excel files
#     df = pd.read_excel('doubleloc.xlsx')

#     #sort excel file before processing
#     df_sorted = df.sort_values('ItemID')
#     df_sorted.to_excel('tempers.xlsx', index=False)

#     df = pd.read_excel('tempers.xlsx')

#     #length of each file
#     i_df = len(df) - 1

#     i = 0

#     #remove cores
#     while i_df >= 2:
#         i2 = i_df - 1

#         if df.loc[i2, 'ItemID'] in df.loc[i_df, 'ItemID']:
#             df = df.drop(i_df)
#             df = df.drop(i2)
#             i_df = i2 - 1
#         else:
#             i_df -= 1

#     df.sort_values(by='PrimaryBin', inplace=True)

#     st.subheader("NOBIN List")
#     st.write(dz)
#     st.subheader("ZERO List")
#     st.write(dt)
#     st.subheader("Multiple Items in One Location")
#     st.write(df)
#     st.subheader("Items with Multiple Locations")
#     st.write(duplicate_rows)
#     st.subheader("Items with No Primary Locations")
#     st.write(itemnobin)
#     st.write(itemnone)    