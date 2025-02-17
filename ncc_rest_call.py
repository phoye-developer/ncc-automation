import http.client
import urllib.parse
import json


def search_rest_calls(ncc_location: str, ncc_token: str, rest_call_name: str) -> dict:
    """
    This function searches for an existing REST API call object with the same name as the intended new REST API call object.
    """
    rest_call = {}
    conn = http.client.HTTPSConnection(ncc_location)
    payload = ""
    headers = {"Authorization": ncc_token}
    url_encoded_name = urllib.parse.quote(rest_call_name)
    try:
        conn.request(
            "GET",
            f"/data/api/types/restcall?q={url_encoded_name}",
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
                    if result["name"] == rest_call_name:
                        rest_call = result
                        break
    except:
        pass
    conn.close()
    return rest_call


def hubspot_create_search_contacts_rest_call(
    ncc_location: str, ncc_token: str, hubspot_access_token: str, rest_call_name: str
) -> dict:
    """
    This function creates a REST API call object to search for contacts in HubSpot.
    """
    rest_call = {}
    conn = http.client.HTTPSConnection(ncc_location)
    payload = json.dumps(
        {
            "name": rest_call_name,
            "localizations": {
                "name": {"en": {"language": "en", "value": rest_call_name}}
            },
            "method": "POST",
            "url": "https://api.hubspot.com/crm/v3/objects/contacts/search",
            "body": '{\r\n  "filterGroups": [\r\n    {\r\n      "filters": [\r\n        {\r\n          "value": "$V.workitem.from",\r\n          "propertyName": "phone",\r\n          "operator": "EQ"\r\n        }\r\n      ]\r\n    }\r\n  ]\r\n}',
            "authUrl": "",
            "authType": "NO_AUTH",
            "authUsername": "",
            "authPassword": "",
            "headerParameters": [
                {
                    "key": "Authorization",
                    "value": f"Bearer {hubspot_access_token}",
                },
                {"key": "Content-Type", "value": "application/json"},
            ],
            "authClientId": "",
            "authClientSecret": "",
            "authGrantType": "",
            "authScope": "",
            "msAuthURL": "",
            "msAuthClientId": "",
            "msAuthGrantType": "",
            "msAuthClientSecret": "",
            "msAuthScope": "",
            "msAuthUsername": "",
            "msAuthPassword": "",
        }
    )
    headers = {
        "Authorization": ncc_token,
        "Content-Type": "application/json",
    }
    try:
        conn.request("POST", "/data/api/types/restcall/", payload, headers)
        res = conn.getresponse()
        if res.status == 201:
            data = res.read().decode("utf-8")
            rest_call = json.loads(data)
    except:
        pass
    conn.close()
    return rest_call


def hubspot_create_activity_rest_call(
    ncc_location: str, ncc_token: str, hubspot_access_token: str, rest_call_name: str
) -> dict:
    """
    This function creates a REST API call object to create an activity in HubSpot.
    """
    rest_call = {}
    conn = http.client.HTTPSConnection(ncc_location)
    payload = json.dumps(
        {
            "name": rest_call_name,
            "localizations": {
                "name": {"en": {"language": "en", "value": rest_call_name}}
            },
            "method": "POST",
            "url": "https://api.hubspot.com/crm/v3/objects/calls",
            "body": '{\r\n    "properties": {\r\n        "hs_timestamp": "2022-10-29T13:17:31.000Z",\r\n        "hs_call_title": "Get Insurance",\r\n        "hs_call_body": "Agent comments: Paul called in to get car insurance.\\nSent quote via email.",\r\n        "hs_call_duration": "894144",\r\n        "hs_call_direction": "INBOUND",\r\n        "hs_call_disposition": "f240bbac-87c9-4f6e-bf70-924b57d47db7",\r\n        "hs_call_from_number": "+16024053038",\r\n        "hs_call_to_number": "+16029000135",\r\n        "hubspot_owner_id": "{{OWNER_ID}}",\r\n        "hs_call_status": "COMPLETED"\r\n    }\r\n}',
            "authUrl": "",
            "authType": "NO_AUTH",
            "authUsername": "",
            "authPassword": "",
            "headerParameters": [
                {
                    "key": "Authorization",
                    "value": f"Bearer {hubspot_access_token}",
                },
                {"key": "Content-Type", "value": "application/json"},
            ],
            "authClientId": "",
            "authClientSecret": "",
            "authGrantType": "",
            "authScope": "",
            "msAuthURL": "",
            "msAuthClientId": "",
            "msAuthGrantType": "",
            "msAuthClientSecret": "",
            "msAuthScope": "",
            "msAuthUsername": "",
            "msAuthPassword": "",
        }
    )
    headers = {
        "Authorization": ncc_token,
        "Content-Type": "application/json",
    }
    try:
        conn.request("POST", "/data/api/types/restcall/", payload, headers)
        res = conn.getresponse()
        if res.status == 201:
            data = res.read().decode("utf-8")
            rest_call = json.loads(data)
    except:
        pass
    conn.close()
    return rest_call


def zendesk_create_search_contacts_rest_call(
    ncc_location: str,
    ncc_token: str,
    zendesk_username: str,
    zendesk_password: str,
    rest_call_name: str,
) -> dict:
    """
    This function creates a REST API call object to search for contacts in Zendesk.
    """
    rest_call = {}
    conn = http.client.HTTPSConnection(ncc_location)
    payload = json.dumps(
        {
            "name": rest_call_name,
            "localizations": {
                "name": {"en": {"language": "en", "value": rest_call_name}}
            },
            "method": "GET",
            "url": "https://d3v-phoye.zendesk.com/api/v2/users/search.json?query=$V.workitem.data.phone",
            "body": "",
            "authUrl": "",
            "authType": "BASIC_AUTH",
            "authUsername": zendesk_username,
            "authPassword": zendesk_password,
            "authClientId": "",
            "authClientSecret": "",
            "authGrantType": "",
            "authScope": "",
            "msAuthURL": "",
            "msAuthClientId": "",
            "msAuthGrantType": "",
            "msAuthClientSecret": "",
            "msAuthScope": "",
            "msAuthUsername": "",
            "msAuthPassword": "",
        }
    )
    headers = {
        "Authorization": ncc_token,
        "Content-Type": "application/json",
    }
    try:
        conn.request("POST", "/data/api/types/restcall/", payload, headers)
        res = conn.getresponse()
        if res.status == 201:
            data = res.read().decode("utf-8")
            rest_call = json.loads(data)
    except:
        pass
    conn.close()
    return rest_call


def zendesk_create_ticket_rest_call(
    ncc_location: str,
    ncc_token: str,
    zendesk_username: str,
    zendesk_password: str,
    rest_call_name: str,
) -> dict:
    """
    This function creates a REST API call object to create a ticket in Zendesk.
    """
    rest_call = {}
    conn = http.client.HTTPSConnection(ncc_location)
    payload = json.dumps(
        {
            "name": rest_call_name,
            "localizations": {
                "name": {"en": {"language": "en", "value": rest_call_name}}
            },
            "method": "POST",
            "url": "https://d3v-phoye.zendesk.com/api/v2/tickets.json",
            "body": '{\r\n    "ticket": {\r\n        "subject": "${workitem.data.ticketSubject}",\r\n        "status": "${workitem.data.ticketStatus}",\r\n        "comment": {\r\n            "body": "${workitem.data.ticketComments}",\r\n            "public": false\r\n        },\r\n        "priority": "${workitem.data.ticketPriority}",\r\n        "requester_id": "${workitem.data.newContactId}",\r\n        "submitter_id": 1515190483562\r\n    }\r\n}',
            "authUrl": "",
            "authType": "NO_AUTH",
            "authUsername": zendesk_username,
            "authPassword": zendesk_password,
            "headerParameters": [{"key": "Content-Type", "value": "application/json"}],
            "authClientId": "",
            "authClientSecret": "",
            "authGrantType": "",
            "authScope": "",
            "msAuthURL": "",
            "msAuthClientId": "",
            "msAuthGrantType": "",
            "msAuthClientSecret": "",
            "msAuthScope": "",
            "msAuthUsername": "",
            "msAuthPassword": "",
        }
    )
    headers = {
        "Authorization": ncc_token,
        "Content-Type": "application/json",
    }
    try:
        conn.request("POST", "/data/api/types/restcall/", payload, headers)
        res = conn.getresponse()
        if res.status == 201:
            data = res.read().decode("utf-8")
            rest_call = json.loads(data)
    except:
        pass
    conn.close()
    return rest_call


def delete_rest_call(ncc_location: str, ncc_token: str, rest_call_id: str) -> bool:
    """
    This function deletes a REST API call object with the specified ID.
    """
    success = False
    conn = http.client.HTTPSConnection(ncc_location)
    payload = ""
    headers = {"Authorization": ncc_token}
    try:
        conn.request(
            "DELETE", f"/data/api/types/restcall/{rest_call_id}", payload, headers
        )
        res = conn.getresponse()
        if res.status == 204:
            success = True
    except:
        pass
    conn.close()
    return success
