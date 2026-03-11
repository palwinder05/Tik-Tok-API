import os
import json
import requests

TOKEN_URL = "https://open.tiktokapis.com/v2/oauth/token/"
AD_API_URL = (
    "https://open.tiktokapis.com/v2/research/adlib/ad/query/"
    "?fields=ad.id,ad.advertiser_name,ad.published_date,ad.videos"
)

CLIENT_KEY = os.getenv("TIKTOK_CLIENT_KEY")
CLIENT_SECRET = os.getenv("TIKTOK_CLIENT_SECRET")


def get_access_token():
    payload = {
        "client_key": CLIENT_KEY,
        "client_secret": CLIENT_SECRET,
        "grant_type": "client_credentials",
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    resp = requests.post(TOKEN_URL, data=payload, headers=headers, timeout=30)

    if resp.status_code != 200:
        print("Token request failed")
        print(resp.text)
        return None

    token = resp.json().get("access_token")
    print("Access token received")
    return token


def fetch_ads(access_token):

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "filters": {
            "ad_published_date_range": {
                "min": "20240101",
                "max": "20260101"
            },
            "country": "CA"
        },
        "max_count": 20
    }

    resp = requests.post(AD_API_URL, json=payload, headers=headers, timeout=30)

    print("Status Code:", resp.status_code)

    if resp.status_code != 200:
        print(resp.text)
        return

    data = resp.json()
    print(json.dumps(data, indent=2))


def main():
    token = get_access_token()

    if not token:
        print("Token generation failed")
        return

    fetch_ads(token)


if __name__ == "__main__":
    main()
