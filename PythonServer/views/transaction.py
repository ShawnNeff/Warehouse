import pandas as pd
import streamlit as st
from datetime import datetime, date, timedelta
import xlsxwriter
import os

# Function remove blank rows
def clean_file(file):
    file.drop(file.columns[[
    1, 2, 3, 4, 6, 7, 8, 10, 11, 14, 15, 17, 19, 20
    ]], axis=1, inplace=True)

    file.columns = ['DATETIME', 'ITEMID', 'TRANSACTION', 'SOURCEBIN', 'DESTBIN', 'QUANTITY', 'JOB']

    cleaned = file.dropna(subset=['DATETIME'])

    cleaned = cleaned.drop(index=0)

    return cleaned

# Function - keep all actual transactions
def clean_user(user, users, carts, bagntag):
    row_to_copy = []
    master = pd.DataFrame()

    for index, row in user.iterrows():
        if row['DATETIME'] in users:
            row_to_copy.append(row)
        elif row['TRANSACTION'] == "ORD.PICK":
            row_to_copy.append(row)
        elif row['TRANSACTION'] == "ORD.SHIP":
            row_to_copy.append(row)
        elif row['TRANSACTION'] == "ITEM.RECEIVE":
            row_to_copy.append(row)
        elif row['TRANSACTION'] == "ITEM.PUTAWAY":
            row_to_copy.append(row)
        elif row['TRANSACTION'] == "ITEM.RETURN":
            row_to_copy.append(row)
        elif row['TRANSACTION'] == "ITEM.INDUCT":
            row_to_copy.append(row)
        elif row['TRANSACTION'] == "ITEM.DEDUCT":
            row_to_copy.append(row)
        elif row['TRANSACTION'] == "BIN.CHANGE.P":
            row_to_copy.append(row)
        elif row['TRANSACTION'] == "ITEM.MOVE":
            if row['SOURCEBIN'] in carts or row['SOURCEBIN'] in bagntag:
                row_to_copy.append(row)
        elif row['TRANSACTION'] == "LOAD.STAGE":
            if row['SOURCEBIN'] == "PICK" and row['DESTBIN'] == "PACK":
                row_to_copy.append(row)
        elif row['TRANSACTION'] == "ITEM.CYCLECOUNT":      
            row_to_copy.append(row)
        elif row['TRANSACTION'] == "ITEM.UNRECEIVE":
            row_to_copy.append(row)
        elif row['TRANSACTION'] == "ORD.UNPICK":
            row_to_copy.append(row)
        elif row['TRANSACTION'] == "ORD.COMPLINE":
            row_to_copy.append(row)
        elif row['TRANSACTION'] == "PROBLEM":
            row_to_copy.append(row)
        elif row['TRANSACTION'] == "WHSE.PICK":
            row_to_copy.append(row)

    master = pd.DataFrame(row_to_copy, columns=['DATETIME', 'ITEMID', 'TRANSACTION', 'SOURCEBIN', 'DESTBIN', 'QUANTITY', 'JOB'])
    return master

# Funciton - get time for each employee
def get_time(employee, employeetime):

    for index, row in employeetime.iterrows():
        u = row['EmployeeID']

        if employee[u]['clockin'] == "nan":
            employee[u]['clockin'] = ""
        else:
            employee[u]['clockin'] = employeetime.loc[index, "ClockedIn"]

        if employee[u]['lunchout'] == "nan":
            employee[u]['lunchout'] = ""
        else:
            employee[u]['lunchout'] = employeetime.loc[index, "LunchOut"]
        
        if employee[u]['lunchin'] == "nan":
            employee[u]['lunchin'] = ""
        else:
            employee[u]['lunchin'] = employeetime.loc[index, "LunchIn"]

        if employee[u]['clockout'] == "nan":
            employee[u]['clockout'] = ""
        else:
            employee[u]['clockout'] = employeetime.loc[index, "ClockOut"]

        if employee[u]['break_one'] == "nan":
            employee[u]['break_one'] = ""
        else:
            employee[u]['break_one'] = employeetime.loc[index, "1stBreak"]

        if employee[u]['break_two'] == "nan":
            employee[u]['breal_two'] = ""
        else:
            employee[u]['break_two'] = employeetime.loc[index, "2ndBreak"]
        if u == "SC306":
            break

    return employee

