import streamlit as st
import pandas as pd

zeromaster = pd.read_excel('zeromaster.xlsx')

item = st.file_uploader("Upload inventory file.",type="xlsx")

if item is not None:

    file = pd.read_excel(item)

    file2 = file[file['Quantity'] == 0]

    file2.to_excel('zerolist.xlsx', index=False)

    file = pd.read_excel('zerolist.xlsx')
    file2 = pd.read_excel('zeromaster.xlsx')

    file3 = file['ItemID'].isin(file2['ItemID'])
    file.drop(file2[file3].index, inplace=True)

    st.write(file)

    #file.to_excel('zeromaster.xlsx', index=False)
