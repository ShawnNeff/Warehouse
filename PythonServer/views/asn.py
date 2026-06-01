import streamlit as st
import os
import pandas as pd
import openpyxl as op
import io
import xlsxwriter

# Function - cleans the excel file, keeps only what is needed
def clean_data(file):
    file = file.drop(file.columns[[0, 1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 18, 19, 20, 21, 22, 23, 24, 25]], axis=1, inplace=True)
    file.columns = ['ASN', 'CONSOLIDATED']
    file = file.dropna()
    return file

# Function - returns set of all ASN's in the file
def get_asn(file):
    s = set()
    for index, row in file.iterrows():
        if row['CONSOLIDATED'] == "" or row['CONSOLIDATED'] == " ":
            s.add(row['ASN'])
        else:
            s.add(row['CONSOLIDATION'])
    return s

# Functions - returns only the unique ASN's from yesterdays file sorted a to z
def get_unique_asn(file, file2):
    unique_file = set()
    unique_file = file2 - file
    
    unique_file = sort_set(unique_file)

    return unique_file

# Function - returns sorted set from a to z
def sort_set(file):
    return sorted(file)

# Variable - sorts both files
item = st.file_uploader("**Today's ASN File** - Upload today's open ASN file.",type="xlsx")
item2 = st.file_uploader("**Yesterday's ASN File** - Upload yesterday's open ASN file.", type="xlsx")

# Variable - dataframe to save results
file3 = pd.DataFrame()

# Variable - counter
x = 0

# Variable - set variables to hold unique ASN's from each excel file
sf = set()
sf2 = set()

# IF Statement - makes sure user added both files before running report
if file is not None and file2 is not None:

    file = pd.read_excel(item)
    file2 = pd.read_excel(item2)
    
    # Function Call - returns only ASN information
    file = clean_data(file)
    file2 = clean_data(file2)

    # Function Call - returns only unique ASN's from each file
    sf = get_asn(file)
    sf2 = get_asn(file2)

    # Function Call - returns sorted unique ASN's from yesterday's file
    unique_sf = get_unique_asn(sf, sf2)

    # Add each ASN in set to dataframe
    for s in unique_sf:
        file3.loc[x, 0] = s
        x += 1

    # Display File
    st.write(file3)
