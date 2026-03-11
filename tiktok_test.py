import os
import requests
import json

# ------------------------------------------------------------
# TikTok API Endpoints
# ------------------------------------------------------------

# Endpoint used to request an OAuth access token
TOKEN_URL = "https://open.tiktokapis.com/v2/oauth/token/"

# Endpoint used to query commercial content (sponsored videos)
API_URL = (
    "https://open.tiktokapis.com/v2/research/adlib/commercial_content/query/"
    "?fields=id,create_date,brand_names,creator,videos"
)


# ------------------------------------------------------------
# Read API credentials from environment variables
# (These are stored as GitHub Secrets in your workflow)
# ------------------------------------------------------------

CLIENT_KEY = os.getenv("TIKTOK_CLIENT_KEY")
CLIENT_SECRET = os.getenv("TIKTOK_CLIENT_SECRET")


# ------------------------------------------------------------
# Function: Get Access Token
# ------------------------------------------------------------
# TikTok requires authentication before accessing the API.
# This function sends the client key and secret to TikTok
# and receives an access token in return.
# ------------------------------------------------------------

def get_access_token():

    payload = {
        "client_key": CLIENT_KEY,
        "client_secret": CLIENT_SECRET,
        "grant_type": "client_credentials"
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = requests.post(TOKEN_URL, data=payload, headers=headers)

    # If authentication fails, print the error
    if response.status_code != 200:
        print("Failed to retrieve access token")
        print(response.text)
        return None

    # Extract the access token from the JSON response
    token = response.json()["access_token"]

    print("Access token received")

    return token


# ------------------------------------------------------------
# Function: Query TikTok Commercial Content
# ------------------------------------------------------------
# This function sends a request to TikTok's research API
# to retrieve sponsored or branded TikTok videos.
# ------------------------------------------------------------

def fetch_content(token):

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # Filters help narrow down the search results
    payload = {
        "filters": {
            "content_published_date_range": {
                "min": "20240101",
                "max": "20241231"
            },

            # Country code of creators (ISO country code)
            "creator_country_code": "FR"
        },

        # Maximum number of results returned per request
        "max_count": 10
    }

    response = requests.post(API_URL, json=payload, headers=headers)

    print("Status Code:", response.status_code)

    if response.status_code != 200:
        print("API request failed")
        print(response.text)
        return None

    return response.json()


# ------------------------------------------------------------
# Function: Display Results
# ------------------------------------------------------------
# This function reads the API response and prints a simple
# summary of the videos returned by the TikTok API.
# ------------------------------------------------------------

def display_results(data):

    contents = data["data"]["commercial_contents"]

    print("\nTikTok Commercial Content Results\n")

    for item in contents:

        creator = item["creator"]["username"]
        date = item["create_date"]

        # Some videos may not contain brand names
        brand = "None"
        if item["brand_names"]:
            brand = item["brand_names"][0]

        # Each result includes a list of video objects
        video_url = item["videos"][0]["url"]

        print("Creator:", creator)
        print("Date:", date)
        print("Brand:", brand)
        print("Video URL:", video_url)
        print("-" * 40)


# ------------------------------------------------------------
# Main Program
# ------------------------------------------------------------
# This is the entry point of the script.
# It runs the authentication and API request functions.
# ------------------------------------------------------------

def main():

    # Step 1: Authenticate and obtain access token
    token = get_access_token()

    if not token:
        return

    # Step 2: Query TikTok API
    data = fetch_content(token)

    if not data:
        return

    # Step 3: Display formatted results
    display_results(data)


# Run the script
if __name__ == "__main__":
    main()
