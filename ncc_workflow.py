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
    try:
        conn.request("GET", f"/data/api/types/workflow/{workflow_id}", payload, headers)
        res = conn.getresponse()
        if res.status == 200:
            data = res.read().decode("utf-8")
            workflow = json.loads(data)
    except:
        pass
    conn.close()
    return workflow


def get_workflows(ncc_location: str, ncc_token: str) -> list:
    """
    This function fetches a list of workflows in Nextiva Contact Center (NCC).
    """
    workflows = []
    conn = http.client.HTTPSConnection(ncc_location)
    payload = ""
    headers = {"Authorization": ncc_token}
    try:
        conn.request("GET", f"/data/api/types/workflow", payload, headers)
        res = conn.getresponse()
        if res.status == 200:
            data = res.read().decode("utf-8")
            json_data = json.loads(data)
            total = json_data["total"]
            if total > 0:
                results = json_data["objects"]
                for result in results:
                    workflows.append(result)
    except:
        pass
    conn.close()
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
    try:
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
    except:
        pass
    conn.close()
    return workflow


def create_iva_workflow(
    ncc_location: str,
    ncc_token: str,
    workflow_name: str,
    business_name: str,
    queues: dict,
    search_contacts_function: dict,
    two_way_chat_function: dict,
    two_way_sms_function: dict,
    prompt: dict,
    acd_voicemail_function: dict,
    acd_callback_function: dict,
) -> dict:
    """
    This function creates a workflow in Nextiva Contact Center (NCC) for use as an Intelligent Virtual Agent (IVA).
    """
    workflow = {}
    conn = http.client.HTTPSConnection(ncc_location)
    payload = json.dumps(
        {
            "maxActions": 10000,
            "localizations": {
                "name": {"en": {"language": "en", "value": workflow_name}},
                "description": {"en": {"language": "en", "value": "IVA workflow"}},
            },
            "states": {
                "67b1186f5510d9081ac8e32b": {
                    "category": "Standard",
                    "campaignStateId": "67b1186f5510d9081ac8e32b",
                    "actions": [
                        {
                            "name": "ACD Voicemail From Expression",
                            "description": "Create ACD Voicemail",
                            "properties": {
                                "transcription": True,
                                "priority": 3,
                                "queueIdsExpression": "workitem.data.queueId",
                                "toAddress": "",
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "operator": "==",
                                            "leftExpression": "workitem.data.messageRecorded",
                                            "rightExpression": "1",
                                        }
                                    ],
                                },
                                "description": "Create ACD Voicemail",
                            },
                            "type": "acdvmfromexpression",
                            "_selected": False,
                            "id": "refId1723818900554",
                            "icon": "icon-directconnect",
                        },
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
                        },
                    ],
                    "objectType": "campaignstate",
                    "key": "67b1186f5510d9081ac8e32b",
                    "_id": "67b1186f5510d9081ac8e32b",
                    "description": "End State",
                    "name": "End State",
                    "location": "-147.23017129888294 34.91808770109185",
                    "transitions": [],
                },
                "start-state": {
                    "category": "Begin",
                    "campaignStateId": "start-state",
                    "actions": [
                        {
                            "name": "Save Variable",
                            "description": "",
                            "properties": {
                                "description": "companyName",
                                "rightExpression": business_name,
                                "variableName": "companyName",
                                "asObject": False,
                                "dlpOption": False,
                                "wfmOption": False,
                                "dashboard": False,
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                            },
                            "type": "savevariable",
                            "_selected": False,
                            "id": "refId1739600227611",
                            "icon": "icon-save",
                        },
                        {
                            "icon": "icon-save",
                            "name": "Save Variable",
                            "description": "",
                            "properties": {
                                "description": "sourceLanguage",
                                "rightExpression": "en",
                                "variableName": "sourceLanguage",
                                "asObject": False,
                                "dlpOption": False,
                                "wfmOption": False,
                                "dashboard": False,
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                            },
                            "type": "savevariable",
                            "_selected": False,
                        },
                        {
                            "name": "Save Variable",
                            "description": "",
                            "properties": {
                                "description": "contactFound",
                                "rightExpression": "false",
                                "variableName": "contactFound",
                                "asObject": True,
                                "dlpOption": False,
                                "wfmOption": False,
                                "dashboard": False,
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                            },
                            "type": "savevariable",
                            "_selected": False,
                            "id": "refId1739600227612",
                            "icon": "icon-save",
                        },
                        {
                            "name": "Save Variable",
                            "description": "",
                            "properties": {
                                "description": "contactConfirmed",
                                "rightExpression": "false",
                                "variableName": "contactConfirmed",
                                "asObject": True,
                                "dlpOption": False,
                                "wfmOption": False,
                                "dashboard": False,
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                            },
                            "type": "savevariable",
                            "_selected": False,
                            "id": "refId1739600227613",
                            "icon": "icon-save",
                        },
                        {
                            "icon": "icon-save",
                            "name": "Save Variable",
                            "description": "",
                            "properties": {
                                "description": "phone (Chat)",
                                "rightExpression": "workitem.data.context.consumerData.phone",
                                "variableName": "phone",
                                "asObject": False,
                                "dlpOption": False,
                                "wfmOption": False,
                                "dashboard": False,
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.type",
                                            "operator": "==",
                                            "rightExpression": "'Chat'",
                                        }
                                    ],
                                },
                            },
                            "type": "savevariable",
                            "_selected": False,
                            "id": "refId1741893969929",
                        },
                        {
                            "name": "Save Variable",
                            "description": "",
                            "properties": {
                                "description": "phone (InboundCall or InboundSMS)",
                                "rightExpression": "workitem.from.slice(-10)",
                                "variableName": "phone",
                                "asObject": False,
                                "dlpOption": False,
                                "wfmOption": False,
                                "dashboard": False,
                                "condition": {
                                    "conditionType": "OR",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.type",
                                            "operator": "==",
                                            "rightExpression": "'InboundCall'",
                                        },
                                        {
                                            "leftExpression": "workitem.type",
                                            "operator": "==",
                                            "rightExpression": "'InboundSMS'",
                                        },
                                    ],
                                },
                            },
                            "type": "savevariable",
                            "_selected": False,
                            "id": "refId1741893969877",
                            "icon": "icon-save",
                        },
                        {
                            "name": "Save Variable",
                            "description": "",
                            "properties": {
                                "description": "phone (OutboundCall or OutboundSMS)",
                                "rightExpression": "workitem.to.slice(-10)",
                                "variableName": "phone",
                                "asObject": False,
                                "dlpOption": False,
                                "wfmOption": False,
                                "dashboard": False,
                                "condition": {
                                    "conditionType": "OR",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.type",
                                            "operator": "==",
                                            "rightExpression": "'OutboundCall'",
                                        },
                                        {
                                            "leftExpression": "workitem.type",
                                            "operator": "==",
                                            "rightExpression": "'OutboundSMS'",
                                        },
                                    ],
                                },
                            },
                            "type": "savevariable",
                            "_selected": False,
                            "id": "refId1741893969878",
                            "icon": "icon-save",
                        },
                        {
                            "icon": "icon-save",
                            "name": "Save Variable",
                            "description": "",
                            "properties": {
                                "description": "priority",
                                "rightExpression": "Standard",
                                "variableName": "priority",
                                "asObject": False,
                                "dlpOption": False,
                                "wfmOption": False,
                                "dashboard": False,
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                            },
                            "type": "savevariable",
                            "_selected": False,
                        },
                        {
                            "name": "Save Variable",
                            "description": "",
                            "properties": {
                                "description": "queueId",
                                "rightExpression": queues["Customer Service"],
                                "variableName": "queueId",
                                "asObject": False,
                                "dlpOption": False,
                                "wfmOption": False,
                                "dashboard": False,
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                            },
                            "type": "savevariable",
                            "_selected": False,
                            "icon": "icon-save",
                            "id": "refId1739600227615",
                        },
                        {
                            "name": "Save Variable",
                            "description": "",
                            "properties": {
                                "description": "nextState",
                                "rightExpression": "Webhook",
                                "variableName": "nextState",
                                "asObject": False,
                                "dlpOption": False,
                                "wfmOption": False,
                                "dashboard": False,
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                            },
                            "type": "savevariable",
                            "_selected": False,
                            "icon": "icon-save",
                            "id": "refId1746218700282",
                        },
                        {
                            "name": "Survey",
                            "description": "Transition to another state",
                            "properties": {
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.type",
                                            "operator": "==",
                                            "rightExpression": "'Survey'",
                                        }
                                    ],
                                },
                                "stateName": "Survey",
                                "description": "Transition to another state",
                            },
                            "type": "transitionbyname",
                            "_selected": False,
                            "transitionId": "refId1739600227151",
                            "id": "refId1739600227616",
                            "icon": "icon-transition",
                        },
                        {
                            "icon": "icon-ai-message",
                            "name": "Chat Message Consumer",
                            "description": "Thank you for contacting...",
                            "properties": {
                                "description": "Thank you for contacting...",
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.type",
                                            "operator": "==",
                                            "rightExpression": "'Chat'",
                                        }
                                    ],
                                },
                                "from": "workitem.data.companyName",
                                "message": "Thank you for contacting ${workitem.data.companyName}.",
                                "messageType": "BOT",
                                "options": [],
                            },
                            "type": "chatmessageconsumer",
                            "_selected": False,
                        },
                        {
                            "name": "Search Contacts",
                            "type": "transition",
                            "description": "Transition to another state",
                            "properties": {
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "stateId": "67b11894720280f716c36bdf",
                                "name": "Start",
                                "description": "Transition to another state",
                            },
                            "transitionId": "67b118871e7c034010972864",
                            "_selected": False,
                            "id": "refId1739600227617",
                            "icon": "icon-transition",
                        },
                    ],
                    "transitions": [
                        {"name": "Survey", "id": "refId1739600227151"},
                        {"name": "Search Contacts", "id": "67b118871e7c034010972864"},
                    ],
                    "objectType": "campaignstate",
                    "key": "start-state",
                    "_id": "start-state",
                    "description": "Begin State",
                    "name": "Begin State",
                    "location": "-92.43594451534577 -158.49227385694343",
                },
                "67b11894720280f716c36bdf": {
                    "category": "Standard",
                    "objectType": "campaignstate",
                    "campaignStateId": "67b11894720280f716c36bdf",
                    "name": "Search Contacts",
                    "description": "Newly Created State",
                    "actions": [
                        {
                            "name": "Execute Function",
                            "description": "",
                            "properties": {
                                "description": "Search Contacts",
                                "functionId": search_contacts_function["_id"],
                                "functionExpression": "",
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "expansions": {
                                    "functionId": {
                                        "name": search_contacts_function["name"]
                                    }
                                },
                                "_working": False,
                            },
                            "type": "function",
                            "_selected": False,
                            "id": "refId1739600227189",
                            "icon": "icon-function",
                        },
                        {
                            "name": "Chat",
                            "description": "Transition to another state",
                            "properties": {
                                "description": "Transition to another state",
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.type",
                                            "operator": "==",
                                            "rightExpression": "'Chat'",
                                        }
                                    ],
                                },
                                "stateId": "67b11b3a4492457796ee0690",
                            },
                            "type": "transition",
                            "_selected": False,
                            "transitionId": "refId1739600227187",
                            "icon": "icon-transition",
                            "id": "refId1739600227190",
                        },
                        {
                            "name": "InboundCall",
                            "description": "Transition to another state",
                            "properties": {
                                "description": "Transition to another state",
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.type",
                                            "operator": "==",
                                            "rightExpression": "'InboundCall'",
                                        }
                                    ],
                                },
                                "stateId": "67b11b424881f97a86b2640f",
                            },
                            "type": "transition",
                            "_selected": False,
                            "transitionId": "refId1739600227163",
                            "id": "refId1739600227191",
                            "icon": "icon-transition",
                        },
                        {
                            "icon": "icon-transition",
                            "name": "InboundSMS",
                            "description": "Transition to another state",
                            "properties": {
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.type",
                                            "operator": "==",
                                            "rightExpression": "'InboundSMS'",
                                        }
                                    ],
                                },
                                "stateId": "67b11b4990b64c67bfb0e882",
                            },
                            "type": "transition",
                            "_selected": False,
                            "transitionId": "refId1739600227203",
                        },
                        {
                            "icon": "icon-transition",
                            "name": "Email",
                            "description": "Transition to another state",
                            "properties": {
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.type",
                                            "operator": "==",
                                            "rightExpression": "'Email'",
                                        }
                                    ],
                                },
                                "stateId": "67bea3b642b196ca21fb0623",
                            },
                            "type": "transition",
                            "_selected": False,
                            "transitionId": "refId1740544930914",
                        },
                    ],
                    "_id": "67b11894720280f716c36bdf",
                    "key": "67b11894720280f716c36bdf",
                    "location": "235.689872021094 86.58930650937515",
                    "transitions": [
                        {"name": "Chat", "id": "refId1739600227187"},
                        {"name": "InboundCall", "id": "refId1739600227163"},
                        {"name": "InboundSMS", "id": "refId1739600227203"},
                        {"name": "Email", "id": "refId1740544930914"},
                    ],
                },
                "67b11b35410f937347fe9aee": {
                    "category": "Standard",
                    "objectType": "campaignstate",
                    "campaignStateId": "67b11b35410f937347fe9aee",
                    "name": "Survey",
                    "description": "Newly Created State",
                    "actions": [
                        {
                            "icon": "icon-transition",
                            "name": "End State",
                            "description": "Transition to another state",
                            "properties": {
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "stateName": "End State",
                            },
                            "type": "transitionbyname",
                            "_selected": False,
                            "transitionId": "refId1739600226811",
                        }
                    ],
                    "_id": "67b11b35410f937347fe9aee",
                    "key": "67b11b35410f937347fe9aee",
                    "location": "626.610300152467 -88.1600651150722",
                    "transitions": [{"name": "End State", "id": "refId1739600226811"}],
                },
                "67b11b3a4492457796ee0690": {
                    "category": "Standard",
                    "objectType": "campaignstate",
                    "campaignStateId": "67b11b3a4492457796ee0690",
                    "name": "Chat",
                    "description": "Newly Created State",
                    "actions": [
                        {
                            "icon": "icon-ai-message",
                            "name": "Chat Message Consumer",
                            "description": "",
                            "properties": {
                                "description": "In a few words...",
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "from": "workitem.data.companyName",
                                "message": "In a few words, what can I help you with today?",
                                "messageType": "BOT",
                                "options": [],
                            },
                            "type": "chatmessageconsumer",
                            "_selected": False,
                        },
                        {
                            "icon": "icon-transition",
                            "name": "Chat IVA",
                            "description": "Transition to another state",
                            "properties": {
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "stateName": "Chat IVA",
                            },
                            "type": "transitionbyname",
                            "_selected": False,
                            "transitionId": "refId1758064484666",
                        },
                    ],
                    "_id": "67b11b3a4492457796ee0690",
                    "key": "67b11b3a4492457796ee0690",
                    "location": "631.1006997298108 221.82400319465438",
                    "transitions": [{"name": "Chat IVA", "id": "refId1758064484666"}],
                },
                "67b11b424881f97a86b2640f": {
                    "category": "Standard",
                    "objectType": "campaignstate",
                    "campaignStateId": "67b11b424881f97a86b2640f",
                    "name": "InboundCall",
                    "description": "Newly Created State",
                    "actions": [
                        {
                            "icon": "icon-dialogflow",
                            "name": "Transfer to Dialogflow",
                            "description": "",
                            "properties": {
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                }
                            },
                            "type": "transfertodialogflow",
                            "_selected": False,
                        },
                        {
                            "icon": "icon-transition",
                            "name": "Webhook",
                            "description": "Transition to another state",
                            "properties": {
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "stateId": "67b11bac9255944444f52b95",
                            },
                            "type": "transition",
                            "_selected": False,
                            "transitionId": "refId1739600226869",
                        },
                    ],
                    "_id": "67b11b424881f97a86b2640f",
                    "key": "67b11b424881f97a86b2640f",
                    "location": "629.7129565844244 412.9189486459884",
                    "transitions": [{"name": "Webhook", "id": "refId1739600226869"}],
                },
                "67b11b4990b64c67bfb0e882": {
                    "category": "Standard",
                    "objectType": "campaignstate",
                    "campaignStateId": "67b11b4990b64c67bfb0e882",
                    "name": "InboundSMS",
                    "description": "Newly Created State",
                    "actions": [
                        {
                            "icon": "icon-save",
                            "name": "Save Variable",
                            "description": "",
                            "properties": {
                                "description": "smsCounter",
                                "rightExpression": "1",
                                "variableName": "smsCounter",
                                "asObject": True,
                                "dlpOption": False,
                                "wfmOption": False,
                                "dashboard": False,
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                            },
                            "type": "savevariable",
                            "_selected": False,
                        },
                        {
                            "name": "SMS IVA",
                            "description": "Transition to another state",
                            "properties": {
                                "description": "Transition to another state",
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "stateName": "SMS IVA",
                            },
                            "type": "transitionbyname",
                            "_selected": False,
                            "transitionId": "refId1758064484803",
                            "icon": "icon-transition",
                            "id": "refId1758064484806",
                        },
                    ],
                    "_id": "67b11b4990b64c67bfb0e882",
                    "key": "67b11b4990b64c67bfb0e882",
                    "location": "631.2642848004031 588.219037051561",
                    "transitions": [{"name": "SMS IVA", "id": "refId1758064484803"}],
                },
                "67b11bac9255944444f52b95": {
                    "category": "Standard",
                    "objectType": "campaignstate",
                    "campaignStateId": "67b11bac9255944444f52b95",
                    "name": "Webhook",
                    "description": "Newly Created State",
                    "actions": [
                        {
                            "name": "Wait for messages",
                            "description": "",
                            "properties": {
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                }
                            },
                            "type": "waitforbot",
                            "_selected": False,
                            "id": "refId1739600228047",
                            "icon": "icon-ai-message",
                        },
                        {
                            "name": "Tag Value",
                            "description": "Transition to another state",
                            "properties": {
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [
                                        {
                                            "leftExpression": "",
                                            "operator": "!=",
                                            "rightExpression": "",
                                        }
                                    ],
                                },
                                "stateName": "workitem.data.botWebhookRequest.fulfillmentInfo.tag",
                                "description": "Transition to another state",
                            },
                            "type": "transitionbyname",
                            "_selected": False,
                            "transitionId": "68cafbf349abe8246b1000f2",
                            "id": "refId1758127572229",
                            "icon": "icon-transition",
                        },
                    ],
                    "_id": "67b11bac9255944444f52b95",
                    "key": "67b11bac9255944444f52b95",
                    "location": "1095.232082041558 763.2564039101042",
                    "transitions": [
                        {"name": "InboundCall Action", "id": "refId1739600228115"},
                    ],
                },
                "67b11daace899acb3e0d1c38": {
                    "category": "Standard",
                    "objectType": "campaignstate",
                    "campaignStateId": "67b11daace899acb3e0d1c38",
                    "name": "ConnectAgent",
                    "description": "Newly Created State",
                    "actions": [
                        {
                            "icon": "icon-timer",
                            "name": "Start Timer",
                            "description": "",
                            "properties": {
                                "timeoutInSeconds": "3",
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.type",
                                            "operator": "==",
                                            "rightExpression": "'InboundCall'",
                                        }
                                    ],
                                },
                            },
                            "type": "starttimer",
                            "_selected": False,
                        },
                        {
                            "name": "Retrieve the call",
                            "description": "",
                            "properties": {
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.type",
                                            "operator": "==",
                                            "rightExpression": "'InboundCall'",
                                        }
                                    ],
                                }
                            },
                            "type": "dialogflowtakeback",
                            "_selected": False,
                            "icon": "icon-dialogflow",
                            "id": "refId1739600228216",
                        },
                        {
                            "name": "Enter Queue from Expression",
                            "description": "",
                            "properties": {
                                "priorityExpression": "workitem.data.priority",
                                "queueIdsExpression": "workitem.data.queueId",
                                "ringAllEnabled": False,
                                "stickyEnabled": False,
                                "stickyUserType": "5",
                                "stickyDurationToWaitSeconds": 0,
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                            },
                            "type": "enterqueuefromexpression",
                            "_selected": False,
                            "id": "refId1739600228218",
                            "icon": "icon-enterqueues",
                        },
                        {
                            "name": "Execute Function",
                            "description": "",
                            "properties": {
                                "description": "Two way Chat conversation",
                                "functionId": two_way_chat_function["_id"],
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.type",
                                            "operator": "==",
                                            "rightExpression": "'Chat'",
                                        }
                                    ],
                                },
                                "expansions": {
                                    "functionId": {
                                        "name": two_way_chat_function["name"]
                                    }
                                },
                                "_working": False,
                            },
                            "type": "function",
                            "_selected": False,
                            "id": "refId1739600228219",
                            "icon": "icon-function",
                        },
                        {
                            "name": "Execute Function",
                            "description": "",
                            "properties": {
                                "description": "Two way SMS conversation",
                                "functionId": two_way_sms_function["_id"],
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.type",
                                            "operator": "==",
                                            "rightExpression": "'InboundSMS'",
                                        }
                                    ],
                                },
                                "expansions": {
                                    "functionId": {"name": two_way_sms_function["name"]}
                                },
                                "_working": False,
                            },
                            "type": "function",
                            "_selected": False,
                            "id": "refId1739600228220",
                            "icon": "icon-function",
                        },
                        {
                            "name": "HoldQueue",
                            "description": "Transition to another state",
                            "properties": {
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.type",
                                            "operator": "==",
                                            "rightExpression": "'InboundCall'",
                                        }
                                    ],
                                },
                                "stateId": "67b11dbf1fac7db53c1d0210",
                                "description": "Transition to another state",
                                "points": {
                                    "h": True,
                                    "r": [],
                                    "ct": 0,
                                    "__gohashid": 115203,
                                },
                            },
                            "type": "transition",
                            "_selected": False,
                            "transitionId": "refId1739600227355",
                            "id": "refId1739600228221",
                            "icon": "icon-transition",
                        },
                    ],
                    "_id": "67b11daace899acb3e0d1c38",
                    "key": "67b11daace899acb3e0d1c38",
                    "location": "1381.9621588018802 462.6942731551528",
                    "transitions": [{"name": "HoldQueue", "id": "refId1739600227355"}],
                },
                "67b11dbf1fac7db53c1d0210": {
                    "category": "Standard",
                    "objectType": "campaignstate",
                    "campaignStateId": "67b11dbf1fac7db53c1d0210",
                    "name": "HoldQueue",
                    "description": "Newly Created State",
                    "actions": [
                        {
                            "name": "Play & Collect Digits",
                            "description": "",
                            "properties": {
                                "loop": 1,
                                "numberDigits": 1,
                                "promptId": prompt["_id"],
                                "terminationKey": "#",
                                "timeoutInSeconds": "1",
                                "dlpOption": False,
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "operator": "!=",
                                            "leftExpression": "workitem.digits",
                                            "rightExpression": "'1'",
                                        },
                                        {
                                            "leftExpression": "workitem.digits",
                                            "operator": "!=",
                                            "rightExpression": "'2'",
                                        },
                                    ],
                                },
                                "expansions": {"promptId": {"name": prompt["name"]}},
                                "_working": False,
                            },
                            "type": "playdigits",
                            "_selected": False,
                            "id": "refId1740283338201",
                            "icon": "icon-playdigits",
                        },
                        {
                            "name": "Play Collect Google TTS",
                            "description": "Play Collect using Text-To-Speech",
                            "properties": {
                                "voiceName": "en-US-Wavenet-J",
                                "voiceGender": "male",
                                "text": '<prosody pitch="-2st">To leave a voicemail, press 1. To request a callback, press 2. Otherwise, please stay on the line.</prosody>',
                                "numberDigits": 1,
                                "terminationKey": "#",
                                "timeoutInSeconds": "1",
                                "dlpOption": False,
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "operator": "!=",
                                            "leftExpression": "workitem.digits",
                                            "rightExpression": "'1'",
                                        },
                                        {
                                            "leftExpression": "workitem.digits",
                                            "operator": "!=",
                                            "rightExpression": "'2'",
                                        },
                                    ],
                                },
                                "description": "Play Collect using Text-To-Speech",
                            },
                            "type": "googlettscollect",
                            "_selected": False,
                            "id": "refId1758127573071",
                            "icon": "icon-tts",
                        },
                        {
                            "icon": "icon-function",
                            "name": "Execute Function",
                            "description": "",
                            "properties": {
                                "description": "ACD Voicemail (1)",
                                "functionId": acd_voicemail_function["_id"],
                                "functionExpression": "",
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.digits",
                                            "operator": "==",
                                            "rightExpression": "'1'",
                                        }
                                    ],
                                },
                                "expansions": {
                                    "functionId": {
                                        "name": acd_voicemail_function["name"]
                                    }
                                },
                                "_working": False,
                            },
                            "type": "function",
                            "_selected": False,
                        },
                        {
                            "icon": "icon-function",
                            "name": "Execute Function",
                            "description": "",
                            "properties": {
                                "description": "ACD Callback (2)",
                                "functionId": acd_callback_function["_id"],
                                "functionExpression": "",
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.digits",
                                            "operator": "==",
                                            "rightExpression": "'2'",
                                        }
                                    ],
                                },
                                "expansions": {
                                    "functionId": {
                                        "name": acd_callback_function["name"]
                                    }
                                },
                                "_working": False,
                            },
                            "type": "function",
                            "_selected": False,
                            "id": "refId1739600228575",
                        },
                        {
                            "name": "Loop",
                            "description": "Transition to another state",
                            "properties": {
                                "description": "Back to Top",
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "stateName": "HoldQueue",
                            },
                            "type": "transitionbyname",
                            "_selected": False,
                            "transitionId": "refId1739600227365",
                            "icon": "icon-transition",
                            "id": "refId1739600228544",
                        },
                    ],
                    "_id": "67b11dbf1fac7db53c1d0210",
                    "key": "67b11dbf1fac7db53c1d0210",
                    "location": "1710.5859782839211 639.5535706670023",
                    "transitions": [{"name": "Loop", "id": "refId1739600227365"}],
                },
                "67bd02ee8a738c4befeec93a": {
                    "category": "Standard",
                    "objectType": "campaignstate",
                    "campaignStateId": "67bd02ee8a738c4befeec93a",
                    "name": "Goodbye",
                    "description": "Newly Created State",
                    "actions": [
                        {
                            "icon": "icon-ai-message",
                            "name": "Chat Message Consumer",
                            "description": "Thank you for contacting...",
                            "properties": {
                                "description": "Thank you for contacting...",
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.type",
                                            "operator": "==",
                                            "rightExpression": "'Chat'",
                                        }
                                    ],
                                },
                                "from": "workitem.data.companyName",
                                "message": "Thank you for contacting ${workitem.data.companyName} and have a great day!",
                                "messageType": "BOT",
                                "options": [],
                            },
                            "type": "chatmessageconsumer",
                            "_selected": False,
                        },
                        {
                            "name": "Start Timer",
                            "description": "",
                            "properties": {
                                "timeoutInSeconds": 10,
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.type",
                                            "operator": "==",
                                            "rightExpression": "'Chat'",
                                        }
                                    ],
                                },
                                "description": "Chat",
                            },
                            "type": "starttimer",
                            "_selected": False,
                            "id": "refId1758127572757",
                            "icon": "icon-timer",
                        },
                        {
                            "name": "Start Timer",
                            "description": "",
                            "properties": {
                                "timeoutInSeconds": "5",
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.type",
                                            "operator": "==",
                                            "rightExpression": "'InboundCall'",
                                        }
                                    ],
                                },
                                "description": "InboundCall",
                            },
                            "type": "starttimer",
                            "_selected": False,
                            "id": "refId1758127572792",
                            "icon": "icon-timer",
                        },
                        {
                            "name": "End State",
                            "description": "Transition to another state",
                            "properties": {
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "stateName": "End State",
                                "description": "Transition to another state",
                            },
                            "type": "transitionbyname",
                            "_selected": False,
                            "transitionId": "refId1740431837535",
                            "icon": "icon-transition",
                            "id": "refId1740431837551",
                        },
                    ],
                    "_id": "67bd02ee8a738c4befeec93a",
                    "key": "67bd02ee8a738c4befeec93a",
                    "location": "-53.149243957620115 454.07154501420496",
                    "transitions": [{"name": "End State", "id": "refId1740431837535"}],
                },
                "67bea3b642b196ca21fb0623": {
                    "category": "Standard",
                    "objectType": "campaignstate",
                    "campaignStateId": "67bea3b642b196ca21fb0623",
                    "name": "Email",
                    "description": "Newly Created State",
                    "actions": [
                        {
                            "icon": "icon-transition",
                            "name": "ConnectAgent",
                            "description": "Transition to another state",
                            "properties": {
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "stateName": "ConnectAgent",
                            },
                            "type": "transitionbyname",
                            "_selected": False,
                            "transitionId": "refId1740544930881",
                        }
                    ],
                    "_id": "67bea3b642b196ca21fb0623",
                    "key": "67bea3b642b196ca21fb0623",
                    "location": "631.1252797552795 768.2636496590599",
                    "transitions": [
                        {"name": "ConnectAgent", "id": "refId1740544930881"}
                    ],
                },
                "68c9e821c657fd9e2c8e050a": {
                    "category": "Standard",
                    "objectType": "campaignstate",
                    "campaignStateId": "68c9e821c657fd9e2c8e050a",
                    "name": "Chat IVA",
                    "description": "Newly Created State",
                    "actions": [
                        {
                            "name": "Wait Chat Message",
                            "description": "",
                            "properties": {
                                "timeoutDuration": -1,
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                            },
                            "type": "waitforchatmessage",
                            "_selected": False,
                            "id": "refId1758064484670",
                            "icon": "icon-timer",
                        },
                        {
                            "name": "Message Bot",
                            "description": "",
                            "properties": {
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "message": "$V.workitem.currentChatMessage.textMsg",
                            },
                            "type": "chatmessagebot",
                            "_selected": False,
                            "icon": "icon-ai-message",
                            "id": "refId1758064484671",
                        },
                        {
                            "name": "Forward Bot Response",
                            "description": "Forward BOT response to consumer",
                            "properties": {
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "from": "KPMG",
                                "description": "Forward BOT response to consumer",
                            },
                            "type": "chatforwardbotresponseconsumer",
                            "_selected": False,
                            "id": "refId1758672835759",
                            "icon": "icon-mail-forward",
                        },
                        {
                            "name": "nextState",
                            "description": "Transition to another state",
                            "properties": {
                                "description": "Transition to another state",
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.chatBotResponse.parameters.nextState",
                                            "operator": "!=",
                                            "rightExpression": "null",
                                        }
                                    ],
                                },
                                "stateName": "workitem.chatBotResponse.parameters.nextState.string",
                            },
                            "type": "transitionbyname",
                            "_selected": False,
                            "transitionId": "refId1758672834263",
                            "id": "refId1758672835760",
                            "icon": "icon-transition",
                        },
                        {
                            "name": "Loop",
                            "description": "Transition to another state",
                            "properties": {
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "stateName": "Chat IVA",
                                "description": "Transition to another state",
                            },
                            "type": "transitionbyname",
                            "_selected": False,
                            "transitionId": "refId1758064484628",
                            "icon": "icon-transition",
                            "id": "refId1758672835761",
                        },
                    ],
                    "_id": "68c9e821c657fd9e2c8e050a",
                    "key": "68c9e821c657fd9e2c8e050a",
                    "location": "934.8961912870105 156.56394033397495",
                    "transitions": [
                        {"name": "nextState", "id": "refId1758672834263"},
                        {"name": "Loop", "id": "refId1758064484628"},
                    ],
                },
                "68c9f22451feedbeaf70558a": {
                    "category": "Standard",
                    "objectType": "campaignstate",
                    "campaignStateId": "68c9f22451feedbeaf70558a",
                    "name": "SMS IVA",
                    "description": "Newly Created State",
                    "actions": [
                        {
                            "name": "SMS Wait For Messages",
                            "description": "",
                            "properties": {
                                "timeoutDuration": 3600000,
                                "stateId": "67b1186f5510d9081ac8e32b",
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "operator": "!=",
                                            "leftExpression": "workitem.data.smsCounter",
                                            "rightExpression": "1",
                                        }
                                    ],
                                },
                            },
                            "type": "smswaitformessage",
                            "_selected": False,
                            "id": "refId1758672835669",
                            "icon": "icon-timer",
                        },
                        {
                            "name": "Message Bot",
                            "description": "",
                            "properties": {
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "message": "$V.workitem.currentSMSMessage.textMsg",
                                "event": "",
                            },
                            "type": "chatmessagebot",
                            "_selected": False,
                            "id": "refId1758672835670",
                            "icon": "icon-ai-message",
                        },
                        {
                            "name": "Forward Bot Message to Consumer",
                            "description": "",
                            "properties": {
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                }
                            },
                            "type": "smsforwardbotmessagetoconsumer",
                            "_selected": False,
                            "icon": "icon-mail-forward",
                            "id": "refId1758672835671",
                        },
                        {
                            "name": "Save Variable",
                            "description": "",
                            "properties": {
                                "description": "smsCounter",
                                "rightExpression": "workitem.data.smsCounter + 1",
                                "variableName": "smsCounter",
                                "asObject": True,
                                "dlpOption": False,
                                "wfmOption": False,
                                "dashboard": False,
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                            },
                            "type": "savevariable",
                            "_selected": False,
                            "icon": "icon-save",
                            "id": "refId1758672835672",
                        },
                        {
                            "name": "nextState",
                            "description": "Transition to another state",
                            "properties": {
                                "description": "Transition to another state",
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.chatBotResponse.parameters.nextState",
                                            "operator": "!=",
                                            "rightExpression": "null",
                                        }
                                    ],
                                },
                                "stateName": "workitem.chatBotResponse.parameters.nextState.string",
                            },
                            "type": "transitionbyname",
                            "_selected": False,
                            "transitionId": "68c9f2e28c19a30ac822e07e",
                            "id": "refId1758672835673",
                            "icon": "icon-transition",
                        },
                        {
                            "name": "Loop",
                            "description": "Transition to another state",
                            "properties": {
                                "description": "Transition to another state",
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [
                                        {
                                            "leftExpression": "\\",
                                            "operator": "!=",
                                            "rightExpression": "'FollowUp'",
                                        }
                                    ],
                                },
                                "stateName": "SMS IVA",
                            },
                            "type": "transitionbyname",
                            "_selected": False,
                            "transitionId": "refId1758064484728",
                            "id": "refId1758064484913",
                            "icon": "icon-transition",
                        },
                    ],
                    "_id": "68c9f22451feedbeaf70558a",
                    "key": "68c9f22451feedbeaf70558a",
                    "location": "1159.2325174108068 156.51594302040465",
                    "transitions": [
                        {"name": "nextState", "id": "68c9f2e28c19a30ac822e07e"},
                        {"name": "Loop", "id": "refId1758064484728"},
                    ],
                },
            },
            "finalWorkitemStateId": "67b1186f5510d9081ac8e32b",
            "finalUserStateId": "67b1186f5510d9081ac8e32b",
            "name": workflow_name,
            "description": "IVA workflow",
        }
    )
    headers = {
        "Authorization": ncc_token,
        "Content-Type": "application/json",
    }
    try:
        conn.request("POST", "/data/api/types/workflow/", payload, headers)
        res = conn.getresponse()
        if res.status == 201:
            data = res.read().decode("utf-8")
            workflow = json.loads(data)
    except:
        pass
    conn.close()
    return workflow


