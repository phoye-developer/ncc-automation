import http.client
import json


def post_datadog_event(
    dd_api_key: str,
    dd_application_key: str,
    username: str,
    alert_type: str,
    priority: str,
    title: str,
    text: str,
    tags: list,
) -> bool:
    success = False
    conn = http.client.HTTPSConnection("api.us3.datadoghq.com")
    payload = json.dumps(
        {
            "aggregation_key": username,
            "alert_type": alert_type,
            "priority": priority,
            "source_type_name": "python",
            "title": title,
            "text": text,
            "tags": tags,
        }
    )
    headers = {
        "DD-API-KEY": dd_api_key,
        "DD-APPLICATION-KEY": dd_application_key,
        "Content-Type": "application/json",
    }
    try:
        conn.request("POST", "/api/v1/events", payload, headers)
        res = conn.getresponse()
        if res.status == 202:
            success = True
    except:
        pass
    conn.close()
    return success
