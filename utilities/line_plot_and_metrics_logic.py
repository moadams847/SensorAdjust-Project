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

def line_plot(csv_file_list, key_value_one="line_plot_file_selection", key_value_two="line_plot_col_selection_two", form_value="line plot form"):
    # file_options = ["uploaded_data.csv", "resampled_data.csv", "calibrated_data.csv"]
    file_options = csv_file_list
    warning_message = "No files found in the cloud directory."
    file_selection  = "Select CSV file for line Plot"
    df = select_and_read_file(file_options, warning_message, file_selection, key=key_value_one)
    if df is not None:
            cols = df.columns
            item_to_exclude = 'DataDate'
            updated_col = list(filter(lambda item: item != item_to_exclude, cols))

            with st.form(form_value):
                col_options_line_plot = st.multiselect(
                'Select columns for the line plot',
                updated_col, key=key_value_two, placeholder="Select columns")

                submit_to_plot = st.form_submit_button('Plot')

                if submit_to_plot:
                    if len(col_options_line_plot) >=1:
                        plot_line_graph(df, 'DataDate', col_options_line_plot, col_options_line_plot)
                        session_dir = get_session_directory() 
                        image_filename = "line_plot.png" 
                        image_path = session_dir / image_filename
                        st.image(str(image_path))
                    else:
                        st.warning("Please select a data column")


#--------------------------------------------------------------------------------------------
def metrics(csv_file_list, key_value_one="sensor_metrics_file_selection", key_value_two="sensor_metrics_col_selection", form_value="sensor metrics form"):
    file_options = csv_file_list
    # file_options = ["uploaded_data.csv", "resampled_data.csv", "calibrated_data.csv"]
    warning_message = "No files found in the cloud directory."
    file_selection  = "Select CSV file for Sensor Metrics"
    df = select_and_read_file(file_options, warning_message, file_selection, key=key_value_one)

    if df is not None:
        cols = df.columns
        item_to_exclude = 'DataDate'
        updated_col = list(filter(lambda item: item != item_to_exclude, cols))

        with st.form(form_value):
            col_options_sensor_metrics = st.multiselect(
            'Select columns for sensor metrics',
            updated_col, key=key_value_two, placeholder="Select columns")

            submit_to_compute_metrics = st.form_submit_button('Compute Metrics')

            if submit_to_compute_metrics:
                if len(col_options_sensor_metrics) ==2:

                    rmse = compute_rmse(df, col_options_sensor_metrics[0], col_options_sensor_metrics[1])
                    # st.write(rmse)

                    mae = compute_mae(df, col_options_sensor_metrics[0], col_options_sensor_metrics[1])
                    # st.write(mae)

                    correlation = df[col_options_sensor_metrics[0]].corr(df[col_options_sensor_metrics[1]])
                    # st.write(correlation)

                    r_squared = correlation ** 2
                    # st.write(r_squared)

                    difference = df[col_options_sensor_metrics[0]] - df[col_options_sensor_metrics[1]]
                    bias = difference.mean()
                    # st.write(bias)

                    # Create a DataFrame to hold the results
                    metrics_df = pd.DataFrame({
                        'Metric': ['RMSE', 'MAE', 'Correlation', 'R-squared'],
                        'Value': [rmse, mae, correlation, r_squared]
                    })

                    # Round the 'Value' column to two decimal places
                    metrics_df['Value'] = metrics_df['Value'].round(12)
                    
                    # Display the DataFrame in Streamlit
                    transposed_metrics_df = metrics_df.transpose()

                    st.subheader("Metrics")
                    st.write(transposed_metrics_df)\
                    
                    plot_scatter_with_one_to_one_line(df, col_options_sensor_metrics[0], col_options_sensor_metrics[1])

                    session_dir = get_session_directory() 
                    image_filename = "scatter_plot.png" 
                    image_path = session_dir / image_filename

                    st.subheader("Scatter Plot")
                    st.image(str(image_path))
                else:
                    st.warning("Only two columns can be selected at a time")

    