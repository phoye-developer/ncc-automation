import http.client
import ssl
import urllib.parse
import json


def search_prompts(ncc_location: str, ncc_token: str, prompt_name: str) -> dict:
    """
    This function searches for an existing prompt in Nextiva Contact Center (NCC).
    """
    prompt = {}
    context = ssl._create_unverified_context()
    conn = http.client.HTTPSConnection(ncc_location, context=context)
    payload = ""
    headers = {"Authorization": ncc_token}
    url_encoded_name = urllib.parse.quote(prompt_name)
    try:
        conn.request(
            "GET",
            f"/data/api/types/prompt?q={url_encoded_name}",
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
                    if result["name"] == prompt_name:
                        prompt = result
                        break
    except:
        pass
    conn.close()
    return prompt
