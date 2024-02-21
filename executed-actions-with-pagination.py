import json
import requests

from intersight_auth import IntersightAuth

def getActions():
    # Initialize the url with the base endpoint and query parameters
    url = "https://us-east-1.intersight.com/wo/api/v3/markets/Market/actions?limit=50&ascending=true"
    baseurl = url
    
    #Payload for market actions API
    payload = '{"startDate":1579568403,"startTime":1579568403,"endDate":1708459034802,"endTime":1708459034802,"actionStateList":["SUCCEEDED","FAILED"],"environmentType":"HYBRID","detailLevel":"EXECUTION"}'

    # Initialize a variable to store the next page cursor
    next_page = None

    # Loop until there is no next page
    while True:
        # If there is a next page, append the cursor value to the url
        if next_page:
            url = baseurl + "&cursor=" + next_page
        # Make a GET request to the url
        response = requests.request(
            method="POST",
            url=url,
            data=payload,
            auth=AUTH
        )
        # Check if the response was successful
        if response.status_code == 200:
            # Get the value of X-Next-Cursor from the headers
            next_page = response.headers.get("X-Next-Cursor")
            # Get the JSON data from the response
            record = response.json()
            # Loop through the record and print the relevant fields
            for group in record:
                print(group["uuid"],group["target"]["className"],group["target"]["displayName"],group["details"],group["actionID"],group["actionState"],group["userName"])
            # If there is no next page, break the loop
            if not next_page:
                break
        else:
            # Handle the error
            print(f"Request failed with status code {response.status_code}")
            break

#Configure Intersight API token       
AUTH = IntersightAuth(
    secret_key_filename='SecretKey.txt',
    api_key_id='60264b767564612d330b3898/6033d7527564612d316d4b5f/61df14647564612d314a5158'
    )

getActions()