import os
import streamlit as st
import pandas as pd
from datetime import datetime as dt
from savefile import save_uploadedfile, load_file
from glob import glob

filename = None

st.set_page_config(page_title="EPM Breakdown", layout="wide")
file_uploaded = st.file_uploader("Upload EPM export here...",type=['csv', 'xlsx'])

with st.expander("See additional instructions..."):
    st.write(
        """
        1.)  Get a fresh EPM export from Jeff Ngo so all the members of the team are included.\n
        2.)  Add a column called "Region Supported" at the end of the columns of the export (after comments) for each associate. You may opt to perform lookup functions.\n
        3.)  Double check the names of the associate (i.e. Transferred Colleagues hours must reflect when they actually transferred / Joined the team.) before importing to ensure correct hours are being logged.
        
        """)

if file_uploaded is not None:
    save_uploadedfile(file_uploaded)
    st.success('File was successfully uploaded')

#read file after upload
filepath = "SavedFile/"
filename = glob(filepath+"*.csv")
filename = filename[0].split("\\")
filename= filename[1]

df = pd.read_csv(f"SavedFile/{str(filename)}")


#display billable hours.

billable_hours = df[(df['Billable Hours'] != 0)].groupby(['Transaction Calendar Month', 'Region Supported'])['Billable Hours'].sum()
billable_hours = billable_hours.unstack(level=0)
billable_hours.columns = billable_hours.columns.str.title()
billable_hours.columns = pd.to_datetime(billable_hours.columns, format="%y-%b")
billable_hours = billable_hours[sorted(billable_hours.columns)]
billable_hours.columns = billable_hours.columns.strftime("%b-%y")
billable_hours['YTD Billable Hours'] = billable_hours.sum(axis=1)

st.subheader('Billable Hours')
st.dataframe(data=billable_hours,width=None)

#display billable equivalent hours.
bilable_equiv_hours = df[(df['Billable Equivalent Hours'] != 0) & (df['Customer Name'] != 'Unspecified')].groupby(['Transaction Calendar Month','Region Supported'])['Billable Equivalent Hours'].sum()
bilable_equiv_hours = bilable_equiv_hours.unstack(level=0)
bilable_equiv_hours.columns = bilable_equiv_hours.columns.str.title()
bilable_equiv_hours.columns = pd.to_datetime(bilable_equiv_hours.columns, format="%y-%b")
bilable_equiv_hours = bilable_equiv_hours[sorted(bilable_equiv_hours.columns)]
bilable_equiv_hours.columns = bilable_equiv_hours.columns.strftime("%b-%y")
bilable_equiv_hours['YTD Licensed Hours'] = bilable_equiv_hours.sum(axis=1)

st.subheader('Billable Equivalent Hours')
st.dataframe(data=bilable_equiv_hours,width=None)

#display Non-billable equivalent hours.
Non_Billable_hours = df[(df['Non Billable Hours*'] != 0) & (df['Task Number - Name'] != '01.01-Internal Management')].groupby(['Transaction Calendar Month','Region Supported'])['Non Billable Hours*'].sum()
Non_Billable_hours = Non_Billable_hours.unstack(level=0)
Non_Billable_hours.columns = Non_Billable_hours.columns.str.title()
Non_Billable_hours.columns = pd.to_datetime(Non_Billable_hours.columns, format="%y-%b")
Non_Billable_hours = Non_Billable_hours[sorted(Non_Billable_hours.columns)]
Non_Billable_hours.columns = Non_Billable_hours.columns.strftime("%b-%y")
Non_Billable_hours['YTD Non Billable Hours Total'] = Non_Billable_hours.sum(axis=1)

st.subheader('Non Billable Hours w/o Internal Management')
st.dataframe(data=Non_Billable_hours,width=None)
