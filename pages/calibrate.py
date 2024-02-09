import streamlit as st
from utilities.read_process_data_utility import (
    files_upload_for_already_paired, 
    summary_statistics, 
    resample_and_aggregate,get_session_directory, ensure_session_id, read_files_from_directory)


st.header("File Selection for Calibration")

cleaned_data = None

# Assuming session_dir is a Path object
session_dir = get_session_directory()

csv_files = list(session_dir.glob('*.csv'))
file_options = {
    "Uploaded Data": "already_paired_data.csv",
    "Resampled Data": "resampled_data.csv"
}

if not csv_files:
    st.warning("No CSV files found in the cloud directory.")
else:
    # Map user choices to filenames
    choice_to_filename = {label: filename for label, filename in file_options.items() if (session_dir / filename) in csv_files}
    
    if not choice_to_filename:
        st.error("Required calibration files are missing.")
    else:
        # Let the user select from available options that match files found
        paired_label = st.radio("Select File for Calibration", list(choice_to_filename.keys()))
        print(file_options[paired_label])
        filename =file_options[paired_label]
        df = read_files_from_directory(filename)
        cleaned_data = df.dropna()
        cleaned_data.reindex()
        print(cleaned_data)
        st.write(cleaned_data.head())

       

tab1, tab2, tab3, tab4, tab5 = st.tabs(["Line Plot", "Select Machine Learning Model",  "Cross Validation", "Create Correction Factor", "View Metrics"])

with tab1:
    st.header("Line Plot")
    if cleaned_data is None:
        print("Check")
    else:
        pass

with tab2:
    st.header("Select Machine Learning Model")

with tab3:
    st.header("Cross Validation")

with tab4:
    st.header("Create Correction Factor")

with tab5:
    st.header("View Metrics")

    
                

           

            



    
       
        


   