def create_non_iva_dtmf_workflow(
    ncc_location: str,
    ncc_token: str,
    workflow_name: str,
    business_name: str,
    queues: dict,
    search_contacts_function: dict,
    two_way_chat_function: dict,
    two_way_sms_function: dict,
    prompt: dict,
    acd_voicemail_function: dict,
    acd_callback_function: dict,
    chat_survey: dict,
    user_survey: dict,
    vertical: str,
) -> dict:
    """
    This function creates a workflow in Nextiva Contact Center (NCC) that uses a DTMF menu.
    """
    workflow = {}
    conn = http.client.HTTPSConnection(ncc_location)
    workflow_body = {
        "maxActions": 10000,
        "localizations": {
            "name": {"en": {"language": "en", "value": workflow_name}},
            "description": {
                "en": {"language": "en", "value": "Non-IVA, DTMF workflow"}
            },
        },
        "description": "Non-IVA, DTMF workflow",
        "states": {
            "67b1186f5510d9081ac8e32b": {
                "category": "Standard",
                "campaignStateId": "67b1186f5510d9081ac8e32b",
                "actions": [
                    {
                        "name": "ACD Voicemail From Expression",
                        "description": "Create ACD Voicemail",
                        "properties": {
                            "transcription": True,
                            "priority": 3,
                            "queueIdsExpression": "workitem.data.queueId",
                            "toAddress": "",
                            "condition": {
                                "conditionType": "AND",
                                "expressions": [
                                    {
                                        "operator": "==",
                                        "leftExpression": "workitem.data.messageRecorded",
                                        "rightExpression": "1",
                                    }
                                ],
                            },
                            "description": "Create ACD Voicemail",
                        },
                        "type": "acdvmfromexpression",
                        "_selected": False,
                        "id": "refId1723818900554",
                        "icon": "icon-directconnect",
                    },
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
                    },
                ],
                "objectType": "campaignstate",
                "key": "67b1186f5510d9081ac8e32b",
                "_id": "67b1186f5510d9081ac8e32b",
                "description": "End State",
                "name": "End State",
                "location": "-147.23017129888294 34.91808770109185",
                "transitions": [],
            },
            "start-state": {
                "category": "Begin",
                "campaignStateId": "start-state",
                "actions": [
                    {
                        "name": "Save Variable",
                        "description": "",
                        "properties": {
                            "description": "companyName",
                            "rightExpression": business_name,
                            "variableName": "companyName",
                            "asObject": False,
                            "dlpOption": False,
                            "wfmOption": False,
                            "dashboard": False,
                            "condition": {
                                "conditionType": "NONE",
                                "expressions": [{"operator": "=="}],
                            },
                        },
                        "type": "savevariable",
                        "_selected": False,
                        "id": "refId1739934453997",
                        "icon": "icon-save",
                    },
                    {
                        "icon": "icon-save",
                        "name": "Save Variable",
                        "description": "",
                        "properties": {
                            "description": "sourceLanguage",
                            "rightExpression": "en",
                            "variableName": "sourceLanguage",
                            "asObject": False,
                            "dlpOption": False,
                            "wfmOption": False,
                            "dashboard": False,
                            "condition": {
                                "conditionType": "NONE",
                                "expressions": [{"operator": "=="}],
                            },
                        },
                        "type": "savevariable",
                        "_selected": False,
                    },
                    {
                        "name": "Save Variable",
                        "description": "",
                        "properties": {
                            "description": "contactFound",
                            "rightExpression": "false",
                            "variableName": "contactFound",
                            "asObject": True,
                            "dlpOption": False,
                            "wfmOption": False,
                            "dashboard": False,
                            "condition": {
                                "conditionType": "NONE",
                                "expressions": [{"operator": "=="}],
                            },
                        },
                        "type": "savevariable",
                        "_selected": False,
                        "id": "refId1739934453998",
                        "icon": "icon-save",
                    },
                    {
                        "name": "Save Variable",
                        "description": "",
                        "properties": {
                            "description": "contactConfirmed",
                            "rightExpression": "false",
                            "variableName": "contactConfirmed",
                            "asObject": True,
                            "dlpOption": False,
                            "wfmOption": False,
                            "dashboard": False,
                            "condition": {
                                "conditionType": "NONE",
                                "expressions": [{"operator": "=="}],
                            },
                        },
                        "type": "savevariable",
                        "_selected": False,
                        "id": "refId1739934453999",
                        "icon": "icon-save",
                    },
                    {
                        "icon": "icon-save",
                        "name": "Save Variable",
                        "description": "",
                        "properties": {
                            "description": "phone (Chat)",
                            "rightExpression": "workitem.data.context.consumerData.phone",
                            "variableName": "phone",
                            "asObject": False,
                            "dlpOption": False,
                            "wfmOption": False,
                            "dashboard": False,
                            "condition": {
                                "conditionType": "AND",
                                "expressions": [
                                    {
                                        "leftExpression": "workitem.type",
                                        "operator": "==",
                                        "rightExpression": "'Chat'",
                                    }
                                ],
                            },
                        },
                        "type": "savevariable",
                        "_selected": False,
                        "id": "refId1741893969929",
                    },
                    {
                        "name": "Save Variable",
                        "description": "",
                        "properties": {
                            "description": "phone (InboundCall or InboundSMS)",
                            "rightExpression": "workitem.from.slice(-10)",
                            "variableName": "phone",
                            "asObject": False,
                            "dlpOption": False,
                            "wfmOption": False,
                            "dashboard": False,
                            "condition": {
                                "conditionType": "OR",
                                "expressions": [
                                    {
                                        "leftExpression": "workitem.type",
                                        "operator": "==",
                                        "rightExpression": "'InboundCall'",
                                    },
                                    {
                                        "leftExpression": "workitem.type",
                                        "operator": "==",
                                        "rightExpression": "'InboundSMS'",
                                    },
                                ],
                            },
                        },
                        "type": "savevariable",
                        "_selected": False,
                        "id": "refId1741893969877",
                        "icon": "icon-save",
                    },
                    {
                        "name": "Save Variable",
                        "description": "",
                        "properties": {
                            "description": "phone (OutboundCall or OutboundSMS)",
                            "rightExpression": "workitem.to.slice(-10)",
                            "variableName": "phone",
                            "asObject": False,
                            "dlpOption": False,
                            "wfmOption": False,
                            "dashboard": False,
                            "condition": {
                                "conditionType": "OR",
                                "expressions": [
                                    {
                                        "leftExpression": "workitem.type",
                                        "operator": "==",
                                        "rightExpression": "'OutboundCall'",
                                    },
                                    {
                                        "leftExpression": "workitem.type",
                                        "operator": "==",
                                        "rightExpression": "'OutboundSMS'",
                                    },
                                ],
                            },
                        },
                        "type": "savevariable",
                        "_selected": False,
                        "id": "refId1741893969878",
                        "icon": "icon-save",
                    },
                    {
                        "name": "Save Variable",
                        "description": "",
                        "properties": {
                            "description": "priority",
                            "rightExpression": "Standard",
                            "variableName": "priority",
                            "asObject": False,
                            "dlpOption": False,
                            "wfmOption": False,
                            "dashboard": False,
                            "condition": {
                                "conditionType": "NONE",
                                "expressions": [{"operator": "=="}],
                            },
                        },
                        "type": "savevariable",
                        "_selected": False,
                        "id": "refId1739934454001",
                        "icon": "icon-save",
                    },
                    {
                        "name": "Save Variable",
                        "description": "",
                        "properties": {
                            "description": "queueId",
                            "rightExpression": queues["Customer Service"],
                            "variableName": "queueId",
                            "asObject": False,
                            "dlpOption": False,
                            "wfmOption": False,
                            "dashboard": False,
                            "condition": {
                                "conditionType": "NONE",
                                "expressions": [{"operator": "=="}],
                            },
                        },
                        "type": "savevariable",
                        "_selected": False,
                        "id": "refId1739934454002",
                        "icon": "icon-save",
                    },
                    {
                        "name": "Survey",
                        "description": "Transition to another state",
                        "properties": {
                            "condition": {
                                "conditionType": "AND",
                                "expressions": [
                                    {
                                        "leftExpression": "workitem.type",
                                        "operator": "==",
                                        "rightExpression": "'Survey'",
                                    }
                                ],
                            },
                            "stateName": "Survey",
                            "description": "Transition to another state",
                        },
                        "type": "transitionbyname",
                        "_selected": False,
                        "transitionId": "refId1739600227151",
                        "id": "refId1739934454003",
                        "icon": "icon-transition",
                    },
                    {
                        "icon": "icon-ai-message",
                        "name": "Chat Message Consumer",
                        "description": "Thank you for contacting...",
                        "properties": {
                            "description": "Thank you for contacting...",
                            "condition": {
                                "conditionType": "AND",
                                "expressions": [
                                    {
                                        "leftExpression": "workitem.type",
                                        "operator": "==",
                                        "rightExpression": "'Chat'",
                                    }
                                ],
                            },
                            "from": "workitem.data.companyName",
                            "message": "Thank you for contacting ${workitem.data.companyName}.",
                            "messageType": "BOT",
                            "options": [],
                        },
                        "type": "chatmessageconsumer",
                        "_selected": False,
                    },
                    {
                        "icon": "icon-tts",
                        "name": "Synthesize Text via Google TTS",
                        "description": "Thank you for contacting...",
                        "properties": {
                            "description": "Thank you for contacting...",
                            "voiceName": "en-US-Wavenet-J",
                            "text": '<prosody pitch="-2st">Thank you for contacting ${workitem.data.companyName}.</prosody>',
                            "condition": {
                                "conditionType": "AND",
                                "expressions": [
                                    {
                                        "leftExpression": "workitem.type",
                                        "operator": "==",
                                        "rightExpression": "'InboundCall'",
                                    }
                                ],
                            },
                        },
                        "type": "googletts",
                        "_selected": False,
                    },
                    {
                        "name": "Search Contacts",
                        "type": "transition",
                        "description": "Transition to another state",
                        "properties": {
                            "condition": {
                                "conditionType": "NONE",
                                "expressions": [{"operator": "=="}],
                            },
                            "stateId": "67b11894720280f716c36bdf",
                            "name": "Start",
                            "description": "Transition to another state",
                        },
                        "transitionId": "67b118871e7c034010972864",
                        "_selected": False,
                        "id": "refId1739934454005",
                        "icon": "icon-transition",
                    },
                ],
                "transitions": [
                    {"name": "Survey", "id": "refId1739600227151"},
                    {"name": "Search Contacts", "id": "67b118871e7c034010972864"},
                ],
                "objectType": "campaignstate",
                "key": "start-state",
                "_id": "start-state",
                "description": "Begin State",
                "name": "Begin State",
                "location": "-103.83820690278785 -186.18348251215994",
            },
            "67b11894720280f716c36bdf": {
                "category": "Standard",
                "objectType": "campaignstate",
                "campaignStateId": "67b11894720280f716c36bdf",
                "name": "Search Contacts",
                "description": "Newly Created State",
                "actions": [
                    {
                        "name": "Execute Function",
                        "description": "",
                        "properties": {
                            "description": "Search Contacts",
                            "functionId": search_contacts_function["_id"],
                            "functionExpression": "",
                            "condition": {
                                "conditionType": "NONE",
                                "expressions": [{"operator": "=="}],
                            },
                            "expansions": {
                                "functionId": {"name": search_contacts_function["name"]}
                            },
                            "_working": False,
                        },
                        "type": "function",
                        "_selected": False,
                        "id": "refId1739934453972",
                        "icon": "icon-function",
                    },
                    {
                        "name": "Chat",
                        "description": "Transition to another state",
                        "properties": {
                            "description": "Transition to another state",
                            "condition": {
                                "conditionType": "AND",
                                "expressions": [
                                    {
                                        "leftExpression": "workitem.type",
                                        "operator": "==",
                                        "rightExpression": "'Chat'",
                                    }
                                ],
                            },
                            "stateId": "67b11b3a4492457796ee0690",
                        },
                        "type": "transition",
                        "_selected": False,
                        "transitionId": "refId1739600227187",
                        "id": "refId1739934453973",
                        "icon": "icon-transition",
                    },
                    {
                        "name": "InboundCall",
                        "description": "Transition to another state",
                        "properties": {
                            "description": "Transition to another state",
                            "condition": {
                                "conditionType": "AND",
                                "expressions": [
                                    {
                                        "leftExpression": "workitem.type",
                                        "operator": "==",
                                        "rightExpression": "'InboundCall'",
                                    }
                                ],
                            },
                            "stateId": "67b11b424881f97a86b2640f",
                        },
                        "type": "transition",
                        "_selected": False,
                        "transitionId": "refId1739600227163",
                        "id": "refId1739934453974",
                        "icon": "icon-transition",
                    },
                    {
                        "name": "InboundSMS",
                        "description": "Transition to another state",
                        "properties": {
                            "condition": {
                                "conditionType": "AND",
                                "expressions": [
                                    {
                                        "leftExpression": "workitem.type",
                                        "operator": "==",
                                        "rightExpression": "'InboundSMS'",
                                    }
                                ],
                            },
                            "stateId": "67b11b4990b64c67bfb0e882",
                            "description": "Transition to another state",
                        },
                        "type": "transition",
                        "_selected": False,
                        "transitionId": "refId1739600227203",
                        "id": "refId1739934453975",
                        "icon": "icon-transition",
                    },
                    {
                        "icon": "icon-transition",
                        "name": "OutboundCall",
                        "description": "Transition to another state",
                        "properties": {
                            "condition": {
                                "conditionType": "AND",
                                "expressions": [
                                    {
                                        "leftExpression": "workitem.type",
                                        "operator": "==",
                                        "rightExpression": "'OutboundCall'",
                                    }
                                ],
                            },
                            "stateId": "67b552f294171b486a3d1b7a",
                        },
                        "type": "transition",
                        "_selected": False,
                        "transitionId": "refId1739934453995",
                    },
                    {
                        "icon": "icon-transition",
                        "name": "Email",
                        "description": "Transition to another state",
                        "properties": {
                            "condition": {
                                "conditionType": "AND",
                                "expressions": [
                                    {
                                        "leftExpression": "workitem.type",
                                        "operator": "==",
                                        "rightExpression": "'Email'",
                                    }
                                ],
                            },
                            "stateId": "67bea5bba2c3472a0f1cfba2",
                        },
                        "type": "transition",
                        "_selected": False,
                        "transitionId": "refId1740544930979",
                    },
                ],
                "_id": "67b11894720280f716c36bdf",
                "key": "67b11894720280f716c36bdf",
                "location": "165.88010230206072 74.17868078154703",
                "transitions": [
                    {"name": "Chat", "id": "refId1739600227187"},
                    {"name": "InboundCall", "id": "refId1739600227163"},
                    {"name": "InboundSMS", "id": "refId1739600227203"},
                    {"name": "OutboundCall", "id": "refId1739934453995"},
                    {"name": "Email", "id": "refId1740544930979"},
                ],
            },
            "67b11b35410f937347fe9aee": {
                "category": "Standard",
                "objectType": "campaignstate",
                "campaignStateId": "67b11b35410f937347fe9aee",
                "name": "Survey",
                "description": "Newly Created State",
                "actions": [
                    {
                        "icon": "icon-transition",
                        "name": "End State",
                        "description": "Transition to another state",
                        "properties": {
                            "condition": {
                                "conditionType": "NONE",
                                "expressions": [{"operator": "=="}],
                            },
                            "stateName": "End State",
                        },
                        "type": "transitionbyname",
                        "_selected": False,
                        "transitionId": "refId1739600226811",
                    }
                ],
                "_id": "67b11b35410f937347fe9aee",
                "key": "67b11b35410f937347fe9aee",
                "location": "484.89646762282933 -76.7578027276301",
                "transitions": [{"name": "End State", "id": "refId1739600226811"}],
            },
            "67b11b3a4492457796ee0690": {
                "category": "Standard",
                "objectType": "campaignstate",
                "campaignStateId": "67b11b3a4492457796ee0690",
                "name": "Chat",
                "description": "Newly Created State",
                "actions": [
                    {
                        "icon": "icon-save",
                        "name": "Save Variable",
                        "description": "",
                        "properties": {
                            "description": "interest",
                            "rightExpression": "workitem.data.context.consumerData.interest",
                            "variableName": "interest",
                            "asObject": False,
                            "dlpOption": False,
                            "wfmOption": False,
                            "dashboard": False,
                            "condition": {
                                "conditionType": "NONE",
                                "expressions": [{"operator": "=="}],
                            },
                        },
                        "type": "savevariable",
                        "_selected": False,
                    },
                    {
                        "name": "ConnectAgent",
                        "description": "Transition to another state",
                        "properties": {
                            "condition": {
                                "conditionType": "NONE",
                                "expressions": [{"operator": "=="}],
                            },
                            "stateId": "67b11daace899acb3e0d1c38",
                            "description": "Transition to another state",
                        },
                        "type": "transition",
                        "_selected": False,
                        "transitionId": "refId1739600226839",
                        "id": "refId1739600229946",
                        "icon": "icon-transition",
                    },
                ],
                "_id": "67b11b3a4492457796ee0690",
                "key": "67b11b3a4492457796ee0690",
                "location": "480.78544785048666 214.34893700073843",
                "transitions": [{"name": "ConnectAgent", "id": "refId1739600226839"}],
            },
            "67b11b424881f97a86b2640f": {
                "category": "Standard",
                "objectType": "campaignstate",
                "campaignStateId": "67b11b424881f97a86b2640f",
                "name": "InboundCall",
                "description": "Newly Created State",
                "actions": [
                    {
                        "icon": "icon-tts",
                        "name": "Play Collect Google TTS",
                        "description": "DTMF menu",
                        "properties": {
                            "description": "DTMF menu",
                            "voiceName": "en-US-Wavenet-J",
                            "voiceGender": "male",
                            "text": "",
                            "numberDigits": 1,
                            "terminationKey": "#",
                            "timeoutInSeconds": "3",
                            "dlpOption": False,
                            "condition": {
                                "conditionType": "NONE",
                                "expressions": [{"operator": "=="}],
                            },
                        },
                        "type": "googlettscollect",
                        "_selected": False,
                    },
                    {
                        "name": "ConnectAgent",
                        "description": "Transition to another state",
                        "properties": {
                            "condition": {
                                "conditionType": "NONE",
                                "expressions": [{"operator": "=="}],
                            },
                            "stateId": "67b11daace899acb3e0d1c38",
                            "description": "Transition to another state",
                        },
                        "type": "transition",
                        "_selected": False,
                        "transitionId": "refId1739600226869",
                        "id": "refId1739600231292",
                        "icon": "icon-transition",
                    },
                ],
                "_id": "67b11b424881f97a86b2640f",
                "key": "67b11b424881f97a86b2640f",
                "location": "476.13146320255123 409.81629221403136",
                "transitions": [{"name": "ConnectAgent", "id": "refId1739600226869"}],
            },
            "67b11b4990b64c67bfb0e882": {
                "category": "Standard",
                "objectType": "campaignstate",
                "campaignStateId": "67b11b4990b64c67bfb0e882",
                "name": "InboundSMS",
                "description": "Newly Created State",
                "actions": [
                    {
                        "icon": "icon-transition",
                        "name": "ConnectAgent",
                        "description": "Transition to another state",
                        "properties": {
                            "condition": {
                                "conditionType": "NONE",
                                "expressions": [{"operator": "=="}],
                            },
                            "stateId": "67b11daace899acb3e0d1c38",
                        },
                        "type": "transition",
                        "_selected": False,
                        "transitionId": "refId1739600229655",
                    }
                ],
                "_id": "67b11b4990b64c67bfb0e882",
                "key": "67b11b4990b64c67bfb0e882",
                "location": "471.4774785546159 591.3216934835181",
                "transitions": [{"name": "ConnectAgent", "id": "refId1739600229655"}],
            },
            "67b11daace899acb3e0d1c38": {
                "category": "Standard",
                "objectType": "campaignstate",
                "campaignStateId": "67b11daace899acb3e0d1c38",
                "name": "ConnectAgent",
                "description": "Newly Created State",
                "actions": [
                    {
                        "name": "Chat Message Consumer",
                        "description": "",
                        "properties": {
                            "description": "Please wait...",
                            "condition": {
                                "conditionType": "AND",
                                "expressions": [
                                    {
                                        "leftExpression": "workitem.type",
                                        "operator": "==",
                                        "rightExpression": "'Chat'",
                                    }
                                ],
                            },
                            "from": "workitem.data.companyName",
                            "message": "Please wait while I transfer you to an agent who can assist you.",
                            "messageType": "BOT",
                            "options": [],
                        },
                        "type": "chatmessageconsumer",
                        "_selected": False,
                        "icon": "icon-ai-message",
                        "id": "refId1739600229770",
                    },
                    {
                        "name": "SMS Message Consumer",
                        "description": "",
                        "properties": {
                            "description": "Please wait...",
                            "message": "Please wait while I transfer you to an agent who can assist you.",
                            "toAddress": "workitem.from",
                            "fromAddress": "workitem.to",
                            "createNewWorkitem": False,
                            "condition": {
                                "conditionType": "AND",
                                "expressions": [
                                    {
                                        "leftExpression": "workitem.type",
                                        "operator": "==",
                                        "rightExpression": "'InboundSMS'",
                                    }
                                ],
                            },
                        },
                        "type": "smsmessageconsumer",
                        "_selected": False,
                        "icon": "icon-ai-message",
                        "id": "refId1739600229771",
                    },
                    {
                        "name": "Synthesize Text via Google TTS",
                        "description": "Convert Text into Audio using Google's Text-To-Speech",
                        "properties": {
                            "voiceName": "en-US-Wavenet-J",
                            "text": '<prosody pitch="-2st">Please wait while I transfer you to an agent who can assist you.</prosody>',
                            "condition": {
                                "conditionType": "AND",
                                "expressions": [
                                    {
                                        "leftExpression": "workitem.type",
                                        "operator": "==",
                                        "rightExpression": "'InboundCall'",
                                    }
                                ],
                            },
                            "description": "Please wait...",
                        },
                        "type": "googletts",
                        "_selected": False,
                        "id": "refId1739600229773",
                        "icon": "icon-tts",
                    },
                    {
                        "name": "Enter Queue from Expression",
                        "description": "",
                        "properties": {
                            "priorityExpression": "workitem.data.priority",
                            "queueIdsExpression": "workitem.data.queueId",
                            "ringAllEnabled": False,
                            "stickyEnabled": False,
                            "stickyUserType": "5",
                            "stickyDurationToWaitSeconds": 0,
                            "condition": {
                                "conditionType": "NONE",
                                "expressions": [{"operator": "=="}],
                            },
                        },
                        "type": "enterqueuefromexpression",
                        "_selected": False,
                        "id": "refId1739600229774",
                        "icon": "icon-enterqueues",
                    },
                    {
                        "name": "Execute Function",
                        "description": "",
                        "properties": {
                            "description": "Two way Chat conversation",
                            "functionId": two_way_chat_function["_id"],
                            "condition": {
                                "conditionType": "AND",
                                "expressions": [
                                    {
                                        "leftExpression": "workitem.type",
                                        "operator": "==",
                                        "rightExpression": "'Chat'",
                                    }
                                ],
                            },
                            "expansions": {
                                "functionId": {"name": two_way_chat_function["name"]}
                            },
                            "_working": False,
                        },
                        "type": "function",
                        "_selected": False,
                        "id": "refId1739600229775",
                        "icon": "icon-function",
                    },
                    {
                        "name": "Execute Function",
                        "description": "",
                        "properties": {
                            "description": "Two way SMS conversation",
                            "functionId": two_way_sms_function["_id"],
                            "condition": {
                                "conditionType": "AND",
                                "expressions": [
                                    {
                                        "leftExpression": "workitem.type",
                                        "operator": "==",
                                        "rightExpression": "'InboundSMS'",
                                    }
                                ],
                            },
                            "expansions": {
                                "functionId": {"name": two_way_sms_function["name"]}
                            },
                            "_working": False,
                        },
                        "type": "function",
                        "_selected": False,
                        "id": "refId1739600229776",
                        "icon": "icon-function",
                    },
                    {
                        "name": "HoldQueue",
                        "description": "Transition to another state",
                        "properties": {
                            "condition": {
                                "conditionType": "AND",
                                "expressions": [
                                    {
                                        "leftExpression": "workitem.type",
                                        "operator": "==",
                                        "rightExpression": "'InboundCall'",
                                    }
                                ],
                            },
                            "stateId": "67b11dbf1fac7db53c1d0210",
                            "description": "Transition to another state",
                        },
                        "type": "transition",
                        "_selected": False,
                        "transitionId": "refId1739600227355",
                        "id": "refId1739600229777",
                        "icon": "icon-transition",
                    },
                ],
                "_id": "67b11daace899acb3e0d1c38",
                "key": "67b11daace899acb3e0d1c38",
                "location": "768.7933111586822 1146.522875177372",
                "transitions": [{"name": "HoldQueue", "id": "refId1739600227355"}],
            },
            "67b11dbf1fac7db53c1d0210": {
                "category": "Standard",
                "objectType": "campaignstate",
                "campaignStateId": "67b11dbf1fac7db53c1d0210",
                "name": "HoldQueue",
                "description": "Newly Created State",
                "actions": [
                    {
                        "name": "Play & Collect Digits",
                        "description": "",
                        "properties": {
                            "loop": 1,
                            "numberDigits": 1,
                            "promptId": prompt["_id"],
                            "terminationKey": "#",
                            "timeoutInSeconds": "1",
                            "dlpOption": False,
                            "condition": {
                                "conditionType": "AND",
                                "expressions": [
                                    {
                                        "operator": "!=",
                                        "leftExpression": "workitem.digits",
                                        "rightExpression": "'1'",
                                    },
                                    {
                                        "leftExpression": "workitem.digits",
                                        "operator": "!=",
                                        "rightExpression": "'2'",
                                    },
                                ],
                            },
                            "expansions": {"promptId": {"name": prompt["name"]}},
                            "_working": False,
                        },
                        "type": "playdigits",
                        "_selected": False,
                        "id": "refId1740283338201",
                        "icon": "icon-playdigits",
                    },
                    {
                        "icon": "icon-tts",
                        "name": "Play Collect Google TTS",
                        "description": "Play Collect using Text-To-Speech",
                        "properties": {
                            "voiceName": "en-US-Wavenet-J",
                            "voiceGender": "male",
                            "text": '<prosody pitch="-2st">To leave a voicemail, press 1. To request a callback, press 2. Otherwise, please stay on the line.</prosody>',
                            "numberDigits": 1,
                            "terminationKey": "#",
                            "timeoutInSeconds": "1",
                            "dlpOption": False,
                            "condition": {
                                "conditionType": "AND",
                                "expressions": [
                                    {
                                        "operator": "!=",
                                        "leftExpression": "workitem.digits",
                                        "rightExpression": "'1'",
                                    },
                                    {
                                        "leftExpression": "workitem.digits",
                                        "operator": "!=",
                                        "rightExpression": "'2'",
                                    },
                                ],
                            },
                        },
                        "type": "googlettscollect",
                        "_selected": False,
                    },
                    {
                        "name": "Execute Function",
                        "description": "",
                        "properties": {
                            "description": "ACD Voicemail (1)",
                            "functionId": acd_voicemail_function["_id"],
                            "functionExpression": "",
                            "condition": {
                                "conditionType": "AND",
                                "expressions": [
                                    {
                                        "leftExpression": "workitem.digits",
                                        "operator": "==",
                                        "rightExpression": "'1'",
                                    }
                                ],
                            },
                            "expansions": {
                                "functionId": {"name": acd_voicemail_function["name"]}
                            },
                            "_working": False,
                        },
                        "type": "function",
                        "_selected": False,
                        "icon": "icon-function",
                        "id": "refId1739600229018",
                    },
                    {
                        "name": "Execute Function",
                        "description": "",
                        "properties": {
                            "description": "ACD Callback (2)",
                            "functionId": acd_callback_function["_id"],
                            "functionExpression": "",
                            "condition": {
                                "conditionType": "AND",
                                "expressions": [
                                    {
                                        "leftExpression": "workitem.digits",
                                        "operator": "==",
                                        "rightExpression": "'2'",
                                    }
                                ],
                            },
                            "expansions": {
                                "functionId": {"name": acd_callback_function["name"]}
                            },
                            "_working": False,
                        },
                        "type": "function",
                        "_selected": False,
                        "id": "refId1739600229019",
                        "icon": "icon-function",
                    },
                    {
                        "name": "Loop",
                        "description": "Transition to another state",
                        "properties": {
                            "description": "Back to Top",
                            "condition": {
                                "conditionType": "NONE",
                                "expressions": [{"operator": "=="}],
                            },
                            "stateName": "HoldQueue",
                        },
                        "type": "transitionbyname",
                        "_selected": False,
                        "transitionId": "refId1739600227365",
                        "id": "refId1739600229020",
                        "icon": "icon-transition",
                    },
                ],
                "_id": "67b11dbf1fac7db53c1d0210",
                "key": "67b11dbf1fac7db53c1d0210",
                "location": "1020.8849386524496 1327.8145390205887",
                "transitions": [{"name": "Loop", "id": "refId1739600227365"}],
            },
            "67b552f294171b486a3d1b7a": {
                "category": "Standard",
                "objectType": "campaignstate",
                "campaignStateId": "67b552f294171b486a3d1b7a",
                "name": "OutboundCall",
                "description": "Newly Created State",
                "actions": [
                    {
                        "name": "Save Variable",
                        "description": "",
                        "properties": {
                            "description": "interest",
                            "rightExpression": f'workitem.surveyResult["{chat_survey["_id"]}"].interest.value',
                            "variableName": "interest",
                            "asObject": False,
                            "dlpOption": False,
                            "wfmOption": False,
                            "dashboard": False,
                            "condition": {
                                "conditionType": "NONE",
                                "expressions": [{"operator": "=="}],
                            },
                        },
                        "type": "savevariable",
                        "_selected": False,
                        "id": "refId1739934455752",
                        "icon": "icon-save",
                    },
                    {
                        "name": "ConnectAgent",
                        "description": "Transition to another state",
                        "properties": {
                            "description": "Transition to another state",
                            "condition": {
                                "conditionType": "NONE",
                                "expressions": [{"operator": "=="}],
                            },
                            "stateId": "67b11daace899acb3e0d1c38",
                        },
                        "type": "transition",
                        "_selected": False,
                        "transitionId": "refId1739934454854",
                        "id": "refId1739934455758",
                        "icon": "icon-transition",
                    },
                ],
                "_id": "67b552f294171b486a3d1b7a",
                "key": "67b552f294171b486a3d1b7a",
                "location": "469.70693096850323 778.9689734663827",
                "transitions": [{"name": "ConnectAgent", "id": "refId1739934454854"}],
            },
            "67bea5bba2c3472a0f1cfba2": {
                "category": "Standard",
                "objectType": "campaignstate",
                "campaignStateId": "67bea5bba2c3472a0f1cfba2",
                "name": "Email",
                "description": "Newly Created State",
                "actions": [
                    {
                        "icon": "icon-transition",
                        "name": "ConnectAgent",
                        "description": "Transition to another state",
                        "properties": {
                            "condition": {
                                "conditionType": "NONE",
                                "expressions": [{"operator": "=="}],
                            },
                            "stateId": "67b11daace899acb3e0d1c38",
                        },
                        "type": "transition",
                        "_selected": False,
                        "transitionId": "refId1740544931138",
                    }
                ],
                "_id": "67bea5bba2c3472a0f1cfba2",
                "key": "67bea5bba2c3472a0f1cfba2",
                "location": "468.9006442254572 970.810891049498",
                "transitions": [{"name": "ConnectAgent", "id": "refId1740544931138"}],
            },
        },
        "finalWorkitemStateId": "67b1186f5510d9081ac8e32b",
        "finalUserStateId": "67b1186f5510d9081ac8e32b",
        "name": workflow_name,
    }

    if vertical == "general":
        inbound_call_menu = '<prosody pitch="-2st">For sales, press 1. For customer service, press 2. For billing, press 3. For technical support, press 4. Otherwise, please stay on the line.</prosody>'
        chat_variables = [
            {
                "icon": "icon-save",
                "name": "Save Variable",
                "description": "",
                "properties": {
                    "description": "queueId - Sales",
                    "rightExpression": queues["Sales"],
                    "variableName": "queueId",
                    "asObject": False,
                    "dlpOption": False,
                    "wfmOption": False,
                    "dashboard": False,
                    "condition": {
                        "conditionType": "AND",
                        "expressions": [
                            {
                                "leftExpression": "workitem.data.interest",
                                "operator": "==",
                                "rightExpression": "'Sales'",
                            }
                        ],
                    },
                },
                "type": "savevariable",
                "_selected": False,
            },
            {
                "icon": "icon-save",
                "name": "Save Variable",
                "description": "",
                "properties": {
                    "description": "queueId - Customer Service",
                    "rightExpression": queues["Customer Service"],
                    "variableName": "queueId",
                    "asObject": False,
                    "dlpOption": False,
                    "wfmOption": False,
                    "dashboard": False,
                    "condition": {
                        "conditionType": "AND",
                        "expressions": [
                            {
                                "leftExpression": "workitem.data.interest",
                                "operator": "==",
                                "rightExpression": "'Customer Service'",
                            }
                        ],
                    },
                },
                "type": "savevariable",
                "_selected": False,
                "id": "refId1739749451080",
            },
            {
                "icon": "icon-save",
                "name": "Save Variable",
                "description": "",
                "properties": {
                    "description": "queueId - Billing",
                    "rightExpression": queues["Billing"],
                    "variableName": "queueId",
                    "asObject": False,
                    "dlpOption": False,
                    "wfmOption": False,
                    "dashboard": False,
                    "condition": {
                        "conditionType": "AND",
                        "expressions": [
                            {
                                "leftExpression": "workitem.data.interest",
                                "operator": "==",
                                "rightExpression": "'Billing'",
                            }
                        ],
                    },
                },
                "type": "savevariable",
                "_selected": False,
                "id": "refId1739749451064",
            },
            {
                "icon": "icon-save",
                "name": "Save Variable",
                "description": "",
                "properties": {
                    "description": "queueId - Technical Support",
                    "rightExpression": queues["Technical Support"],
                    "variableName": "queueId",
                    "asObject": False,
                    "dlpOption": False,
                    "wfmOption": False,
                    "dashboard": False,
                    "condition": {
                        "conditionType": "AND",
                        "expressions": [
                            {
                                "leftExpression": "workitem.data.interest",
                                "operator": "==",
                                "rightExpression": "'Technical Support'",
                            }
                        ],
                    },
                },
                "type": "savevariable",
                "_selected": False,
                "id": "refId1739749451048",
            },
        ]
        inbound_call_variables = [
            {
                "name": "Save Variable",
                "description": "",
                "properties": {
                    "description": "queueId - Sales",
                    "rightExpression": queues["Sales"],
                    "variableName": "queueId",
                    "asObject": False,
                    "dlpOption": False,
                    "wfmOption": False,
                    "dashboard": False,
                    "condition": {
                        "conditionType": "AND",
                        "expressions": [
                            {
                                "operator": "==",
                                "leftExpression": "workitem.digits",
                                "rightExpression": "'1'",
                            }
                        ],
                    },
                },
                "type": "savevariable",
                "_selected": False,
                "icon": "icon-save",
                "id": "refId1739600231288",
            },
            {
                "name": "Save Variable",
                "description": "",
                "properties": {
                    "description": "queueId - Customer Service",
                    "rightExpression": queues["Customer Service"],
                    "variableName": "queueId",
                    "asObject": False,
                    "dlpOption": False,
                    "wfmOption": False,
                    "dashboard": False,
                    "condition": {
                        "conditionType": "AND",
                        "expressions": [
                            {
                                "operator": "==",
                                "leftExpression": "workitem.digits",
                                "rightExpression": "'2'",
                            }
                        ],
                    },
                },
                "type": "savevariable",
                "_selected": False,
                "id": "refId1739600231289",
                "icon": "icon-save",
            },
            {
                "name": "Save Variable",
                "description": "",
                "properties": {
                    "description": "queueId - Billing",
                    "rightExpression": queues["Billing"],
                    "variableName": "queueId",
                    "asObject": False,
                    "dlpOption": False,
                    "wfmOption": False,
                    "dashboard": False,
                    "condition": {
                        "conditionType": "AND",
                        "expressions": [
                            {
                                "operator": "==",
                                "leftExpression": "workitem.digits",
                                "rightExpression": "'3'",
                            }
                        ],
                    },
                },
                "type": "savevariable",
                "_selected": False,
                "id": "refId1739600231290",
                "icon": "icon-save",
            },
            {
                "name": "Save Variable",
                "description": "",
                "properties": {
                    "description": "queueId - Technical Support",
                    "rightExpression": queues["Technical Support"],
                    "variableName": "queueId",
                    "asObject": False,
                    "dlpOption": False,
                    "wfmOption": False,
                    "dashboard": False,
                    "condition": {
                        "conditionType": "AND",
                        "expressions": [
                            {
                                "operator": "==",
                                "leftExpression": "workitem.digits",
                                "rightExpression": "'4'",
                            }
                        ],
                    },
                },
                "type": "savevariable",
                "_selected": False,
                "id": "refId1739600231291",
                "icon": "icon-save",
            },
        ]
        outbound_call_variables = [
            {
                "name": "Save Variable",
                "description": "",
                "properties": {
                    "description": "queueId - Sales",
                    "rightExpression": queues["Sales"],
                    "variableName": "queueId",
                    "asObject": False,
                    "dlpOption": False,
                    "wfmOption": False,
                    "dashboard": False,
                    "condition": {
                        "conditionType": "AND",
                        "expressions": [
                            {
                                "leftExpression": "workitem.data.interest",
                                "operator": "==",
                                "rightExpression": "'Sales'",
                            }
                        ],
                    },
                },
                "type": "savevariable",
                "_selected": False,
                "id": "refId1739934455753",
                "icon": "icon-save",
            },
            {
                "name": "Save Variable",
                "description": "",
                "properties": {
                    "description": "queueId - Customer Service",
                    "rightExpression": queues["Customer Service"],
                    "variableName": "queueId",
                    "asObject": False,
                    "dlpOption": False,
                    "wfmOption": False,
                    "dashboard": False,
                    "condition": {
                        "conditionType": "AND",
                        "expressions": [
                            {
                                "leftExpression": "workitem.data.interest",
                                "operator": "==",
                                "rightExpression": "'Customer Service'",
                            }
                        ],
                    },
                },
                "type": "savevariable",
                "_selected": False,
                "id": "refId1739934455754",
                "icon": "icon-save",
            },
            {
                "name": "Save Variable",
                "description": "",
                "properties": {
                    "description": "queueId - Billing",
                    "rightExpression": queues["Billing"],
                    "variableName": "queueId",
                    "asObject": False,
                    "dlpOption": False,
                    "wfmOption": False,
                    "dashboard": False,
                    "condition": {
                        "conditionType": "AND",
                        "expressions": [
                            {
                                "leftExpression": "workitem.data.interest",
                                "operator": "==",
                                "rightExpression": "'Billing'",
                            }
                        ],
                    },
                },
                "type": "savevariable",
                "_selected": False,
                "id": "refId1739934455755",
                "icon": "icon-save",
            },
            {
                "name": "Save Variable",
                "description": "",
                "properties": {
                    "description": "queueId - Technical Support",
                    "rightExpression": queues["Technical Support"],
                    "variableName": "queueId",
                    "asObject": False,
                    "dlpOption": False,
                    "wfmOption": False,
                    "dashboard": False,
                    "condition": {
                        "conditionType": "AND",
                        "expressions": [
                            {
                                "leftExpression": "workitem.data.interest",
                                "operator": "==",
                                "rightExpression": "'Technical Support'",
                            }
                        ],
                    },
                },
                "type": "savevariable",
                "_selected": False,
                "id": "refId1739934455756",
                "icon": "icon-save",
            },
            {
                "name": "Survey",
                "description": "Assign survey to workitem",
                "properties": {
                    "description": user_survey["name"],
                    "condition": {
                        "conditionType": "NONE",
                        "expressions": [{"operator": "=="}],
                    },
                    "surveyId": user_survey["_id"],
                    "expansions": {"surveyId": {"name": user_survey["name"]}},
                    "_working": False,
                },
                "type": "assignsurvey",
                "_selected": False,
                "id": "refId1739934455757",
                "icon": "icon-survey",
            },
        ]
    elif vertical == "hc":
        inbound_call_menu = '<prosody pitch="-2st">To refill a prescription, press 1. To schedule, reschedule, or cancel an appointment, press 2. For billing, press 3. For customer service, press 4. Otherwise, please stay on the line.</prosody>'
        chat_variables = [
            {
                "icon": "icon-save",
                "name": "Save Variable",
                "description": "",
                "properties": {
                    "description": "queueId - Prescription Refills",
                    "rightExpression": queues["Prescription Refills"],
                    "variableName": "queueId",
                    "asObject": False,
                    "dlpOption": False,
                    "wfmOption": False,
                    "dashboard": False,
                    "condition": {
                        "conditionType": "AND",
                        "expressions": [
                            {
                                "leftExpression": "workitem.data.interest",
                                "operator": "==",
                                "rightExpression": "'Prescription Refills'",
                            }
                        ],
                    },
                },
                "type": "savevariable",
                "_selected": False,
            },
            {
                "icon": "icon-save",
                "name": "Save Variable",
                "description": "",
                "properties": {
                    "description": "queueId - Appointments",
                    "rightExpression": queues["Appointments"],
                    "variableName": "queueId",
                    "asObject": False,
                    "dlpOption": False,
                    "wfmOption": False,
                    "dashboard": False,
                    "condition": {
                        "conditionType": "AND",
                        "expressions": [
                            {
                                "leftExpression": "workitem.data.interest",
                                "operator": "==",
                                "rightExpression": "'Appointments'",
                            }
                        ],
                    },
                },
                "type": "savevariable",
                "_selected": False,
                "id": "refId1739749451080",
            },
            {
                "icon": "icon-save",
                "name": "Save Variable",
                "description": "",
                "properties": {
                    "description": "queueId - Billing",
                    "rightExpression": queues["Billing"],
                    "variableName": "queueId",
                    "asObject": False,
                    "dlpOption": False,
                    "wfmOption": False,
                    "dashboard": False,
                    "condition": {
                        "conditionType": "AND",
                        "expressions": [
                            {
                                "leftExpression": "workitem.data.interest",
                                "operator": "==",
                                "rightExpression": "'Billing'",
                            }
                        ],
                    },
                },
                "type": "savevariable",
                "_selected": False,
                "id": "refId1739749451064",
            },
            {
                "icon": "icon-save",
                "name": "Save Variable",
                "description": "",
                "properties": {
                    "description": "queueId - Customer Service",
                    "rightExpression": queues["Customer Service"],
                    "variableName": "queueId",
                    "asObject": False,
                    "dlpOption": False,
                    "wfmOption": False,
                    "dashboard": False,
                    "condition": {
                        "conditionType": "AND",
                        "expressions": [
                            {
                                "leftExpression": "workitem.data.interest",
                                "operator": "==",
                                "rightExpression": "'Customer Service'",
                            }
                        ],
                    },
                },
                "type": "savevariable",
                "_selected": False,
                "id": "refId1739749451048",
            },
        ]
        inbound_call_variables = [
            {
                "name": "Save Variable",
                "description": "",
                "properties": {
                    "description": "queueId - Prescription Refills",
                    "rightExpression": queues["Prescription Refills"],
                    "variableName": "queueId",
                    "asObject": False,
                    "dlpOption": False,
                    "wfmOption": False,
                    "dashboard": False,
                    "condition": {
                        "conditionType": "AND",
                        "expressions": [
                            {
                                "operator": "==",
                                "leftExpression": "workitem.digits",
                                "rightExpression": "'1'",
                            }
                        ],
                    },
                },
                "type": "savevariable",
                "_selected": False,
                "icon": "icon-save",
                "id": "refId1739600231288",
            },
            {
                "name": "Save Variable",
                "description": "",
                "properties": {
                    "description": "queueId - Appointments",
                    "rightExpression": queues["Appointments"],
                    "variableName": "queueId",
                    "asObject": False,
                    "dlpOption": False,
                    "wfmOption": False,
                    "dashboard": False,
                    "condition": {
                        "conditionType": "AND",
                        "expressions": [
                            {
                                "operator": "==",
                                "leftExpression": "workitem.digits",
                                "rightExpression": "'2'",
                            }
                        ],
                    },
                },
                "type": "savevariable",
                "_selected": False,
                "id": "refId1739600231289",
                "icon": "icon-save",
            },
            {
                "name": "Save Variable",
                "description": "",
                "properties": {
                    "description": "queueId - Billing",
                    "rightExpression": queues["Billing"],
                    "variableName": "queueId",
                    "asObject": False,
                    "dlpOption": False,
                    "wfmOption": False,
                    "dashboard": False,
                    "condition": {
                        "conditionType": "AND",
                        "expressions": [
                            {
                                "operator": "==",
                                "leftExpression": "workitem.digits",
                                "rightExpression": "'3'",
                            }
                        ],
                    },
                },
                "type": "savevariable",
                "_selected": False,
                "id": "refId1739600231290",
                "icon": "icon-save",
            },
            {
                "name": "Save Variable",
                "description": "",
                "properties": {
                    "description": "queueId - Customer Service",
                    "rightExpression": queues["Customer Service"],
                    "variableName": "queueId",
                    "asObject": False,
                    "dlpOption": False,
                    "wfmOption": False,
                    "dashboard": False,
                    "condition": {
                        "conditionType": "AND",
                        "expressions": [
                            {
                                "operator": "==",
                                "leftExpression": "workitem.digits",
                                "rightExpression": "'4'",
                            }
                        ],
                    },
                },
                "type": "savevariable",
                "_selected": False,
                "id": "refId1739600231291",
                "icon": "icon-save",
            },
        ]
        outbound_call_variables = [
            {
                "name": "Save Variable",
                "description": "",
                "properties": {
                    "description": "queueId - Prescription Refills",
                    "rightExpression": queues["Prescription Refills"],
                    "variableName": "queueId",
                    "asObject": False,
                    "dlpOption": False,
                    "wfmOption": False,
                    "dashboard": False,
                    "condition": {
                        "conditionType": "AND",
                        "expressions": [
                            {
                                "leftExpression": "workitem.data.interest",
                                "operator": "==",
                                "rightExpression": "'Prescription Refills'",
                            }
                        ],
                    },
                },
                "type": "savevariable",
                "_selected": False,
                "id": "refId1739934455753",
                "icon": "icon-save",
            },
            {
                "name": "Save Variable",
                "description": "",
                "properties": {
                    "description": "queueId - Appointments",
                    "rightExpression": queues["Appointments"],
                    "variableName": "queueId",
                    "asObject": False,
                    "dlpOption": False,
                    "wfmOption": False,
                    "dashboard": False,
                    "condition": {
                        "conditionType": "AND",
                        "expressions": [
                            {
                                "leftExpression": "workitem.data.interest",
                                "operator": "==",
                                "rightExpression": "'Appointments'",
                            }
                        ],
                    },
                },
                "type": "savevariable",
                "_selected": False,
                "id": "refId1739934455754",
                "icon": "icon-save",
            },
            {
                "name": "Save Variable",
                "description": "",
                "properties": {
                    "description": "queueId - Billing",
                    "rightExpression": queues["Billing"],
                    "variableName": "queueId",
                    "asObject": False,
                    "dlpOption": False,
                    "wfmOption": False,
                    "dashboard": False,
                    "condition": {
                        "conditionType": "AND",
                        "expressions": [
                            {
                                "leftExpression": "workitem.data.interest",
                                "operator": "==",
                                "rightExpression": "'Billing'",
                            }
                        ],
                    },
                },
                "type": "savevariable",
                "_selected": False,
                "id": "refId1739934455755",
                "icon": "icon-save",
            },
            {
                "name": "Save Variable",
                "description": "",
                "properties": {
                    "description": "queueId - Customer Service",
                    "rightExpression": queues["Customer Service"],
                    "variableName": "queueId",
                    "asObject": False,
                    "dlpOption": False,
                    "wfmOption": False,
                    "dashboard": False,
                    "condition": {
                        "conditionType": "AND",
                        "expressions": [
                            {
                                "leftExpression": "workitem.data.interest",
                                "operator": "==",
                                "rightExpression": "'Customer Service'",
                            }
                        ],
                    },
                },
                "type": "savevariable",
                "_selected": False,
                "id": "refId1739934455756",
                "icon": "icon-save",
            },
            {
                "name": "Survey",
                "description": "Assign survey to workitem",
                "properties": {
                    "description": user_survey["name"],
                    "condition": {
                        "conditionType": "NONE",
                        "expressions": [{"operator": "=="}],
                    },
                    "surveyId": user_survey["_id"],
                    "expansions": {"surveyId": {"name": user_survey["name"]}},
                    "_working": False,
                },
                "type": "assignsurvey",
                "_selected": False,
                "id": "refId1739934455757",
                "icon": "icon-survey",
            },
        ]
    elif vertical == "finserv":
        inbound_call_menu = '<prosody pitch="-2st">To apply for a new credit card, press 1. To apply for a new loan, press 2. To open a new checking or savings account, press 3. For billing, press 4. For customer service, press 5. Otherwise, please stay on the line.</prosody>'
        chat_variables = [
            {
                "icon": "icon-save",
                "name": "Save Variable",
                "description": "",
                "properties": {
                    "description": "queueId - Credit Card Applications",
                    "rightExpression": queues["Credit Card Applications"],
                    "variableName": "queueId",
                    "asObject": False,
                    "dlpOption": False,
                    "wfmOption": False,
                    "dashboard": False,
                    "condition": {
                        "conditionType": "AND",
                        "expressions": [
                            {
                                "leftExpression": "workitem.data.interest",
                                "operator": "==",
                                "rightExpression": "'Credit Card Applications'",
                            }
                        ],
                    },
                },
                "type": "savevariable",
                "_selected": False,
            },
            {
                "icon": "icon-save",
                "name": "Save Variable",
                "description": "",
                "properties": {
                    "description": "queueId - Loan Applications",
                    "rightExpression": queues["Loan Applications"],
                    "variableName": "queueId",
                    "asObject": False,
                    "dlpOption": False,
                    "wfmOption": False,
                    "dashboard": False,
                    "condition": {
                        "conditionType": "AND",
                        "expressions": [
                            {
                                "leftExpression": "workitem.data.interest",
                                "operator": "==",
                                "rightExpression": "'Loan Applications'",
                            }
                        ],
                    },
                },
                "type": "savevariable",
                "_selected": False,
                "id": "refId1739749451080",
            },
            {
                "icon": "icon-save",
                "name": "Save Variable",
                "description": "",
                "properties": {
                    "description": "queueId - Accounts",
                    "rightExpression": queues["Accounts"],
                    "variableName": "queueId",
                    "asObject": False,
                    "dlpOption": False,
                    "wfmOption": False,
                    "dashboard": False,
                    "condition": {
                        "conditionType": "AND",
                        "expressions": [
                            {
                                "leftExpression": "workitem.data.interest",
                                "operator": "==",
                                "rightExpression": "'Accounts'",
                            }
                        ],
                    },
                },
                "type": "savevariable",
                "_selected": False,
                "id": "refId1739749451080",
            },
            {
                "icon": "icon-save",
                "name": "Save Variable",
                "description": "",
                "properties": {
                    "description": "queueId - Billing",
                    "rightExpression": queues["Billing"],
                    "variableName": "queueId",
                    "asObject": False,
                    "dlpOption": False,
                    "wfmOption": False,
                    "dashboard": False,
                    "condition": {
                        "conditionType": "AND",
                        "expressions": [
                            {
                                "leftExpression": "workitem.data.interest",
                                "operator": "==",
                                "rightExpression": "'Billing'",
                            }
                        ],
                    },
                },
                "type": "savevariable",
                "_selected": False,
                "id": "refId1739749451048",
            },
            {
                "icon": "icon-save",
                "name": "Save Variable",
                "description": "",
                "properties": {
                    "description": "queueId - Customer Service",
                    "rightExpression": queues["Customer Service"],
                    "variableName": "queueId",
                    "asObject": False,
                    "dlpOption": False,
                    "wfmOption": False,
                    "dashboard": False,
                    "condition": {
                        "conditionType": "AND",
                        "expressions": [
                            {
                                "leftExpression": "workitem.data.interest",
                                "operator": "==",
                                "rightExpression": "'Customer Service'",
                            }
                        ],
                    },
                },
                "type": "savevariable",
                "_selected": False,
                "id": "refId1739749451048",
            },
        ]
        inbound_call_variables = [
            {
                "name": "Save Variable",
                "description": "",
                "properties": {
                    "description": "queueId - Credit Card Applications",
                    "rightExpression": queues["Credit Card Applications"],
                    "variableName": "queueId",
                    "asObject": False,
                    "dlpOption": False,
                    "wfmOption": False,
                    "dashboard": False,
                    "condition": {
                        "conditionType": "AND",
                        "expressions": [
                            {
                                "operator": "==",
                                "leftExpression": "workitem.digits",
                                "rightExpression": "'1'",
                            }
                        ],
                    },
                },
                "type": "savevariable",
                "_selected": False,
                "icon": "icon-save",
                "id": "refId1739600231288",
            },
            {
                "name": "Save Variable",
                "description": "",
                "properties": {
                    "description": "queueId - Loan Applications",
                    "rightExpression": queues["Loan Applications"],
                    "variableName": "queueId",
                    "asObject": False,
                    "dlpOption": False,
                    "wfmOption": False,
                    "dashboard": False,
                    "condition": {
                        "conditionType": "AND",
                        "expressions": [
                            {
                                "operator": "==",
                                "leftExpression": "workitem.digits",
                                "rightExpression": "'2'",
                            }
                        ],
                    },
                },
                "type": "savevariable",
                "_selected": False,
                "id": "refId1739600231289",
                "icon": "icon-save",
            },
            {
                "name": "Save Variable",
                "description": "",
                "properties": {
                    "description": "queueId - Accounts",
                    "rightExpression": queues["Accounts"],
                    "variableName": "queueId",
                    "asObject": False,
                    "dlpOption": False,
                    "wfmOption": False,
                    "dashboard": False,
                    "condition": {
                        "conditionType": "AND",
                        "expressions": [
                            {
                                "operator": "==",
                                "leftExpression": "workitem.digits",
                                "rightExpression": "'3'",
                            }
                        ],
                    },
                },
                "type": "savevariable",
                "_selected": False,
                "id": "refId1739600231290",
                "icon": "icon-save",
            },
            {
                "name": "Save Variable",
                "description": "",
                "properties": {
                    "description": "queueId - Billing",
                    "rightExpression": queues["Billing"],
                    "variableName": "queueId",
                    "asObject": False,
                    "dlpOption": False,
                    "wfmOption": False,
                    "dashboard": False,
                    "condition": {
                        "conditionType": "AND",
                        "expressions": [
                            {
                                "operator": "==",
                                "leftExpression": "workitem.digits",
                                "rightExpression": "'4'",
                            }
                        ],
                    },
                },
                "type": "savevariable",
                "_selected": False,
                "id": "refId1739600231291",
                "icon": "icon-save",
            },
            {
                "name": "Save Variable",
                "description": "",
                "properties": {
                    "description": "queueId - Customer Service",
                    "rightExpression": queues["Customer Service"],
                    "variableName": "queueId",
                    "asObject": False,
                    "dlpOption": False,
                    "wfmOption": False,
                    "dashboard": False,
                    "condition": {
                        "conditionType": "AND",
                        "expressions": [
                            {
                                "operator": "==",
                                "leftExpression": "workitem.digits",
                                "rightExpression": "'5'",
                            }
                        ],
                    },
                },
                "type": "savevariable",
                "_selected": False,
                "id": "refId1739600231291",
                "icon": "icon-save",
            },
        ]
        outbound_call_variables = [
            {
                "name": "Save Variable",
                "description": "",
                "properties": {
                    "description": "queueId - Credit Card Applications",
                    "rightExpression": queues["Credit Card Applications"],
                    "variableName": "queueId",
                    "asObject": False,
                    "dlpOption": False,
                    "wfmOption": False,
                    "dashboard": False,
                    "condition": {
                        "conditionType": "AND",
                        "expressions": [
                            {
                                "leftExpression": "workitem.data.interest",
                                "operator": "==",
                                "rightExpression": "'Credit Card Applications'",
                            }
                        ],
                    },
                },
                "type": "savevariable",
                "_selected": False,
                "id": "refId1739934455753",
                "icon": "icon-save",
            },
            {
                "name": "Save Variable",
                "description": "",
                "properties": {
                    "description": "queueId - Loan Applications",
                    "rightExpression": queues["Loan Applications"],
                    "variableName": "queueId",
                    "asObject": False,
                    "dlpOption": False,
                    "wfmOption": False,
                    "dashboard": False,
                    "condition": {
                        "conditionType": "AND",
                        "expressions": [
                            {
                                "leftExpression": "workitem.data.interest",
                                "operator": "==",
                                "rightExpression": "'Loan Applications'",
                            }
                        ],
                    },
                },
                "type": "savevariable",
                "_selected": False,
                "id": "refId1739934455754",
                "icon": "icon-save",
            },
            {
                "name": "Save Variable",
                "description": "",
                "properties": {
                    "description": "queueId - Accounts",
                    "rightExpression": queues["Accounts"],
                    "variableName": "queueId",
                    "asObject": False,
                    "dlpOption": False,
                    "wfmOption": False,
                    "dashboard": False,
                    "condition": {
                        "conditionType": "AND",
                        "expressions": [
                            {
                                "leftExpression": "workitem.data.interest",
                                "operator": "==",
                                "rightExpression": "'Accounts'",
                            }
                        ],
                    },
                },
                "type": "savevariable",
                "_selected": False,
                "id": "refId1739934455755",
                "icon": "icon-save",
            },
            {
                "name": "Save Variable",
                "description": "",
                "properties": {
                    "description": "queueId - Billing",
                    "rightExpression": queues["Billing"],
                    "variableName": "queueId",
                    "asObject": False,
                    "dlpOption": False,
                    "wfmOption": False,
                    "dashboard": False,
                    "condition": {
                        "conditionType": "AND",
                        "expressions": [
                            {
                                "leftExpression": "workitem.data.interest",
                                "operator": "==",
                                "rightExpression": "'Billing'",
                            }
                        ],
                    },
                },
                "type": "savevariable",
                "_selected": False,
                "id": "refId1739934455755",
                "icon": "icon-save",
            },
            {
                "name": "Save Variable",
                "description": "",
                "properties": {
                    "description": "queueId - Customer Service",
                    "rightExpression": queues["Customer Service"],
                    "variableName": "queueId",
                    "asObject": False,
                    "dlpOption": False,
                    "wfmOption": False,
                    "dashboard": False,
                    "condition": {
                        "conditionType": "AND",
                        "expressions": [
                            {
                                "leftExpression": "workitem.data.interest",
                                "operator": "==",
                                "rightExpression": "'Customer Service'",
                            }
                        ],
                    },
                },
                "type": "savevariable",
                "_selected": False,
                "id": "refId1739934455756",
                "icon": "icon-save",
            },
            {
                "name": "Survey",
                "description": "Assign survey to workitem",
                "properties": {
                    "description": user_survey["name"],
                    "condition": {
                        "conditionType": "NONE",
                        "expressions": [{"operator": "=="}],
                    },
                    "surveyId": user_survey["_id"],
                    "expansions": {"surveyId": {"name": user_survey["name"]}},
                    "_working": False,
                },
                "type": "assignsurvey",
                "_selected": False,
                "id": "refId1739934455757",
                "icon": "icon-survey",
            },
        ]
    elif vertical == "insurance":
        inbound_call_menu = '<prosody pitch="-2st">To sign up for a new policy, or to make changes to an existing policy, press 1. To file a new claim, or check the status of an existing claim, press 2. For billing, press 3. For customer service, press 4. Otherwise, please stay on the line.</prosody>'
        chat_variables = [
            {
                "icon": "icon-save",
                "name": "Save Variable",
                "description": "",
                "properties": {
                    "description": "queueId - Policies",
                    "rightExpression": queues["Policies"],
                    "variableName": "queueId",
                    "asObject": False,
                    "dlpOption": False,
                    "wfmOption": False,
                    "dashboard": False,
                    "condition": {
                        "conditionType": "AND",
                        "expressions": [
                            {
                                "leftExpression": "workitem.data.interest",
                                "operator": "==",
                                "rightExpression": "'Policies'",
                            }
                        ],
                    },
                },
                "type": "savevariable",
                "_selected": False,
            },
            {
                "icon": "icon-save",
                "name": "Save Variable",
                "description": "",
                "properties": {
                    "description": "queueId - Claims",
                    "rightExpression": queues["Claims"],
                    "variableName": "queueId",
                    "asObject": False,
                    "dlpOption": False,
                    "wfmOption": False,
                    "dashboard": False,
                    "condition": {
                        "conditionType": "AND",
                        "expressions": [
                            {
                                "leftExpression": "workitem.data.interest",
                                "operator": "==",
                                "rightExpression": "'Claims'",
                            }
                        ],
                    },
                },
                "type": "savevariable",
                "_selected": False,
                "id": "refId1739749451080",
            },
            {
                "icon": "icon-save",
                "name": "Save Variable",
                "description": "",
                "properties": {
                    "description": "queueId - Billing",
                    "rightExpression": queues["Billing"],
                    "variableName": "queueId",
                    "asObject": False,
                    "dlpOption": False,
                    "wfmOption": False,
                    "dashboard": False,
                    "condition": {
                        "conditionType": "AND",
                        "expressions": [
                            {
                                "leftExpression": "workitem.data.interest",
                                "operator": "==",
                                "rightExpression": "'Billing'",
                            }
                        ],
                    },
                },
                "type": "savevariable",
                "_selected": False,
                "id": "refId1739749451048",
            },
            {
                "icon": "icon-save",
                "name": "Save Variable",
                "description": "",
                "properties": {
                    "description": "queueId - Customer Service",
                    "rightExpression": queues["Customer Service"],
                    "variableName": "queueId",
                    "asObject": False,
                    "dlpOption": False,
                    "wfmOption": False,
                    "dashboard": False,
                    "condition": {
                        "conditionType": "AND",
                        "expressions": [
                            {
                                "leftExpression": "workitem.data.interest",
                                "operator": "==",
                                "rightExpression": "'Customer Service'",
                            }
                        ],
                    },
                },
                "type": "savevariable",
                "_selected": False,
                "id": "refId1739749451048",
            },
        ]
        inbound_call_variables = [
            {
                "name": "Save Variable",
                "description": "",
                "properties": {
                    "description": "queueId - Policies",
                    "rightExpression": queues["Policies"],
                    "variableName": "queueId",
                    "asObject": False,
                    "dlpOption": False,
                    "wfmOption": False,
                    "dashboard": False,
                    "condition": {
                        "conditionType": "AND",
                        "expressions": [
                            {
                                "operator": "==",
                                "leftExpression": "workitem.digits",
                                "rightExpression": "'1'",
                            }
                        ],
                    },
                },
                "type": "savevariable",
                "_selected": False,
                "icon": "icon-save",
                "id": "refId1739600231288",
            },
            {
                "name": "Save Variable",
                "description": "",
                "properties": {
                    "description": "queueId - Claims",
                    "rightExpression": queues["Claims"],
                    "variableName": "queueId",
                    "asObject": False,
                    "dlpOption": False,
                    "wfmOption": False,
                    "dashboard": False,
                    "condition": {
                        "conditionType": "AND",
                        "expressions": [
                            {
                                "operator": "==",
                                "leftExpression": "workitem.digits",
                                "rightExpression": "'2'",
                            }
                        ],
                    },
                },
                "type": "savevariable",
                "_selected": False,
                "id": "refId1739600231289",
                "icon": "icon-save",
            },
            {
                "name": "Save Variable",
                "description": "",
                "properties": {
                    "description": "queueId - Billing",
                    "rightExpression": queues["Billing"],
                    "variableName": "queueId",
                    "asObject": False,
                    "dlpOption": False,
                    "wfmOption": False,
                    "dashboard": False,
                    "condition": {
                        "conditionType": "AND",
                        "expressions": [
                            {
                                "operator": "==",
                                "leftExpression": "workitem.digits",
                                "rightExpression": "'3'",
                            }
                        ],
                    },
                },
                "type": "savevariable",
                "_selected": False,
                "id": "refId1739600231291",
                "icon": "icon-save",
            },
            {
                "name": "Save Variable",
                "description": "",
                "properties": {
                    "description": "queueId - Customer Service",
                    "rightExpression": queues["Customer Service"],
                    "variableName": "queueId",
                    "asObject": False,
                    "dlpOption": False,
                    "wfmOption": False,
                    "dashboard": False,
                    "condition": {
                        "conditionType": "AND",
                        "expressions": [
                            {
                                "operator": "==",
                                "leftExpression": "workitem.digits",
                                "rightExpression": "'4'",
                            }
                        ],
                    },
                },
                "type": "savevariable",
                "_selected": False,
                "id": "refId1739600231291",
                "icon": "icon-save",
            },
        ]
        outbound_call_variables = [
            {
                "name": "Save Variable",
                "description": "",
                "properties": {
                    "description": "queueId - Policies",
                    "rightExpression": queues["Policies"],
                    "variableName": "queueId",
                    "asObject": False,
                    "dlpOption": False,
                    "wfmOption": False,
                    "dashboard": False,
                    "condition": {
                        "conditionType": "AND",
                        "expressions": [
                            {
                                "leftExpression": "workitem.data.interest",
                                "operator": "==",
                                "rightExpression": "'Policies'",
                            }
                        ],
                    },
                },
                "type": "savevariable",
                "_selected": False,
                "id": "refId1739934455753",
                "icon": "icon-save",
            },
            {
                "name": "Save Variable",
                "description": "",
                "properties": {
                    "description": "queueId - Claims",
                    "rightExpression": queues["Claims"],
                    "variableName": "queueId",
                    "asObject": False,
                    "dlpOption": False,
                    "wfmOption": False,
                    "dashboard": False,
                    "condition": {
                        "conditionType": "AND",
                        "expressions": [
                            {
                                "leftExpression": "workitem.data.interest",
                                "operator": "==",
                                "rightExpression": "'Claims'",
                            }
                        ],
                    },
                },
                "type": "savevariable",
                "_selected": False,
                "id": "refId1739934455754",
                "icon": "icon-save",
            },
            {
                "name": "Save Variable",
                "description": "",
                "properties": {
                    "description": "queueId - Billing",
                    "rightExpression": queues["Billing"],
                    "variableName": "queueId",
                    "asObject": False,
                    "dlpOption": False,
                    "wfmOption": False,
                    "dashboard": False,
                    "condition": {
                        "conditionType": "AND",
                        "expressions": [
                            {
                                "leftExpression": "workitem.data.interest",
                                "operator": "==",
                                "rightExpression": "'Billing'",
                            }
                        ],
                    },
                },
                "type": "savevariable",
                "_selected": False,
                "id": "refId1739934455755",
                "icon": "icon-save",
            },
            {
                "name": "Save Variable",
                "description": "",
                "properties": {
                    "description": "queueId - Customer Service",
                    "rightExpression": queues["Customer Service"],
                    "variableName": "queueId",
                    "asObject": False,
                    "dlpOption": False,
                    "wfmOption": False,
                    "dashboard": False,
                    "condition": {
                        "conditionType": "AND",
                        "expressions": [
                            {
                                "leftExpression": "workitem.data.interest",
                                "operator": "==",
                                "rightExpression": "'Customer Service'",
                            }
                        ],
                    },
                },
                "type": "savevariable",
                "_selected": False,
                "id": "refId1739934455756",
                "icon": "icon-save",
            },
            {
                "name": "Survey",
                "description": "Assign survey to workitem",
                "properties": {
                    "description": user_survey["name"],
                    "condition": {
                        "conditionType": "NONE",
                        "expressions": [{"operator": "=="}],
                    },
                    "surveyId": user_survey["_id"],
                    "expansions": {"surveyId": {"name": user_survey["name"]}},
                    "_working": False,
                },
                "type": "assignsurvey",
                "_selected": False,
                "id": "refId1739934455757",
                "icon": "icon-survey",
            },
        ]
    elif vertical == "retail":
        inbound_call_menu = '<prosody pitch="-2st">For order inquiries, press 1. For stock availability, press 2. To exchange an item, press 3. For billing, press 4. For customer service, press 5. Otherwise, please stay on the line.</prosody>'
        chat_variables = [
            {
                "icon": "icon-save",
                "name": "Save Variable",
                "description": "",
                "properties": {
                    "description": "queueId - Orders",
                    "rightExpression": queues["Orders"],
                    "variableName": "queueId",
                    "asObject": False,
                    "dlpOption": False,
                    "wfmOption": False,
                    "dashboard": False,
                    "condition": {
                        "conditionType": "AND",
                        "expressions": [
                            {
                                "leftExpression": "workitem.data.interest",
                                "operator": "==",
                                "rightExpression": "'Orders'",
                            }
                        ],
                    },
                },
                "type": "savevariable",
                "_selected": False,
            },
            {
                "icon": "icon-save",
                "name": "Save Variable",
                "description": "",
                "properties": {
                    "description": "queueId - Orders",
                    "rightExpression": queues["Orders"],
                    "variableName": "queueId",
                    "asObject": False,
                    "dlpOption": False,
                    "wfmOption": False,
                    "dashboard": False,
                    "condition": {
                        "conditionType": "AND",
                        "expressions": [
                            {
                                "leftExpression": "workitem.data.interest",
                                "operator": "==",
                                "rightExpression": "'Stock Availability'",
                            }
                        ],
                    },
                },
                "type": "savevariable",
                "_selected": False,
                "id": "refId1739749451080",
            },
            {
                "icon": "icon-save",
                "name": "Save Variable",
                "description": "",
                "properties": {
                    "description": "queueId - Exchanges",
                    "rightExpression": queues["Exchanges"],
                    "variableName": "queueId",
                    "asObject": False,
                    "dlpOption": False,
                    "wfmOption": False,
                    "dashboard": False,
                    "condition": {
                        "conditionType": "AND",
                        "expressions": [
                            {
                                "leftExpression": "workitem.data.interest",
                                "operator": "==",
                                "rightExpression": "'Exchanges'",
                            }
                        ],
                    },
                },
                "type": "savevariable",
                "_selected": False,
                "id": "refId1739749451080",
            },
            {
                "icon": "icon-save",
                "name": "Save Variable",
                "description": "",
                "properties": {
                    "description": "queueId - Billing",
                    "rightExpression": queues["Billing"],
                    "variableName": "queueId",
                    "asObject": False,
                    "dlpOption": False,
                    "wfmOption": False,
                    "dashboard": False,
                    "condition": {
                        "conditionType": "AND",
                        "expressions": [
                            {
                                "leftExpression": "workitem.data.interest",
                                "operator": "==",
                                "rightExpression": "'Billing'",
                            }
                        ],
                    },
                },
                "type": "savevariable",
                "_selected": False,
                "id": "refId1739749451048",
            },
            {
                "icon": "icon-save",
                "name": "Save Variable",
                "description": "",
                "properties": {
                    "description": "queueId - Customer Service",
                    "rightExpression": queues["Customer Service"],
                    "variableName": "queueId",
                    "asObject": False,
                    "dlpOption": False,
                    "wfmOption": False,
                    "dashboard": False,
                    "condition": {
                        "conditionType": "AND",
                        "expressions": [
                            {
                                "leftExpression": "workitem.data.interest",
                                "operator": "==",
                                "rightExpression": "'Customer Service'",
                            }
                        ],
                    },
                },
                "type": "savevariable",
                "_selected": False,
                "id": "refId1739749451048",
            },
        ]
        inbound_call_variables = [
            {
                "name": "Save Variable",
                "description": "",
                "properties": {
                    "description": "queueId - Orders",
                    "rightExpression": queues["Orders"],
                    "variableName": "queueId",
                    "asObject": False,
                    "dlpOption": False,
                    "wfmOption": False,
                    "dashboard": False,
                    "condition": {
                        "conditionType": "AND",
                        "expressions": [
                            {
                                "operator": "==",
                                "leftExpression": "workitem.digits",
                                "rightExpression": "'1'",
                            }
                        ],
                    },
                },
                "type": "savevariable",
                "_selected": False,
                "icon": "icon-save",
                "id": "refId1739600231288",
            },
            {
                "name": "Save Variable",
                "description": "",
                "properties": {
                    "description": "queueId - Orders",
                    "rightExpression": queues["Orders"],
                    "variableName": "queueId",
                    "asObject": False,
                    "dlpOption": False,
                    "wfmOption": False,
                    "dashboard": False,
                    "condition": {
                        "conditionType": "AND",
                        "expressions": [
                            {
                                "operator": "==",
                                "leftExpression": "workitem.digits",
                                "rightExpression": "'2'",
                            }
                        ],
                    },
                },
                "type": "savevariable",
                "_selected": False,
                "id": "refId1739600231289",
                "icon": "icon-save",
            },
            {
                "name": "Save Variable",
                "description": "",
                "properties": {
                    "description": "queueId - Exchanges",
                    "rightExpression": queues["Exchanges"],
                    "variableName": "queueId",
                    "asObject": False,
                    "dlpOption": False,
                    "wfmOption": False,
                    "dashboard": False,
                    "condition": {
                        "conditionType": "AND",
                        "expressions": [
                            {
                                "operator": "==",
                                "leftExpression": "workitem.digits",
                                "rightExpression": "'3'",
                            }
                        ],
                    },
                },
                "type": "savevariable",
                "_selected": False,
                "id": "refId1739600231289",
                "icon": "icon-save",
            },
            {
                "name": "Save Variable",
                "description": "",
                "properties": {
                    "description": "queueId - Billing",
                    "rightExpression": queues["Billing"],
                    "variableName": "queueId",
                    "asObject": False,
                    "dlpOption": False,
                    "wfmOption": False,
                    "dashboard": False,
                    "condition": {
                        "conditionType": "AND",
                        "expressions": [
                            {
                                "operator": "==",
                                "leftExpression": "workitem.digits",
                                "rightExpression": "'4'",
                            }
                        ],
                    },
                },
                "type": "savevariable",
                "_selected": False,
                "id": "refId1739600231291",
                "icon": "icon-save",
            },
            {
                "name": "Save Variable",
                "description": "",
                "properties": {
                    "description": "queueId - Customer Service",
                    "rightExpression": queues["Customer Service"],
                    "variableName": "queueId",
                    "asObject": False,
                    "dlpOption": False,
                    "wfmOption": False,
                    "dashboard": False,
                    "condition": {
                        "conditionType": "AND",
                        "expressions": [
                            {
                                "operator": "==",
                                "leftExpression": "workitem.digits",
                                "rightExpression": "'5'",
                            }
                        ],
                    },
                },
                "type": "savevariable",
                "_selected": False,
                "id": "refId1739600231291",
                "icon": "icon-save",
            },
        ]
        outbound_call_variables = [
            {
                "name": "Save Variable",
                "description": "",
                "properties": {
                    "description": "queueId - Orders",
                    "rightExpression": queues["Orders"],
                    "variableName": "queueId",
                    "asObject": False,
                    "dlpOption": False,
                    "wfmOption": False,
                    "dashboard": False,
                    "condition": {
                        "conditionType": "AND",
                        "expressions": [
                            {
                                "leftExpression": "workitem.data.interest",
                                "operator": "==",
                                "rightExpression": "'Orders'",
                            }
                        ],
                    },
                },
                "type": "savevariable",
                "_selected": False,
                "id": "refId1739934455753",
                "icon": "icon-save",
            },
            {
                "name": "Save Variable",
                "description": "",
                "properties": {
                    "description": "queueId - Orders",
                    "rightExpression": queues["Orders"],
                    "variableName": "queueId",
                    "asObject": False,
                    "dlpOption": False,
                    "wfmOption": False,
                    "dashboard": False,
                    "condition": {
                        "conditionType": "AND",
                        "expressions": [
                            {
                                "leftExpression": "workitem.data.interest",
                                "operator": "==",
                                "rightExpression": "'Stock Availability'",
                            }
                        ],
                    },
                },
                "type": "savevariable",
                "_selected": False,
                "id": "refId1739934455754",
                "icon": "icon-save",
            },
            {
                "name": "Save Variable",
                "description": "",
                "properties": {
                    "description": "queueId - Exchanges",
                    "rightExpression": queues["Exchanges"],
                    "variableName": "queueId",
                    "asObject": False,
                    "dlpOption": False,
                    "wfmOption": False,
                    "dashboard": False,
                    "condition": {
                        "conditionType": "AND",
                        "expressions": [
                            {
                                "leftExpression": "workitem.data.interest",
                                "operator": "==",
                                "rightExpression": "'Exchanges'",
                            }
                        ],
                    },
                },
                "type": "savevariable",
                "_selected": False,
                "id": "refId1739934455754",
                "icon": "icon-save",
            },
            {
                "name": "Save Variable",
                "description": "",
                "properties": {
                    "description": "queueId - Billing",
                    "rightExpression": queues["Billing"],
                    "variableName": "queueId",
                    "asObject": False,
                    "dlpOption": False,
                    "wfmOption": False,
                    "dashboard": False,
                    "condition": {
                        "conditionType": "AND",
                        "expressions": [
                            {
                                "leftExpression": "workitem.data.interest",
                                "operator": "==",
                                "rightExpression": "'Billing'",
                            }
                        ],
                    },
                },
                "type": "savevariable",
                "_selected": False,
                "id": "refId1739934455755",
                "icon": "icon-save",
            },
            {
                "name": "Save Variable",
                "description": "",
                "properties": {
                    "description": "queueId - Customer Service",
                    "rightExpression": queues["Customer Service"],
                    "variableName": "queueId",
                    "asObject": False,
                    "dlpOption": False,
                    "wfmOption": False,
                    "dashboard": False,
                    "condition": {
                        "conditionType": "AND",
                        "expressions": [
                            {
                                "leftExpression": "workitem.data.interest",
                                "operator": "==",
                                "rightExpression": "'Customer Service'",
                            }
                        ],
                    },
                },
                "type": "savevariable",
                "_selected": False,
                "id": "refId1739934455756",
                "icon": "icon-save",
            },
            {
                "name": "Survey",
                "description": "Assign survey to workitem",
                "properties": {
                    "description": user_survey["name"],
                    "condition": {
                        "conditionType": "NONE",
                        "expressions": [{"operator": "=="}],
                    },
                    "surveyId": user_survey["_id"],
                    "expansions": {"surveyId": {"name": user_survey["name"]}},
                    "_working": False,
                },
                "type": "assignsurvey",
                "_selected": False,
                "id": "refId1739934455757",
                "icon": "icon-survey",
            },
        ]
    elif vertical == "pubsec":
        inbound_call_menu = '<prosody pitch="-2st">To report a pothole, press 1. To report an abandoned vehicle, press 2. To report a missed trash pickup, press 3. For billing, press 4. Otherwise, please stay on the line.</prosody>'
        chat_variables = [
            {
                "icon": "icon-save",
                "name": "Save Variable",
                "description": "",
                "properties": {
                    "description": "queueId - Maintenance",
                    "rightExpression": queues["Maintenance"],
                    "variableName": "queueId",
                    "asObject": False,
                    "dlpOption": False,
                    "wfmOption": False,
                    "dashboard": False,
                    "condition": {
                        "conditionType": "AND",
                        "expressions": [
                            {
                                "leftExpression": "workitem.data.interest",
                                "operator": "==",
                                "rightExpression": "'Pothole'",
                            }
                        ],
                    },
                },
                "type": "savevariable",
                "_selected": False,
            },
            {
                "icon": "icon-save",
                "name": "Save Variable",
                "description": "",
                "properties": {
                    "description": "queueId - Vehicle Services",
                    "rightExpression": queues["Vehicle Services"],
                    "variableName": "queueId",
                    "asObject": False,
                    "dlpOption": False,
                    "wfmOption": False,
                    "dashboard": False,
                    "condition": {
                        "conditionType": "AND",
                        "expressions": [
                            {
                                "leftExpression": "workitem.data.interest",
                                "operator": "==",
                                "rightExpression": "'Abandoned Vehicle'",
                            }
                        ],
                    },
                },
                "type": "savevariable",
                "_selected": False,
                "id": "refId1739749451080",
            },
            {
                "icon": "icon-save",
                "name": "Save Variable",
                "description": "",
                "properties": {
                    "description": "queueId - Waste Management",
                    "rightExpression": queues["Waste Management"],
                    "variableName": "queueId",
                    "asObject": False,
                    "dlpOption": False,
                    "wfmOption": False,
                    "dashboard": False,
                    "condition": {
                        "conditionType": "AND",
                        "expressions": [
                            {
                                "leftExpression": "workitem.data.interest",
                                "operator": "==",
                                "rightExpression": "'Missed Trash Pickup'",
                            }
                        ],
                    },
                },
                "type": "savevariable",
                "_selected": False,
                "id": "refId1739749451080",
            },
            {
                "icon": "icon-save",
                "name": "Save Variable",
                "description": "",
                "properties": {
                    "description": "queueId - Billing",
                    "rightExpression": queues["Billing"],
                    "variableName": "queueId",
                    "asObject": False,
                    "dlpOption": False,
                    "wfmOption": False,
                    "dashboard": False,
                    "condition": {
                        "conditionType": "AND",
                        "expressions": [
                            {
                                "leftExpression": "workitem.data.interest",
                                "operator": "==",
                                "rightExpression": "'Billing'",
                            }
                        ],
                    },
                },
                "type": "savevariable",
                "_selected": False,
                "id": "refId1739749451048",
            },
            {
                "icon": "icon-save",
                "name": "Save Variable",
                "description": "",
                "properties": {
                    "description": "queueId - Customer Service",
                    "rightExpression": queues["Customer Service"],
                    "variableName": "queueId",
                    "asObject": False,
                    "dlpOption": False,
                    "wfmOption": False,
                    "dashboard": False,
                    "condition": {
                        "conditionType": "AND",
                        "expressions": [
                            {
                                "leftExpression": "workitem.data.interest",
                                "operator": "==",
                                "rightExpression": "'Other'",
                            }
                        ],
                    },
                },
                "type": "savevariable",
                "_selected": False,
                "id": "refId1739749451048",
            },
        ]
        inbound_call_variables = [
            {
                "name": "Save Variable",
                "description": "",
                "properties": {
                    "description": "queueId - Maintenance",
                    "rightExpression": queues["Maintenance"],
                    "variableName": "queueId",
                    "asObject": False,
                    "dlpOption": False,
                    "wfmOption": False,
                    "dashboard": False,
                    "condition": {
                        "conditionType": "AND",
                        "expressions": [
                            {
                                "operator": "==",
                                "leftExpression": "workitem.digits",
                                "rightExpression": "'1'",
                            }
                        ],
                    },
                },
                "type": "savevariable",
                "_selected": False,
                "icon": "icon-save",
                "id": "refId1739600231288",
            },
            {
                "name": "Save Variable",
                "description": "",
                "properties": {
                    "description": "queueId - Vehicle Services",
                    "rightExpression": queues["Vehicle Services"],
                    "variableName": "queueId",
                    "asObject": False,
                    "dlpOption": False,
                    "wfmOption": False,
                    "dashboard": False,
                    "condition": {
                        "conditionType": "AND",
                        "expressions": [
                            {
                                "operator": "==",
                                "leftExpression": "workitem.digits",
                                "rightExpression": "'2'",
                            }
                        ],
                    },
                },
                "type": "savevariable",
                "_selected": False,
                "id": "refId1739600231289",
                "icon": "icon-save",
            },
            {
                "name": "Save Variable",
                "description": "",
                "properties": {
                    "description": "queueId - Waste Management",
                    "rightExpression": queues["Waste Management"],
                    "variableName": "queueId",
                    "asObject": False,
                    "dlpOption": False,
                    "wfmOption": False,
                    "dashboard": False,
                    "condition": {
                        "conditionType": "AND",
                        "expressions": [
                            {
                                "operator": "==",
                                "leftExpression": "workitem.digits",
                                "rightExpression": "'3'",
                            }
                        ],
                    },
                },
                "type": "savevariable",
                "_selected": False,
                "id": "refId1739600231289",
                "icon": "icon-save",
            },
            {
                "name": "Save Variable",
                "description": "",
                "properties": {
                    "description": "queueId - Billing",
                    "rightExpression": queues["Billing"],
                    "variableName": "queueId",
                    "asObject": False,
                    "dlpOption": False,
                    "wfmOption": False,
                    "dashboard": False,
                    "condition": {
                        "conditionType": "AND",
                        "expressions": [
                            {
                                "operator": "==",
                                "leftExpression": "workitem.digits",
                                "rightExpression": "'4'",
                            }
                        ],
                    },
                },
                "type": "savevariable",
                "_selected": False,
                "id": "refId1739600231291",
                "icon": "icon-save",
            },
        ]
        outbound_call_variables = [
            {
                "name": "Save Variable",
                "description": "",
                "properties": {
                    "description": "queueId - Maintenance",
                    "rightExpression": queues["Maintenance"],
                    "variableName": "queueId",
                    "asObject": False,
                    "dlpOption": False,
                    "wfmOption": False,
                    "dashboard": False,
                    "condition": {
                        "conditionType": "AND",
                        "expressions": [
                            {
                                "leftExpression": "workitem.data.interest",
                                "operator": "==",
                                "rightExpression": "'Pothole'",
                            }
                        ],
                    },
                },
                "type": "savevariable",
                "_selected": False,
                "id": "refId1739934455753",
                "icon": "icon-save",
            },
            {
                "name": "Save Variable",
                "description": "",
                "properties": {
                    "description": "queueId - Vehicle Services",
                    "rightExpression": queues["Vehicle Services"],
                    "variableName": "queueId",
                    "asObject": False,
                    "dlpOption": False,
                    "wfmOption": False,
                    "dashboard": False,
                    "condition": {
                        "conditionType": "AND",
                        "expressions": [
                            {
                                "leftExpression": "workitem.data.interest",
                                "operator": "==",
                                "rightExpression": "'Abandoned Vehicle'",
                            }
                        ],
                    },
                },
                "type": "savevariable",
                "_selected": False,
                "id": "refId1739934455754",
                "icon": "icon-save",
            },
            {
                "name": "Save Variable",
                "description": "",
                "properties": {
                    "description": "queueId - Waste Management",
                    "rightExpression": queues["Waste Management"],
                    "variableName": "queueId",
                    "asObject": False,
                    "dlpOption": False,
                    "wfmOption": False,
                    "dashboard": False,
                    "condition": {
                        "conditionType": "AND",
                        "expressions": [
                            {
                                "leftExpression": "workitem.data.interest",
                                "operator": "==",
                                "rightExpression": "'Missed Trash Pickup'",
                            }
                        ],
                    },
                },
                "type": "savevariable",
                "_selected": False,
                "id": "refId1739934455754",
                "icon": "icon-save",
            },
            {
                "name": "Save Variable",
                "description": "",
                "properties": {
                    "description": "queueId - Billing",
                    "rightExpression": queues["Billing"],
                    "variableName": "queueId",
                    "asObject": False,
                    "dlpOption": False,
                    "wfmOption": False,
                    "dashboard": False,
                    "condition": {
                        "conditionType": "AND",
                        "expressions": [
                            {
                                "leftExpression": "workitem.data.interest",
                                "operator": "==",
                                "rightExpression": "'Billing'",
                            }
                        ],
                    },
                },
                "type": "savevariable",
                "_selected": False,
                "id": "refId1739934455755",
                "icon": "icon-save",
            },
            {
                "name": "Save Variable",
                "description": "",
                "properties": {
                    "description": "queueId - Customer Service",
                    "rightExpression": queues["Customer Service"],
                    "variableName": "queueId",
                    "asObject": False,
                    "dlpOption": False,
                    "wfmOption": False,
                    "dashboard": False,
                    "condition": {
                        "conditionType": "AND",
                        "expressions": [
                            {
                                "leftExpression": "workitem.data.interest",
                                "operator": "==",
                                "rightExpression": "'Other'",
                            }
                        ],
                    },
                },
                "type": "savevariable",
                "_selected": False,
                "id": "refId1739934455756",
                "icon": "icon-save",
            },
            {
                "name": "Survey",
                "description": "Assign survey to workitem",
                "properties": {
                    "description": user_survey["name"],
                    "condition": {
                        "conditionType": "NONE",
                        "expressions": [{"operator": "=="}],
                    },
                    "surveyId": user_survey["_id"],
                    "expansions": {"surveyId": {"name": user_survey["name"]}},
                    "_working": False,
                },
                "type": "assignsurvey",
                "_selected": False,
                "id": "refId1739934455757",
                "icon": "icon-survey",
            },
        ]

    # Modify workflow body
    if "67b11b3a4492457796ee0690" in workflow_body["states"]:
        chat_actions = workflow_body["states"]["67b11b3a4492457796ee0690"]["actions"]
        for chat_variable in chat_variables:
            chat_actions.insert(-1, chat_variable)
    if "67b11b424881f97a86b2640f" in workflow_body["states"]:
        if (
            workflow_body["states"]["67b11b424881f97a86b2640f"]["actions"][0]["type"]
            == "googlettscollect"
        ):
            workflow_body["states"]["67b11b424881f97a86b2640f"]["actions"][0][
                "properties"
            ]["text"] = inbound_call_menu
        inbound_call_actions = workflow_body["states"]["67b11b424881f97a86b2640f"][
            "actions"
        ]
        for inbound_call_variable in inbound_call_variables:
            inbound_call_actions.insert(-1, inbound_call_variable)
    if "67b552f294171b486a3d1b7a" in workflow_body["states"]:
        outbound_call_actions = workflow_body["states"]["67b552f294171b486a3d1b7a"][
            "actions"
        ]
        for outbound_call_variable in outbound_call_variables:
            outbound_call_actions.insert(-1, outbound_call_variable)

    payload = json.dumps(workflow_body)
    headers = {
        "Authorization": ncc_token,
        "Content-Type": "application/json",
    }
    try:
        conn.request("POST", "/data/api/types/workflow/", payload, headers)
        res = conn.getresponse()
        if res.status == 201:
            data = res.read().decode("utf-8")
            workflow = json.loads(data)
    except:
        pass
    conn.close()
    return workflow


