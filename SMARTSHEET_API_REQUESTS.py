import requests  # Library for making HTTP requests to interact with APIs

# Your Smartsheet API token
api_token = 'Wc457yhWVgKmFjCHSr4se0yQflI5WpWJUEo2k'

# Set up the headers for the request
headers = {
    "Authorization": f"Bearer {api_token}",  # API token required for authentication.
    "Content-Type": "application/json"  # The content being sent to the server is in JSON format.
}

# URL to the Smartsheet API endpoint
url = 'https://api.smartsheet.com/2.0/sheets'

# Make a GET request to the Smartsheet API to get the list of all sheets
response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:

    # Extract the data portion of the JSON response and assign it to the <<sheets>> variable
    sheets = response.json()['data']

    # Print all sheets and their IDs
    for sheet in sheets:
        print(f"Sheet Name: {sheet['name']}, Sheet ID: {sheet['id']}")
else:
    # Print error message
    print(f"Error: {response.status_code} - {response.text}")