import http.client
import urllib.parse
import json


def search_services(
    ncc_location: str, ncc_token: str, service_name: str, service_type: str
) -> dict:
    """
    This function searches for an existing service with the same name and type as the intended new service.
    """
    service = {}
    conn = http.client.HTTPSConnection(ncc_location)
    payload = ""
    headers = {"Authorization": ncc_token}
    url_encoded_name = urllib.parse.quote(service_name)
    conn.request(
        "GET",
        f"/data/api/types/service?q={url_encoded_name}",
        payload,
        headers,
    )
    res = conn.getresponse()
    if res.status == 200:
        data = res.read().decode("utf-8")
        json_data = json.loads(data)
        total = json_data["total"]
        if total > 0:
            results = json_data["objects"]
            for result in results:
                if result["name"] == service_name and result["type"] == service_type:
                    service = result
                    break
    conn.close()
    return service


def create_real_time_transcription_service(
    ncc_location: str, ncc_token: str, ncc_service_name: str, deepgram_api_key: str
) -> dict:
    """
    This function creates an NCC REALTIME_ANALYSIS service with the specified name.
    """
    service = {}
    conn = http.client.HTTPSConnection(ncc_location)
    payload = json.dumps(
        {
            "apiKey": deepgram_api_key,
            "name": ncc_service_name,
            "localizations": {
                "name": {
                    "en": {
                        "language": "en",
                        "value": ncc_service_name,
                    }
                }
            },
            "type": "REALTIME_ANALYSIS",
            "enabled": True,
            "provider": "DEEPGRAM",
            "parameters": [
                {"key": "model", "value": "nova-2"},
                {"key": "multichannel", "value": "false"},
                {"key": "punctuate", "value": "true"},
                {"key": "smart_format", "value": "true"},
                {"key": "redact", "value": "pci"},
                {"key": "redact", "value": "ssn"},
                {"key": "redact", "value": "pii"},
                {"key": "encoding", "value": "linear16"},
                {"key": "sample_rate", "value": "16000"},
                {"key": "language", "value": "multi"},
            ],
        }
    )
    headers = {
        "Authorization": ncc_token,
        "Content-Type": "application/json",
    }
    conn.request("POST", "/data/api/types/service/", payload, headers)
    res = conn.getresponse()
    if res.status == 201:
        data = res.read().decode("utf-8")
        service = json.loads(data)
    conn.close()
    return service


def delete_service(ncc_location: str, ncc_token: str, service_id: str) -> bool:
    """
    This function deletes a service with the specified service ID.
    """
    success = False
    conn = http.client.HTTPSConnection(ncc_location)
    payload = ""
    headers = {"Authorization": ncc_token}
    conn.request(
        "DELETE",
        f"/data/api/types/service/{service_id}",
        payload,
        headers,
    )
    res = conn.getresponse()
    if res.status == 204:
        success = True
    return success
