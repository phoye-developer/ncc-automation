import http.client
import json


def search_campaign_scorecards(
    ncc_location: str, ncc_token: str, campaign_id: str, scorecard_id: str
) -> bool:
    """
    This function searches for a specified scorecard ID in the campaignscorecard objects.
    """
    success = False
    conn = http.client.HTTPSConnection(ncc_location)
    payload = ""
    headers = {"Authorization": ncc_token}
    conn.request(
        "GET",
        f"/data/api/types/campaignscorecard?q={scorecard_id}",
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
                if result["campaignId"] == campaign_id:
                    success = True
                    break
    conn.close()
    return success


def create_campaign_scorecard(
    ncc_location: str, ncc_token: str, campaign_id: str, scorecard_id: str
) -> bool:
    """
    This function assigns a scorecard to a campaign.
    """
    success = False
    conn = http.client.HTTPSConnection(ncc_location)
    payload = json.dumps(
        {
            "campaignId": campaign_id,
            "scorecardId": scorecard_id,
        }
    )
    headers = {
        "Authorization": ncc_token,
        "Content-Type": "application/json",
    }
    conn.request("POST", "/data/api/types/campaignscorecard/", payload, headers)
    res = conn.getresponse()
    if res.status == 201:
        success = True
    return success
