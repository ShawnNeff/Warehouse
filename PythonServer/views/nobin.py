import streamlit as st
import pandas as pd
import io
import os

# list for all non locations

nobinmaster = pd.read_excel('./files/nobinmaster.xlsx')

item = st.file_uploader("Upload unassigned bins file.",type="xlsx")

if item is not None:

    file = pd.read_excel(item)

    # Combine both dataframes vertically
    combined_file = pd.concat([file, nobinmaster])

    # keep=False drops ALL occurrences of any rows that have matches
    unique_combined_file = combined_file.drop_duplicates(keep=False)

    st.write(unique_combined_file)

    file.to_excel('nobinmaster.xlsx', index=False)
