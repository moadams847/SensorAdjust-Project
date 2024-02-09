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

def file_upload_form_for_already_paired():
    return st.file_uploader("Upload already paired data (CSV)", type=['csv'])

def custom_date_parser(date):
    return pd.to_datetime(date, format='%d/%m/%Y %H:%M')

def files_upload_for_already_paired():
    session_dir = get_session_directory()  # Use session-specific directory
    
    # File uploader placeholder
    placeholder = st.empty()

    with st.form("Paird Data"):
        uploaded_already_paired_data = file_upload_form_for_already_paired()

        submit_button = st.form_submit_button('Submit')

        if submit_button:
            if uploaded_already_paired_data is None:
                st.warning("Please upload paired data to proceed.")
            else:
                placeholder.success("Uploaded successfully to the cloud")
                already_paired_df = pd.read_csv(uploaded_already_paired_data, 
                                                parse_dates=["DataDate"])
                st.write(already_paired_df.head())
                
                # Save file in session directory
                already_paired_df.to_csv(session_dir / 'already_paired_data.csv', index=False)


# def read_files_from_directory():
#      session_dir = get_session_directory()  # Use session-specific directory

#      csv_files = list(session_dir.glob('*.csv'))
#      print(csv_files)
     
#      if not csv_files:
#          st.warning("No CSV files found in the cloud directory.")
#      else:
#          data = pd.read_csv(csv_files[0], parse_dates=["DataDate"])
#          return data
        

def read_files_from_directory(filename):
    session_dir = Path(get_session_directory())  # Ensure session_dir is a Path object

    # Build the full path to the target file within the session directory
    target_file = session_dir / filename

    # Check if the target file exists
    if not target_file.exists():
        st.warning(f"No file found in the cloud directory.")
        return None

    # If the file exists, read it into a DataFrame
    data = pd.read_csv(target_file)
    # print(data.info())
    return data


def read_already_paired_dfs():
    df = read_files_from_directory("already_paired_data.csv")
    st.write(df)


def summary_statistics():
    df = read_files_from_directory('already_paired_data.csv')

    if df is not None:
        
        st.write(f"Uploaded Data")
        st.write(df)

        st.write(f"Data Information")
        buffer = StringIO()
        df.info(buf=buffer)
        s = buffer.getvalue()
        st.text(s)

        st.write(f"Summary statistics")
        st.write(df.iloc[:, df.columns != 'DataDate'].describe())

        
def resample_and_aggregate(resample_freq, aggregation_func):
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

        data = read_files_from_directory("already_paired_data.csv")
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




