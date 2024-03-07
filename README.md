# [Guide for SensorAdjust Project ](https://sensor-adjust-project.streamlit.app/ "The SensorAdjust Project website")

**Overview**: SensorAdjust is an open source project that aims to simplify 
the calibration process for users with minimal or no coding expertise. 
By enabling users to directly upload data from both low-cost sensors and reference monitors, or data that has already 
been paired, the platform effortlessly creates a correction factor based on the uploaded data, provided the users follow the specified guidelines. 
This generated correction factor can be applied to the low-cost sensor data to significantly improve its accuracy, thereby democratizing access to high-quality environmental monitoring for everyone.

**Objective**: The primary objective of the SensorAdjust Project is to 
democratize access to accurate environmental data collection. We aim to accomplish this by 
offering a user-friendly platform that 
automates the generation of correction factors for low-cost sensors in 
comparison to reference monitors. This initiative guarantees that all users, 
irrespective of their technical expertise, can effortlessly calibrate their low-cost 
sensor data. By simplifying this process, we ensure that accurate environmental 
monitoring is accessible to everyone, enabling users to trust and utilize their 
data for a wide range of applications with confidence.

### How to Use the SensorAdjust System

In this section, we'll guide you through the essential steps to prepare your data for upload to the SensorAdjust project platform. 
Adhering to these guidelines will guarantee a seamless generation of the correction factor:

1. **Preparing Your Data Timestamp:**
   - Make sure the column containing the timestamps in your dataset is named `DataDate`. This is crucial for the system to correctly recognize and format the Timestamp column.

2. **Cleaning Your Data:**
   - Before uploading, review your dataset to remove any unnecessary columns. This helps in streamlining the process of creating the correction factor and ensures that the system focuses only on relevant data.
   - If you are uploading both reference monitor data and low-cost sensor data separately, the system will automatically modify the column names for clarity:
     - Column names in the reference monitor data, except for the `DataDate` column, will be suffixed with `_Reference`. For example, a column named `PM2.5` will be renamed to `PM2.5_Reference`.
     - Similarly, column names in the low-cost sensor data, excluding the `DataDate` column, will be suffixed with `_LCS` (indicating Low-Cost Sensor). For example, `PM2.5` becomes `PM2.5_LCS`.
   - If your dataset is already paired (meaning each timestamp has corresponding values from both the low-cost sensor and the reference monitor), and you upload this combined data, the platform will not alter the column names. This feature is designed to accommodate users who have pre-processed their data.

Adhering to these preparatory guidelines guarantees that your data is properly formatted and ready for the SensorAdjust platform. This initial preparation is crucial for fully harnessing the platform's potential, facilitating a streamlined and precise generation of correction factor. Consequently, you can apply this correction factor to your low-cost sensor data with confidence, ensuring accuracy and reliability in your environmental monitoring efforts.

[Project URL](https://sensor-adjust-project.streamlit.app/ "The SensorAdjust Project website")
