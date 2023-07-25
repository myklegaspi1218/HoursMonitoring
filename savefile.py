import os
import pandas as pd
import streamlit as st
from glob import glob


def save_uploadedfile(uploadedfile):
    existingFileCheck = glob("SavedFile/"+"*csv")
    existingFileCheck = existingFileCheck[0].split("\\")
    existingFileCheck = existingFileCheck[1]
    os.remove(f"SavedFile/{existingFileCheck}")    
    if existingFileCheck != uploadedfile:
        with open(os.path.join("SavedFile/",uploadedfile.name),"wb") as f:
            f.write(uploadedfile.getbuffer())
            
    
        

@st.cache_data
def load_file(filename):
    with open(os.path.join("SavedFile/",filename.name),"r") as f:
     return pd.read_csv(f)
