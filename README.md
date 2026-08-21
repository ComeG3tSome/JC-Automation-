# Smartsheet API Folder Monitoring Application

## An automation utility that monitors a local directory to detect new files, extract data from filenames, and send the extracted data directly to a Smartsheet spreadsheet. 

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
self.sheet_id = "your_target_sheet_ID_numbers_" 


# SMARTSHEET_API_REQUESTS.py
api_token = "your_actual_api_token_here"
```

## Usage
1. Configure your Smartsheet API token and Sheet ID.
2. Start the application.
3. Select the folder you want to monitor.
4. Add a new Word document (`.docx`) to the monitored folder.
5. The filename must use an underscore (`_`) to separate the employee's first name from the quote number, and the quote number must begin with `Q`.
6. The application uses everything before the final underscore as the employee's first name and the final portion as the quote number.
7. For example, a file named `John_Q12345.docx` is interpreted as:
   - **First Name:** John
   - **Quote #:** Q12345
8. The extracted first name and quote number are automatically sent to the configured Smartsheet.
9. The `.xlsx` files are detected and reported by the application but they are not used for data extraction.
10. Other file types are reported as invalid.

    
## Dependencies
* tkinter
* requests
* smartsheet-python-sdk
* threading
* os
  
## Licensing
This project is licensed under the [MIT License](https://opensource.org/license/mit).

