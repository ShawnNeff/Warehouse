import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta

# Function remove blank rows
def clean_file(file, employee):
    last = ['Anglin', 'Anguiano', 'Barrera', 'Dingler', 'Ford', 'Gaddy', 'Garcia', 'Garcia-Sanchez', 'Hall', 'Hernandez', 'Jackson', 'Khun', 'Lee', 'Long', 'McGriff', 'Neff', 'Newton', 'North', 'Perry Jr.', 'Phimmasone', 'Yates']
    name = ""
    temp_str = ""
    temp_index = 0
    total = 0
    first = ""

    for index, row in file.iterrows():
        value = row.iloc[0]

        if value in last:
            first = row.iloc[6]
            first = first.replace(" ", "")
            name = f"{value}, {first}"
        
        if value == "P":
            if temp_index == 0:
                temp_str = row.iloc[5]
                employee[name]['clockin']= temp_str[:8]
                employee[name]['lunchout'] = temp_str[-8:]
                employee[name]['total'] += row.iloc[9]
                temp_index = 1
            else:
                temp_str = row.iloc[5]
                employee[name]['lunchin'] = temp_str[:8]
                employee[name]['clockout'] = temp_str[-8:]
                employee[name]['total'] += row.iloc[9]
                temp_index = 0

    return employee

def save_file(employee):

    entertime = pd.read_excel('dailytph.xlsx')

    for index, row in entertime.iterrows():
        if row['Employee'] in employee:
            entertime.loc[index, "StartTime"] = employee[row['Employee']]['starttime']
            entertime.loc[index, "1stBreak"] = employee[row['Employee']]['breakone']
            entertime.loc[index, "2ndBreak"] = employee[row['Employee']]['breaktwo']
            entertime.loc[index, "ClockedIn"] = employee[row['Employee']]['clockin']
            entertime.loc[index, "LunchOut"] = employee[row['Employee']]['lunchout']
            entertime.loc[index, "LunchIn"] = employee[row['Employee']]['lunchin']
            entertime.loc[index, "ClockOut"] = employee[row['Employee']]['clockout']
            if row['Employee'] == "Neff, Shawn" or row['Employee'] == "Yates, Ericsen":
                entertime.loc[index, "HoursWorked"] = ""
            else:
                entertime.loc[index, "HoursWorked"] = employee[row['Employee']]['total']

            if employee[row['Employee']]['total'] > 8:
                entertime.loc[index, "OT"] = "X"

    entertime.to_excel('report.xlsx', index=False)

def load_file():
    file = pd.read_excel('timecard.xls')

    return file

def get_employee():

    employee_template = {
        "starttime": "",
        "breakone": "",
        "breaktwo": "",
        "clockin": "",
        "lunchout": "",
        "lunchin": "",
        "clockout": "",
        "total": 0
    }

    employee = {
        "Anglin, Desmond": employee_template.copy(),
        "Anguiano, Jose": employee_template.copy(),
        "Barrera, Alejandro": employee_template.copy(),
        "Dingler, Stephana": employee_template.copy(),
        "Ford, Thomas": employee_template.copy(),
        "Gaddy, Alicia": employee_template.copy(),
        "Garcia, Adam": employee_template.copy(),
        "Garcia-Sanchez, Jesus": employee_template.copy(),
        "Hall, Brian": employee_template.copy(),
        "Hall, Charlotte": employee_template.copy(),
        "Hernandez, Anna": employee_template.copy(),
        "Jackson, Domislo": employee_template.copy(),
        "Khun, Dara": employee_template.copy(),
        "Lee, Pheng": employee_template.copy(),
        "Long, Maurice": employee_template.copy(),
        "McGriff, Lounzo": employee_template.copy(),
        "Neff, Shawn": employee_template.copy(),
        "Newton, Donna": employee_template.copy(),
        "North, Brian": employee_template.copy(),
        "North, Kevin": employee_template.copy(),
        "Perry Jr., Calvin": employee_template.copy(),
        "Phimmasone, Nathan": employee_template.copy(),
        "Yates, Ericsen": employee_template.copy(),
    }

    employee = set_breaks(employee)

    return employee

