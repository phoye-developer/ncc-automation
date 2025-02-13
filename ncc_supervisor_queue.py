import http.client
import json


def search_supervisor_queues(
    ncc_location: str, ncc_token: str, supervisor_id: str, queue_id: str
) -> bool:
    """
    This function searches for a specified queue ID in the supervisorqueue objects.
    """
    success = False
    conn = http.client.HTTPSConnection(ncc_location)
    payload = ""
    headers = {"Authorization": ncc_token}
    try:
        conn.request(
            "GET",
            f"/data/api/types/supervisorqueue?q={queue_id}",
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
                    if result["userId"] == supervisor_id:
                        success = True
                        break
    except:
        pass
    conn.close()
    return success


def create_supervisor_queue(
    ncc_location: str, ncc_token: str, supervisor_id: str, queue_id: str
) -> bool:
    """
    This function assigns a supervisor to a queue.
    """
    success = False
    conn = http.client.HTTPSConnection(ncc_location)
    payload = json.dumps(
        {
            "userId": supervisor_id,
            "queueId": queue_id,
        }
    )
    headers = {
        "Authorization": ncc_token,
        "Content-Type": "application/json",
    }
    try:
        conn.request("POST", "/data/api/types/supervisorqueue/", payload, headers)
        res = conn.getresponse()
        if res.status == 201:
            success = True
    except:
        pass
    conn.close()
    return success
