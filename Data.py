import streamlit as st
import pandas as pd
import warnings

# Ignore all warnings
warnings.filterwarnings('ignore')

from utilities.read_process_data_utility import (
    summary_statistics, load_specific_csv_from_session_directory, 
    resample_and_aggregate, get_session_directory, resample_and_merge_csv,
    add_suffix_to_columns)


if 'DateTimeFormat_input' not in st.session_state:
    st.session_state['DateTimeFormat_input'] = "%Y-%m-%d %H:%M:%S"

if 'DateTimeColumn_input' not in st.session_state:
    st.session_state['DateTimeColumn_input'] = "DataDate"

def custom_date_parser(date):
    format_ = st.session_state["DateTimeFormat_input"]
    return pd.to_datetime(date, format=format_)

tab1, tab2, tab3, tab4  = st.tabs(["Documentation", "Upload Data", "View Data", "Resample Data"])
   
with tab1:
    st.title("Guide for SensorAdjust Project")

    st.markdown("""
    **Overview**: SensorAdjust is an open source project that aims to simplify 
    the calibration process for users with minimal or no coding expertise. 
    By enabling users to directly upload data from both low-cost sensors and reference monitors, or data that has already 
    been paired, the platform effortlessly creates a correction factor based on the uploaded data, provided the users follow the specified guidelines. 
    This generated correction factor can be applied to the low-cost sensor data to significantly improve its accuracy, thereby democratizing access to high-quality environmental monitoring for everyone.
    """, unsafe_allow_html=False)

    st.markdown("""
    **Objective**: The primary objective of the SensorAdjust Project is to 
    democratize access to accurate environmental data collection. We aim to accomplish this by 
    offering a user-friendly platform that 
    automates the generation of correction factors for low-cost sensors in 
    comparison to reference monitors. This initiative guarantees that all users, 
    irrespective of their technical expertise, can effortlessly calibrate their low-cost 
    sensor data. By simplifying this process, we ensure that accurate environmental 
    monitoring is accessible to everyone, enabling users to trust and utilize their 
    data for a wide range of applications with confidence.
    """, unsafe_allow_html=False)


    st.markdown("""
    ### How to Use the SensorAdjust System

    In this section, we'll guide you through the essential steps to prepare your data for upload to the SensorAdjust project platform. 
    Adhering to these guidelines will guarantee a seamless generation of the correction factor:

    1. **Preparing Your Data Timestamp:**
    - Make sure the column containing the timestamps in your dataset is named `DataDate`. This is crucial for the system to correctly recognize and format the Timestamp column.

    2. **Cleaning Your Data:**
    - Before uploading, review your dataset to remove any unnecessary columns. This helps in streamlining the process of creating the correction factor and ensures that the system focuses only on relevant data.
    - If you are uploading both reference monitor data and low-cost sensor data separately, the system will automatically modify the column names for clarity:
    - Column names in the reference monitor data, except for the `DataDate` column, will be suffixed with `_Reference`. For example, a column named `PM2.5` will be renamed to `PM2.5_Reference`.
    - Similarly, column names in the low-cost sensor data, excluding the `DataDate` column, will be suffixed with `_LCS` (indicating Low-Cost Sensor). For example, `PM2.5` becomes `PM2.5_LCS`.
    - If your dataset is already paired (meaning each timestamp has corresponding values from both the low-cost sensor and the reference monitor), and you upload this combined data, the platform will not alter the column names. This feature is designed to accommodate users who have pre-processed their data.

    Adhering to these preparatory guidelines guarantees that your data is properly formatted and ready for the SensorAdjust platform. This initial preparation is crucial for fully harnessing the platform's potential, facilitating a streamlined and precise generation of correction factor. Consequently, you can apply this correction factor to your low-cost sensor data with confidence, ensuring accuracy and reliability in your environmental monitoring efforts. 
    """, unsafe_allow_html=True)










 
