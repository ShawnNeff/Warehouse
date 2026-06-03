import streamlit as st
import pandas as pd

st.header("Item Velocity Missmatch")
st.write("")
st.write("")

item = st.file_uploader("Upload inventory file.",type="xlsx")

if item is not None:
    file = pd.read_excel(item)

    df = file[file['ItemVelocityClassID'] != file['BinVelocityClassID']]

    st.write(df[['ItemID', 'PrimaryBin', 'Quantity', 'BinVelocityClassID', 'ItemVelocityClassID']])
