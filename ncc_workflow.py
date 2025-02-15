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


def create_iva_workflow(
    ncc_location: str,
    ncc_token: str,
    workflow_name: str,
    business_name: str,
    queues: dict,
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
                "name": {"en": {"language": "en", "value": workflow_name}}
            },
            "states": {
                "67b1186f5510d9081ac8e32b": {
                    "category": "Standard",
                    "campaignStateId": "67b1186f5510d9081ac8e32b",
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
                            "name": "Save Variable",
                            "description": "",
                            "properties": {
                                "description": "phone",
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
                            "id": "refId1739600227614",
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
                            "_selected": True,
                        },
                        {
                            "name": "Save Variable",
                            "description": "",
                            "properties": {
                                "description": "queueId",
                                "rightExpression": queues["Test Customer Service"],
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
                    "tenantId": "nextivaretaildemo",
                    "actions": [
                        {
                            "name": "Execute Function",
                            "description": "",
                            "properties": {
                                "description": "Search Contacts - Main",
                                "functionId": "67b119abaade3e5c8919bcc0",
                                "functionExpression": "",
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "expansions": {
                                    "functionId": {"name": "Search Contacts - Main"}
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
                            "_selected": True,
                            "transitionId": "refId1739600227203",
                        },
                    ],
                    "_id": "67b11894720280f716c36bdf",
                    "key": "67b11894720280f716c36bdf",
                    "location": "235.689872021094 86.58930650937515",
                    "transitions": [
                        {"name": "Chat", "id": "refId1739600227187"},
                        {"name": "InboundCall", "id": "refId1739600227163"},
                        {"name": "InboundSMS", "id": "refId1739600227203"},
                    ],
                },
                "67b11b35410f937347fe9aee": {
                    "category": "Standard",
                    "objectType": "campaignstate",
                    "campaignStateId": "67b11b35410f937347fe9aee",
                    "name": "Survey",
                    "description": "Newly Created State",
                    "tenantId": "nextivaretaildemo",
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
                            "_selected": True,
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
                    "tenantId": "nextivaretaildemo",
                    "actions": [
                        {
                            "name": "Chat Message Consumer",
                            "description": "",
                            "properties": {
                                "description": "Thank you for contacting...",
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "from": "workitem.data.companyName",
                                "message": "Thank you for contacting ${workitem.data.companyName}. In a few words, what can I help you with today?",
                                "messageType": "BOT",
                                "options": [],
                            },
                            "type": "chatmessageconsumer",
                            "_selected": False,
                            "icon": "icon-ai-message",
                            "id": "refId1739600226829",
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
                            "_selected": True,
                            "transitionId": "refId1739600226839",
                        },
                    ],
                    "_id": "67b11b3a4492457796ee0690",
                    "key": "67b11b3a4492457796ee0690",
                    "location": "631.2642848004028 236.06753202443764",
                    "transitions": [{"name": "Webhook", "id": "refId1739600226839"}],
                },
                "67b11b424881f97a86b2640f": {
                    "category": "Standard",
                    "objectType": "campaignstate",
                    "campaignStateId": "67b11b424881f97a86b2640f",
                    "name": "InboundCall",
                    "description": "Newly Created State",
                    "tenantId": "nextivaretaildemo",
                    "actions": [
                        {
                            "icon": "icon-tts",
                            "name": "Synthesize Text via Google TTS",
                            "description": "Convert Text into Audio using Google's Text-To-Speech",
                            "properties": {
                                "description": "Thank you for contacting...",
                                "voiceName": "en-US-Wavenet-J",
                                "text": '<prosody pitch="-2st">Thank you for contacting ${workitem.data.companyName}.</prosody>',
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                            },
                            "type": "googletts",
                            "_selected": False,
                        },
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
                            "_selected": True,
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
                    "tenantId": "nextivaretaildemo",
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
                            "_selected": True,
                            "transitionId": "refId1739600226894",
                        },
                    ],
                    "_id": "67b11b4990b64c67bfb0e882",
                    "key": "67b11b4990b64c67bfb0e882",
                    "location": "631.2642848004031 588.219037051561",
                    "transitions": [{"name": "Webhook", "id": "refId1739600226894"}],
                },
                "67b11bac9255944444f52b95": {
                    "category": "Standard",
                    "objectType": "campaignstate",
                    "campaignStateId": "67b11bac9255944444f52b95",
                    "name": "Webhook",
                    "description": "Newly Created State",
                    "tenantId": "nextivaretaildemo",
                    "actions": [
                        {
                            "name": "Wait Chat Message",
                            "description": "",
                            "properties": {
                                "timeoutDuration": 3600000,
                                "stateId": "67b1186f5510d9081ac8e32b",
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
                            "type": "waitforchatmessage",
                            "_selected": False,
                            "id": "refId1739600228033",
                            "icon": "icon-timer",
                        },
                        {
                            "name": "Message Bot",
                            "description": "",
                            "properties": {
                                "description": "Chat",
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
                                "message": "$V.workitem.currentChatMessage.textMsg",
                                "event": "",
                            },
                            "type": "chatmessagebot",
                            "_selected": False,
                            "icon": "icon-ai-message",
                            "id": "refId1739600228034",
                        },
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
                                            "leftExpression": "workitem.type",
                                            "operator": "==",
                                            "rightExpression": "'InboundSMS'",
                                        },
                                        {
                                            "leftExpression": "workitem.data.smsCounter",
                                            "operator": ">",
                                            "rightExpression": "1",
                                        },
                                    ],
                                },
                            },
                            "type": "smswaitformessage",
                            "_selected": False,
                            "id": "refId1739600228035",
                            "icon": "icon-timer",
                        },
                        {
                            "name": "Message Bot",
                            "description": "",
                            "properties": {
                                "description": "InboundSMS",
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
                                "message": "$V.workitem.currentSMSMessage.textMsg",
                                "event": "",
                            },
                            "type": "chatmessagebot",
                            "_selected": False,
                            "icon": "icon-ai-message",
                            "id": "refId1739600228036",
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
                            "type": "savevariable",
                            "_selected": False,
                            "icon": "icon-save",
                            "id": "refId1739600228037",
                        },
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
                            "icon": "icon-transition",
                            "name": "Chat or InboundSMS Action",
                            "description": "Transition to another state",
                            "properties": {
                                "condition": {
                                    "conditionType": "OR",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.type",
                                            "operator": "==",
                                            "rightExpression": "'Chat'",
                                        },
                                        {
                                            "leftExpression": "workitem.type",
                                            "operator": "==",
                                            "rightExpression": "'InboundSMS'",
                                        },
                                    ],
                                },
                                "stateName": "workitem.chatBotResponse.action",
                            },
                            "type": "transitionbyname",
                            "_selected": False,
                            "transitionId": "67b1220e628aee17f5928472",
                            "id": "refId1739600228096",
                        },
                        {
                            "icon": "icon-transition",
                            "name": "InboundCall Action",
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
                                "stateName": "workitem.data.botWebhookRequest.queryResult.action",
                            },
                            "type": "transitionbyname",
                            "_selected": True,
                            "transitionId": "refId1739600228115",
                        },
                    ],
                    "_id": "67b11bac9255944444f52b95",
                    "key": "67b11bac9255944444f52b95",
                    "location": "1095.232082041558 763.2564039101042",
                    "transitions": [
                        {
                            "name": "Chat or InboundSMS Action",
                            "id": "67b1220e628aee17f5928472",
                        },
                        {"name": "InboundCall Action", "id": "refId1739600228115"},
                    ],
                },
                "67b11d83f4a104689291447f": {
                    "category": "Standard",
                    "objectType": "campaignstate",
                    "campaignStateId": "67b11d83f4a104689291447f",
                    "name": "FollowUp",
                    "description": "Newly Created State",
                    "tenantId": "nextivaretaildemo",
                    "actions": [
                        {
                            "icon": "icon-ai-message",
                            "name": "Chat Message Consumer",
                            "description": "",
                            "properties": {
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
                                "message": "$V.workitem.chatBotResponse.text[0]",
                                "messageType": "BOT",
                                "options": [],
                            },
                            "type": "chatmessageconsumer",
                            "_selected": True,
                        },
                        {
                            "icon": "icon-ai-message",
                            "name": "SMS Message Consumer",
                            "description": "",
                            "properties": {
                                "message": "$V.workitem.chatBotResponse.text[0]",
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
                        },
                        {
                            "name": "Webhook",
                            "description": "Transition to another state",
                            "properties": {
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "stateName": "Webhook",
                                "description": "Transition to another state",
                            },
                            "type": "transitionbyname",
                            "_selected": False,
                            "transitionId": "refId1739600227224",
                            "icon": "icon-transition",
                            "id": "refId1739600228385",
                        },
                    ],
                    "_id": "67b11d83f4a104689291447f",
                    "key": "67b11d83f4a104689291447f",
                    "location": "1378.6929147598528 315.9038660630413",
                    "transitions": [{"name": "Webhook", "id": "refId1739600227224"}],
                },
                "67b11daace899acb3e0d1c38": {
                    "category": "Standard",
                    "objectType": "campaignstate",
                    "campaignStateId": "67b11daace899acb3e0d1c38",
                    "name": "ConnectAgent",
                    "description": "Newly Created State",
                    "tenantId": "nextivaretaildemo",
                    "actions": [
                        {
                            "icon": "icon-ai-message",
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
                        },
                        {
                            "icon": "icon-ai-message",
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
                            "icon": "icon-tts",
                            "id": "refId1739600228217",
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
                            "_selected": True,
                            "id": "refId1739600228218",
                            "icon": "icon-enterqueues",
                        },
                        {
                            "name": "Execute Function",
                            "description": "",
                            "properties": {
                                "description": "Two way Chat conversation",
                                "functionId": "62f5f778a4a0a35b078738fe",
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
                                    "functionId": {"name": "Two way Chat conversation"}
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
                                "functionId": "5c79411ad4f8db0001649bc5",
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
                                    "functionId": {"name": "Two way SMS conversation"}
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
                    "tenantId": "nextivaretaildemo",
                    "actions": [
                        {
                            "icon": "icon-playdigits",
                            "name": "Play & Collect Digits",
                            "description": "",
                            "properties": {
                                "loop": 1,
                                "numberDigits": 1,
                                "promptId": "6261a7ca399bc2244d354090",
                                "terminationKey": "#",
                                "timeoutInSeconds": "1",
                                "dlpOption": False,
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "expansions": {
                                    "promptId": {"name": "music accoustic1"}
                                },
                                "_working": False,
                            },
                            "type": "playdigits",
                            "_selected": False,
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
                            "_selected": True,
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


def create_non_iva_dtmf_workflow(
    ncc_location: str,
    ncc_token: str,
    workflow_name: str,
    business_name: str,
    queues: dict,
    acd_voicemail_function: dict,
    acd_callback_function: dict,
) -> dict:
    """
    This function creates a workflow in Nextiva Contact Center (NCC) that uses a DTMF menu.
    """
    workflow = {}
    conn = http.client.HTTPSConnection(ncc_location)
    payload = json.dumps(
        {
            "maxActions": 10000,
            "localizations": {
                "name": {"en": {"value": workflow_name}},
                "description": {"en": {"value": "Non-IVA, DTMF Workflow"}},
            },
            "states": {
                "655e5bff8000b3fefffccc6e": {
                    "category": "Standard",
                    "campaignStateId": "655e5bff8000b3fefffccc6e",
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
                            "_selected": True,
                            "id": "refId1723818900554",
                            "icon": "icon-directconnect",
                        },
                        {
                            "name": "Terminate",
                            "type": "terminate",
                            "description": "Terminate",
                            "properties": {
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                }
                            },
                            "_selected": False,
                            "id": "refId1723818900555",
                            "icon": "icon-terminate",
                        },
                    ],
                    "objectType": "campaignstate",
                    "key": "655e5bff8000b3fefffccc6e",
                    "_id": "655e5bff8000b3fefffccc6e",
                    "description": "End State",
                    "name": "End State",
                    "location": "-2668.0279541015625 -1000.7500610351562",
                    "__gohashid": 17820,
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
                            "id": "refId1738366172156",
                            "icon": "icon-save",
                        },
                        {
                            "name": "Save Variable",
                            "description": "",
                            "properties": {
                                "description": "queueId",
                                "rightExpression": queues["Test Customer Service"],
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
                            "id": "refId1715372161609",
                            "icon": "icon-save",
                        },
                        {
                            "name": "Save Variable",
                            "description": "",
                            "properties": {
                                "description": "phone",
                                "rightExpression": "workitem.from.slice(-10)",
                                "variableName": "phone",
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
                            "id": "refId1715372161610",
                            "icon": "icon-save",
                        },
                        {
                            "name": "Transition- Survey",
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
                                "stateId": "65b681d5192355364082a91d",
                                "description": "Survey",
                            },
                            "type": "transition",
                            "_selected": False,
                            "transitionId": "refId1706457924900",
                            "id": "refId1715372161611",
                            "icon": "icon-transition",
                        },
                        {
                            "name": "Transition- Chat",
                            "description": "Transition to another state",
                            "properties": {
                                "description": "Chat",
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
                                "stateId": "65b68288256da8d4cc8400cd",
                            },
                            "type": "transition",
                            "_selected": False,
                            "transitionId": "refId1706457925022",
                            "id": "refId1715372161612",
                            "icon": "icon-transition",
                        },
                        {
                            "name": "Transition",
                            "description": "Transition to another state",
                            "properties": {
                                "description": "Transition - Inbound Email",
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
                                "stateId": "656e4c1678107e0206362208",
                            },
                            "type": "transition",
                            "_selected": False,
                            "transitionId": "refId1701726650857",
                            "id": "refId1715372161613",
                            "icon": "icon-transition",
                        },
                        {
                            "name": "Transition",
                            "description": "Transition to another state",
                            "properties": {
                                "description": "Transition - Outbound Email",
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.type",
                                            "operator": "==",
                                            "rightExpression": "'OutboundEmail'",
                                        }
                                    ],
                                },
                                "stateId": "656e4b748b3f76f0586f2497",
                            },
                            "type": "transition",
                            "_selected": False,
                            "transitionId": "refId1701726650829",
                            "id": "refId1715372161614",
                            "icon": "icon-transition",
                        },
                        {
                            "name": "Transition",
                            "description": "Transition to another state",
                            "properties": {
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "operator": "==",
                                            "leftExpression": "workitem.businessEvents.General_Regular_Opened",
                                            "rightExpression": "false",
                                        },
                                        {
                                            "leftExpression": "workitem.type",
                                            "operator": "==",
                                            "rightExpression": "'InboundSMS'",
                                        },
                                    ],
                                },
                                "description": "Transition - AH and Holidays SMS",
                                "stateId": "65660377c93272480dc2e4b0",
                            },
                            "type": "transition",
                            "_selected": False,
                            "transitionId": "65b95e3fa08fbfea3bf141ac",
                            "id": "refId1715372161615",
                            "icon": "icon-transition",
                        },
                        {
                            "name": "Transition",
                            "description": "Transition to another state",
                            "properties": {
                                "description": "Transition - Inbound SMS",
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
                                "stateId": "656601b3f3bcef73c55d9764",
                            },
                            "type": "transition",
                            "_selected": False,
                            "transitionId": "656612c27be66629827e487b",
                            "id": "refId1715372161616",
                            "icon": "icon-transition",
                        },
                        {
                            "name": "Transition",
                            "description": "Transition to another state",
                            "properties": {
                                "description": "Transition - Outbound SMS",
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
                                "stateId": "656601c0063bad1c139eebdb",
                            },
                            "type": "transition",
                            "_selected": False,
                            "transitionId": "656612bc3f61989ca1c908a7",
                            "id": "refId1715372161617",
                            "icon": "icon-transition",
                        },
                        {
                            "name": "Transition",
                            "description": "Transition to another state",
                            "properties": {
                                "description": "Transition - Callback",
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
                                "stateId": "656a29a2084c71822201e2cc",
                            },
                            "type": "transition",
                            "_selected": False,
                            "transitionId": "refId1701455750935",
                            "id": "refId1715372161618",
                            "icon": "icon-transition",
                        },
                        {
                            "name": "Transition",
                            "description": "Transition to another state",
                            "properties": {
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.businessEvents.General_Regular_Opened",
                                            "operator": "==",
                                            "rightExpression": "false",
                                        },
                                        {
                                            "leftExpression": "workitem.type",
                                            "operator": "==",
                                            "rightExpression": "'InboundCall'",
                                        },
                                    ],
                                },
                                "description": "Transition - AH and Holidays Voice",
                                "stateId": "65660110c4430aa14601cdfa",
                            },
                            "type": "transition",
                            "_selected": False,
                            "transitionId": "65b95e391e9819e26b0b8b10",
                            "id": "refId1715372161619",
                            "icon": "icon-transition",
                        },
                        {
                            "name": "Transition",
                            "type": "transition",
                            "description": "Transition to another state",
                            "properties": {
                                "description": "Transition - Inbound Voice",
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
                                "stateId": "655e5d884af8b41fd12da496",
                                "name": "Start",
                            },
                            "_selected": False,
                            "id": "refId1715372161620",
                            "transitionId": "refId1700681898306",
                            "icon": "icon-transition",
                        },
                    ],
                    "transitions": [
                        {
                            "name": "Transition- Survey",
                            "id": "refId1706457924900",
                            "__gohashid": 2641,
                        },
                        {
                            "name": "Transition- Chat",
                            "id": "refId1706457925022",
                            "__gohashid": 2646,
                        },
                        {
                            "name": "Transition",
                            "id": "refId1701726650857",
                            "__gohashid": 2651,
                        },
                        {
                            "name": "Transition",
                            "id": "refId1701726650829",
                            "__gohashid": 2656,
                        },
                        {
                            "name": "Transition",
                            "id": "65b95e3fa08fbfea3bf141ac",
                            "__gohashid": 2661,
                        },
                        {
                            "name": "Transition",
                            "id": "656612c27be66629827e487b",
                            "__gohashid": 2666,
                        },
                        {
                            "name": "Transition",
                            "id": "656612bc3f61989ca1c908a7",
                            "__gohashid": 2671,
                        },
                        {
                            "name": "Transition",
                            "id": "refId1701455750935",
                            "__gohashid": 2676,
                        },
                        {
                            "name": "Transition",
                            "id": "65b95e391e9819e26b0b8b10",
                            "__gohashid": 2681,
                        },
                        {
                            "name": "Transition",
                            "id": "refId1700681898306",
                            "__gohashid": 2686,
                        },
                    ],
                    "objectType": "campaignstate",
                    "key": "start-state",
                    "_id": "start-state",
                    "description": "Begin State",
                    "name": "Begin State",
                    "location": "-3794.6666870117188 -1463.5333251953125",
                    "__gohashid": 17821,
                },
                "655e5d884af8b41fd12da496": {
                    "category": "Standard",
                    "objectType": "campaignstate",
                    "campaignStateId": "655e5d884af8b41fd12da496",
                    "name": "Inbound Voice",
                    "description": "Newly Created State",
                    "actions": [
                        {
                            "name": "Synthesize Text via Google TTS",
                            "description": "Convert Text into Audio using Google's Text-To-Speech",
                            "properties": {
                                "voiceName": "en-US-Wavenet-F",
                                "text": "Thank you for calling ${workitem.data.companyName}.",
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "description": "Welcome",
                            },
                            "type": "googletts",
                            "_selected": False,
                            "id": "refId1715372158867",
                            "icon": "icon-tts",
                        },
                        {
                            "name": "Enter Queue from Expression",
                            "description": "",
                            "properties": {
                                "description": "workitem.data.queueId",
                                "priorityExpression": "Standard",
                                "queueIdsExpression": "workitem.data.queueId",
                                "ringAllEnabled": False,
                                "stickyEnabled": False,
                                "stickyUserIdFromExpression": "workitem.data.stickyAgent",
                                "stickyDurationToWaitSeconds": "60",
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                            },
                            "type": "enterqueuefromexpression",
                            "_selected": False,
                            "id": "refId1715372158874",
                            "icon": "icon-enterqueues",
                        },
                        {
                            "name": "Transition - Hold",
                            "description": "Transition to another state",
                            "properties": {
                                "description": "Hold",
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "stateId": "65b01880267d5184c650aba5",
                            },
                            "type": "transition",
                            "_selected": False,
                            "transitionId": "refId1706457925878",
                            "id": "refId1715372158875",
                            "icon": "icon-transition",
                        },
                    ],
                    "_id": "655e5d884af8b41fd12da496",
                    "key": "655e5d884af8b41fd12da496",
                    "location": "-3444.1751098632812 -1281.4058227539062",
                    "transitions": [
                        {
                            "name": "Transition - Hold",
                            "id": "refId1706457925878",
                            "__gohashid": 2732,
                        }
                    ],
                    "__gohashid": 17822,
                },
                "65660110c4430aa14601cdfa": {
                    "category": "Standard",
                    "objectType": "campaignstate",
                    "campaignStateId": "65660110c4430aa14601cdfa",
                    "name": "AH and Holidays Voice",
                    "description": "Newly Created State",
                    "actions": [
                        {
                            "name": "Play & Collect Digits",
                            "description": "",
                            "properties": {
                                "description": "Nextiva - Closed",
                                "loop": 1,
                                "numberDigits": 1,
                                "promptId": "65d3874cf3cef83870e7630f",
                                "terminationKey": "#",
                                "timeoutInSeconds": "3",
                                "dlpOption": False,
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "expansions": {
                                    "promptId": {"name": "Nextiva - Closed"}
                                },
                                "_working": False,
                            },
                            "type": "playdigits",
                            "_selected": False,
                            "icon": "icon-playdigits",
                            "id": "refId1708363729177",
                        },
                        {
                            "name": "Execute Function",
                            "description": "",
                            "properties": {
                                "description": "ACD Voicemail",
                                "functionId": "65afe16f39fd325f29b43464",
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
                                "expansions": {"functionId": {"name": "ACD Voicemail"}},
                                "_working": False,
                            },
                            "type": "function",
                            "_selected": True,
                            "icon": "icon-function",
                            "id": "refId1708363729178",
                        },
                        {
                            "name": "Transition",
                            "description": "Transition to another state",
                            "properties": {
                                "description": "Transition - End State",
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "stateId": "655e5bff8000b3fefffccc6e",
                            },
                            "type": "transition",
                            "_selected": False,
                            "transitionId": "refId1701453663739",
                            "id": "refId1708363729179",
                            "icon": "icon-transition",
                        },
                    ],
                    "_id": "65660110c4430aa14601cdfa",
                    "key": "65660110c4430aa14601cdfa",
                    "location": "-3467.8545232704014 -1052.0893680871702",
                    "transitions": [
                        {
                            "name": "Transition",
                            "id": "refId1701453663739",
                            "__gohashid": 2778,
                        }
                    ],
                    "__gohashid": 17824,
                },
                "656601b3f3bcef73c55d9764": {
                    "category": "Standard",
                    "objectType": "campaignstate",
                    "campaignStateId": "656601b3f3bcef73c55d9764",
                    "name": "Inbound SMS",
                    "description": "Newly Created State",
                    "actions": [
                        {
                            "name": "Enter Queue from Expression",
                            "description": "",
                            "properties": {
                                "description": "workitem.data.queueId",
                                "priorityExpression": "Standard",
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
                            "id": "refId1711467981185",
                            "icon": "icon-enterqueues",
                        },
                        {
                            "name": "Execute Function",
                            "description": "",
                            "properties": {
                                "description": "Two way SMS conversation",
                                "functionId": "65afe20b6e054855bfa85c51",
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "expansions": {
                                    "functionId": {"name": "Two way SMS conversation"}
                                },
                                "_working": False,
                            },
                            "type": "function",
                            "_selected": False,
                            "id": "refId1711467981186",
                            "icon": "icon-function",
                        },
                    ],
                    "_id": "656601b3f3bcef73c55d9764",
                    "key": "656601b3f3bcef73c55d9764",
                    "location": "-2850.9374090125884 -1382.8392460168577",
                    "transitions": [],
                    "__gohashid": 17825,
                },
                "656601c0063bad1c139eebdb": {
                    "category": "Standard",
                    "objectType": "campaignstate",
                    "campaignStateId": "656601c0063bad1c139eebdb",
                    "name": "Outbound SMS",
                    "description": "Newly Created State",
                    "actions": [
                        {
                            "name": "Execute Function",
                            "description": "",
                            "properties": {
                                "description": "Two way SMS conversation",
                                "functionId": "65afe20b6e054855bfa85c51",
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "expansions": {
                                    "functionId": {"name": "Two way SMS conversation"}
                                },
                                "_working": False,
                            },
                            "type": "function",
                            "_selected": True,
                            "id": "refId1709680640621",
                            "icon": "icon-function",
                        }
                    ],
                    "_id": "656601c0063bad1c139eebdb",
                    "key": "656601c0063bad1c139eebdb",
                    "location": "-3039.3543096473545 -1365.255810958264",
                    "transitions": [],
                    "__gohashid": 17826,
                },
                "65660377c93272480dc2e4b0": {
                    "category": "Standard",
                    "objectType": "campaignstate",
                    "campaignStateId": "65660377c93272480dc2e4b0",
                    "name": "AH and Holidays SMS",
                    "description": "Newly Created State",
                    "actions": [
                        {
                            "name": "SMS Message Consumer",
                            "description": "",
                            "properties": {
                                "createNewWorkitem": False,
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "description": "AH and Holiday message",
                                "message": "Thank you for contacting Nextiva!  You've reached us outside of Normal Business Hours.  Please try us again between 5am and 6pm, Mountain Standard Time (Arizona).",
                                "toAddress": "workitem.from",
                                "fromAddress": "workitem.to",
                            },
                            "type": "smsmessageconsumer",
                            "_selected": True,
                            "id": "refId1706645974182",
                            "icon": "icon-sms-message-consumer",
                        },
                        {
                            "name": "Transition",
                            "description": "Transition to another state",
                            "properties": {
                                "description": "Transition - End State",
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "stateId": "655e5bff8000b3fefffccc6e",
                            },
                            "type": "transition",
                            "_selected": False,
                            "transitionId": "refId1701186502862",
                            "id": "refId1706645974183",
                            "icon": "icon-transition",
                        },
                    ],
                    "_id": "65660377c93272480dc2e4b0",
                    "key": "65660377c93272480dc2e4b0",
                    "location": "-3695.2710882118076 -1053.3375813973307",
                    "transitions": [
                        {
                            "name": "Transition",
                            "id": "refId1701186502862",
                            "__gohashid": 2902,
                        }
                    ],
                    "__gohashid": 17827,
                },
                "656a29a2084c71822201e2cc": {
                    "category": "Standard",
                    "objectType": "campaignstate",
                    "campaignStateId": "656a29a2084c71822201e2cc",
                    "name": "WebCallback",
                    "description": "Newly Created State",
                    "actions": [
                        {
                            "name": "Survey",
                            "description": "Assign survey to workitem",
                            "properties": {
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "surveyId": "65afef285754d32573a76733",
                                "expansions": {
                                    "surveyId": {"name": "JFDiotte - All - User Survey"}
                                },
                                "_working": False,
                                "description": "Assign survey to workitem",
                            },
                            "type": "assignsurvey",
                            "_selected": True,
                            "id": "refId1706645973822",
                            "icon": "icon-survey",
                        },
                        {
                            "name": "Enter Queue from Expression",
                            "description": "",
                            "properties": {
                                "description": "workitem.data.queueId",
                                "priorityExpression": "Standard",
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
                            "id": "refId1706645973823",
                            "icon": "icon-enterqueues",
                        },
                    ],
                    "_id": "656a29a2084c71822201e2cc",
                    "key": "656a29a2084c71822201e2cc",
                    "location": "-3227.1875005653233 -1337.0012519761244",
                    "transitions": [],
                    "__gohashid": 17828,
                },
                "656e4b748b3f76f0586f2497": {
                    "category": "Standard",
                    "objectType": "campaignstate",
                    "campaignStateId": "656e4b748b3f76f0586f2497",
                    "name": "Outbound Email",
                    "description": "Newly Created State",
                    "actions": [
                        {
                            "name": "Send Email From Expression",
                            "description": "",
                            "properties": {
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "dispositionId": "65e8b4099d95866a1b124750",
                                "emailaccountId": "65d90668d9ed19568eb2b3aa",
                                "subject": "Thank you for speaking with Nextiva!",
                                "toAddress": "workitem.to",
                                "emailTemplateIdExpression": "6606ebf36080540b02a8b9a7",
                                "expansions": {
                                    "dispositionId": {"name": "General Inquiry"},
                                    "emailaccountId": {"name": "Nextiva SE2"},
                                },
                                "_working": False,
                            },
                            "type": "sendemailfromexpression",
                            "_selected": True,
                            "id": "refId1711728424700",
                            "icon": "icon-sendemail",
                        },
                        {
                            "name": "Transition",
                            "description": "Transition to another state",
                            "properties": {
                                "description": "Transition - End State",
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "stateId": "655e5bff8000b3fefffccc6e",
                            },
                            "type": "transition",
                            "_selected": False,
                            "transitionId": "refId1701726651002",
                            "id": "refId1711728424701",
                            "icon": "icon-transition",
                        },
                    ],
                    "_id": "656e4b748b3f76f0586f2497",
                    "key": "656e4b748b3f76f0586f2497",
                    "location": "-2639.6515569716316 -1424.2704826725424",
                    "transitions": [
                        {
                            "name": "Transition",
                            "id": "refId1701726651002",
                            "__gohashid": 2987,
                        }
                    ],
                    "__gohashid": 7644,
                },
                "656e4c1678107e0206362208": {
                    "category": "Standard",
                    "objectType": "campaignstate",
                    "campaignStateId": "656e4c1678107e0206362208",
                    "name": "Inbound Email",
                    "description": "Newly Created State",
                    "actions": [
                        {
                            "name": "Enter Queue from Expression",
                            "description": "",
                            "properties": {
                                "description": "workitem.data.queueId",
                                "priorityExpression": "Standard",
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
                            "id": "refId1708363728978",
                            "icon": "icon-enterqueues",
                        }
                    ],
                    "_id": "656e4c1678107e0206362208",
                    "key": "656e4c1678107e0206362208",
                    "location": "-2429.5680608778816 -1461.9372002018392",
                    "transitions": [],
                    "__gohashid": 15589,
                },
                "65b01880267d5184c650aba5": {
                    "category": "Standard",
                    "objectType": "campaignstate",
                    "campaignStateId": "65b01880267d5184c650aba5",
                    "name": "HoldQueue",
                    "description": "Newly Created State",
                    "actions": [
                        {
                            "name": "Play & Collect Digits",
                            "description": "",
                            "properties": {
                                "description": "music accoustic1",
                                "loop": 1,
                                "numberDigits": 1,
                                "promptId": "6261a7ca399bc2244d354090",
                                "terminationKey": "#",
                                "timeoutInSeconds": "1",
                                "dlpOption": False,
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "expansions": {
                                    "promptId": {"name": "music accoustic1"}
                                },
                                "_working": False,
                            },
                            "type": "playdigits",
                            "_selected": False,
                            "id": "refId1723781535537",
                            "icon": "icon-playdigits",
                        },
                        {
                            "name": "Execute Function",
                            "description": "",
                            "properties": {
                                "description": "ACD Voicemail (1)",
                                "functionId": acd_voicemail_function["_id"],
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
                            "id": "refId1723781535538",
                            "icon": "icon-function",
                        },
                        {
                            "name": "Execute Function",
                            "description": "",
                            "properties": {
                                "description": "ACD Callback (2)",
                                "functionId": acd_callback_function["_id"],
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
                            "id": "refId1723781535539",
                            "icon": "icon-function",
                        },
                        {
                            "name": "Play & Collect Digits",
                            "description": "",
                            "properties": {
                                "description": "music accoustic1",
                                "loop": 1,
                                "numberDigits": 1,
                                "promptId": "6261a7ca399bc2244d354090",
                                "terminationKey": "#",
                                "timeoutInSeconds": "1",
                                "dlpOption": False,
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "expansions": {
                                    "promptId": {"name": "music accoustic1"}
                                },
                                "_working": False,
                            },
                            "type": "playdigits",
                            "_selected": False,
                            "id": "refId1723781535541",
                            "icon": "icon-playdigits",
                        },
                        {
                            "name": "Execute Function",
                            "description": "",
                            "properties": {
                                "description": "ACD Voicemail (1)",
                                "functionId": acd_voicemail_function["_id"],
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
                            "_selected": True,
                            "id": "refId1723781535542",
                            "icon": "icon-function",
                        },
                        {
                            "name": "Execute Function",
                            "description": "",
                            "properties": {
                                "description": "ACD Callback (2)",
                                "functionId": acd_callback_function["_id"],
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
                            "id": "refId1723781535543",
                            "icon": "icon-function",
                        },
                        {
                            "name": "Transition- Loop",
                            "description": "Transition to another state",
                            "properties": {
                                "description": "Loop",
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "stateId": "65b01880267d5184c650aba5",
                            },
                            "type": "transition",
                            "_selected": False,
                            "transitionId": "refId1706457925717",
                            "id": "refId1723781535545",
                            "icon": "icon-transition",
                        },
                    ],
                    "_id": "65b01880267d5184c650aba5",
                    "key": "65b01880267d5184c650aba5",
                    "location": "-3213.6666870117188 -1185.9999389648438",
                    "transitions": [
                        {
                            "name": "Transition- Loop",
                            "id": "refId1706457925717",
                            "__gohashid": 3072,
                        }
                    ],
                    "__gohashid": 15384,
                },
                "65b681d5192355364082a91d": {
                    "category": "Standard",
                    "objectType": "campaignstate",
                    "campaignStateId": "65b681d5192355364082a91d",
                    "name": "Survey",
                    "description": "Newly Created State",
                    "actions": [
                        {
                            "name": "Execute Function",
                            "description": "",
                            "properties": {
                                "description": "Two way Survey conversation",
                                "functionId": "65afe255a4d255439999a8a7",
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "expansions": {
                                    "functionId": {
                                        "name": "Two way Survey conversation"
                                    }
                                },
                                "_working": False,
                            },
                            "type": "function",
                            "_selected": True,
                            "id": "refId1708363728848",
                            "icon": "icon-function",
                        }
                    ],
                    "_id": "65b681d5192355364082a91d",
                    "key": "65b681d5192355364082a91d",
                    "location": "-2071.66650390625 -1539.6666259765625",
                    "transitions": [],
                    "__gohashid": 8488,
                },
                "65b68288256da8d4cc8400cd": {
                    "category": "Standard",
                    "objectType": "campaignstate",
                    "campaignStateId": "65b68288256da8d4cc8400cd",
                    "name": "Chat",
                    "description": "Newly Created State",
                    "actions": [
                        {
                            "name": "Save Variable",
                            "description": "",
                            "properties": {
                                "description": "contactType",
                                "rightExpression": "workitem.data.context.consumerData.contactType",
                                "variableName": "contactType",
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
                            "id": "refId1722013941414",
                            "icon": "icon-save",
                        },
                        {
                            "name": "Save Variable",
                            "description": "",
                            "properties": {
                                "description": "firstName",
                                "rightExpression": "workitem.data.context.consumerData.firstName",
                                "variableName": "firstName",
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
                            "id": "refId1722013941415",
                            "icon": "icon-save",
                        },
                        {
                            "name": "Save Variable",
                            "description": "",
                            "properties": {
                                "description": "lastName",
                                "rightExpression": "workitem.data.context.consumerData.lastName",
                                "variableName": "lastName",
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
                            "id": "refId1722013941416",
                            "icon": "icon-save",
                        },
                        {
                            "name": "Save Variable",
                            "description": "",
                            "properties": {
                                "description": "email",
                                "rightExpression": "workitem.data.context.consumerData.email",
                                "variableName": "email",
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
                            "id": "refId1722013941417",
                            "icon": "icon-save",
                        },
                        {
                            "name": "Save Variable",
                            "description": "",
                            "properties": {
                                "description": "phone",
                                "rightExpression": "workitem.data.context.consumerData.phone",
                                "variableName": "phone",
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
                            "id": "refId1722013941418",
                            "icon": "icon-save",
                        },
                        {
                            "name": "Skill Name",
                            "description": "Add skill to workitem",
                            "properties": {
                                "description": "skills mandatory for contactType",
                                "skillName": "workitem.data.contactType",
                                "mandatory": True,
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                            },
                            "type": "skillbyname",
                            "_selected": False,
                            "id": "refId1722013941419",
                            "icon": "icon-ll-skills",
                        },
                        {
                            "name": "Enter Queue from Expression",
                            "description": "",
                            "properties": {
                                "description": "workitem.data.queueId",
                                "priorityExpression": "Standard",
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
                            "id": "refId1722013941420",
                            "icon": "icon-enterqueues",
                        },
                        {
                            "name": "Execute Function",
                            "description": "",
                            "properties": {
                                "description": "Two way Chat conversation",
                                "functionId": "65afe1ee39fd325f29b43466",
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "expansions": {
                                    "functionId": {"name": "Two way Chat conversation"}
                                },
                                "_working": False,
                                "functionExpression": "",
                            },
                            "type": "function",
                            "_selected": True,
                            "id": "refId1722013941421",
                            "icon": "icon-function",
                        },
                    ],
                    "_id": "65b68288256da8d4cc8400cd",
                    "key": "65b68288256da8d4cc8400cd",
                    "location": "-2248.3333740234375 -1499",
                    "transitions": [],
                    "__gohashid": 12397,
                },
            },
            "finalWorkitemStateId": "655e5bff8000b3fefffccc6e",
            "finalUserStateId": "655e5bff8000b3fefffccc6e",
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


def create_direct_line_workflow(
    ncc_location: str,
    ncc_token: str,
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
    payload = json.dumps(
        {
            "maxActions": 10000,
            "localizations": {
                "name": {"en": {"value": workflow_name}},
                "description": {"en": {"value": "Direct Line Workflow"}},
            },
            "states": {
                "66d8f9e3104729188ed41685": {
                    "category": "Standard",
                    "campaignStateId": "66d8f9e3104729188ed41685",
                    "actions": [
                        {
                            "name": "ACD Voicemail From Expression",
                            "description": "Create ACD Voicemail",
                            "properties": {
                                "description": "Create ACD Voicemail",
                                "transcription": True,
                                "priority": 3,
                                "queueIdsExpression": "workitem.data.queueId",
                                "toAddress": "",
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.data.messageRecorded",
                                            "operator": "==",
                                            "rightExpression": "'1'",
                                        }
                                    ],
                                },
                            },
                            "type": "acdvmfromexpression",
                            "_selected": False,
                            "id": "refId1725570892321",
                            "icon": "icon-directconnect",
                        },
                        {
                            "name": "Terminate",
                            "type": "terminate",
                            "description": "Terminate",
                            "properties": {
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                }
                            },
                            "_selected": False,
                            "id": "refId1725570892323",
                            "icon": "icon-terminate",
                        },
                    ],
                    "objectType": "campaignstate",
                    "key": "66d8f9e3104729188ed41685",
                    "_id": "66d8f9e3104729188ed41685",
                    "description": "End State",
                    "name": "End State",
                    "location": "1023.0958707809248 417.0087238302355",
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
                            "id": "refId1738366172156",
                            "icon": "icon-save",
                        },
                        {
                            "name": "Save Variable",
                            "description": "",
                            "properties": {
                                "description": "queueId",
                                "rightExpression": queues["Test Customer Service"],
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
                            "id": "refId1728896032862",
                            "icon": "icon-save",
                        },
                        {
                            "name": "Save Variable",
                            "description": "",
                            "properties": {
                                "description": "preferredLanguage",
                                "rightExpression": "English",
                                "variableName": "preferredLanguage",
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
                            "id": "refId1728896032863",
                            "icon": "icon-save",
                        },
                        {
                            "name": "Transition",
                            "description": "Transition to another state",
                            "properties": {
                                "description": "InboundCall",
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
                                "stateId": "670ca5ecfdefe77a5801fdbb",
                            },
                            "type": "transition",
                            "_selected": True,
                            "transitionId": "refId1725492300624",
                            "id": "refId1728896032864",
                            "icon": "icon-transition",
                        },
                        {
                            "name": "Transition",
                            "description": "Transition to another state",
                            "properties": {
                                "description": "OutboundSMS",
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
                                "stateId": "6707178a057e0af18faedc7d",
                            },
                            "type": "transition",
                            "_selected": False,
                            "transitionId": "refId1728517832620",
                            "id": "refId1728896032866",
                            "icon": "icon-transition",
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
                                "stateId": "66d8f9e3104729188ed41685",
                                "name": "Start",
                                "description": "Transition to another state",
                            },
                            "transitionId": "66d8f9fc37e19143fb9f21e2",
                            "_selected": False,
                            "id": "refId1728896032867",
                            "icon": "icon-transition",
                        },
                    ],
                    "transitions": [
                        {"name": "Transition", "id": "refId1725492300624"},
                        {"name": "Transition", "id": "refId1728517832620"},
                        {"name": "Start", "id": "66d8f9fc37e19143fb9f21e2"},
                    ],
                    "objectType": "campaignstate",
                    "key": "start-state",
                    "_id": "start-state",
                    "description": "Begin State",
                    "name": "Begin State",
                    "location": "712.7212863159832 -20.793664538718872",
                },
                "66d8fa0d32652cf89e82962b": {
                    "category": "Standard",
                    "objectType": "campaignstate",
                    "campaignStateId": "66d8fa0d32652cf89e82962b",
                    "name": "EnterQueue",
                    "description": "Newly Created State",
                    "tenantId": "nextivaretaildemo",
                    "actions": [
                        {
                            "name": "Look Up Agent Info",
                            "description": "",
                            "properties": {
                                "scriptId": "66c6bdda96c7f718c8cd8f3b",
                                "variableName": "agentUserId",
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "expansions": {"scriptId": {"name": "Contact Info"}},
                                "_working": False,
                            },
                            "type": "script",
                            "_selected": False,
                            "id": "refId1729821754218",
                            "icon": "icon-script",
                        },
                        {
                            "name": "Save Variable",
                            "description": "",
                            "properties": {
                                "description": "intent",
                                "rightExpression": "Customer Service",
                                "variableName": "intent",
                                "asObject": False,
                                "dlpOption": False,
                                "wfmOption": False,
                                "dashboard": True,
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                            },
                            "type": "savevariable",
                            "_selected": False,
                            "id": "refId1729821754219",
                            "icon": "icon-save",
                        },
                        {
                            "name": "Save Variable",
                            "description": "",
                            "properties": {
                                "description": "subunit",
                                "rightExpression": "N/A",
                                "variableName": "subunit",
                                "asObject": False,
                                "dlpOption": False,
                                "wfmOption": False,
                                "dashboard": True,
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                            },
                            "type": "savevariable",
                            "_selected": False,
                            "id": "refId1729821754220",
                            "icon": "icon-save",
                        },
                        {
                            "name": "Save Variable",
                            "description": "",
                            "properties": {
                                "description": "department",
                                "rightExpression": "Customer Service",
                                "variableName": "department",
                                "asObject": False,
                                "dlpOption": False,
                                "wfmOption": False,
                                "dashboard": True,
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                            },
                            "type": "savevariable",
                            "_selected": False,
                            "id": "refId1729821754221",
                            "icon": "icon-save",
                        },
                        {
                            "icon": "icon-playprompt",
                            "name": "Play Prompt",
                            "description": "",
                            "properties": {
                                "description": "Litify - Please Wait",
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "loop": 1,
                                "promptId": "671b105ee6c64a69cf713f96",
                                "expansions": {
                                    "promptId": {"name": "Litify - Please Wait"}
                                },
                                "_working": False,
                            },
                            "type": "playprompt",
                            "_selected": False,
                        },
                        {
                            "name": "Enter Queue from Expression",
                            "description": "",
                            "properties": {
                                "priorityExpression": "Standard",
                                "queueIdsExpression": "workitem.data.queueId",
                                "ringAllEnabled": False,
                                "stickyEnabled": True,
                                "stickyUserType": "userIdFromExpression",
                                "stickyUserIdFromExpression": "workitem.data.agentUserId",
                                "stickyDurationToWaitSeconds": "7200",
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                            },
                            "type": "enterqueuefromexpression",
                            "_selected": False,
                            "id": "refId1729821754224",
                            "icon": "icon-enterqueues",
                        },
                        {
                            "name": "Execute Function",
                            "description": "",
                            "properties": {
                                "description": "Two way SMS conversation",
                                "functionId": "5c79411ad4f8db0001649bc5",
                                "functionExpression": "",
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
                                    "functionId": {"name": "Two way SMS conversation"}
                                },
                                "_working": False,
                            },
                            "type": "function",
                            "_selected": False,
                            "id": "refId1729821754225",
                            "icon": "icon-function",
                        },
                        {
                            "name": "Transition",
                            "description": "Transition to another state",
                            "properties": {
                                "description": "HoldQueue",
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
                                "stateId": "66d8fb13ad3c61caa09d1110",
                            },
                            "type": "transition",
                            "_selected": False,
                            "transitionId": "refId1725492300850",
                            "id": "refId1729821754226",
                            "icon": "icon-transition",
                        },
                    ],
                    "_id": "66d8fa0d32652cf89e82962b",
                    "key": "66d8fa0d32652cf89e82962b",
                    "location": "2901.6485757105515 1140.6023515871557",
                    "transitions": [{"name": "Transition", "id": "refId1725492300850"}],
                },
                "66d8fb13ad3c61caa09d1110": {
                    "category": "Standard",
                    "objectType": "campaignstate",
                    "campaignStateId": "66d8fb13ad3c61caa09d1110",
                    "name": "HoldQueue",
                    "description": "Newly Created State",
                    "tenantId": "nextivaretaildemo",
                    "actions": [
                        {
                            "name": "Play & Collect Digits",
                            "description": "",
                            "properties": {
                                "description": "music accoustic1",
                                "loop": 1,
                                "numberDigits": 1,
                                "promptId": "6261a7ca399bc2244d354090",
                                "terminationKey": "#",
                                "timeoutInSeconds": "1",
                                "dlpOption": False,
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "expansions": {
                                    "promptId": {"name": "music accoustic1"}
                                },
                                "_working": False,
                            },
                            "type": "playdigits",
                            "_selected": False,
                            "id": "refId1738600563580",
                            "icon": "icon-playdigits",
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
                            "id": "refId1738600563581",
                            "icon": "icon-function",
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
                            "id": "refId1738600563582",
                            "icon": "icon-function",
                        },
                        {
                            "name": "Play & Collect Digits",
                            "description": "",
                            "properties": {
                                "description": "music accoustic1",
                                "loop": 1,
                                "numberDigits": 1,
                                "promptId": "6261a7ca399bc2244d354090",
                                "terminationKey": "#",
                                "timeoutInSeconds": "1",
                                "dlpOption": False,
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "expansions": {
                                    "promptId": {"name": "music accoustic1"}
                                },
                                "_working": False,
                            },
                            "type": "playdigits",
                            "_selected": True,
                            "id": "refId1738600563583",
                            "icon": "icon-playdigits",
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
                            "id": "refId1738600563584",
                            "icon": "icon-function",
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
                            "id": "refId1738600563585",
                            "icon": "icon-function",
                        },
                        {
                            "name": "Transition",
                            "description": "Transition to another state",
                            "properties": {
                                "description": "Loop",
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "stateId": "66d8fb13ad3c61caa09d1110",
                            },
                            "type": "transition",
                            "_selected": False,
                            "transitionId": "refId1725492300938",
                            "id": "refId1738600563586",
                            "icon": "icon-transition",
                        },
                    ],
                    "_id": "66d8fb13ad3c61caa09d1110",
                    "key": "66d8fb13ad3c61caa09d1110",
                    "location": "3201.3012699091823 1307.7540018006155",
                    "transitions": [{"name": "Transition", "id": "refId1725492300938"}],
                },
                "6707178a057e0af18faedc7d": {
                    "category": "Standard",
                    "objectType": "campaignstate",
                    "campaignStateId": "6707178a057e0af18faedc7d",
                    "name": "OutboundSMS",
                    "description": "Newly Created State",
                    "tenantId": "nextivaretaildemo",
                    "actions": [
                        {
                            "icon": "icon-function",
                            "name": "Execute Function",
                            "description": "",
                            "properties": {
                                "description": "Two way SMS conversation",
                                "functionId": "5c79411ad4f8db0001649bc5",
                                "functionExpression": "",
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "expansions": {
                                    "functionId": {"name": "Two way SMS conversation"}
                                },
                                "_working": False,
                            },
                            "type": "function",
                            "_selected": True,
                        }
                    ],
                    "_id": "6707178a057e0af18faedc7d",
                    "key": "6707178a057e0af18faedc7d",
                    "location": "1198.5146171007284 322.6567628330434",
                    "transitions": [],
                },
                "670ca4e625ed9996262cc286": {
                    "category": "Standard",
                    "objectType": "campaignstate",
                    "campaignStateId": "670ca4e625ed9996262cc286",
                    "name": "CheckPrefLang",
                    "description": "Newly Created State",
                    "tenantId": "nextivaretaildemo",
                    "actions": [
                        {
                            "name": "Transition",
                            "description": "Transition to another state",
                            "properties": {
                                "condition": {
                                    "conditionType": "OR",
                                    "expressions": [
                                        {
                                            "operator": "==",
                                            "leftExpression": "workitem.data.preferredLanguage",
                                            "rightExpression": "'English'",
                                        },
                                        {
                                            "leftExpression": "workitem.data.preferredLanguage",
                                            "operator": "==",
                                            "rightExpression": "'Spanish'",
                                        },
                                    ],
                                },
                                "stateId": "670cc602dd90eb0f8f0980e4",
                                "description": "Transition to another state",
                            },
                            "type": "transition",
                            "_selected": True,
                            "transitionId": "670cb472659969154290cd0b",
                            "id": "refId1728890057467",
                            "icon": "icon-transition",
                        },
                        {
                            "name": "Transition",
                            "description": "Transition to another state",
                            "properties": {
                                "description": "Transition to another state",
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [],
                                },
                                "stateId": "670ca881295277f9f946e876",
                            },
                            "type": "transition",
                            "_selected": False,
                            "transitionId": "refId1728881253112",
                            "id": "refId1728890057468",
                            "icon": "icon-transition",
                        },
                    ],
                    "_id": "670ca4e625ed9996262cc286",
                    "key": "670ca4e625ed9996262cc286",
                    "location": "2009.9989589671272 580.4637014087123",
                    "transitions": [
                        {"name": "Transition", "id": "670cb472659969154290cd0b"},
                        {"name": "Transition", "id": "refId1728881253112"},
                    ],
                },
                "670ca5ecfdefe77a5801fdbb": {
                    "category": "Standard",
                    "objectType": "campaignstate",
                    "campaignStateId": "670ca5ecfdefe77a5801fdbb",
                    "name": "SearchContacts",
                    "description": "Newly Created State",
                    "tenantId": "nextivaretaildemo",
                    "actions": [
                        {
                            "name": "Save Variable",
                            "description": "",
                            "properties": {
                                "description": "phone",
                                "rightExpression": "workitem.from.slice(-10)",
                                "variableName": "phone",
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
                            "id": "refId1738607250005",
                            "icon": "icon-save",
                        },
                        {
                            "name": "Execute REST Call",
                            "description": "",
                            "properties": {
                                "description": "Litify - Search Contacts",
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "responseVariable": "searchContactsResponse",
                                "restCallId": "66d8ec3ed36e0e5b10d105cd",
                                "expansions": {
                                    "restCallId": {"name": "Litify - Search Contacts"}
                                },
                                "_working": False,
                            },
                            "type": "restapi",
                            "_selected": False,
                            "id": "refId1738607250006",
                            "icon": "icon-api",
                        },
                        {
                            "name": "Transition",
                            "description": "Transition to another state",
                            "properties": {
                                "description": "workitem.data.apiResponse.httpStatus == 200 && workitem.data.apiResponse.body.totalSize == '1'",
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.data.searchContactsResponse.httpStatus",
                                            "operator": "==",
                                            "rightExpression": "200",
                                        },
                                        {
                                            "leftExpression": "workitem.data.searchContactsResponse.body.totalSize",
                                            "operator": "==",
                                            "rightExpression": "'1'",
                                        },
                                    ],
                                },
                                "stateId": "670ca7469db654594e96e93c",
                                "points": {
                                    "h": True,
                                    "r": [],
                                    "ct": 0,
                                    "__gohashid": 3755,
                                },
                            },
                            "type": "transition",
                            "_selected": True,
                            "transitionId": "refId1728881252987",
                            "id": "refId1738607250007",
                            "icon": "icon-transition",
                        },
                    ],
                    "_id": "670ca5ecfdefe77a5801fdbb",
                    "key": "670ca5ecfdefe77a5801fdbb",
                    "location": "1410.2807399707942 166.35588969177047",
                    "transitions": [{"name": "Transition", "id": "refId1728881252987"}],
                },
                "670ca7469db654594e96e93c": {
                    "category": "Standard",
                    "objectType": "campaignstate",
                    "campaignStateId": "670ca7469db654594e96e93c",
                    "name": "GetAccountDetails",
                    "description": "Newly Created State",
                    "tenantId": "nextivaretaildemo",
                    "actions": [
                        {
                            "name": "Save Variable",
                            "description": "",
                            "properties": {
                                "description": "whoId",
                                "rightExpression": "workitem.data.searchContactsResponse.body.records[0].Id",
                                "variableName": "whoId",
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
                            "id": "refId1738607250029",
                            "icon": "icon-save",
                        },
                        {
                            "name": "Save Variable",
                            "description": "",
                            "properties": {
                                "description": "name",
                                "rightExpression": "workitem.data.searchContactsResponse.body.records[0].Name",
                                "variableName": "name",
                                "asObject": False,
                                "dlpOption": False,
                                "wfmOption": False,
                                "dashboard": True,
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                            },
                            "type": "savevariable",
                            "_selected": False,
                            "id": "refId1738607250030",
                            "icon": "icon-save",
                        },
                        {
                            "name": "Save Variable",
                            "description": "",
                            "properties": {
                                "description": "accountId",
                                "rightExpression": "workitem.data.searchContactsResponse.body.records[0].AccountId",
                                "variableName": "accountId",
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
                            "id": "refId1738607250031",
                            "icon": "icon-save",
                        },
                        {
                            "name": "Execute REST Call",
                            "description": "",
                            "properties": {
                                "description": "Litify - Get Account Details",
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "responseVariable": "getAccountDetailsResponse",
                                "restCallId": "670ca5bf3b729f0c47e638d1",
                                "expansions": {
                                    "restCallId": {
                                        "name": "Litify - Get Account Details"
                                    }
                                },
                                "_working": False,
                            },
                            "type": "restapi",
                            "_selected": False,
                            "id": "refId1738607250032",
                            "icon": "icon-api",
                        },
                        {
                            "name": "Save Variable",
                            "description": "",
                            "properties": {
                                "description": "preferredLanguage",
                                "rightExpression": "workitem.data.getAccountDetailsResponse.body.Preferred_Language__c",
                                "variableName": "preferredLanguage",
                                "asObject": False,
                                "dlpOption": False,
                                "wfmOption": False,
                                "dashboard": False,
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "operator": "==",
                                            "leftExpression": "workitem.data.apiResponse.httpStatus",
                                            "rightExpression": "200",
                                        }
                                    ],
                                },
                            },
                            "type": "savevariable",
                            "_selected": False,
                            "id": "refId1738607250033",
                            "icon": "icon-save",
                        },
                        {
                            "name": "Transition",
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
                                "stateId": "66d8fa0d32652cf89e82962b",
                                "description": "Transition to another state",
                                "points": {
                                    "h": True,
                                    "r": [
                                        {
                                            "b": 1796.157061852348,
                                            "k": 346.6035165442374,
                                            "h": True,
                                        },
                                        {
                                            "b": 1806.157061852348,
                                            "k": 346.6035165442374,
                                            "h": True,
                                        },
                                        {"b": 1804, "k": 346.6035165442374, "h": True},
                                        {"b": 1804, "k": 346.6035165442374, "h": True},
                                        {
                                            "b": 2901.6485757105515,
                                            "k": 346.6035165442374,
                                            "h": True,
                                        },
                                        {
                                            "b": 2901.6485757105515,
                                            "k": 1066.3623674562962,
                                            "h": True,
                                        },
                                        {
                                            "b": 2901.6485757105515,
                                            "k": 1076.3623674562962,
                                            "h": True,
                                        },
                                    ],
                                    "ct": 7,
                                    "__gohashid": 5528,
                                },
                            },
                            "type": "transition",
                            "_selected": False,
                            "transitionId": "refId1728896033011",
                            "id": "refId1738607250034",
                            "icon": "icon-transition",
                        },
                        {
                            "name": "Transition",
                            "description": "Transition to another state",
                            "properties": {
                                "description": "workitem.data.apiResponse.httpStatus == 200",
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.data.getAccountDetailsResponse.httpStatus",
                                            "operator": "==",
                                            "rightExpression": "200",
                                        }
                                    ],
                                },
                                "stateId": "670ca4e625ed9996262cc286",
                                "points": {
                                    "h": True,
                                    "r": [
                                        {
                                            "b": 1796.157061852348,
                                            "k": 390.6035165442374,
                                            "h": True,
                                        },
                                        {
                                            "b": 1806.157061852348,
                                            "k": 390.6035165442374,
                                            "h": True,
                                        },
                                        {
                                            "b": 1806.157061852348,
                                            "k": 390.6035165442374,
                                            "h": True,
                                        },
                                        {"b": 1806.157061852348, "k": 452, "h": True},
                                        {"b": 2009.9989589671272, "k": 452, "h": True},
                                        {
                                            "b": 2009.9989589671272,
                                            "k": 484.22371727785287,
                                            "h": True,
                                        },
                                        {
                                            "b": 2009.9989589671272,
                                            "k": 494.22371727785287,
                                            "h": True,
                                        },
                                    ],
                                    "ct": 7,
                                    "__gohashid": 5529,
                                },
                            },
                            "type": "transition",
                            "_selected": True,
                            "transitionId": "refId1728881253060",
                            "id": "refId1738607250035",
                            "icon": "icon-transition",
                        },
                    ],
                    "_id": "670ca7469db654594e96e93c",
                    "key": "670ca7469db654594e96e93c",
                    "location": "1713.157061852348 351.86353241337804",
                    "transitions": [
                        {"name": "Transition", "id": "refId1728896033011"},
                        {"name": "Transition", "id": "refId1728881253060"},
                    ],
                },
                "670ca881295277f9f946e876": {
                    "category": "Standard",
                    "objectType": "campaignstate",
                    "campaignStateId": "670ca881295277f9f946e876",
                    "name": "PromptLang",
                    "description": "Newly Created State",
                    "tenantId": "nextivaretaildemo",
                    "actions": [
                        {
                            "name": "Save Variable",
                            "description": "",
                            "properties": {
                                "description": "preferredLanguage == English",
                                "rightExpression": "English",
                                "variableName": "preferredLanguage",
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
                            "id": "refId1729821755530",
                            "icon": "icon-save",
                        },
                        {
                            "name": "Play Prompt",
                            "description": "",
                            "properties": {
                                "description": "Litify - Welcome",
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "loop": 1,
                                "promptId": "671b0cbf8fec8776eabc05d5",
                                "expansions": {
                                    "promptId": {"name": "Litify - Welcome"}
                                },
                                "_working": False,
                            },
                            "type": "playprompt",
                            "_selected": False,
                            "id": "refId1729821755531",
                            "icon": "icon-playprompt",
                        },
                        {
                            "name": "Play & Collect Digits",
                            "description": "",
                            "properties": {
                                "description": "Litify - Spanish Option",
                                "loop": 1,
                                "numberDigits": 1,
                                "promptId": "671b100be6c64a69cf713f95",
                                "terminationKey": "#",
                                "timeoutInSeconds": "3",
                                "dlpOption": False,
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "expansions": {
                                    "promptId": {"name": "Litify - Spanish Option"}
                                },
                                "_working": False,
                            },
                            "type": "playdigits",
                            "_selected": False,
                            "icon": "icon-playdigits",
                            "id": "refId1729821755532",
                        },
                        {
                            "icon": "icon-reset",
                            "name": "Set Language",
                            "description": "",
                            "properties": {
                                "description": "Spanish",
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.digits",
                                            "operator": "==",
                                            "rightExpression": "'8'",
                                        }
                                    ],
                                },
                                "languageId": "5856910dd1cde32bc192b8e6",
                                "expansions": {"languageId": {"name": "Spanish"}},
                                "_working": False,
                            },
                            "type": "setlanguage",
                            "_selected": True,
                        },
                        {
                            "name": "Save Variable",
                            "description": "",
                            "properties": {
                                "description": "preferredLanguage == Spanish",
                                "rightExpression": "Spanish",
                                "variableName": "preferredLanguage",
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
                                            "rightExpression": "'8'",
                                        }
                                    ],
                                },
                            },
                            "type": "savevariable",
                            "_selected": False,
                            "id": "refId1729821755533",
                            "icon": "icon-save",
                        },
                        {
                            "name": "Transition",
                            "description": "Transition to another state",
                            "properties": {
                                "description": "UpdatePrefLang",
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "stateId": "670ca987f116924f28a46251",
                            },
                            "type": "transition",
                            "_selected": False,
                            "transitionId": "refId1728881253362",
                            "id": "refId1729821755534",
                            "icon": "icon-transition",
                        },
                    ],
                    "_id": "670ca881295277f9f946e876",
                    "key": "670ca881295277f9f946e876",
                    "location": "2306.9008182257976 775.9696699595421",
                    "transitions": [{"name": "Transition", "id": "refId1728881253362"}],
                },
                "670ca987f116924f28a46251": {
                    "category": "Standard",
                    "objectType": "campaignstate",
                    "campaignStateId": "670ca987f116924f28a46251",
                    "name": "UpdatePrefLang",
                    "description": "Newly Created State",
                    "tenantId": "nextivaretaildemo",
                    "actions": [
                        {
                            "name": "Execute REST Call",
                            "description": "",
                            "properties": {
                                "description": "Litify - Update Preferred Language",
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "responseVariable": "updatePreferredLanguageResponse",
                                "restCallId": "670cabec4cc7a140809eb919",
                                "expansions": {
                                    "restCallId": {
                                        "name": "Litify - Update Preferred Language"
                                    }
                                },
                                "_working": False,
                            },
                            "type": "restapi",
                            "_selected": True,
                            "id": "refId1728881257176",
                            "icon": "icon-api",
                        },
                        {
                            "name": "Transition",
                            "description": "Transition to another state",
                            "properties": {
                                "description": "Welcome",
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "stateId": "66d8fa0d32652cf89e82962b",
                            },
                            "type": "transition",
                            "_selected": False,
                            "transitionId": "refId1728881253454",
                            "id": "refId1728881257177",
                            "icon": "icon-transition",
                        },
                    ],
                    "_id": "670ca987f116924f28a46251",
                    "key": "670ca987f116924f28a46251",
                    "location": "2543.34642867992 974.7483534080326",
                    "transitions": [{"name": "Transition", "id": "refId1728881253454"}],
                },
                "670cc602dd90eb0f8f0980e4": {
                    "category": "Standard",
                    "objectType": "campaignstate",
                    "campaignStateId": "670cc602dd90eb0f8f0980e4",
                    "name": "Welcome",
                    "description": "Newly Created State",
                    "tenantId": "nextivaretaildemo",
                    "actions": [
                        {
                            "icon": "icon-reset",
                            "name": "Set Language",
                            "description": "",
                            "properties": {
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.data.preferredLanguage",
                                            "operator": "==",
                                            "rightExpression": "'Spanish'",
                                        }
                                    ],
                                },
                                "languageId": "5856910dd1cde32bc192b8e6",
                                "expansions": {"languageId": {"name": "Spanish"}},
                                "_working": False,
                            },
                            "type": "setlanguage",
                            "_selected": True,
                        },
                        {
                            "icon": "icon-playprompt",
                            "name": "Play Prompt",
                            "description": "",
                            "properties": {
                                "description": "Litify - Welcome",
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "loop": 1,
                                "promptId": "671b0cbf8fec8776eabc05d5",
                                "expansions": {
                                    "promptId": {"name": "Litify - Welcome"}
                                },
                                "_working": False,
                            },
                            "type": "playprompt",
                            "_selected": False,
                        },
                        {
                            "name": "Transition",
                            "description": "Transition to another state",
                            "properties": {
                                "description": "EnterQueue",
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "stateId": "66d8fa0d32652cf89e82962b",
                            },
                            "type": "transition",
                            "_selected": False,
                            "transitionId": "refId1728890057465",
                            "icon": "icon-transition",
                            "id": "refId1729821753867",
                        },
                    ],
                    "_id": "670cc602dd90eb0f8f0980e4",
                    "key": "670cc602dd90eb0f8f0980e4",
                    "location": "2701.9396287318796 708.3558662644192",
                    "transitions": [{"name": "Transition", "id": "refId1728890057465"}],
                },
            },
            "finalWorkitemStateId": "66d8f9e3104729188ed41685",
            "finalUserStateId": "66d8f9e3104729188ed41685",
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
