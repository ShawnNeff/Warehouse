import streamlit as st
import os
import pandas as pd
import openpyxl as op
import io
import xlsxwriter

def get_string(item, bin, qty, openorder, binvel, itemvel):
    str = ""
    str = item + "   " + bin + "    " + qty + "    " +  openorder + "     " + binvel + "     " + itemvel
    return str

def get_row(file, item):
    l = len(file) - 1
    d = {}

    while l >= 0:
        if item == file.loc(l, 'ItemID'):
            d = {"ItemID:": file.loc(l, 'ItemID'), "PrimaryBin": file.loc(l, 'PrimaryBin'), "Quantity": file.loc(l, 'Quantity'), "HostOnPurchaseOrder": file.loc(l, 'HostOnPurchseOrder'), "BinVelocityClassID": file.loc(l, 'BinVelocityClassID'), "ItemVelocityClassID": file.loc(l, 'ItemVelocityClassID')}
            return d
        l -= 1

st.set_page_config(layout="wide")
st.title("Bin Change Log Report")
st.sidebar.success("Reliable Parts")

with st.sidebar:
    st.page_link('./main.py', label="Home")
    st.page_link('./pages/2_zeroprogram.py', label="Inventory History")
    st.page_link('./pages/3_inboundreports.py', label="Inbound Reports")
    st.page_link('./pages/4_nobinzerolist.py', label="Nobin / Zero Reports")
    st.page_link('./pages/5_3dayold.py', label="ASN 3 Day Old Report")
    st.page_link('./pages/6_binchange.py', label="Item Bin Size Change")
    st.page_link('./pages/7_itemclasssize.py', label="Calculate Item Class Size")
    st.page_link('./pages/8_swap.py', label="Swap Bins (Velocity)")


file1 = st.file_uploader("**Inventory File** - Upload inventory excel file in xlsx format.",type="xlsx")

#report = pd.DataFrame(columns=['ItemID', 'PrimaryBin', 'Quantity', 'HostOnPurchaseOrder', 'BinVelocityClassID', 'ItemVelocityClassID', 'Blank', 'Blank1', 'Blank2', 'ItemID', 'PrimaryBin', 'Quantity', 'HostOnPurchaseOrder', 'BinVelocityClassID', 'ItemVelocityClassID'])

if file1 is not None:

    file = pd.read_excel(file1)

    l = len(file) - 1
    ab, ac, ad, ba, bc, bd, ca, cb, cd, da, db, dc = ([] for i in range(12))

    while l >= 0:
        whichlist = file.loc[l, 'BinVelocityClassID'] + file.loc[l, 'ItemVelocityClassID']
 
        if whichlist == "AB":
            ab.append(file.loc[l, 'ItemID'])
        elif whichlist == "AC":
            ac.append(file.loc[l, 'ItemID'])
        elif whichlist == "AD":
            ad.append(file.loc[l, 'ItemID'])
        elif whichlist == "BA":
            ba.append(file.loc[l, 'ItemID'])
        elif whichlist == "BC":
            bc.append(file.loc[l, 'ItemID'])
        elif whichlist == "BD":
            bd.append(file.loc[l, 'ItemID'])
        elif whichlist == "CA":
            ca.append(file.loc[l, 'ItemID'])
        elif whichlist == "CB":
            cb.append(file.loc[l, 'ItemID'])
        elif whichlist == "CD":
            cd.append(file.loc[l, 'ItemID'])
        elif whichlist == "DA":
            da.append(file.loc[l, 'ItemID'])
        elif whichlist == "DB":
            db.append(file.loc[l, 'ItemID'])
        elif whichlist == "DC":
            dc.append(file.loc[l, 'ItemID'])

        l -= 1

    st.subheader("A <-> B")
    st.write(ab)
    st.write("-------------")
    st.write(ba)    
    st.subheader("A <-> C")
    st.write(ac)
    st.write("-------------")
    st.write(ca)
    st.subheader("A <-> D")
    st.write(ad)
    st.write("-------------")
    st.write(da)
    st.subheader("B <-> C")
    st.write(bc)
    st.write("-------------")
    st.write(cb)
    st.subheader("B <-> D")
    st.write(bd)
    st.write("-------------")
    st.write(db)
    st.subheader("C <-> D")
    st.write(cd)
    st.write("-------------")
    st.write(dc)