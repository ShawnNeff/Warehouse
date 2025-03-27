import streamlit as st
import os
import pandas as pd
import openpyxl as op
import io
import xlsxwriter

st.set_page_config(layout="wide")
st.title("Slotting Reports")
# st.sidebar.success("Reliable Parts")
# with st.sidebar:
#     st.page_link('./main.py', label="Home")
#     st.page_link('./pages/2_Inventory_History.py', label="Inventory History")
#     st.page_link('./pages/3_Inventory_Reports.py', label="Inbound Reports")
#     st.page_link('./pages/4_Nobin_Zero_Lists.py', label="Nobin / Zero Reports")
#     st.page_link('./pages/5_Three_Day_Old_ASN_Reports.py', label="ASN 3 Day Old Report")
#     st.page_link('./pages/6_Bin_Change_Log.py', label="Slotting Reports")

file1 = st.file_uploader("**Inventory File** - Upload inventory excel file in xlsx format.",type="xlsx")
file6 = st.file_uploader("**Unassigned Bin File** - Upload inventory excel file in xlsx format.",type="xlsx")
file7 = st.file_uploader("**Bin File** - Upload inventory excel file in xlsx format.",type="xlsx")

# file2 = st.file_uploader("**Bin Change Log** - Upload bin change log excel file in xlsx format.",type="xlsx")
# file3 = st.file_uploader("**Size Class Log** - Upload LAT_US_Missing_Item_Size_Class excel file in xlsx format.",type="xlsx")

# if file1 is not None and file2 is not None and file3 is not None:
#     f1 = pd.read_excel(file1)
#     f2 = pd.read_excel(file2)
#     f3 = pd.read_excel(file3)

#     f1.drop(f1.columns[[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 28, 29, 30, 31, 32, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 59. 62, 63, 64]], axis=1, inplace=True)

    # TODO: if lat us missing item size class in bin change log delete line in bin change long
    # TODO: if primary bin = "NOBIN" delete in bin change log
    # TODO: go line by lin in bin change log and check to see if new bin size changed in inventory file (if not, delete line)
    # TODO: remove and duplicate values

xs = [0, 0, 0, 0]
sbin1 = [0, 0, 0, 0]
sbin2 = [0, 0, 0, 0]
sbin3 = [0, 0, 0, 0]
sbin4 = [0, 0, 0, 0]
sbin5 = [0, 0, 0, 0]
lbin1 = [0, 0, 0, 0]
lbin2 = [0, 0, 0, 0]
lbin3 = [0, 0, 0, 0]
lbin4 = [0, 0, 0, 0]
lbin5 = [0, 0, 0, 0]
lbin6 = [0, 0, 0, 0]
spallet = [0, 0, 0, 0]
lpallet = [0, 0, 0, 0]
xlpallet = [0, 0, 0, 0]

