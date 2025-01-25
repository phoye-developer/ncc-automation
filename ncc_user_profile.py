import http.client
import json


def search_user_profiles(
    ncc_location: str, ncc_token: str, user_profile_name: str
) -> dict:
    """
    This function searches for an existing user profile with the specified name.
    """
    user_profile = {}
    conn = http.client.HTTPSConnection(ncc_location)
    payload = ""
    headers = {"Authorization": ncc_token}
    conn.request(
        "GET",
        f"/data/api/types/userprofile?q={user_profile_name}",
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
                if result["name"] == user_profile_name:
                    user_profile = result
                    break
    conn.close()
    return user_profile
