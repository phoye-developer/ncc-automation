import http.client
import json


def search_campaign_templates(
    ncc_location: str, ncc_token: str, campaign_id: str, template_id: str
) -> bool:
    """
    This function searches for a specified template ID in the campaigntemplate objects.
    """
    success = False
    conn = http.client.HTTPSConnection(ncc_location)
    payload = ""
    headers = {"Authorization": ncc_token}
    try:
        conn.request(
            "GET",
            f"/data/api/types/campaigntemplate?q={template_id}",
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
    except:
        pass
    conn.close()
    return success


def create_campaign_template(
    ncc_location: str, ncc_token: str, campaign_id: str, template_id: str
) -> bool:
    """
    This function assigns a template to a campaign.
    """
    success = False
    conn = http.client.HTTPSConnection(ncc_location)
    payload = json.dumps(
        {
            "campaignId": campaign_id,
            "templateId": template_id,
        }
    )
    headers = {
        "Authorization": ncc_token,
        "Content-Type": "application/json",
    }
    try:
        conn.request("POST", "/data/api/types/campaigntemplate/", payload, headers)
        res = conn.getresponse()
        if res.status == 201:
            success = True
    except:
        pass
    conn.close()
    return success
