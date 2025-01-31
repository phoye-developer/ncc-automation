import http.client
import urllib.parse
import json


def get_scorecards(ncc_location: str, ncc_token: str) -> list:
    """
    This function fetches a list of scorecards present on the Nextiva Contact Center tenant.
    """
    scorecards = []
    conn = http.client.HTTPSConnection(ncc_location)
    payload = ""
    headers = {"Authorization": ncc_token}
    conn.request("GET", "/data/api/types/scorecard?q=Test%20", payload, headers)
    res = conn.getresponse()
    if res.status == 200:
        data = res.read().decode("utf-8")
        json_data = json.loads(data)
        total = json_data["total"]
        if total > 0:
            results = json_data["objects"]
            for result in results:
                scorecard_name = result["name"]
                if scorecard_name[0:5] == "Test ":
                    scorecards.append(result)
    return scorecards


def search_scorecards(ncc_location: str, ncc_token: str, scorecard_name: str) -> dict:
    """
    This function searches for an existing scorecard with the same name as the intended new scorecard.
    """
    scorecard = {}
    conn = http.client.HTTPSConnection(ncc_location)
    payload = ""
    headers = {"Authorization": ncc_token}
    url_encoded_name = urllib.parse.quote(scorecard_name)
    conn.request(
        "GET",
        f"/data/api/types/scorecard?q={url_encoded_name}",
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
                if result["name"] == scorecard_name:
                    scorecard = result
                    break
    conn.close()
    return scorecard


def create_scorecard(ncc_location: str, ncc_token: str, scorecard_name: str) -> dict:
    """
    This function creates a scorecard with a specified name.
    """
    scorecard = {}
    conn = http.client.HTTPSConnection(ncc_location)
    payload = json.dumps(
        {
            "localizations": {
                "name": {"en": {"language": "en", "value": scorecard_name}}
            },
            "name": scorecard_name,
        }
    )
    headers = {
        "Authorization": ncc_token,
        "Content-Type": "application/json",
    }
    conn.request("POST", "/data/api/types/scorecard/", payload, headers)
    res = conn.getresponse()
    if res.status == 201:
        data = res.read().decode("utf-8")
        scorecard = json.loads(data)
    conn.close()
    return scorecard


def delete_scorecard(ncc_location: str, ncc_token: str, scorecard_id: str) -> bool:
    """
    This function deletes a scorecard with the specified scorecard ID.
    """
    success = False
    conn = http.client.HTTPSConnection(ncc_location)
    payload = ""
    headers = {"Authorization": ncc_token}
    conn.request(
        "DELETE", f"/data/api/types/scorecard/{scorecard_id}", payload, headers
    )
    res = conn.getresponse()
    if res.status == 204:
        success = True
    return success
