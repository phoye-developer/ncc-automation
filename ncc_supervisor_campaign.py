import http.client
import json


def search_supervisor_campaigns(
    ncc_location: str, ncc_token: str, supervisor_id: str, campaign_id: str
) -> bool:
    """
    This function searches for a specified campaign ID in the supervisorcampaigns objects.
    """
    success = False
    conn = http.client.HTTPSConnection(ncc_location)
    payload = ""
    headers = {"Authorization": ncc_token}
    conn.request(
        "GET",
        f"/data/api/types/supervisorcampaign?q={campaign_id}",
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
                if result["userId"] == supervisor_id:
                    success = True
                    break
    conn.close()
    return success


def create_supervisor_campaign(
    ncc_location: str, ncc_token: str, supervisor_id: str, campaign_id: str
) -> bool:
    """
    This function assigns a supervisor to a campaign.
    """
    success = False
    conn = http.client.HTTPSConnection(ncc_location)
    payload = json.dumps(
        {
            "userId": supervisor_id,
            "campaignId": campaign_id,
        }
    )
    headers = {
        "Authorization": ncc_token,
        "Content-Type": "application/json",
    }
    conn.request("POST", "/data/api/types/supervisorcampaign/", payload, headers)
    res = conn.getresponse()
    if res.status == 201:
        success = True
    return success
