# TikTok API Test

This repository contains a simple Python script used to test the TikTok
Research Ad Library API. The project was created for a college
assignment to demonstrate how to authenticate with the TikTok API and
retrieve advertisement data using Python.

## Project Overview

The script performs three main tasks:

1.  Authenticates with the TikTok API using OAuth client credentials.
2.  Requests an access token.
3.  Uses the token to query the TikTok Research Ad Library API for
    advertisement data.

The workflow can also be executed through GitHub Actions using stored
repository secrets.

## Project Structure

. ├── tiktok_test.py ├── requirements.txt └── .github └── workflows └──
tiktok-test.yml

-   tiktok_test.py -- Python script that authenticates and queries the
    TikTok API
-   requirements.txt -- Python dependencies required to run the script
-   .github/workflows/tiktok-test.yml -- GitHub Actions workflow used to
    run the test manually

## Requirements

-   Python 3.10 or newer
-   A TikTok Developer account
-   Access to the TikTok Research API
-   A valid client_key and client_secret

Python dependencies:

requests

Install dependencies:

pip install -r requirements.txt

## Configuration

The script reads credentials from environment variables.

Required variables:

TIKTOK_CLIENT_KEY TIKTOK_CLIENT_SECRET

Example:

export TIKTOK_CLIENT_KEY=your_client_key export
TIKTOK_CLIENT_SECRET=your_client_secret

## Running the Script

Run the script locally with:

python tiktok_test.py

The script will:

1.  Request an access token from TikTok.
2.  Use the token to query the Ad Library API.
3.  Print the API response in JSON format.

## Code Explanation

### get_access_token()

This function authenticates with the TikTok OAuth API.

Steps performed: - Sends a POST request to the token endpoint. - Uses
the client_key and client_secret. - Requests a token using the
client_credentials grant type. - Returns the access token used for
future API requests.

### fetch_ads(access_token)

This function queries the TikTok Research Ad Library API.

Steps performed: - Uses the access token for authorization. - Sends a
POST request to the Ad Library query endpoint. - Filters ads based on: -
country - publication date range - Limits the number of results returned
per request.

The function prints the response returned by the API.

### main()

The main function coordinates the script.

Steps performed: 1. Calls get_access_token() to retrieve an access
token. 2. If the token is valid, calls fetch_ads() to query
advertisement data.

## GitHub Actions

The repository includes a GitHub Actions workflow that allows the script
to be executed manually.

The workflow performs the following steps:

1.  Checks out the repository.
2.  Installs Python.
3.  Installs required dependencies.
4.  Reads TikTok API credentials from repository secrets.
5.  Executes the test script.

Required GitHub repository secrets:

TIKTOK_CLIENT_KEY TIKTOK_CLIENT_SECRET
