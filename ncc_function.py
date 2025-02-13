import http.client
import urllib.parse
import json
from config import *


def get_functions(ncc_location: str, ncc_token: str) -> list:
    """
    This function fetches a list of NCC functions present on the Nextiva Contact Center tenant.
    """
    functions = []
    conn = http.client.HTTPSConnection(ncc_location)
    payload = ""
    headers = {"Authorization": ncc_token}
    try:
        conn.request("GET", "/data/api/types/function?q=Test%20", payload, headers)
        res = conn.getresponse()
        if res.status == 200:
            data = res.read().decode("utf-8")
            json_data = json.loads(data)
            total = json_data["total"]
            if total > 0:
                results = json_data["objects"]
                for result in results:
                    function_name = result["name"]
                    if function_name[0:5] == "Test ":
                        functions.append(result)
    except:
        pass
    conn.close()
    return functions


def search_functions(ncc_location: str, ncc_token: str, function_name: str) -> dict:
    """
    This function searches for an existing NCC function with the same name as the intended new NCC function.
    """
    function = {}
    conn = http.client.HTTPSConnection(ncc_location)
    payload = ""
    headers = {"Authorization": ncc_token}
    url_encoded_name = urllib.parse.quote(function_name)
    try:
        conn.request(
            "GET",
            f"/data/api/types/function?q={url_encoded_name}",
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
                    if result["name"] == function_name:
                        function = result
                        break
    except:
        pass
    conn.close()
    return function


def create_function(ncc_location: str, ncc_token: str, function_body: dict) -> dict:
    """
    This function creates an NCC function.
    """
    function = {}
    conn = http.client.HTTPSConnection(ncc_location)
    payload = json.dumps(function_body)
    headers = {
        "Authorization": ncc_token,
        "Content-Type": "application/json",
    }
    try:
        conn.request("POST", "/data/api/types/function/", payload, headers)
        res = conn.getresponse()
        if res.status == 201:
            data = res.read().decode("utf-8")
            function = json.loads(data)
    except:
        pass
    conn.close()
    return function


def delete_function(ncc_location: str, ncc_token: str, function_id: str) -> bool:
    """
    This function deletes an NCC function with the specified function ID.
    """
    success = False
    conn = http.client.HTTPSConnection(ncc_location)
    payload = ""
    headers = {"Authorization": ncc_token}
    try:
        conn.request(
            "DELETE", f"/data/api/types/function/{function_id}", payload, headers
        )
        res = conn.getresponse()
        if res.status == 204:
            success = True
    except:
        pass
    conn.close()
    return success
