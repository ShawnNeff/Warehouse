import streamlit as st
import pandas as pd

item = st.file_uploader("Upload Inventory file.",type="xlsx")

l = ['L PALLET', 'XL PALLET', 'S PALLET', 'L BIN 6', 'M SHELF', 'S SHELF', 'L SHELF', 'LONG']

if item is not None:
        
    # open inventory file
    file = pd.read_excel(item)

    file = file[file.duplicated(subset=['PrimaryBin'], keep=False)]

    for index, row in file.iterrows():
        if row['BinSizeClassID'] in l:
            file = file.drop(index)

    for index, row in file.iterrows():
        index2 = index + 1
        if file.loc[index2, 'ItemID'] in file.loc[index, 'ItemID']
            file = file.drop(index2)
            file = file.drop(index)
        
    st.write(file)
