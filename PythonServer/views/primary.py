import streamlit as st
import pandas as pd
import numpy as np

# Function - Output non matching columns [PrimaryBin], [BinID]
def get_primary(file):
    matching_row = pd.DataFrame()

    matching_row = file[file['PrimaryBin'] != file['BinID']]

    return matching_row
        
# Variable - upload inventory file
item = st.file_uploader("Upload inventory file.",type="xlsx")

# IF Statement - makes sure user added both files before running report
if item is not None:

    # Variable - read excel file
    file = pd.read_excel(item)

    # Function call - get parts that do not have a primary
    #file = primary(file)
    file = get_primary(file)
    
    st.write(file)
