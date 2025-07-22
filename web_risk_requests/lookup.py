# lookup.py
import os
import requests

API_KEY = os.getenv("WEB_RISK_KEY")
THREAT_TYPES = [
    "MALWARE",
    "SOCIAL_ENGINEERING",
    "UNWANTED_SOFTWARE",
    "SOCIAL_ENGINEERING_EXTENDED_COVERAGE",
]

def lookup_uri(uri: str) -> dict:
    if not API_KEY:
        raise RuntimeError("Set WEB_RISK_KEY in your environment.")
    # Build params: repeat threatTypes for each value
    params = [
        ("key", API_KEY),
        ("uri", uri)
    ] + [("threatTypes", t) for t in THREAT_TYPES]

    url = "https://webrisk.googleapis.com/v1/uris:search"

    response = requests.get(url, params=params, timeout=30)
    #print(response.text)
    data = response.json()
    print("data:", data)
    try:
        response.raise_for_status()
    except requests.HTTPError:
        # Log body for easier debugging
        raise RuntimeError(f"Web Risk error {response.status_code}: {response.text}") from None
    result = {}
    threat_info = data.get("threat")
    if threat_info and "threatTypes" in threat_info:
        result["scores"] = [
            {"threatType": t, "confidenceLevel": "HIGH"}
            for t in threat_info["threatTypes"]
        ]
    else:
        result = {
            "scores": [
                {"confidenceLevel": "SAFE", "threatType": t}
                for t in THREAT_TYPES
            ]
        }
    return result
