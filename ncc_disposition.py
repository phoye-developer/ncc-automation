import http.client
import urllib.parse
import json


def get_dispositions(ncc_location: str, ncc_token: str) -> list:
    """
    This function fetches a list of dispositions present on the Nextiva Contact Center tenant.
    """
    dispositions = []
    conn = http.client.HTTPSConnection(ncc_location)
    payload = ""
    headers = {"Authorization": ncc_token}
    conn.request("GET", "/data/api/types/disposition?q=Test%20", payload, headers)
    res = conn.getresponse()
    if res.status == 200:
        data = res.read().decode("utf-8")
        json_data = json.loads(data)
        total = json_data["total"]
        if total > 0:
            results = json_data["objects"]
            for result in results:
                disposition_name = result["name"]
                if disposition_name[0:5] == "Test ":
                    dispositions.append(result)
    return dispositions


def search_dispositions(
    ncc_location: str, ncc_token: str, disposition_name: str
) -> dict:
    """
    This function searches for an existing disposition with the same name as the intended new disposition.
    """
    disposition = {}
    conn = http.client.HTTPSConnection(ncc_location)
    payload = ""
    headers = {"Authorization": ncc_token}
    url_encoded_name = urllib.parse.quote(disposition_name)
    conn.request(
        "GET",
        f"/data/api/types/disposition?q={url_encoded_name}",
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
                if result["name"] == disposition_name:
                    disposition = result
                    break
    conn.close()
    return disposition


def create_disposition(
    ncc_location: str, ncc_token: str, disposition_name: str
) -> dict:
    """
    This function creates a disposition with a specified name.
    """
    disposition_id = ""
    conn = http.client.HTTPSConnection(ncc_location)
    payload = json.dumps(
        {
            "name": disposition_name,
            "useCampaignIdForDNC": False,
            "resolved": False,
            "localizations": {
                "name": {
                    "en": {
                        "language": "en",
                        "value": disposition_name,
                    }
                }
            },
            "forceSurveyValidation": False,
            "forceContactAssignment": False,
            "blockNumber": False,
            "connectAgain": False,
        }
    )
    headers = {
        "Authorization": ncc_token,
        "Content-Type": "application/json",
    }
    conn.request("POST", "/data/api/types/disposition/", payload, headers)
    res = conn.getresponse()
    if res.status == 201:
        data = res.read().decode("utf-8")
        disposition = json.loads(data)
    conn.close()
    return disposition


def assign_rest_call_to_dispositon(
    ncc_location: str, ncc_token: str, rest_call_id: str, disposition_id: str
) -> bool:
    success = False
    conn = http.client.HTTPSConnection(ncc_location)
    payload = json.dumps({"restcallId": rest_call_id})
    headers = {"Authorization": ncc_token, "Content-Type": "application/json"}
    conn.request(
        "PATCH", f"/data/api/types/disposition/{disposition_id}", payload, headers
    )
    res = conn.getresponse()
    if res.status == 200:
        success = True
    conn.close()
    return success


def delete_disposition(ncc_location: str, ncc_token: str, disposition_id: str) -> bool:
    """
    This function deletes a disposition with the specified disposition ID.
    """
    success = False
    conn = http.client.HTTPSConnection(ncc_location)
    payload = ""
    headers = {"Authorization": ncc_token}
    conn.request(
        "DELETE", f"/data/api/types/disposition/{disposition_id}", payload, headers
    )
    res = conn.getresponse()
    if res.status == 204:
        success = True
    return success