def create_direct_line_workflow(
    ncc_location: str,
    ncc_token: str,
    workflow_name: str,
    business_name: str,
    queues: dict,
    search_contacts_function: dict,
    two_way_chat_function: dict,
    two_way_sms_function: dict,
    prompt: dict,
    acd_voicemail_function: dict,
    acd_callback_function: dict,
    user_survey: dict,
) -> dict:
    """
    This function creates a workflow in Nextiva Contact Center (NCC).
    """
    workflow = {}
    conn = http.client.HTTPSConnection(ncc_location)
    payload = json.dumps(
        {
            "maxActions": 10000,
            "localizations": {
                "name": {"en": {"language": "en", "value": workflow_name}},
                "description": {"en": {"language": "en", "value": "Direct workflow"}},
            },
            "description": "Direct workflow",
            "states": {
                "67b1186f5510d9081ac8e32b": {
                    "category": "Standard",
                    "campaignStateId": "67b1186f5510d9081ac8e32b",
                    "actions": [
                        {
                            "name": "ACD Voicemail From Expression",
                            "description": "Create ACD Voicemail",
                            "properties": {
                                "transcription": True,
                                "priority": 3,
                                "queueIdsExpression": "workitem.data.queueId",
                                "toAddress": "",
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "operator": "==",
                                            "leftExpression": "workitem.data.messageRecorded",
                                            "rightExpression": "1",
                                        }
                                    ],
                                },
                                "description": "Create ACD Voicemail",
                            },
                            "type": "acdvmfromexpression",
                            "_selected": False,
                            "id": "refId1723818900554",
                            "icon": "icon-directconnect",
                        },
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
                        },
                    ],
                    "objectType": "campaignstate",
                    "key": "67b1186f5510d9081ac8e32b",
                    "_id": "67b1186f5510d9081ac8e32b",
                    "description": "End State",
                    "name": "End State",
                    "location": "-147.23017129888294 34.91808770109185",
                    "transitions": [],
                },
                "start-state": {
                    "category": "Begin",
                    "campaignStateId": "start-state",
                    "actions": [
                        {
                            "name": "Save Variable",
                            "description": "",
                            "properties": {
                                "description": "companyName",
                                "rightExpression": business_name,
                                "variableName": "companyName",
                                "asObject": False,
                                "dlpOption": False,
                                "wfmOption": False,
                                "dashboard": False,
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                            },
                            "type": "savevariable",
                            "_selected": False,
                            "id": "refId1739600227611",
                            "icon": "icon-save",
                        },
                        {
                            "icon": "icon-save",
                            "name": "Save Variable",
                            "description": "",
                            "properties": {
                                "description": "sourceLanguage",
                                "rightExpression": "en",
                                "variableName": "sourceLanguage",
                                "asObject": False,
                                "dlpOption": False,
                                "wfmOption": False,
                                "dashboard": False,
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                            },
                            "type": "savevariable",
                            "_selected": False,
                        },
                        {
                            "name": "Save Variable",
                            "description": "",
                            "properties": {
                                "description": "contactFound",
                                "rightExpression": "false",
                                "variableName": "contactFound",
                                "asObject": True,
                                "dlpOption": False,
                                "wfmOption": False,
                                "dashboard": False,
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                            },
                            "type": "savevariable",
                            "_selected": False,
                            "id": "refId1739600227612",
                            "icon": "icon-save",
                        },
                        {
                            "name": "Save Variable",
                            "description": "",
                            "properties": {
                                "description": "contactConfirmed",
                                "rightExpression": "false",
                                "variableName": "contactConfirmed",
                                "asObject": True,
                                "dlpOption": False,
                                "wfmOption": False,
                                "dashboard": False,
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                            },
                            "type": "savevariable",
                            "_selected": False,
                            "id": "refId1739600227613",
                            "icon": "icon-save",
                        },
                        {
                            "icon": "icon-save",
                            "name": "Save Variable",
                            "description": "",
                            "properties": {
                                "description": "phone (Chat)",
                                "rightExpression": "workitem.data.context.consumerData.phone",
                                "variableName": "phone",
                                "asObject": False,
                                "dlpOption": False,
                                "wfmOption": False,
                                "dashboard": False,
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.type",
                                            "operator": "==",
                                            "rightExpression": "'Chat'",
                                        }
                                    ],
                                },
                            },
                            "type": "savevariable",
                            "_selected": False,
                            "id": "refId1741893969929",
                        },
                        {
                            "name": "Save Variable",
                            "description": "",
                            "properties": {
                                "description": "phone (InboundCall or InboundSMS)",
                                "rightExpression": "workitem.from.slice(-10)",
                                "variableName": "phone",
                                "asObject": False,
                                "dlpOption": False,
                                "wfmOption": False,
                                "dashboard": False,
                                "condition": {
                                    "conditionType": "OR",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.type",
                                            "operator": "==",
                                            "rightExpression": "'InboundCall'",
                                        },
                                        {
                                            "leftExpression": "workitem.type",
                                            "operator": "==",
                                            "rightExpression": "'InboundSMS'",
                                        },
                                    ],
                                },
                            },
                            "type": "savevariable",
                            "_selected": False,
                            "id": "refId1741893969877",
                            "icon": "icon-save",
                        },
                        {
                            "name": "Save Variable",
                            "description": "",
                            "properties": {
                                "description": "phone (OutboundCall or OutboundSMS)",
                                "rightExpression": "workitem.to.slice(-10)",
                                "variableName": "phone",
                                "asObject": False,
                                "dlpOption": False,
                                "wfmOption": False,
                                "dashboard": False,
                                "condition": {
                                    "conditionType": "OR",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.type",
                                            "operator": "==",
                                            "rightExpression": "'OutboundCall'",
                                        },
                                        {
                                            "leftExpression": "workitem.type",
                                            "operator": "==",
                                            "rightExpression": "'OutboundSMS'",
                                        },
                                    ],
                                },
                            },
                            "type": "savevariable",
                            "_selected": False,
                            "id": "refId1741893969878",
                            "icon": "icon-save",
                        },
                        {
                            "icon": "icon-save",
                            "name": "Save Variable",
                            "description": "",
                            "properties": {
                                "description": "priority",
                                "rightExpression": "Standard",
                                "variableName": "priority",
                                "asObject": False,
                                "dlpOption": False,
                                "wfmOption": False,
                                "dashboard": False,
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                            },
                            "type": "savevariable",
                            "_selected": False,
                        },
                        {
                            "name": "Save Variable",
                            "description": "",
                            "properties": {
                                "description": "queueId",
                                "rightExpression": queues["Customer Service"],
                                "variableName": "queueId",
                                "asObject": False,
                                "dlpOption": False,
                                "wfmOption": False,
                                "dashboard": False,
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                            },
                            "type": "savevariable",
                            "_selected": False,
                            "icon": "icon-save",
                            "id": "refId1739600227615",
                        },
                        {
                            "name": "Survey",
                            "description": "Transition to another state",
                            "properties": {
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.type",
                                            "operator": "==",
                                            "rightExpression": "'Survey'",
                                        }
                                    ],
                                },
                                "stateName": "Survey",
                                "description": "Transition to another state",
                            },
                            "type": "transitionbyname",
                            "_selected": False,
                            "transitionId": "refId1739600227151",
                            "id": "refId1739600227616",
                            "icon": "icon-transition",
                        },
                        {
                            "icon": "icon-ai-message",
                            "name": "Chat Message Consumer",
                            "description": "Thank you for contacting...",
                            "properties": {
                                "description": "Thank you for contacting...",
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.type",
                                            "operator": "==",
                                            "rightExpression": "'Chat'",
                                        }
                                    ],
                                },
                                "from": "workitem.data.companyName",
                                "message": "Thank you for contacting ${workitem.data.companyName}.",
                                "messageType": "BOT",
                                "options": [],
                            },
                            "type": "chatmessageconsumer",
                            "_selected": False,
                        },
                        {
                            "icon": "icon-tts",
                            "name": "Synthesize Text via Google TTS",
                            "description": "Thank you for contacting...",
                            "properties": {
                                "description": "Thank you for contacting...",
                                "voiceName": "en-US-Wavenet-J",
                                "text": '<prosody pitch="-2st">Thank you for contacting ${workitem.data.companyName}.</prosody>',
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.type",
                                            "operator": "==",
                                            "rightExpression": "'InboundCall'",
                                        }
                                    ],
                                },
                            },
                            "type": "googletts",
                            "_selected": False,
                        },
                        {
                            "name": "Search Contacts",
                            "type": "transition",
                            "description": "Transition to another state",
                            "properties": {
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "stateId": "67b11894720280f716c36bdf",
                                "name": "Start",
                                "description": "Transition to another state",
                            },
                            "transitionId": "67b118871e7c034010972864",
                            "_selected": False,
                            "id": "refId1739600227617",
                            "icon": "icon-transition",
                        },
                    ],
                    "transitions": [
                        {"name": "Survey", "id": "refId1739600227151"},
                        {"name": "Search Contacts", "id": "67b118871e7c034010972864"},
                    ],
                    "objectType": "campaignstate",
                    "key": "start-state",
                    "_id": "start-state",
                    "description": "Begin State",
                    "name": "Begin State",
                    "location": "-92.43594451534577 -158.49227385694343",
                },
                "67b11894720280f716c36bdf": {
                    "category": "Standard",
                    "objectType": "campaignstate",
                    "campaignStateId": "67b11894720280f716c36bdf",
                    "name": "Search Contacts",
                    "description": "Newly Created State",
                    "actions": [
                        {
                            "name": "Execute Function",
                            "description": "",
                            "properties": {
                                "description": "Search Contacts",
                                "functionId": search_contacts_function["_id"],
                                "functionExpression": "",
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "expansions": {
                                    "functionId": {
                                        "name": search_contacts_function["name"]
                                    }
                                },
                                "_working": False,
                            },
                            "type": "function",
                            "_selected": False,
                            "id": "refId1740106542548",
                            "icon": "icon-function",
                        },
                        {
                            "name": "Chat",
                            "description": "Transition to another state",
                            "properties": {
                                "description": "Transition to another state",
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.type",
                                            "operator": "==",
                                            "rightExpression": "'Chat'",
                                        }
                                    ],
                                },
                                "stateId": "67b11b3a4492457796ee0690",
                                "points": {
                                    "h": True,
                                    "r": [
                                        {
                                            "b": 248.88010230206072,
                                            "k": 47.062687281791156,
                                            "h": True,
                                        },
                                        {
                                            "b": 258.8801023020607,
                                            "k": 47.062687281791156,
                                            "h": True,
                                        },
                                        {"b": 260, "k": 47.062687281791156, "h": True},
                                        {"b": 260, "k": 47.062687281791156, "h": True},
                                        {
                                            "b": 480.78544785048666,
                                            "k": 47.062687281791156,
                                            "h": True,
                                        },
                                        {
                                            "b": 480.78544785048666,
                                            "k": 139.9649305004943,
                                            "h": True,
                                        },
                                        {
                                            "b": 480.78544785048666,
                                            "k": 149.9649305004943,
                                            "h": True,
                                        },
                                    ],
                                    "ct": 7,
                                    "__gohashid": 60756,
                                },
                            },
                            "type": "transition",
                            "_selected": False,
                            "transitionId": "refId1739600227187",
                            "id": "refId1740106542549",
                            "icon": "icon-transition",
                        },
                        {
                            "name": "InboundCall",
                            "description": "Transition to another state",
                            "properties": {
                                "description": "Transition to another state",
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.type",
                                            "operator": "==",
                                            "rightExpression": "'InboundCall'",
                                        }
                                    ],
                                },
                                "stateId": "67b11b424881f97a86b2640f",
                                "points": {
                                    "h": True,
                                    "r": [
                                        {
                                            "b": 248.88010230206072,
                                            "k": 91.06268728179116,
                                            "h": True,
                                        },
                                        {
                                            "b": 258.8801023020607,
                                            "k": 91.06268728179116,
                                            "h": True,
                                        },
                                        {"b": 260, "k": 91.06268728179116, "h": True},
                                        {"b": 260, "k": 292, "h": True},
                                        {"b": 476.13146320255123, "k": 292, "h": True},
                                        {
                                            "b": 476.13146320255123,
                                            "k": 335.43228571378717,
                                            "h": True,
                                        },
                                        {
                                            "b": 476.13146320255123,
                                            "k": 345.43228571378717,
                                            "h": True,
                                        },
                                    ],
                                    "ct": 7,
                                    "__gohashid": 60757,
                                },
                            },
                            "type": "transition",
                            "_selected": False,
                            "transitionId": "refId1739600227163",
                            "id": "refId1740106542550",
                            "icon": "icon-transition",
                        },
                        {
                            "name": "InboundSMS",
                            "description": "Transition to another state",
                            "properties": {
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.type",
                                            "operator": "==",
                                            "rightExpression": "'InboundSMS'",
                                        }
                                    ],
                                },
                                "stateId": "67b11b4990b64c67bfb0e882",
                                "points": {
                                    "h": True,
                                    "r": [
                                        {
                                            "b": 248.88010230206072,
                                            "k": 135.06268728179117,
                                            "h": True,
                                        },
                                        {
                                            "b": 258.8801023020607,
                                            "k": 135.06268728179117,
                                            "h": True,
                                        },
                                        {"b": 260, "k": 135.06268728179117, "h": True},
                                        {"b": 260, "k": 484, "h": True},
                                        {"b": 471.4774785546159, "k": 484, "h": True},
                                        {
                                            "b": 471.4774785546159,
                                            "k": 516.9376869832739,
                                            "h": True,
                                        },
                                        {
                                            "b": 471.4774785546159,
                                            "k": 526.9376869832739,
                                            "h": True,
                                        },
                                    ],
                                    "ct": 7,
                                    "__gohashid": 60758,
                                },
                                "description": "Transition to another state",
                            },
                            "type": "transition",
                            "_selected": False,
                            "transitionId": "refId1739600227203",
                            "icon": "icon-transition",
                            "id": "refId1740106542551",
                        },
                        {
                            "icon": "icon-transition",
                            "name": "OutboundCall",
                            "description": "Transition to another state",
                            "properties": {
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.type",
                                            "operator": "==",
                                            "rightExpression": "'OutboundCall'",
                                        }
                                    ],
                                },
                                "stateId": "67b80e6253218fc5093deb5c",
                            },
                            "type": "transition",
                            "_selected": False,
                            "transitionId": "refId1740106542563",
                        },
                        {
                            "icon": "icon-transition",
                            "name": "Email",
                            "description": "Transition to another state",
                            "properties": {
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.type",
                                            "operator": "==",
                                            "rightExpression": "'Email'",
                                        }
                                    ],
                                },
                                "stateId": "67bea6ccb1b61fed3ca6b744",
                            },
                            "type": "transition",
                            "_selected": False,
                            "transitionId": "refId1740544931036",
                        },
                        {
                            "icon": "icon-transition",
                            "name": "OutboundSMS",
                            "description": "Transition to another state",
                            "properties": {
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.type",
                                            "operator": "==",
                                            "rightExpression": "'OutboundSMS'",
                                        }
                                    ],
                                },
                                "stateId": "68d7114766b31902e3ebc111",
                            },
                            "type": "transition",
                            "_selected": False,
                            "transitionId": "refId1758920143843",
                        },
                    ],
                    "_id": "67b11894720280f716c36bdf",
                    "key": "67b11894720280f716c36bdf",
                    "location": "165.88010230206072 74.17868078154703",
                    "transitions": [
                        {"name": "Chat", "id": "refId1739600227187"},
                        {"name": "InboundCall", "id": "refId1739600227163"},
                        {"name": "InboundSMS", "id": "refId1739600227203"},
                        {"name": "OutboundCall", "id": "refId1740106542563"},
                        {"name": "Email", "id": "refId1740544931036"},
                        {"name": "OutboundSMS", "id": "refId1758920143843"},
                    ],
                },
                "67b11b35410f937347fe9aee": {
                    "category": "Standard",
                    "objectType": "campaignstate",
                    "campaignStateId": "67b11b35410f937347fe9aee",
                    "name": "Survey",
                    "description": "Newly Created State",
                    "actions": [
                        {
                            "icon": "icon-transition",
                            "name": "End State",
                            "description": "Transition to another state",
                            "properties": {
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "stateName": "End State",
                            },
                            "type": "transitionbyname",
                            "_selected": False,
                            "transitionId": "refId1739600226811",
                        }
                    ],
                    "_id": "67b11b35410f937347fe9aee",
                    "key": "67b11b35410f937347fe9aee",
                    "location": "484.89646762282933 -76.7578027276301",
                    "transitions": [{"name": "End State", "id": "refId1739600226811"}],
                },
                "67b11b3a4492457796ee0690": {
                    "category": "Standard",
                    "objectType": "campaignstate",
                    "campaignStateId": "67b11b3a4492457796ee0690",
                    "name": "Chat",
                    "description": "Newly Created State",
                    "actions": [
                        {
                            "name": "ConnectAgent",
                            "description": "Transition to another state",
                            "properties": {
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "stateId": "67b11daace899acb3e0d1c38",
                                "description": "Transition to another state",
                            },
                            "type": "transition",
                            "_selected": False,
                            "transitionId": "refId1739600226839",
                            "id": "refId1739600229946",
                            "icon": "icon-transition",
                        },
                    ],
                    "_id": "67b11b3a4492457796ee0690",
                    "key": "67b11b3a4492457796ee0690",
                    "location": "480.78544785048666 214.34893700073843",
                    "transitions": [
                        {"name": "ConnectAgent", "id": "refId1739600226839"}
                    ],
                },
                "67b11b424881f97a86b2640f": {
                    "category": "Standard",
                    "objectType": "campaignstate",
                    "campaignStateId": "67b11b424881f97a86b2640f",
                    "name": "InboundCall",
                    "description": "Newly Created State",
                    "actions": [
                        {
                            "name": "ConnectAgent",
                            "description": "Transition to another state",
                            "properties": {
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "stateId": "67b11daace899acb3e0d1c38",
                                "description": "Transition to another state",
                            },
                            "type": "transition",
                            "_selected": False,
                            "transitionId": "refId1739600226869",
                            "icon": "icon-transition",
                            "id": "refId1739600229680",
                        },
                    ],
                    "_id": "67b11b424881f97a86b2640f",
                    "key": "67b11b424881f97a86b2640f",
                    "location": "476.13146320255123 409.81629221403136",
                    "transitions": [
                        {"name": "ConnectAgent", "id": "refId1739600226869"}
                    ],
                },
                "67b11b4990b64c67bfb0e882": {
                    "category": "Standard",
                    "objectType": "campaignstate",
                    "campaignStateId": "67b11b4990b64c67bfb0e882",
                    "name": "InboundSMS",
                    "description": "Newly Created State",
                    "actions": [
                        {
                            "icon": "icon-transition",
                            "name": "ConnectAgent",
                            "description": "Transition to another state",
                            "properties": {
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "stateId": "67b11daace899acb3e0d1c38",
                            },
                            "type": "transition",
                            "_selected": False,
                            "transitionId": "refId1739600229655",
                        }
                    ],
                    "_id": "67b11b4990b64c67bfb0e882",
                    "key": "67b11b4990b64c67bfb0e882",
                    "location": "471.4774785546159 591.3216934835181",
                    "transitions": [
                        {"name": "ConnectAgent", "id": "refId1739600229655"}
                    ],
                },
                "67b11daace899acb3e0d1c38": {
                    "category": "Standard",
                    "objectType": "campaignstate",
                    "campaignStateId": "67b11daace899acb3e0d1c38",
                    "name": "ConnectAgent",
                    "description": "Newly Created State",
                    "actions": [
                        {
                            "name": "Chat Message Consumer",
                            "description": "",
                            "properties": {
                                "description": "Please wait...",
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.type",
                                            "operator": "==",
                                            "rightExpression": "'Chat'",
                                        }
                                    ],
                                },
                                "from": "workitem.data.companyName",
                                "message": "Please wait while I transfer you to an agent who can assist you.",
                                "messageType": "BOT",
                                "options": [],
                            },
                            "type": "chatmessageconsumer",
                            "_selected": False,
                            "icon": "icon-ai-message",
                            "id": "refId1739600229770",
                        },
                        {
                            "name": "SMS Message Consumer",
                            "description": "",
                            "properties": {
                                "description": "Please wait...",
                                "message": "Please wait while I transfer you to an agent who can assist you.",
                                "toAddress": "workitem.from",
                                "fromAddress": "workitem.to",
                                "createNewWorkitem": False,
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.type",
                                            "operator": "==",
                                            "rightExpression": "'InboundSMS'",
                                        }
                                    ],
                                },
                            },
                            "type": "smsmessageconsumer",
                            "_selected": False,
                            "icon": "icon-ai-message",
                            "id": "refId1739600229771",
                        },
                        {
                            "name": "Synthesize Text via Google TTS",
                            "description": "Convert Text into Audio using Google's Text-To-Speech",
                            "properties": {
                                "voiceName": "en-US-Wavenet-J",
                                "text": '<prosody pitch="-2st">Please wait while I transfer you to an agent who can assist you.</prosody>',
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.type",
                                            "operator": "==",
                                            "rightExpression": "'InboundCall'",
                                        }
                                    ],
                                },
                                "description": "Please wait...",
                            },
                            "type": "googletts",
                            "_selected": False,
                            "id": "refId1739600229773",
                            "icon": "icon-tts",
                        },
                        {
                            "name": "Enter Queue from Expression",
                            "description": "",
                            "properties": {
                                "priorityExpression": "workitem.data.priority",
                                "queueIdsExpression": "workitem.data.queueId",
                                "ringAllEnabled": False,
                                "stickyEnabled": False,
                                "stickyUserType": "5",
                                "stickyDurationToWaitSeconds": 0,
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                            },
                            "type": "enterqueuefromexpression",
                            "_selected": False,
                            "id": "refId1739600229774",
                            "icon": "icon-enterqueues",
                        },
                        {
                            "name": "Execute Function",
                            "description": "",
                            "properties": {
                                "description": "Two way Chat conversation",
                                "functionId": two_way_chat_function["_id"],
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.type",
                                            "operator": "==",
                                            "rightExpression": "'Chat'",
                                        }
                                    ],
                                },
                                "expansions": {
                                    "functionId": {
                                        "name": two_way_chat_function["name"]
                                    }
                                },
                                "_working": False,
                            },
                            "type": "function",
                            "_selected": False,
                            "id": "refId1739600229775",
                            "icon": "icon-function",
                        },
                        {
                            "name": "Execute Function",
                            "description": "",
                            "properties": {
                                "description": "Two way SMS conversation",
                                "functionId": two_way_sms_function["_id"],
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.type",
                                            "operator": "==",
                                            "rightExpression": "'InboundSMS'",
                                        }
                                    ],
                                },
                                "expansions": {
                                    "functionId": {"name": two_way_sms_function["name"]}
                                },
                                "_working": False,
                            },
                            "type": "function",
                            "_selected": False,
                            "id": "refId1739600229776",
                            "icon": "icon-function",
                        },
                        {
                            "name": "HoldQueue",
                            "description": "Transition to another state",
                            "properties": {
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.type",
                                            "operator": "==",
                                            "rightExpression": "'InboundCall'",
                                        }
                                    ],
                                },
                                "stateId": "67b11dbf1fac7db53c1d0210",
                                "description": "Transition to another state",
                            },
                            "type": "transition",
                            "_selected": False,
                            "transitionId": "refId1739600227355",
                            "id": "refId1739600229777",
                            "icon": "icon-transition",
                        },
                    ],
                    "_id": "67b11daace899acb3e0d1c38",
                    "key": "67b11daace899acb3e0d1c38",
                    "location": "800.1809064054271 1304.3867183282998",
                    "transitions": [{"name": "HoldQueue", "id": "refId1739600227355"}],
                },
                "67b11dbf1fac7db53c1d0210": {
                    "category": "Standard",
                    "objectType": "campaignstate",
                    "campaignStateId": "67b11dbf1fac7db53c1d0210",
                    "name": "HoldQueue",
                    "description": "Newly Created State",
                    "actions": [
                        {
                            "name": "Play & Collect Digits",
                            "description": "",
                            "properties": {
                                "loop": 1,
                                "numberDigits": 1,
                                "promptId": prompt["_id"],
                                "terminationKey": "#",
                                "timeoutInSeconds": "1",
                                "dlpOption": False,
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "operator": "!=",
                                            "leftExpression": "workitem.digits",
                                            "rightExpression": "'1'",
                                        },
                                        {
                                            "leftExpression": "workitem.digits",
                                            "operator": "!=",
                                            "rightExpression": "'2'",
                                        },
                                    ],
                                },
                                "expansions": {"promptId": {"name": prompt["name"]}},
                                "_working": False,
                            },
                            "type": "playdigits",
                            "_selected": False,
                            "id": "refId1740283338201",
                            "icon": "icon-playdigits",
                        },
                        {
                            "icon": "icon-tts",
                            "name": "Play Collect Google TTS",
                            "description": "Play Collect using Text-To-Speech",
                            "properties": {
                                "voiceName": "en-US-Wavenet-J",
                                "voiceGender": "male",
                                "text": '<prosody pitch="-2st">To leave a voicemail, press 1. To request a callback, press 2. Otherwise, please stay on the line.</prosody>',
                                "numberDigits": 1,
                                "terminationKey": "#",
                                "timeoutInSeconds": "1",
                                "dlpOption": False,
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "operator": "!=",
                                            "leftExpression": "workitem.digits",
                                            "rightExpression": "'1'",
                                        },
                                        {
                                            "leftExpression": "workitem.digits",
                                            "operator": "!=",
                                            "rightExpression": "'2'",
                                        },
                                    ],
                                },
                            },
                            "type": "googlettscollect",
                            "_selected": False,
                        },
                        {
                            "name": "Execute Function",
                            "description": "",
                            "properties": {
                                "description": "ACD Voicemail (1)",
                                "functionId": acd_voicemail_function["_id"],
                                "functionExpression": "",
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.digits",
                                            "operator": "==",
                                            "rightExpression": "'1'",
                                        }
                                    ],
                                },
                                "expansions": {
                                    "functionId": {
                                        "name": acd_voicemail_function["name"]
                                    }
                                },
                                "_working": False,
                            },
                            "type": "function",
                            "_selected": False,
                            "icon": "icon-function",
                            "id": "refId1739600229018",
                        },
                        {
                            "name": "Execute Function",
                            "description": "",
                            "properties": {
                                "description": "ACD Callback (2)",
                                "functionId": acd_callback_function["_id"],
                                "functionExpression": "",
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.digits",
                                            "operator": "==",
                                            "rightExpression": "'2'",
                                        }
                                    ],
                                },
                                "expansions": {
                                    "functionId": {
                                        "name": acd_callback_function["name"]
                                    }
                                },
                                "_working": False,
                            },
                            "type": "function",
                            "_selected": False,
                            "id": "refId1739600229019",
                            "icon": "icon-function",
                        },
                        {
                            "name": "Loop",
                            "description": "Transition to another state",
                            "properties": {
                                "description": "Back to Top",
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "stateName": "HoldQueue",
                            },
                            "type": "transitionbyname",
                            "_selected": False,
                            "transitionId": "refId1739600227365",
                            "id": "refId1739600229020",
                            "icon": "icon-transition",
                        },
                    ],
                    "_id": "67b11dbf1fac7db53c1d0210",
                    "key": "67b11dbf1fac7db53c1d0210",
                    "location": "1052.2725338991945 1485.6783821715164",
                    "transitions": [{"name": "Loop", "id": "refId1739600227365"}],
                },
                "67b80e6253218fc5093deb5c": {
                    "category": "Standard",
                    "objectType": "campaignstate",
                    "campaignStateId": "67b80e6253218fc5093deb5c",
                    "name": "OutboundCall",
                    "description": "Newly Created State",
                    "actions": [
                        {
                            "icon": "icon-survey",
                            "name": "Survey",
                            "description": "Assign survey to workitem",
                            "properties": {
                                "description": user_survey["name"],
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "surveyId": user_survey["_id"],
                                "expansions": {
                                    "surveyId": {"name": user_survey["name"]}
                                },
                                "_working": False,
                            },
                            "type": "assignsurvey",
                            "_selected": False,
                        },
                        {
                            "name": "ConnectAgent",
                            "description": "Transition to another state",
                            "properties": {
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "stateId": "67b11daace899acb3e0d1c38",
                                "description": "Transition to another state",
                            },
                            "type": "transition",
                            "_selected": False,
                            "transitionId": "refId1740106542546",
                            "icon": "icon-transition",
                            "id": "refId1740106542747",
                        },
                    ],
                    "_id": "67b80e6253218fc5093deb5c",
                    "key": "67b80e6253218fc5093deb5c",
                    "location": "473.1430260529314 768.5038362516186",
                    "transitions": [
                        {"name": "ConnectAgent", "id": "refId1740106542546"}
                    ],
                },
                "67bea6ccb1b61fed3ca6b744": {
                    "category": "Standard",
                    "objectType": "campaignstate",
                    "campaignStateId": "67bea6ccb1b61fed3ca6b744",
                    "name": "Email",
                    "description": "Newly Created State",
                    "actions": [
                        {
                            "icon": "icon-transition",
                            "name": "ConnectAgent",
                            "description": "Transition to another state",
                            "properties": {
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "stateId": "67b11daace899acb3e0d1c38",
                            },
                            "type": "transition",
                            "_selected": False,
                            "transitionId": "refId1740544931001",
                        }
                    ],
                    "_id": "67bea6ccb1b61fed3ca6b744",
                    "key": "67bea6ccb1b61fed3ca6b744",
                    "location": "472.8361694567607 949.8124110619559",
                    "transitions": [
                        {"name": "ConnectAgent", "id": "refId1740544931001"}
                    ],
                },
                "68d7114766b31902e3ebc111": {
                    "category": "Standard",
                    "objectType": "campaignstate",
                    "campaignStateId": "68d7114766b31902e3ebc111",
                    "name": "OutboundSMS",
                    "description": "Newly Created State",
                    "tenantId": "nextivase2",
                    "actions": [
                        {
                            "icon": "icon-transition",
                            "name": "ConnectAgent",
                            "description": "Transition to another state",
                            "properties": {
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "stateId": "67b11daace899acb3e0d1c38",
                            },
                            "type": "transition",
                            "_selected": False,
                            "transitionId": "refId1758920143807",
                        }
                    ],
                    "_id": "68d7114766b31902e3ebc111",
                    "key": "68d7114766b31902e3ebc111",
                    "location": "470.9057281089773 1124.731867146721",
                    "transitions": [
                        {"name": "ConnectAgent", "id": "refId1758920143807"}
                    ],
                },
            },
            "finalWorkitemStateId": "67b1186f5510d9081ac8e32b",
            "finalUserStateId": "67b1186f5510d9081ac8e32b",
            "name": workflow_name,
        }
    )
    headers = {
        "Authorization": ncc_token,
        "Content-Type": "application/json",
    }
    try:
        conn.request("POST", "/data/api/types/workflow/", payload, headers)
        res = conn.getresponse()
        if res.status == 201:
            data = res.read().decode("utf-8")
            workflow = json.loads(data)
    except:
        pass
    conn.close()
    return workflow


