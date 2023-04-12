# Final-FIM-Project

## FILE INTEGIRTY MONITORING 

# This file integrity monitoring projects covers:
    - Real-time file integrity monitoring
    - Real time logs display on web
    - Log visulalization 
    - Alerting with message though Slack
    
    
# Real-time monitoring
  For this i am using the checksum method where the hash value of the file is being constantly being checked, watchdog is popular for this type of real-time check but instead of using the watchdog which monitors the file in real-time I am checking the hash value every 1 second.
  
 # Real-time log display
  Logs could be accessed through the http://localhost:5000 or http://localhost:5000/data for real time logging there are multiple way it can be achieve, here i ma reading the logs from the log folder and constantly checking for new update. 
  
 # Log visualization
    For log visualization  i have used the python plotly library, simple visualization for the logs has been done with correlation, scatter plot etc.
  
  # Alerting with message   
    For the purpose of real time alerting i have implement the slack api for recieving the real time alert whenever the change happens!!
 

More I am planning to implement a machine learning algorithm for analysis.
