# # files_upload_for_low_cost_sensor_and_reference_monitor, 
# # read_already_paired_dfs

# def file_upload_form_for_reference_monitor():
#     return st.file_uploader("Upload Reference monitor data (CSV)", type=['csv'])

# def file_upload_form_for_low_cost_sensor_data():
#     return st.file_uploader("Upload Low-cost sensor data (CSV)", type=['csv'])

# def read_csv(uploaded_file):
#     # Read a CSV file from an uploaded file object
#     return pd.read_csv(uploaded_file, parse_dates=["DataDate"])



# def files_upload_for_low_cost_sensor_and_reference_monitor():
#     session_dir = get_session_directory()  # Use session-specific directory
    
#     # File uploaders
#     placeholder = st.empty()

#     uploaded_low_cost_sensor_data = file_upload_form_for_low_cost_sensor_data()
#     data_placeholder_one = st.empty()

#     uploaded_reference_monitor_data = file_upload_form_for_reference_monitor()
#     data_placeholder_two = st.empty()

#     # Process uploaded files
#     if uploaded_low_cost_sensor_data and uploaded_reference_monitor_data:
#         placeholder.success("Uploaded successfully to the cloud")
        
#         # Process and display low-cost sensor data
#         low_cost_sensor_df = read_csv(uploaded_low_cost_sensor_data)
#         data_placeholder_one.write(low_cost_sensor_df)

#         # Process and display reference monitor data
#         reference_monitor_df = read_csv(uploaded_reference_monitor_data)
#         data_placeholder_two.write(reference_monitor_df)

#         # Save files in session directory
#         low_cost_sensor_df.to_csv(session_dir / 'low_cost_sensor_data.csv', index=False)
#         reference_monitor_df.to_csv(session_dir / 'reference_monitor_data.csv', index=False)
#     else:
#         st.warning("Please upload both low-cost sensor data and reference monitor data to proceed.")


# def resample_and_merge_csv(df1, df2):

#     # Convert the date columns to DataDate objects
#     df1['DataDate'] = pd.to_datetime(df1['DataDate'], format='%Y-%m-%d %H:%M:%S')
#     df2['DataDate'] = pd.to_datetime(df2['DataDate'], format='%Y-%m-%d %H:%M:%S')

#     # Set the date column as the index for resampling
#     df1.set_index('DataDate', inplace=True)
#     df2.set_index('DataDate', inplace=True)
    

#     # Resample both DataFrames from seconds to minutes, using the mean
#     df1 = df1.resample('T').mean().dropna()
#     df2 = df2.resample('T').mean().dropna()

#     # Inner merge the two DataFrames based on the date index
#     merged_df = pd.merge(df1, df2, left_index=True, right_index=True, how='inner')

#     return merged_df, merged_df.isnull().sum()
