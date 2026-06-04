import streamlit as st
import pandas as pd
import io
import os

def printzero(file):
    lsta = []
    lstb = []
    temp = []
    multibins = ['L BIN 6', 'L SHELF', 'LONG', 'M SHELF']
    
    file = file.reset_index()

    for index, row in file.iterrows():
        if row['BinSizeClassID'] in multibins:
            temp = [row['ItemID'], row['PrimaryBin']]
            lsta.appent(temp)
        else:
            lstb.append(row['PrimaryBin'])

    lstb.sort()
    lsta = sorted(lsta, key=itemgetter(1))

    df = pd.DataFrame()
    bins = pd.Series(lstb)

    df.insert(loc=0, column='Bins', value=bins)

    items = []
    location = []

    for x, y in lsta:
        items.append(x)
        location.append(y)

    ia = pd.Series(items)
    ib = pd.Series(location)

    df.insert(loc=1, column='Item', value=ia)
    df.insert(loc=2, column='Location', value=ib)

    return df
    
filepath = "./PythonServer/files/zeromaster.xlsx"
zeromaster = pd.DataFrame()

if os.path.exists(filepath):
    zeromaster = pd.read_excel(filepath)
    st.write("file loaded")
else:
    st.error("File not found on the server.")

item = st.file_uploader("Upload inventory file.",type="xlsx")

if item is not None:

    file = pd.read_excel(item)

    file2 = file[file['Quantity'] == 0]

    file2.to_excel('./PythonServer/files/zerolist.xlsx', index=False)

    file = pd.read_excel('./PythonServer/files/zerolist.xlsx')
    #file2 = pd.read_excel('zeromaster.xlsx')

    file3 = file['ItemID'].isin(zeromaster['ItemID'])
    file.drop(zeromaster[file3].index, inplace=True)

    file = printzero(file)
    
    st.write(file)

    file.to_excel('./PythonServer/files/zeromaster.xlsx', index=False)
