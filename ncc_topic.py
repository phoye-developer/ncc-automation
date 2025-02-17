import http.client
import urllib.parse
import json


def search_topics(ncc_location: str, ncc_token: str, topic_name: str) -> dict:
    """
    This function searches for an existing topic with the same name as the intended new topic.
    """
    topic = {}
    conn = http.client.HTTPSConnection(ncc_location)
    payload = ""
    headers = {"Authorization": ncc_token}
    url_encoded_name = urllib.parse.quote(topic_name)
    try:
        conn.request(
            "GET",
            f"/data/api/types/topic?q={url_encoded_name}",
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
                    if result["name"] == topic_name:
                        topic = result
                        break
    except:
        pass
    conn.close()
    return topic


def create_topic(ncc_location: str, ncc_token: str, topic_name: str) -> dict:
    """
    This function creates a topic with a specified name.
    """
    topic = {}
    conn = http.client.HTTPSConnection(ncc_location)
    payload = json.dumps({"name": topic_name})
    headers = {
        "Authorization": ncc_token,
        "Content-Type": "application/json",
    }
    try:
        conn.request("POST", "/data/api/types/topic/", payload, headers)
        res = conn.getresponse()
        if res.status == 201:
            data = res.read().decode("utf-8")
            topic = json.loads(data)
    except:
        pass
    conn.close()
    return topic


def update_topic_users(
    ncc_location: str, ncc_token: str, topic_id: str, users: list
) -> bool:
    """
    This function updates the list of users assigned to a topic in Nextiva Contact Center (NCC).
    """
    success = False
    conn = http.client.HTTPSConnection(ncc_location)
    payload = json.dumps({"users": users})
    headers = {
        "Authorization": ncc_token,
        "Content-Type": "application/json",
    }
    try:
        conn.request("PATCH", f"/data/api/types/topic/{topic_id}", payload, headers)
        res = conn.getresponse()
        if res.status == 200:
            success = True
    except:
        pass
    conn.close()
    return success


def delete_topic(ncc_location: str, ncc_token: str, topic_id: str) -> bool:
    """
    This function deletes a topic with the specified topic ID.
    """
    success = False
    conn = http.client.HTTPSConnection(ncc_location)
    payload = ""
    headers = {"Authorization": ncc_token}
    try:
        conn.request("DELETE", f"/data/api/types/topic/{topic_id}", payload, headers)
        res = conn.getresponse()
        if res.status == 204:
            success = True
    except:
        pass
    conn.close()
    return success
