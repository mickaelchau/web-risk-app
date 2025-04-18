
import google.cloud.webrisk_v1 as webrisk_v1

def lookup_uri(uri: str) -> dict:
#Example: "http://testsafebrowsing.appspot.com/s/malware.html"
    try:
        webrisk_client = webrisk_v1.WebRiskServiceClient()

        request = webrisk_v1.SearchUrisRequest()
        request.threat_types = [webrisk_v1.ThreatType.MALWARE,
                                 webrisk_v1.ThreatType.SOCIAL_ENGINEERING,
                                 webrisk_v1.ThreatType.UNWANTED_SOFTWARE,
                                 webrisk_v1.ThreatType.SOCIAL_ENGINEERING_EXTENDED_COVERAGE]
        request.uri = uri

        response = webrisk_client.search_uris(request)
        
        result = {}
        if response.threat:
            result['scores'] = [
                {"threatType": threat_type.name, "confidenceLevel": "HIGH"} for threat_type in response.threat.threat_types
            ]
        else:
            result = { 
                "scores": [
                    {
                        "confidenceLevel": "SAFE",
                        "threatType": "SOCIAL_ENGINEERING"
                    },
                    {
                        "confidenceLevel": "SAFE",
                        "threatType": "MALWARE"
                    },
                    {
                        "confidenceLevel": "SAFE",
                        "threatType": "UNWANTED_SOFTWARE"
                    }
                ]
            }
        return result
    except Exception as e:
        return {"error": f"An error occurred: {e}"}