if file1 is not None and file6 is not None:
    file = pd.read_excel(file1)
    file2 = pd.read_excel(file1)
    file4 = pd.read_excel(file6)    # Match empty bin with binsizecalss and velocity 
    bindata = pd.read_excel(file7)

    # Drop garbage columns
    file.drop(file.columns[[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 28, 29, 30, 31, 32, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 62, 63, 64]], axis=1, inplace=True)
    file2.drop(file2.columns[[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 28, 29, 30, 31, 32, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 62, 63, 64]], axis=1, inplace=True)

    # merge both bin files
    merge_bin = file4.merge(bindata, how='inner', on=['BinID'])
    merge_bin.to_excel('temp.xlsx')
    test = pd.read_excel('temp.xlsx')

    i_db = len(file) - 1
    i_bin = len(test) - 1

    while i_db >= 0:
        if file.loc[i_db, 'ItemSizeClassID'] == file.loc[i_db, 'BinSizeClassID']:
            file = file.drop(i_db)
        i_db -= 1

    i_db = len(file2) - 1

    while i_db >= 0:
        if file2.loc[i_db, 'ItemVelocityClassID'] == file2.loc[i_db, 'BinVelocityClassID']:
            file2 = file2.drop(i_db)
        i_db -= 1

    size = ""
    vel = ""

    while i_bin >= 0:
        size = test.loc[i_bin, 'SizeClassID']
        vel = test.loc[i_bin, 'VelocityClassID']

        if size == "X/S":
            if vel == "A":
                xs[0] += 1
            elif vel == "B":
                xs[1] += 1
            elif vel == "C":
                xs[2] +=  1
            elif vel == "D":
                xs[3] += 1
        elif size == "S BIN 1":
            if vel == "A":
                sbin1[0] += 1
            elif vel == "B":
                sbin1[1] += 1
            elif vel == "C":
                sbin1[2] += 1
            elif vel == "D":
                sbin1[3] += 1
        elif size == "S BIN 2":
            if vel == "A":
                sbin2[0] += 1
            elif vel == "B":
                sbin2[1] += 1
            elif vel == "C":
                sbin2[2] += 1
            elif vel == "D":
                sbin2[3] += 1
        elif size == "S BIN 3":
            if vel == "A":
                sbin3[0] += 1
            elif vel == "B":
                sbin3[1] += 1
            elif vel == "C":
                sbin3[2] += 1
            elif vel == "D":
                sbin3[3] += 1
        elif size == "S BIN 4":
            if vel == "A":
                sbin4[0] += 1
            elif vel == "B":
                sbin4[1] += 1
            elif vel == "C":
                sbin4[2] += 1
            elif vel == "D":
                sbin4[3] += 1
        elif size == "S BIN 5":
            if vel == "A":
                sbin5[0] += 1
            elif vel == "B":
                sbin5[1] += 1
            elif vel == "C":
                sbin5[2] += 1
            elif vel == "D":
                sbin5[3] += 1
        elif size == "L BIN 1":
            if vel == "A":
                lbin1[0] += 1
            elif vel == "B":
                lbin1[1] += 1
            elif vel == "C":
                lbin1[2] += 1
            elif vel == "D":
                lbin1[3] += 1
        elif size == "L BIN 2":
            if vel == "A":
                lbin2[0] += 1
            elif vel == "B":
                lbin2[1] += 1
            elif vel == "C":
                lbin2[2] += 1
            elif vel == "D":
                lbin2[3] += 1
        elif size == "L BIN 3":
            if vel == "A":
                lbin3[0] += 1
            elif vel == "B":
                lbin3[1] += 1
            elif vel == "C":
                lbin3[2] += 1
            elif vel == "D":
                lbin3[3] += 1
        elif size == "L BIN 4":
            if vel == "A":
                lbin4[0] += 1
            elif vel == "B":
                lbin4[1] += 1
            elif vel == "C":
                lbin4[2] += 1
            elif vel == "D":
                lbin4[3] += 1
        elif size == "L BIN 5":
            if vel == "A":
                lbin5[0] += 1
            elif vel == "B":
                lbin5[1] += 1
            elif vel == "C":
                lbin5[2] += 1
            elif vel == "D":
                lbin5[3] += 1
        elif size == "L BIN 6":
            if vel == "A":
                lbin6[0] += 1
            elif vel == "B":
                lbin6[1] += 1
            elif vel == "C":
                lbin6[2] += 1
            elif vel == "D":
                lbin6[3] += 1
        elif size == "S PALLET":
            if vel == "A":
                spallet[0] += 1
            elif vel == "B":
                spallet[1] += 1
            elif vel == "C":
                spallet[2] += 1
            elif vel == "D":
                spallet[3] += 1
        elif size == "L PALLET":
            if vel == "A":
                lpallet[0] += 1
            elif vel == "B":
                lpallet[1] += 1
            elif vel == "C":
                lpallet[2] += 1
            elif vel == "D":
                lpallet[3] += 1
        else:
            if vel == "A":
                xlpallet[0] += 1
            elif vel == "B":
                xlpallet[1] += 1
            elif vel == "C":
                xlpallet[2] += 1
            elif vel == "D":
                xlpallet[3] += 1

        i_bin -= 1

    st.subheader("Bin and Size Class Mismatch")
    st.write(file)
    st.subheader("Velocity Mismatch")
    st.write(file2)
    st.subheader("Open Bins based on Velocity")
    st.write("X/S", xs)
    st.write("S BIN 1", sbin1)
    st.write("S BIN 2", sbin2)
    st.write("S BIN 3", sbin3)
    st.write("S BIN 4", sbin4)
    st.write("S BIN 5", sbin5)
    st.write("L BIN 1", lbin1)
    st.write("L BIN 2", lbin2)
    st.write("L BIN 3", lbin3)
    st.write("L BIN 4", lbin4)
    st.write("L BIN 5", lbin5)
    st.write("L BIN 6", lbin6)
    st.write("S PALLET", spallet)
    st.write("L PALLET", lpallet)
    st.write("XL PALLET", xlpallet)
