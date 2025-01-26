import http.client
import json


def get_pstn_numbers(ncc_location: str, ncc_token: str) -> list:
    """
    This function gets a list of PSTN numbers present on the Nextiva Contact Center (NCC) tenant.
    """
    pstn_numbers = []
    conn = http.client.HTTPSConnection(ncc_location)
    payload = ""
    headers = {"Authorization": ncc_token}
    conn.request("GET", "/data/api/types/pstnnumber", payload, headers)
    res = conn.getresponse()
    if res.status == 200:
        data = res.read().decode("utf-8")
        json_data = json.loads(data)
        total = json_data["total"]
        if total > 0:
            results = json_data["objects"]
            for result in results:
                pstn_numbers.append(result)
    return pstn_numbers
