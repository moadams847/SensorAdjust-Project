import streamlit as st
from io import StringIO
from pathlib import Path
import pandas as pd
import os


# Modelling
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from sklearn.model_selection import RandomizedSearchCV
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import Pipeline
from joblib import dump, load
import warnings

from utilities.read_process_data_utility import ( 
    summary_statistics, load_specific_csv_from_session_directory,
    resample_and_aggregate, get_session_directory, ensure_session_id, 
    load_specific_csv_from_session_directory)

from utilities.calibration_utility import ( 
    check_files_in_directory, select_and_read_file, plot_line_graph, 
    compute_rmse, compute_mae, plot_scatter_with_one_to_one_line, evaluate_model)


def basic_calibration():
    file_options = ["uploaded_data.csv", "resampled_data.csv"]
    warning_message = "No files found in the cloud directory."
    file_selection  = "Select CSV file to create correction factor"

    df = select_and_read_file(file_options, warning_message, file_selection, key="create_correction_file_selection")
    if df is not None:
        df_copy = df.copy()
        cols = df.columns
        item_to_exclude = 'DataDate'
        updated_col = list(filter(lambda item: item != item_to_exclude, cols))

        with st.form("create correction factor"):

            # Save file in session directory
            session_dir = get_session_directory()  # Use session-specific directory

            col_options_create_correction_independent = st.multiselect('Select independent column(s)',
            updated_col, key="create_correction_col_selection_independent", 
            placeholder="Select column(s)",)

            col_options_create_correction_dependent = st.selectbox('Select dependent column',
            updated_col, key="create_correction_col_selection_dependent", index=None, placeholder="Select a column")

            submit_to_create_correction = st.form_submit_button('Create correction factor')

            if submit_to_create_correction:
                # st.write(col_options_create_correction_independent)
                # st.write(col_options_create_correction_dependent)

                print(col_options_create_correction_independent)
                print(col_options_create_correction_dependent)

                if col_options_create_correction_dependent not in col_options_create_correction_independent:
                
                    # Construct the full path for the model file
                    model_path = session_dir / f'correction_factor.joblib'  # If session_dir is a Path object
                    
                    X = df[col_options_create_correction_independent]
                    numerical_columns = X.select_dtypes(exclude="object").columns

                    y = df[col_options_create_correction_dependent]

                    imputer = SimpleImputer(strategy="median")

                    preprocessor = ColumnTransformer(
                    [
                        ('imputer', imputer, numerical_columns),      
                    ])

                    # X_proccessed = preprocessor.fit_transform(X)

                    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
                    
                    # X_train.shape, X_test.shape

                    model =  LinearRegression()

                    # Create a pipeline that includes the preprocessing steps and the model
                    pipeline = Pipeline(steps=[
                        ('preprocessor', preprocessor),
                        ('model', model)
                    ])

                    pipeline.fit(X_train, y_train)

                    # Save the model to the specified directory
                    dump(pipeline, model_path)

                    # Get coefficients and intercept
                    coefficients = model.coef_
                    # st.write(coefficients)
                    intercept = model.intercept_
                    # st.write(intercept)

                    st.subheader("Correction factor")
                    features = numerical_columns
                    # Construct the equation string using f-string
                    equation = f"correction factor = {intercept:.2f}"
                    for coef, feature in zip(coefficients, features):
                        equation  +=  f" + [({coef:.2f}) * {feature}]"
                    st.code(equation)

                    # Make predictions
                    y_train_pred = model.predict(X_train)

                    y_test_pred = model.predict(X_test)

                    # Evaluate Train and Test dataset
                    rmse, mae, correlation, r2_square, bias = evaluate_model(y_train, y_train_pred)
                    test_rmse, test_mae, test_correlation, test_r2_square, test_bias = evaluate_model(y_test, y_test_pred)

                    #cross validation
                    lin_scores = cross_val_score(model, X_train, y_train,
                                                    scoring="neg_mean_absolute_error", cv=10)

                    # Convert scores to positive MAE scores
                    mae_scores = -lin_scores

                    # st.write("MAE scores:", mae_scores)

                    # st.write("Mean MAE:", mae_scores.mean())

                    # st.write("Standard deviation of MAE:", mae_scores.std())

                    cross_validation_MAE = mae_scores.mean()

                    # Create a DataFrame to hold the results
                    st.subheader("Test Set Metrics ")
                    metrics_df = pd.DataFrame({
                        'Metric': ['RMSE', 'MAE','CVMAE', 'Correlation', 'R-squared'],
                        'Value': [test_rmse, test_mae, cross_validation_MAE, test_correlation, test_r2_square]
                    })

                    # Round the 'Value' column to two decimal places
                    metrics_df['Value'] = metrics_df['Value'].round(12)

                    st.dataframe(metrics_df.T)

                    #----------------------------------------------------------------

                     # Attempt to load the model
                    try:
                        loaded_model = load(model_path)
                    except FileNotFoundError:
                        print(f"Model file not found at {model_path}.")
                        loaded_model = None
                    except Exception as e:
                        print(f"An error occurred while loading the model: {e}")
                        loaded_model = None

                    # Check if the model is loaded and then make predictions
                    if loaded_model is not None:
                        try:
                            new_data =  df_copy[col_options_create_correction_independent]
                            calibrated_col = loaded_model.predict(new_data)
                            calibrated_col_df=pd.DataFrame({f'Calibrated_column':calibrated_col})
                            horizontal_concat_of_cal_df = pd.concat([calibrated_col_df, df_copy, ], axis=1)  
                            
                            placeholder = st.empty()
                            st.subheader("Data after Calibration")
                            st.write(horizontal_concat_of_cal_df)
                            horizontal_concat_of_cal_df.to_csv(session_dir / 'calibrated_data.csv', index=False)
                            placeholder.success(f"'Calibrated_column' added to dataset and dataset saved as 'calibrated_data.csv'.")
        
                        except Exception as e:
                            print(f"An error occurred while making predictions: {e}")
                    else:
                        print("Model loading failed; predictions cannot be made.")

                    #extract index from y_train
                    # index = y_test.index

                    # selected_ref_pm2_5 = df.loc[index, "PM2_5_Ref"]
                    # selected_df_after_cal = df_copy.iloc[index]
                    # st.write(selected_df_after_cal)

                    # Calibrated df
                    # calibrated_df_pm25_df=pd.DataFrame({'Calibrated_PM2_5':y_test_pred}, index=index)
                    # st.write(calibrated_df_pm25_df)

                    # Concatenate horizontally
                    #Calibrated and Raw PM2_5
                    # st.subheader("Data after Calibration")
                    # horizontal_concat_of_cal_df = pd.concat([selected_df_after_cal, calibrated_df_pm25_df], axis=1)  # Place one beside the other
                    # placeholder = st.empty()
                    # st.dataframe(horizontal_concat_of_cal_df)

                   
                    # horizontal_concat_of_cal_df.to_csv(session_dir / 'calibrated_data.csv', index=False)
                    # placeholder.success("Updated dataframe successfully to the cloud as calibrated_data.csv")                
                else:
                    st.warning("An independent column cannot be selected as a dependent column")