import http.client
import json


def search_scorecard_classifications(
    ncc_location: str, ncc_token: str, scorecard_id: str, classification_id: str
) -> bool:
    """
    This function searches for a specified classification ID in the scorecardclassification objects.
    """
    success = False
    conn = http.client.HTTPSConnection(ncc_location)
    payload = ""
    headers = {"Authorization": ncc_token}
    try:
        conn.request(
            "GET",
            f"/data/api/types/scorecardclassification?q={classification_id}",
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
                    if result["scorecardId"] == scorecard_id:
                        success = True
                        break
    except:
        pass
    conn.close()
    return success


def create_scorecard_classification(
    ncc_location: str, ncc_token: str, scorecard_id: str, classification_id: str
) -> bool:
    """
    This function assigns a classification to a scorecard.
    """
    success = False
    conn = http.client.HTTPSConnection(ncc_location)
    payload = json.dumps(
        {
            "scorecardId": scorecard_id,
            "classificationId": classification_id,
        }
    )
    headers = {
        "Authorization": ncc_token,
        "Content-Type": "application/json",
    }
    try:
        conn.request(
            "POST", "/data/api/types/scorecardclassification/", payload, headers
        )
        res = conn.getresponse()
        if res.status == 201:
            success = True
    except:
        pass
    conn.close()
    return success
