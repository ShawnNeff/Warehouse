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
#slotting = st.file_uploader("**Slotting Info** - Upload inventory excel file in xlsx format.",type="xlsx")
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

xs = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
sbin1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
sbin2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
sbin3 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
sbin4 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
sbin5 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
lbin1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
lbin2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
lbin3 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
lbin4 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
lbin5 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
lbin6 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
lshelf = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
spallet = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
lpallet = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
xlpallet = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
long = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

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
    # slotting = pd.read_excel('Slottinginfo.xlsx')
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
        
    file2.to_excel('velocity.xlsx')
    velocity = pd.read_excel('velocity.xlsx')

    i = len(velocity) - 1
    size = ""
    item_vel = ""
    bin_vel = ""

    while i >= 0:

        size = velocity.loc[i, 'ItemSizeClassID']
        item_vel = velocity.loc[i, 'ItemVelocityClassID']
        bin_vel = velocity.loc[i, 'BinVelocityClassID']

        if size == "X/S":
            if bin_vel == "A" and item_vel == "B":
                xs[4] += 1
                xs[5] += 1
                xs[9] += 1
            elif bin_vel == "A" and item_vel == "C":
                xs[4] += 1
                xs[5] += 1
                xs[10] += 1
            elif bin_vel == "A" and item_vel == "D":
                xs[4] += 1
                xs[5] += 1
                xs[11] += 1
            elif bin_vel == "B" and item_vel == "A":
                xs[4] += 1
                xs[6] += 1
                xs[12] += 1
            elif bin_vel == "B" and item_vel == "C":
                xs[4] += 1
                xs[6] += 1
                xs[13] += 1
            elif bin_vel == "B" and item_vel == "D":
                xs[4] += 1
                xs[6] += 1
                xs[14] += 1
            elif bin_vel == "C" and item_vel == "A":
                xs[4] += 1
                xs[7] += 1
                xs[15] += 1
            elif bin_vel == "C" and item_vel == "B":
                xs[4] += 1
                xs[7] += 1
                xs[16] += 1
            elif bin_vel == "C" and item_vel == "D":
                xs[4] += 1
                xs[7] += 1
                xs[17] += 1
            elif bin_vel == "D" and item_vel == "A":
                xs[4] += 1
                xs[8] += 1
                xs[18] += 1
            elif bin_vel == "D" and item_vel == "B":
                xs[4] += 1
                xs[8] += 1
                xs[19] += 1
            elif bin_vel == "D" and item_vel == "C":
                xs[4] += 1
                xs[8] += 1
                xs[20] += 1

        elif size == "S BIN 1":
            if bin_vel == "A" and item_vel == "B":
                sbin1[4] += 1
                sbin1[5] += 1
                sbin1[9] += 1
            elif bin_vel == "A" and item_vel == "C":
                sbin1[4] += 1
                sbin1[5] += 1
                sbin1[10] += 1
            elif bin_vel == "A" and item_vel == "D":
                sbin1[4] += 1
                sbin1[5] += 1
                sbin1[11] += 1
            elif bin_vel == "B" and item_vel == "A":
                sbin1[4] += 1
                sbin1[6] += 1
                sbin1[12] += 1
            elif bin_vel == "B" and item_vel == "C":
                sbin1[4] += 1
                sbin1[6] += 1
                sbin1[13] += 1
            elif bin_vel == "B" and item_vel == "D":
                sbin1[4] += 1
                sbin1[6] += 1
                sbin1[14] += 1
            elif bin_vel == "C" and item_vel == "A":
                sbin1[4] += 1
                sbin1[7] += 1
                sbin1[15] += 1
            elif bin_vel == "C" and item_vel == "B":
                sbin1[4] += 1
                sbin1[7] += 1
                sbin1[16] += 1
            elif bin_vel == "C" and item_vel == "D":
                sbin1[4] += 1
                sbin1[7] += 1
                sbin1[17] += 1
            elif bin_vel == "D" and item_vel == "A":
                sbin1[4] += 1
                sbin1[8] += 1
                sbin1[18] += 1
            elif bin_vel == "D" and item_vel == "B":
                sbin1[4] += 1
                sbin1[8] += 1
                sbin1[19] += 1
            elif bin_vel == "D" and item_vel == "C":
                sbin1[4] += 1
                sbin1[8] += 1
                sbin1[20] += 1
        elif size == "S BIN 2":
            if bin_vel == "A" and item_vel == "B":
                sbin2[4] += 1
                sbin2[5] += 1
                sbin2[9] += 1
            elif bin_vel == "A" and item_vel == "C":
                sbin2[4] += 1
                sbin2[5] += 1
                sbin2[10] += 1
            elif bin_vel == "A" and item_vel == "D":
                sbin2[4] += 1
                sbin2[5] += 1
                sbin2[11] += 1
            elif bin_vel == "B" and item_vel == "A":
                sbin2[4] += 1
                sbin2[6] += 1
                sbin2[12] += 1
            elif bin_vel == "B" and item_vel == "C":
                sbin2[4] += 1
                sbin2[6] += 1
                sbin2[13] += 1
            elif bin_vel == "B" and item_vel == "D":
                sbin2[4] += 1
                sbin2[6] += 1
                sbin2[14] += 1
            elif bin_vel == "C" and item_vel == "A":
                sbin2[4] += 1
                sbin2[7] += 1
                sbin2[15] += 1
            elif bin_vel == "C" and item_vel == "B":
                sbin2[4] += 1
                sbin2[7] += 1
                sbin2[16] += 1
            elif bin_vel == "C" and item_vel == "D":
                sbin2[4] += 1
                sbin2[7] += 1
                sbin2[17] += 1
            elif bin_vel == "D" and item_vel == "A":
                sbin2[4] += 1
                sbin2[8] += 1
                sbin2[18] += 1
            elif bin_vel == "D" and item_vel == "B":
                sbin2[4] += 1
                sbin2[8] += 1
                sbin2[19] += 1
            elif bin_vel == "D" and item_vel == "C":
                sbin2[4] += 1
                sbin2[8] += 1
                sbin2[20] += 1
        elif size == "S BIN 3":
            if bin_vel == "A" and item_vel == "B":
                sbin3[4] += 1
                sbin3[5] += 1
                sbin3[9] += 1
            elif bin_vel == "A" and item_vel == "C":
                sbin3[4] += 1
                sbin3[5] += 1
                sbin3[10] += 1
            elif bin_vel == "A" and item_vel == "D":
                sbin3[4] += 1
                sbin3[5] += 1
                sbin3[11] += 1
            elif bin_vel == "B" and item_vel == "A":
                sbin3[4] += 1
                sbin3[6] += 1
                sbin3[12] += 1
            elif bin_vel == "B" and item_vel == "C":
                sbin3[4] += 1
                sbin3[6] += 1
                sbin3[13] += 1
            elif bin_vel == "B" and item_vel == "D":
                sbin3[4] += 1
                sbin3[6] += 1
                sbin3[14] += 1
            elif bin_vel == "C" and item_vel == "A":
                sbin3[4] += 1
                sbin3[7] += 1
                sbin3[15] += 1
            elif bin_vel == "C" and item_vel == "B":
                sbin3[4] += 1
                sbin3[7] += 1
                sbin3[16] += 1
            elif bin_vel == "C" and item_vel == "D":
                sbin3[4] += 1
                sbin3[7] += 1
                sbin3[17] += 1
            elif bin_vel == "D" and item_vel == "A":
                sbin3[4] += 1
                sbin3[8] += 1
                sbin3[18] += 1
            elif bin_vel == "D" and item_vel == "B":
                sbin3[4] += 1
                sbin3[8] += 1
                sbin3[19] += 1
            elif bin_vel == "D" and item_vel == "C":
                sbin3[4] += 1
                sbin3[8] += 1
                sbin3[20] += 1
        elif size == "S BIN 4":
            if bin_vel == "A" and item_vel == "B":
                sbin4[4] += 1
                sbin4[5] += 1
                sbin4[9] += 1
            elif bin_vel == "A" and item_vel == "C":
                sbin4[4] += 1
                sbin4[5] += 1
                sbin4[10] += 1
            elif bin_vel == "A" and item_vel == "D":
                sbin4[4] += 1
                sbin4[5] += 1
                sbin4[11] += 1
            elif bin_vel == "B" and item_vel == "A":
                sbin4[4] += 1
                sbin4[6] += 1
                sbin4[12] += 1
            elif bin_vel == "B" and item_vel == "C":
                sbin4[4] += 1
                sbin4[6] += 1
                sbin4[13] += 1
            elif bin_vel == "B" and item_vel == "D":
                sbin4[4] += 1
                sbin4[6] += 1
                sbin4[14] += 1
            elif bin_vel == "C" and item_vel == "A":
                sbin4[4] += 1
                sbin4[7] += 1
                sbin4[15] += 1
            elif bin_vel == "C" and item_vel == "B":
                sbin4[4] += 1
                sbin4[7] += 1
                sbin4[16] += 1
            elif bin_vel == "C" and item_vel == "D":
                sbin4[4] += 1
                sbin4[7] += 1
                sbin4[17] += 1
            elif bin_vel == "D" and item_vel == "A":
                sbin4[4] += 1
                sbin4[8] += 1
                sbin4[18] += 1
            elif bin_vel == "D" and item_vel == "B":
                sbin4[4] += 1
                sbin4[8] += 1
                sbin4[19] += 1
            elif bin_vel == "D" and item_vel == "C":
                sbin4[4] += 1
                sbin4[8] += 1
                sbin4[20] += 1
        elif size == "S BIN 5":
            if bin_vel == "A" and item_vel == "B":
                sbin5[4] += 1
                sbin5[5] += 1
                sbin5[9] += 1
            elif bin_vel == "A" and item_vel == "C":
                sbin5[4] += 1
                sbin5[5] += 1
                sbin5[10] += 1
            elif bin_vel == "A" and item_vel == "D":
                sbin5[4] += 1
                sbin5[5] += 1
                sbin5[11] += 1
            elif bin_vel == "B" and item_vel == "A":
                sbin5[4] += 1
                sbin5[6] += 1
                sbin5[12] += 1
            elif bin_vel == "B" and item_vel == "C":
                sbin5[4] += 1
                sbin5[6] += 1
                sbin5[13] += 1
            elif bin_vel == "B" and item_vel == "D":
                sbin5[4] += 1
                sbin5[6] += 1
                sbin5[14] += 1
            elif bin_vel == "C" and item_vel == "A":
                sbin5[4] += 1
                sbin5[7] += 1
                sbin5[15] += 1
            elif bin_vel == "C" and item_vel == "B":
                sbin5[4] += 1
                sbin5[7] += 1
                sbin5[16] += 1
            elif bin_vel == "C" and item_vel == "D":
                sbin5[4] += 1
                sbin5[7] += 1
                sbin5[17] += 1
            elif bin_vel == "D" and item_vel == "A":
                sbin5[4] += 1
                sbin5[8] += 1
                sbin5[18] += 1
            elif bin_vel == "D" and item_vel == "B":
                sbin5[4] += 1
                sbin5[8] += 1
                sbin5[19] += 1
            elif bin_vel == "D" and item_vel == "C":
                sbin5[4] += 1
                sbin5[8] += 1
                sbin5[20] += 1
        elif size == "L BIN 1":
            if bin_vel == "A" and item_vel == "B":
                lbin1[4] += 1
                lbin1[5] += 1
                lbin1[9] += 1
            elif bin_vel == "A" and item_vel == "C":
                lbin1[4] += 1
                lbin1[5] += 1
                lbin1[10] += 1
            elif bin_vel == "A" and item_vel == "D":
                lbin1[4] += 1
                lbin1[5] += 1
                lbin1[11] += 1
            elif bin_vel == "B" and item_vel == "A":
                lbin1[4] += 1
                lbin1[6] += 1
                lbin1[12] += 1
            elif bin_vel == "B" and item_vel == "C":
                lbin1[4] += 1
                lbin1[6] += 1
                lbin1[13] += 1
            elif bin_vel == "B" and item_vel == "D":
                lbin1[4] += 1
                lbin1[6] += 1
                lbin1[14] += 1
            elif bin_vel == "C" and item_vel == "A":
                lbin1[4] += 1
                lbin1[7] += 1
                lbin1[15] += 1
            elif bin_vel == "C" and item_vel == "B":
                lbin1[4] += 1
                lbin1[7] += 1
                lbin1[16] += 1
            elif bin_vel == "C" and item_vel == "D":
                lbin1[4] += 1
                lbin1[7] += 1
                lbin1[17] += 1
            elif bin_vel == "D" and item_vel == "A":
                lbin1[4] += 1
                lbin1[8] += 1
                lbin1[18] += 1
            elif bin_vel == "D" and item_vel == "B":
                lbin1[4] += 1
                lbin1[8] += 1
                lbin1[19] += 1
            elif bin_vel == "D" and item_vel == "C":
                lbin1[4] += 1
                lbin1[8] += 1
                lbin1[20] += 1
        elif size == "L BIN 2":
            if bin_vel == "A" and item_vel == "B":
                lbin2[4] += 1
                lbin2[5] += 1
                lbin2[9] += 1
            elif bin_vel == "A" and item_vel == "C":
                lbin2[4] += 1
                lbin2[5] += 1
                lbin2[10] += 1
            elif bin_vel == "A" and item_vel == "D":
                lbin2[4] += 1
                lbin2[5] += 1
                lbin2[11] += 1
            elif bin_vel == "B" and item_vel == "A":
                lbin2[4] += 1
                lbin2[6] += 1
                lbin2[12] += 1
            elif bin_vel == "B" and item_vel == "C":
                lbin2[4] += 1
                lbin2[6] += 1
                lbin2[13] += 1
            elif bin_vel == "B" and item_vel == "D":
                lbin2[4] += 1
                lbin2[6] += 1
                lbin2[14] += 1
            elif bin_vel == "C" and item_vel == "A":
                lbin2[4] += 1
                lbin2[7] += 1
                lbin2[15] += 1
            elif bin_vel == "C" and item_vel == "B":
                lbin2[4] += 1
                lbin2[7] += 1
                lbin2[16] += 1
            elif bin_vel == "C" and item_vel == "D":
                lbin2[4] += 1
                lbin2[7] += 1
                lbin2[17] += 1
            elif bin_vel == "D" and item_vel == "A":
                lbin2[4] += 1
                lbin2[8] += 1
                lbin2[18] += 1
            elif bin_vel == "D" and item_vel == "B":
                lbin2[4] += 1
                lbin2[8] += 1
                lbin2[19] += 1
            elif bin_vel == "D" and item_vel == "C":
                lbin2[4] += 1
                lbin2[8] += 1
                lbin2[20] += 1
        elif size == "L BIN 3":
            if bin_vel == "A" and item_vel == "B":
                lbin3[4] += 1
                lbin3[5] += 1
                lbin3[9] += 1
            elif bin_vel == "A" and item_vel == "C":
                lbin3[4] += 1
                lbin3[5] += 1
                lbin3[10] += 1
            elif bin_vel == "A" and item_vel == "D":
                lbin3[4] += 1
                lbin3[5] += 1
                lbin3[11] += 1
            elif bin_vel == "B" and item_vel == "A":
                lbin3[4] += 1
                lbin3[6] += 1
                lbin3[12] += 1
            elif bin_vel == "B" and item_vel == "C":
                lbin3[4] += 1
                lbin3[6] += 1
                lbin3[13] += 1
            elif bin_vel == "B" and item_vel == "D":
                lbin3[4] += 1
                lbin3[6] += 1
                lbin3[14] += 1
            elif bin_vel == "C" and item_vel == "A":
                lbin3[4] += 1
                lbin3[7] += 1
                lbin3[15] += 1
            elif bin_vel == "C" and item_vel == "B":
                lbin3[4] += 1
                lbin3[7] += 1
                lbin3[16] += 1
            elif bin_vel == "C" and item_vel == "D":
                lbin3[4] += 1
                lbin3[7] += 1
                lbin3[17] += 1
            elif bin_vel == "D" and item_vel == "A":
                lbin3[4] += 1
                lbin3[8] += 1
                lbin3[18] += 1
            elif bin_vel == "D" and item_vel == "B":
                lbin3[4] += 1
                lbin3[8] += 1
                lbin3[19] += 1
            elif bin_vel == "D" and item_vel == "C":
                lbin3[4] += 1
                lbin3[8] += 1
                lbin3[20] += 1
        elif size == "L BIN 4":
            if bin_vel == "A" and item_vel == "B":
                lbin4[4] += 1
                lbin4[5] += 1
                lbin4[9] += 1
            elif bin_vel == "A" and item_vel == "C":
                lbin4[4] += 1
                lbin4[5] += 1
                lbin4[10] += 1
            elif bin_vel == "A" and item_vel == "D":
                lbin4[4] += 1
                lbin4[5] += 1
                lbin4[11] += 1
            elif bin_vel == "B" and item_vel == "A":
                lbin4[4] += 1
                lbin4[6] += 1
                lbin4[12] += 1
            elif bin_vel == "B" and item_vel == "C":
                lbin4[4] += 1
                lbin4[6] += 1
                lbin4[13] += 1
            elif bin_vel == "B" and item_vel == "D":
                lbin4[4] += 1
                lbin4[6] += 1
                lbin4[14] += 1
            elif bin_vel == "C" and item_vel == "A":
                lbin4[4] += 1
                lbin4[7] += 1
                lbin4[15] += 1
            elif bin_vel == "C" and item_vel == "B":
                lbin4[4] += 1
                lbin4[7] += 1
                lbin4[16] += 1
            elif bin_vel == "C" and item_vel == "D":
                lbin4[4] += 1
                lbin4[7] += 1
                lbin4[17] += 1
            elif bin_vel == "D" and item_vel == "A":
                lbin4[4] += 1
                lbin4[8] += 1
                lbin4[18] += 1
            elif bin_vel == "D" and item_vel == "B":
                lbin4[4] += 1
                lbin4[8] += 1
                lbin4[19] += 1
            elif bin_vel == "D" and item_vel == "C":
                lbin4[4] += 1
                lbin4[8] += 1
                lbin4[20] += 1
        elif size == "L BIN 5":
            if bin_vel == "A" and item_vel == "B":
                lbin5[4] += 1
                lbin5[5] += 1
                lbin5[9] += 1
            elif bin_vel == "A" and item_vel == "C":
                lbin5[4] += 1
                lbin5[5] += 1
                lbin5[10] += 1
            elif bin_vel == "A" and item_vel == "D":
                lbin5[4] += 1
                lbin5[5] += 1
                lbin5[11] += 1
            elif bin_vel == "B" and item_vel == "A":
                lbin5[4] += 1
                lbin5[6] += 1
                lbin5[12] += 1
            elif bin_vel == "B" and item_vel == "C":
                lbin5[4] += 1
                lbin5[6] += 1
                lbin5[13] += 1
            elif bin_vel == "B" and item_vel == "D":
                lbin5[4] += 1
                lbin5[6] += 1
                lbin5[14] += 1
            elif bin_vel == "C" and item_vel == "A":
                lbin5[4] += 1
                lbin5[7] += 1
                lbin5[15] += 1
            elif bin_vel == "C" and item_vel == "B":
                lbin5[4] += 1
                lbin5[7] += 1
                lbin5[16] += 1
            elif bin_vel == "C" and item_vel == "D":
                lbin5[4] += 1
                lbin5[7] += 1
                lbin5[17] += 1
            elif bin_vel == "D" and item_vel == "A":
                lbin5[4] += 1
                lbin5[8] += 1
                lbin5[18] += 1
            elif bin_vel == "D" and item_vel == "B":
                lbin5[4] += 1
                lbin5[8] += 1
                lbin5[19] += 1
            elif bin_vel == "D" and item_vel == "C":
                lbin5[4] += 1
                lbin5[8] += 1
                lbin5[20] += 1
        elif size == "L BIN 6":
            if bin_vel == "A" and item_vel == "B":
                lbin6[4] += 1
                lbin6[5] += 1
                lbin6[9] += 1
            elif bin_vel == "A" and item_vel == "C":
                lbin6[4] += 1
                lbin6[5] += 1
                lbin6[10] += 1
            elif bin_vel == "A" and item_vel == "D":
                lbin6[4] += 1
                lbin6[5] += 1
                lbin6[11] += 1
            elif bin_vel == "B" and item_vel == "A":
                lbin6[4] += 1
                lbin6[6] += 1
                lbin6[12] += 1
            elif bin_vel == "B" and item_vel == "C":
                lbin6[4] += 1
                lbin6[6] += 1
                lbin6[13] += 1
            elif bin_vel == "B" and item_vel == "D":
                lbin6[4] += 1
                lbin6[6] += 1
                lbin6[14] += 1
            elif bin_vel == "C" and item_vel == "A":
                lbin6[4] += 1
                lbin6[7] += 1
                lbin6[15] += 1
            elif bin_vel == "C" and item_vel == "B":
                lbin6[4] += 1
                lbin6[7] += 1
                lbin6[16] += 1
            elif bin_vel == "C" and item_vel == "D":
                lbin6[4] += 1
                lbin6[7] += 1
                lbin6[17] += 1
            elif bin_vel == "D" and item_vel == "A":
                lbin6[4] += 1
                lbin6[8] += 1
                lbin6[18] += 1
            elif bin_vel == "D" and item_vel == "B":
                lbin6[4] += 1
                lbin6[8] += 1
                lbin6[19] += 1
            elif bin_vel == "D" and item_vel == "C":
                lbin6[4] += 1
                lbin6[8] += 1
                lbin6[20] += 1
        elif size == "S PALLET":
            if bin_vel == "A" and item_vel == "B":
                spallet[4] += 1
                spallet[5] += 1
                spallet[9] += 1
            elif bin_vel == "A" and item_vel == "C":
                spallet[4] += 1
                spallet[5] += 1
                spallet[10] += 1
            elif bin_vel == "A" and item_vel == "D":
                spallet[4] += 1
                spallet[5] += 1
                spallet[11] += 1
            elif bin_vel == "B" and item_vel == "A":
                spallet[4] += 1
                spallet[6] += 1
                spallet[12] += 1
            elif bin_vel == "B" and item_vel == "C":
                spallet[4] += 1
                spallet[6] += 1
                spallet[13] += 1
            elif bin_vel == "B" and item_vel == "D":
                spallet[4] += 1
                spallet[6] += 1
                spallet[14] += 1
            elif bin_vel == "C" and item_vel == "A":
                spallet[4] += 1
                spallet[7] += 1
                spallet[15] += 1
            elif bin_vel == "C" and item_vel == "B":
                spallet[4] += 1
                spallet[7] += 1
                spallet[16] += 1
            elif bin_vel == "C" and item_vel == "D":
                spallet[4] += 1
                spallet[7] += 1
                spallet[17] += 1
            elif bin_vel == "D" and item_vel == "A":
                spallet[4] += 1
                spallet[8] += 1
                spallet[18] += 1
            elif bin_vel == "D" and item_vel == "B":
                spallet[4] += 1
                spallet[8] += 1
                spallet[19] += 1
            elif bin_vel == "D" and item_vel == "C":
                spallet[4] += 1
                spallet[8] += 1
                spallet[20] += 1
        elif size == "L PALLET":
            if bin_vel == "A" and item_vel == "B":
                lpallet[4] += 1
                lpallet[5] += 1
                lpallet[9] += 1
            elif bin_vel == "A" and item_vel == "C":
                lpallet[4] += 1
                lpallet[5] += 1
                lpallet[10] += 1
            elif bin_vel == "A" and item_vel == "D":
                lpallet[4] += 1
                lpallet[5] += 1
                lpallet[11] += 1
            elif bin_vel == "B" and item_vel == "A":
                lpallet[4] += 1
                lpallet[6] += 1
                lpallet[12] += 1
            elif bin_vel == "B" and item_vel == "C":
                lpallet[4] += 1
                lpallet[6] += 1
                lpallet[13] += 1
            elif bin_vel == "B" and item_vel == "D":
                lpallet[4] += 1
                lpallet[6] += 1
                lpallet[14] += 1
            elif bin_vel == "C" and item_vel == "A":
                lpallet[4] += 1
                lpallet[7] += 1
                lpallet[15] += 1
            elif bin_vel == "C" and item_vel == "B":
                lpallet[4] += 1
                lpallet[7] += 1
                lpallet[16] += 1
            elif bin_vel == "C" and item_vel == "D":
                lpallet[4] += 1
                lpallet[7] += 1
                lpallet[17] += 1
            elif bin_vel == "D" and item_vel == "A":
                lpallet[4] += 1
                lpallet[8] += 1
                lpallet[18] += 1
            elif bin_vel == "D" and item_vel == "B":
                lpallet[4] += 1
                lpallet[8] += 1
                lpallet[19] += 1
            elif bin_vel == "D" and item_vel == "C":
                lpallet[4] += 1
                lpallet[8] += 1
                lpallet[20] += 1
        elif size == "L SHELF":
            if bin_vel == "A" and item_vel == "B":
                lshelf[4] += 1
                lshelf[5] += 1
                lshelf[9] += 1
            elif bin_vel == "A" and item_vel == "C":
                lshelf[4] += 1
                lshelf[5] += 1
                lshelf[10] += 1
            elif bin_vel == "A" and item_vel == "D":
                lshelf[4] += 1
                lshelf[5] += 1
                lshelf[11] += 1
            elif bin_vel == "B" and item_vel == "A":
                lshelf[4] += 1
                lshelf[6] += 1
                lshelf[12] += 1
            elif bin_vel == "B" and item_vel == "C":
                lshelf[4] += 1
                lshelf[6] += 1
                lshelf[13] += 1
            elif bin_vel == "B" and item_vel == "D":
                lshelf[4] += 1
                lshelf[6] += 1
                lshelf[14] += 1
            elif bin_vel == "C" and item_vel == "A":
                lshelf[4] += 1
                lshelf[7] += 1
                lshelf[15] += 1
            elif bin_vel == "C" and item_vel == "B":
                lshelf[4] += 1
                lshelf[7] += 1
                lshelf[16] += 1
            elif bin_vel == "C" and item_vel == "D":
                lshelf[4] += 1
                lshelf[7] += 1
                lshelf[17] += 1
            elif bin_vel == "D" and item_vel == "A":
                lshelf[4] += 1
                lshelf[8] += 1
                lshelf[18] += 1
            elif bin_vel == "D" and item_vel == "B":
                lshelf[4] += 1
                lshelf[8] += 1
                lshelf[19] += 1
            elif bin_vel == "D" and item_vel == "C":
                lshelf[4] += 1
                lshelf[8] += 1
                lshelf[20] += 1
        elif size == "LONG":
            if bin_vel == "A" and item_vel == "B":
                long[4] += 1
                long[5] += 1
                long[9] += 1
            elif bin_vel == "A" and item_vel == "C":
                long[4] += 1
                long[5] += 1
                long[10] += 1
            elif bin_vel == "A" and item_vel == "D":
                long[4] += 1
                long[5] += 1
                long[11] += 1
            elif bin_vel == "B" and item_vel == "A":
                long[4] += 1
                long[6] += 1
                long[12] += 1
            elif bin_vel == "B" and item_vel == "C":
                long[4] += 1
                long[6] += 1
                long[13] += 1
            elif bin_vel == "B" and item_vel == "D":
                long[4] += 1
                long[6] += 1
                long[14] += 1
            elif bin_vel == "C" and item_vel == "A":
                long[4] += 1
                long[7] += 1
                long[15] += 1
            elif bin_vel == "C" and item_vel == "B":
                long[4] += 1
                long[7] += 1
                long[16] += 1
            elif bin_vel == "C" and item_vel == "D":
                long[4] += 1
                long[7] += 1
                long[17] += 1
            elif bin_vel == "D" and item_vel == "A":
                long[4] += 1
                long[8] += 1
                long[18] += 1
            elif bin_vel == "D" and item_vel == "B":
                long[4] += 1
                long[8] += 1
                long[19] += 1
            elif bin_vel == "D" and item_vel == "C":
                long[4] += 1
                long[8] += 1
                long[20] += 1
        else: #XLpallet
            if bin_vel == "A" and item_vel == "B":
                xlpallet[4] += 1
                xlpallet[5] += 1
                xlpallet[9] += 1
            elif bin_vel == "A" and item_vel == "C":
                xlpallet[4] += 1
                xlpallet[5] += 1
                xlpallet[10] += 1
            elif bin_vel == "A" and item_vel == "D":
                xlpallet[4] += 1
                xlpallet[5] += 1
                xlpallet[11] += 1
            elif bin_vel == "B" and item_vel == "A":
                xlpallet[4] += 1
                xlpallet[6] += 1
                xlpallet[12] += 1
            elif bin_vel == "B" and item_vel == "C":
                xlpallet[4] += 1
                xlpallet[6] += 1
                xlpallet[13] += 1
            elif bin_vel == "B" and item_vel == "D":
                xlpallet[4] += 1
                xlpallet[6] += 1
                xlpallet[14] += 1
            elif bin_vel == "C" and item_vel == "A":
                xlpallet[4] += 1
                xlpallet[7] += 1
                xlpallet[15] += 1
            elif bin_vel == "C" and item_vel == "B":
                xlpallet[4] += 1
                xlpallet[7] += 1
                xlpallet[16] += 1
            elif bin_vel == "C" and item_vel == "D":
                xlpallet[4] += 1
                xlpallet[7] += 1
                xlpallet[17] += 1
            elif bin_vel == "D" and item_vel == "A":
                xlpallet[4] += 1
                xlpallet[8] += 1
                xlpallet[18] += 1
            elif bin_vel == "D" and item_vel == "B":
                xlpallet[4] += 1
                xlpallet[8] += 1
                xlpallet[19] += 1
            elif bin_vel == "D" and item_vel == "C":
                xlpallet[4] += 1
                xlpallet[8] += 1
                xlpallet[20] += 1
        i -= 1

    # slotting.loc[0, "AVelocityNobin"] = xs[0]
    # slotting.loc[0, "BVelocityNobin"] = xs[1]
    # slotting.loc[0, "CVelocityNobin"] = xs[2]
    # slotting.loc[0, "DVelocityNobin"] = xs[3]
    # slotting.loc[0, "TotalToMove"] = xs[4]
    # slotting.loc[0, "TotalA"] = xs[5]
    # slotting.loc[0, "TotalB"] = xs[6]
    # slotting.loc[0, "TotalC"] = xs[7]
    # slotting.loc[0, "TotalD"] = xs[8]
    # slotting.loc[0, "AtoB"] = xs[9]
    # slotting.loc[0, "AtoC"] = xs[10]
    # slotting.loc[0, "AtoD"] = xs[11]
    # slotting.loc[0, "BtoA"] = xs[12]
    # slotting.loc[0, "BtoC"] = xs[13]
    # slotting.loc[0, "BtoD"] = xs[14]
    # slotting.loc[0, "CtoA"] = xs[15]
    # slotting.loc[0, "CtoB"] = xs[16]
    # slotting.loc[0, "CtoD"] = xs[17]
    # slotting.loc[0, "DtoA"] = xs[18]
    # slotting.loc[0, "DtoB"] = xs[19]
    # slotting.loc[0, "DtoC"] = xs[20]
    
    # slotting.loc[1, "AVelocityNobin"] = sbin1[0]
    # slotting.loc[1, "BVelocityNobin"] = sbin1[1]
    # slotting.loc[1, "CVelocityNobin"] = sbin1[2]
    # slotting.loc[1, "DVelocityNobin"] = sbin1[3]
    # slotting.loc[1, "TotalToMove"] = sbin1[4]
    # slotting.loc[1, "TotalA"] = sbin1[5]
    # slotting.loc[1, "TotalB"] = sbin1[6]
    # slotting.loc[1, "TotalC"] = sbin1[7]
    # slotting.loc[1, "TotalD"] = sbin1[8]
    # slotting.loc[1, "AtoB"] = sbin1[9]
    # slotting.loc[1, "AtoC"] = sbin1[10]
    # slotting.loc[1, "AtoD"] = sbin1[11]
    # slotting.loc[1, "BtoA"] = sbin1[12]
    # slotting.loc[1, "BtoC"] = sbin1[13]
    # slotting.loc[1, "BtoD"] = sbin1[14]
    # slotting.loc[1, "CtoA"] = sbin1[15]
    # slotting.loc[1, "CtoB"] = sbin1[16]
    # slotting.loc[1, "CtoD"] = sbin1[17]
    # slotting.loc[1, "DtoA"] = sbin1[18]
    # slotting.loc[1, "DtoB"] = sbin1[19]
    # slotting.loc[1, "DtoC"] = sbin1[20]

    # slotting.loc[2, "AVelocityNobin"] = sbin2[0]
    # slotting.loc[2, "BVelocityNobin"] = sbin2[1]
    # slotting.loc[2, "CVelocityNobin"] = sbin2[2]
    # slotting.loc[2, "DVelocityNobin"] = sbin2[3]
    # slotting.loc[2, "TotalToMove"] = sbin2[4]
    # slotting.loc[2, "TotalA"] = sbin2[5]
    # slotting.loc[2, "TotalB"] = sbin2[6]
    # slotting.loc[2, "TotalC"] = sbin2[7]
    # slotting.loc[2, "TotalD"] = sbin2[8]
    # slotting.loc[2, "AtoB"] = sbin2[9]
    # slotting.loc[2, "AtoC"] = sbin2[10]
    # slotting.loc[2, "AtoD"] = sbin2[11]
    # slotting.loc[2, "BtoA"] = sbin2[12]
    # slotting.loc[2, "BtoC"] = sbin2[13]
    # slotting.loc[2, "BtoD"] = sbin2[14]
    # slotting.loc[2, "CtoA"] = sbin2[15]
    # slotting.loc[2, "CtoB"] = sbin2[16]
    # slotting.loc[2, "CtoD"] = sbin2[17]
    # slotting.loc[2, "DtoA"] = sbin2[18]
    # slotting.loc[2, "DtoB"] = sbin2[19]
    # slotting.loc[2, "DtoC"] = sbin2[20]

    # slotting.loc[3, "AVelocityNobin"] = sbin3[0]
    # slotting.loc[3, "BVelocityNobin"] = sbin3[1]
    # slotting.loc[3, "CVelocityNobin"] = sbin3[2]
    # slotting.loc[3, "DVelocityNobin"] = sbin3[3]
    # slotting.loc[3, "TotalToMove"] = sbin3[4]
    # slotting.loc[3, "TotalA"] = sbin3[5]
    # slotting.loc[3, "TotalB"] = sbin3[6]
    # slotting.loc[3, "TotalC"] = sbin3[7]
    # slotting.loc[3, "TotalD"] = sbin3[8]
    # slotting.loc[3, "AtoB"] = sbin3[9]
    # slotting.loc[3, "AtoC"] = sbin3[10]
    # slotting.loc[3, "AtoD"] = sbin3[11]
    # slotting.loc[3, "BtoA"] = sbin3[12]
    # slotting.loc[3, "BtoC"] = sbin3[13]
    # slotting.loc[3, "BtoD"] = sbin3[14]
    # slotting.loc[3, "CtoA"] = sbin3[15]
    # slotting.loc[3, "CtoB"] = sbin3[16]
    # slotting.loc[3, "CtoD"] = sbin3[17]
    # slotting.loc[3, "DtoA"] = sbin3[18]
    # slotting.loc[3, "DtoB"] = sbin3[19]
    # slotting.loc[3, "DtoC"] = sbin3[20]

    # slotting.loc[4, "AVelocityNobin"] = sbin4[0]
    # slotting.loc[4, "BVelocityNobin"] = sbin4[1]
    # slotting.loc[4, "CVelocityNobin"] = sbin4[2]
    # slotting.loc[4, "DVelocityNobin"] = sbin4[3]
    # slotting.loc[4, "TotalToMove"] = sbin4[4]
    # slotting.loc[4, "TotalA"] = sbin4[5]
    # slotting.loc[4, "TotalB"] = sbin4[6]
    # slotting.loc[4, "TotalC"] = sbin4[7]
    # slotting.loc[4, "TotalD"] = sbin4[8]
    # slotting.loc[4, "AtoB"] = sbin4[9]
    # slotting.loc[4, "AtoC"] = sbin4[10]
    # slotting.loc[4, "AtoD"] = sbin4[11]
    # slotting.loc[4, "BtoA"] = sbin4[12]
    # slotting.loc[4, "BtoC"] = sbin4[13]
    # slotting.loc[4, "BtoD"] = sbin4[14]
    # slotting.loc[4, "CtoA"] = sbin4[15]
    # slotting.loc[4, "CtoB"] = sbin4[16]
    # slotting.loc[4, "CtoD"] = sbin4[17]
    # slotting.loc[4, "DtoA"] = sbin4[18]
    # slotting.loc[4, "DtoB"] = sbin4[19]
    # slotting.loc[4, "DtoC"] = sbin4[20]

    # slotting.loc[5, "AVelocityNobin"] = sbin5[0]
    # slotting.loc[5, "BVelocityNobin"] = sbin5[1]
    # slotting.loc[5, "CVelocityNobin"] = sbin5[2]
    # slotting.loc[5, "DVelocityNobin"] = sbin5[3]
    # slotting.loc[5, "TotalToMove"] = sbin5[4]
    # slotting.loc[5, "TotalA"] = sbin5[5]
    # slotting.loc[5, "TotalB"] = sbin5[6]
    # slotting.loc[5, "TotalC"] = sbin5[7]
    # slotting.loc[5, "TotalD"] = sbin5[8]
    # slotting.loc[5, "AtoB"] = sbin5[9]
    # slotting.loc[5, "AtoC"] = sbin5[10]
    # slotting.loc[5, "AtoD"] = sbin5[11]
    # slotting.loc[5, "BtoA"] = sbin5[12]
    # slotting.loc[5, "BtoC"] = sbin5[13]
    # slotting.loc[5, "BtoD"] = sbin5[14]
    # slotting.loc[5, "CtoA"] = sbin5[15]
    # slotting.loc[5, "CtoB"] = sbin5[16]
    # slotting.loc[5, "CtoD"] = sbin5[17]
    # slotting.loc[5, "DtoA"] = sbin5[18]
    # slotting.loc[5, "DtoB"] = sbin5[19]
    # slotting.loc[5, "DtoC"] = sbin5[20]

    # slotting.loc[6, "AVelocityNobin"] = lbin1[0]
    # slotting.loc[6, "BVelocityNobin"] = lbin1[1]
    # slotting.loc[6, "CVelocityNobin"] = lbin1[2]
    # slotting.loc[6, "DVelocityNobin"] = lbin1[3]
    # slotting.loc[6, "TotalToMove"] = lbin1[4]
    # slotting.loc[6, "TotalA"] = lbin1[5]
    # slotting.loc[6, "TotalB"] = lbin1[6]
    # slotting.loc[6, "TotalC"] = lbin1[7]
    # slotting.loc[6, "TotalD"] = lbin1[8]
    # slotting.loc[6, "AtoB"] = lbin1[9]
    # slotting.loc[6, "AtoC"] = lbin1[10]
    # slotting.loc[6, "AtoD"] = lbin1[11]
    # slotting.loc[6, "BtoA"] = lbin1[12]
    # slotting.loc[6, "BtoC"] = lbin1[13]
    # slotting.loc[6, "BtoD"] = lbin1[14]
    # slotting.loc[6, "CtoA"] = lbin1[15]
    # slotting.loc[6, "CtoB"] = lbin1[16]
    # slotting.loc[6, "CtoD"] = lbin1[17]
    # slotting.loc[6, "DtoA"] = lbin1[18]
    # slotting.loc[6, "DtoB"] = lbin1[19]
    # slotting.loc[6, "DtoC"] = lbin1[20]

    # slotting.loc[7, "AVelocityNobin"] = lbin2[0]
    # slotting.loc[7, "BVelocityNobin"] = lbin2[1]
    # slotting.loc[7, "CVelocityNobin"] = lbin2[2]
    # slotting.loc[7, "DVelocityNobin"] = lbin2[3]
    # slotting.loc[7, "TotalToMove"] = lbin2[4]
    # slotting.loc[7, "TotalA"] = lbin2[5]
    # slotting.loc[7, "TotalB"] = lbin2[6]
    # slotting.loc[7, "TotalC"] = lbin2[7]
    # slotting.loc[7, "TotalD"] = lbin2[8]
    # slotting.loc[7, "AtoB"] = lbin2[9]
    # slotting.loc[7, "AtoC"] = lbin2[10]
    # slotting.loc[7, "AtoD"] = lbin2[11]
    # slotting.loc[7, "BtoA"] = lbin2[12]
    # slotting.loc[7, "BtoC"] = lbin2[13]
    # slotting.loc[7, "BtoD"] = lbin2[14]
    # slotting.loc[7, "CtoA"] = lbin2[15]
    # slotting.loc[7, "CtoB"] = lbin2[16]
    # slotting.loc[7, "CtoD"] = lbin2[17]
    # slotting.loc[7, "DtoA"] = lbin2[18]
    # slotting.loc[7, "DtoB"] = lbin2[19]
    # slotting.loc[7, "DtoC"] = lbin2[20]

    # slotting.loc[8, "AVelocityNobin"] = lbin3[0]
    # slotting.loc[8, "BVelocityNobin"] = lbin3[1]
    # slotting.loc[8, "CVelocityNobin"] = lbin3[2]
    # slotting.loc[8, "DVelocityNobin"] = lbin3[3]
    # slotting.loc[8, "TotalToMove"] = lbin3[4]
    # slotting.loc[8, "TotalA"] = lbin3[5]
    # slotting.loc[8, "TotalB"] = lbin3[6]
    # slotting.loc[8, "TotalC"] = lbin3[7]
    # slotting.loc[8, "TotalD"] = lbin3[8]
    # slotting.loc[8, "AtoB"] = lbin3[9]
    # slotting.loc[8, "AtoC"] = lbin3[10]
    # slotting.loc[8, "AtoD"] = lbin3[11]
    # slotting.loc[8, "BtoA"] = lbin3[12]
    # slotting.loc[8, "BtoC"] = lbin3[13]
    # slotting.loc[8, "BtoD"] = lbin3[14]
    # slotting.loc[8, "CtoA"] = lbin3[15]
    # slotting.loc[8, "CtoB"] = lbin3[16]
    # slotting.loc[8, "CtoD"] = lbin3[17]
    # slotting.loc[8, "DtoA"] = lbin3[18]
    # slotting.loc[8, "DtoB"] = lbin3[19]
    # slotting.loc[8, "DtoC"] = lbin3[20]

    # slotting.loc[9, "AVelocityNobin"] = lbin4[0]
    # slotting.loc[9, "BVelocityNobin"] = lbin4[1]
    # slotting.loc[9, "CVelocityNobin"] = lbin4[2]
    # slotting.loc[9, "DVelocityNobin"] = lbin4[3]
    # slotting.loc[9, "TotalToMove"] = lbin4[4]
    # slotting.loc[9, "TotalA"] = lbin4[5]
    # slotting.loc[9, "TotalB"] = lbin4[6]
    # slotting.loc[9, "TotalC"] = lbin4[7]
    # slotting.loc[9, "TotalD"] = lbin4[8]
    # slotting.loc[9, "AtoB"] = lbin4[9]
    # slotting.loc[9, "AtoC"] = lbin4[10]
    # slotting.loc[9, "AtoD"] = lbin4[11]
    # slotting.loc[9, "BtoA"] = lbin4[12]
    # slotting.loc[9, "BtoC"] = lbin4[13]
    # slotting.loc[9, "BtoD"] = lbin4[14]
    # slotting.loc[9, "CtoA"] = lbin4[15]
    # slotting.loc[9, "CtoB"] = lbin4[16]
    # slotting.loc[9, "CtoD"] = lbin4[17]
    # slotting.loc[9, "DtoA"] = lbin4[18]
    # slotting.loc[9, "DtoB"] = lbin4[19]
    # slotting.loc[9, "DtoC"] = lbin4[20]

    # slotting.loc[10, "AVelocityNobin"] = lbin5[0]
    # slotting.loc[10, "BVelocityNobin"] = lbin5[1]
    # slotting.loc[10, "CVelocityNobin"] = lbin5[2]
    # slotting.loc[10, "DVelocityNobin"] = lbin5[3]
    # slotting.loc[10, "TotalToMove"] = lbin5[4]
    # slotting.loc[10, "TotalA"] = lbin5[5]
    # slotting.loc[10, "TotalB"] = lbin5[6]
    # slotting.loc[10, "TotalC"] = lbin5[7]
    # slotting.loc[10, "TotalD"] = lbin5[8]
    # slotting.loc[10, "AtoB"] = lbin5[9]
    # slotting.loc[10, "AtoC"] = lbin5[10]
    # slotting.loc[10, "AtoD"] = lbin5[11]
    # slotting.loc[10, "BtoA"] = lbin5[12]
    # slotting.loc[10, "BtoC"] = lbin5[13]
    # slotting.loc[10, "BtoD"] = lbin5[14]
    # slotting.loc[10, "CtoA"] = lbin5[15]
    # slotting.loc[10, "CtoB"] = lbin5[16]
    # slotting.loc[10, "CtoD"] = lbin5[17]
    # slotting.loc[10, "DtoA"] = lbin5[18]
    # slotting.loc[10, "DtoB"] = lbin5[19]
    # slotting.loc[10, "DtoC"] = lbin5[20]

    # slotting.loc[14, "AVelocityNobin"] = spallet[0]
    # slotting.loc[14, "BVelocityNobin"] = spallet[1]
    # slotting.loc[14, "CVelocityNobin"] = spallet[2]
    # slotting.loc[14, "DVelocityNobin"] = spallet[3]
    # slotting.loc[14, "TotalToMove"] = spallet[4]
    # slotting.loc[14, "TotalA"] = spallet[5]
    # slotting.loc[14, "TotalB"] = spallet[6]
    # slotting.loc[14, "TotalC"] = spallet[7]
    # slotting.loc[14, "TotalD"] = spallet[8]
    # slotting.loc[14, "AtoB"] = spallet[9]
    # slotting.loc[14, "AtoC"] = spallet[10]
    # slotting.loc[14, "AtoD"] = spallet[11]
    # slotting.loc[14, "BtoA"] = spallet[12]
    # slotting.loc[14, "BtoC"] = spallet[13]
    # slotting.loc[14, "BtoD"] = spallet[14]
    # slotting.loc[14, "CtoA"] = spallet[15]
    # slotting.loc[14, "CtoB"] = spallet[16]
    # slotting.loc[14, "CtoD"] = spallet[17]
    # slotting.loc[14, "DtoA"] = spallet[18]
    # slotting.loc[14, "DtoB"] = spallet[19]
    # slotting.loc[14, "DtoC"] = spallet[20]

    # slotting.loc[15, "AVelocityNobin"] = lpallet[0]
    # slotting.loc[15, "BVelocityNobin"] = lpallet[1]
    # slotting.loc[15, "CVelocityNobin"] = lpallet[2]
    # slotting.loc[15, "DVelocityNobin"] = lpallet[3]
    # slotting.loc[15, "TotalToMove"] = lpallet[4]
    # slotting.loc[15, "TotalA"] = lpallet[5]
    # slotting.loc[15, "TotalB"] = lpallet[6]
    # slotting.loc[15, "TotalC"] = lpallet[7]
    # slotting.loc[15, "TotalD"] = lpallet[8]
    # slotting.loc[15, "AtoB"] = lpallet[9]
    # slotting.loc[15, "AtoC"] = lpallet[10]
    # slotting.loc[15, "AtoD"] = lpallet[11]
    # slotting.loc[15, "BtoA"] = lpallet[12]
    # slotting.loc[15, "BtoC"] = lpallet[13]
    # slotting.loc[15, "BtoD"] = lpallet[14]
    # slotting.loc[15, "CtoA"] = lpallet[15]
    # slotting.loc[15, "CtoB"] = lpallet[16]
    # slotting.loc[15, "CtoD"] = lpallet[17]
    # slotting.loc[15, "DtoA"] = lpallet[18]
    # slotting.loc[15, "DtoB"] = lpallet[19]
    # slotting.loc[15, "DtoC"] = lpallet[20]

    # slotting.loc[16, "AVelocityNobin"] = xlpallet[0]
    # slotting.loc[16, "BVelocityNobin"] = xlpallet[1]
    # slotting.loc[16, "CVelocityNobin"] = xlpallet[2]
    # slotting.loc[16, "DVelocityNobin"] = xlpallet[3]
    # slotting.loc[16, "TotalToMove"] = xlpallet[4]
    # slotting.loc[16, "TotalA"] = xlpallet[5]
    # slotting.loc[16, "TotalB"] = xlpallet[6]
    # slotting.loc[16, "TotalC"] = xlpallet[7]
    # slotting.loc[16, "TotalD"] = xlpallet[8]
    # slotting.loc[16, "AtoB"] = xlpallet[9]
    # slotting.loc[16, "AtoC"] = xlpallet[10]
    # slotting.loc[16, "AtoD"] = xlpallet[11]
    # slotting.loc[16, "BtoA"] = xlpallet[12]
    # slotting.loc[16, "BtoC"] = xlpallet[13]
    # slotting.loc[16, "BtoD"] = xlpallet[14]
    # slotting.loc[16, "CtoA"] = xlpallet[15]
    # slotting.loc[16, "CtoB"] = xlpallet[16]
    # slotting.loc[16, "CtoD"] = xlpallet[17]
    # slotting.loc[16, "DtoA"] = xlpallet[18]
    # slotting.loc[16, "DtoB"] = xlpallet[19]
    # slotting.loc[16, "DtoC"] = xlpallet[20]

    # slotting.loc[12, "TotalToMove"] = lshelf[4]
    # slotting.loc[12, "TotalA"] = lshelf[5]
    # slotting.loc[12, "TotalB"] = lshelf[6]
    # slotting.loc[12, "TotalC"] = lshelf[7]
    # slotting.loc[12, "TotalD"] = lshelf[8]
    # slotting.loc[12, "AtoB"] = lshelf[9]
    # slotting.loc[12, "AtoC"] = lshelf[10]
    # slotting.loc[12, "AtoD"] = lshelf[11]
    # slotting.loc[12, "BtoA"] = lshelf[12]
    # slotting.loc[12, "BtoC"] = lshelf[13]
    # slotting.loc[12, "BtoD"] = lshelf[14]
    # slotting.loc[12, "CtoA"] = lshelf[15]
    # slotting.loc[12, "CtoB"] = lshelf[16]
    # slotting.loc[12, "CtoD"] = lshelf[17]
    # slotting.loc[12, "DtoA"] = lshelf[18]
    # slotting.loc[12, "DtoB"] = lshelf[19]
    # slotting.loc[12, "DtoC"] = lshelf[20]

    # slotting.loc[11, "TotalToMove"] = lbin6[4]
    # slotting.loc[11, "TotalA"] = lbin6[5]
    # slotting.loc[11, "TotalB"] = lbin6[6]
    # slotting.loc[11, "TotalC"] = lbin6[7]
    # slotting.loc[11, "TotalD"] = lbin6[8]
    # slotting.loc[11, "AtoB"] = lbin6[9]
    # slotting.loc[11, "AtoC"] = lbin6[10]
    # slotting.loc[11, "AtoD"] = lbin6[11]
    # slotting.loc[11, "BtoA"] = lbin6[12]
    # slotting.loc[11, "BtoC"] = lbin6[13]
    # slotting.loc[11, "BtoD"] = lbin6[14]
    # slotting.loc[11, "CtoA"] = lbin6[15]
    # slotting.loc[11, "CtoB"] = lbin6[16]
    # slotting.loc[11, "CtoD"] = lbin6[17]
    # slotting.loc[11, "DtoA"] = lbin6[18]
    # slotting.loc[11, "DtoB"] = lbin6[19]
    # slotting.loc[11, "DtoC"] = lbin6[20]

    # slotting.loc[17, "TotalToMove"] = long[4]
    # slotting.loc[17, "TotalA"] = long[5]
    # slotting.loc[17, "TotalB"] = long[6]
    # slotting.loc[17, "TotalC"] = long[7]
    # slotting.loc[17, "TotalD"] = long[8]
    # slotting.loc[17, "AtoB"] = long[9]
    # slotting.loc[17, "AtoC"] = long[10]
    # slotting.loc[17, "AtoD"] = long[11]
    # slotting.loc[17, "BtoA"] = long[12]
    # slotting.loc[17, "BtoC"] = long[13]
    # slotting.loc[17, "BtoD"] = long[14]
    # slotting.loc[17, "CtoA"] = long[15]
    # slotting.loc[17, "CtoB"] = long[16]
    # slotting.loc[17, "CtoD"] = long[17]
    # slotting.loc[17, "DtoA"] = long[18]
    # slotting.loc[17, "DtoB"] = long[19]
    # slotting.loc[17, "DtoC"] = long[20]
    
    st.subheader("Bin and Size Class Mismatch")
    st.write(file)
    st.subheader("Velocity Mismatch")
    st.write(file2)
    st.subheader("Open Bins based on Velocity")
    #st.write(slotting)
    
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
    st.write("L SHELF", lshelf)
    st.write("S PALLET", spallet)
    st.write("L PALLET", lpallet)
    st.write("XL PALLET", xlpallet)
    st.write("LONG", long)
