import streamlit as st
import os
import pandas as pd
import openpyxl as op
import io
import xlsxwriter

def get_cube(cube, calc_cube):
    if calc_cube > cube:
        return calc_cube
    else:
        return cube

def calculate_cube(length, width, height):
    return length * width * height

def check_bin(item, bin):
    if item[3] <= bin[3]:
        if item[0] <= bin[0] and item[0] <= bin[1] and item[0] <= bin[2]:
            if item[1] <= bin[0] and item[1] <= bin[1] and item[1] <= bin[2]:
                if item[2] <= bin[0] and item[2] <= bin[1] and item[2] <= bin[2]:
                    return True
    else:
        return False

st.set_page_config(layout="wide")
st.title("Calculate Item Class Size")

file = st.file_uploader("**Inventory File** - upload inventory file", type="xlsx")
#file2 = st.file_uploader("**Slotting File** - upload inventory slotting file", type="xlsx")

#df = pd.read_excel(file)
#df2 = pd.read_excel(file2)

if file is not None:
    #merge_files = df.merge(df2, how='outer', on=['ItemID'])

    #merge_files.to_excel('database.xlsx', index=False)

    # Open files
    database = pd.read_excel(file)

    database['NEWCLASSSIZE'] = ""

    cubic = [120, 240, 360, 480, 600, 720, 1140, 3456, 5184, 51840]

    bins = {
        'X/S (2)': [12,2,5,120],
        'S BIN 1 (4)': [12,4,5,240],
        'S BIN 2 (6)': [12,6,5,360],
        'S BIN 3 (8)': [12,8,5,480],
        'S BIN 4 (10)': [12,10,5,600],
        'S BIN 5 (12)': [12,12,5,720],
        'L BIN 1 (Brown)': [24,6,10,1140],
        'L BIN 2 (White Small)': [24,12,12,3456],
        'L BIN 3 (White Large)': [24,18,12,5184],
        'L BIN 4 (Pallet Bin)': [40,20, 17, 13600],
        'L SHELF (Top Shelf)': [24,60,36,51840]
    }

    open_shelves = {
        'L SHELF (Top Shelf)': [24,60,36,51840],
        'L BIN 6 (Racks)': [48,48,37,85248],
        'XL PALLET': [40, 48, 96, 184320]
    }

    compressors = {
        'S SHELF': [29, 48, 12, 16704],
        'S PALLET': [40, 12, 42, 20160],
        'L PALLET': [40, 42, 42, 70560]
    }

    pallets = {
        'L BIN 1 (Brown)': [24,6,10,1140],
        'L BIN 2 (White Small)': [24,12,12,3456],
        'L BIN 3 (White Large)': [24,18,12,5184],
        'L BIN 4 (Pallet Bin)': [40,20, 17, 13600],
        'L BIN 5 (Rack Bin)': [48,24,36,41472],
        'L PALLET': [40, 42, 42, 70560],
        'XL PALLET': [40, 42, 42, 70560],
        'LONG': [45, 108, 36, 174960]
    }

    i = 0

    ilen = len(database) - 1

    while i <= ilen:

        # Gets cubic dimensions from database
        cube = float(database.loc[i, 'ITEM_CUBE'])

        # Calculate cubic dimensions based on length, width, and height
        calc_cube = calculate_cube(float(database.loc[i, 'ITEMLENGTH']), float(database.loc[i, 'ITEMWIDTH']), float(database.loc[i, 'ITEMHEIGHT']))
        
        # Check wich is greater, calculated cube or cube from database
        cube = get_cube(cube, calc_cube)
        
        # Get quantity on hand and quantity on order
        quantity = float(database.loc[i, 'Quantity'])
        order = float(database.loc[i, 'HostOnPurchaseOrder'])

        # Calculate total cubic measurements cube * total qty
        total = quantity + order
        total = total * cube
        
        # Get all info for item to calculate which bin it fits in
        item = [float(database.loc[i, 'ITEMLENGTH']), float(database.loc[i, 'ITEMWIDTH']), float(database.loc[i, 'ITEMHEIGHT']), total]

        
        for key, (v1, v2, v3, v4) in bins.items():
            bin = [float(v1), float(v2), float(v3), float(v4)]

            if total <= bin[3]:
                check = check_bin(item, bin)
                if check == True:
                    database.loc[i, 'NEWCLASSSIZE'] = key
                    break
                else:
                    continue

        i += 1


    st.write(database)
    # Save database
    #database.to_excel('downsize_list.xlsx', index=False)
