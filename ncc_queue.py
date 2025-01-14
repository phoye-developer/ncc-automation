import http.client
import urllib.parse
import json


def get_queues(ncc_location: str, ncc_token: str) -> str:
    """
    This function fetches a list of queues present on the Nextiva Contact Center tenant.
    """
    test_queue_ids = []
    conn = http.client.HTTPSConnection(ncc_location)
    payload = ""
    headers = {"Authorization": ncc_token}
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
                    test_queue_ids.append(result["queueId"])
    return test_queue_ids


def search_queues(ncc_location: str, ncc_token: str, queue_name: str) -> str:
    """
    This function searches for an existing queue with the same name as the intended new queue.
    """
    queue_id = ""
    conn = http.client.HTTPSConnection(ncc_location)
    payload = ""
    headers = {"Authorization": ncc_token}
    url_encoded_name = urllib.parse.quote(queue_name)
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
                    queue_id = result["queueId"]
                    break
    conn.close()
    return queue_id


def create_queue(ncc_location: str, ncc_token: str, queue_name: str) -> str:
    """
    This function creates a queue with the specified name.
    """
    queue_id = ""
    conn = http.client.HTTPSConnection(ncc_location)
    payload = json.dumps(
        {
            "blended": False,
            "assignmentType": "fifo_across_all_queues",
            "pushQueueDataInRealTime": True,
            "hideInCompanyDirectory": False,
            "disableSkills": False,
            "noAnswerStatusAsAvailable": False,
            "socialSLA": 3600,
            "localizations": {"name": {"en": {"language": "en", "value": queue_name}}},
            "slaCalculation": 1,
            "emailSLA": 3600,
            "realtimeAssignment": True,
            "lifo": False,
            "name": queue_name,
            "voiceSLA": 30,
            "chatSLA": 30,
        }
    )
    headers = {
        "Authorization": ncc_token,
        "Content-Type": "application/json",
    }
    conn.request("POST", "/data/api/types/queue/", payload, headers)
    res = conn.getresponse()
    if res.status == 201:
        data = res.read().decode("utf-8")
        json_data = json.loads(data)
        queue_id = json_data["queueId"]
    conn.close()
    return queue_id


def delete_queue(ncc_location: str, ncc_token: str, queue_id: str) -> bool:
    """
    This function deletes a queue with the specified queue ID.
    """
    success = False
    conn = http.client.HTTPSConnection(ncc_location)
    payload = ""
    headers = {"Authorization": ncc_token}
    conn.request("DELETE", f"/data/api/types/queue/{queue_id}", payload, headers)
    res = conn.getresponse()
    if res.status == 204:
        success = True
    return success
