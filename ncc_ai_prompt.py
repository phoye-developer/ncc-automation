import http.client
import urllib.parse
import json


def get_ai_prompts(ncc_location: str, ncc_token: str) -> dict:
    """
    This function fetches a list of AI prompts in Nextiva Contact Center (NCC).
    """
    ai_prompts = []
    conn = http.client.HTTPSConnection(ncc_location)
    payload = ""
    headers = {"Authorization": ncc_token}
    try:
        conn.request(
            "GET",
            f"/data/api/types/aiprompt",
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
                    ai_prompts.append(result)
    except:
        pass
    conn.close()
    return ai_prompts


def search_ai_prompts(ncc_location: str, ncc_token: str, ai_prompt_name: str) -> dict:
    """
    This function searches for an existing AI prompt with the same name as the intended new AI prompt.
    """
    ai_prompt = {}
    conn = http.client.HTTPSConnection(ncc_location)
    payload = ""
    headers = {"Authorization": ncc_token}
    url_encoded_name = urllib.parse.quote(ai_prompt_name)
    try:
        conn.request(
            "GET",
            f"/data/api/types/aiprompt?q={url_encoded_name}",
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
                    if result["name"] == ai_prompt_name:
                        ai_prompt = result
                        break
    except:
        pass
    conn.close()
    return ai_prompt


def create_ai_prompt(ncc_location: str, ncc_token: str, ai_prompt_body: dict) -> dict:
    """
    This function creates a AI prompt with a specified name.
    """
    ai_prompt = {}
    conn = http.client.HTTPSConnection(ncc_location)
    payload = json.dumps(ai_prompt_body)
    headers = {
        "Authorization": ncc_token,
        "Content-Type": "application/json",
    }
    try:
        conn.request("POST", "/data/api/types/aiprompt/", payload, headers)
        res = conn.getresponse()
        if res.status == 201:
            data = res.read().decode("utf-8")
            ai_prompt = json.loads(data)
    except:
        pass
    conn.close()
    return ai_prompt


def delete_ai_prompt(ncc_location: str, ncc_token: str, ai_prompt_id: str) -> bool:
    """
    This function deletes a AI prompt with the specified AI prompt ID.
    """
    success = False
    conn = http.client.HTTPSConnection(ncc_location)
    payload = ""
    headers = {"Authorization": ncc_token}
    try:
        conn.request(
            "DELETE", f"/data/api/types/aiprompt/{ai_prompt_id}", payload, headers
        )
        res = conn.getresponse()
        if res.status == 204:
            success = True
    except:
        pass
    conn.close()
    return success
