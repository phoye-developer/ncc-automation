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
                "name": {"en": {"value": workflow_name}},
                "description": {"en": {"value": "IVA Workflow"}},
            },
            "states": {
                "67548667ca85e7eb0bed9d1d": {
                    "category": "Standard",
                    "campaignStateId": "67548667ca85e7eb0bed9d1d",
                    "actions": [
                        {
                            "name": "SMS Message Consumer",
                            "description": "",
                            "properties": {
                                "description": "InboundCall or InboundSMS",
                                "message": "Thank you for contacting ${workitem.data.companyName}! To take a brief survey, go to https://login.thrio.io/survey/?tenant=nextivase19&campaignId=67588455e3c06e3d040ca5df&context=%7B%22language%22%3A%22en%22%2C%22workitemId%22%3A%22${workitem.workitemId}%22%7D.",
                                "toAddress": "workitem.from",
                                "fromAddress": "workitem.to",
                                "createNewWorkitem": False,
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
                            "type": "smsmessageconsumer",
                            "_selected": False,
                            "id": "refId1736293727538",
                            "icon": "icon-ai-message",
                        },
                        {
                            "name": "SMS Message Consumer",
                            "description": "",
                            "properties": {
                                "description": "Chat",
                                "message": "Thank you for contacting ${workitem.data.companyName}. To take a brief survey, go to https://login.thrio.io/survey/?tenant=nextivase19&campaignId=67588455e3c06e3d040ca5df&context=%7B%22language%22%3A%22en%22%2C%22workitemId%22%3A%22${workitem.workitemId}%22%7D.",
                                "toAddress": "workitem.data.context.consumerData.phone",
                                "fromAddress": "'+14809192185'",
                                "createNewWorkitem": False,
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
                            "type": "smsmessageconsumer",
                            "_selected": True,
                            "id": "refId1736293727539",
                            "icon": "icon-ai-message",
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
                            "id": "refId1736293727540",
                            "icon": "icon-terminate",
                        },
                    ],
                    "objectType": "campaignstate",
                    "key": "67548667ca85e7eb0bed9d1d",
                    "_id": "67548667ca85e7eb0bed9d1d",
                    "description": "End State",
                    "name": "End State",
                    "location": "104.73465829197903 358.887243337547",
                    "transitions": [],
                },
                "start-state": {
                    "category": "Begin",
                    "campaignStateId": "start-state",
                    "actions": [
                        {
                            "icon": "icon-save",
                            "name": "Save Variable",
                            "description": "",
                            "properties": {
                                "description": "currency",
                                "rightExpression": "'$'",
                                "variableName": "currency",
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
                                "description": "liveTransfer",
                                "rightExpression": "false",
                                "variableName": "liveTransfer",
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
                            "id": "refId1738366172155",
                            "icon": "icon-save",
                        },
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
                                "description": "verified",
                                "rightExpression": "false",
                                "variableName": "verified",
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
                            "id": "refId1738366172157",
                            "icon": "icon-save",
                        },
                        {
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
                            "id": "refId1738366172158",
                            "icon": "icon-save",
                        },
                        {
                            "name": "Save Variable",
                            "description": "",
                            "properties": {
                                "description": "ccAmount",
                                "rightExpression": "6346",
                                "variableName": "ccAmount",
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
                            "id": "refId1738366172159",
                            "icon": "icon-save",
                        },
                        {
                            "name": "Execute Function",
                            "description": "",
                            "properties": {
                                "description": "SpinSci - Patient Lookup",
                                "functionId": "675486df3bf7aa24c8198202",
                                "functionExpression": "",
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "expansions": {
                                    "functionId": {"name": "SpinSci - Patient Lookup"}
                                },
                                "_working": False,
                            },
                            "type": "function",
                            "_selected": False,
                            "id": "refId1738366172160",
                            "icon": "icon-function",
                        },
                        {
                            "name": "Survey",
                            "description": "Transition to another state",
                            "properties": {
                                "description": "Survey",
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
                            "transitionId": "refId1733873034739",
                            "id": "refId1738366172161",
                            "icon": "icon-transition",
                        },
                        {
                            "name": "Chat",
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
                                "stateName": "Chat",
                            },
                            "type": "transitionbyname",
                            "_selected": False,
                            "transitionId": "refId1733592655593",
                            "id": "refId1738366172162",
                            "icon": "icon-transition",
                        },
                        {
                            "name": "InboundSMS",
                            "description": "Transition to another state",
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
                                "stateName": "InboundSMS",
                            },
                            "type": "transitionbyname",
                            "_selected": False,
                            "transitionId": "refId1733592655652",
                            "id": "refId1738366172163",
                            "icon": "icon-transition",
                        },
                        {
                            "name": "InboundCall",
                            "description": "Transition to another state",
                            "properties": {
                                "description": "InboundCall",
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
                                "stateName": "InboundCall",
                            },
                            "type": "transitionbyname",
                            "_selected": False,
                            "transitionId": "refId1733592655594",
                            "id": "refId1738366172164",
                            "icon": "icon-transition",
                        },
                        {
                            "name": "End State",
                            "description": "Transition to another state",
                            "properties": {
                                "description": "End State",
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "stateId": "67548667ca85e7eb0bed9d1d",
                            },
                            "type": "transition",
                            "_selected": False,
                            "transitionId": "refId1733592655667",
                            "id": "refId1738366172165",
                            "icon": "icon-transition",
                        },
                    ],
                    "transitions": [
                        {"name": "Survey", "id": "refId1733873034739"},
                        {"name": "Chat", "id": "refId1733592655593"},
                        {"name": "InboundSMS", "id": "refId1733592655652"},
                        {"name": "InboundCall", "id": "refId1733592655594"},
                        {"name": "End State", "id": "refId1733592655667"},
                    ],
                    "objectType": "campaignstate",
                    "key": "start-state",
                    "_id": "start-state",
                    "description": "Begin State",
                    "name": "Begin State",
                    "location": "-127.05378088864046 -24.43341940166158",
                },
                "67549fef8c3694beb965b21c": {
                    "category": "Standard",
                    "objectType": "campaignstate",
                    "campaignStateId": "67549fef8c3694beb965b21c",
                    "name": "Webhook",
                    "description": "Newly Created State",
                    "tenantId": "nextivase19",
                    "actions": [
                        {
                            "name": "Wait Chat Message",
                            "description": "",
                            "properties": {
                                "description": "workitem.type == 'Chat'",
                                "timeoutDuration": 3600000,
                                "stateId": "67548667ca85e7eb0bed9d1d",
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
                            "id": "refId1734645471839",
                            "icon": "icon-timer",
                        },
                        {
                            "name": "Execute REST Call",
                            "description": "",
                            "properties": {
                                "description": "Google Translation (to English)",
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
                                "responseVariable": "googletranslateresponse",
                                "restCallId": "675915e93bf7aa24c81986ac",
                                "expansions": {
                                    "restCallId": {
                                        "name": "Google Translation (to English)"
                                    }
                                },
                                "_working": False,
                            },
                            "type": "restapi",
                            "_selected": False,
                            "id": "refId1734645471840",
                            "icon": "icon-api",
                        },
                        {
                            "name": "Save Variable",
                            "description": "",
                            "properties": {
                                "description": "sourceLanguage",
                                "rightExpression": "workitem.data.googletranslateresponse.body.data.translations[0].detectedSourceLanguage",
                                "variableName": "sourceLanguage",
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
                            "id": "refId1734645471841",
                            "icon": "icon-save",
                        },
                        {
                            "name": "Message Bot",
                            "description": "",
                            "properties": {
                                "description": "Chat (English)",
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.type",
                                            "operator": "==",
                                            "rightExpression": "'Chat'",
                                        },
                                        {
                                            "leftExpression": "workitem.data.sourceLanguage",
                                            "operator": "==",
                                            "rightExpression": "'en'",
                                        },
                                    ],
                                },
                                "message": "$V.workitem.currentChatMessage.textMsg",
                                "event": "",
                                "serviceId": "6750b6e43bf7aa24c8197bfe",
                                "expansions": {
                                    "serviceId": {"name": "Dialogflow (HC)"}
                                },
                                "_working": False,
                            },
                            "type": "chatmessagebot",
                            "_selected": False,
                            "id": "refId1734645471842",
                            "icon": "icon-ai-message",
                        },
                        {
                            "name": "Message Bot",
                            "description": "",
                            "properties": {
                                "description": "Chat (Non-English)",
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.type",
                                            "operator": "==",
                                            "rightExpression": "'Chat'",
                                        },
                                        {
                                            "leftExpression": "workitem.data.sourceLanguage",
                                            "operator": "!=",
                                            "rightExpression": "'en'",
                                        },
                                    ],
                                },
                                "message": "$V.workitem.data.googletranslateresponse.body.data.translations[0].translatedText",
                                "event": "",
                                "serviceId": "6750b6e43bf7aa24c8197bfe",
                                "expansions": {
                                    "serviceId": {"name": "Dialogflow (HC)"}
                                },
                                "_working": False,
                            },
                            "type": "chatmessagebot",
                            "_selected": False,
                            "id": "refId1734645471843",
                            "icon": "icon-ai-message",
                        },
                        {
                            "name": "SMS Wait For Messages",
                            "description": "",
                            "properties": {
                                "description": "workitem.type == 'InboundSMS'",
                                "timeoutDuration": 3600000,
                                "stateId": "67548667ca85e7eb0bed9d1d",
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
                                            "operator": "!=",
                                            "rightExpression": "1",
                                        },
                                    ],
                                },
                            },
                            "type": "smswaitformessage",
                            "_selected": False,
                            "id": "refId1734645471844",
                            "icon": "icon-timer",
                        },
                        {
                            "name": "Message Bot",
                            "description": "",
                            "properties": {
                                "description": "workitem.type == 'InboundSMS'",
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
                                "serviceId": "6750b6e43bf7aa24c8197bfe",
                                "expansions": {
                                    "serviceId": {"name": "Dialogflow (HC)"}
                                },
                                "_working": False,
                            },
                            "type": "chatmessagebot",
                            "_selected": False,
                            "id": "refId1734645471845",
                            "icon": "icon-ai-message",
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
                            "id": "refId1734645471846",
                        },
                        {
                            "name": "Wait for messages",
                            "description": "",
                            "properties": {
                                "description": "Wait for a fulfillment response from Dialogflow",
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                            },
                            "type": "waitforbot",
                            "_selected": False,
                            "id": "refId1734645471847",
                            "icon": "icon-ai-message",
                        },
                        {
                            "name": "Execute Script",
                            "description": "",
                            "properties": {
                                "description": "Check hasAllParameters",
                                "scriptId": "67036ef0cc85b112bd1cae3e",
                                "variableName": "hasAllParameters",
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "expansions": {
                                    "scriptId": {"name": "Check hasAllParameters"}
                                },
                                "_working": False,
                            },
                            "type": "script",
                            "_selected": False,
                            "id": "refId1734645471848",
                            "icon": "icon-script",
                        },
                        {
                            "name": "FollowUp",
                            "description": "Transition to another state",
                            "properties": {
                                "description": "FollowUp",
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
                                "stateId": "6754a66807e637133888d11b",
                                "points": {
                                    "h": True,
                                    "r": [],
                                    "ct": 0,
                                    "__gohashid": 6972,
                                },
                            },
                            "type": "transition",
                            "_selected": False,
                            "transitionId": "refId1733592654758",
                            "id": "refId1734645471849",
                            "icon": "icon-transition",
                        },
                        {
                            "name": "Execute Script",
                            "description": "",
                            "properties": {
                                "description": "queueId",
                                "scriptId": "670370dccfd52b2fabf52f5c",
                                "variableName": "queueId",
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "expansions": {"scriptId": {"name": "Get queueId"}},
                                "_working": False,
                            },
                            "type": "script",
                            "_selected": False,
                            "id": "refId1734645471850",
                            "icon": "icon-script",
                        },
                        {
                            "name": "Execute Script",
                            "description": "",
                            "properties": {
                                "description": "surveyId",
                                "scriptId": "67037c2523f72d338ef3aa68",
                                "variableName": "surveyId",
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "expansions": {"scriptId": {"name": "Get surveyId"}},
                                "_working": False,
                            },
                            "type": "script",
                            "_selected": False,
                            "id": "refId1734645471851",
                            "icon": "icon-script",
                        },
                        {
                            "icon": "icon-script",
                            "name": "Execute Script",
                            "description": "",
                            "properties": {
                                "description": "priority",
                                "scriptId": "67649cb46aa5ac0fee70b93e",
                                "variableName": "priority",
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "expansions": {"scriptId": {"name": "Get priority"}},
                                "_working": False,
                            },
                            "type": "script",
                            "_selected": True,
                        },
                        {
                            "name": "Chat or InboundSMS",
                            "description": "Transition to another state",
                            "properties": {
                                "description": "Chat or InboundSMS",
                                "condition": {
                                    "conditionType": "OR",
                                    "expressions": [
                                        {
                                            "operator": "==",
                                            "leftExpression": "workitem.type",
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
                            "transitionId": "refId1733592654882",
                            "id": "refId1734645471852",
                            "icon": "icon-transition",
                        },
                        {
                            "name": "InboundCall",
                            "description": "Transition to another state",
                            "properties": {
                                "description": "InboundCall",
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
                                "stateName": "workitem.data.botWebhookRequest.queryResult.action",
                            },
                            "type": "transitionbyname",
                            "_selected": False,
                            "transitionId": "67561ee2e2c43cea855b41a6",
                            "id": "refId1734645471853",
                            "icon": "icon-transition",
                        },
                    ],
                    "_id": "67549fef8c3694beb965b21c",
                    "key": "67549fef8c3694beb965b21c",
                    "location": "645.3735128053632 308.11266549492274",
                    "transitions": [
                        {"name": "FollowUp", "id": "refId1733592654758"},
                        {"name": "Chat or InboundSMS", "id": "refId1733592654882"},
                        {"name": "InboundCall", "id": "67561ee2e2c43cea855b41a6"},
                    ],
                },
                "6754a52e31e712f586a54dce": {
                    "category": "Standard",
                    "objectType": "campaignstate",
                    "campaignStateId": "6754a52e31e712f586a54dce",
                    "name": "InboundCall",
                    "description": "Newly Created State",
                    "tenantId": "nextivase19",
                    "actions": [
                        {
                            "icon": "icon-dialogflow",
                            "name": "Transfer to Dialogflow",
                            "description": "",
                            "properties": {
                                "description": "+1 301-615-7514",
                                "address": "'+13016157514'",
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                            },
                            "type": "transfertodialogflow",
                            "_selected": True,
                        },
                        {
                            "icon": "icon-transition",
                            "name": "Webhook",
                            "description": "Transition to another state",
                            "properties": {
                                "description": "Webhook",
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "stateId": "67549fef8c3694beb965b21c",
                            },
                            "type": "transition",
                            "_selected": False,
                            "transitionId": "refId1733592654663",
                        },
                    ],
                    "_id": "6754a52e31e712f586a54dce",
                    "key": "6754a52e31e712f586a54dce",
                    "location": "346.2543127656253 149.5229978031253",
                    "transitions": [{"name": "Webhook", "id": "refId1733592654663"}],
                },
                "6754a66807e637133888d11b": {
                    "category": "Standard",
                    "objectType": "campaignstate",
                    "campaignStateId": "6754a66807e637133888d11b",
                    "name": "FollowUp",
                    "description": "Newly Created State",
                    "tenantId": "nextivase19",
                    "actions": [
                        {
                            "name": "Forward Bot Response",
                            "description": "Forward BOT response to consumer",
                            "properties": {
                                "description": "Chat (English)",
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.type",
                                            "operator": "==",
                                            "rightExpression": "'Chat'",
                                        },
                                        {
                                            "leftExpression": "workitem.data.sourceLanguage",
                                            "operator": "==",
                                            "rightExpression": "'en'",
                                        },
                                    ],
                                },
                                "from": "NEXT Healthcare",
                            },
                            "type": "chatforwardbotresponseconsumer",
                            "_selected": False,
                            "id": "refId1736293727193",
                            "icon": "icon-mail-forward",
                        },
                        {
                            "name": "Execute REST Call",
                            "description": "",
                            "properties": {
                                "description": "Google Translation (Chatbot to Source Language)",
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.type",
                                            "operator": "==",
                                            "rightExpression": "'Chat'",
                                        },
                                        {
                                            "leftExpression": "workitem.data.sourceLanguage",
                                            "operator": "!=",
                                            "rightExpression": "'en'",
                                        },
                                    ],
                                },
                                "responseVariable": "googletranslateresponse",
                                "restCallId": "6759159ccb6cdb0056107af8",
                                "expansions": {
                                    "restCallId": {
                                        "name": "Google Translation (Chatbot to Source Language)"
                                    }
                                },
                                "_working": False,
                            },
                            "type": "restapi",
                            "_selected": False,
                            "icon": "icon-api",
                            "id": "refId1736293727194",
                        },
                        {
                            "name": "Chat Message Consumer",
                            "description": "",
                            "properties": {
                                "description": "Chat (Non-English)",
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.type",
                                            "operator": "==",
                                            "rightExpression": "'Chat'",
                                        },
                                        {
                                            "leftExpression": "workitem.data.sourceLanguage",
                                            "operator": "!=",
                                            "rightExpression": "'en'",
                                        },
                                    ],
                                },
                                "from": "${workitem.data.companyName}",
                                "message": "$V.workitem.data.googletranslateresponse.body.data.translations[0].translatedText",
                                "messageType": "BOT",
                                "options": [],
                            },
                            "type": "chatmessageconsumer",
                            "_selected": False,
                            "icon": "icon-ai-message",
                            "id": "refId1736293727195",
                        },
                        {
                            "name": "SMS Message Consumer",
                            "description": "",
                            "properties": {
                                "description": "workitem.type == 'InboundSMS'",
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
                            "_selected": True,
                            "id": "refId1736293727196",
                            "icon": "icon-ai-message",
                        },
                        {
                            "name": "Webhook",
                            "description": "Transition to another state",
                            "properties": {
                                "description": "Webhook",
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "stateName": "Webhook",
                            },
                            "type": "transitionbyname",
                            "_selected": False,
                            "transitionId": "refId1733592655455",
                            "id": "refId1736293727197",
                            "icon": "icon-transition",
                        },
                    ],
                    "_id": "6754a66807e637133888d11b",
                    "key": "6754a66807e637133888d11b",
                    "location": "970 490",
                    "transitions": [{"name": "Webhook", "id": "refId1733592655455"}],
                },
                "6754d21cf309b28f125b9338": {
                    "category": "Standard",
                    "objectType": "campaignstate",
                    "campaignStateId": "6754d21cf309b28f125b9338",
                    "name": "ConnectAgent",
                    "description": "Newly Created State",
                    "tenantId": "nextivase19",
                    "actions": [
                        {
                            "name": "Save Variable",
                            "description": "",
                            "properties": {
                                "description": "liveTransfer",
                                "rightExpression": "true",
                                "variableName": "liveTransfer",
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
                            "id": "refId1736870642343",
                            "icon": "icon-save",
                        },
                        {
                            "name": "Save Variable",
                            "description": "",
                            "properties": {
                                "description": "nextMessage",
                                "rightExpression": "Please wait while I transfer you to an agent who can assist you.",
                                "variableName": "nextMessage",
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
                            "id": "refId1736870642344",
                            "icon": "icon-save",
                        },
                        {
                            "name": "Chat Message Consumer",
                            "description": "",
                            "properties": {
                                "description": "Please wait... (English)",
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.type",
                                            "operator": "==",
                                            "rightExpression": "'Chat'",
                                        },
                                        {
                                            "leftExpression": "workitem.data.sourceLanguage",
                                            "operator": "==",
                                            "rightExpression": "'en'",
                                        },
                                    ],
                                },
                                "from": "${workitem.data.companyName}",
                                "message": "Please wait while I transfer you to an agent who can assist you.",
                                "messageType": "BOT",
                                "options": [],
                            },
                            "type": "chatmessageconsumer",
                            "_selected": False,
                            "id": "refId1736870642345",
                            "icon": "icon-ai-message",
                        },
                        {
                            "name": "Execute REST Call",
                            "description": "",
                            "properties": {
                                "description": "Google Translation (Next Message to Source Language)",
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.type",
                                            "operator": "==",
                                            "rightExpression": "'Chat'",
                                        },
                                        {
                                            "leftExpression": "workitem.data.sourceLanguage",
                                            "operator": "!=",
                                            "rightExpression": "'en'",
                                        },
                                    ],
                                },
                                "responseVariable": "googletranslateresponse",
                                "restCallId": "67592dbd3bf7aa24c81986b0",
                                "expansions": {
                                    "restCallId": {
                                        "name": "Google Translation (Next Message to Source Language)"
                                    }
                                },
                                "_working": False,
                            },
                            "type": "restapi",
                            "_selected": False,
                            "id": "refId1736870642346",
                            "icon": "icon-api",
                        },
                        {
                            "name": "Chat Message Consumer",
                            "description": "",
                            "properties": {
                                "description": "Please wait... (Non-English)",
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.type",
                                            "operator": "==",
                                            "rightExpression": "'Chat'",
                                        },
                                        {
                                            "leftExpression": "workitem.data.sourceLanguage",
                                            "operator": "!=",
                                            "rightExpression": "'en'",
                                        },
                                    ],
                                },
                                "from": "${workitem.data.companyName}",
                                "message": "$V.workitem.data.googletranslateresponse.body.data.translations[0].translatedText",
                                "messageType": "BOT",
                                "options": [],
                            },
                            "type": "chatmessageconsumer",
                            "_selected": False,
                            "id": "refId1736870642347",
                            "icon": "icon-ai-message",
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
                            "id": "refId1736870642348",
                            "icon": "icon-ai-message",
                        },
                        {
                            "name": "Synthesize Text via Google TTS",
                            "description": "Convert Text into Audio using Google's Text-To-Speech",
                            "properties": {
                                "description": "Please wait...",
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
                            },
                            "type": "googletts",
                            "_selected": False,
                            "id": "refId1736870642349",
                            "icon": "icon-tts",
                        },
                        {
                            "name": "Execute Script",
                            "description": "",
                            "properties": {
                                "description": "Contact Info",
                                "scriptId": "6703724d50226e7fac14eff4",
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
                            "id": "refId1736870642350",
                            "icon": "icon-script",
                        },
                        {
                            "name": "Execute Script",
                            "description": "",
                            "properties": {
                                "description": "Get VIP status",
                                "scriptId": "6764a2e295da237375b528d6",
                                "variableName": "vip",
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "expansions": {"scriptId": {"name": "Get VIP status"}},
                                "_working": False,
                            },
                            "type": "script",
                            "_selected": False,
                            "id": "refId1736870642351",
                            "icon": "icon-script",
                        },
                        {
                            "name": "Save Variable",
                            "description": "",
                            "properties": {
                                "description": "priority",
                                "rightExpression": "Highest",
                                "variableName": "priority",
                                "asObject": False,
                                "dlpOption": False,
                                "wfmOption": False,
                                "dashboard": False,
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.data.vip",
                                            "operator": "==",
                                            "rightExpression": "true",
                                        }
                                    ],
                                },
                            },
                            "type": "savevariable",
                            "_selected": False,
                            "id": "refId1736870642352",
                            "icon": "icon-save",
                        },
                        {
                            "name": "Enter Queue from Expression",
                            "description": "",
                            "properties": {
                                "priorityExpression": "workitem.data.priority",
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
                            "_selected": True,
                            "id": "refId1736870642353",
                            "icon": "icon-enterqueues",
                        },
                        {
                            "name": "Execute Function",
                            "description": "",
                            "properties": {
                                "description": "MH - Two way Chat conversation (with translation)",
                                "functionId": "67591497cb6cdb0056107af7",
                                "functionExpression": "",
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
                                        "name": "MH - Two way Chat conversation (with translation)"
                                    }
                                },
                                "_working": False,
                            },
                            "type": "function",
                            "_selected": False,
                            "id": "refId1736870642354",
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
                            "id": "refId1736870642355",
                            "icon": "icon-function",
                        },
                        {
                            "name": "HoldQueue",
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
                                "stateId": "6754d3e1cebccc1b46fb81b9",
                                "points": {
                                    "h": True,
                                    "r": [],
                                    "ct": 0,
                                    "__gohashid": 18129,
                                },
                            },
                            "type": "transition",
                            "_selected": False,
                            "transitionId": "refId1733592655314",
                            "id": "refId1736870642356",
                            "icon": "icon-transition",
                        },
                    ],
                    "_id": "6754d21cf309b28f125b9338",
                    "key": "6754d21cf309b28f125b9338",
                    "location": "1291.8858968900809 138.65132175363544",
                    "transitions": [{"name": "HoldQueue", "id": "refId1733592655314"}],
                },
                "6754d3e1cebccc1b46fb81b9": {
                    "category": "Standard",
                    "objectType": "campaignstate",
                    "campaignStateId": "6754d3e1cebccc1b46fb81b9",
                    "name": "HoldQueue",
                    "description": "Newly Created State",
                    "tenantId": "nextivase19",
                    "actions": [
                        {
                            "icon": "icon-playdigits",
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
                        },
                        {
                            "icon": "icon-playdigits",
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
                            "id": "refId1733592655333",
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
                            "_selected": True,
                            "id": "refId1733592655346",
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
                            "id": "refId1733592655369",
                        },
                        {
                            "icon": "icon-transition",
                            "name": "HoldQueue",
                            "description": "Transition to another state",
                            "properties": {
                                "description": "HoldQueue",
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "stateName": "HoldQueue",
                            },
                            "type": "transitionbyname",
                            "_selected": False,
                            "id": "refId1733592655368",
                            "transitionId": "6754d499ccb6c1f8f6fe72de",
                        },
                    ],
                    "_id": "6754d3e1cebccc1b46fb81b9",
                    "key": "6754d3e1cebccc1b46fb81b9",
                    "location": "1591.6195351472147 271.0110364906225",
                    "transitions": [
                        {"name": "HoldQueue", "id": "6754d499ccb6c1f8f6fe72de"}
                    ],
                },
                "6754d66b14feffef0a0fe835": {
                    "category": "Standard",
                    "objectType": "campaignstate",
                    "campaignStateId": "6754d66b14feffef0a0fe835",
                    "name": "input.welcome",
                    "description": "Newly Created State",
                    "tenantId": "nextivase19",
                    "actions": [
                        {
                            "name": "Forward Bot Response",
                            "description": "Forward BOT response to consumer",
                            "properties": {
                                "description": "Chat (English)",
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.type",
                                            "operator": "==",
                                            "rightExpression": "'Chat'",
                                        },
                                        {
                                            "leftExpression": "workitem.data.sourceLanguage",
                                            "operator": "==",
                                            "rightExpression": "'en'",
                                        },
                                    ],
                                },
                                "from": "NEXT Healthcare",
                            },
                            "type": "chatforwardbotresponseconsumer",
                            "_selected": True,
                            "id": "refId1736293727288",
                            "icon": "icon-mail-forward",
                        },
                        {
                            "name": "Execute REST Call",
                            "description": "",
                            "properties": {
                                "description": "Google Translation (Chatbot to Source Language)",
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.type",
                                            "operator": "==",
                                            "rightExpression": "'Chat'",
                                        },
                                        {
                                            "leftExpression": "workitem.data.sourceLanguage",
                                            "operator": "!=",
                                            "rightExpression": "'en'",
                                        },
                                    ],
                                },
                                "responseVariable": "googletranslateresponse",
                                "restCallId": "6759159ccb6cdb0056107af8",
                                "expansions": {
                                    "restCallId": {
                                        "name": "Google Translation (Chatbot to Source Language)"
                                    }
                                },
                                "_working": False,
                            },
                            "type": "restapi",
                            "_selected": False,
                            "icon": "icon-api",
                            "id": "refId1736293727289",
                        },
                        {
                            "name": "Chat Message Consumer",
                            "description": "",
                            "properties": {
                                "description": "Chat (Non-English)",
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.type",
                                            "operator": "==",
                                            "rightExpression": "'Chat'",
                                        },
                                        {
                                            "leftExpression": "workitem.data.sourceLanguage",
                                            "operator": "!=",
                                            "rightExpression": "'en'",
                                        },
                                    ],
                                },
                                "from": "${workitem.data.companyName}",
                                "message": "$V.workitem.data.googletranslateresponse.body.data.translations[0].translatedText",
                                "messageType": "BOT",
                                "options": [],
                            },
                            "type": "chatmessageconsumer",
                            "_selected": False,
                            "icon": "icon-ai-message",
                            "id": "refId1736293727290",
                        },
                        {
                            "name": "SMS Message Consumer",
                            "description": "",
                            "properties": {
                                "description": "workitem.type == 'InboundSMS'",
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
                            "id": "refId1736293727291",
                            "icon": "icon-ai-message",
                        },
                        {
                            "name": "Webhook",
                            "description": "Transition to another state",
                            "properties": {
                                "description": "Webhook",
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "stateName": "Webhook",
                            },
                            "type": "transitionbyname",
                            "_selected": False,
                            "transitionId": "refId1733592655432",
                            "id": "refId1736293727292",
                            "icon": "icon-transition",
                        },
                    ],
                    "_id": "6754d66b14feffef0a0fe835",
                    "key": "6754d66b14feffef0a0fe835",
                    "location": "977.681174605216 141.4922316884425",
                    "transitions": [{"name": "Webhook", "id": "refId1733592655432"}],
                },
                "6754d6b1013b53b761521cb1": {
                    "category": "Standard",
                    "objectType": "campaignstate",
                    "campaignStateId": "6754d6b1013b53b761521cb1",
                    "name": "input.unknown",
                    "description": "Newly Created State",
                    "tenantId": "nextivase19",
                    "actions": [
                        {
                            "name": "Forward Bot Response",
                            "description": "Forward BOT response to consumer",
                            "properties": {
                                "description": "Chat (English)",
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.type",
                                            "operator": "==",
                                            "rightExpression": "'Chat'",
                                        },
                                        {
                                            "leftExpression": "workitem.data.sourceLanguage",
                                            "operator": "==",
                                            "rightExpression": "'en'",
                                        },
                                    ],
                                },
                                "from": "NEXT Healthcare",
                            },
                            "type": "chatforwardbotresponseconsumer",
                            "_selected": True,
                            "id": "refId1736293727271",
                            "icon": "icon-mail-forward",
                        },
                        {
                            "name": "Execute REST Call",
                            "description": "",
                            "properties": {
                                "description": "Google Translation (Chatbot to Source Language)",
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.type",
                                            "operator": "==",
                                            "rightExpression": "'Chat'",
                                        },
                                        {
                                            "leftExpression": "workitem.data.sourceLanguage",
                                            "operator": "!=",
                                            "rightExpression": "'en'",
                                        },
                                    ],
                                },
                                "responseVariable": "googletranslateresponse",
                                "restCallId": "6759159ccb6cdb0056107af8",
                                "expansions": {
                                    "restCallId": {
                                        "name": "Google Translation (Chatbot to Source Language)"
                                    }
                                },
                                "_working": False,
                            },
                            "type": "restapi",
                            "_selected": False,
                            "icon": "icon-api",
                            "id": "refId1736293727272",
                        },
                        {
                            "name": "Chat Message Consumer",
                            "description": "",
                            "properties": {
                                "description": "Chat (Non-English)",
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.type",
                                            "operator": "==",
                                            "rightExpression": "'Chat'",
                                        },
                                        {
                                            "leftExpression": "workitem.data.sourceLanguage",
                                            "operator": "!=",
                                            "rightExpression": "'en'",
                                        },
                                    ],
                                },
                                "from": "${workitem.data.companyName}",
                                "message": "$V.workitem.data.googletranslateresponse.body.data.translations[0].translatedText",
                                "messageType": "BOT",
                                "options": [],
                            },
                            "type": "chatmessageconsumer",
                            "_selected": False,
                            "icon": "icon-ai-message",
                            "id": "refId1736293727273",
                        },
                        {
                            "name": "SMS Message Consumer",
                            "description": "",
                            "properties": {
                                "description": "workitem.type == 'InboundSMS'",
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
                            "id": "refId1736293727274",
                            "icon": "icon-ai-message",
                        },
                        {
                            "name": "Webhook",
                            "description": "Transition to another state",
                            "properties": {
                                "description": "Webhook",
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "stateName": "Webhook",
                            },
                            "type": "transitionbyname",
                            "_selected": False,
                            "transitionId": "refId1733592655445",
                            "id": "refId1736293727275",
                            "icon": "icon-transition",
                        },
                    ],
                    "_id": "6754d6b1013b53b761521cb1",
                    "key": "6754d6b1013b53b761521cb1",
                    "location": "978.2321383050015 2.3998122501033095",
                    "transitions": [{"name": "Webhook", "id": "refId1733592655445"}],
                },
                "6754d9242071cae7ccc0408f": {
                    "category": "Standard",
                    "objectType": "campaignstate",
                    "campaignStateId": "6754d9242071cae7ccc0408f",
                    "name": "ScheduleAppt",
                    "description": "Newly Created State",
                    "tenantId": "nextivase19",
                    "actions": [
                        {
                            "name": "Save Variable",
                            "description": "",
                            "properties": {
                                "description": "action",
                                "rightExpression": "ScheduleAppt",
                                "variableName": "action",
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
                            "id": "refId1733699106764",
                        },
                        {
                            "name": "Save Variable",
                            "description": "",
                            "properties": {
                                "description": "actionPhrase",
                                "rightExpression": "schedule your appointment",
                                "variableName": "actionPhrase",
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
                            "id": "refId1733699106765",
                            "icon": "icon-save",
                        },
                        {
                            "name": "Verify",
                            "description": "Transition to another state",
                            "properties": {
                                "description": "Verify",
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.data.verified",
                                            "operator": "==",
                                            "rightExpression": "false",
                                        }
                                    ],
                                },
                                "stateName": "Verify",
                            },
                            "type": "transitionbyname",
                            "_selected": False,
                            "transitionId": "refId1733592655964",
                            "id": "refId1733699106766",
                            "icon": "icon-transition",
                        },
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
                                "from": "${workitem.data.companyName}",
                                "message": "Please wait while I schedule your appointment.",
                                "messageType": "BOT",
                                "options": [],
                            },
                            "type": "chatmessageconsumer",
                            "_selected": True,
                            "id": "refId1733699106767",
                            "icon": "icon-ai-message",
                        },
                        {
                            "name": "SMS Message Consumer",
                            "description": "",
                            "properties": {
                                "description": "Please wait...",
                                "message": "Please wait while I schedule your appointment.",
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
                            "id": "refId1733699106768",
                            "icon": "icon-ai-message",
                        },
                        {
                            "name": "Synthesize Text via Google TTS",
                            "description": "Convert Text into Audio using Google's Text-To-Speech",
                            "properties": {
                                "description": "Please wait...",
                                "voiceName": "en-US-Wavenet-J",
                                "text": '<prosody pitch="-2st">Please wait while I schedule your appointment.</prosody>',
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
                            "id": "refId1733699106769",
                            "icon": "icon-tts",
                        },
                        {
                            "name": "Webhook",
                            "description": "Transition to another state",
                            "properties": {
                                "description": "Webhook",
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "stateName": "Webhook",
                            },
                            "type": "transitionbyname",
                            "_selected": False,
                            "transitionId": "refId1733592655517",
                            "id": "refId1733699106770",
                            "icon": "icon-transition",
                        },
                    ],
                    "_id": "6754d9242071cae7ccc0408f",
                    "key": "6754d9242071cae7ccc0408f",
                    "location": "1059.7172096802483 -318.93998231888554",
                    "transitions": [
                        {"name": "Verify", "id": "refId1733592655964"},
                        {"name": "Webhook", "id": "refId1733592655517"},
                    ],
                },
                "6754d948bf9b42b9875f3441": {
                    "category": "Standard",
                    "objectType": "campaignstate",
                    "campaignStateId": "6754d948bf9b42b9875f3441",
                    "name": "RescheduleAppt",
                    "description": "Newly Created State",
                    "tenantId": "nextivase19",
                    "actions": [
                        {
                            "name": "Execute Script",
                            "description": "",
                            "properties": {
                                "description": "Get date",
                                "scriptId": "6750dbe7e3c06e3d040c9c3d",
                                "variableName": "date",
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "expansions": {"scriptId": {"name": "Get date"}},
                                "_working": False,
                            },
                            "type": "script",
                            "_selected": False,
                            "id": "refId1736293726963",
                            "icon": "icon-script",
                        },
                        {
                            "name": "Execute Script",
                            "description": "",
                            "properties": {
                                "description": "Get time",
                                "scriptId": "6750dc09c3e1f25ae7bb4b20",
                                "variableName": "time",
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "expansions": {"scriptId": {"name": "Get time"}},
                                "_working": False,
                            },
                            "type": "script",
                            "_selected": False,
                            "id": "refId1736293726964",
                            "icon": "icon-script",
                        },
                        {
                            "name": "Retrieve the call",
                            "description": "",
                            "properties": {
                                "description": "workitem.type == 'InboundCall'",
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
                            "type": "dialogflowtakeback",
                            "_selected": False,
                            "id": "refId1736293726965",
                            "icon": "icon-dialogflow",
                        },
                        {
                            "name": "Save Variable",
                            "description": "",
                            "properties": {
                                "description": "action",
                                "rightExpression": "RescheduleAppt",
                                "variableName": "action",
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
                            "id": "refId1736293726966",
                            "icon": "icon-save",
                        },
                        {
                            "name": "Save Variable",
                            "description": "",
                            "properties": {
                                "description": "actionPhrase",
                                "rightExpression": "reschedule your appointment",
                                "variableName": "actionPhrase",
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
                            "id": "refId1736293726967",
                            "icon": "icon-save",
                        },
                        {
                            "name": "Verify",
                            "description": "Transition to another state",
                            "properties": {
                                "description": "Verify",
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.data.verified",
                                            "operator": "==",
                                            "rightExpression": "false",
                                        }
                                    ],
                                },
                                "stateName": "Verify",
                            },
                            "type": "transitionbyname",
                            "_selected": False,
                            "transitionId": "refId1733592655978",
                            "id": "refId1736293726968",
                            "icon": "icon-transition",
                        },
                        {
                            "name": "Execute Function",
                            "description": "",
                            "properties": {
                                "description": "SpinSci - Appointment Lookup (with translation)",
                                "functionId": "675945003fb21379dc622fb5",
                                "functionExpression": "",
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "expansions": {
                                    "functionId": {
                                        "name": "SpinSci - Appointment Lookup (with translation)"
                                    }
                                },
                                "_working": False,
                            },
                            "type": "function",
                            "_selected": False,
                            "id": "refId1736293726969",
                            "icon": "icon-function",
                        },
                        {
                            "name": "ConnectAgent",
                            "description": "Transition to another state",
                            "properties": {
                                "description": "workitem.data.apptLookupResult != Found",
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.data.apptLookupResult",
                                            "operator": "!=",
                                            "rightExpression": "'Found'",
                                        }
                                    ],
                                },
                                "stateName": "ConnectAgent",
                            },
                            "type": "transitionbyname",
                            "_selected": False,
                            "transitionId": "refId1733699103083",
                            "id": "refId1736293726970",
                            "icon": "icon-transition",
                        },
                        {
                            "name": "Save Variable",
                            "description": "",
                            "properties": {
                                "description": "nextMessage",
                                "rightExpression": "Please wait while I reschedule your appointment.",
                                "variableName": "nextMessage",
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
                            "id": "refId1736293726971",
                            "icon": "icon-save",
                        },
                        {
                            "name": "Chat Message Consumer",
                            "description": "",
                            "properties": {
                                "description": "Please wait... (English)",
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.type",
                                            "operator": "==",
                                            "rightExpression": "'Chat'",
                                        },
                                        {
                                            "leftExpression": "workitem.data.sourceLanguage",
                                            "operator": "==",
                                            "rightExpression": "'en'",
                                        },
                                    ],
                                },
                                "from": "${workitem.data.companyName}",
                                "message": "Please wait while I reschedule your appointment.",
                                "messageType": "BOT",
                                "options": [],
                            },
                            "type": "chatmessageconsumer",
                            "_selected": False,
                            "id": "refId1736293726972",
                            "icon": "icon-ai-message",
                        },
                        {
                            "name": "Execute REST Call",
                            "description": "",
                            "properties": {
                                "description": "Google Translation (Next Message to Source Language)",
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.type",
                                            "operator": "==",
                                            "rightExpression": "'Chat'",
                                        },
                                        {
                                            "leftExpression": "workitem.data.sourceLanguage",
                                            "operator": "!=",
                                            "rightExpression": "'en'",
                                        },
                                    ],
                                },
                                "responseVariable": "googletranslateresponse",
                                "restCallId": "67592dbd3bf7aa24c81986b0",
                                "expansions": {
                                    "restCallId": {
                                        "name": "Google Translation (Next Message to Source Language)"
                                    }
                                },
                                "_working": False,
                            },
                            "type": "restapi",
                            "_selected": False,
                            "id": "refId1736293726973",
                            "icon": "icon-api",
                        },
                        {
                            "name": "Chat Message Consumer",
                            "description": "",
                            "properties": {
                                "description": "Please wait... (Non-English)",
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.type",
                                            "operator": "==",
                                            "rightExpression": "'Chat'",
                                        },
                                        {
                                            "leftExpression": "workitem.data.sourceLanguage",
                                            "operator": "!=",
                                            "rightExpression": "'en'",
                                        },
                                    ],
                                },
                                "from": "${workitem.data.companyName}",
                                "message": "$V.workitem.data.googletranslateresponse.body.data.translations[0].translatedText",
                                "messageType": "BOT",
                                "options": [],
                            },
                            "type": "chatmessageconsumer",
                            "_selected": False,
                            "id": "refId1736293726974",
                            "icon": "icon-ai-message",
                        },
                        {
                            "name": "SMS Message Consumer",
                            "description": "",
                            "properties": {
                                "description": "Please wait...",
                                "message": "Please wait while I reschedule your appointment.",
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
                            "id": "refId1736293726975",
                            "icon": "icon-ai-message",
                        },
                        {
                            "name": "Synthesize Text via Google TTS",
                            "description": "Convert Text into Audio using Google's Text-To-Speech",
                            "properties": {
                                "description": "Please wait...",
                                "voiceName": "en-US-Wavenet-J",
                                "text": '<prosody pitch="-2st">Please wait while I reschedule your appointment.</prosody>',
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
                            "id": "refId1736293726976",
                            "icon": "icon-tts",
                        },
                        {
                            "name": "Execute REST Call",
                            "description": "",
                            "properties": {
                                "description": "Spinsci-Reschedule appointment",
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "responseVariable": "rescheduleApptResponse",
                                "restCallId": "6740646d7a6d716bb5a83f0a",
                                "expansions": {
                                    "restCallId": {
                                        "name": "Spinsci-Reschedule appointment"
                                    }
                                },
                                "_working": False,
                            },
                            "type": "restapi",
                            "_selected": False,
                            "id": "refId1736293726977",
                            "icon": "icon-api",
                        },
                        {
                            "name": "Start Timer",
                            "description": "",
                            "properties": {
                                "timeoutInSeconds": "2",
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                            },
                            "type": "starttimer",
                            "_selected": False,
                            "id": "refId1736293726978",
                            "icon": "icon-timer",
                        },
                        {
                            "name": "Save Variable",
                            "description": "",
                            "properties": {
                                "description": "nextMessage",
                                "rightExpression": "Your appointment has been rescheduled for ${workitem.data.date}. What else can I help you with today?",
                                "variableName": "nextMessage",
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
                            "id": "refId1736293726979",
                            "icon": "icon-save",
                        },
                        {
                            "name": "Chat Message Consumer",
                            "description": "",
                            "properties": {
                                "description": "Your appointment has been rescheduled for... (English)",
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.type",
                                            "operator": "==",
                                            "rightExpression": "'Chat'",
                                        },
                                        {
                                            "leftExpression": "workitem.data.sourceLanguage",
                                            "operator": "==",
                                            "rightExpression": "'en'",
                                        },
                                    ],
                                },
                                "from": "${workitem.data.companyName}",
                                "message": "Your appointment has been rescheduled for ${workitem.data.date}. What else can I help you with today?",
                                "messageType": "BOT",
                                "options": [
                                    {"label": "Get Location", "value": "Get Location"},
                                    {
                                        "label": "Find a Doctor",
                                        "value": "Find a Doctor",
                                    },
                                    {
                                        "label": "Refill Prescription",
                                        "value": "Refill Prescription",
                                    },
                                ],
                            },
                            "type": "chatmessageconsumer",
                            "_selected": False,
                            "id": "refId1736293726980",
                            "icon": "icon-ai-message",
                        },
                        {
                            "name": "Execute REST Call",
                            "description": "",
                            "properties": {
                                "description": "Google Translation (Next Message to Source Language)",
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.type",
                                            "operator": "==",
                                            "rightExpression": "'Chat'",
                                        },
                                        {
                                            "leftExpression": "workitem.data.sourceLanguage",
                                            "operator": "!=",
                                            "rightExpression": "'en'",
                                        },
                                    ],
                                },
                                "responseVariable": "googletranslateresponse",
                                "restCallId": "67592dbd3bf7aa24c81986b0",
                                "expansions": {
                                    "restCallId": {
                                        "name": "Google Translation (Next Message to Source Language)"
                                    }
                                },
                                "_working": False,
                            },
                            "type": "restapi",
                            "_selected": False,
                            "id": "refId1736293726981",
                            "icon": "icon-api",
                        },
                        {
                            "name": "Chat Message Consumer",
                            "description": "",
                            "properties": {
                                "description": "Your appointment has been rescheduled for... (Non-English)",
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.type",
                                            "operator": "==",
                                            "rightExpression": "'Chat'",
                                        },
                                        {
                                            "leftExpression": "workitem.data.sourceLanguage",
                                            "operator": "!=",
                                            "rightExpression": "'en'",
                                        },
                                    ],
                                },
                                "from": "${workitem.data.companyName}",
                                "message": "$V.workitem.data.googletranslateresponse.body.data.translations[0].translatedText",
                                "messageType": "BOT",
                                "options": [],
                            },
                            "type": "chatmessageconsumer",
                            "_selected": False,
                            "id": "refId1736293726982",
                            "icon": "icon-ai-message",
                        },
                        {
                            "name": "SMS Message Consumer",
                            "description": "",
                            "properties": {
                                "description": "Your appointment has been rescheduled for...",
                                "message": "Your appointment has been rescheduled for ${workitem.data.date}. What else can I help you with today?",
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
                            "id": "refId1736293726983",
                            "icon": "icon-ai-message",
                        },
                        {
                            "name": "Synthesize Text via Google TTS",
                            "description": "Convert Text into Audio using Google's Text-To-Speech",
                            "properties": {
                                "description": "Your appointment has been rescheduled for...",
                                "voiceName": "en-US-Wavenet-J",
                                "text": '<prosody pitch="-2st">Your appointment has been rescheduled for ${workitem.data.date}. Thank you and have a great day!</prosody>',
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
                            "id": "refId1736293726984",
                            "icon": "icon-tts",
                        },
                        {
                            "name": "SMS Message Consumer",
                            "description": "",
                            "properties": {
                                "description": "workitem.type == 'InboundCall'",
                                "message": "Hi, this is ${workitem.data.companyName}! Your appointment has been rescheduled for ${workitem.data.date}. Reply back with any questions!",
                                "toAddress": "workitem.from",
                                "fromAddress": "workitem.to",
                                "createNewWorkitem": False,
                                "condition": {
                                    "conditionType": "OR",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.type",
                                            "operator": "==",
                                            "rightExpression": "'InboundCall'",
                                        }
                                    ],
                                },
                            },
                            "type": "smsmessageconsumer",
                            "_selected": False,
                            "id": "refId1736293726985",
                            "icon": "icon-ai-message",
                        },
                        {
                            "name": "End State",
                            "description": "Transition to another state",
                            "properties": {
                                "description": "workitem.type == 'InboundCall'",
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
                                "stateName": "End State",
                            },
                            "type": "transitionbyname",
                            "_selected": False,
                            "transitionId": "refId1733699104431",
                            "id": "refId1736293726986",
                            "icon": "icon-transition",
                        },
                        {
                            "name": "SMS Message Consumer",
                            "description": "",
                            "properties": {
                                "description": "workitem.type == 'Chat'",
                                "message": "Hi, this is ${workitem.data.companyName}! Your appointment has been rescheduled for ${workitem.data.date}. Reply back with any questions!",
                                "toAddress": "workitem.data.context.consumerData.phone",
                                "fromAddress": "'+14809192185'",
                                "createNewWorkitem": False,
                                "condition": {
                                    "conditionType": "OR",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.type",
                                            "operator": "==",
                                            "rightExpression": "'Chat'",
                                        }
                                    ],
                                },
                            },
                            "type": "smsmessageconsumer",
                            "_selected": True,
                            "id": "refId1736293726987",
                            "icon": "icon-ai-message",
                        },
                        {
                            "name": "Webhook",
                            "description": "Transition to another state",
                            "properties": {
                                "description": "Webhook",
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [],
                                },
                                "stateName": "Webhook",
                            },
                            "type": "transitionbyname",
                            "_selected": False,
                            "transitionId": "refId1733592655529",
                            "id": "refId1736293726988",
                            "icon": "icon-transition",
                        },
                    ],
                    "_id": "6754d948bf9b42b9875f3441",
                    "key": "6754d948bf9b42b9875f3441",
                    "location": "1295.106319285092 -273.3481790910305",
                    "transitions": [
                        {"name": "Verify", "id": "refId1733592655978"},
                        {"name": "ConnectAgent", "id": "refId1733699103083"},
                        {"name": "End State", "id": "refId1733699104431"},
                        {"name": "Webhook", "id": "refId1733592655529"},
                    ],
                },
                "6754d9691a335d2b40f9da7d": {
                    "category": "Standard",
                    "objectType": "campaignstate",
                    "campaignStateId": "6754d9691a335d2b40f9da7d",
                    "name": "CancelAppt",
                    "description": "Newly Created State",
                    "tenantId": "nextivase19",
                    "actions": [
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
                                },
                                "description": "workitem.type == 'InboundCall'",
                            },
                            "type": "dialogflowtakeback",
                            "_selected": False,
                            "id": "refId1736293727021",
                            "icon": "icon-dialogflow",
                        },
                        {
                            "name": "Save Variable",
                            "description": "",
                            "properties": {
                                "description": "action",
                                "rightExpression": "CancelAppt",
                                "variableName": "action",
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
                            "id": "refId1736293727022",
                            "icon": "icon-save",
                        },
                        {
                            "name": "Save Variable",
                            "description": "",
                            "properties": {
                                "description": "actionPhrase",
                                "rightExpression": "cancel your appointment",
                                "variableName": "actionPhrase",
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
                            "id": "refId1736293727023",
                            "icon": "icon-save",
                        },
                        {
                            "name": "Verify",
                            "description": "Transition to another state",
                            "properties": {
                                "description": "Verify",
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.data.verified",
                                            "operator": "==",
                                            "rightExpression": "false",
                                        }
                                    ],
                                },
                                "stateName": "Verify",
                            },
                            "type": "transitionbyname",
                            "_selected": False,
                            "transitionId": "refId1733592656022",
                            "id": "refId1736293727024",
                            "icon": "icon-transition",
                        },
                        {
                            "name": "Execute Function",
                            "description": "",
                            "properties": {
                                "description": "SpinSci - Appointment Lookup (with translation)",
                                "functionId": "675945003fb21379dc622fb5",
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "expansions": {
                                    "functionId": {
                                        "name": "SpinSci - Appointment Lookup (with translation)"
                                    }
                                },
                                "_working": False,
                                "functionExpression": "",
                            },
                            "type": "function",
                            "_selected": False,
                            "id": "refId1736293727025",
                            "icon": "icon-function",
                        },
                        {
                            "name": "ConnectAgent",
                            "description": "Transition to another state",
                            "properties": {
                                "description": "workitem.data.apptLookupResult != Found",
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.data.apptLookupResult",
                                            "operator": "!=",
                                            "rightExpression": "'Found'",
                                        }
                                    ],
                                },
                                "stateName": "ConnectAgent",
                            },
                            "type": "transitionbyname",
                            "_selected": False,
                            "transitionId": "refId1733699107755",
                            "id": "refId1736293727026",
                            "icon": "icon-transition",
                        },
                        {
                            "name": "Save Variable",
                            "description": "",
                            "properties": {
                                "description": "nextMessage",
                                "rightExpression": "Please wait while I cancel your appointment.",
                                "variableName": "nextMessage",
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
                            "id": "refId1736293727027",
                            "icon": "icon-save",
                        },
                        {
                            "name": "Chat Message Consumer",
                            "description": "",
                            "properties": {
                                "description": "Please wait... (English)",
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.type",
                                            "operator": "==",
                                            "rightExpression": "'Chat'",
                                        },
                                        {
                                            "leftExpression": "workitem.data.sourceLanguage",
                                            "operator": "==",
                                            "rightExpression": "'en'",
                                        },
                                    ],
                                },
                                "from": "${workitem.data.companyName}",
                                "message": "Please wait while I cancel your appointment.",
                                "messageType": "BOT",
                                "options": [],
                            },
                            "type": "chatmessageconsumer",
                            "_selected": False,
                            "id": "refId1736293727028",
                            "icon": "icon-ai-message",
                        },
                        {
                            "name": "Execute REST Call",
                            "description": "",
                            "properties": {
                                "description": "Google Translation (Next Message to Source Language)",
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.type",
                                            "operator": "==",
                                            "rightExpression": "'Chat'",
                                        },
                                        {
                                            "leftExpression": "workitem.data.sourceLanguage",
                                            "operator": "!=",
                                            "rightExpression": "'en'",
                                        },
                                    ],
                                },
                                "responseVariable": "googletranslateresponse",
                                "restCallId": "67592dbd3bf7aa24c81986b0",
                                "expansions": {
                                    "restCallId": {
                                        "name": "Google Translation (Next Message to Source Language)"
                                    }
                                },
                                "_working": False,
                            },
                            "type": "restapi",
                            "_selected": False,
                            "id": "refId1736293727029",
                            "icon": "icon-api",
                        },
                        {
                            "name": "Chat Message Consumer",
                            "description": "",
                            "properties": {
                                "description": "Please wait... (Non-English)",
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.type",
                                            "operator": "==",
                                            "rightExpression": "'Chat'",
                                        },
                                        {
                                            "leftExpression": "workitem.data.sourceLanguage",
                                            "operator": "!=",
                                            "rightExpression": "'en'",
                                        },
                                    ],
                                },
                                "from": "${workitem.data.companyName}",
                                "message": "$V.workitem.data.googletranslateresponse.body.data.translations[0].translatedText",
                                "messageType": "BOT",
                                "options": [],
                            },
                            "type": "chatmessageconsumer",
                            "_selected": False,
                            "id": "refId1736293727030",
                            "icon": "icon-ai-message",
                        },
                        {
                            "name": "SMS Message Consumer",
                            "description": "",
                            "properties": {
                                "description": "Please wait...",
                                "message": "Please wait while I cancel your appointment.",
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
                            "id": "refId1736293727031",
                            "icon": "icon-ai-message",
                        },
                        {
                            "name": "Synthesize Text via Google TTS",
                            "description": "Convert Text into Audio using Google's Text-To-Speech",
                            "properties": {
                                "description": "Please wait...",
                                "voiceName": "en-US-Wavenet-J",
                                "text": '<prosody pitch="-2st">Please wait while I cancel your appointment.</prosody>',
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
                            "id": "refId1736293727032",
                            "icon": "icon-tts",
                        },
                        {
                            "name": "Execute REST Call",
                            "description": "",
                            "properties": {
                                "description": "Spinsci - cancelAppointment",
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "responseVariable": "cancelApptResponse",
                                "restCallId": "673ef796186614179724fccf",
                                "expansions": {
                                    "restCallId": {
                                        "name": "Spinsci - cancelAppointment"
                                    }
                                },
                                "_working": False,
                            },
                            "type": "restapi",
                            "_selected": False,
                            "id": "refId1736293727033",
                            "icon": "icon-api",
                        },
                        {
                            "name": "Start Timer",
                            "description": "",
                            "properties": {
                                "timeoutInSeconds": "2",
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                            },
                            "type": "starttimer",
                            "_selected": False,
                            "id": "refId1736293727034",
                            "icon": "icon-timer",
                        },
                        {
                            "name": "Save Variable",
                            "description": "",
                            "properties": {
                                "description": "nextMessage",
                                "rightExpression": "Your appointment has been cancelled.",
                                "variableName": "nextMessage",
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
                            "id": "refId1736293727035",
                            "icon": "icon-save",
                        },
                        {
                            "name": "Chat Message Consumer",
                            "description": "",
                            "properties": {
                                "description": "Your appointment has been cancelled. (English)",
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.type",
                                            "operator": "==",
                                            "rightExpression": "'Chat'",
                                        },
                                        {
                                            "leftExpression": "workitem.data.sourceLanguage",
                                            "operator": "==",
                                            "rightExpression": "'en'",
                                        },
                                    ],
                                },
                                "from": "${workitem.data.companyName}",
                                "message": "Your appointment has been cancelled. What else can I help you with today?",
                                "messageType": "BOT",
                                "options": [
                                    {"label": "Get Location", "value": "Get Location"},
                                    {
                                        "label": "Find a Doctor",
                                        "value": "Find a Doctor",
                                    },
                                    {
                                        "label": "Refill Prescription",
                                        "value": "Refill Prescription",
                                    },
                                ],
                            },
                            "type": "chatmessageconsumer",
                            "_selected": False,
                            "id": "refId1736293727036",
                            "icon": "icon-ai-message",
                        },
                        {
                            "name": "Execute REST Call",
                            "description": "",
                            "properties": {
                                "description": "Google Translation (Next Message to Source Language)",
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.type",
                                            "operator": "==",
                                            "rightExpression": "'Chat'",
                                        },
                                        {
                                            "leftExpression": "workitem.data.sourceLanguage",
                                            "operator": "!=",
                                            "rightExpression": "'en'",
                                        },
                                    ],
                                },
                                "responseVariable": "googletranslateresponse",
                                "restCallId": "67592dbd3bf7aa24c81986b0",
                                "expansions": {
                                    "restCallId": {
                                        "name": "Google Translation (Next Message to Source Language)"
                                    }
                                },
                                "_working": False,
                            },
                            "type": "restapi",
                            "_selected": False,
                            "id": "refId1736293727037",
                            "icon": "icon-api",
                        },
                        {
                            "name": "Chat Message Consumer",
                            "description": "",
                            "properties": {
                                "description": "Your appointment has been cancelled. (Non-English)",
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.type",
                                            "operator": "==",
                                            "rightExpression": "'Chat'",
                                        },
                                        {
                                            "leftExpression": "workitem.data.sourceLanguage",
                                            "operator": "!=",
                                            "rightExpression": "'en'",
                                        },
                                    ],
                                },
                                "from": "${workitem.data.companyName}",
                                "message": "$V.workitem.data.googletranslateresponse.body.data.translations[0].translatedText",
                                "messageType": "BOT",
                                "options": [],
                            },
                            "type": "chatmessageconsumer",
                            "_selected": False,
                            "id": "refId1736293727038",
                            "icon": "icon-ai-message",
                        },
                        {
                            "name": "SMS Message Consumer",
                            "description": "",
                            "properties": {
                                "description": "Your appointment has been cancelled.",
                                "message": "Your appointment has been cancelled. What else can I help you with today?",
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
                            "id": "refId1736293727039",
                            "icon": "icon-ai-message",
                        },
                        {
                            "name": "Synthesize Text via Google TTS",
                            "description": "Convert Text into Audio using Google's Text-To-Speech",
                            "properties": {
                                "description": "Your appointment has been cancelled.",
                                "voiceName": "en-US-Wavenet-J",
                                "text": '<prosody pitch="-2st">Your appointment has been cancelled. Thank you for calling and have a great day!</prosody>',
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
                            "id": "refId1736293727040",
                            "icon": "icon-tts",
                        },
                        {
                            "name": "SMS Message Consumer",
                            "description": "",
                            "properties": {
                                "description": "workitem.type == 'InboundCall'",
                                "message": "Hi, this is ${workitem.data.companyName}! Your appointment has been cancelled. Reply back with any questions!",
                                "toAddress": "workitem.from",
                                "fromAddress": "workitem.to",
                                "createNewWorkitem": False,
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
                            "type": "smsmessageconsumer",
                            "_selected": False,
                            "id": "refId1736293727041",
                            "icon": "icon-ai-message",
                        },
                        {
                            "name": "End State",
                            "description": "Transition to another state",
                            "properties": {
                                "description": "workitem.type == 'InboundCall'",
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
                                "stateName": "End State",
                            },
                            "type": "transitionbyname",
                            "_selected": False,
                            "transitionId": "refId1733699108123",
                            "id": "refId1736293727042",
                            "icon": "icon-transition",
                        },
                        {
                            "name": "SMS Message Consumer",
                            "description": "",
                            "properties": {
                                "description": "workitem.type == 'Chat'",
                                "message": "Hi, this is ${workitem.data.companyName}! Your appointment has been cancelled. Reply back with any questions!",
                                "toAddress": "workitem.data.context.consumerData.phone",
                                "fromAddress": "'+14809192185'",
                                "createNewWorkitem": False,
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
                            "type": "smsmessageconsumer",
                            "_selected": True,
                            "id": "refId1736293727043",
                            "icon": "icon-ai-message",
                        },
                        {
                            "name": "Webhook",
                            "description": "Transition to another state",
                            "properties": {
                                "description": "Webhook",
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "stateName": "Webhook",
                            },
                            "type": "transitionbyname",
                            "_selected": False,
                            "transitionId": "refId1733592655542",
                            "id": "refId1736293727044",
                            "icon": "icon-transition",
                        },
                    ],
                    "_id": "6754d9691a335d2b40f9da7d",
                    "key": "6754d9691a335d2b40f9da7d",
                    "location": "1530.297258596479 -273.8989790871552",
                    "transitions": [
                        {"name": "Verify", "id": "refId1733592656022"},
                        {"name": "ConnectAgent", "id": "refId1733699107755"},
                        {"name": "End State", "id": "refId1733699108123"},
                        {"name": "Webhook", "id": "refId1733592655542"},
                    ],
                },
                "6754d9c04898b3bca10e5363": {
                    "category": "Standard",
                    "objectType": "campaignstate",
                    "campaignStateId": "6754d9c04898b3bca10e5363",
                    "name": "RequestRefill",
                    "description": "Newly Created State",
                    "tenantId": "nextivase19",
                    "actions": [
                        {
                            "name": "Retrieve the call",
                            "description": "",
                            "properties": {
                                "description": "workitem.type == 'InboundCall'",
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
                            "type": "dialogflowtakeback",
                            "_selected": False,
                            "id": "refId1736293727069",
                            "icon": "icon-dialogflow",
                        },
                        {
                            "name": "Save Variable",
                            "description": "",
                            "properties": {
                                "description": "action",
                                "rightExpression": "RequestRefill",
                                "variableName": "action",
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
                            "id": "refId1736293727070",
                            "icon": "icon-save",
                        },
                        {
                            "name": "Save Variable",
                            "description": "",
                            "properties": {
                                "description": "actionPhrase",
                                "rightExpression": "refill your prescription",
                                "variableName": "actionPhrase",
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
                            "id": "refId1736293727071",
                            "icon": "icon-save",
                        },
                        {
                            "name": "Verify",
                            "description": "Transition to another state",
                            "properties": {
                                "description": "Verify",
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.data.verified",
                                            "operator": "==",
                                            "rightExpression": "false",
                                        }
                                    ],
                                },
                                "stateName": "Verify",
                            },
                            "type": "transitionbyname",
                            "_selected": False,
                            "transitionId": "refId1733592656036",
                            "id": "refId1736293727072",
                            "icon": "icon-transition",
                        },
                        {
                            "name": "Execute Function",
                            "description": "",
                            "properties": {
                                "description": "SpinSci - Prescription Lookup (with translation)",
                                "functionId": "67593e50e3c06e3d040ca6e1",
                                "functionExpression": "",
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "expansions": {
                                    "functionId": {
                                        "name": "SpinSci - Prescription Lookup (with translation)"
                                    }
                                },
                                "_working": False,
                            },
                            "type": "function",
                            "_selected": False,
                            "id": "refId1736293727073",
                            "icon": "icon-function",
                        },
                        {
                            "name": "ConnectAgent",
                            "description": "Transition to another state",
                            "properties": {
                                "description": "workitem.data.prescriptionLookupResult != Found",
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.data.prescriptionLookupResult",
                                            "operator": "!=",
                                            "rightExpression": "'Found'",
                                        }
                                    ],
                                },
                                "stateName": "ConnectAgent",
                            },
                            "type": "transitionbyname",
                            "_selected": False,
                            "transitionId": "refId1733699110119",
                            "id": "refId1736293727074",
                            "icon": "icon-transition",
                        },
                        {
                            "name": "Save Variable",
                            "description": "",
                            "properties": {
                                "description": "nextMessage",
                                "rightExpression": "Please wait while I refill your prescription.",
                                "variableName": "nextMessage",
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
                            "id": "refId1736293727075",
                            "icon": "icon-save",
                        },
                        {
                            "name": "Chat Message Consumer",
                            "description": "",
                            "properties": {
                                "description": "Please wait... (English)",
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.type",
                                            "operator": "==",
                                            "rightExpression": "'Chat'",
                                        },
                                        {
                                            "leftExpression": "workitem.data.sourceLanguage",
                                            "operator": "==",
                                            "rightExpression": "'en'",
                                        },
                                    ],
                                },
                                "from": "${workitem.data.companyName}",
                                "message": "Please wait while I refill your prescription.",
                                "messageType": "BOT",
                                "options": [],
                            },
                            "type": "chatmessageconsumer",
                            "_selected": False,
                            "id": "refId1736293727076",
                            "icon": "icon-ai-message",
                        },
                        {
                            "name": "Execute REST Call",
                            "description": "",
                            "properties": {
                                "description": "Google Translation (Next Message to Source Language)",
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.type",
                                            "operator": "==",
                                            "rightExpression": "'Chat'",
                                        },
                                        {
                                            "leftExpression": "workitem.data.sourceLanguage",
                                            "operator": "!=",
                                            "rightExpression": "'en'",
                                        },
                                    ],
                                },
                                "responseVariable": "googletranslateresponse",
                                "restCallId": "67592dbd3bf7aa24c81986b0",
                                "expansions": {
                                    "restCallId": {
                                        "name": "Google Translation (Next Message to Source Language)"
                                    }
                                },
                                "_working": False,
                            },
                            "type": "restapi",
                            "_selected": False,
                            "id": "refId1736293727077",
                            "icon": "icon-api",
                        },
                        {
                            "name": "Chat Message Consumer",
                            "description": "",
                            "properties": {
                                "description": "Please wait... (Non-English)",
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.type",
                                            "operator": "==",
                                            "rightExpression": "'Chat'",
                                        },
                                        {
                                            "leftExpression": "workitem.data.sourceLanguage",
                                            "operator": "!=",
                                            "rightExpression": "'en'",
                                        },
                                    ],
                                },
                                "from": "${workitem.data.companyName}",
                                "message": "$V.workitem.data.googletranslateresponse.body.data.translations[0].translatedText",
                                "messageType": "BOT",
                                "options": [],
                            },
                            "type": "chatmessageconsumer",
                            "_selected": False,
                            "id": "refId1736293727078",
                            "icon": "icon-ai-message",
                        },
                        {
                            "name": "SMS Message Consumer",
                            "description": "",
                            "properties": {
                                "description": "Please wait...",
                                "message": "Please wait while I refill your prescription.",
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
                            "id": "refId1736293727079",
                            "icon": "icon-ai-message",
                        },
                        {
                            "name": "Synthesize Text via Google TTS",
                            "description": "Convert Text into Audio using Google's Text-To-Speech",
                            "properties": {
                                "description": "Please wait...",
                                "voiceName": "en-US-Wavenet-J",
                                "text": '<prosody pitch="-2st">Please wait while I refill your prescription.</prosody>',
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
                            "id": "refId1736293727080",
                            "icon": "icon-tts",
                        },
                        {
                            "name": "Execute REST Call",
                            "description": "",
                            "properties": {
                                "description": "Spinsci - Request Refills",
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "responseVariable": "requestRefillsResponse",
                                "restCallId": "673ef224186614179724fccc",
                                "expansions": {
                                    "restCallId": {"name": "Spinsci - Request Refills"}
                                },
                                "_working": False,
                            },
                            "type": "restapi",
                            "_selected": False,
                            "id": "refId1736293727081",
                            "icon": "icon-api",
                        },
                        {
                            "name": "Start Timer",
                            "description": "",
                            "properties": {
                                "timeoutInSeconds": "2",
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                            },
                            "type": "starttimer",
                            "_selected": False,
                            "id": "refId1736293727082",
                            "icon": "icon-timer",
                        },
                        {
                            "name": "Save Variable",
                            "description": "",
                            "properties": {
                                "description": "nextMessage",
                                "rightExpression": "Your prescription has been refilled. You have ${workitem.data.refillQty - 1} remaining refills. What else can I help you with today?",
                                "variableName": "nextMessage",
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
                            "id": "refId1736293727083",
                            "icon": "icon-save",
                        },
                        {
                            "name": "Chat Message Consumer",
                            "description": "",
                            "properties": {
                                "description": "Your prescription has been refilled. (English)",
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.type",
                                            "operator": "==",
                                            "rightExpression": "'Chat'",
                                        },
                                        {
                                            "leftExpression": "workitem.data.sourceLanguage",
                                            "operator": "==",
                                            "rightExpression": "'en'",
                                        },
                                    ],
                                },
                                "from": "${workitem.data.companyName}",
                                "message": "Your prescription has been refilled. You have ${workitem.data.refillQty - 1} remaining refills. What else can I help you with today?",
                                "messageType": "BOT",
                                "options": [
                                    {
                                        "label": "Reschedule Appointment",
                                        "value": "Reschedule Appointment",
                                    },
                                    {
                                        "label": "Cancel Appointment",
                                        "value": "Cancel Appointment",
                                    },
                                    {"label": "Get Location", "value": "Get Location"},
                                    {
                                        "label": "Find a Doctor",
                                        "value": "Find a Doctor",
                                    },
                                ],
                            },
                            "type": "chatmessageconsumer",
                            "_selected": False,
                            "id": "refId1736293727084",
                            "icon": "icon-ai-message",
                        },
                        {
                            "name": "Execute REST Call",
                            "description": "",
                            "properties": {
                                "description": "Google Translation (Next Message to Source Language)",
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.type",
                                            "operator": "==",
                                            "rightExpression": "'Chat'",
                                        },
                                        {
                                            "leftExpression": "workitem.data.sourceLanguage",
                                            "operator": "!=",
                                            "rightExpression": "'en'",
                                        },
                                    ],
                                },
                                "responseVariable": "googletranslateresponse",
                                "restCallId": "67592dbd3bf7aa24c81986b0",
                                "expansions": {
                                    "restCallId": {
                                        "name": "Google Translation (Next Message to Source Language)"
                                    }
                                },
                                "_working": False,
                            },
                            "type": "restapi",
                            "_selected": False,
                            "id": "refId1736293727085",
                            "icon": "icon-api",
                        },
                        {
                            "name": "Chat Message Consumer",
                            "description": "",
                            "properties": {
                                "description": "Your prescription has been refilled. (Non-English)",
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.type",
                                            "operator": "==",
                                            "rightExpression": "'Chat'",
                                        },
                                        {
                                            "leftExpression": "workitem.data.sourceLanguage",
                                            "operator": "!=",
                                            "rightExpression": "'en'",
                                        },
                                    ],
                                },
                                "from": "${workitem.data.companyName}",
                                "message": "$V.workitem.data.googletranslateresponse.body.data.translations[0].translatedText",
                                "messageType": "BOT",
                                "options": [],
                            },
                            "type": "chatmessageconsumer",
                            "_selected": False,
                            "id": "refId1736293727086",
                            "icon": "icon-ai-message",
                        },
                        {
                            "name": "SMS Message Consumer",
                            "description": "",
                            "properties": {
                                "description": "Your prescription has been refilled.",
                                "message": "Your prescription has been refilled. You have ${workitem.data.refillQty - 1} remaining refills. What else can I help you with today?",
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
                            "id": "refId1736293727087",
                            "icon": "icon-ai-message",
                        },
                        {
                            "name": "Synthesize Text via Google TTS",
                            "description": "Convert Text into Audio using Google's Text-To-Speech",
                            "properties": {
                                "description": "Your prescription has been refilled.",
                                "voiceName": "en-US-Wavenet-J",
                                "text": '<prosody pitch="-2st">Your prescription has been refilled, and you have ${workitem.data.refillQty - 1} remaining refills. Thank you for contacting us and have a great day!</prosody>',
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                            },
                            "type": "googletts",
                            "_selected": False,
                            "id": "refId1736293727088",
                            "icon": "icon-tts",
                        },
                        {
                            "name": "SMS Message Consumer",
                            "description": "",
                            "properties": {
                                "description": "workitem.type == 'InboundCall'",
                                "message": "Hi, this is ${workitem.data.companyName}! Your prescription has been refilled. You have ${workitem.data.refillQty - 1} remaining refills. Reply back with any questions!",
                                "toAddress": "workitem.from",
                                "fromAddress": "workitem.to",
                                "createNewWorkitem": False,
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
                            "type": "smsmessageconsumer",
                            "_selected": False,
                            "id": "refId1736293727089",
                            "icon": "icon-ai-message",
                        },
                        {
                            "name": "End State",
                            "description": "Transition to another state",
                            "properties": {
                                "description": "workitem.type == 'InboundCall'",
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
                                "stateName": "End State",
                            },
                            "type": "transitionbyname",
                            "_selected": False,
                            "transitionId": "refId1733699110361",
                            "id": "refId1736293727090",
                            "icon": "icon-transition",
                        },
                        {
                            "name": "SMS Message Consumer",
                            "description": "",
                            "properties": {
                                "description": "workitem.type == 'Chat'",
                                "message": "Hi, this is ${workitem.data.companyName}! Your prescription has been refilled. You have ${workitem.data.refillQty - 1} remaining refills. Reply back with any questions!",
                                "toAddress": "workitem.data.context.consumerData.phone",
                                "fromAddress": "'+14809192185'",
                                "createNewWorkitem": False,
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
                            "type": "smsmessageconsumer",
                            "_selected": True,
                            "id": "refId1736293727091",
                            "icon": "icon-ai-message",
                        },
                        {
                            "name": "Webhook",
                            "description": "Transition to another state",
                            "properties": {
                                "description": "Webhook",
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "stateName": "Webhook",
                            },
                            "type": "transitionbyname",
                            "_selected": False,
                            "transitionId": "refId1733592655560",
                            "id": "refId1736293727092",
                            "icon": "icon-transition",
                        },
                    ],
                    "_id": "6754d9c04898b3bca10e5363",
                    "key": "6754d9c04898b3bca10e5363",
                    "location": "1764.223567332189 -274.6610381074282",
                    "transitions": [
                        {"name": "Verify", "id": "refId1733592656036"},
                        {"name": "ConnectAgent", "id": "refId1733699110119"},
                        {"name": "End State", "id": "refId1733699110361"},
                        {"name": "Webhook", "id": "refId1733592655560"},
                    ],
                },
                "6754da1a398b8d68d2fcaf8a": {
                    "category": "Standard",
                    "objectType": "campaignstate",
                    "campaignStateId": "6754da1a398b8d68d2fcaf8a",
                    "name": "Chat",
                    "description": "Newly Created State",
                    "tenantId": "nextivase19",
                    "actions": [
                        {
                            "icon": "icon-transition",
                            "name": "Webhook",
                            "description": "Transition to another state",
                            "properties": {
                                "description": "Webhook",
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "stateId": "67549fef8c3694beb965b21c",
                            },
                            "type": "transition",
                            "_selected": True,
                            "transitionId": "refId1733592655624",
                        }
                    ],
                    "_id": "6754da1a398b8d68d2fcaf8a",
                    "key": "6754da1a398b8d68d2fcaf8a",
                    "location": "351.85810891596213 -210.7054961374019",
                    "transitions": [{"name": "Webhook", "id": "refId1733592655624"}],
                },
                "6754da97b4f471f89ec7228e": {
                    "category": "Standard",
                    "objectType": "campaignstate",
                    "campaignStateId": "6754da97b4f471f89ec7228e",
                    "name": "InboundSMS",
                    "description": "Newly Created State",
                    "tenantId": "nextivase19",
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
                            "_selected": True,
                        },
                        {
                            "name": "Webhook",
                            "description": "Transition to another state",
                            "properties": {
                                "description": "Webhook",
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "stateId": "67549fef8c3694beb965b21c",
                            },
                            "type": "transition",
                            "_selected": False,
                            "transitionId": "refId1733592655637",
                            "icon": "icon-transition",
                            "id": "refId1733935253678",
                        },
                    ],
                    "_id": "6754da97b4f471f89ec7228e",
                    "key": "6754da97b4f471f89ec7228e",
                    "location": "349.90335666480416 -28.133357944239435",
                    "transitions": [{"name": "Webhook", "id": "refId1733592655637"}],
                },
                "6754e45df91eebd4e98c05f3": {
                    "category": "Standard",
                    "objectType": "campaignstate",
                    "campaignStateId": "6754e45df91eebd4e98c05f3",
                    "name": "Verify",
                    "description": "Newly Created State",
                    "tenantId": "nextivase19",
                    "actions": [
                        {
                            "name": "Execute Function",
                            "description": "",
                            "properties": {
                                "description": "SpinSci - Verify Patient (with translation)",
                                "functionId": "67593b84c3e1f25ae7bb55e6",
                                "functionExpression": "",
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "expansions": {
                                    "functionId": {
                                        "name": "SpinSci - Verify Patient (with translation)"
                                    }
                                },
                                "_working": False,
                            },
                            "type": "function",
                            "_selected": True,
                            "id": "refId1733873039929",
                            "icon": "icon-function",
                        },
                        {
                            "name": "End State",
                            "description": "Transition to another state",
                            "properties": {
                                "description": "End State",
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.data.verified",
                                            "operator": "==",
                                            "rightExpression": "'timeout'",
                                        }
                                    ],
                                },
                                "stateName": "End State",
                            },
                            "type": "transitionbyname",
                            "_selected": False,
                            "transitionId": "refId1733681592463",
                            "icon": "icon-transition",
                            "id": "refId1733873039930",
                        },
                        {
                            "name": "workitem.data.action",
                            "description": "Transition to another state",
                            "properties": {
                                "description": "workitem.data.action",
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "operator": "==",
                                            "leftExpression": "workitem.data.verified",
                                            "rightExpression": "true",
                                        }
                                    ],
                                },
                                "stateName": "workitem.data.action",
                            },
                            "type": "transitionbyname",
                            "_selected": False,
                            "transitionId": "refId1733592655950",
                            "id": "refId1733873039931",
                            "icon": "icon-transition",
                        },
                        {
                            "name": "ConnectAgent",
                            "description": "Transition to another state",
                            "properties": {
                                "description": "ConnectAgent",
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "stateName": "ConnectAgent",
                            },
                            "type": "transitionbyname",
                            "_selected": False,
                            "transitionId": "refId1733681591776",
                            "id": "refId1733873039932",
                            "icon": "icon-transition",
                        },
                    ],
                    "_id": "6754e45df91eebd4e98c05f3",
                    "key": "6754e45df91eebd4e98c05f3",
                    "location": "1938.3633977706813 76.18977094170623",
                    "transitions": [
                        {"name": "End State", "id": "refId1733681592463"},
                        {"name": "workitem.data.action", "id": "refId1733592655950"},
                        {"name": "ConnectAgent", "id": "refId1733681591776"},
                    ],
                },
                "6754e4bc03f97c8d984c4508": {
                    "category": "Standard",
                    "objectType": "campaignstate",
                    "campaignStateId": "6754e4bc03f97c8d984c4508",
                    "name": "PayBill",
                    "description": "Newly Created State",
                    "tenantId": "nextivase19",
                    "actions": [
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
                                },
                                "description": "workitem.type == 'InboundCall'",
                            },
                            "type": "dialogflowtakeback",
                            "_selected": False,
                            "id": "refId1736293727117",
                            "icon": "icon-dialogflow",
                        },
                        {
                            "name": "Save Variable",
                            "description": "",
                            "properties": {
                                "description": "action",
                                "rightExpression": "PayBill",
                                "variableName": "action",
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
                            "id": "refId1736293727118",
                            "icon": "icon-save",
                        },
                        {
                            "name": "Save Variable",
                            "description": "",
                            "properties": {
                                "description": "actionPhrase",
                                "rightExpression": "pay your bill",
                                "variableName": "actionPhrase",
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
                            "id": "refId1736293727119",
                            "icon": "icon-save",
                        },
                        {
                            "name": "Verify",
                            "description": "Transition to another state",
                            "properties": {
                                "description": "Verify",
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.data.verified",
                                            "operator": "==",
                                            "rightExpression": "false",
                                        }
                                    ],
                                },
                                "stateName": "Verify",
                            },
                            "type": "transitionbyname",
                            "_selected": False,
                            "transitionId": "refId1733592656049",
                            "id": "refId1736293727120",
                            "icon": "icon-transition",
                        },
                        {
                            "name": "Execute REST Call",
                            "description": "",
                            "properties": {
                                "description": "Spinsci - getpatientbillingdetails",
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "responseVariable": "patientBillingResponse",
                                "restCallId": "675331d7c3e1f25ae7bb4ead",
                                "expansions": {
                                    "restCallId": {
                                        "name": "Spinsci - getpatientbillingdetails"
                                    }
                                },
                                "_working": False,
                            },
                            "type": "restapi",
                            "_selected": False,
                            "id": "refId1736293727121",
                            "icon": "icon-api",
                        },
                        {
                            "name": "Save Variable",
                            "description": "",
                            "properties": {
                                "description": "ccAmount",
                                "rightExpression": "6346",
                                "variableName": "ccAmount",
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
                            "id": "refId1736293727122",
                            "icon": "icon-save",
                        },
                        {
                            "name": "ConnectAgent",
                            "description": "Transition to another state",
                            "properties": {
                                "description": "Chat or InboundSMS",
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
                                "stateName": "ConnectAgent",
                            },
                            "type": "transitionbyname",
                            "_selected": False,
                            "transitionId": "refId1733699102643",
                            "id": "refId1736293727123",
                            "icon": "icon-transition",
                        },
                        {
                            "name": "Execute Function",
                            "description": "",
                            "properties": {
                                "description": "SPAA - Payment Gateway (IVA)",
                                "functionId": "6753325ce3c06e3d040ca008",
                                "functionExpression": "",
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
                                    "functionId": {
                                        "name": "SPAA - Payment Gateway (IVA)"
                                    }
                                },
                                "_working": False,
                            },
                            "type": "function",
                            "_selected": False,
                            "id": "refId1736293727124",
                            "icon": "icon-function",
                        },
                        {
                            "name": "SMS Message Consumer",
                            "description": "",
                            "properties": {
                                "description": "workitem.type == 'InboundCall'",
                                "message": "Hi, this is ${workitem.data.companyName}! Your payment of $${workitem.data.ccAmount} has been processed. Reply back with any questions.",
                                "toAddress": "workitem.from",
                                "fromAddress": "workitem.to",
                                "createNewWorkitem": False,
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
                            "type": "smsmessageconsumer",
                            "_selected": True,
                            "id": "refId1736293727125",
                            "icon": "icon-ai-message",
                        },
                        {
                            "name": "End State",
                            "description": "Transition to another state",
                            "properties": {
                                "description": "End State",
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "stateName": "End State",
                            },
                            "type": "transitionbyname",
                            "_selected": False,
                            "transitionId": "refId1733592655923",
                            "id": "refId1736293727126",
                            "icon": "icon-transition",
                        },
                    ],
                    "_id": "6754e4bc03f97c8d984c4508",
                    "key": "6754e4bc03f97c8d984c4508",
                    "location": "1994.600291230676 -297.5828329134683",
                    "transitions": [
                        {"name": "Verify", "id": "refId1733592656049"},
                        {"name": "ConnectAgent", "id": "refId1733699102643"},
                        {"name": "End State", "id": "refId1733592655923"},
                    ],
                },
                "67562198a361ef475749dd55": {
                    "category": "Standard",
                    "objectType": "campaignstate",
                    "campaignStateId": "67562198a361ef475749dd55",
                    "name": "API Failure",
                    "description": "Newly Created State",
                    "tenantId": "nextivase19",
                    "actions": [
                        {
                            "name": "Save Variable",
                            "description": "",
                            "properties": {
                                "description": "nextMessage",
                                "rightExpression": "Sorry, but I'm unable to help you ${workitem.data.actionPhrase} at this time",
                                "variableName": "nextMessage",
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
                            "id": "refId1736293726766",
                        },
                        {
                            "name": "Chat Message Consumer",
                            "description": "",
                            "properties": {
                                "description": "Sorry... (English)",
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.type",
                                            "operator": "==",
                                            "rightExpression": "'Chat'",
                                        },
                                        {
                                            "leftExpression": "workitem.data.sourceLanguage",
                                            "operator": "==",
                                            "rightExpression": "'en'",
                                        },
                                    ],
                                },
                                "from": "${workitem.data.companyName}",
                                "message": "Sorry, but I'm unable to help you ${workitem.data.actionPhrase} at this time",
                                "messageType": "BOT",
                                "options": [],
                            },
                            "type": "chatmessageconsumer",
                            "_selected": False,
                            "id": "refId1736293726767",
                            "icon": "icon-ai-message",
                        },
                        {
                            "name": "Execute REST Call",
                            "description": "",
                            "properties": {
                                "description": "Google Translation (Next Message to Source Language)",
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.type",
                                            "operator": "==",
                                            "rightExpression": "'Chat'",
                                        },
                                        {
                                            "leftExpression": "workitem.data.sourceLanguage",
                                            "operator": "!=",
                                            "rightExpression": "'en'",
                                        },
                                    ],
                                },
                                "responseVariable": "googletranslateresponse",
                                "restCallId": "67592dbd3bf7aa24c81986b0",
                                "expansions": {
                                    "restCallId": {
                                        "name": "Google Translation (Next Message to Source Language)"
                                    }
                                },
                                "_working": False,
                            },
                            "type": "restapi",
                            "_selected": False,
                            "id": "refId1736293726768",
                            "icon": "icon-api",
                        },
                        {
                            "name": "Chat Message Consumer",
                            "description": "",
                            "properties": {
                                "description": "Sorry... (Non-English)",
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.type",
                                            "operator": "==",
                                            "rightExpression": "'Chat'",
                                        },
                                        {
                                            "leftExpression": "workitem.data.sourceLanguage",
                                            "operator": "!=",
                                            "rightExpression": "'en'",
                                        },
                                    ],
                                },
                                "from": "${workitem.data.companyName}",
                                "message": "$V.workitem.data.googletranslateresponse.body.data.translations[0].translatedText",
                                "messageType": "BOT",
                                "options": [],
                            },
                            "type": "chatmessageconsumer",
                            "_selected": False,
                            "id": "refId1736293726769",
                            "icon": "icon-ai-message",
                        },
                        {
                            "name": "SMS Message Consumer",
                            "description": "",
                            "properties": {
                                "description": "workitem.type == 'InboundSMS'",
                                "message": "Sorry, but I'm unable to help you ${workitem.data.actionPhrase} at this time",
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
                            "_selected": True,
                            "id": "refId1736293726770",
                            "icon": "icon-ai-message",
                        },
                        {
                            "name": "Synthesize Text via Google TTS",
                            "description": "Convert Text into Audio using Google's Text-To-Speech",
                            "properties": {
                                "description": "Sorry...",
                                "voiceName": "en-US-Standard-J",
                                "text": '<prosody pitch="-2st">Sorry, but I\'m unable to help you ${workitem.data.actionPhrase} at this time.</prosody>',
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                            },
                            "type": "googletts",
                            "_selected": False,
                            "id": "refId1736293726771",
                            "icon": "icon-tts",
                        },
                        {
                            "name": "ConnectAgent",
                            "description": "Transition to another state",
                            "properties": {
                                "description": "ConnectAgent",
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "stateName": "ConnectAgent",
                            },
                            "type": "transitionbyname",
                            "_selected": False,
                            "transitionId": "refId1733681595668",
                            "id": "refId1736293726772",
                            "icon": "icon-transition",
                        },
                    ],
                    "_id": "67562198a361ef475749dd55",
                    "key": "67562198a361ef475749dd55",
                    "location": "2168.483284879579 30.484444816956113",
                    "transitions": [
                        {"name": "ConnectAgent", "id": "refId1733681595668"}
                    ],
                },
                "6756793d70c5b89c819837d4": {
                    "category": "Standard",
                    "objectType": "campaignstate",
                    "campaignStateId": "6756793d70c5b89c819837d4",
                    "name": "Goodbye",
                    "description": "Newly Created State",
                    "tenantId": "nextivase19",
                    "actions": [
                        {
                            "name": "Retrieve the call",
                            "description": "",
                            "properties": {
                                "description": "workitem.type == 'InboundCall'",
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
                            "type": "dialogflowtakeback",
                            "_selected": False,
                            "id": "refId1733873035995",
                            "icon": "icon-dialogflow",
                        },
                        {
                            "name": "Chat Message Consumer",
                            "description": "",
                            "properties": {
                                "description": "Thank you... (English)",
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.type",
                                            "operator": "==",
                                            "rightExpression": "'Chat'",
                                        },
                                        {
                                            "leftExpression": "workitem.data.sourceLanguage",
                                            "operator": "==",
                                            "rightExpression": "'en'",
                                        },
                                    ],
                                },
                                "from": "${workitem.data.companyName}",
                                "message": "Thank you for contacting us and have a great day!",
                                "messageType": "BOT",
                                "options": [],
                            },
                            "type": "chatmessageconsumer",
                            "_selected": False,
                            "id": "refId1733873035996",
                            "icon": "icon-ai-message",
                        },
                        {
                            "icon": "icon-api",
                            "name": "Execute REST Call",
                            "description": "",
                            "properties": {
                                "description": "Google Translation (Chatbot to Source Language)",
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.type",
                                            "operator": "==",
                                            "rightExpression": "'Chat'",
                                        },
                                        {
                                            "leftExpression": "workitem.data.sourceLanguage",
                                            "operator": "!=",
                                            "rightExpression": "'en'",
                                        },
                                    ],
                                },
                                "responseVariable": "googletranslateresponse",
                                "restCallId": "6759159ccb6cdb0056107af8",
                                "expansions": {
                                    "restCallId": {
                                        "name": "Google Translation (Chatbot to Source Language)"
                                    }
                                },
                                "_working": False,
                            },
                            "type": "restapi",
                            "_selected": False,
                        },
                        {
                            "icon": "icon-ai-message",
                            "name": "Chat Message Consumer",
                            "description": "",
                            "properties": {
                                "description": "Thank you... (Non-English)",
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.type",
                                            "operator": "==",
                                            "rightExpression": "'Chat'",
                                        },
                                        {
                                            "leftExpression": "workitem.data.sourceLanguage",
                                            "operator": "!=",
                                            "rightExpression": "'en'",
                                        },
                                    ],
                                },
                                "from": "${workitem.data.companyName}",
                                "message": "$V.workitem.data.googletranslateresponse.body.data.translations[0].translatedText",
                                "messageType": "BOT",
                                "options": [],
                            },
                            "type": "chatmessageconsumer",
                            "_selected": False,
                        },
                        {
                            "name": "SMS Message Consumer",
                            "description": "",
                            "properties": {
                                "description": "Thank you...",
                                "message": "Thank you for contacting us and have a great day!",
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
                            "id": "refId1733873035997",
                            "icon": "icon-ai-message",
                        },
                        {
                            "name": "Synthesize Text via Google TTS",
                            "description": "Convert Text into Audio using Google's Text-To-Speech",
                            "properties": {
                                "description": "Thank you...",
                                "voiceName": "en-US-Wavenet-J",
                                "text": '<prosody pitch="-2st">Thank you for contacting us and have a great day!</prosody>',
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
                            "id": "refId1733873035998",
                            "icon": "icon-tts",
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
                                            "operator": "==",
                                            "leftExpression": "workitem.type",
                                            "rightExpression": "'Chat'",
                                        }
                                    ],
                                },
                            },
                            "type": "starttimer",
                            "_selected": True,
                            "id": "refId1733873035999",
                            "icon": "icon-timer",
                        },
                        {
                            "name": "End State",
                            "description": "Transition to another state",
                            "properties": {
                                "description": "End State",
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "stateName": "End State",
                            },
                            "type": "transitionbyname",
                            "_selected": False,
                            "transitionId": "refId1733699107266",
                            "id": "refId1733873036000",
                            "icon": "icon-transition",
                        },
                    ],
                    "_id": "6756793d70c5b89c819837d4",
                    "key": "6756793d70c5b89c819837d4",
                    "location": "343.3303703091898 496.4486004786945",
                    "transitions": [{"name": "End State", "id": "refId1733699107266"}],
                },
                "675900b6e58af826dec55828": {
                    "category": "Standard",
                    "objectType": "campaignstate",
                    "campaignStateId": "675900b6e58af826dec55828",
                    "name": "Survey",
                    "description": "Newly Created State",
                    "tenantId": "nextivase19",
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
                            "_selected": True,
                        },
                        {
                            "icon": "icon-transition",
                            "name": "End State",
                            "description": "Transition to another state",
                            "properties": {
                                "description": "End State",
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "stateName": "End State",
                            },
                            "type": "transitionbyname",
                            "_selected": False,
                            "transitionId": "refId1733873034596",
                        },
                    ],
                    "_id": "675900b6e58af826dec55828",
                    "key": "675900b6e58af826dec55828",
                    "location": "349.7475715937059 -377.6856510603927",
                    "transitions": [{"name": "End State", "id": "refId1733873034596"}],
                },
            },
            "finalWorkitemStateId": "67548667ca85e7eb0bed9d1d",
            "finalUserStateId": "67548667ca85e7eb0bed9d1d",
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
