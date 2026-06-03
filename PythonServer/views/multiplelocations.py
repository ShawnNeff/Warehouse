import streamlit as st
import pandas as pd

st.header("Mulitple Locations for Single Item")
st.write("")
st.write("")

item = st.file_uploader("Upload Inventory file.",type="xlsx")

l = ['L PALLET', 'XL PALLET', 'S PALLET', 'L BIN 6', 'M SHELF', 'S SHELF', 'L SHELF', 'LONG']

if item is not None:
        
    # open inventory file
    file = pd.read_excel(item)

    file = file[file.duplicated(subset=['ItemID'], keep=False)]

    st.write(file[['ItemID', 'PrimaryBin', 'Quantity']])
