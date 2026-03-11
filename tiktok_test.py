import os
import requests
import json

# TikTok OAuth endpoint
TOKEN_URL = "https://open.tiktokapis.com/v2/oauth/token/"

# Ad Library endpoint with VALID fields
AD_API_URL = (
    "https://open.tiktokapis.com/v2/research/adlib/ad/query/"
    "?fields=ad.id,ad.first_shown_date,ad.last_shown_date,ad.videos,advertiser.business_name"
)

# Load API credentials from environment variables
CLIENT_KEY = os.getenv("TIKTOK_CLIENT_KEY")
CLIENT_SECRET = os.getenv("TIKTOK_CLIENT_SECRET")


def get_access_token():
    """
    Request an access token from TikTok using the client credentials.
    """

    payload = {
        "client_key": CLIENT_KEY,
        "client_secret": CLIENT_SECRET,
        "grant_type": "client_credentials"
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = requests.post(TOKEN_URL, data=payload, headers=headers)

    if response.status_code != 200:
        print("Token request failed")
        print(response.text)
        return None

    token = response.json()["access_token"]
    print("Access token received")

    return token


def fetch_ads(token):
    """
    Query the TikTok Ad Library API.
    """

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    payload = {
        "filters": {
            "ad_published_date_range": {
                "min": "20240101",
                "max": "20251231"
            },
            "country_code": "CA"
        },
        "max_count": 20
    }

    response = requests.post(AD_API_URL, json=payload, headers=headers)

    print("Status Code:", response.status_code)
    print(response.text)

    if response.status_code != 200:
        return None

    return response.json()


def main():

    token = get_access_token()

    if not token:
        return

    data = fetch_ads(token)

    if data:
        print("\nFormatted JSON Output:\n")
        print(json.dumps(data, indent=2))


if __name__ == "__main__":
    main()
