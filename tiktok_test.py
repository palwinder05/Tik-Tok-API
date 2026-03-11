#!/usr/bin/env python3

"""
Simple TikTok API Test Script

This script demonstrates a basic workflow for interacting with the
TikTok Research Ad Library API.

Steps performed:
1. Request an access token from TikTok using client credentials.
2. Use the access token to send a request to the Ad Library API.
3. Print the response returned by the API.

The goal of this script is only to test the API and inspect the data.
"""

import os
import json
import requests


# -----------------------------------------------------------
# STEP 1: DEFINE API ENDPOINTS
# -----------------------------------------------------------

# Endpoint used to request an OAuth access token
TOKEN_URL = "https://open.tiktokapis.com/v2/oauth/token/"

# Endpoint used to query the TikTok Research Ad Library
# The 'fields' parameter tells the API what information we want returned
AD_API_URL = "https://open.tiktokapis.com/v2/research/adlib/ad/query/?fields=ad"


# -----------------------------------------------------------
# STEP 2: READ API CREDENTIALS FROM ENVIRONMENT VARIABLES
# -----------------------------------------------------------

"""
For security reasons, the client key and secret are not stored
directly inside the script.

Instead, they are read from environment variables.

Required variables:
TIKTOK_CLIENT_KEY
TIKTOK_CLIENT_SECRET
"""

CLIENT_KEY = os.getenv("TIKTOK_CLIENT_KEY")
CLIENT_SECRET = os.getenv("TIKTOK_CLIENT_SECRET")


# -----------------------------------------------------------
# STEP 3: FUNCTION TO GET ACCESS TOKEN
# -----------------------------------------------------------

def get_access_token():
    """
    This function sends a request to TikTok's OAuth API to obtain
    an access token.

    The token is required to authenticate all future API requests.
    """

    # Data sent to TikTok to request the token
    payload = {
        "client_key": CLIENT_KEY,
        "client_secret": CLIENT_SECRET,
        "grant_type": "client_credentials"
    }

    # Required request header
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    # Send POST request to TikTok
    response = requests.post(TOKEN_URL, data=payload, headers=headers)

    # Print error if authentication fails
    if response.status_code != 200:
        print("Token request failed")
        print(response.text)
        return None

    # Extract token from JSON response
    token = response.json()["access_token"]

    print("Access token received")

    return token


# -----------------------------------------------------------
# STEP 4: FUNCTION TO REQUEST AD DATA
# -----------------------------------------------------------

def fetch_ads(token):
    """
    This function queries the TikTok Ad Library API.

    The access token is passed in the request header
    to prove the request is authenticated.
    """

    # Authorization header containing the access token
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # Filters help limit which ads are returned
    payload = {
        "filters": {
            "ad_published_date_range": {
                "min": "20240101",
                "max": "20251231"
            },
            "country": "CA"
        },

        # Limits how many ads are returned in a single request
        "max_count": 20
    }

    # Send request to the TikTok Ad Library API
    response = requests.post(AD_API_URL, json=payload, headers=headers)

    # Print HTTP status code
    print("Status Code:", response.status_code)

    # Print the raw API response for debugging
    print(response.text)

    # Stop if the request failed
    if response.status_code != 200:
        return None

    # Convert response into JSON format
    return response.json()


# -----------------------------------------------------------
# STEP 5: MAIN PROGRAM
# -----------------------------------------------------------

def main():
    """
    Main program execution.

    The program:
    1. Gets an access token
    2. Uses the token to query ad data
    3. Prints the results
    """

    # Request authentication token
    token = get_access_token()

    if token is None:
        print("Authentication failed")
        return

    # Request advertisement data
    data = fetch_ads(token)

    if data:
        print("\nFormatted API Response:\n")
        print(json.dumps(data, indent=2))


# Run the program
if __name__ == "__main__":
    main()
