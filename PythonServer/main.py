import streamlit as st
import os
import pandas as pd
#import openpyxl as op
import io
#import xlsxwriter

# --- PAGE SETUP ---
dashboard_page = st.Page(
    page="views/index.py",
    title="Sacramento Dashboard",
    icon=":material/bar_chart:",
    default=True,
)

employee_page = st.Page(
    page="views/employee.py",
    title="Employee TimeCard",
    icon=":material/account_circle:",
)

transactions_page = st.Page(
    page="views/transaction.py",
    title="Clean Transactions",
    icon=":material/assignment:",
)

transactions_gaps = st.Page(
    page="views/gaps.py",
    title="Transacitons Gaps",
    icon=":material/assignment:",
)

tph_page = st.Page(
    page="views/tph.py",
    title="Employee TPH",
    icon=":material/assignment:",  
)

inventory_history = st.Page(
    page="views/inventoryhistory.py",
    title="Inventory History",
    icon=":material/assignment:",
)

multiple_item_page = st.Page(
    page="views/multipleitems.py",
    title="Multiple Items in Bin",
    icon=":material/pallet:",
)

multiple_locations_per_item = st.Page(
    page="views/multiplelocations.py",
    title="Multiple Locations per Item",
    icon=":material/pallet:",
)

primary_page = st.Page(
    page="views/primary.py",
    title="Missing Primary Location",
    icon=":material/pallet:",
)

core_page = st.Page(
    page="views/cores.py",
    title="CORE Missmatch",
    icon=":material/pallet:",
)

nobins_page = st.Page(
    page="views/nobin.py",
    title="Nobins (new)",
    icon=":material/package_2:",
)

zero_page = st.Page(
    page="views/zero.py",
    title="Zero Qty Itmes",
    icon=":material/package_2:",
)

asn_page = st.Page(
    page="views/asn.py",
    title="ASN Report",
    icon=":material/assignment:",
)

slot_page = st.Page(
    page="views/slot.py",
    title="Slotting Report",
    icon=":material/assignment:",
)

size_class_page = st.Page(
    page="views/binsize.py",
    title="Bin Size Missmatch",
    icon=":material/assignment:",
)

velocity_page = st.Page(
    page="views/velocity.py",
    title="Velocity Missmatch",
    icon=":material/assignment:",
)

contact_me = st.Page(
    page="views/about_me.py",
    title="About Me",
    icon=":material/account_circle:",
)

# --- NAVIGATION SETUP [WITH SECTIONS] ---
pg = st.navigation(
    {
        "Dashboard": [dashboard_page],
        #"Employee": [employee_page, transactions_page, transactions_gaps, tph_page],
        "Warehouse": [inventory_history, asn_page, multiple_item_page, multiple_locations_per_item, primary_page, core_page, nobins_page, zero_page],
        "Slotting": [slot_page, size_class_page, velocity_page],
        #"Contact": [contact_me]
    }
)

# --- SHARED ON ALL PAGES ---
#st.logo("assets/Reliable-Parts_Logo.webp")
#st.logo("assets/logo.png")
st.sidebar.text("Made by Shawn Neff")

# --- RUN NAVIGATION ---
pg.run()
