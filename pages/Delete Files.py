import streamlit as st
import os
import shutil

from utilities.read_process_data_utility import ( 
    get_session_directory, ensure_session_id)

# Assuming get_session_directory() is a function that returns the path object of the session directory
session_dir = get_session_directory()

def list_files(directory):
    """Lists files in a given directory"""
    return [file for file in os.listdir(directory) if os.path.isfile(os.path.join(directory, file))]

def delete_all_files(directory):
    """Deletes all files in a given directory"""
    for file in os.listdir(directory):
        file_path = os.path.join(directory, file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)  # Removes each file
            elif os.path.isdir(file_path):  # Extra check in case there are directories
                shutil.rmtree(file_path)  # Removes directories and their contents
        except Exception as e:
            st.error(f"Error while deleting file {file_path}: {e}")

# Use a form for the delete operation
with st.form("Delete files in the cloud directory"):
    delete_all_files_button = st.form_submit_button('Delete all files')

if delete_all_files_button:
    delete_all_files(session_dir)
    st.success("All files have been deleted.")

    # Refresh the file list immediately after deletion
    files = list_files(session_dir)
else:
    # List files in the directory if the button wasn't clicked or after listing the updated directory
    files = list_files(session_dir)
    if files:
        st.subheader("Files in the cloud directory:")
        for file in files:
            st.write(file)
    else:
        st.warning("The cloud directory is empty.")
