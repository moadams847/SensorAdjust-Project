import streamlit as st
from io import StringIO
from pathlib import Path
import pandas as pd

# Modelling
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from sklearn.model_selection import RandomizedSearchCV
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
import warnings

from utilities.read_process_data_utility import ( 
    summary_statistics, load_specific_csv_from_session_directory,
    resample_and_aggregate, get_session_directory, ensure_session_id, 
    load_specific_csv_from_session_directory)

from utilities.calibration_utility import ( 
    check_files_in_directory, select_and_read_file, plot_line_graph, 
    compute_rmse, compute_mae, plot_scatter_with_one_to_one_line, evaluate_model)

from utilities.line_plot_and_metrics_logic import (
    line_plot, metrics
    )

from utilities.basic_calibraton_logic import (basic_calibration)

# from utilities.Advanced_calibration_logic import (advanced_calibrations)


session_dir = get_session_directory()  # Use session-specific directory


# "st.session_state object", st.session_state

# if "my_radio" in st.session_state:
#     st.write(f"You selected: {st.session_state.my_radio}")

tab1, tab2, tab3, tab4, tab5 = st.tabs(["Data for Calibration ", "Line Graph", "Metrics and Scatter Plot", "Create Correction Factor", "Graph and metrics"])

with tab1:
    st.header("Data stored in the cloud directory")

    file_options = ["uploaded_data.csv", "resampled_data.csv"]
    warning_message = "No files found in the directory."
    file_selection  = "Select CSV file for calibration"
    df = select_and_read_file(file_options, warning_message, file_selection, key="calibration_file_selection")
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
        
with tab2:
    st.header("Line graph before calibration")
    csv_file_list = ["uploaded_data.csv", "resampled_data.csv"]
    line_plot(csv_file_list)

with tab3:
    st.header("Metrics with scatter Plot before calibration")
    csv_file_list = ["uploaded_data.csv", "resampled_data.csv"]
    metrics(csv_file_list)
    
with tab4:
    st.header("Create Correction Factor")

    type_of_calibration = st.selectbox("Select type", ["Basic", "Advanced"])

    if type_of_calibration == "Basic":
        basic_calibration()

    else:
        # advanced_calibrations()
        st.write("Coming Soon")

with tab5:
    type_of_metric_graph = st.selectbox("Select", ["Line Graph", "Metrics with Scatter plot"])
    csv_file_list = ["calibrated_data.csv"]

    if type_of_metric_graph == 'Line Graph':
        st.header("Line graph after Calibration")
        line_plot(csv_file_list, "line_plot_file_selection_calibrated", "line_plot_file_selection_calibrated_two", "line plot form calibrated")

    else:
        st.header("Metrics with Scatter Plot after Calibration")
        metrics(csv_file_list, "sensor_metrics_file_selection_one", "sensor_metrics_file_selection_two", "sensor metrics form calibrated")






    
                

           

            



    
       
        


   


