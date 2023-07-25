import streamlit as st
import pandas as pd
from savefile import load_file 
from glob import glob

st.set_page_config(page_title="EPM Breakdown", layout="wide")

#read file after upload
filepath = "SavedFile/"
filename = glob(filepath+"*.csv")
filename = filename[0].split("\\")
filename= filename[1]

df = pd.read_csv(f"SavedFile/{str(filename)}")

#Billable Hours by associate
st.subheader("Billable Hours By Task Code")
billableHoursByAssociate = df[(df['Billable Hours'] != 0)].groupby(['Transaction Calendar Month','Region Supported', 'Task Number - Name'])\
['Billable Hours'].sum()
billableHoursByAssociate = billableHoursByAssociate.unstack(level=0)
billableHoursByAssociate.columns = billableHoursByAssociate.columns.str.title()
billableHoursByAssociate.columns = pd.to_datetime(billableHoursByAssociate.columns, format="%y-%b")
billableHoursByAssociate = billableHoursByAssociate[sorted(billableHoursByAssociate.columns)]
billableHoursByAssociate.columns = billableHoursByAssociate.columns.strftime("%b-%y")
billableHoursByAssociate['YTD Billable Hours'] = billableHoursByAssociate.sum(axis=1)
st.dataframe(billableHoursByAssociate,use_container_width=True)

#billable equivalent hours
st.subheader("Billable Equivalent Hours By Task Code")
billableEquivalentHoursByAssociate = df[(df['Billable Equivalent Hours'] != 0) & (df['Customer Name'] != 'Unspecified')].groupby(['Transaction Calendar Month','Region Supported', 'Task Number - Name'])\
['Billable Equivalent Hours'].sum()
billableEquivalentHoursByAssociate = billableEquivalentHoursByAssociate.unstack(level=0)
billableEquivalentHoursByAssociate.columns = billableEquivalentHoursByAssociate.columns.str.title()
billableEquivalentHoursByAssociate.columns = pd.to_datetime(billableEquivalentHoursByAssociate.columns, format="%y-%b")
billableEquivalentHoursByAssociate = billableEquivalentHoursByAssociate[sorted(billableEquivalentHoursByAssociate.columns)]
billableEquivalentHoursByAssociate.columns = billableEquivalentHoursByAssociate.columns.strftime("%b-%y")
billableEquivalentHoursByAssociate['YTD Billable Equivalent Hours'] = billableEquivalentHoursByAssociate.sum(axis=1)
st.dataframe(billableEquivalentHoursByAssociate,use_container_width=True)

#breakdown by Non-Billable Hours
st.subheader("Non-Billable Hours By Task Code")
nonBillableHoursByAssociate = df[(df['Non Billable Hours*'] != 0) & (df['Task Number - Name'] != '01.01-Internal Management')].groupby(['Transaction Calendar Month','Region Supported','Task Number - Name'])['Non Billable Hours*'].sum()
nonBillableHoursByAssociate = nonBillableHoursByAssociate.unstack(level=0)
nonBillableHoursByAssociate.columns = nonBillableHoursByAssociate.columns.str.title()
nonBillableHoursByAssociate.columns = pd.to_datetime(nonBillableHoursByAssociate.columns, format="%y-%b")
nonBillableHoursByAssociate = nonBillableHoursByAssociate[sorted(nonBillableHoursByAssociate.columns)]
nonBillableHoursByAssociate.columns = nonBillableHoursByAssociate.columns.strftime("%b-%y")
nonBillableHoursByAssociate['Total Hours'] = nonBillableHoursByAssociate.sum(axis=1)
st.dataframe(nonBillableHoursByAssociate, use_container_width = True)


