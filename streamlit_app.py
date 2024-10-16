import streamlit as st
# from sorter import Sorter

st.title("Medtronic Excel Processor")

uploaded_files = st.file_uploader(
    "Choose a CSV file", accept_multiple_files=True
)

for uploaded_file in uploaded_files:
    bytes_data = uploaded_file.read()
    st.write("filename:", uploaded_file.name)

