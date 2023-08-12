# Final-FIM-Project

## FILE INTEGRITY MONITORING 

# This file integrity monitoring project covers:
    - Real-time file integrity monitoring
    - Real-time logs displayed on the web
    - Log visualization 
    - Alerting with messages through Slack
    
    
# Real-time monitoring
  For this I am using the checksum method where the hash value of the file is constantly being checked, watchdog is popular for this type of real-time check but instead of using the watchdog which monitors the file in real-time, I am checking the hash value every 1 second.
  
 # Real-time log display
  Logs could be accessed through http://localhost:5000 or http://localhost:5000/data for real-time logging there are multiple ways it can be achieved, here I am reading the logs from the log folder and constantly checking for new updates.
  ![image](https://github.com/Nabin0727/Final-FIM-Project/assets/51498755/83f61184-00be-45d3-b0e7-a19342cd1d10)

  
 # Log visualization
    For log visualization  I have used the python plotly library, simple visualization for the logs has been done with correlation, scatter plot, etc.
  ![image](https://github.com/Nabin0727/Final-FIM-Project/assets/51498755/686d9906-2701-44ab-9a67-8583cf0a5fb6)

  # Alerting with message   
    For the purpose of real-time alerting, I have implemented the Slack app for receiving real-time alert whenever a change happens!!
 ![image](https://github.com/Nabin0727/Final-FIM-Project/assets/51498755/396c21cb-ae17-4b0b-b775-8f562108a4e0)


I am planning to implement a machine learning algorithm for analysis.
