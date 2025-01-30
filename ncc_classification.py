import http.client
import urllib.parse
import json


def get_classifications(ncc_location: str, ncc_token: str) -> list:
    """
    This function fetches a list of classifications present in Nextiva Contact Center (NCC).
    """
    classifications = []
    conn = http.client.HTTPSConnection(ncc_location)
    payload = ""
    headers = {"Authorization": ncc_token}
    conn.request("GET", "/data/api/types/classification?q=Test%20", payload, headers)
    res = conn.getresponse()
    if res.status == 200:
        data = res.read().decode("utf-8")
        json_data = json.loads(data)
        total = json_data["total"]
        if total > 0:
            results = json_data["objects"]
            for result in results:
                classification_name = result["name"]
                if classification_name[0:5] == "Test ":
                    classifications.append(result)
    return classifications


def search_classifications(
    ncc_location: str, ncc_token: str, classification_name: str
) -> dict:
    """
    This function searches for an existing classification in Nextiva Contact Center (NCC) with the same name as the intended new classification.
    """
    classification = {}
    conn = http.client.HTTPSConnection(ncc_location)
    payload = ""
    headers = {"Authorization": ncc_token}
    url_encoded_name = urllib.parse.quote(classification_name)
    conn.request(
        "GET",
        f"/data/api/types/classification?q={url_encoded_name}",
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
                if result["name"] == classification_name:
                    classification = result
                    break
    conn.close()
    return classification


def create_classification(
    ncc_location: str,
    ncc_token: str,
    classification_name: str,
    classification_phrases: list,
) -> dict:
    """
    This function creates a classification in Nextiva Contact Center (NCC).
    """
    classification = {}
    conn = http.client.HTTPSConnection(ncc_location)
    payload = json.dumps(
        {
            "data": classification_phrases,
            "localizations": {
                "name": {"en": {"language": "en", "value": classification_name}}
            },
            "name": classification_name,
        }
    )
    headers = {
        "Authorization": ncc_token,
        "Content-Type": "application/json",
    }
    conn.request("POST", "/data/api/types/classification", payload, headers)
    res = conn.getresponse()
    if res.status == 201:
        data = res.read().decode("utf-8")
        classification = json.loads(data)
    return classification


def delete_classification(
    ncc_location: str, ncc_token: str, classification_id: str
) -> bool:
    """
    This function deletes a classification with the specified classification ID.
    """
    success = False
    conn = http.client.HTTPSConnection(ncc_location)
    payload = ""
    headers = {"Authorization": ncc_token}
    conn.request(
        "DELETE",
        f"/data/api/types/classification/{classification_id}",
        payload,
        headers,
    )
    res = conn.getresponse()
    if res.status == 204:
        success = True
    return success
