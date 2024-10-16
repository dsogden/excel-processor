import pandas as pd
import numpy as np

class Sorter:
    def __init__(self, df_dict: dict):
        self.df = df_dict
        self.units = {'mg/kg': 1.0, '%': 10000.0, 'µg/kg': 1e-3}
        self.special_tests = [
            'REACH',
            'Medical Device Regulation',
            'Per-and Polyfluoroalkyl Substances'
        ]
        self.columns_to_remove = ['Test No', 'Status', 'Weight']
        self.string = '---'

    def update_special(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        '''
        Updates the dataframe results for the following tests:
            REACH/MDR/PFAS

        Input:
            DataFrame and input string to replace

        Returns:
            DataFrame
        '''
        columns = dataframe.columns
        for column in columns:
            dataframe[column] = dataframe[column].replace(self.string, np.nan)
        return dataframe

    def refactor_dataframes(self):
        '''
        Update the column names, extracts the reporting limit,
        and checks the units for result processing

        Input:
            Dictionary of dataframes

        Returns:
            Dictionary of dataframes with updates to the column names
            and processed results
        '''
        for key, dataframe in self.df_dict.items():
            column_names = dataframe.columns[1:] # get columns to rename
            if key in self.special_tests:
                dataframe = self.update_special(dataframe)
            names = []
            for column in column_names:
                # column name = Name, Limit*, RL, Units
                # Limit may not be present in column name
                parts = column.split(', ')
                name = parts[0] # first split
                names.append(name)
                 # second to last
                reporting_limit = float(parts[-2].split(': ')[-1])
                unit = self.units[parts[-1].split(': ')[-1]] # final index
                name_mapper = {column: name} # dict to rename the column names
                # Rename columns
                dataframe = dataframe.rename(columns=name_mapper)
                # Update Results
                dataframe[name] = dataframe[name].apply(
                    lambda x: f'<{reporting_limit * unit}' \
                    if (x == '< RL') or (x == '<RL') else x
                )
            dataframe['Test'] = key
            self.df_dict[key] = dataframe

    def concat_dataframes(self) -> pd.DataFrame:
        '''
        Takes an input dictionary of dataframes and concats into one dataframe

        Input:
            Dictionary of dataframes and a column to sort by

        Returns:
            Dataframe sorted by material number
        '''
        # concat along the rows (first axis; axis=0)
        # the number of columns is irrelevant
        return pd.concat(
            [dataframe for dataframe in self.df_dict.values()],
            axis=0
        ).sort_values('Mat. No').reset_index().drop(columns='index')

    def final_dataframe(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        '''
        Maps row data of dataframe into individual columns of Material(s),
        Substance, Test type, and Result (mg/kg)

        Input:
            Dataframe of material numbers, substances (columns), and results

        Returns:
            Dataframe organized by Material, Substance, Test, and Result
        '''
        # dictionary with the appropriate columns needed for final dataframe
        df_mapper = {
            'Material(s)': [],
            'Substance': [],
            'Test': [],
            'Result (mg/kg)': []
        }

        # get the unique materials tested
        materials = dataframe['Mat. No'].unique()
        for material in materials:
            partition = dataframe[dataframe['Mat. No'] == material]
            N = partition.shape[0]
            # iterate by row
            for i in range(N):
                vals = partition.iloc[i].dropna()
                columns = vals.index[1:] # skip material number
                test = vals.loc['Test']
                # material and test are appended every time to ensure
                # all lists are the same size in the dictionary
                for column in columns:
                    if column != 'Test': # ignore test column
                        df_mapper['Material(s)'].append(material)
                        df_mapper['Substance'].append(column)
                        df_mapper['Test'].append(test)
                        res = vals[column]
                        if ('<' in res) or (res == 'NT') or (res == 'n.d.'):
                            df_mapper['Result (mg/kg)'].append(vals[column])
                        else:
                            df_mapper['Result (mg/kg)'].append(float(res))
        return pd.DataFrame(df_mapper)

    def results_corrections(self, df: pd.DataFrame) -> pd.DataFrame:
        '''
        Removes rows that have results not necessary to report

        Input:
            Dataframe organized by Material, Substance, Test, and Result

        Returns:
            Dataframe organized by Material, Substance, Test, and Result
        '''
        # removing rows that aren't necessary to report
        # i.e. anything non-detected or not tested
        df = df.query(
            "Substance != 'Conclusion' & (`Result (mg/kg)` != 'NT')"
        
        )
        # get the test "REACH"
        test = self.special_tests[0]
        column = 'Result (mg/kg)'
        limit = 0.1 # REACH limit is 0.1 % to report results 
        partition = df.loc[df['Test'] == test, :]
        partition = partition.astype({column: np.float32})
        indices = partition[partition[column] < 0.1].index
        # remove REACH indices, update the index, and remove index column
        df = df.drop(axis=0, index=indices).reset_index().drop(columns='index')
        # update REACH and MDR results to correct units
        for test in self.special_tests[:2]:
            scaled = df.loc[df['Test'] == test, column]
            if scaled.dtype is not float:
                scaled = scaled.astype({column: np.float32})
            scaled = scaled * 10000
            scaled_indices = scaled.index
            results = scaled.values
            df.loc[scaled_indices, column] = results
        return df

    def map_results(self, df: pd.DataFrame, mapper: dict) -> pd.DataFrame:
        df['Substance'] = df['Substance'].apply(
            lambda x: mapper[x] if x in mapper else x
        )
        return df

    # def run(self):
        # self.refactor_dataframes()
        # dataframe = self.concat_dataframes()
        # final = self.final_dataframe(dataframe)
        # corrected = self.results_corrections(final)
        # mapped = self.map_results(corrected, sub_mapper)
        # return mapped