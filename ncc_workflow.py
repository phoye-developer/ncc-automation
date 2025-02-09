import http.client
import urllib.parse
import json


def get_workflow(ncc_location: str, ncc_token: str, workflow_id: str) -> dict:
    """
    This function fetches the details for a specific workflow.
    """
    workflow = {}
    conn = http.client.HTTPSConnection(ncc_location)
    payload = ""
    headers = {"Authorization": ncc_token}
    conn.request("GET", f"/data/api/types/workflow/{workflow_id}", payload, headers)
    res = conn.getresponse()
    if res.status == 200:
        data = res.read().decode("utf-8")
        workflow = json.loads(data)
    return workflow


def get_workflows(ncc_location: str, ncc_token: str) -> list:
    """
    This function fetches a list of workflows present on the Nextiva Contact Center tenant.
    """
    workflows = []
    conn = http.client.HTTPSConnection(ncc_location)
    payload = ""
    headers = {"Authorization": ncc_token}
    conn.request("GET", "/data/api/types/workflow?q=Test%20", payload, headers)
    res = conn.getresponse()
    if res.status == 200:
        data = res.read().decode("utf-8")
        json_data = json.loads(data)
        total = json_data["total"]
        if total > 0:
            results = json_data["objects"]
            for result in results:
                workflow_name = result["name"]
                if workflow_name[0:5] == "Test ":
                    workflows.append(result)
    return workflows


def search_workflows(ncc_location: str, ncc_token: str, workflow_name: str) -> dict:
    """
    This function searches for an existing workflow with the same name as the intended new workflow.
    """
    workflow = {}
    conn = http.client.HTTPSConnection(ncc_location)
    payload = ""
    headers = {"Authorization": ncc_token}
    url_encoded_workflow_name = urllib.parse.quote(workflow_name)
    conn.request(
        "GET",
        f"/data/api/types/workflow?q={url_encoded_workflow_name}",
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
                if result["name"] == workflow_name:
                    workflow = result
                    break
    conn.close()
    return workflow


def create_workflow(
    ncc_location: str,
    ncc_token: str,
    workflow_body: dict,
    workflow_name: str,
    business_name: str,
    queues: dict,
    acd_voicemail_function: dict,
    acd_callback_function: dict,
) -> dict:
    """
    This function creates a workflow in Nextiva Contact Center (NCC).
    """
    workflow = {}
    conn = http.client.HTTPSConnection(ncc_location)

    workflow_body["localizations"]["name"]["en"]["value"] = workflow_name
    workflow_body["name"] = workflow_name

    states = workflow_body["states"]
    for state, value in enumerate(states):
        if value == "start-state":
            actions = states[value]["actions"]
            for action in actions:
                try:
                    if action["properties"]["variableName"] == "companyName":
                        action["properties"]["rightExpression"] = business_name
                    elif action["properties"]["variableName"] == "queueId":
                        action["properties"]["rightExpression"] = queues[
                            "Test Customer Service"
                        ]
                except:
                    pass
        elif (
            value == "6754d3e1cebccc1b46fb81b9"
            or value == "65b01880267d5184c650aba5"
            or value == "66d8fb13ad3c61caa09d1110"
        ):
            actions = states[value]["actions"]
            for action in actions:
                try:
                    if action["properties"]["description"] == "ACD Voicemail (1)":
                        action["properties"]["functionId"] = acd_voicemail_function[
                            "_id"
                        ]
                        action["properties"]["expansions"]["functionId"]["name"] = (
                            acd_voicemail_function["name"]
                        )
                    elif action["properties"]["description"] == "ACD Callback (2)":
                        action["properties"]["functionId"] = acd_callback_function[
                            "_id"
                        ]
                        action["properties"]["expansions"]["functionId"]["name"] = (
                            acd_callback_function["name"]
                        )
                except:
                    pass

    payload = json.dumps(workflow_body)
    headers = {
        "Authorization": ncc_token,
        "Content-Type": "application/json",
    }
    conn.request("POST", "/data/api/types/workflow/", payload, headers)
    res = conn.getresponse()
    if res.status == 201:
        data = res.read().decode("utf-8")
        workflow = json.loads(data)
    return workflow


def assign_rest_call_to_workflow(
    ncc_location: str,
    ncc_token: str,
    rest_call_id: str,
    workflow_id: str,
    rest_call_name: str,
) -> bool:
    """
    This function adds an Execute Rest component to a Nextiva Contact Center (NCC) workflow.
    """
    success = False
    conn = http.client.HTTPSConnection(ncc_location)
    payload = json.dumps(
        {
            "states": {
                "67875b41a4c102ae206943b9": {
                    "category": "Standard",
                    "campaignStateId": "67875b41a4c102ae206943b9",
                    "actions": [
                        {
                            "category": "Action",
                            "title": "Terminate",
                            "name": "Terminate",
                            "type": "terminate",
                            "description": "Terminate",
                            "icon": "./assets/svg/icon-terminate",
                            "svg": "",
                            "color": "#FFFFFF",
                            "fig": "Rectangle",
                            "properties": {
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                }
                            },
                        }
                    ],
                    "objectType": "campaignstate",
                    "key": "67875b41a4c102ae206943b9",
                    "_id": "67875b41a4c102ae206943b9",
                    "description": "End State",
                    "name": "End State",
                    "location": "200 100",
                    "transitions": [],
                },
                "start-state": {
                    "category": "Begin",
                    "campaignStateId": "start-state",
                    "actions": [
                        {
                            "icon": "icon-api",
                            "name": "Execute REST Call",
                            "description": "Search Contacts",
                            "properties": {
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "responseVariable": "searchContactsResponse",
                                "restCallId": rest_call_id,
                                "_working": False,
                                "description": "Search Contacts",
                                "expansions": {"restCallId": {"name": rest_call_name}},
                            },
                            "type": "restapi",
                            "_selected": True,
                        },
                        {
                            "name": "Start",
                            "type": "transition",
                            "description": "Transition to another state",
                            "properties": {
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "stateId": "67875b41a4c102ae206943b9",
                                "name": "Start",
                                "description": "Transition to another state",
                            },
                            "transitionId": "6787681cf851f26a1784df71",
                            "_selected": False,
                            "icon": "icon-transition",
                            "id": "refId1736922763544",
                        },
                    ],
                    "transitions": [
                        {"name": "Start", "id": "6787681cf851f26a1784df71"}
                    ],
                    "objectType": "campaignstate",
                    "key": "start-state",
                    "_id": "start-state",
                    "description": "Begin State",
                    "name": "Begin State",
                    "location": "0 0",
                },
            }
        }
    )
    headers = {
        "Authorization": ncc_token,
        "Content-Type": "application/json",
    }
    conn.request("PATCH", f"/data/api/types/workflow/{workflow_id}", payload, headers)
    res = conn.getresponse()
    if res.status == 200:
        success = True
    conn.close()
    return success


