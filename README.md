# Smartsheet API folder monitoring application

## An automation utility that monitors a local directory to detect new files, extract data from filenames, and send the extracted data directly to a Smartsheet spreadsheet automatically. 

## Features
* **Folder Monitoring:** Tracks a user-selected local directory for newly added files.
* **Data Extraction:** Automatically parses the employee name and quote number from Word document filenames.
* **Instant Smartsheet Updates:** Transmits extracted data directly to your sheet via the Smartsheet API without manual entry.
* **Error Handling:** Validates folder paths and ensures stable API connectivity during data transfer.

## Live Demo
[![Smartsheet API folder monitoring GUI app](https://github.com/ComeG3tSome/JC-Automation-/blob/main/SmartsheetGUIAPP.jpg?raw=true)](https://www.youtube.com/watch?v=O7L47zKL2pU)

## Prerequisites

Before running the application, ensure you have the following: 

* **Python 3.8+** installed in your system.
* A **Smartsheet Access Token** (generated under *Account > Personal Settings > API Access > Generate new access token*).
* The **Sheet ID** of the target Smartsheet spreadsheet.

## Installation

1. Clone this repository to your local machine:
   ```bash
   git clone https://github.com/ComeG3tSome/JC-Automation-
   cd JC-Automation-
   ``` 
2.  Install the necessary Python packages required for the script to execute successfully:
```
pip install smartsheet-python-sdk
pip install requests
```

## Configuration
The application requires your unique Smartsheet access details to push data. Two files are used to include this data, which are the following: FILEMONITORING_GUI.py and SMARTSHEET_API_REQUESTS.py.

```python
# FILEMONITORING_GUI.py
self.api_token = "your_actual_api_token_here"
self.sheet_id = 1234567890123456  # Your target sheet ID numbers


# SMARTSHEET_API_REQUESTS.py
api_token = "your_actual_api_token_here"


```
