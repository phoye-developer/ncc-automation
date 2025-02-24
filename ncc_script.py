import http.client
import urllib.parse
import json


def search_scripts(ncc_location: str, ncc_token: str, script_name: str) -> dict:
    """
    This function searches for an existing script with the same name as the intended new script.
    """
    script = {}
    conn = http.client.HTTPSConnection(ncc_location)
    payload = ""
    headers = {"Authorization": ncc_token}
    url_encoded_name = urllib.parse.quote(script_name)
    try:
        conn.request(
            "GET",
            f"/data/api/types/script?q={url_encoded_name}",
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
                    if result["name"] == script_name:
                        script = result
                        break
    except:
        pass
    conn.close()
    return script


def create_check_has_all_parameters_script(
    ncc_location: str, ncc_token: str, script_name: str
) -> dict:
    """
    This function creates a script to check whether all required paramaters have been collected by Google Dialogflow.
    """
    script = {}
    conn = http.client.HTTPSConnection(ncc_location)
    payload = json.dumps(
        {
            "localizations": {"name": {"en": {"language": "en", "value": script_name}}},
            "content": 'if (workitem.type == "Chat" || workitem.type == "InboundSMS") {\n    if (workitem.chatBotResponse.parameters.hasAllParameters) {\n        hasAllParameters = true;\n    } else {\n        hasAllParameters = false;\n    }\n} else if (workitem.type == "InboundCall") {\n    if (workitem.data.botWebhookRequest.queryResult.allRequiredParamsPresent) {\n        hasAllParameters = true;\n    } else {\n        hasAllParameters = false;\n    }\n} else {\n    hasAllParameters = false;\n}',
            "name": script_name,
        }
    )
    headers = {
        "Authorization": ncc_token,
        "Content-Type": "application/json",
    }
    try:
        conn.request("POST", "/data/api/types/script/", payload, headers)
        res = conn.getresponse()
        if res.status == 201:
            data = res.read().decode("utf-8")
            script = json.loads(data)
    except:
        pass
    conn.close()
    return script


def create_get_function_id_script(
    ncc_location: str, ncc_token: str, script_name: str
) -> dict:
    """
    This function creates a script to get the funtionId parameter returned by Google Dialogflow.
    """
    script = {}
    conn = http.client.HTTPSConnection(ncc_location)
    payload = json.dumps(
        {
            "localizations": {"name": {"en": {"language": "en", "value": script_name}}},
            "content": 'functionId = "";\n\nif (workitem.type == "Chat" || workitem.type == "InboundSMS") {\n    functionId = workitem.chatBotResponse.parameters.functionId.string;\n} else if (workitem.type == "InboundCall") {\n    functionId = workitem.data.botWebhookRequest.queryResult.parameters.functionId;\n} else {\n    functionId = Unknown;\n}\n\nfunctionId',
            "name": script_name,
        }
    )
    headers = {
        "Authorization": ncc_token,
        "Content-Type": "application/json",
    }
    try:
        conn.request("POST", "/data/api/types/script/", payload, headers)
        res = conn.getresponse()
        if res.status == 201:
            data = res.read().decode("utf-8")
            script = json.loads(data)
    except:
        pass
    conn.close()
    return script


def delete_script(ncc_location: str, ncc_token: str, script_id: str) -> bool:
    """
    This function deletes a script with the specified script ID.
    """
    success = False
    conn = http.client.HTTPSConnection(ncc_location)
    payload = ""
    headers = {"Authorization": ncc_token}
    try:
        conn.request("DELETE", f"/data/api/types/script/{script_id}", payload, headers)
        res = conn.getresponse()
        if res.status == 204:
            success = True
    except:
        pass
    conn.close()
    return success