def create_csat_workflow(
    ncc_location: str,
    ncc_token: str,
    workflow_name: str,
) -> dict:
    """
    This function creates a workflow in Nextiva Contact Center (NCC).
    """
    workflow = {}
    conn = http.client.HTTPSConnection(ncc_location)
    payload = json.dumps(
        {
            "maxActions": 10000,
            "localizations": {
                "name": {"en": {"language": "en", "value": workflow_name}}
            },
            "states": {
                "67c22a297a298cbb08ad55a2": {
                    "category": "Standard",
                    "campaignStateId": "67c22a297a298cbb08ad55a2",
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
                    "key": "67c22a297a298cbb08ad55a2",
                    "_id": "67c22a297a298cbb08ad55a2",
                    "description": "End State",
                    "name": "End State",
                    "location": "239.35924999999997 130.09825",
                    "transitions": [],
                },
                "start-state": {
                    "category": "Begin",
                    "campaignStateId": "start-state",
                    "actions": [
                        {
                            "icon": "icon-transition",
                            "name": "Survey",
                            "description": "Transition to another state",
                            "properties": {
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.type",
                                            "operator": "==",
                                            "rightExpression": "'Survey'",
                                        }
                                    ],
                                },
                                "stateName": "Survey",
                            },
                            "type": "transitionbyname",
                            "_selected": False,
                            "transitionId": "refId1740775771533",
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
                                "stateId": "67c22a297a298cbb08ad55a2",
                                "name": "Start",
                                "description": "Transition to another state",
                            },
                            "transitionId": "67c22e1c291f8bcc46061363",
                            "_selected": False,
                            "icon": "icon-transition",
                            "id": "refId1740775771522",
                        },
                    ],
                    "transitions": [
                        {"name": "Survey", "id": "refId1740775771533"},
                        {"name": "Start", "id": "67c22e1c291f8bcc46061363"},
                    ],
                    "objectType": "campaignstate",
                    "key": "start-state",
                    "_id": "start-state",
                    "description": "Begin State",
                    "name": "Begin State",
                    "location": "0 0",
                },
                "67c22dfd63bdfe58b65e30cd": {
                    "category": "Standard",
                    "objectType": "campaignstate",
                    "campaignStateId": "67c22dfd63bdfe58b65e30cd",
                    "name": "Survey",
                    "description": "Newly Created State",
                    "actions": [
                        {
                            "icon": "icon-timer",
                            "name": "Start Timer",
                            "description": "",
                            "properties": {
                                "timeoutInSeconds": "300",
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                            },
                            "type": "starttimer",
                            "_selected": False,
                        },
                        {
                            "icon": "icon-transition",
                            "name": "End State",
                            "description": "Transition to another state",
                            "properties": {
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "stateName": "End State",
                            },
                            "type": "transitionbyname",
                            "_selected": False,
                            "transitionId": "refId1740775771520",
                        },
                    ],
                    "_id": "67c22dfd63bdfe58b65e30cd",
                    "key": "67c22dfd63bdfe58b65e30cd",
                    "location": "420.1982499999998 -89.70224999999994",
                    "transitions": [{"name": "End State", "id": "refId1740775771520"}],
                },
            },
            "finalWorkitemStateId": "67c22a297a298cbb08ad55a2",
            "finalUserStateId": "67c22a297a298cbb08ad55a2",
            "name": workflow_name,
        }
    )
    headers = {
        "Authorization": ncc_token,
        "Content-Type": "application/json",
    }
    try:
        conn.request("POST", "/data/api/types/workflow/", payload, headers)
        res = conn.getresponse()
        if res.status == 201:
            data = res.read().decode("utf-8")
            workflow = json.loads(data)
    except:
        pass
    conn.close()
    return workflow


def update_workflow(
    ncc_location: str,
    ncc_token: str,
    workflow_id: str,
    workflow: dict,
) -> bool:
    """
    This function updates a workflow with the specified workflow ID.
    """
    success = False
    conn = http.client.HTTPSConnection(ncc_location)
    payload = json.dumps(workflow)
    headers = {"Authorization": ncc_token, "Content-Type": "application/json"}
    try:
        conn.request(
            "PATCH", f"/data/api/types/workflow/{workflow_id}", payload, headers
        )
        res = conn.getresponse()
        if res.status == 200:
            success = True
    except:
        pass
    conn.close()
    return success


def delete_workflow(ncc_location: str, ncc_token: str, workflow_id: str) -> bool:
    """
    This function deletes a workflow with the specified workflow ID.
    """
    success = False
    conn = http.client.HTTPSConnection(ncc_location)
    payload = ""
    headers = {"Authorization": ncc_token}
    try:
        conn.request(
            "DELETE", f"/data/api/types/workflow/{workflow_id}", payload, headers
        )
        res = conn.getresponse()
        if res.status == 204:
            success = True
    except:
        pass
    conn.close()
    return success
