#!/usr/bin/env python3

"""
TikTok Research Ad Library API Test Script

This script demonstrates how to authenticate with the TikTok API using
client credentials and retrieve advertisement data from the TikTok
Research Ad Library endpoint.

Workflow of the script:
1. Request an OAuth access token from TikTok.
2. Use the access token to authenticate API requests.
3. Send a query request to the TikTok Ad Library API.
4. Print the API response for inspection.
"""

import os
import json
import requests

# ------------------------------------------------------------------
# API ENDPOINTS
# ------------------------------------------------------------------

# OAuth endpoint used to request an access token
TOKEN_URL = "https://open.tiktokapis.com/v2/oauth/token/"

# TikTok Research Ad Library endpoint
# The 'fields' parameter must be provided in the query string
AD_API_URL = "https://open.tiktokapis.com/v2/research/adlib/ad/query/?fields=ad"

# ------------------------------------------------------------------
# LOAD API CREDENTIALS FROM ENVIRONMENT VARIABLES
# ------------------------------------------------------------------

"""
The API credentials are not stored directly in the script for security reasons.
Instead, they are loaded from environment variables.

When running locally or in GitHub Actions, these variables must be set:

TIKTOK_CLIENT_KEY
TIKTOK_CLIENT_SECRET
"""

CLIENT_KEY = os.getenv("TIKTOK_CLIENT_KEY")
CLIENT_SECRET = os.getenv("TIKTOK_CLIENT_SECRET")


# ------------------------------------------------------------------
# FUNCTION: REQUEST ACCESS TOKEN
# ------------------------------------------------------------------

def get_access_token():
    """
    Requests an OAuth access token from the TikTok API.

    The TikTok API requires authentication before accessing protected
    endpoints. This function sends a POST request to the OAuth token
    endpoint using the client credentials grant type.

    Returns:
        str: Access token if successful
        None: If authentication fails
    """

    payload = {
        "client_key": CLIENT_KEY,
        "client_secret": CLIENT_SECRET,
        "grant_type": "client_credentials",
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    # Send POST request to obtain access token
    response = requests.post(
        TOKEN_URL,
        data=payload,
        headers=headers,
        timeout=30
    )

    # Check if request was successful
    if response.status_code != 200:
        print("Token request failed")
        print(response.text)
        return None

    # Extract token from JSON response
    token = response.json().get("access_token")

    print("Access token received")

    return token


# ------------------------------------------------------------------
# FUNCTION: QUERY TIKTOK AD LIBRARY
# ------------------------------------------------------------------

def fetch_ads(access_token):
    """
    Queries the TikTok Research Ad Library API.

    This function sends a POST request to retrieve advertisement data.
    Filters are applied to limit the results to a specific country
    and date range.

    Parameters:
        access_token (str): OAuth token obtained from TikTok

    Returns:
        dict: JSON response from the API
        None: If the request fails
    """

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    """
    The payload defines filters and request parameters.

    filters:
        Limits results to specific ads.

    ad_published_date_range:
        Filters ads published between two dates.

    country:
        Limits ads to a specific geographic region.

    max_count:
        Limits how many results are returned per request.
        TikTok allows a maximum of 50.
    """

    payload = {
        "filters": {
            "ad_published_date_range": {
                "min": "20251001",
                "max": "20260224"
            },
            "country": "CA"
        },
        "max_count": 20
    }

    # Send POST request to TikTok Ad Library API
    response = requests.post(
        AD_API_URL,
        json=payload,
        headers=headers,
        timeout=30
    )

    # Print status code for debugging
    print("Status Code:", response.status_code)

    # Print raw response text for inspection
    print(response.text)

    # If request failed, return None
    if response.status_code != 200:
        return None

    # Convert API response to JSON
    return response.json()


# ------------------------------------------------------------------
# MAIN PROGRAM EXECUTION
# ------------------------------------------------------------------

def main():
    """
    Main execution function for the script.

    Steps:
    1. Request access token
    2. If successful, query the TikTok Ad Library
    3. Print formatted JSON response
    """

    # Step 1: Authenticate with TikTok
    token = get_access_token()

    if not token:
        print("Token generation failed")
        return

    # Step 2: Query advertisement data
    data = fetch_ads(token)

    # Step 3: Print formatted results
    if data:
        print(json.dumps(data, indent=2))


# Run the script only when executed directly
if __name__ == "__main__":
    main()