def set_breaks(employee):

    for e in employee:
        if e == "Anglin, Desmond":
            employee[e]['starttime'] = "8:30 AM"
            employee[e]['breakone'] = "10:30 AM"
            employee[e]['breaktwo'] = "3:00 PM"
        elif e == "Anguiano, Jose":
            employee[e]['starttime'] = "6:45 AM"
            employee[e]['breakone'] = "10:00 AM"
            employee[e]['breaktwo'] = "2:30 PM"
        elif e == "Barrera, Alejandro":
            employee[e]['starttime'] = "10:30 AM"
            employee[e]['breakone'] = "12:30 PM"
            employee[e]['breaktwo'] = "4:30 PM"
        elif e == "Dingler, Stephana":
            employee[e]['starttime'] = "7:30 AM"
            employee[e]['breakone'] = "9:30 AM"
            employee[e]['breaktwo'] = "2:00 PM"
        elif e == "Ford, Thomas":
            employee[e]['starttime'] = "8:30 AM"
            employee[e]['breakone'] = "10:30 AM"
            employee[e]['breaktwo'] = "3:30 PM"
        elif e == "Gaddy, Alicia":
            employee[e]['starttime'] = "11:00 AM"
            employee[e]['breakone'] = "1:00 PM"
            employee[e]['breaktwo'] = "4:45 PM"
        elif e == "Garcia, Adam":
            employee[e]['starttime'] = "7:00 AM"
            employee[e]['breakone'] = "9:00 AM"
            employee[e]['breaktwo'] = "1:30 PM"
        elif e == "Garcia-Sanchez, Jesus":
            employee[e]['starttime'] = "7:00 AM"
            employee[e]['breakone'] = "9:00 AM"
            employee[e]['breaktwo'] = "1:45 PM"
        elif e == "Hall, Brian":
            employee[e]['starttime'] = "6:00 AM"
            employee[e]['breakone'] = "8:00 AM"
            employee[e]['breaktwo'] = "12:30 PM"
        elif e == "Hall, Charlotte":
            employee[e]['starttime'] = "6:00 AM"
            employee[e]['breakone'] = "8:00 AM"
            employee[e]['breaktwo'] = "12:30 PM"
        elif e == "Hernandez, Anna":
            employee[e]['starttime'] = "9:00 AM"
            employee[e]['breakone'] = "11:00 AM"
            employee[e]['breaktwo'] = "3:30 PM"
        elif e == "Jackson, Domislo":
            employee[e]['starttime'] = "09:30 AM"
            employee[e]['breakone'] = "11:30 AM"
            employee[e]['breaktwo'] = "03:45 PM"
        elif e == "Khun, Dara":
            employee[e]['starttime'] = "9:00 AM"
            employee[e]['breakone'] = "11:00 AM"
            employee[e]['breaktwo'] = "3:30 PM"
        elif e == "Lee, Pheng":
            employee[e]['starttime'] = "10:00 AM"
            employee[e]['breakone'] = "12:00 PM"
            employee[e]['breaktwo'] = "4:00 PM"
        elif e == "Long, Maurice":
            employee[e]['starttime'] = "9:00 AM"
            employee[e]['breakone'] = "11:00 AM"
            employee[e]['breaktwo'] = "3:00 PM"
        elif e == "McGriff, Lounzo":
            employee[e]['starttime'] = "10:00 AM"
            employee[e]['breakone'] = "12:00 PM"
            employee[e]['breaktwo'] = "4:00 PM"
        elif e == "Newton, Donna":
            employee[e]['starttime'] = "9:00 AM"
            employee[e]['breakone'] = "11:00 AM"
            employee[e]['breaktwo'] = "4:00 PM"
        elif e == "North, Brian":
            employee[e]['starttime'] = "6:00 AM"
            employee[e]['breakone'] = "8:00 AM"
            employee[e]['breaktwo'] = "12:30 PM"
        elif e == "North, Kevin":
            employee[e]['starttime'] = "9:00 AM"
            employee[e]['breakone'] = "11:00 AM"
            employee[e]['breaktwo'] = "3:30 PM"
        elif e == "Perry Jr., Calvin":
            employee[e]['starttime'] = "7:00 AM"
            employee[e]['breakone'] = "9:00 AM"
            employee[e]['breaktwo'] = "1:30 PM"
        elif e == "Phimmasone, Nathan":
            employee[e]['starttime'] = "11:00 AM"
            employee[e]['breakone'] = "1:00 PM"
            employee[e]['breaktwo'] = "5:00 PM"
        elif e == "Yates, Ericsen":
            employee[e]['starttime'] = "11:00 AM"
            employee[e]['breakone'] = ""
            employee[e]['breaktwo'] = ""
        elif e == "Neff, Shawn":
            employee[e]['starttime'] = "7:30 AM"
            employee[e]['breakone'] = ""
            employee[e]['breaktwo'] = ""
    return employee

file = load_file()

employee = get_employee()

employee = clean_file(file, employee)

save_file(employee)
