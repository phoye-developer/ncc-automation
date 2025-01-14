import http.client
import json


def search_deepgram_api_keys(
    deepgram_project_id: str, deepgram_main_api_key: str, deepgram_api_key_name: str
) -> str:
    """
    This function searches for Deepgram API keys with a specified name.
    """
    deepgram_api_key_id = ""
    conn = http.client.HTTPSConnection("api.deepgram.com")
    payload = ""
    headers = {"Authorization": f"Token {deepgram_main_api_key}"}
    conn.request("GET", f"/v1/projects/{deepgram_project_id}/keys", payload, headers)
    res = conn.getresponse()
    if res.status == 200:
        data = res.read().decode("utf-8")
        json_data = json.loads(data)
        results = json_data["api_keys"]
        for result in results:
            if result["api_key"]["comment"] == deepgram_api_key_name:
                deepgram_api_key_id = result["api_key"]["api_key_id"]
                break
    conn.close()
    return deepgram_api_key_id


def create_deepgram_api_key(
    deepgram_project_id: str, deepgram_main_api_key: str
) -> str:
    """
    This function creates a Deepgram API key to be used for real-time and post-call transcription.
    """
    deepgram_api_key = ""
    conn = http.client.HTTPSConnection("api.deepgram.com")
    payload = json.dumps({"comment": "Test Key", "scopes": ["usage:write"]})
    headers = {
        "Authorization": f"Token {deepgram_main_api_key}",
        "Content-Type": "application/json",
    }
    conn.request(
        "POST",
        f"/v1/projects/{deepgram_project_id}/keys",
        payload,
        headers,
    )
    res = conn.getresponse()
    if res.status == 200:
        data = res.read().decode("utf-8")
        json_data = json.loads(data)
        deepgram_api_key = json_data["key"]
    conn.close()
    return deepgram_api_key


def delete_deepgram_api_key(
    deepgram_project_id: str, deepgram_main_api_key: str, deepgram_api_key_id: str
) -> bool:
    """
    This function deletes the Deepgram API key with the specified API key ID.
    """
    success = False
    conn = http.client.HTTPSConnection("api.deepgram.com")
    payload = ""
    headers = {"Authorization": f"Token {deepgram_main_api_key}"}
    conn.request(
        "DELETE",
        f"/v1/projects/{deepgram_project_id}/keys/{deepgram_api_key_id}",
        payload,
        headers,
    )
    res = conn.getresponse()
    if res.status == 200:
        success = True
    return success