with tab2:
    paired = st.radio("Is your data paired alreday?", ["Yes", "No"])
    
    if paired == "Yes":

        session_dir = get_session_directory()  # Use session-specific directory
    
        # File uploader placeholder
        placeholder = st.empty()

        uploaded_already_paired_data = st.file_uploader("Upload already paired data (CSV)", type=['csv'])

        if uploaded_already_paired_data is None:

            st.warning("Please upload data to proceed.")

        else:
            try:
                already_paired_df = pd.read_csv(uploaded_already_paired_data, parse_dates=["DataDate"])
                        
                st.subheader("First five rows of the uploaded data")
                st.write(already_paired_df.head())
                        
                # Save file in session directory
                already_paired_df.to_csv(session_dir / 'uploaded_data.csv', index=False)
                placeholder.success("File successfully uploaded to the cloud as uploaded_data.csv")

            except ValueError as e:
                if "DataDate" in str(e):
                    st.error("The 'DataDate' column is required but was not found in the CSV file.")
                else:
                    # Handle other ValueError exceptions here if necessary
                    st.error("An error occurred while reading the CSV file.")
    else:
        session_dir = get_session_directory()  # Use session-specific directory

        # File uploader placeholders
        uploaded_low_cost_sensor_data = st.file_uploader("Upload low-cost sensor data (CSV)", type=['csv'])
        placeholder_one = st.empty()
        header_placeholder_one = st.empty()
        data_placeholder_one = st.empty()

        uploaded_reference_data = st.file_uploader("Upload reference monitor data (CSV)", type=['csv'])
        placeholder_two = st.empty()
        header_placeholder_two = st.empty()
        data_placeholder_two = st.empty()

        # Initialize flags to check if data is uploaded
        uploaded_low_cost_sensor_df = None
        uploaded_reference_df = None

        # Check and read the low-cost sensor data
        if uploaded_low_cost_sensor_data is not None:
            try:
                uploaded_low_cost_sensor_df = pd.read_csv(uploaded_low_cost_sensor_data, parse_dates=["DataDate"])
               
                #add suffix
                suffix = "_LCS"
                exclude_column = "DataDate"
                add_suffix_to_columns(uploaded_low_cost_sensor_df, suffix, exclude_column)

                header_placeholder_one.subheader("First five rows of uploaded low-cost sensor data")
                data_placeholder_one.write(uploaded_low_cost_sensor_df.head())
                placeholder_one.success("Low-cost sensor data uploaded successfully to the cloud")
            except ValueError as e:
                st.error(f"Error processing low-cost sensor data: {e}")

        # Check and read the reference monitor data
        if uploaded_reference_data is not None:
            try:
                uploaded_reference_df = pd.read_csv(uploaded_reference_data, parse_dates=["DataDate"])

                #add suffix
                suffix = "_Reference"
                exclude_column = "DataDate"
                add_suffix_to_columns(uploaded_reference_df, suffix, exclude_column)

                header_placeholder_two.subheader("First five rows of uploaded reference monitor data")
                data_placeholder_two.write(uploaded_reference_df.head())
                placeholder_two.success("Reference monitor data uploaded successfully to the cloud")
            except ValueError as e:
                st.error(f"Error processing reference monitor data: {e}")
                
        # Proceed only if both dataframes are available
        if uploaded_low_cost_sensor_df is not None and uploaded_reference_df is not None:
            merged_df, null_counts = resample_and_merge_csv(uploaded_low_cost_sensor_df, uploaded_reference_df)
            
            if merged_df is not None:
                # It's safe to save the DataFrame to a CSV file
                merged_df.to_csv(session_dir / 'uploaded_data.csv', index=False)
                st.success("Data merged and saved successfully as uploaded_data.csv")
            else:
                # Handle the situation when merged_df is None
                st.error("Failed to merge data. Check if the data formats are correct.")
        else:
            st.warning("Please upload data to proceed.")

    
with tab3:
    st.header("View Data")
    df = load_specific_csv_from_session_directory(get_session_directory, ["uploaded_data.csv"])

    # Proceed with checking if df is not None and then using the DataFrame
    if df is not None:
        # Perform operations with df
        summary_statistics(df)

with tab4:
    st.header("Resampled Data")
    with st.form("Aggregate"):

        # Creating columns to organize the form
        col1, col2 = st.columns([2, 2])

        with col1:

            aggregation_func = st.selectbox("Select an Aggregation Function", ['mean', 'max', 'min'])
            
        with col2:

            frequency_mapping = {
            'Minute Average': 'T',
            'Hourly Average': 'H',
            'Daily Average': 'D'
            }

            # Streamlit UI for selecting aggregation frequency
            resample_freq = st.selectbox("Select an Aggregation Frequency", list(frequency_mapping.keys()))

        
        submit_button = st.form_submit_button('Resample')
       
        if submit_button:
            
            # Convert the friendly frequency to its corresponding code
            freq_code = frequency_mapping[resample_freq]

            df = load_specific_csv_from_session_directory(get_session_directory, ["uploaded_data.csv"])

            # Proceed with checking if df is not None and then using the DataFrame
            if df is not None:
                    result_df = resample_and_aggregate(df, freq_code, aggregation_func)
                    # print(result_df)
                    cleaned_data = result_df.dropna()
                    # st.write(cleaned_data)

                    # Save file in session directory
                    placeholder_resampled = st.empty()
                    session_dir = get_session_directory()  # Use session-specific directory
                    cleaned_data.to_csv(session_dir / 'resampled_data.csv', index=True)
                    placeholder_resampled.success("Resampled data successfully saved to the cloud as resampled_data.csv")
                    df_resampled = load_specific_csv_from_session_directory(get_session_directory, ["resampled_data.csv"])
                    summary_statistics(df_resampled)


   