def add_extend_call_component(
    ncc_location: str, ncc_token: str, workflow_id: str, function_id: str
) -> bool:
    """
    This function adds the Extend Call component to the Begin State of the specified workflow.
    """
    success = False
    workflow = get_workflow(ncc_location, ncc_token, workflow_id)
    if workflow != {}:
        states = workflow["states"]
        for state_key in states:
            if state_key == "start-state":
                actions = states[state_key]["actions"]
                actions.insert(
                    0,
                    {
                        "name": "Extend Call",
                        "description": "Extend Call",
                        "properties": {
                            "functionId": function_id,
                            "condition": {
                                "conditionType": "AND",
                                "expressions": [
                                    {
                                        "operator": "==",
                                        "leftExpression": "workitem.type",
                                        "rightExpression": "'InboundCall'",
                                    }
                                ],
                            },
                            "expansions": {
                                "functionId": {"name": "Test Post-Call Survey"}
                            },
                            "_working": False,
                        },
                        "type": "aftercallivr",
                        "_selected": False,
                        "icon": "icon-play-voicemail-greeting",
                        "id": "refId1715372161608",
                    },
                )
    success = update_workflow(ncc_location, ncc_token, workflow_id, workflow)
    return success


def add_sms_message_consumer_survey_link(
    ncc_location: str, ncc_token: str, workflow_id: str
) -> bool:
    """
    This function adds the SMS Message Consumer component to the End State of the specified workflow.
    """
    success = False
    workflow = get_workflow(ncc_location, ncc_token, workflow_id)
    if workflow != {}:
        states = workflow["states"]
        for state_key in states:
            if state_key == "67875b41a4c102ae206943b9":
                actions = states[state_key]["actions"]
                actions.insert(
                    0,
                    {
                        "icon": "icon-ai-message",
                        "name": "Send Survey Link",
                        "description": "",
                        "properties": {
                            "description": "",
                            "message": "Thank you for contacting us! To take a brief survey, go to https://www.mysurveysite.com?workitem_id=${workitem.workitemId}",
                            "toAddress": "workitem.from",
                            "fromAddress": "workitem.to",
                            "createNewWorkitem": False,
                            "condition": {
                                "conditionType": "OR",
                                "expressions": [
                                    {
                                        "operator": "==",
                                        "leftExpression": "workitem.type",
                                        "rightExpression": "'InboundCall'",
                                    },
                                    {
                                        "operator": "==",
                                        "leftExpression": "workitem.type",
                                        "rightExpression": "'InboundSMS'",
                                    },
                                ],
                            },
                        },
                        "type": "smsmessageconsumer",
                        "_selected": False,
                    },
                )
    success = update_workflow(ncc_location, ncc_token, workflow_id, workflow)
    return success


def update_workflow(
    ncc_location: str, ncc_token: str, workflow_id: str, workflow_body: dict
) -> bool:
    """
    This function updates an NCC workflow with the specified workflow ID and workflow body.
    """
    success = False
    conn = http.client.HTTPSConnection(ncc_location)
    payload = json.dumps(workflow_body)
    headers = {"Authorization": ncc_token, "Content-Type": "application/json"}
    conn.request("PATCH", f"/data/api/types/workflow/{workflow_id}", payload, headers)
    res = conn.getresponse()
    if res.status == 200:
        success = True
    return success


def delete_workflow(ncc_location: str, ncc_token: str, workflow_id: str) -> bool:
    """
    This function deletes a workflow with the specified workflow ID.
    """
    success = False
    conn = http.client.HTTPSConnection(ncc_location)
    payload = ""
    headers = {"Authorization": ncc_token}
    conn.request("DELETE", f"/data/api/types/workflow/{workflow_id}", payload, headers)
    res = conn.getresponse()
    if res.status == 204:
        success = True
    return success
