import http.client
import urllib.parse
import json


def search_campaign_dispositions(
    ncc_location: str, ncc_token: str, campaign_id: str, disposition_id: str
) -> bool:
    """
    This function searches for a specified disposition ID in the campaigndispositions objects.
    """
    success = False
    conn = http.client.HTTPSConnection(ncc_location)
    payload = ""
    headers = {"Authorization": ncc_token}
    conn.request(
        "GET",
        f"/data/api/types/campaigndisposition?q={disposition_id}",
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


def create_campaign_disposition(
    ncc_location: str, ncc_token: str, campaign_id: str, disposition_id: str
) -> bool:
    """
    This function assigns a disposition code to a campaign.
    """
    success = False
    conn = http.client.HTTPSConnection(ncc_location)
    payload = json.dumps(
        {
            "campaignId": campaign_id,
            "dispositionId": disposition_id,
        }
    )
    headers = {
        "Authorization": ncc_token,
        "Content-Type": "application/json",
    }
    conn.request("POST", "/data/api/types/campaigndisposition/", payload, headers)
    res = conn.getresponse()
    if res.status == 201:
        success = True
    return success
