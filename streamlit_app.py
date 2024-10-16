import streamlit as st
import pandas as pd

from sorter import Sorter

st.title("Medtronic Excel Processor")

files = st.file_uploader(
    "Select all files", accept_multiple_files=True
)

substance_list = st.file_uploader(
    "Add the substance list excel file", accept_multiple_files=False
)
# substances = pd.read_excel(substance_list, skiprows=0)

methods_list = st.file_uploader(
    "Add the methods list excel file", accept_multiple_files=False
)
# methods = pd.read_excel(methods_list, skiprows=0)
if files is not None:
    for f in files:
        st.write("filename:", f.name)
        df = pd.read_excel(f, skiprows=1)
        st.dataframe(df)
# sorter = Sorter(files)