# Funciton - convert string to datetime
def convert_str_date(s):

    #temp = datetime.strptime(s, "%Y-%m-%d %I:%M %p")

    try:
        date_obj = datetime.fromisoformat(s)
    except ValueError:
        date_obj = datetime.strptime(s, '%Y-%m-%d %I:%M %p')

    #date_obj = datetime.fromisoformat(temp)
    #date_obj = datetime.strptime(s, '%Y-%m-%d %I:%M %p')

    return date_obj

# Function - gets date for timecard
def get_date():

    today = date.today()

    holiday = ['2026-05-25', '2026-07-03', '2026-09-07', '2026-11-26', '2026-12-25', '2027-1-1']

    if today.weekday() == 0:
        yesterday_date = today - timedelta(days=3)
    else:
        yesterday_date = today - timedelta(days=1)

    if yesterday_date in holiday:
        if yesterday_date.weekday == 0:
            yesterday_date = yesterday_date - timedelta(days=3)
        else:
            yesterday_date = yesterday_date - timedelta(days=1)

    return yesterday_date



# Funciton - adds employees timecard into cleaned transaction file
def add_time(employee, master_user):
    
    file_len = len(master_user) - 1
    current_user = ""
    date_temp = get_date()
    
    for index, row in master_user.iterrows():
        index2 = index + 1

        if index > file_len or index2 > file_len:
            break

        if row['DATETIME'] in users:
            current_user = row['DATETIME']
            index3 = index + .5
            
            ytime = f"{str(date_temp)} {str(employee[current_user]['clockin'])}"
            ytemp = f"{str(date_temp)} nan"
            
            if ytime != ytemp:
                date_obj = convert_str_date(ytime)
                master_user.loc[index3] = date_obj, "", "Clock In", "", "", "", ""
                    

    return master_user

# Funciton - adds employees timecard lunch out into cleaned transaction file
def add_lunch(employee, master_user):
    file_len = len(master_user) - 1
    current_user = ""
    date_temp = get_date()
    
    for index, row in master_user.iterrows():
        index2 = index + 1

        if index > file_len or index2 > file_len:
            break

        if row['DATETIME'] in users:
            current_user = row['DATETIME']
        else:

            index3 = index - 1

            ytime = f"{str(date_temp)} {str(employee[current_user]['lunchout'])}"
            ytemp = f"{str(date_temp)} nan"

            if ytime != ytemp:
                date_obj = convert_str_date(ytime)

                if date_obj < row['DATETIME'] and date_obj > master_user.loc[index3, 'DATETIME']:
                    index3 = index - .5

                    master_user.loc[index3] = date_obj, "", "Lunch Out", "", "", "", ""

    return master_user

# Function - add employees timecard lunch in into cleaned transaction file
def add_lunchin(employee, master_user):
    file_len = len(master_user) - 1
    current_user = ""
    date_temp = get_date()
    
    for index, row in master_user.iterrows():
        index2 = index + 1

        if index > file_len or index2 > file_len:
            break

        if row['DATETIME'] in users:
            current_user = row['DATETIME']
        else:

            index3 = index - 1

            ytime = f"{str(date_temp)} {str(employee[current_user]['lunchin'])}"
            ytemp = f"{str(date_temp)} nan"

            if ytime != ytemp:
                date_obj = convert_str_date(ytime)

                if date_obj < row['DATETIME'] and date_obj > master_user.loc[index3, 'DATETIME']:
                    index3 = index - .5

                    master_user.loc[index3] = date_obj, "", "Lunch In", "", "", "", ""

    return master_user

# Function - add employees timecard clock out into the cleaned transactions
def add_clockout(employee, master_user):

    file_len = len(master_user) - 1
    current_user = ""
    date_temp = get_date()
    temp = 0

    for index, row in master_user.iterrows():
        index2 = index + 1

        if temp == 0 and row['DATETIME'] in users:
            current_user = row['DATETIME']
            temp = 1
        elif temp == 1 and row['DATETIME'] in users:

            ytime = f"{str(date_temp)} {str(employee[current_user]['clockout'])}"
            ytemp = f"{str(date_temp)} nan"

            if ytime != ytemp:
                date_obj = convert_str_date(ytime)

                index3 = index - .5

                master_user.loc[index3] = date_obj, "", "Clock Out", "", "", "", ""

            current_user = row['DATETIME']
        elif index2 > file_len:
            ytime = f"{str(date_temp)} {str(employee[current_user]['clockout'])}"
            ytemp = f"{str(date_temp)} nan"

            if ytime != ytemp:
                date_obj = convert_str_date(ytime)

                index3 = index + .5

                master_user.loc[index3] = date_obj, "", "Clock Out", "", "", "", ""

        if index > file_len or index2 > file_len:
            break
        
    return master_user

