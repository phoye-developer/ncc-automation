import http.client
import json


def search_user_profile_dispositions(
    ncc_location: str, ncc_token: str, disposition_id: str, user_profile_id: str
) -> bool:
    """
    This function searches for a specified disposition ID in the userprofiledisposition objects.
    """
    success = False
    conn = http.client.HTTPSConnection(ncc_location)
    payload = ""
    headers = {"Authorization": ncc_token}
    try:
        conn.request(
            "GET",
            f"/data/api/types/userprofiledisposition?q={disposition_id}",
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
                    if result["userprofileId"] == user_profile_id:
                        success = True
                        break
    except:
        pass
    conn.close()
    return success


def create_user_profile_disposition(
    ncc_location: str, ncc_token: str, user_profile_id: str, disposition_id: str
) -> dict:
    """
    This function assigns a user profile to a disposition.
    """
    user_profile_disposition = {}
    conn = http.client.HTTPSConnection(ncc_location)
    payload = json.dumps(
        {
            "userprofileId": user_profile_id,
            "dispositionId": disposition_id,
        }
    )
    headers = {
        "Authorization": ncc_token,
        "Content-Type": "application/json",
    }
    try:
        conn.request(
            "POST", "/data/api/types/userprofiledisposition/", payload, headers
        )
        res = conn.getresponse()
        if res.status == 201:
            data = res.read().decode("utf-8")
            user_profile_disposition = json.loads(data)
    except:
        pass
    conn.close()
    return user_profile_disposition
