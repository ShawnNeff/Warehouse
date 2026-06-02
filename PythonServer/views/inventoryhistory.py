import streamlit as st
import os
import pandas as pd
#import openpyxl as op
import io
#import xlsxwriter

st.header("---Inventory History - Item Research Tool ---")
st.write("")
st.write("")

descision = st.radio("Information you want to see:", ["Down to Zero", "Every Transaction"], index=None)

onhand = st.text_input("Enter stock on hand: ")

item = st.file_uploader("**Inventory File** - Upload inventory excel file in xlsx format.",type="xlsx")

if item is not None and onhand != "":
    file = pd.read_excel(item)

    # Drop garbage columns
    file.drop(file.columns[[0, 4, 6, 7, 12, 13]], axis=1, inplace=True)

    # Reorder columns, add OnHand column at the end
    file = file[['ItemID', 'LedgerDate', 'UserID', 'TransactionType', 'TransactionNumber', 'SourceBinID', 'BinID', 'Quantity']]
    #file['OnHand'] = ""
    
    quantity = int(onhand)

    # Declare variables to hold transaction types
    transactions = ['ITEM.RECEIVE', 'ITEM.INDUCT', 'ORD.SHIP', 'ITEM.DEDUCT', 'ITEM.RETURN', 'ITEM.UNRECEIVE', 'PHYSINV.POST']
    returns = ['MISSING', 'DAMAGED']

    file.loc[0, 'OnHand'] = quantity
    #file.loc[0, 8] = quantity

    i = 0

    file.loc[i, 'OnHand'] = quantity
    #file.loc[i, 8] = quantity
    
    type = file.loc[i, 'TransactionType']

    if type in transactions:
        quantity = int(file.loc[i, 'Quantity']) - quantity
        abs(quantity)

    i = 1

    l = len(file) - 1
    while i < l:
        if quantity < 0:
            quantity = quantity * -1

        type = file.loc[i, 'TransactionType']

        if type in transactions:
            file.loc[i, 'OnHand'] = quantity
            #file.loc[i, 8] = quantity

            type = file.loc[i, 'SourceBinID']

            if type not in returns:
                quantity = int(file.loc[i, 'Quantity']) - quantity
        
        if descision == "Down to Zero" and quantity == 0:
            i += 1
            file.loc[i, 'OnHand'] = quantity
            #file.loc[i, 8] = quantity
            
            while l > i:
                file = file.drop(l)
                l -= 1
            break
        i += 1

    st.subheader("Data Preview")
    st.write(file)
    
    st.subheader("Filter Data")
    columns = "TransactionType"
    unique_values = file[columns].unique()
    selected_value = st.selectbox("Select value: ", unique_values)

    filtered_file = file[file[columns] == selected_value]

    st.write(filtered_file)

    st.subheader("All Bin Locations")

    numbers = ["1","2","3","4","5","6", "L", "Q", "Y"]
    bin = "BinID"
    unique_values = file[bin].unique()
    filtered = []

    for l in unique_values:
        temp = str(l)
        if temp[0] in numbers:
            filtered.append(temp)

    for l in filtered:
        st.write(l)
