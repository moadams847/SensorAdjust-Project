import streamlit as st
import pandas as pd
import os
from pathlib import Path
import uuid
from io import StringIO

def ensure_session_id():
    if 'session_id' not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())

def get_session_directory(): 
    ensure_session_id()
    session_dir = Path('artifacts') / st.session_state.session_id
    session_dir.mkdir(parents=True, exist_ok=True)
    return session_dir

def load_specific_csv_from_session_directory(session_directory_getter, preferred_filenames=['uploaded_data.csv']):
    """
    Loads a specific CSV file, preferring 'data.csv' or 'resampled.csv', found in the session-specific directory.

    Parameters:
    - session_directory_getter: A callable that returns a Path object representing the session-specific directory.
    - preferred_filenames: List of filenames to look for, in order of preference.

    Returns:
    - A pandas DataFrame loaded from the specified CSV file, or None if the files are not found.
    """
    session_dir = session_directory_getter()  # Get session-specific directory as a Path object

    # Look for preferred files first
    for filename in preferred_filenames:
        file_path = session_dir / filename
        if file_path.exists():
            try:
                df = pd.read_csv(file_path, parse_dates=["DataDate"])
                return df
            except ValueError as e:
                if "DataDate" in str(e):
                    st.error(f"The 'DataDate' column is required but was not found in {filename}.")
                else:
                    st.error(f"An error occurred while reading {filename}.")
                return None
    
    # If preferred files are not found, look for any CSV file
    csv_files = list(session_dir.glob('*.csv'))
    if csv_files:
        try:
            df = pd.read_csv(csv_files[0], parse_dates=["DataDate"])
            return df
        except ValueError as e:
            if "DataDate" in str(e):
                st.error("The 'DataDate' column is required but was not found in the CSV file.")
            else:
                st.error("An error occurred while reading the CSV file.")
            return None
    else:
        st.warning("No CSV file found in the cloud directory.")
        return None


def summary_statistics(df):
    try:

        if df is not None:
            st.write(f"Data")
            st.write(df)

            st.write(f"Data Information")
            buffer = StringIO()
            df.info(buf=buffer)
            s = buffer.getvalue()
            st.text(s)

            st.write(f"Summary statistics")
            st.write(df.iloc[:, df.columns != 'DataDate'].describe())

    except ValueError as e:
                st.error("Something might be wrong with with the uploaded file")
        
def resample_and_aggregate(data, resample_freq, aggregation_func):
        """
        Resample a DataFrame by a specified frequency and perform aggregation using a given function.
        
        Parameters:
            - data: DataFrame
                The input DataFrame to be resampled and aggregated.
            - resample_freq: str
                The resampling frequency (e.g., 'H' for hourly, 'D' for daily).
            - aggregation_func: str
                The aggregation function to apply ('mean', 'max', or 'min').

        Returns:
            - resampled_df: DataFrame
                The resampled and aggregated DataFrame.
        """

        resampled_df = None  # Initialize resampled_df to handle cases where data might be None

        if data is not None:
            data['DataDate'] = pd.to_datetime(data['DataDate'])
            data = data.set_index('DataDate') 

            if aggregation_func == 'mean':
                resampled_df = data.resample(resample_freq).mean()
            elif aggregation_func == 'max':
                resampled_df = data.resample(resample_freq).max()
            elif aggregation_func == 'min':
                resampled_df = data.resample(resample_freq).min()
            else:
                raise ValueError("Invalid aggregation function. Choose 'mean', 'max', or 'min'.")
        return resampled_df


# def resample_and_merge_csv(df1, df2, date_format='%Y-%m-%d %H:%M:%S', resample_freq='T'):
def resample_and_merge_csv(df1, df2, resample_freq='T'):

    def prepare_df(df):
        # Convert 'DataDate' to datetime and set as index
        df['DataDate'] = pd.to_datetime(df['DataDate'])
        df.set_index('DataDate', inplace=True)
        
        # Check if the index is a DatetimeIndex before resampling
        if isinstance(df.index, pd.DatetimeIndex):
            return df.resample(resample_freq).mean().dropna()
        else:
            raise TypeError("Index is not a DatetimeIndex. Resampling requires a DatetimeIndex.")
    
    try:
        df1_prepared = prepare_df(df1)
        df2_prepared = prepare_df(df2)
        
        # Inner merge the two DataFrames based on the date index
        merged_df = pd.merge(df1_prepared, df2_prepared, left_index=True, right_index=True, how='inner')
        
        # Optionally, reset the index if you want 'DataDate' back as a column
        merged_df.reset_index(inplace=True)
        
        return merged_df, merged_df.isnull().sum()

    except ValueError as e:
        st.error(f"Error: {e}")
        return None, None
    except TypeError as e:
        st.error(f"Error: {e}")
        return None, None
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        return None, None

# Example usage:
# merged_df, null_counts = resample_and_merge_csv(df1, df2, date_format='%Y-%m-%d %H:%M:%S', resample_freq='H')


def add_suffix_to_columns(df, suffix, exclude_column):
    """
    Adds a suffix to all columns in a DataFrame except for specified columns to exclude.

    Parameters:
    - df (pd.DataFrame): The DataFrame to modify.
    - suffix (str): The suffix to add to the column names.
    - exclude_column (str or list): The column name(s) to exclude from having the suffix added.
    """
    if isinstance(exclude_column, str):
        exclude_column = [exclude_column]  # Convert to list for uniform processing
    
    df.columns = [col + suffix if col not in exclude_column else col for col in df.columns]