# Function - add employees timecard break in into cleaned transaction file
def add_breakone(employee, master_user):
    file_len = len(master_user) - 1
    current_user = ""
    date_temp = get_date()
    
    for index, row in master_user.iterrows():
        index2 = index + 1

        if index > file_len or index2 > file_len:
            break

        if row['DATETIME'] in users:
            current_user = row['DATETIME']
        else:

            index3 = index - 1

            ytime = f"{str(date_temp)} {str(employee[current_user]['break_one'])}"
            ytemp = f"{str(date_temp)} nan"

            if ytime != ytemp:
                date_obj = convert_str_date(ytime)

                if date_obj < row['DATETIME'] and date_obj > master_user.loc[index3, 'DATETIME']:
                    index3 = index - .5

                    master_user.loc[index3] = date_obj, "", "1st Break", "", "", "", ""

    return master_user

# Function - add employees timecard break in into cleaned transaction file
def add_breaktwo(employee, master_user):
    file_len = len(master_user) - 1
    current_user = ""
    date_temp = get_date()
    
    for index, row in master_user.iterrows():
        index2 = index + 1

        if index > file_len or index2 > file_len:
            break

        if row['DATETIME'] in users:
            current_user = row['DATETIME']
        else:

            index3 = index - 1

            ytime = f"{str(date_temp)} {str(employee[current_user]['break_two'])}"
            ytemp = f"{str(date_temp)} nan"

            if ytime != ytemp:
                date_obj = convert_str_date(ytime)

                if date_obj < row['DATETIME'] and date_obj > master_user.loc[index3, 'DATETIME']:
                    index3 = index - .5

                    master_user.loc[index3] = date_obj, "", "2nd Break", "", "", "", ""

    return master_user

item = st.file_uploader("Upload transcations file to clean.",type=["xlsx", "xls"])

