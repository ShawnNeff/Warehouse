import streamlit as st
import pandas as pd

# Function - get items without a primary location
def primary(file):
    f = pd.DataFrame()
    f2 = pd.DataFrame()
    mergef = pd.DataFrame()

    f = file[file['PrimaryBin'] == "NOBIN"]
    f2 = file[file['PrimaryBin'] == "<NONE>"]

    mergef = pd.merge(f, f2, how='outer')

    return mergef

# Variable - upload inventory file
file = st.file_uploader("Upload inventory file.",type="xlsx")

# IF Statement - makes sure user added both files before running report
if file is not None:
    # Function call - get parts that do not have a primary
    file = primary(file)
    
    st.write(file)