import streamlit as st
from utilities.read_process_data_utility import (
    files_upload_for_already_paired, 
    summary_statistics, 
    resample_and_aggregate,get_session_directory, ensure_session_id)

tab1, tab2, tab3, tab4, tab5  = st.tabs(["Instructions", "Upload Data", "Data Info", "Pair Data", "Aggregate Data"])
   
with tab1:
    st.header("Instructions")
    st.write("Coming soon")
   
with tab2:
    paired = st.radio("Is your data paired alreday?", ["Yes", "No"])
    
    if paired == "Yes":
        files_upload_for_already_paired()
    else:
        st.write("Coming soon")

with tab3:
    st.header("Data Info")
    summary_statistics()

with tab4:
    st.header("Pair Data")
    # read_already_paired_dfs()
    st.write("Coming soon")

with tab5:
    st.header("Aggregate Data")

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
            # st.write(resample_freq)
            # st.write(aggregation_func)

             # Convert the friendly frequency to its corresponding code
            freq_code = frequency_mapping[resample_freq]

            # resampled_df = data.resample('H').mean()
            result_df = resample_and_aggregate(freq_code, aggregation_func)
            if result_df is not None:
                cleaned_data = result_df.dropna()
                st.write(cleaned_data.reindex())

                 # Save file in session directory
                session_dir = get_session_directory()  # Use session-specific directory
                cleaned_data.to_csv(session_dir / 'resampled_data.csv', index=False)
            
                

           

            



    
       
        


   


