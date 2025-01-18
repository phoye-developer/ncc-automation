import http.client
import json


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
