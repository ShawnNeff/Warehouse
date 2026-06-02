import streamlit as st
import pandas as pd

item = st.file_uploader("Upload inventory file.",type="xlsx")

if item is not None:
    file = pd.read_excel(item)

    df = file[file['ItemSizeClassID'] != file['BinSizeClassID']]

    
    st.write(df[['ItemID', 'BinSizeClassID']])
