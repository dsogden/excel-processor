import streamlit as st
import pandas as pd

from sorter import Sorter

st.title("Data Processor")

files = st.file_uploader(
    "Select all files", accept_multiple_files=True
)

substance_list = st.file_uploader(
    "Add the substance list csv", accept_multiple_files=False
)

if substance_list:
    substances = pd.read_csv(substance_list, skiprows=0)

# methods_list = st.file_uploader(
#     "Add the methods list csv", accept_multiple_files=False
# )
# methods = pd.read_excel(methods_list, skiprows=0)
if len(files) > 0:
    df_dict = {f.name.split('.csv')[0]: pd.read_csv(f, skiprows=1) for f in files}
    # st.write(df_dict)
    # sorter = Sorter(df_dict)
    st.write(df_dict[])
    # substance_mapper = {value[-1]: value[0] for value in substances.values}
    # df = sorter.run(substance_mapper)
    # st.dataframe(df.head(10))
# st.write(sorter.input_files)
# def main():
# csv = df.to_csv(index=False)

# Create a download button
# st.download_button(
#     label="Download data as CSV",
#     data=csv,
#     file_name='data.csv',
#     mime='text/csv',
# )