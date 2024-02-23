# import streamlit as st
# from io import StringIO
# from pathlib import Path
# import pandas as pd

# # Modelling
# from sklearn.metrics import mean_squared_error, r2_score
# from sklearn.linear_model import LinearRegression
# from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
# from sklearn.model_selection import RandomizedSearchCV
# from sklearn.preprocessing import OneHotEncoder, StandardScaler
# from sklearn.compose import ColumnTransformer
# from sklearn.impute import SimpleImputer
# from sklearn.model_selection import train_test_split
# import warnings

# from utilities.read_process_data_utility import ( 
#     summary_statistics, load_specific_csv_from_session_directory,
#     resample_and_aggregate, get_session_directory, ensure_session_id, 
#     load_specific_csv_from_session_directory)

# from utilities.calibration_utility import ( 
#     check_files_in_directory, select_and_read_file, plot_line_graph, 
#     compute_rmse, compute_mae, plot_scatter_with_one_to_one_line, evaluate_model)

# from utilities.pycaret_script import (run_pycaret_script)

# session_dir = get_session_directory()  # Use session-specific directory

# def advanced_calibrations():
#     file_options = ["uploaded_data.csv", "resampled_data.csv"]
#     warning_message = "No calibration files found in the directory."
#     file_selection  = "Select CSV file to create correction factor"

#     df = select_and_read_file(file_options, warning_message, file_selection, key="create_correction_file_selection")
#     if df is not None:
#         df_copy = df.copy()
#         cols = df.columns
#         item_to_exclude = 'DataDate'
#         updated_col = list(filter(lambda item: item != item_to_exclude, cols))

#         with st.form("create correction factor"):

#             col_options_create_correction_independent = st.multiselect('Select independent column(s)',
#             updated_col, key="create_correction_col_selection_independent", 
#             placeholder="Select column(s)",)

#             col_options_create_correction_dependent = st.selectbox('Select dependent column',
#             updated_col, key="create_correction_col_selection_dependent", index=None, placeholder="Select a column")

#             submit_to_create_correction = st.form_submit_button('Create correction factor')

#             if submit_to_create_correction:
#                 # st.write(col_options_create_correction_independent)
#                 # st.write(col_options_create_correction_dependent)

#                 # print(col_options_create_correction_independent)
#                 # print(col_options_create_correction_dependent)

#                 if col_options_create_correction_dependent not in col_options_create_correction_independent:
                    
#                     X = df[col_options_create_correction_independent]
                    
#                     y = df[col_options_create_correction_dependent]

#                     df_for_pycaret = pd.concat([X, y], axis=1)  # Place one beside the other
#                     st.write(df_for_pycaret)

#                     session_dir = get_session_directory()  # Use session-specific directory
#                     df_for_pycaret.to_csv(session_dir / 'data_for_pycaret.csv', index=True)

#                     df =  run_pycaret_script(col_options_create_correction_dependent, col_options_create_correction_independent)
#                     st.write(df)

                   
                    




                    