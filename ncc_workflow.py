import http.client
import urllib.parse
import json


def search_workflows(ncc_location: str, ncc_token: str, workflow_name: str) -> str:
    """
    This function searches for an existing workflow with the same name as the intended new workflow.
    """
    workflow_id = ""
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
                    workflow_id = result["workflowId"]
                    break
    conn.close()
    return workflow_id


def create_workflow(ncc_location: str, ncc_token: str, workflow_name: str) -> str:
    workflow_id = ""
    conn = http.client.HTTPSConnection(ncc_location)
    payload = json.dumps(
        {
            "maxActions": 10000,
            "localizations": {
                "name": {"en": {"language": "en", "value": workflow_name}}
            },
            "description": "",
            "states": {
                "67548667ca85e7eb0bed9d1d": {
                    "category": "Standard",
                    "campaignStateId": "67548667ca85e7eb0bed9d1d",
                    "actions": [
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
                            "id": "refId1736300392801",
                            "icon": "icon-terminate",
                        }
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
                            "id": "refId1736300392506",
                            "icon": "icon-save",
                        },
                        {
                            "name": "Save Variable",
                            "description": "",
                            "properties": {
                                "description": "companyName",
                                "rightExpression": "NEXT Healthcare",
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
                            "_selected": True,
                            "id": "refId1736300392507",
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
                            "id": "refId1736300392509",
                            "icon": "icon-save",
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
                            "id": "refId1736300392512",
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
                            "id": "refId1736300392513",
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
                            "id": "refId1736300392514",
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
                            "id": "refId1736300392515",
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
                            "id": "refId1736300392516",
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
                            "name": "Synthesize Text via Google TTS",
                            "description": "Convert Text into Audio using Google's Text-To-Speech",
                            "properties": {
                                "description": "Thank you for calling.",
                                "voiceName": "en-US-Wavenet-J",
                                "text": '<prosody pitch="-2st">Thank you for calling.</prosody>',
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                            },
                            "type": "googletts",
                            "_selected": True,
                            "icon": "icon-tts",
                            "id": "refId1736300392926",
                        },
                        {
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
                            "_selected": False,
                            "id": "refId1736300392927",
                            "icon": "icon-dialogflow",
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
                                "points": {
                                    "h": True,
                                    "r": [],
                                    "ct": 0,
                                    "__gohashid": 16355,
                                },
                            },
                            "type": "transition",
                            "_selected": False,
                            "transitionId": "refId1733592654663",
                            "id": "refId1736300392928",
                            "icon": "icon-transition",
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
                            "id": "refId1736300392661",
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
                            "id": "refId1736300392662",
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
                            "id": "refId1736300392663",
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
                            "id": "refId1736300392664",
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
                            "id": "refId1736300392665",
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
                            "id": "refId1736300392666",
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
                            "id": "refId1736300392667",
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
                            "id": "refId1736300392668",
                            "icon": "icon-script",
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
                            "_selected": True,
                            "id": "refId1736300392671",
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
                            "id": "refId1736300392672",
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
                            "id": "refId1736300392673",
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
                                    "r": [
                                        {
                                            "b": 1374.8858968900809,
                                            "k": 155.3913058844948,
                                            "h": True,
                                        },
                                        {
                                            "b": 1384.8858968900809,
                                            "k": 155.3913058844948,
                                            "h": True,
                                        },
                                        {"b": 1388, "k": 155.3913058844948, "h": True},
                                        {"b": 1388, "k": 155.3913058844948, "h": True},
                                        {
                                            "b": 1591.6195351472147,
                                            "k": 155.3913058844948,
                                            "h": True,
                                        },
                                        {
                                            "b": 1591.6195351472147,
                                            "k": 196.7710523597631,
                                            "h": True,
                                        },
                                        {
                                            "b": 1591.6195351472147,
                                            "k": 206.7710523597631,
                                            "h": True,
                                        },
                                    ],
                                    "ct": 7,
                                    "__gohashid": 4587,
                                },
                            },
                            "type": "transition",
                            "_selected": False,
                            "transitionId": "refId1733592655314",
                            "id": "refId1736300392674",
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
                                "description": "Demo - Music - 60",
                                "loop": 1,
                                "numberDigits": 1,
                                "promptId": "641c589f9535e44e4b8b0c4d",
                                "terminationKey": "#",
                                "timeoutInSeconds": "1",
                                "dlpOption": False,
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "expansions": {
                                    "promptId": {"name": "Demo - Music - 60"}
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
                                "functionId": "62f5f778a4a0a35b07873919",
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
                                "expansions": {"functionId": {"name": "ACD Voicemail"}},
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
                                "functionId": "62f5f778a4a0a35b078738ff",
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
                                "expansions": {"functionId": {"name": "ACD Callback"}},
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
                                "description": "Demo - Music - 60",
                                "loop": 1,
                                "numberDigits": 1,
                                "promptId": "641c589f9535e44e4b8b0c4d",
                                "terminationKey": "#",
                                "timeoutInSeconds": "1",
                                "dlpOption": False,
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "expansions": {
                                    "promptId": {"name": "Demo - Music - 60"}
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
                                "functionId": "62f5f778a4a0a35b07873919",
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
                                "expansions": {"functionId": {"name": "ACD Voicemail"}},
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
                                "functionId": "62f5f778a4a0a35b078738ff",
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
                                "expansions": {"functionId": {"name": "ACD Callback"}},
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
                "6754da1a398b8d68d2fcaf8a": {
                    "category": "Standard",
                    "objectType": "campaignstate",
                    "campaignStateId": "6754da1a398b8d68d2fcaf8a",
                    "name": "Chat",
                    "description": "Newly Created State",
                    "tenantId": "nextivase19",
                    "actions": [
                        {
                            "icon": "icon-ai-message",
                            "name": "Chat Message Consumer",
                            "description": "",
                            "properties": {
                                "description": "How can I help you today?",
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "from": "${workitem.data.companyName}",
                                "message": "How can I help you today?",
                                "messageType": "BOT",
                                "options": [],
                            },
                            "type": "chatmessageconsumer",
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
                                "points": {
                                    "h": True,
                                    "r": [],
                                    "ct": 0,
                                    "__gohashid": 9878,
                                },
                            },
                            "type": "transition",
                            "_selected": False,
                            "transitionId": "refId1733592655624",
                            "icon": "icon-transition",
                            "id": "refId1736300392869",
                        },
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
    conn.request("POST", "/data/api/types/workflow/", payload, headers)
    res = conn.getresponse()
    if res.status == 201:
        data = res.read().decode("utf-8")
        json_data = json.loads(data)
        workflow_id = json_data["workflowId"]
    return workflow_id

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