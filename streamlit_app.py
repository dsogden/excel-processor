import streamlit as st
import pandas as pd

# from sorter import Sorter

st.title("Medtronic Excel Processor")

uploaded_files = st.file_uploader(
    "Select all files", accept_multiple_files=True
)

# for uploaded_file in uploaded_files:
#     bytes_data = uploaded_file.read()
#     st.write("filename:", uploaded_file.name)

substance_list = st.file_uploader(
    "Add the substance list excel file", accept_multiple_files=False
)
substances = pd.read_excel(substance_list, skiprows=0)

# methods_list = st.file_uploader(
#     "Add the methods list excel file", accept_multiple_files=False
# )
# methods = pd.read_excel(methods_list, skiprows=0)