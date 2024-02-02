import streamlit as st
import pandas as pd
import os


def file_upload_form_for_already_paired():
    return st.file_uploader("Upload already paired data (CSV)", type=['csv'])

def file_upload_form_for_reference_monitor():
    return st.file_uploader("Upload Reference monitor data (CSV)", type=['csv'])

def file_upload_form_for_low_cost_sensor_data():
    return st.file_uploader("Upload Low-cost sensor data (CSV)", type=['csv'])

def read_csv_reference_monitor(uploaded_reference_monitor_data):
    return pd.read_csv(uploaded_reference_monitor_data)

def read_low_cost_sensor_data(uploaded_low_cost_sensor_data):        
    return pd.read_csv(uploaded_low_cost_sensor_data)
    

def files_upload_for_low_cost_sensor_and_reference_monitor():
    # File uploaders
    placeholder = st.empty()
    uploaded_low_cost_sensor_data = file_upload_form_for_low_cost_sensor_data()

    data_placeholder_one = st.empty()

    uploaded_reference_monitor_data = file_upload_form_for_reference_monitor()
    data_placeholder_two = st.empty()

    # Check if files are uploaded
    if uploaded_low_cost_sensor_data is not None and uploaded_reference_monitor_data is not None:
        
        placeholder.success(f"uploaded successfully to the cloud")

        # Read the uploaded reference monitor data
        reference_monitor_df = read_csv_reference_monitor(uploaded_reference_monitor_data)
        data_placeholder_two.write(reference_monitor_df)

        # Read the uploaded low-cost sensor data
        low_cost_sensor_df = read_low_cost_sensor_data(uploaded_low_cost_sensor_data)
        data_placeholder_one.write(low_cost_sensor_df)

        # Define default file paths for saving
        default_file_path1 = 'artifacts/low_cost_sensor_data.csv'
        default_file_path2 = 'artifacts/reference_monitor_data.csv'

        # Save the first CSV file automatically
        low_cost_sensor_df.to_csv(default_file_path1, index=False)

        # Save the second CSV file automatically
        reference_monitor_df.to_csv(default_file_path2, index=False)

    else:
        st.warning("Please upload both low-cost sensor data and reference monitor data to proceed.")



def files_upload_for_already_paired():

    # File uploaders
    placeholder = st.empty()

    uploaded_already_paired_data = file_upload_form_for_already_paired()

    # Check if files are uploaded
    if uploaded_already_paired_data is not None:

        placeholder.success(f"uploaded successfully to the cloud")

        already_paired_df = pd.read_csv(uploaded_already_paired_data)
        st.write(already_paired_df)

        already_paired_data_file_path = 'artifacts/already_paired_data.csv'
                
        # Save the second CSV file automatically
        already_paired_df.to_csv(already_paired_data_file_path, index=False)

    else:
        st.warning("Please upload paired to proceed.")



def summary_statistics():
    # Path to the artifacts directory
    artifacts_dir = 'artifacts'
    
    # List all files in the artifacts directory
    files = os.listdir(artifacts_dir)
    
    # Filter out CSV files
    csv_files = [file for file in files if file.endswith('.csv')]
    
    # Check if there are any CSV files
    if not csv_files:
        st.write("No CSV files found in the cloud directory.")
        return

    # If CSV files exist, process them
    for csv_file in csv_files:
        file_path = os.path.join(artifacts_dir, csv_file)
        df = pd.read_csv(file_path)
        st.write(f"Summary statistics for {csv_file}:")
        st.write(df.describe())
        



