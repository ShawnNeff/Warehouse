import streamlit as st
import pandas as pd

def MultiItems(f):
    temp = f.duplicated(subset=['PrimaryBin'], keep=False)
    dupitem = f[temp]
    
    dupitem.sort_values(by='ItemID', inplace=True)
    dupitem.to_excel('MultipleBins.xlsx', index=False)
    dupitem = pd.read_excel('MultipleBins.xlsx')

    i = len(dupitem) - 1

    while i >= 1:
        i2 = i - 1

        if dupitem.loc[i2, 'ItemID'] in dupitem.loc[i, 'ItemID']:
            dupitem = dupitem.drop(i)
            dupitem = dupitem.drop(i2)
            i = i2 - 1
        else:
            i -= 1
    
    dupitem.sort_values(by='PrimaryBin', inplace=True)
    #dupitem.to_excel('MultipleBins.xlsx', index=False)

    return dupitem

st.header("Muliple Items in Discrete Location")
st.write("")
st.write("")

item = st.file_uploader("Upload Inventory file.",type="xlsx")

if item is not None:
        
    # open inventory file
    file = pd.read_excel(item)

    # declare multi bin variable
    multibin = ("L BIN 6", "L SHELF", "LONG", "M SHELF", "XL PALLET")
    sysbin = ("BAGNTAG", "DAMAGED", "DCORE1", "DIRTYCORE", "FCRTN", "INV", "LOBBY", "MISSING", "MLSTAGE", 
            "NLCRT1", "NLCRT2", "NLPLT1", "NLPLT2", "P3RACK1", "P3RACK1A", "P3RACK1B", "P3RACK1C", "P3RACK1D", 
            "P3RACK3", "PACK", "PICK", "QUARANTINE", "RCCRT1", "RECV", "RETURN", "RRTNCRT3", "RTNCRT1", 
            "RTNCRT2", "RTNCRT3", "RTNFRONT", "RTNPLT1", "SAC NS", "STSHORT", "TRASH", "VELOCITY A", 
            "VELOCITY B", "VECOLICTY C", "VELOCITY D")
    carts = ("RCVCRT1", "RCVCRT2", "RCVCRT3", "RCVCRT4", "RCVCRT5", "RCVCRT6", "RCVCRT7", "RCVCRT8", 
            "RCVCRT9", "RCVCRT10", "RCVCRT11", "RCVCRT12", "RCVCRT13", "RCVCRT14", "RCVCRT15",
            "RCVCRT16", "RCVCRT17", "RCVCRT18", "RCVCRT19", "RCVCRT20", "RCVCRT21", "RCVCRT22",
            "RCVPLT1", "RCVPLT2", "RCVPLT3", "RCVPLT4", "RCVPLT5", "RCVPLT6", "RCVPLT7", "RCVPLT8",
            "RCVPLT9", "RCVPLT10", "RCVPLT11", "RCVPLT12", "RCVPLT13", "RCVPLT14", "RCVPLT15", 
            "RCVPLT16", "RCVPLT17", "RCVPLT18", "RCVPLT19", "RCVPLT20", "RCVPLT21", "RCVPLT22",
            "RCVPLT23", "RCVPLT24", "RCVPLT25", "RCVPLT26", "RCVPLT27", "RCVPLT28", "RCVPLT29",
            "RCVPLT30", "RCVPLT31", "RCVPLT32", "RCVPLT33", "RCVPLT34", "RCVPLT35", "RCVPLT36", 
            "RCVPLT37", "RCVPLT38", "RCVPLT39", "RCVPLT40", "RCVPLT41", "RCVPLT42", "RCVPLT43", 
            "RCVPLT44", "RCVPLT45", "RCVPLT46", "RCVPLT47", "RCVPLT48", "RCVPLT49", "RCVPLT50", 
            "RCVPLT51", "RCVPLT52", "RCVPLT53", "RCVPLT54", "RCVPLT55", "RCVPLT56", "RCVPLT57", 
            "RCVPLT58", "RCVPLT59", "RCVSMALL1", "RCVSMALL2", "RCVSMALL3", "RCVSMALL4")

    file.drop(file.columns[[
        1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 23,
        24, 25, 26, 28, 29, 30, 31, 32, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44,
        45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 62, 63, 64
    ]], axis=1, inplace=True)

    length = len(file) - 1

    while length >= 1:

        if file.loc[length, 'BinSizeClassID'] in multibin or file.loc[length, 'BinID'] in sysbin or file.loc[length, 'BinID'] in carts:
            file = file.drop(length)

        length -= 1

    file = MultiItems(file)

    st.write(file[['ItemID', 'Quanitty', 'PrimaryBin']])
