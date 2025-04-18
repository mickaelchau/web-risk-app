import os
import requests

def evaluate_uri(uri: str) -> dict:
    # 1. grab API key from env
    api_key = os.getenv("WEB_RISK_KEY")
    if not api_key:
        return {"error": "WEB_RISK_KEY environment variable not set"}

    # 2. construct URL with the key
    url = f"https://webrisk.googleapis.com/v1eap1:evaluateUri?key={api_key}"

    payload = {
        "uri": uri,
        "threatTypes": [
            "MALWARE",
            "SOCIAL_ENGINEERING",
            "UNWANTED_SOFTWARE",
        ],
    }

    headers = {
        "Content-Type": "application/json; charset=utf-8",
        # you can also pull your quota project from env if you like:
        "x-goog-user-project": os.getenv("WEB_RISK_QUOTA_PROJECT")
    }

    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        return {"error": f"An error occurred: {e}"}
