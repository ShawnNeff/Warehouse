import streamlit as st
import os
import pandas as pd
import openpyxl as op
import io
import xlsxwriter

# st.set_page_config(layout="wide")
# st.title("Bin Change Log Report")
# st.sidebar.success("Reliable Parts")

# with st.sidebar:
#     st.page_link('./main.py', label="Home")
#     st.page_link('./pages/2_zeroprogram.py', label="Inventory History")
#     st.page_link('./pages/3_inboundreports.py', label="Inbound Reports")
#     st.page_link('./pages/4_nobinzerolist.py', label="Nobin / Zero Reports")
#     st.page_link('./pages/5_3dayold.py', label="ASN 3 Day Old Report")
#     st.page_link('./pages/6_binchange.py', label="Item Bin Size Change")
#     st.page_link('./pages/7_itemclasssize.py', label="Calculate Item Class Size")
#     st.page_link('./pages/8_swap.py', label="Swap Bins (Velocity)")

option = st.selectbox('What Aisle do you want to work on?', ('All', '11', '13', '15', '17', '19', '21', '23', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '49', '50', '51', '52', '53', '54', '55', '56', '57', '58', '59', '60', '61', '62'))

option2 = st.selectbox('What bin type do you want to move?', ('X/S', 'S BIN 1', 'S BIN 2', 'S BIN 3', 'S BIN 4', 'S BIN 5', 'L BIN 1', 'L BIN 2', 'L BIN 3', 'L BIN 4', 'L BIN 5', 'L BIN 6', 'L SHELF', 'S SHELF', 'S PALLET', 'L PALLET', 'XL PALLET', 'LONG'))

file1 = st.file_uploader("**Inventory File** - Upload inventory excel file in xlsx format.",type="xlsx")

if file1 is not None:

    file = pd.read_excel(file1)

    l = len(file) - 1
    
    while l >= 0:

        size = file.loc[l, 'BinSizeClassID']
        bin = file.loc[l, 'PrimaryBin']
        bin = bin[:2]

        if option == "All":
            if file.loc[l, 'ItemVelocityClassID'] == file.loc[l, 'BinVelocityClassID'] or size != option2 or file.loc[l, 'ItemVelocityClassID'] == "<NONE>":
                file = file.drop(l)
        elif bin != option or file.loc[l, 'ItemVelocityClassID'] == file.loc[l, 'BinVelocityClassID'] or size != option2 or file.loc[l, 'ItemVelocityClassID'] == "<NONE>":
            file = file.drop(l)

        l -= 1

    st.write(file)
