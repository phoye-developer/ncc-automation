import http.client
import json


def search_services(ncc_location: str, ncc_token: str, service_type: str) -> dict:
    """
    This function searches for an existing service with the same type as the intended new service.
    """
    service = {}
    conn = http.client.HTTPSConnection(ncc_location)
    payload = ""
    headers = {"Authorization": ncc_token}
    conn.request(
        "GET",
        "/data/api/types/service",
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
                if result["type"] == service_type:
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


def create_tts_service(
    ncc_location: str, ncc_token: str, ncc_service_name: str
) -> dict:
    """
    This function creates an NCC TEXT_TO_SPEECH service with the specified name.
    """
    service = {}
    conn = http.client.HTTPSConnection(ncc_location)
    payload = json.dumps(
        {
            "localizations": {
                "name": {"en": {"language": "en", "value": ncc_service_name}},
            },
            "type": "TEXT_TO_SPEECH",
            "enabled": True,
            "provider": "GOOGLE",
            "name": ncc_service_name,
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


def create_gen_ai_service(
    ncc_location: str, ncc_token: str, ncc_service_name: str, ncc_project_id: str
) -> dict:
    """
    This function creates an NCC GENERATIVE_AI service with the specified name.
    """
    service = {}
    conn = http.client.HTTPSConnection(ncc_location)
    payload = json.dumps(
        {
            "localizations": {
                "name": {"en": {"language": "en", "value": ncc_service_name}}
            },
            "type": "GENERATIVE_AI",
            "enabled": True,
            "provider": "GOOGLE",
            "name": ncc_service_name,
            "parameters": [
                {"key": "temperature", "value": "0"},
                {"key": "maxOutputTokens", "value": "8192"},
                {"key": "topP", "value": "1.0"},
                {"key": "topK", "value": "40"},
                {
                    "key": "endpoint",
                    "value": "us-central1-aiplatform.googleapis.com:443",
                },
                {"key": "project", "value": ncc_project_id},
                {"key": "location", "value": "us-central1"},
                {"key": "publisher", "value": "google"},
                {"key": "model", "value": "gemini-1.0-pro"},
                {
                    "key": "content",
                    "value": "Your input is the conversation transcript below. The conversation includes a customer and an agent. For this conversation, I'd like you to generate a short, HTML summary that meets the following criteria:  Headline: Briefly capture the essence of the conversation in a single sentence. Sentiment: Identify the overall sentiment of the customer and the agent throughout the conversation. Use separate bullets for each. Bullet Points: Summarize the key points of the conversation using HTML bullet points. The entire summary must be in HTML format. Please do not return the summary in markdown format. An example of the format of the response can be <html><head><title>...</title></head><body><h1>...</h1><h2>Headline:</h2><p>...</p><h2>Sentiment:</h2><ul><li><b>Customer:</b>...</li><li><b>Agent:</b>...</li></ul><h2>Key Points:</h2><ul><li>...</li><li>...</li><li>...</li><li>...</li></ul></body></html>",
                },
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