if item is not None:
    timegap = pd.read_excel(item)
    # Varialbe - set of all users
    users = ("AJB002", "ALH002", "AXG004", "AXG006", "BBN001", "BJH001", "CXH003", "CXP001", "DLJ001", "DVA001", "DXN001", "DXK001", "EAY001", "JJS001", "JXA001", "KAN001", "LJM001", "MDL001", "NXP003", "PXL001", "SC303", "SC304", "SC306", "SPN001", "SXD001", "TXF001")
    # Variable - set for all return carts, p3 carts, and bagntag cart
    carts = ("#ACRT2A", "#ACRT2B", "#ACRT2C", "#ACRT2D", "#ACRT3A", "#ACRT3B", "#ACRT3C", "#ACRT3D", "RTNPLT1", "RTNFRONT", "P3RACK1A", "P3RACK1B", "P3RACK1C", "P3RACK1D", "#P3BINAA", "#P3BINAB", "#P3BINAC", "#P3BINBA", "#P3BINBB", "#P3BINBC", "#P3BINBD", "#P3BINCA", "#P3BINCB", "#P3BINCC", "#P3BINCD", "#P3BINDA", "#P3BINDB", "#P3BINDC", "#P3BINDD", "#P3BINDE", "#P3BINEA", "#P3BINEB", "#P3BINEC", "#P3BINED", "#P3BINEE", "#P3BINEF", "#P3BINFA", "#P3BINFB", "#P3BINFC", "#P3BINFD", "#P3BINFE", "#P3BINFF", "#P3BINFG", "#P3BINFH", "#P3BINGA", "#P3BINGB", "#P3BINGC", "#P3BINGD", "#P3BINGE", "#P3BINGF", "#P3BINGG", "#P3BINGH", "#P3BINHA", "#P3BINHB", "#P3BINHC", "#P3BINHD", "#P3BINHE", "#P3BINHG", "#P3BINHH", "#P3BINHI", "#P3BINHJ", "#P3BINHK", "#P3BINHL", "#P3BINHM", "#P3BINHN", "#P3BINHO", "#P3BINIA", "#P3BINIB", "#P3BINIC", "#P3BINID", "#P3BINIE", "#P3BINIF", "#P3BINIG", "#P3BINIH", "#P3BINII", "#P3BINIJ", "#P3BINIK", "#P3BINIL", "#P3BINIM", "#P3BININ", "#P3BINIO")
    # Variable - set for bagntag locations
    bagntag = ("#ACBAT", "#ACDMG", "#ACLABEL", "#ACOTHER")

    # Variable - used to add row to user dataframe
    row_to_copy = []
    # Variable - list to hold user indexs
    user_rows_cleaned = []
    # Vailable - dictionary to store employee time
    employee_template = {
        "clockin": "",
        "lunchout": 0,
        "lunchin": 0,
        "clockout": 0,
        "break_one": 0,
        "break_two": 0
    }

    employee = {
        "DVA001": employee_template.copy(),
        "JXA001": employee_template.copy(),
        "AJB002": employee_template.copy(),
        "SXD001": employee_template.copy(),
        "TXF001": employee_template.copy(),
        "AXG006": employee_template.copy(),
        "AXG004": employee_template.copy(),
        "JJS001": employee_template.copy(),
        "BJH001": employee_template.copy(),
        "CXH003": employee_template.copy(),
        "ALH002": employee_template.copy(),
        "DLJ001": employee_template.copy(),
        "DXK001": employee_template.copy(),
        "PXL001": employee_template.copy(),
        "MDL001": employee_template.copy(),
        "LJM001": employee_template.copy(),
        "SPN001": employee_template.copy(),
        "DXN001": employee_template.copy(),
        "BBN001": employee_template.copy(),
        "KAN001": employee_template.copy(),
        "CXP001": employee_template.copy(),
        "NXP003": employee_template.copy(),
        "EAY001": employee_template.copy(),
        "SC303": employee_template.copy(),
        "SC304": employee_template.copy(),
        "SC306": employee_template.copy()
    }

    # Variable - dataframe to store initial excel file
    #timegap = pd.read_excel('transactions.xls')

    # Variable - dataframe to store employee clock in time
    employeetime = pd.read_excel('./PythonServer/files/dailytph.xlsx')

    # Function Call - calls function to load employee time clock
    employee = get_time(employee, employeetime)

    # Function Call - calls funtion clean file which removes all empty lines
    timegap = clean_file(timegap)

    # Save File - saves the new dataframe
    timegap.to_excel('./PythonServer/files/test.xlsx', index=False)

    # Variable - dataframe to store excel file
    timegap = pd.read_excel('./PythonServer/files/test.xlsx')
    # Variable - column names
    column_names = ['DATETIME', 'ITEMID', 'TRANSACTION', 'SOURCEBIN', 'DESTBIN', 'QUANTITY', 'JOB']
    # Variable - master dataframe to hold cleaned data
    master_user = pd.DataFrame(columns=column_names)

    # Variable - lenght of file
    l = len(timegap) - 1

    # For Loop - Clean data to remove unessassary lines
    for index, row in timegap.iterrows():
        if index == l:
            row_to_copy.append(row)
            user = pd.DataFrame(row_to_copy, columns=['DATETIME', 'ITEMID', 'TRANSACTION', 'SOURCEBIN', 'DESTBIN', 'QUANTITY', 'JOB'])
            user = clean_user(user, users, carts, bagntag)
            master_user = pd.concat([master_user, user], ignore_index=True)

            break

        if row['DATETIME'] in users:
            if row_to_copy == []:
                row_to_copy.append(row)
            else:
                user = pd.DataFrame(row_to_copy, columns=['DATETIME', 'ITEMID', 'TRANSACTION', 'SOURCEBIN', 'DESTBIN', 'QUANTITY', 'JOB'])
                user = clean_user(user, users, carts, bagntag)
                master_user = pd.concat([master_user, user], ignore_index=True)
                
                row_to_copy = []
                row_to_copy.append(row)
        else:
            row_to_copy.append(row)

    # Save excel file
    master_user.to_excel('./PythonServer/files/cleaned.xlsx', index=False)

    # Open cleaned file
    master_user = pd.read_excel('./PythonServer/files/cleaned.xlsx')

    # Funciton Call - calls function to add employees timecard into the cleaned transcations
    master_user = add_time(employee, master_user)
    master_user = master_user.sort_index().reset_index(drop=True)
    master_user = add_lunch(employee, master_user)
    master_user = master_user.sort_index().reset_index(drop=True)
    master_user = add_lunchin(employee, master_user)
    master_user = master_user.sort_index().reset_index(drop=True)
    master_user = add_clockout(employee, master_user)
    master_user = master_user.sort_index().reset_index(drop=True)
    master_user = add_breakone(employee, master_user)
    master_user = master_user.sort_index().reset_index(drop=True)
    master_user = add_breaktwo(employee, master_user)
    master_user = master_user.sort_index().reset_index(drop=True)
    # Save excel file

    master_user.to_excel('./PythonServer/files/cleaned2.xlsx', index=False)
    st.write(master_user)
