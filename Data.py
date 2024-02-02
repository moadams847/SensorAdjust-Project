import streamlit as st
from utility import files_upload_for_low_cost_sensor_and_reference_monitor, files_upload_for_already_paired, summary_statistics


tab1, tab2, tab3, tab4, tab5  = st.tabs(["Instructions", "Upload Data", "Data Info", "Merge Data", "Aggregate Data"])
   
with tab1:
    st.header("Instructions")
   
with tab2:
    paired = st.radio("Is your data paired alreday?", 
                      ["Yes", "No"])
    
    if paired == "Yes":
        files_upload_for_already_paired()
    else:
        files_upload_for_low_cost_sensor_and_reference_monitor()

with tab3:
    st.header("Data Info")
    summary_statistics()

with tab4:
    st.header("Merge Data")


with tab5:
    st.header("Aggregate Data")

   


