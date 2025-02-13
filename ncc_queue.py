import http.client
import urllib.parse
import json


def get_queues(ncc_location: str, ncc_token: str) -> list:
    """
    This function fetches a list of queues present on the Nextiva Contact Center tenant.
    """
    queues = []
    conn = http.client.HTTPSConnection(ncc_location)
    payload = ""
    headers = {"Authorization": ncc_token}
    try:
        conn.request("GET", "/data/api/types/queue?q=Test%20", payload, headers)
        res = conn.getresponse()
        if res.status == 200:
            data = res.read().decode("utf-8")
            json_data = json.loads(data)
            total = json_data["total"]
            if total > 0:
                results = json_data["objects"]
                for result in results:
                    queue_name = result["name"]
                    if queue_name[0:5] == "Test ":
                        queues.append(result)
    except:
        pass
    conn.close()
    return queues


def search_queues(ncc_location: str, ncc_token: str, queue_name: str) -> dict:
    """
    This function searches for an existing queue with the same name as the intended new queue.
    """
    queue = {}
    conn = http.client.HTTPSConnection(ncc_location)
    payload = ""
    headers = {"Authorization": ncc_token}
    url_encoded_name = urllib.parse.quote(queue_name)
    try:
        conn.request(
            "GET",
            f"/data/api/types/queue?q={url_encoded_name}",
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
                    if result["name"] == queue_name:
                        queue = result
                        break
    except:
        pass
    conn.close()
    return queue


def create_queue(ncc_location: str, ncc_token: str, queue_body: dict) -> dict:
    """
    This function creates a queue with the specified name.
    """
    queue = {}
    conn = http.client.HTTPSConnection(ncc_location)
    payload = json.dumps(queue_body)
    headers = {
        "Authorization": ncc_token,
        "Content-Type": "application/json",
    }
    try:
        conn.request("POST", "/data/api/types/queue/", payload, headers)
        res = conn.getresponse()
        if res.status == 201:
            data = res.read().decode("utf-8")
            queue = json.loads(data)
    except:
        pass
    conn.close()
    return queue


def delete_queue(ncc_location: str, ncc_token: str, queue_id: str) -> bool:
    """
    This function deletes a queue with the specified queue ID.
    """
    success = False
    conn = http.client.HTTPSConnection(ncc_location)
    payload = ""
    headers = {"Authorization": ncc_token}
    try:
        conn.request("DELETE", f"/data/api/types/queue/{queue_id}", payload, headers)
        res = conn.getresponse()
        if res.status == 204:
            success = True
    except:
        pass
    conn.close()
    return success
