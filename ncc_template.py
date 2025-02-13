import http.client
import urllib.parse
import json


def get_templates(ncc_location: str, ncc_token: str) -> list:
    """
    This function fetches a list of templates present in Nextiva Contact Center (NCC).
    """
    templates = []
    conn = http.client.HTTPSConnection(ncc_location)
    payload = ""
    headers = {"Authorization": ncc_token}
    try:
        conn.request("GET", "/data/api/types/template?q=Test%20", payload, headers)
        res = conn.getresponse()
        if res.status == 200:
            data = res.read().decode("utf-8")
            json_data = json.loads(data)
            total = json_data["total"]
            if total > 0:
                results = json_data["objects"]
                for result in results:
                    template_name = result["name"]
                    if template_name[0:5] == "Test ":
                        templates.append(result)
    except:
        pass
    conn.close()
    return templates


def search_templates(ncc_location: str, ncc_token: str, template_name: str) -> dict:
    """
    This function searches for an existing template in Nextiva Contact Center (NCC) with the same name as the intended new template.
    """
    template = {}
    conn = http.client.HTTPSConnection(ncc_location)
    payload = ""
    headers = {"Authorization": ncc_token}
    url_encoded_name = urllib.parse.quote(template_name)
    try:
        conn.request(
            "GET",
            f"/data/api/types/template?q={url_encoded_name}",
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
                    if result["name"] == template_name:
                        template = result
                        break
    except:
        pass
    conn.close()
    return template


def create_template(
    ncc_location: str,
    ncc_token: str,
    template_body: dict,
) -> dict:
    """
    This function creates a template in Nextiva Contact Center (NCC).
    """
    template = {}
    conn = http.client.HTTPSConnection(ncc_location)
    payload = json.dumps(template_body)
    headers = {
        "Authorization": ncc_token,
        "Content-Type": "application/json",
    }
    try:
        conn.request("POST", "/data/api/types/template", payload, headers)
        res = conn.getresponse()
        if res.status == 201:
            data = res.read().decode("utf-8")
            template = json.loads(data)
    except:
        pass
    conn.close()
    return template


def delete_template(ncc_location: str, ncc_token: str, template_id: str) -> bool:
    """
    This function deletes a template with the specified template ID.
    """
    success = False
    conn = http.client.HTTPSConnection(ncc_location)
    payload = ""
    headers = {"Authorization": ncc_token}
    try:
        conn.request(
            "DELETE",
            f"/data/api/types/template/{template_id}",
            payload,
            headers,
        )
        res = conn.getresponse()
        if res.status == 204:
            success = True
    except:
        pass
    conn.close()
    return success
