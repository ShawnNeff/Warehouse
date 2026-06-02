import streamlit as st
import pandas as pd

item = st.file_uploader("Upload inventory file.",type="xlsx")

if item is not None:
    file = pd.read_excel(item)
    # item_list = [["", ""]]

    # for index, row in file.iterrows():
    #     if row['ItemSizeClassID'] != row['BinSizeClassID']:
    #         item_list.append([row['ItemID'], row['BinSizeClassID']])
    
    # st.write(item_list)

    df = file[file['ItemSizeClassID'] != file['BinSizeClassID']]

    
    st.write(df[['ItemID', 'BinSizeClassID']])
