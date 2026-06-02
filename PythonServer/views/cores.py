import streamlit as st
import pandas as pd

item = st.file_uploader("Upload inventory file.",type="xlsx")

if item is not None:
    file = pd.read_excel(item)

    core = [["", "", "", 0]]
    part = []

    file.drop(file.columns[[1,2,3,4,5,6,7,8,9,10,12,13,14,15,16,17,18,19,20,21,23,24,25,26,28,29,30,31,32,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,62,63,64,]],axis=1,inplace=True,)

    i = 0

    for index, row in file.iterrows():
        temp = row["ItemID"]
        check = temp[-4:]

        if check == "CORE":
            i = index + 1

        core.append([temp, temp[:-4], row["PrimaryBin"], row["Quantity"]])

    for index, row in file.iterrows():
        temp = row["ItemID"]

        for c in core:
            if temp == c[1]:
                if row["PrimaryBin"] != c[2] or row["Quantity"] != c[3]:
                    part.append(temp)

    st.write(part)
