from flask import Flask, render_template
import os
import json
from flask import jsonify
import plotly.graph_objs as go
import plotly.io as pio
import pandas as pd
import requests
from datetime import datetime, timedelta


app = Flask(__name__)

log_directory = os.path.join(os.path.expanduser("~"), "Desktop", "Project", "Final_FIM", "Logs", "ASUS")
log_contents = []
last_modified = 0

def read_log_files():
    global log_contents
    log_contents = []  # clear the list of logs to prevent duplicates

    log_files = os.listdir(log_directory)

    for log_file in log_files:
        with open(os.path.join(log_directory, log_file), 'r') as f:
            # read the contents of the log file
            log_lines = f.readlines()

        # parse the log file and create a list of log dictionaries
        for line in log_lines:
            log_parts = line.strip().split(" - ")
            # Extracting the timestamp, device name, log level log message and file name
            timestamp = log_parts[0]
            device_name = log_parts[1]
            #log_module = log_parts[2].strip()
            log_level = log_parts[3].strip()
            file_name_path = log_parts[4].strip()

            # Extracting the file name only from the file_name
            file_name = os.path.basename(file_name_path)

            # Extracting the message only
            index_of_c = file_name_path.find("C")
            if index_of_c != -1:
                log_message = file_name_path[:index_of_c]
            else:
                log_message = file_name_path

            # Check if the log already exists in the list
            log_exists = any(log["timestamp"] == timestamp and log["device_name"] == device_name and log["log_level"] == log_level and log["log_message"] == log_message for log in log_contents)
            if not log_exists:
                log_contents.append({
                    "timestamp": timestamp,
                    "device_name": device_name,
                    "log_level": log_level,
                    "log_message": log_message,
                    "file_name": file_name
                })

    log_contents.reverse() # Reverse the list so that the latest log entries appear first

# Checking for update
@app.before_request
def check_log_files():
    global last_modified
    modified_time = os.path.getmtime(log_directory)
    if modified_time > last_modified:
        last_modified = modified_time
        read_log_files()

# Index route that displays the logs
@app.route("/")
def display():
    read_log_files()
    # Render the HTML template and pass the log contents to it
    return render_template('index.html', log_contents=log_contents)

@app.route('/data')
def get_data():
    # code to retrieve data and return it as JSON
    return jsonify(log_contents)

@app.route('/visualize')
def log_counts():
   url = "http://127.0.0.1:5000/data"
   # Send request to API
   response = requests.get(url)

   # Extract JSON string from response
   log_data = response.json()

   # convert log data to pandas DataFrame
   df = pd.DataFrame.from_dict(log_data)

   def data_corelation(df):
       # convert timestamp string to datetime object
       df['time'] = pd.to_datetime(df['timestamp'])

       # set the time column as the DataFrame index
       df.set_index('time', inplace=True)

       # group the DataFrame by time intervals
       interval_minutes = 5
       interval_str = f'{interval_minutes}T'  # '5T' for 5-minute intervals
       grouped = df.groupby(pd.Grouper(freq=interval_str))

        # calculate statistics for each time interval
       stats = grouped.agg({'log_level': 'count',
                            'log_message': lambda x: '; '.join(x),
                            'file_name': lambda x: '; '.join(x)})

        # calculate rolling statistics
       rolling_window_minutes = 15
       rolling_window = rolling_window_minutes * interval_minutes
       rolling_stats = stats.rolling(f'{rolling_window}T').agg({'log_level': 'sum'})

        # create a line plot of log count over time
       fig_core = go.Figure(data=go.Scatter(x=stats.index, y=stats['log_level'], name='Log Count'))

        # create a line plot of rolling log count over time
       fig_core.add_trace(go.Scatter(x=rolling_stats.index, y=rolling_stats['log_level'], name=f'Rolling Log Count ({rolling_window_minutes} min)'))

        # update the layout
       fig_core.update_layout(title='Log Counts over Time', xaxis_title='Time', yaxis_title='Log Count')

        # convert the figure to HTML
       return pio.to_html(fig_core, full_html=False)
       
   def data_plot_new(df):
       # group the DataFrame by file name
       grouped = df.groupby('file_name')

       # calculate statistics for each file name
       stats = grouped.agg({'log_level': 'count',
                        'log_message': lambda x: '; '.join(x)})

       # sort the statistics by log count
       stats.sort_values('log_level', ascending=False, inplace=True)

        # create a horizontal bar chart of log count by file name
       fig = go.Figure(data=go.Bar(x=stats['log_level'], y=stats.index, orientation='h'))

       # update the layout
       fig.update_layout(title='Log Counts by File Name', xaxis_title='Log Count', yaxis_title='File Name')

       # convert the figure to HTML
       return pio.to_html(fig, full_html=False)

   def data_plot(df):               
            # create a count plot by filename
            filename_counts = df['file_name'].value_counts()
            filename_bar = go.Bar(x=filename_counts.index, y=filename_counts.values, name='Filename')

            # create a count plot by log level
            log_level_counts = df['log_level'].value_counts()
            log_level_bar = go.Bar(x=log_level_counts.index, y=log_level_counts.values, name='Log Level')

            # create a count plot by log message
            log_message_counts = df['log_message'].value_counts()
            log_message_bar = go.Bar(x=log_message_counts.index, y=log_message_counts.values, name='Log Message')

            # create a plotly figure
            fig_data_visu = go.Figure(data=[filename_bar, log_level_bar, log_message_bar])

            # update the layout
            fig_data_visu.update_layout(title='Log Counts', xaxis_title='Log Category', yaxis_title='Count')
            
            # convert the figure to HTML
            return pio.to_html(fig_data_visu, full_html=False)
   
   def data_scat(df):
       # create a scatter plot of time vs log level
       fig_data_sca = go.Figure(data=go.Scatter(x=df['timestamp'], y=df['log_level'], mode='markers'))

       # update the layout
       fig_data_sca.update_layout(title='Time vs Log Level', xaxis_title='Time', yaxis_title='Log Level')
        
       # convert the figure to HTML
       return pio.to_html(fig_data_sca, full_html=False)
   
   plot_html_core = data_corelation(df)
   plot_html_plot = data_plot_new(df)
   plot_html = data_plot(df)
   plot_html_scatter = data_scat(df)
   
   # render the HTML page with the plot
   return render_template('visualize.html', plot_html=plot_html, 
                          plot_html_scatter=plot_html_scatter, 
                          plot_html_core=plot_html_core, 
                          plot_html_plot=plot_html_plot)

if __name__ == "__main__":
    read_log_files()  # Read the log files when the server starts
    last_modified = os.path.getmtime(log_directory)
    app.run(debug=True)  # Start the Flask app
