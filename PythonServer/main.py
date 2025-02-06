import streamlit as st
import os
import pandas as pd
import openpyxl as op
import io
import xlsxwriter

st.set_page_config(layout="wide")

st.sidebar.image('logo.png', width=260)

st.sidebar.page_link("main.py", label="Home")
st.sidebar.page_link("Pages/inboundreports.py", label="Inventory Reports")
st.sidebar.page_link("Pages/nobinzerolist.py", label="NOBIN / ZERO Lists")
st.sidebar.page_link("Pages/3dayold.py", label="3 Day old ASN's")
st.sidebar.page_link("Pages/zeroprogram.py", label="Zero Program")
st.sidebar.page_link("Pages/itemclasssize.py", label="Calculate Item Class Size")
