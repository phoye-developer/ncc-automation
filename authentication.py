import http.client
import base64
import json


def get_ncc_token(login_site: str, ncc_username: str, ncc_password: str) -> str:
    """
    This function fetches a token from Nextiva Contact Center (NCC).
    """
    json_data = False
    conn = http.client.HTTPSConnection(login_site)
    payload = ""
    string_to_encode = f"{ncc_username}:{ncc_password}"
    encoded_bytes = base64.b64encode(string_to_encode.encode("utf-8"))
    encoded_string = encoded_bytes.decode("utf-8")
    headers = {"Authorization": f"Basic {encoded_string}"}
    try:
        conn.request("GET", "/provider/token-with-authorities", payload, headers)
        res = conn.getresponse()
        if res.status == 200:
            data = res.read().decode("utf-8")
            json_data = json.loads(data)
    except:
        pass
    conn.close()
    return json_data
