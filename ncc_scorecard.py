import http.client
import urllib.parse
import json


def search_scorecards(ncc_location: str, ncc_token: str, scorecard_name: str) -> dict:
    """
    This function searches for an existing scorecard with the same name as the intended new scorecard.
    """
    scorecard = {}
    conn = http.client.HTTPSConnection(ncc_location)
    payload = ""
    headers = {"Authorization": ncc_token}
    url_encoded_name = urllib.parse.quote(scorecard_name)
    try:
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
    except:
        pass
    conn.close()
    return scorecard


def search_campaign_scorecards(
    ncc_location: str, ncc_token: str, campaign_name: str
) -> dict:
    """
    This function searches for existing scorecards in Nextiva Contact Center (NCC) whose name begins with the specified campaign name.
    """
    scorecards = []
    conn = http.client.HTTPSConnection(ncc_location)
    payload = ""
    headers = {"Authorization": ncc_token}
    url_encoded_name = urllib.parse.quote(campaign_name)
    try:
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
                    if str(result["name"]).startswith(campaign_name):
                        scorecards.append(result)
    except:
        pass
    conn.close()
    return scorecards


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
    try:
        conn.request("POST", "/data/api/types/scorecard/", payload, headers)
        res = conn.getresponse()
        if res.status == 201:
            data = res.read().decode("utf-8")
            scorecard = json.loads(data)
    except:
        pass
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
    try:
        conn.request(
            "DELETE", f"/data/api/types/scorecard/{scorecard_id}", payload, headers
        )
        res = conn.getresponse()
        if res.status == 204:
            success = True
    except:
        pass
    conn.close()
    return success
