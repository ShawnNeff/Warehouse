import streamlit as st
import pandas as pd
import io
import os

# list for all non locations
#script_dir = os.path.dirname(__file__)
#filepath = os.path.join(script_dir, 'nobinmaster.xlsx')

filepath = "./PythonServer/files/nobinmaster.xlsx"
nobinmaster = pd.DataFrame()

if os.path.exists(filepath):
    nobinmaster = pd.read_excel(filepath)
    st.write("file loaded")
else:
    st.error("File not found on the server.")
    st.write(os.getcwd())
    
item = st.file_uploader("Upload unassigned bins file.",type="xlsx")

if item is not None:

    file = pd.read_excel(item)

    # Combine both dataframes vertically
    combined_file = pd.concat([file, nobinmaster])

    # keep=False drops ALL occurrences of any rows that have matches
    unique_combined_file = combined_file.drop_duplicates(keep=False)

    st.write(unique_combined_file)

    file.to_excel('nobinmaster.xlsx', index=False)
