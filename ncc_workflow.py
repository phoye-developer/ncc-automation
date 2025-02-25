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
    search_contacts_function: dict,
    two_way_chat_function: dict,
    two_way_sms_function: dict,
    prompt: dict,
    acd_voicemail_function: dict,
    acd_callback_function: dict,
    get_function_id_script: dict,
    check_has_all_parameters_script: dict,
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
                            "_selected": True,
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
                            "_selected": True,
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
                                "description": "phone (inbound)",
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
                            "id": "refId1739934454000",
                            "icon": "icon-save",
                        },
                        {
                            "icon": "icon-save",
                            "name": "Save Variable",
                            "description": "",
                            "properties": {
                                "description": "phone (outbound)",
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
                            "_selected": True,
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
                            "description": "Thank you for contacting...",
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
                            "description": "Thank you for contacting...",
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
                            "name": "Execute Script",
                            "description": "",
                            "properties": {
                                "description": check_has_all_parameters_script["name"],
                                "scriptId": check_has_all_parameters_script["_id"],
                                "variableName": "hasAllParameters",
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "expansions": {
                                    "scriptId": {
                                        "name": check_has_all_parameters_script["name"]
                                    }
                                },
                                "_working": False,
                            },
                            "type": "script",
                            "_selected": False,
                            "id": "refId1740431837492",
                            "icon": "icon-script",
                        },
                        {
                            "name": "FollowUp",
                            "description": "Transition to another state",
                            "properties": {
                                "description": "Transition to another state",
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.data.hasAllParameters",
                                            "operator": "==",
                                            "rightExpression": "false",
                                        }
                                    ],
                                },
                                "stateName": "FollowUp",
                            },
                            "type": "transitionbyname",
                            "_selected": True,
                            "transitionId": "refId1740431837457",
                            "id": "refId1740431837493",
                            "icon": "icon-transition",
                        },
                        {
                            "icon": "icon-script",
                            "name": "Execute Script",
                            "description": "",
                            "properties": {
                                "description": get_function_id_script["name"],
                                "scriptId": get_function_id_script["_id"],
                                "variableName": "functionId",
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "expansions": {
                                    "scriptId": {"name": get_function_id_script["name"]}
                                },
                                "_working": False,
                            },
                            "type": "script",
                            "_selected": True,
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
                    "tenantId": "nextivaretaildemo",
                    "actions": [
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
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                            },
                            "type": "googlettscollect",
                            "_selected": True,
                        },
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
                            "_selected": True,
                            "id": "refId1740283338201",
                            "icon": "icon-playdigits",
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
                "67bcd53e2b4d33bf671ba610": {
                    "category": "Standard",
                    "objectType": "campaignstate",
                    "campaignStateId": "67bcd53e2b4d33bf671ba610",
                    "name": "TakeAction",
                    "description": "Newly Created State",
                    "tenantId": "nextivaretaildemo",
                    "actions": [
                        {
                            "icon": "icon-function",
                            "name": "Execute Function",
                            "description": "",
                            "properties": {
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "functionExpression": "workitem.data.functionId",
                            },
                            "type": "function",
                            "_selected": True,
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
                                "stateName": "Webhook",
                            },
                            "type": "transitionbyname",
                            "_selected": False,
                            "transitionId": "refId1740420824069",
                        },
                    ],
                    "_id": "67bcd53e2b4d33bf671ba610",
                    "key": "67bcd53e2b4d33bf671ba610",
                    "location": "1377.2676533950016 165.8574496311703",
                    "transitions": [{"name": "Webhook", "id": "refId1740420824069"}],
                },
                "67bd02ee8a738c4befeec93a": {
                    "category": "Standard",
                    "objectType": "campaignstate",
                    "campaignStateId": "67bd02ee8a738c4befeec93a",
                    "name": "Goodbye",
                    "description": "Newly Created State",
                    "tenantId": "nextivaretaildemo",
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
                            "_selected": True,
                        },
                        {
                            "icon": "icon-tts",
                            "name": "Synthesize Text via Google TTS",
                            "description": "Thank you for contacting...",
                            "properties": {
                                "description": "Thank you for contacting...",
                                "voiceName": "en-US-Wavenet-J",
                                "text": '<prosody pitch="-2st">Thank you for contacting ${workitem.data.companyName} and have a great day!</prosody>',
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
                        "_selected": True,
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
                        "_selected": True,
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
                        "name": "Save Variable",
                        "description": "",
                        "properties": {
                            "description": "phone (inbound)",
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
                        "id": "refId1739934454000",
                        "icon": "icon-save",
                    },
                    {
                        "icon": "icon-save",
                        "name": "Save Variable",
                        "description": "",
                        "properties": {
                            "description": "phone (outbound)",
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
                        "_selected": True,
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
                "tenantId": "nextivaretaildemo",
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
                        "_selected": True,
                        "transitionId": "refId1739934453995",
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
                "location": "484.89646762282933 -76.7578027276301",
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
                        "description": "Thank you for contacting...",
                        "properties": {
                            "description": "Thank you for contacting...",
                            "condition": {
                                "conditionType": "NONE",
                                "expressions": [{"operator": "=="}],
                            },
                            "from": "workitem.data.companyName",
                            "message": "Thank you for contacting ${workitem.data.companyName}.",
                            "messageType": "BOT",
                            "options": [],
                        },
                        "type": "chatmessageconsumer",
                        "_selected": True,
                        "id": "refId1739600229945",
                        "icon": "icon-ai-message",
                    },
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
                "tenantId": "nextivaretaildemo",
                "actions": [
                    {
                        "icon": "icon-tts",
                        "name": "Play Collect Google TTS",
                        "description": "Thank you for contacting...",
                        "properties": {
                            "description": "Thank you for contacting...",
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
                        "_selected": True,
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
                "tenantId": "nextivaretaildemo",
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
                        "_selected": True,
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
                "tenantId": "nextivaretaildemo",
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
                        "_selected": True,
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
                "location": "764.6354547998594 951.1036263127032",
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
                                "conditionType": "NONE",
                                "expressions": [{"operator": "=="}],
                            },
                        },
                        "type": "googlettscollect",
                        "_selected": True,
                    },
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
                        "_selected": True,
                        "id": "refId1740283338201",
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
                "location": "1016.7270822936268 1132.3952901559198",
                "transitions": [{"name": "Loop", "id": "refId1739600227365"}],
            },
            "67b552f294171b486a3d1b7a": {
                "category": "Standard",
                "objectType": "campaignstate",
                "campaignStateId": "67b552f294171b486a3d1b7a",
                "name": "OutboundCall",
                "description": "Newly Created State",
                "tenantId": "nextivase2",
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
                        "_selected": True,
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
        },
        "finalWorkitemStateId": "67b1186f5510d9081ac8e32b",
        "finalUserStateId": "67b1186f5510d9081ac8e32b",
        "name": workflow_name,
    }

    if vertical == "general":
        inbound_call_menu = '<prosody pitch="-2st">Thank you for contacting ${workitem.data.companyName}. For sales, press 1. For customer service, press 2. For billing, press 3. For technical support, press 4. Otherwise, please stay on the line.</prosody>'
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
                "_selected": True,
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
        inbound_call_menu = '<prosody pitch="-2st">Thank you for contacting ${workitem.data.companyName}. To refill a prescription, press 1. To schedule, reschedule, or cancel an appointment, press 2. For billing, press 3. For customer service, press 4. Otherwise, please stay on the line.</prosody>'
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
                "_selected": True,
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
        inbound_call_menu = '<prosody pitch="-2st">Thank you for contacting ${workitem.data.companyName}. To apply for a new credit card, press 1. To apply for a new loan, press 2. To open a new checking or savings account, press 3. For billing, press 4. For customer service, press 5. Otherwise, please stay on the line.</prosody>'
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
                "_selected": True,
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
                "_selected": True,
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
        inbound_call_menu = '<prosody pitch="-2st">Thank you for contacting ${workitem.data.companyName}. To sign up for a new policy, or to make changes to an existing policy, press 1. To file a new claim, or check the status of an existing claim, press 2. For billing, press 3. For customer service, press 4. Otherwise, please stay on the line.</prosody>'
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
                "_selected": True,
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
                            "_selected": True,
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
                            "_selected": True,
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
                                "description": "phone (inbound)",
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
                            "id": "refId1739934454000",
                            "icon": "icon-save",
                        },
                        {
                            "icon": "icon-save",
                            "name": "Save Variable",
                            "description": "",
                            "properties": {
                                "description": "phone (outbound)",
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
                            "_selected": True,
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
                            "_selected": True,
                            "transitionId": "refId1740106542563",
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
                    "location": "484.89646762282933 -76.7578027276301",
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
                            "description": "Thank you for contacting...",
                            "properties": {
                                "description": "Thank you for contacting...",
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "from": "workitem.data.companyName",
                                "message": "Thank you for contacting ${workitem.data.companyName}.",
                                "messageType": "BOT",
                                "options": [],
                            },
                            "type": "chatmessageconsumer",
                            "_selected": True,
                            "id": "refId1739600229945",
                            "icon": "icon-ai-message",
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
                    "tenantId": "nextivaretaildemo",
                    "actions": [
                        {
                            "name": "Synthesize Text via Google TTS",
                            "description": "Thank you for contacting...",
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
                            "icon": "icon-tts",
                            "id": "refId1739600229678",
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
                            "_selected": True,
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
                    "tenantId": "nextivaretaildemo",
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
                            "_selected": True,
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
                    "tenantId": "nextivaretaildemo",
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
                            "_selected": True,
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
                    "location": "787.0836588751356 943.8304081923136",
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
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                            },
                            "type": "googlettscollect",
                            "_selected": True,
                        },
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
                            "_selected": True,
                            "id": "refId1740283338201",
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
                    "location": "1039.175286368903 1125.1220720355302",
                    "transitions": [{"name": "Loop", "id": "refId1739600227365"}],
                },
                "67b80e6253218fc5093deb5c": {
                    "category": "Standard",
                    "objectType": "campaignstate",
                    "campaignStateId": "67b80e6253218fc5093deb5c",
                    "name": "OutboundCall",
                    "description": "Newly Created State",
                    "tenantId": "nextivase2",
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
                            "_selected": True,
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
