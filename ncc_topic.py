import http.client
import urllib.parse
import json


def get_topics(ncc_location: str, ncc_token: str) -> list:
    """
    This function fetches a list of topics present on the Nextiva Contact Center tenant.
    """
    topics = []
    conn = http.client.HTTPSConnection(ncc_location)
    payload = ""
    headers = {"Authorization": ncc_token}
    conn.request("GET", "/data/api/types/topic?q=Test%20", payload, headers)
    res = conn.getresponse()
    if res.status == 200:
        data = res.read().decode("utf-8")
        json_data = json.loads(data)
        total = json_data["total"]
        if total > 0:
            results = json_data["objects"]
            for result in results:
                topic_name = result["name"]
                if topic_name[0:5] == "Test ":
                    topics.append(result)
    return topics


def search_topics(ncc_location: str, ncc_token: str, topic_name: str) -> dict:
    """
    This function searches for an existing topic with the same name as the intended new topic.
    """
    topic = {}
    conn = http.client.HTTPSConnection(ncc_location)
    payload = ""
    headers = {"Authorization": ncc_token}
    url_encoded_name = urllib.parse.quote(topic_name)
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
    conn.request("POST", "/data/api/types/topic/", payload, headers)
    res = conn.getresponse()
    if res.status == 201:
        data = res.read().decode("utf-8")
        topic = json.loads(data)
    conn.close()
    return topic


def delete_topic(ncc_location: str, ncc_token: str, topic_id: str) -> bool:
    """
    This function deletes a topic with the specified topic ID.
    """
    success = False
    conn = http.client.HTTPSConnection(ncc_location)
    payload = ""
    headers = {"Authorization": ncc_token}
    conn.request(
        "DELETE", f"/data/api/types/topic/{topic_id}", payload, headers
    )
    res = conn.getresponse()
    if res.status == 204:
        success = True
    return success
