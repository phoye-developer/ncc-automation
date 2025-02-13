import http.client
import json


def search_supervisor_users(
    ncc_location: str, ncc_token: str, supervisor_id: str, user_id: str
) -> bool:
    """
    This function searches for a specified user ID in the supervisorusers objects.
    """
    success = False
    conn = http.client.HTTPSConnection(ncc_location)
    payload = ""
    headers = {"Authorization": ncc_token}
    try:
        conn.request(
            "GET",
            f"/data/api/types/supervisoruser?q={user_id}",
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
                    if result["supervisorId"] == supervisor_id:
                        success = True
                        break
    except:
        pass
    conn.close()
    return success


def create_supervisor_user(
    ncc_location: str, ncc_token: str, supervisor_id: str, user_id: str
) -> bool:
    """
    This function assigns a supervisor to a user.
    """
    success = False
    conn = http.client.HTTPSConnection(ncc_location)
    payload = json.dumps(
        {
            "supervisorId": supervisor_id,
            "userId": user_id,
        }
    )
    headers = {
        "Authorization": ncc_token,
        "Content-Type": "application/json",
    }
    try:
        conn.request("POST", "/data/api/types/supervisoruser/", payload, headers)
        res = conn.getresponse()
        if res.status == 201:
            success = True
    except:
        pass
    conn.close()
    return success
