import http.client
import base64
import json


def get_ncc_token(ncc_username: str, ncc_password: str) -> str:
    """
    This function fetches a token from Nextiva Contact Center (NCC).
    """
    json_data = False
    conn = http.client.HTTPSConnection("login.thrio.com")
    payload = ""
    string_to_encode = f"{ncc_username}:{ncc_password}"
    encoded_bytes = base64.b64encode(string_to_encode.encode("utf-8"))
    encoded_string = encoded_bytes.decode("utf-8")
    headers = {"Authorization": f"Basic {encoded_string}"}
    conn.request("GET", "/provider/token-with-authorities", payload, headers)
    res = conn.getresponse()
    if res.status == 200:
        data = res.read().decode("utf-8")
        json_data = json.loads(data)
    conn.close()
    return json_data
