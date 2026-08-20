import os  # Operating system functions for file operations
from os import path  # Path-related functions for file system operations
import time  # Time-related functions for timing operations
import tkinter as tk  # Tkinter package for GUI components
from tkinter import messagebox, filedialog  # Specific components from Tkinter for dialogs
import threading  # Threading module for managing concurrent operations
import smartsheet  # Package for interacting with Smartsheet API
import requests  # Library for making HTTP requests to interact with APIs

class FileMonitorApp:

    # FileMonitorApp constructor - It sets up the window with all the widgets
    def __init__(self, root):
        self.root = root

        # Set the title of the main window
        self.root.title("Folder Monitoring")

        # Variables - Attributes of the FileMonitorApp class
        self.folder_path = tk.StringVar()  # Stores the folder path entered by the user
        self.is_monitoring = False  # Tracks if folder monitoring is active
        self.files = set()  # Set to store current files in the monitored folder
        self.monitor_thread = None  # Thread for monitoring the folder.

        # Initialize Smartsheet client and set sheet ID
        self.api_token = 'Wc457yhWVgKmFjCHSr4se0yQflI5WpWJUEo2k'  # Replace with your actual Smartsheet API
        self.sheet_id = 8828162142064516  # The sheet ID

        # Create and pack GUI elements: Label, Entry, Buttons, and Text widget
        label = tk.Label(root, text="Enter Folder Path:")
        label.pack(pady=10)

        self.folder_entry = tk.Entry(root, textvariable=self.folder_path, width=50)
        self.folder_entry.pack(padx=20, pady=5)

        self.start_button = tk.Button(root, text="Start Monitoring", command=self.start_monitoring)
        self.start_button.pack(pady=10)

        self.stop_button = tk.Button(root, text="Stop Monitoring", command=self.stop_monitoring, state=tk.DISABLED)
        self.stop_button.pack(pady=5)

        self.change_button = tk.Button(root, text="Change Folder Path", command=self.change_folder_path)
        self.change_button.pack(pady=5)

        self.output_text = tk.Text(root, height=10, width=50)
        self.output_text.pack(padx=20, pady=10)

        self.columns = self.get_sheet_columns()  # Get the column IDs

    # This method has the functionality of the "Start Monitoring" button
    def start_monitoring(self):

        # If the app is already monitoring, and you click the "Start Monitoring" button again...
        if self.is_monitoring:
            messagebox.showinfo("Already Monitoring", "Monitoring is already in progress.")
            return

        # The folder_path variable gets assigned to the value that the user has entered on the Entry widget.
        folder_path = self.folder_path.get().strip()

        # It checks if the folder path is valid; display an error message if not.
        if not path.isdir(folder_path):
            messagebox.showerror("Invalid Folder Path", "Please enter a valid folder path.")
            return

        # Set to True, to start the monitoring thread
        self.is_monitoring = True

        # The files attribute will be assigned a set of unique files and directories found in the entered folder path.
        self.files = set(os.listdir(folder_path))

        # Create and start a separate thread to run the monitor_folder() method concurrently with the main program
        self.monitor_thread = threading.Thread(target=self.monitor_folder, args=(folder_path,))

        # Start the execution of the thread.
        self.monitor_thread.start()

        # This will update the content of the Text widget
        self.update_output("Monitoring started for folder: " + folder_path)

        # It ensures that the window remains in front of other windows during monitoring process unless you minimize it.
        self.root.wm_attributes('-topmost', 1)

        # Enable stop button
        self.stop_button.config(state=tk.NORMAL)

    # This method has the functionality of the "Stop Monitoring" button
    def stop_monitoring(self):

        # Ensure that monitoring is active before stopping it.
        if not self.is_monitoring:
            messagebox.showinfo("Not Monitoring", "Monitoring is not active.")
            return

        # Set is_monitoring to False so the loop in the separate thread terminates after the current iteration.
        self.is_monitoring = False

        # The main program flow will wait for the separate thread to complete execution of the loop iteration.
        self.monitor_thread.join()

        # After the thread has completed its execution, reset monitor_thread to None.
        self.monitor_thread = None

        # Update the Text widget to indicate monitoring has stopped.
        self.update_output("Monitoring stopped.")

        # Allow other windows to come in front of the main GUI window.
        self.root.wm_attributes('-topmost', 0)

        # Disable the stop button
        self.stop_button.config(state=tk.DISABLED)

    # This method has the functionality of the "Change Folder Path" button
    def change_folder_path(self):

        # Open a dialog box for the user to select a new folder path.
        new_path = filedialog.askdirectory()

        # If a new path has been selected, update the Text widget.
        if new_path:

            # Update the folder_path attribute with the new path.
            self.folder_path.set(new_path)

            # Display the updated folder path in the Text widget.
            self.update_output("Folder path changed to: " + new_path)

    # This method contains statements that execute independently of the main program flow to monitor the folder.
    def monitor_folder(self, folder_path):

        # Continuously monitor the folder until the user stops the monitoring.
        while self.is_monitoring:

            # Determine new files by comparing current folder contents with previously tracked files
            new_files = set(os.listdir(folder_path)) - self.files

            # Check if there is a new file
            if new_files:

                # Iterate over each new file detected in the folder
                for file_name in new_files:

                    # Check if the file is a Word document (.docx)
                    if file_name.endswith('.docx'):

                        # Split the file name into parts based on underscores
                        parts = file_name.split('_')

                        # Check if the last part starts with 'Q'
                        if parts[-1].startswith('Q'):

                            # Join all parts except the last one to form the employee name
                            name = '_'.join(parts[:-1])

                            # Remove file extension to get the quote number
                            quote_number = parts[-1].split('.')[0]

                            # Output indicating a new .docx file with employee name and quote number
                            self.update_output(f"New file with the .docx extension added: {file_name} (Employee Name: {name}, Quote #: {quote_number})")
                            self.add_to_smartsheet(name, quote_number, file_name)

                        else:
                            # Output indicating a new .docx file added without specific employee details
                            self.update_output(f"New .docx file added: {file_name}")

                    # Check if the file is an Excel document (.xlsx)
                    elif file_name.endswith('.xlsx'):
                        # Output indicating a new .xlsx file added
                        self.update_output(f"New .xlsx file added: {file_name}")

                    else:
                        # Output indicating an invalid file added (not .docx or .xlsx)
                        self.update_output(f"Invalid file added: {file_name}")

                # Insert the new file(s) into the files attribute
                self.files.update(new_files)

            # Wait for 2 seconds before checking again to conserve resources.
            time.sleep(2)

    # Function for retrieving the Smartsheet columns
    def get_sheet_columns(self):

        # URL for the Smartsheet API endpoint to get details about a specific sheet
        url = f"https://api.smartsheet.com/2.0/sheets/{self.sheet_id}"

        # Set up the headers for the HTTP requests, including the authorization token and the content type.
        headers = {
            "Authorization": f"Bearer {self.api_token}",  # API token required for authentication.
            "Content-Type": "application/json"  # The content being sent to the server is in JSON format.
        }

        # Make a GET request to retrieve data from the Smartsheet API
        response = requests.get(url, headers=headers)

        # Check if the response was successful
        if response.status_code == 200:

            # Convert the response data into a Python dictionary
            sheet_data = response.json()

            # Extract the list of columns fom the returned JSON response.
            columns = sheet_data['columns']

            # Return a dictionary that maps column titles to their respective IDs.
            return {column['title']: column['id'] for column in columns}
        else:

            # Output indicating an error in fetching columns.
            self.update_output(f"Error fetching columns: {response.status_code} - {response.text}")

            # Return an empty dictionary
            return {}

    # Functionality for adding the data to Smartsheet
    def add_to_smartsheet(self, employee_name, quote_number, file_name):
        # Specify the Smartsheet API endpoint to add rows to the Smartsheet
        url = f"https://api.smartsheet.com/2.0/sheets/{self.sheet_id}/rows"

        # Set up the headers for the HTTP requests, including the authorization token and the content type.
        headers = {
            "Authorization": f"Bearer {self.api_token}",  # API token required for authentication with the Smartsheet API.
            "Content-Type": "application/json"  # The content being sent to the server is in JSON format.
        }

        # Ensure the column names match exactly with the column titles in Smartsheet
        employee_column_id = self.columns.get('Employee Name')
        quote_column_id = self.columns.get('Quote #')

        # Check if column IDs are correctly fetched
        if not employee_column_id or not quote_column_id:
            self.update_output(f"Error: Column IDs not found for 'Employee Name' or 'Quote #'")
            return

        # Create the structure and the content that you want to send to Smartsheet.
        data = {
            # Indicate that the new row should be added to the bottom of the sheet.
            "toTop": True,

            # Create a list with dictionaries that represent cells to be added in the new row.
            "cells": [
                # Each dictionary specifies a column and the value to be inserted into it.
                {"columnId": self.columns.get('Quote #'), "value": quote_number},
                {"columnId": self.columns.get('Employee Name'), "value": employee_name}
            ]
        }

        payload = {
            "toTop": data["toTop"],
            "rows": [{
                "cells": data["cells"]
            }]
        }

        # Send the data dictionary for adding the rows to a sheet
        response = requests.post(url, headers=headers, json=data)

        # Check if the POST request was successful
        if response.status_code == 200:
            # Output indicating that the POST request was successful
            self.update_output(f"Successfully added {file_name} to Smartsheet.")
        else:
            # Output indicating an error in sending the data to Smartsheet
            self.update_output(f"Error adding to Smartsheet: {response.status_code} - {response.text}")

    # Method for updating the Text widget (output_text)
    def update_output(self, message):
        self.output_text.insert(tk.END, message + "\n")
        self.output_text.see(tk.END)

# Create the main Tkinter window
root = tk.Tk()

# Create an instance of the FileMonitorApp class with the Tkinter root window
app = FileMonitorApp(root)

# Run the Tkinter main loop to keep the window open
root.mainloop()
