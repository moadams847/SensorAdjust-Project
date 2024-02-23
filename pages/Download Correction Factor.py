import streamlit as st
import os
from datetime import datetime


from utilities.read_process_data_utility import get_session_directory

# Get the current date and time
now = datetime.now()

# Format the date and time
formatted_now = now.strftime("%Y-%m-%d %H:%M:%S")


# Assuming get_session_directory() is a function that returns the path object of the session directory
session_dir = get_session_directory()

def list_joblib_files(directory):
    """Lists .joblib files in a given directory"""
    return [file for file in os.listdir(directory) if file.endswith('.joblib')]

# List .joblib files in the directory
joblib_files = list_joblib_files(session_dir)

if joblib_files:
    # st.subheader("Available correction factor in the cloud directory:")
    
    # Let the user select a file to download
    selected_file = st.selectbox("Download file", joblib_files)


    
    # Full path to the selected file
    file_path = os.path.join(session_dir, selected_file)
    
    # Create a download button for the selected file
    with open(file_path, "rb") as file:
        st.download_button(
            label="Download",
            data=f'{file}',
            file_name=selected_file,
            mime='application/octet-stream'
        )
else:
    st.warning("No correction factor found in the cloud directory.")
