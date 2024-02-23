import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mpl_dates
import numpy as np 

from utilities.read_process_data_utility import ( 
    summary_statistics, load_specific_csv_from_session_directory,
    resample_and_aggregate, get_session_directory, ensure_session_id)

def plot_line_graph(dataframe, x_column, y_columns, labels):
    sns.set_theme()

    plt.figure(figsize=(10, 7))

    for y_col, label in zip(y_columns, labels):
        sns.lineplot(x=x_column, y=y_col, data=dataframe, label=label)

    plt.gcf().autofmt_xdate()
    date_format = mpl_dates.DateFormatter('%b %d, %y')
    plt.gca().xaxis.set_major_formatter(date_format)

    plt.title(f'{", ".join(labels)} vs Date')
    plt.xlabel('(Date)')
    plt.ylabel(f'{", ".join(labels)} Values')
    plt.legend()
    # plt.show()
    session_dir = get_session_directory()  # Use session-specific directory
    plt.savefig(session_dir / 'line_plot.png', dpi=150)

# Assuming 'df' is your DataFrame
# plot_line_graph(df_new, 'DataDate', ['PM2_5_Ref', 'calibrated_PM2_5'], ['PM2_5_Ref', 'calibrated_PM2_5'])



def check_files_in_directory(session_dir, file_list):
    """
    Check which files in file_list exist in session_dir.

    Parameters:
    - session_dir: Path object representing the session-specific directory.
    - file_list: List of filenames (strings) to check.

    Returns:
    - List of filenames that exist in session_dir.
    """
    existing_files = [file for file in file_list if (session_dir / file).exists()]
    return existing_files

def select_and_read_file(file_options, warning_message, file_selection, key):
    session_dir = get_session_directory()
    available_files = check_files_in_directory(session_dir, file_options)

    if available_files:
        selected_file = st.radio(file_selection, available_files, key=key)
        
        if selected_file:
            df = load_specific_csv_from_session_directory(lambda: session_dir, [selected_file])
            if df is not None:
                return df  # Return the DataFrame after processing
            else:
                st.error("Failed to load the selected file.")
    else:
        st.warning(warning_message)
        return None  # Return None if no file is selected or if an error occurs
    

def compute_rmse(dataframe, column1, column2):
        """
        Computes the Root Mean Square Error (RMSE) between two columns in a pandas DataFrame.

        Parameters:
        dataframe (pandas.DataFrame): The DataFrame containing the columns for comparison.
        column1 (str): Name of the first column.
        column2 (str): Name of the second column.

        Returns:
        float: The Root Mean Square Error (RMSE) between the two columns.
        """

        # Ensure columns exist in the DataFrame
        if column1 not in dataframe.columns or column2 not in dataframe.columns:
            raise ValueError("One or both columns not found in the DataFrame.")

        # Remove rows with missing values in either column
        dataframe = dataframe.dropna(subset=[column1, column2])

        # Compute RMSE
        rmse = np.sqrt(np.mean((dataframe[column1] - dataframe[column2]) ** 2))
        
        return rmse

def compute_mae(dataframe, column1, column2):
    """
    Computes the Mean Absolute Error (MAE) between two columns in a pandas DataFrame.

    Parameters:
    dataframe (pandas.DataFrame): The DataFrame containing the columns for comparison.
    column1 (str): Name of the first column.
    column2 (str): Name of the second column.

    Returns:
    float: The Mean Absolute Error (MAE) between the two columns.
    """

    # Ensure columns exist in the DataFrame
    if column1 not in dataframe.columns or column2 not in dataframe.columns:
        raise ValueError("One or both columns not found in the DataFrame.")

    # Remove rows with missing values in either column
    dataframe = dataframe.dropna(subset=[column1, column2])

    # Compute MAE
    mae = np.mean(np.abs(dataframe[column1] - dataframe[column2]))
    
    return mae


def plot_scatter_with_one_to_one_line(dataframe, column1, column2):
    """
    Generates a scatter plot with a 1:1 line for comparing two columns of a DataFrame.

    Parameters:
    - dataframe (pandas.DataFrame): DataFrame containing the data.
    - column1 (str): Name of the first column to plot on the x-axis.
    - column2 (str): Name of the second column to plot on the y-axis.
    """
    # Scatter plot
    plt.figure(figsize=(10, 7))
    plt.scatter(dataframe[column1], dataframe[column2], alpha=0.5, label='Data Points')
    
    # 1:1 Line
    min_val = min(dataframe[column1].min(), dataframe[column2].min())
    max_val = max(dataframe[column1].max(), dataframe[column2].max())
    plt.plot([min_val, max_val], [min_val, max_val], 'r--', label='1:1 Line')
    
    plt.xlabel(column1)
    plt.ylabel(column2)
    plt.title(f'Scatter Plot with 1:1 Line: {column1} vs. {column2}')
    plt.legend()
    plt.grid(True)
    # plt.show()
    
    session_dir = get_session_directory()  # Use session-specific directory
    plt.savefig(session_dir / 'scatter_plot.png', dpi=150)

# plot_scatter_with_one_to_one_line(df, 'Sensor', 'Reference')
    

from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score


def calculate_bias(true_values, predicted_values):
    """
    Calculates the bias (mean difference) between true and predicted values.

    Parameters:
    - true_values (array-like): True values.
    - predicted_values (array-like): Predicted values.

    Returns:
    - float: The calculated bias.
    """
    # Ensure inputs are numpy arrays for consistent mathematical operations
    true_values = np.array(true_values)
    predicted_values = np.array(predicted_values)
    
    # Calculate the difference between true and predicted values
    difference = predicted_values - true_values
    
    # Calculate the mean of these differences
    bias = np.mean(difference)
    
    return bias

# # Example usage
# true = [100, 200, 300, 400, 500]
# predicted = [110, 190, 295, 405, 510]
# bias = calculate_bias(true, predicted)
# print(f"Bias: {bias}")

import numpy as np

def calculate_correlation(true, predicted):
    """
    Calculates the Pearson correlation coefficient between two arrays.

    Parameters:
    - true (array-like): True values.
    - predicted (array-like): Predicted values.

    Returns:
    - float: The Pearson correlation coefficient.
    """
    correlation_matrix = np.corrcoef(true, predicted)
    correlation = correlation_matrix[0, 1]  # Extract the off-diagonal element
    return correlation

# # Example usage
# true_values = np.array([1, 2, 3, 4, 5])
# predicted_values = np.array([1, 2, 3.5, 4, 5])
# correlation = calculate_correlation(true_values, predicted_values)
# print(f"Correlation: {correlation}")


def evaluate_model(true, predicted):
    mae = mean_absolute_error(true, predicted)
    rmse = np.sqrt(mean_squared_error(true, predicted))
    r2_square = r2_score(true, predicted)
    difference =  true - predicted
    bias = difference.mean()    
    correlation = calculate_correlation(true, predicted)
    return rmse, mae, correlation, r2_square, bias




