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
    # st.write('Substances loaded')
    substances = pd.read_csv(substance_list, skiprows=0)

methods_list = st.file_uploader(
    "Add the methods list csv", accept_multiple_files=False
)

if methods_list:
    # st.write('Methods loaded')
    methods = pd.read_csv(methods_list, skiprows=0)

def main():
    df_dict = {
        f.name.split('.csv')[0]: pd.read_csv(f, skiprows=1)\
            .drop(columns=['Test No', 'Status', 'Weight'])
        for f in files
    }
    sorter = Sorter(df_dict)
    st.write(df_dict)
    substance_mapper = {value[-1]: value[0] for value in substances.values}
    df = sorter.run(substance_mapper)
    columns_order = [
        'Material(s)', 'Substance', 'CAS No.', 'Method', 'Result (mg/kg)'
    ]
    return df.merge(
        methods, how='left', left_on='Test', right_on='Method Name'
    ).merge(substances, how='left', on='Substance')[columns_order]

if __name__ == '__main__':
    result = main()
    st.dataframe(result.head(10))

# Create a download button
# st.download_button(
#     label="Download data as CSV",
#     data=csv,
#     file_name='data.csv',
#     mime='text/csv',
# )