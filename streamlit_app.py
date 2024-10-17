import streamlit as st
import pandas as pd
from sorter import Sorter

st.title("Data Processor")

substance_list = st.file_uploader(
    "Add the substance list (csv format)", accept_multiple_files=False
)

if substance_list:
    substances = pd.read_csv(substance_list, skiprows=0)

methods_list = st.file_uploader(
    "Add the methods list (csv format)", accept_multiple_files=False
)

if methods_list:
    methods = pd.read_csv(methods_list, skiprows=0)

files = st.file_uploader(
    "Select all results files (csv format)", accept_multiple_files=True
)

@st.cache_data
def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')

def main():
    sorter = Sorter(df_dict)
    substance_mapper = {value[-1]: value[0] for value in substances.values}
    df = sorter.run(substance_mapper)
    columns_order = [
        'Material(s)', 'Substance', 'CAS No.', 'Method', 'Result (mg/kg)'
    ]
    return df.merge(
        methods, how='left', left_on='Test', right_on='Method Name'
    ).merge(substances, how='left', on='Substance')[columns_order]

if __name__ == '__main__':
    if len(files) > 0:
        df_dict = {
        f.name.split('.csv')[0]: pd.read_csv(f, skiprows=1)\
            .drop(columns=['Test No', 'Status', 'Weight'])
        for f in files
    }
        result = main()
        st.write('Example of the first 10 lines of file')
        st.dataframe(result.head(10).to_string(index=False))

        # Create a download button
        csv = convert_df(result)
        st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name='data.csv',
            mime='text/csv'
        )