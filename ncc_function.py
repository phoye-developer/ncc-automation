import http.client
import urllib.parse
import json
from config import *


def search_functions(ncc_location: str, ncc_token: str, function_name: str) -> dict:
    """
    This function searches for an existing Nextiva Contact Center (NCC) function with the specified name.
    """
    function = {}
    conn = http.client.HTTPSConnection(ncc_location)
    payload = ""
    headers = {"Authorization": ncc_token}
    url_encoded_name = urllib.parse.quote(function_name)
    try:
        conn.request(
            "GET",
            f"/data/api/types/function?q={url_encoded_name}",
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
                    if result["name"] == function_name:
                        function = result
                        break
    except:
        pass
    conn.close()
    return function


def search_campaign_functions(
    ncc_location: str, ncc_token: str, campaign_name: str
) -> dict:
    """
    This function searches for existing Nextiva Contact Center (NCC) functions that begin with the name of an NCC campaign.
    """
    functions = []
    conn = http.client.HTTPSConnection(ncc_location)
    payload = ""
    headers = {"Authorization": ncc_token}
    url_encoded_name = urllib.parse.quote(campaign_name)
    try:
        conn.request(
            "GET",
            f"/data/api/types/function?q={url_encoded_name}",
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
                    if str(result["name"]).startswith(campaign_name):
                        functions.append(result)
    except:
        pass
    conn.close()
    return functions


def create_function(ncc_location: str, ncc_token: str, function_body: dict) -> dict:
    """
    This function creates an NCC function.
    """
    function = {}
    conn = http.client.HTTPSConnection(ncc_location)
    payload = json.dumps(function_body)
    headers = {
        "Authorization": ncc_token,
        "Content-Type": "application/json",
    }
    try:
        conn.request("POST", "/data/api/types/function/", payload, headers)
        res = conn.getresponse()
        if res.status == 201:
            data = res.read().decode("utf-8")
            function = json.loads(data)
    except:
        pass
    conn.close()
    return function


def create_search_contacts_function(
    ncc_location: str, ncc_token: str, function_name: str
) -> dict:
    """
    This function creates an NCC function.
    """
    function = {}
    conn = http.client.HTTPSConnection(ncc_location)
    payload = json.dumps(
        {
            "states": {
                "67b1198ffbec07080c5ed4f5": {
                    "category": "Standard",
                    "campaignStateId": "67b1198ffbec07080c5ed4f5",
                    "actions": [
                        {
                            "icon": "icon-functionreturn",
                            "name": "Return To Workflow",
                            "description": "",
                            "properties": {
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                }
                            },
                            "type": "functionreturn",
                            "_selected": True,
                        }
                    ],
                    "objectType": "campaignstate",
                    "key": "67b1198ffbec07080c5ed4f5",
                    "_id": "67b1198ffbec07080c5ed4f5",
                    "description": "End State",
                    "name": "End State",
                    "location": "-29.15635454687515 171.02506895312501",
                    "transitions": [],
                },
                "start-state": {
                    "category": "Begin",
                    "campaignStateId": "start-state",
                    "actions": [
                        {
                            "name": "Search Contacts",
                            "type": "transition",
                            "description": "Transition to another state",
                            "properties": {
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "stateId": "67b119c1c1ef27217175e22a",
                                "name": "Start",
                                "description": "Transition to another state",
                            },
                            "transitionId": "67b119ac7b83858bc8773ee8",
                            "_selected": True,
                            "icon": "icon-transition",
                            "id": "refId1739600226597",
                        }
                    ],
                    "transitions": [
                        {"name": "Search Contacts", "id": "67b119ac7b83858bc8773ee8"}
                    ],
                    "objectType": "campaignstate",
                    "key": "start-state",
                    "_id": "start-state",
                    "description": "Begin State",
                    "name": "Begin State",
                    "location": "0 0",
                },
                "67b119c1c1ef27217175e22a": {
                    "category": "Standard",
                    "objectType": "campaignstate",
                    "campaignStateId": "67b119c1c1ef27217175e22a",
                    "name": "Search Contacts",
                    "description": "Newly Created State",
                    "tenantId": "nextivaretaildemo",
                    "actions": [
                        {
                            "icon": "icon-search",
                            "name": "Contact",
                            "description": "Assign contact",
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
                                "searchOn": "workitem.data.context.consumerData.phone",
                            },
                            "type": "findcontact",
                            "_selected": False,
                            "id": "refId1739600226656",
                        },
                        {
                            "icon": "icon-search",
                            "name": "Contact",
                            "description": "Assign contact",
                            "properties": {
                                "description": "InboundCall, OutboundCall, InboundSMS, OutboundSMS",
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
                                            "rightExpression": "'OutboundCall'",
                                        },
                                        {
                                            "leftExpression": "workitem.type",
                                            "operator": "==",
                                            "rightExpression": "'InboundSMS'",
                                        },
                                        {
                                            "leftExpression": "workitem.type",
                                            "operator": "==",
                                            "rightExpression": "'OutboundSMS'",
                                        },
                                    ],
                                },
                                "searchOn": "workitem.data.phone",
                            },
                            "type": "findcontact",
                            "_selected": False,
                        },
                        {
                            "icon": "icon-search",
                            "name": "Contact",
                            "description": "Assign contact",
                            "properties": {
                                "description": "Email",
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
                                "searchOn": "workitem.from",
                            },
                            "type": "findcontact",
                            "_selected": True,
                        },
                        {
                            "name": "End State",
                            "description": "Transition to another state",
                            "properties": {
                                "description": "Transition to another state",
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "stateName": "End State",
                            },
                            "type": "transitionbyname",
                            "_selected": False,
                            "transitionId": "refId1739600226625",
                            "icon": "icon-transition",
                            "id": "refId1739600226627",
                        },
                    ],
                    "_id": "67b119c1c1ef27217175e22a",
                    "key": "67b119c1c1ef27217175e22a",
                    "location": "318.1850467343752 131.52630117187525",
                    "transitions": [{"name": "End State", "id": "refId1739600226625"}],
                },
            },
            "showInDashboardOption": False,
            "name": function_name,
        }
    )
    headers = {
        "Authorization": ncc_token,
        "Content-Type": "application/json",
    }
    try:
        conn.request("POST", "/data/api/types/function/", payload, headers)
        res = conn.getresponse()
        if res.status == 201:
            data = res.read().decode("utf-8")
            function = json.loads(data)
    except:
        pass
    conn.close()
    return function


def create_two_way_chat_function(
    ncc_location: str, ncc_token: str, function_name: str
) -> dict:
    """
    This function creates an NCC function.
    """
    function = {}
    conn = http.client.HTTPSConnection(ncc_location)
    payload = json.dumps(
        {
            "name": function_name,
            "states": {
                "612ff2f1d02eea7fc5cb265d": {
                    "category": "Standard",
                    "campaignStateId": "612ff2f1d02eea7fc5cb265d",
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
                    "key": "612ff2f1d02eea7fc5cb265d",
                    "_id": "612ff2f1d02eea7fc5cb265d",
                    "description": "End State",
                    "name": "End State",
                    "location": "-700.5483343194139 -371.32855479249986",
                    "transitions": [],
                    "__gohashid": 66405,
                },
                "start-state": {
                    "category": "Begin",
                    "campaignStateId": "start-state",
                    "actions": [
                        {
                            "name": "Wait for Messages",
                            "description": "Transition to another state",
                            "properties": {
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "stateId": "62b08f28e945230cb5347c5b",
                                "description": "Transition to another state",
                            },
                            "type": "transition",
                            "_selected": True,
                            "transitionId": "refId1630518553842",
                            "id": "refId1740431837692",
                            "icon": "icon-transition",
                        }
                    ],
                    "transitions": [
                        {"name": "Wait for Messages", "id": "refId1630518553842"}
                    ],
                    "objectType": "campaignstate",
                    "key": "start-state",
                    "_id": "start-state",
                    "description": "Begin State",
                    "name": "Begin",
                    "location": "-624.6666564941406 -568.0834203806282",
                    "__gohashid": 66406,
                },
                "612ff3bd59517fb2d65d306b": {
                    "category": "Standard",
                    "objectType": "campaignstate",
                    "campaignStateId": "612ff3bd59517fb2d65d306b",
                    "name": "Process Agent Messages",
                    "description": "Newly Created State",
                    "actions": [
                        {
                            "name": "Save Variable",
                            "description": "",
                            "properties": {
                                "description": "agentMessage",
                                "rightExpression": "workitem.currentChatMessage.textMsg",
                                "variableName": "agentMessage",
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
                            "id": "refId1740431839697",
                            "icon": "icon-save",
                        },
                        {
                            "name": "Translate Agent Messages",
                            "description": "Transition to another state",
                            "properties": {
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.data.sourceLanguage",
                                            "operator": "!=",
                                            "rightExpression": "'en'",
                                        }
                                    ],
                                },
                                "stateId": "67bd425db5bd6e43dbb27755",
                                "points": {
                                    "h": True,
                                    "r": [
                                        {
                                            "b": 536.8383321204963,
                                            "k": -199.32900284537422,
                                            "h": True,
                                        },
                                        {
                                            "b": 546.8383321204963,
                                            "k": -199.32900284537422,
                                            "h": True,
                                        },
                                        {"b": 548, "k": -199.32900284537422, "h": True},
                                        {"b": 548, "k": -199.32900284537422, "h": True},
                                        {
                                            "b": 795.2173121092856,
                                            "k": -199.32900284537422,
                                            "h": True,
                                        },
                                        {
                                            "b": 795.2173121092856,
                                            "k": -128.74992993911124,
                                            "h": True,
                                        },
                                        {
                                            "b": 795.2173121092856,
                                            "k": -118.74992993911124,
                                            "h": True,
                                        },
                                    ],
                                    "ct": 7,
                                    "__gohashid": 110661,
                                },
                                "description": "Transition to another state",
                            },
                            "type": "transition",
                            "_selected": False,
                            "transitionId": "67bd42d06ea2228d92ca88f1",
                            "id": "refId1740431839698",
                            "icon": "icon-transition",
                        },
                        {
                            "name": "Chat Message Consumer",
                            "description": "",
                            "properties": {
                                "description": "workitem.data.sourceLanguage == 'en'",
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.data.sourceLanguage",
                                            "operator": "==",
                                            "rightExpression": "'en'",
                                        }
                                    ],
                                },
                                "from": "workitem.data.companyName",
                                "message": "workitem.data.agentMessage",
                                "messageType": "BOT",
                                "options": [],
                            },
                            "type": "chatmessageconsumer",
                            "_selected": True,
                            "id": "refId1740431839699",
                            "icon": "icon-ai-message",
                        },
                        {
                            "name": "Wait for Messages",
                            "description": "Transition to another state",
                            "properties": {
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "stateName": "Wait for Messages",
                                "description": "Transition to another state",
                            },
                            "type": "transitionbyname",
                            "_selected": False,
                            "transitionId": "refId1740431837801",
                            "id": "refId1740431839700",
                            "icon": "icon-transition",
                        },
                    ],
                    "_id": "612ff3bd59517fb2d65d306b",
                    "key": "612ff3bd59517fb2d65d306b",
                    "location": "453.83833212049626 -204.0290249706183",
                    "transitions": [
                        {
                            "name": "Translate Agent Messages",
                            "id": "67bd42d06ea2228d92ca88f1",
                        },
                        {"name": "Wait for Messages", "id": "refId1740431837801"},
                    ],
                    "__gohashid": 66409,
                },
                "612ff3c80832633212b10106": {
                    "category": "Standard",
                    "objectType": "campaignstate",
                    "campaignStateId": "612ff3c80832633212b10106",
                    "name": "Process Customer Messages",
                    "description": "Newly Created State",
                    "actions": [
                        {
                            "name": "Save Variable",
                            "description": "",
                            "properties": {
                                "description": "customerMessage",
                                "rightExpression": "workitem.currentChatMessage.textMsg",
                                "variableName": "customerMessage",
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
                            "id": "refId1740431839186",
                            "icon": "icon-save",
                        },
                        {
                            "name": "Detect Language",
                            "description": "Detect Language",
                            "properties": {
                                "description": "Detect Language",
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "text": "workitem.data.customerMessage",
                            },
                            "type": "detectlanguage",
                            "_selected": False,
                            "id": "refId1740431839187",
                            "icon": "icon-web",
                        },
                        {
                            "name": "Save Variable",
                            "description": "",
                            "properties": {
                                "description": "sourceLanguage",
                                "rightExpression": "workitem.detectLanguageResult.mostLikelyLanguage",
                                "variableName": "sourceLanguage",
                                "asObject": False,
                                "dlpOption": False,
                                "wfmOption": False,
                                "dashboard": False,
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "operator": "==",
                                            "leftExpression": "'detectLanguageResult' in workitem",
                                            "rightExpression": "true",
                                        },
                                        {
                                            "leftExpression": "workitem.detectLanguageResult.status",
                                            "operator": "==",
                                            "rightExpression": "200",
                                        },
                                    ],
                                },
                            },
                            "type": "savevariable",
                            "_selected": False,
                            "id": "refId1740431839188",
                            "icon": "icon-save",
                        },
                        {
                            "name": "Translate Customer Messages",
                            "description": "Transition to another state",
                            "properties": {
                                "description": "workitem.data.sourceLanguage != 'en'",
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.data.sourceLanguage",
                                            "operator": "!=",
                                            "rightExpression": "'en'",
                                        },
                                        {
                                            "leftExpression": "'detectLanguageResult' in workitem",
                                            "operator": "==",
                                            "rightExpression": "true",
                                        },
                                        {
                                            "leftExpression": "workitem.detectLanguageResult.status",
                                            "operator": "==",
                                            "rightExpression": "200",
                                        },
                                    ],
                                },
                                "stateId": "67bd3c04fb61acb976195eee",
                            },
                            "type": "transition",
                            "_selected": True,
                            "transitionId": "67bd42dbb4d78724063bfa49",
                            "icon": "icon-transition",
                            "id": "refId1740431839192",
                        },
                        {
                            "name": "Chat Message Agent",
                            "description": "",
                            "properties": {
                                "message": "workitem.data.customerMessage",
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "operator": "==",
                                            "leftExpression": "workitem.data.sourceLanguage",
                                            "rightExpression": "'en'",
                                        }
                                    ],
                                },
                                "fromType": "CLIENT",
                                "fromId": "${workitem.data.context.consumerData.firstName} ${workitem.data.context.consumerData.lastName}",
                                "description": "English",
                            },
                            "type": "chatmessageagent",
                            "_selected": False,
                            "id": "refId1740431839189",
                            "icon": "icon-ai-message",
                        },
                        {
                            "name": "Wait for Messages",
                            "description": "Transition to another state",
                            "properties": {
                                "description": "Transition to another state",
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "stateName": "Wait for Messages",
                            },
                            "type": "transitionbyname",
                            "_selected": False,
                            "transitionId": "refId1740431837771",
                            "id": "refId1740431839191",
                            "icon": "icon-transition",
                        },
                    ],
                    "_id": "612ff3c80832633212b10106",
                    "key": "612ff3c80832633212b10106",
                    "location": "-93.53307350110549 -78.98913182391851",
                    "transitions": [
                        {
                            "name": "Translate Customer Messages",
                            "id": "67bd42dbb4d78724063bfa49",
                        },
                        {"name": "Wait for Messages", "id": "refId1740431837771"},
                    ],
                    "__gohashid": 66410,
                },
                "62b08f28e945230cb5347c5b": {
                    "category": "Standard",
                    "objectType": "campaignstate",
                    "campaignStateId": "62b08f28e945230cb5347c5b",
                    "name": "Wait for Messages",
                    "description": "Newly Created State",
                    "actions": [
                        {
                            "name": "Wait Chat Message",
                            "description": "",
                            "properties": {
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "timeoutDuration": 3600000,
                                "stateId": "612ff2f1d02eea7fc5cb265d",
                            },
                            "type": "waitforchatmessage",
                            "_selected": False,
                            "icon": "icon-timer",
                            "id": "refId1740431837702",
                        },
                        {
                            "name": "Process Agent Messages",
                            "description": "Transition to another state",
                            "properties": {
                                "description": "Transition to another state",
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.currentChatMessage.type ",
                                            "operator": "==",
                                            "rightExpression": "'USER'",
                                        }
                                    ],
                                },
                                "stateId": "612ff3bd59517fb2d65d306b",
                            },
                            "type": "transition",
                            "_selected": False,
                            "id": "refId1740431837703",
                            "transitionId": "refId1655733056505",
                            "icon": "icon-transition",
                        },
                        {
                            "name": "Process Customer Messages",
                            "description": "Transition to another state",
                            "properties": {
                                "description": "Transition to another state",
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.currentChatMessage.type ",
                                            "operator": "!=",
                                            "rightExpression": "'USER'",
                                        }
                                    ],
                                },
                                "stateId": "612ff3c80832633212b10106",
                            },
                            "type": "transition",
                            "_selected": True,
                            "transitionId": "refId1655733056506",
                            "id": "refId1740431837704",
                            "icon": "icon-transition",
                        },
                    ],
                    "_id": "62b08f28e945230cb5347c5b",
                    "key": "62b08f28e945230cb5347c5b",
                    "location": "-354.5930447502851 -356.9893398035805",
                    "transitions": [
                        {"name": "Process Agent Messages", "id": "refId1655733056505"},
                        {
                            "name": "Process Customer Messages",
                            "id": "refId1655733056506",
                        },
                    ],
                    "__gohashid": 2780,
                },
                "67bd3c04fb61acb976195eee": {
                    "category": "Standard",
                    "objectType": "campaignstate",
                    "campaignStateId": "67bd3c04fb61acb976195eee",
                    "name": "Translate Customer Messages",
                    "description": "Newly Created State",
                    "tenantId": "nextivaretaildemo",
                    "actions": [
                        {
                            "name": "Translate",
                            "description": "Translate",
                            "properties": {
                                "description": "Spanish",
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.data.sourceLanguage",
                                            "operator": "==",
                                            "rightExpression": "'es'",
                                        }
                                    ],
                                },
                                "text": "workitem.data.customerMessage",
                                "sourceLang": "Spanish",
                                "targetLang": "English",
                            },
                            "type": "translate",
                            "_selected": False,
                            "id": "refId1740431839465",
                            "icon": "icon-web",
                        },
                        {
                            "name": "Translate",
                            "description": "Translate",
                            "properties": {
                                "description": "French",
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.data.sourceLanguage",
                                            "operator": "==",
                                            "rightExpression": "'fr'",
                                        }
                                    ],
                                },
                                "text": "workitem.data.customerMessage",
                                "sourceLang": "French",
                                "targetLang": "English",
                            },
                            "type": "translate",
                            "_selected": False,
                            "id": "refId1740431839466",
                            "icon": "icon-web",
                        },
                        {
                            "name": "Translate",
                            "description": "Translate",
                            "properties": {
                                "description": "Portuguese",
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.data.sourceLanguage",
                                            "operator": "==",
                                            "rightExpression": "'pt'",
                                        }
                                    ],
                                },
                                "text": "workitem.data.customerMessage",
                                "sourceLang": "Portuguese",
                                "targetLang": "English",
                            },
                            "type": "translate",
                            "_selected": False,
                            "id": "refId1740431839467",
                            "icon": "icon-web",
                        },
                        {
                            "name": "Translate",
                            "description": "Translate",
                            "properties": {
                                "description": "Afrikaans",
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.data.sourceLanguage",
                                            "operator": "==",
                                            "rightExpression": "'af'",
                                        }
                                    ],
                                },
                                "text": "workitem.data.customerMessage",
                                "sourceLang": "Afrikaans",
                                "targetLang": "English",
                            },
                            "type": "translate",
                            "_selected": False,
                            "id": "refId1740431839468",
                            "icon": "icon-web",
                        },
                        {
                            "name": "Translate",
                            "description": "Translate",
                            "properties": {
                                "description": "Vietnamese",
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.data.sourceLanguage",
                                            "operator": "==",
                                            "rightExpression": "'vi'",
                                        }
                                    ],
                                },
                                "text": "workitem.data.customerMessage",
                                "sourceLang": "Vietnamese",
                                "targetLang": "English",
                            },
                            "type": "translate",
                            "_selected": False,
                            "id": "refId1740431839469",
                            "icon": "icon-web",
                        },
                        {
                            "name": "Save Variable",
                            "description": "",
                            "properties": {
                                "description": "translatedText",
                                "rightExpression": "workitem.translationResult.translation",
                                "variableName": "translatedText",
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
                            "id": "refId1740431839470",
                        },
                        {
                            "name": "Chat Message Agent",
                            "description": "",
                            "properties": {
                                "description": "workitem.data.translatedText",
                                "message": "workitem.data.translatedText",
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "fromType": "CLIENT",
                                "fromId": "${workitem.data.context.consumerData.firstName} ${workitem.data.context.consumerData.lastName}",
                            },
                            "type": "chatmessageagent",
                            "_selected": True,
                            "id": "refId1740431839471",
                            "icon": "icon-ai-message",
                        },
                        {
                            "name": "Wait for Messages",
                            "description": "Transition to another state",
                            "properties": {
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "stateName": "Wait for Messages",
                                "description": "Transition to another state",
                            },
                            "type": "transitionbyname",
                            "_selected": False,
                            "transitionId": "refId1740431838780",
                            "id": "refId1740431839472",
                            "icon": "icon-transition",
                        },
                    ],
                    "_id": "67bd3c04fb61acb976195eee",
                    "key": "67bd3c04fb61acb976195eee",
                    "location": "219.94526238744243 81.23187805687837",
                    "transitions": [
                        {"name": "Wait for Messages", "id": "refId1740431838780"}
                    ],
                },
                "67bd425db5bd6e43dbb27755": {
                    "category": "Standard",
                    "objectType": "campaignstate",
                    "campaignStateId": "67bd425db5bd6e43dbb27755",
                    "name": "Translate Agent Messages",
                    "description": "Newly Created State",
                    "tenantId": "nextivaretaildemo",
                    "actions": [
                        {
                            "name": "Translate",
                            "description": "Translate",
                            "properties": {
                                "description": "Spanish",
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.data.sourceLanguage",
                                            "operator": "==",
                                            "rightExpression": "'es'",
                                        }
                                    ],
                                },
                                "text": "workitem.data.agentMessage",
                                "sourceLang": "English",
                                "targetLang": "Spanish",
                            },
                            "type": "translate",
                            "_selected": False,
                            "id": "refId1740431839659",
                            "icon": "icon-web",
                        },
                        {
                            "name": "Translate",
                            "description": "Translate",
                            "properties": {
                                "description": "French",
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.data.sourceLanguage",
                                            "operator": "==",
                                            "rightExpression": "'fr'",
                                        }
                                    ],
                                },
                                "text": "workitem.data.agentMessage",
                                "sourceLang": "English",
                                "targetLang": "French",
                            },
                            "type": "translate",
                            "_selected": False,
                            "id": "refId1740431839660",
                            "icon": "icon-web",
                        },
                        {
                            "name": "Translate",
                            "description": "Translate",
                            "properties": {
                                "description": "Portuguese",
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.data.sourceLanguage",
                                            "operator": "==",
                                            "rightExpression": "'pt'",
                                        }
                                    ],
                                },
                                "text": "workitem.data.agentMessage",
                                "sourceLang": "English",
                                "targetLang": "Portuguese",
                            },
                            "type": "translate",
                            "_selected": False,
                            "id": "refId1740431839661",
                            "icon": "icon-web",
                        },
                        {
                            "name": "Translate",
                            "description": "Translate",
                            "properties": {
                                "description": "Afrikaans",
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.data.sourceLanguage",
                                            "operator": "==",
                                            "rightExpression": "'af'",
                                        }
                                    ],
                                },
                                "text": "workitem.data.agentMessage",
                                "sourceLang": "English",
                                "targetLang": "Afrikaans",
                            },
                            "type": "translate",
                            "_selected": False,
                            "id": "refId1740431839662",
                            "icon": "icon-web",
                        },
                        {
                            "name": "Translate",
                            "description": "Translate",
                            "properties": {
                                "description": "Vietnamese",
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.data.sourceLanguage",
                                            "operator": "==",
                                            "rightExpression": "'vi'",
                                        }
                                    ],
                                },
                                "text": "workitem.data.agentMessage",
                                "sourceLang": "English",
                                "targetLang": "Vietnamese",
                            },
                            "type": "translate",
                            "_selected": False,
                            "id": "refId1740431839663",
                            "icon": "icon-web",
                        },
                        {
                            "name": "Save Variable",
                            "description": "",
                            "properties": {
                                "description": "translatedText",
                                "rightExpression": "workitem.translationResult.translation",
                                "variableName": "translatedText",
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
                            "id": "refId1740431839664",
                        },
                        {
                            "name": "Chat Message Consumer",
                            "description": "",
                            "properties": {
                                "description": "workitem.data.translatedText",
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "from": "workitem.data.companyName",
                                "message": "workitem.data.translatedText",
                                "messageType": "BOT",
                                "options": [],
                            },
                            "type": "chatmessageconsumer",
                            "_selected": True,
                            "id": "refId1740431839665",
                            "icon": "icon-ai-message",
                        },
                        {
                            "name": "Wait for Messages",
                            "description": "Transition to another state",
                            "properties": {
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "stateName": "Wait for Messages",
                                "description": "Transition to another state",
                            },
                            "type": "transitionbyname",
                            "_selected": False,
                            "transitionId": "refId1740431839299",
                            "id": "refId1740431839666",
                            "icon": "icon-transition",
                        },
                    ],
                    "_id": "67bd425db5bd6e43dbb27755",
                    "key": "67bd425db5bd6e43dbb27755",
                    "location": "795.2173121092856 -44.549907813867094",
                    "transitions": [
                        {"name": "Wait for Messages", "id": "refId1740431839299"}
                    ],
                },
            },
        }
    )
    headers = {
        "Authorization": ncc_token,
        "Content-Type": "application/json",
    }
    try:
        conn.request("POST", "/data/api/types/function/", payload, headers)
        res = conn.getresponse()
        if res.status == 201:
            data = res.read().decode("utf-8")
            function = json.loads(data)
    except:
        pass
    conn.close()
    return function


def create_two_way_sms_function(
    ncc_location: str, ncc_token: str, function_name: str
) -> dict:
    """
    This function creates an NCC function.
    """
    function = {}
    conn = http.client.HTTPSConnection(ncc_location)
    payload = json.dumps(
        {
            "name": function_name,
            "states": {
                "612ff2f1d02eea7fc5cb265d": {
                    "category": "Standard",
                    "campaignStateId": "612ff2f1d02eea7fc5cb265d",
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
                    "key": "612ff2f1d02eea7fc5cb265d",
                    "_id": "612ff2f1d02eea7fc5cb265d",
                    "description": "End State",
                    "name": "End State",
                    "location": "-161.36846272687495 -49.74660419945286",
                    "transitions": [],
                    "__gohashid": 66405,
                },
                "start-state": {
                    "category": "Begin",
                    "campaignStateId": "start-state",
                    "actions": [
                        {
                            "name": "OutboundSMS",
                            "type": "transition",
                            "description": "Transition to another state",
                            "properties": {
                                "description": "Transition to another state",
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "operator": "==",
                                            "leftExpression": "workitem.type",
                                            "rightExpression": "'OutboundSMS'",
                                        }
                                    ],
                                },
                                "stateId": "612ff35f0e0c559bed2e5c81",
                                "name": "Start",
                            },
                            "_selected": False,
                            "id": "refId1740431839807",
                            "transitionId": "612ff3a2d1ec0e08e1e29bcf",
                            "icon": "icon-transition",
                        },
                        {
                            "name": "Wait for Messages",
                            "description": "Transition to another state",
                            "properties": {
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "stateId": "612ff3880ab56f6610b79c74",
                                "description": "Transition to another state",
                            },
                            "type": "transition",
                            "_selected": True,
                            "transitionId": "refId1630518553842",
                            "id": "refId1740431839808",
                            "icon": "icon-transition",
                        },
                    ],
                    "transitions": [
                        {"name": "OutboundSMS", "id": "612ff3a2d1ec0e08e1e29bcf"},
                        {"name": "Wait for Messages", "id": "refId1630518553842"},
                    ],
                    "objectType": "campaignstate",
                    "key": "start-state",
                    "_id": "start-state",
                    "description": "Begin State",
                    "name": "Begin State",
                    "location": "-53.66585142019534 -315.1062572782813",
                    "__gohashid": 66406,
                },
                "612ff35f0e0c559bed2e5c81": {
                    "category": "Standard",
                    "objectType": "campaignstate",
                    "campaignStateId": "612ff35f0e0c559bed2e5c81",
                    "name": "OutboundSMS",
                    "description": "Newly Created State",
                    "actions": [
                        {
                            "name": "SMS Forward To Consumer",
                            "description": "",
                            "properties": {
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                }
                            },
                            "type": "smsforwardmessageconsumer",
                            "_selected": False,
                            "id": "refId1740431839906",
                            "icon": "icon-mail-forward",
                        },
                        {
                            "icon": "icon-transition",
                            "name": "Wait for Messages",
                            "description": "Transition to another state",
                            "properties": {
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "stateName": "Wait for Messages",
                            },
                            "type": "transitionbyname",
                            "_selected": True,
                            "transitionId": "refId1740431839936",
                        },
                    ],
                    "_id": "612ff35f0e0c559bed2e5c81",
                    "key": "612ff35f0e0c559bed2e5c81",
                    "location": "604.1346275561209 -154.4762946540609",
                    "transitions": [
                        {"name": "Wait for Messages", "id": "refId1740431839936"}
                    ],
                    "__gohashid": 66407,
                },
                "612ff3880ab56f6610b79c74": {
                    "category": "Standard",
                    "objectType": "campaignstate",
                    "campaignStateId": "612ff3880ab56f6610b79c74",
                    "name": "Wait for Messages",
                    "description": "Newly Created State",
                    "actions": [
                        {
                            "name": "SMS Wait For Messages",
                            "description": "",
                            "properties": {
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "timeoutDuration": 3600000,
                                "stateId": "612ff2f1d02eea7fc5cb265d",
                            },
                            "type": "smswaitformessage",
                            "_selected": False,
                            "id": "refId1740431840301",
                            "icon": "icon-timer",
                        },
                        {
                            "name": "Process Agent Messages",
                            "description": "Transition to another state",
                            "properties": {
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.currentSMSMessage.type",
                                            "operator": "==",
                                            "rightExpression": "'USER'",
                                        }
                                    ],
                                },
                                "stateId": "612ff3bd59517fb2d65d306b",
                                "description": "Transition to another state",
                            },
                            "type": "transition",
                            "_selected": True,
                            "transitionId": "refId1630518553915",
                            "id": "refId1740431840302",
                            "icon": "icon-transition",
                        },
                        {
                            "name": "Process Customer Messages",
                            "description": "Transition to another state",
                            "properties": {
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.currentSMSMessage.type",
                                            "operator": "!=",
                                            "rightExpression": "'USER'",
                                        }
                                    ],
                                },
                                "stateId": "612ff3c80832633212b10106",
                                "description": "Transition to another state",
                            },
                            "type": "transition",
                            "_selected": False,
                            "transitionId": "refId1630518553916",
                            "id": "refId1740431840303",
                            "icon": "icon-transition",
                        },
                    ],
                    "_id": "612ff3880ab56f6610b79c74",
                    "key": "612ff3880ab56f6610b79c74",
                    "location": "260.09313151166816 31.702892867660353",
                    "transitions": [
                        {"name": "Process Agent Messages", "id": "refId1630518553915"},
                        {
                            "name": "Process Customer Messages",
                            "id": "refId1630518553916",
                        },
                    ],
                    "__gohashid": 66408,
                },
                "612ff3bd59517fb2d65d306b": {
                    "category": "Standard",
                    "objectType": "campaignstate",
                    "campaignStateId": "612ff3bd59517fb2d65d306b",
                    "name": "Process Agent Messages",
                    "description": "Newly Created State",
                    "actions": [
                        {
                            "name": "Save Variable",
                            "description": "",
                            "properties": {
                                "description": "agentMessage",
                                "rightExpression": "workitem.currentSMSMessage.textMsg",
                                "variableName": "agentMessage",
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
                            "id": "refId1740460008313",
                            "icon": "icon-save",
                        },
                        {
                            "name": "Translate Agent Messages",
                            "description": "Transition to another state",
                            "properties": {
                                "description": "Non-English",
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.data.sourceLanguage",
                                            "operator": "!=",
                                            "rightExpression": "'en'",
                                        }
                                    ],
                                },
                                "stateId": "67bd5428c2ee169ce826991e",
                                "points": {
                                    "h": True,
                                    "r": [],
                                    "ct": 0,
                                    "__gohashid": 33963,
                                },
                            },
                            "type": "transition",
                            "_selected": False,
                            "transitionId": "refId1740460008074",
                            "id": "refId1740460008314",
                            "icon": "icon-transition",
                        },
                        {
                            "icon": "icon-mail-forward",
                            "name": "SMS Forward To Consumer",
                            "description": "",
                            "properties": {
                                "description": "English",
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.data.sourceLanguage",
                                            "operator": "==",
                                            "rightExpression": "'en'",
                                        }
                                    ],
                                },
                            },
                            "type": "smsforwardmessageconsumer",
                            "_selected": True,
                        },
                        {
                            "name": "Wait for Messages",
                            "description": "Transition to another state",
                            "properties": {
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "stateName": "Wait for Messages",
                                "description": "Transition to another state",
                            },
                            "type": "transitionbyname",
                            "_selected": False,
                            "transitionId": "refId1740431839867",
                            "id": "refId1740460008316",
                            "icon": "icon-transition",
                        },
                    ],
                    "_id": "612ff3bd59517fb2d65d306b",
                    "key": "612ff3bd59517fb2d65d306b",
                    "location": "1086.0111696022634 210.05104007830812",
                    "transitions": [
                        {
                            "name": "Translate Agent Messages",
                            "id": "refId1740460008074",
                        },
                        {"name": "Wait for Messages", "id": "refId1740431839867"},
                    ],
                    "__gohashid": 66409,
                },
                "612ff3c80832633212b10106": {
                    "category": "Standard",
                    "objectType": "campaignstate",
                    "campaignStateId": "612ff3c80832633212b10106",
                    "name": "Process Customer Messages",
                    "description": "Newly Created State",
                    "actions": [
                        {
                            "name": "Save Variable",
                            "description": "",
                            "properties": {
                                "description": "customerMessage",
                                "rightExpression": "workitem.currentSMSMessage.textMsg",
                                "variableName": "customerMessage",
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
                            "id": "refId1740460008031",
                            "icon": "icon-save",
                        },
                        {
                            "name": "Detect Language",
                            "description": "Detect Language",
                            "properties": {
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "text": "workitem.data.customerMessage",
                                "description": "Detect Language",
                            },
                            "type": "detectlanguage",
                            "_selected": False,
                            "id": "refId1740460008032",
                            "icon": "icon-web",
                        },
                        {
                            "name": "Save Variable",
                            "description": "",
                            "properties": {
                                "description": "sourceLanguage",
                                "rightExpression": "workitem.detectLanguageResult.mostLikelyLanguage",
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
                            "id": "refId1740460008033",
                            "icon": "icon-save",
                        },
                        {
                            "name": "Translate Customer Messages",
                            "description": "Transition to another state",
                            "properties": {
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.data.sourceLanguage",
                                            "operator": "!=",
                                            "rightExpression": "'en'",
                                        }
                                    ],
                                },
                                "stateId": "67bd503d3d360b21dbeadaab",
                                "description": "Non-English",
                            },
                            "type": "transition",
                            "_selected": True,
                            "transitionId": "refId1740460007689",
                            "id": "refId1740460008034",
                            "icon": "icon-transition",
                        },
                        {
                            "name": "Chat Message Agent",
                            "description": "",
                            "properties": {
                                "message": "workitem.data.customerMessage",
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.data.sourceLanguage",
                                            "operator": "==",
                                            "rightExpression": "'en'",
                                        }
                                    ],
                                },
                                "fromType": "CLIENT",
                                "fromId": "workitem.from",
                                "description": "English",
                            },
                            "type": "chatmessageagent",
                            "_selected": False,
                            "id": "refId1740460008035",
                            "icon": "icon-ai-message",
                        },
                        {
                            "name": "Wait for Messages",
                            "description": "Transition to another state",
                            "properties": {
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "stateName": "Wait for Messages",
                                "description": "Transition to another state",
                            },
                            "type": "transitionbyname",
                            "_selected": False,
                            "transitionId": "refId1740431839904",
                            "id": "refId1740460008036",
                            "icon": "icon-transition",
                        },
                    ],
                    "_id": "612ff3c80832633212b10106",
                    "key": "612ff3c80832633212b10106",
                    "location": "550.3167805397934 335.24967225928475",
                    "transitions": [
                        {
                            "name": "Translate Customer Messages",
                            "id": "refId1740460007689",
                        },
                        {"name": "Wait for Messages", "id": "refId1740431839904"},
                    ],
                    "__gohashid": 66410,
                },
                "67bd503d3d360b21dbeadaab": {
                    "category": "Standard",
                    "objectType": "campaignstate",
                    "campaignStateId": "67bd503d3d360b21dbeadaab",
                    "name": "Translate Customer Messages",
                    "description": "Newly Created State",
                    "tenantId": "nextivaretaildemo",
                    "actions": [
                        {
                            "name": "Translate",
                            "description": "Translate",
                            "properties": {
                                "description": "Spanish",
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.data.sourceLanguage",
                                            "operator": "==",
                                            "rightExpression": "'es'",
                                        }
                                    ],
                                },
                                "text": "workitem.data.customerMessage",
                                "sourceLang": "Spanish",
                                "targetLang": "English",
                            },
                            "type": "translate",
                            "_selected": False,
                            "icon": "icon-web",
                            "id": "refId1740460007893",
                        },
                        {
                            "name": "Translate",
                            "description": "Translate",
                            "properties": {
                                "description": "French",
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.data.sourceLanguage",
                                            "operator": "==",
                                            "rightExpression": "'fr'",
                                        }
                                    ],
                                },
                                "text": "workitem.data.customerMessage",
                                "sourceLang": "French",
                                "targetLang": "English",
                            },
                            "type": "translate",
                            "_selected": False,
                            "icon": "icon-web",
                            "id": "refId1740460007911",
                        },
                        {
                            "name": "Translate",
                            "description": "Translate",
                            "properties": {
                                "description": "Portuguese",
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.data.sourceLanguage",
                                            "operator": "==",
                                            "rightExpression": "'pt'",
                                        }
                                    ],
                                },
                                "text": "workitem.data.customerMessage",
                                "sourceLang": "Portuguese",
                                "targetLang": "English",
                            },
                            "type": "translate",
                            "_selected": False,
                            "icon": "icon-web",
                            "id": "refId1740460007926",
                        },
                        {
                            "name": "Translate",
                            "description": "Translate",
                            "properties": {
                                "description": "Afrikaans",
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.data.sourceLanguage",
                                            "operator": "==",
                                            "rightExpression": "'af'",
                                        }
                                    ],
                                },
                                "text": "workitem.data.customerMessage",
                                "sourceLang": "Afrikaans",
                                "targetLang": "English",
                            },
                            "type": "translate",
                            "_selected": False,
                            "icon": "icon-web",
                            "id": "refId1740460007941",
                        },
                        {
                            "name": "Translate",
                            "description": "Translate",
                            "properties": {
                                "description": "Vietnamese",
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.data.sourceLanguage",
                                            "operator": "==",
                                            "rightExpression": "'vi'",
                                        }
                                    ],
                                },
                                "text": "workitem.data.customerMessage",
                                "sourceLang": "Vietnamese",
                                "targetLang": "English",
                            },
                            "type": "translate",
                            "_selected": False,
                            "icon": "icon-web",
                            "id": "refId1740460007956",
                        },
                        {
                            "name": "Save Variable",
                            "description": "",
                            "properties": {
                                "description": "translatedText",
                                "rightExpression": "workitem.translationResult.translation",
                                "variableName": "translatedText",
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
                            "icon": "icon-save",
                            "id": "refId1740460007894",
                        },
                        {
                            "name": "Chat Message Agent",
                            "description": "",
                            "properties": {
                                "message": "workitem.data.translatedText",
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "fromType": "CLIENT",
                                "fromId": "workitem.from",
                            },
                            "type": "chatmessageagent",
                            "_selected": False,
                            "icon": "icon-ai-message",
                            "id": "refId1740460007895",
                        },
                        {
                            "name": "Wait for Messages",
                            "description": "Transition to another state",
                            "properties": {
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "stateName": "Wait for Messages",
                                "description": "Transition to another state",
                            },
                            "type": "transitionbyname",
                            "_selected": False,
                            "transitionId": "refId1740460007590",
                            "id": "refId1740460007896",
                            "icon": "icon-transition",
                        },
                    ],
                    "_id": "67bd503d3d360b21dbeadaab",
                    "key": "67bd503d3d360b21dbeadaab",
                    "location": "866.7870650001614 535.8438214337766",
                    "transitions": [
                        {"name": "Wait for Messages", "id": "refId1740460007590"}
                    ],
                },
                "67bd5428c2ee169ce826991e": {
                    "category": "Standard",
                    "objectType": "campaignstate",
                    "campaignStateId": "67bd5428c2ee169ce826991e",
                    "name": "Translate Agent Messages",
                    "description": "Newly Created State",
                    "tenantId": "nextivaretaildemo",
                    "actions": [
                        {
                            "name": "Translate",
                            "description": "Translate",
                            "properties": {
                                "description": "Spanish",
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.data.sourceLanguage",
                                            "operator": "==",
                                            "rightExpression": "'es'",
                                        }
                                    ],
                                },
                                "text": "workitem.data.agentMessage",
                                "sourceLang": "English",
                                "targetLang": "Spanish",
                            },
                            "type": "translate",
                            "_selected": False,
                            "icon": "icon-web",
                            "id": "refId1740460008422",
                        },
                        {
                            "name": "Translate",
                            "description": "Translate",
                            "properties": {
                                "description": "French",
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.data.sourceLanguage",
                                            "operator": "==",
                                            "rightExpression": "'fr'",
                                        }
                                    ],
                                },
                                "text": "workitem.data.agentMessage",
                                "sourceLang": "English",
                                "targetLang": "French",
                            },
                            "type": "translate",
                            "_selected": False,
                            "icon": "icon-web",
                            "id": "refId1740460008440",
                        },
                        {
                            "name": "Translate",
                            "description": "Translate",
                            "properties": {
                                "description": "Portuguese",
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.data.sourceLanguage",
                                            "operator": "==",
                                            "rightExpression": "'pt'",
                                        }
                                    ],
                                },
                                "text": "workitem.data.agentMessage",
                                "sourceLang": "English",
                                "targetLang": "Portuguese",
                            },
                            "type": "translate",
                            "_selected": False,
                            "icon": "icon-web",
                            "id": "refId1740460008455",
                        },
                        {
                            "name": "Translate",
                            "description": "Translate",
                            "properties": {
                                "description": "Afrikaans",
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.data.sourceLanguage",
                                            "operator": "==",
                                            "rightExpression": "'af'",
                                        }
                                    ],
                                },
                                "text": "workitem.data.agentMessage",
                                "sourceLang": "English",
                                "targetLang": "Afrikaans",
                            },
                            "type": "translate",
                            "_selected": True,
                            "icon": "icon-web",
                            "id": "refId1740460008470",
                        },
                        {
                            "name": "Translate",
                            "description": "Translate",
                            "properties": {
                                "description": "Vietnamese",
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.data.sourceLanguage",
                                            "operator": "==",
                                            "rightExpression": "'vi'",
                                        }
                                    ],
                                },
                                "text": "workitem.data.agentMessage",
                                "sourceLang": "English",
                                "targetLang": "Vietnamese",
                            },
                            "type": "translate",
                            "_selected": False,
                            "icon": "icon-web",
                            "id": "refId1740460008485",
                        },
                        {
                            "name": "Save Variable",
                            "description": "",
                            "properties": {
                                "description": "translatedText",
                                "rightExpression": "workitem.translationResult.translation",
                                "variableName": "translatedText",
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
                            "id": "refId1740460008423",
                        },
                        {
                            "name": "SMS Message Consumer",
                            "description": "",
                            "properties": {
                                "message": "workitem.data.translatedText",
                                "toAddress": "workitem.from",
                                "fromAddress": "workitem.to",
                                "createNewWorkitem": False,
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                            },
                            "type": "smsmessageconsumer",
                            "_selected": False,
                            "icon": "icon-ai-message",
                            "id": "refId1740460008424",
                        },
                        {
                            "name": "Wait for Messages",
                            "description": "Transition to another state",
                            "properties": {
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "stateName": "Wait for Messages",
                                "description": "Transition to another state",
                            },
                            "type": "transitionbyname",
                            "_selected": False,
                            "transitionId": "refId1740460008012",
                            "id": "refId1740460008425",
                            "icon": "icon-transition",
                        },
                    ],
                    "_id": "67bd5428c2ee169ce826991e",
                    "key": "67bd5428c2ee169ce826991e",
                    "location": "1436.3930803836427 390.18766137899274",
                    "transitions": [
                        {"name": "Wait for Messages", "id": "refId1740460008012"}
                    ],
                },
            },
        }
    )
    headers = {
        "Authorization": ncc_token,
        "Content-Type": "application/json",
    }
    try:
        conn.request("POST", "/data/api/types/function/", payload, headers)
        res = conn.getresponse()
        if res.status == 201:
            data = res.read().decode("utf-8")
            function = json.loads(data)
    except:
        pass
    conn.close()
    return function


def create_acd_voicemail_function(
    ncc_location: str, ncc_token: str, function_name: str
) -> dict:
    """
    This function creates an NCC function.
    """
    function = {}
    conn = http.client.HTTPSConnection(ncc_location)
    payload = json.dumps(
        {
            "localizations": {
                "name": {
                    "en": {
                        "language": "en",
                        "value": function_name,
                    }
                }
            },
            "states": {
                "5dc401ec494df97002ea2b57": {
                    "category": "Standard",
                    "campaignStateId": "5dc401ec494df97002ea2b57",
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
                            "id": "refId1655838057839",
                            "icon": "icon-terminate",
                        }
                    ],
                    "objectType": "campaignstate",
                    "key": "5dc401ec494df97002ea2b57",
                    "_id": "5dc401ec494df97002ea2b57",
                    "description": "End State",
                    "name": "End State",
                    "location": "222.2019827736027 834.963330452857",
                    "transitions": [],
                    "__gohashid": 40842,
                },
                "start-state": {
                    "category": "Begin",
                    "campaignStateId": "start-state",
                    "actions": [
                        {
                            "name": "Time Event",
                            "description": "Add Custom Time Event",
                            "properties": {
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "eventName": "ACD Voicemail",
                                "description": "Add Custom Time Event",
                            },
                            "type": "addtimeevent",
                            "_selected": False,
                            "id": "refId1740101739903",
                            "icon": "icon-clock",
                        },
                        {
                            "name": "Exit Queue",
                            "description": "Remove workitem from queue",
                            "properties": {
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "description": "",
                            },
                            "type": "exitqueue",
                            "_selected": False,
                            "id": "refId1740101739905",
                            "icon": "icon-exitqueues",
                        },
                        {
                            "name": "Save Variable",
                            "description": "",
                            "properties": {
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "rightExpression": "0",
                                "variableName": "messageRecorded",
                                "description": "messageRecorded = 0",
                                "asObject": True,
                            },
                            "type": "savevariable",
                            "_selected": False,
                            "id": "refId1740101739906",
                            "icon": "icon-save",
                        },
                        {
                            "name": "Record VM",
                            "type": "transition",
                            "description": "Transition to another state",
                            "properties": {
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "stateId": "5dc401fe07b302d7a780e761",
                                "name": "Start",
                                "description": "Transition to another state",
                                "points": {
                                    "h": True,
                                    "r": [],
                                    "ct": 0,
                                    "__gohashid": 26492,
                                },
                            },
                            "transitionId": "5dc4023452d09c4fc8369c19",
                            "_selected": True,
                            "id": "refId1740101739907",
                            "icon": "icon-transition",
                        },
                    ],
                    "transitions": [
                        {"name": "Record VM", "id": "5dc4023452d09c4fc8369c19"}
                    ],
                    "objectType": "campaignstate",
                    "key": "start-state",
                    "_id": "start-state",
                    "description": "Begin State",
                    "name": "Begin State",
                    "location": "-868.9999999999999 104.5557884668251",
                    "__gohashid": 40843,
                },
                "5dc401fe07b302d7a780e761": {
                    "category": "Standard",
                    "campaignStateId": "5dc401fe07b302d7a780e761",
                    "actions": [
                        {
                            "icon": "icon-tts",
                            "name": "Synthesize Text via Google TTS",
                            "description": "Convert Text into Audio using Google's Text-To-Speech",
                            "properties": {
                                "voiceName": "en-US-Wavenet-J",
                                "text": '<prosody pitch="-2st">Please leave your message after the tone. When you are finished, you may hang up, or stay on the line for more options.</prosody>',
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                            },
                            "type": "googletts",
                            "_selected": False,
                        },
                        {
                            "name": "Recording",
                            "description": "",
                            "properties": {
                                "description": "",
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "maxLengthInSeconds": "60",
                                "playBeep": 1,
                                "silenceTimeout": "7",
                                "terminationKey": "#",
                                "transcribe": 0,
                                "trim": 1,
                                "variable": "acdvm",
                            },
                            "type": "record",
                            "_selected": False,
                            "id": "refId1740101739815",
                            "icon": "icon-record-start",
                        },
                        {
                            "name": "Save Variable",
                            "description": "",
                            "properties": {
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "rightExpression": "1",
                                "variableName": "messageRecorded",
                                "description": "messageRecorded = 1",
                                "asObject": True,
                            },
                            "type": "savevariable",
                            "_selected": False,
                            "id": "refId1740101739816",
                            "icon": "icon-save",
                        },
                        {
                            "name": "Start Timer",
                            "description": "",
                            "properties": {
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "timeoutInSeconds": "1",
                                "description": "Pause in case of hangup before leaving message",
                            },
                            "type": "starttimer",
                            "_selected": False,
                            "id": "refId1740101739817",
                            "icon": "icon-timer",
                        },
                        {
                            "name": "Save Variable",
                            "description": "",
                            "properties": {
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "rightExpression": "1",
                                "variableName": "retries",
                                "description": "retries = 1",
                                "asObject": True,
                            },
                            "type": "savevariable",
                            "_selected": False,
                            "id": "refId1740101739818",
                            "icon": "icon-save",
                        },
                        {
                            "name": "Options Menu",
                            "description": "Transition to another state",
                            "properties": {
                                "description": "",
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "stateId": "5dc40291e680339a6aecc831",
                                "name": "Transition",
                                "points": {
                                    "h": True,
                                    "r": [],
                                    "ct": 0,
                                    "__gohashid": 24281,
                                },
                            },
                            "type": "transition",
                            "_selected": True,
                            "transitionId": "refId1573126598874",
                            "id": "refId1740101739819",
                            "icon": "icon-transition",
                        },
                    ],
                    "name": "Record VM",
                    "description": "Newly Created State",
                    "objectType": "campaignstate",
                    "_id": "5dc401fe07b302d7a780e761",
                    "key": "5dc401fe07b302d7a780e761",
                    "location": "-617.0166999820101 254.1879751541553",
                    "loc": "200.03145361646278 -52.4453125",
                    "__gohashid": 4074,
                    "transitions": [
                        {"name": "Options Menu", "id": "refId1573126598874"}
                    ],
                },
                "5dc40291e680339a6aecc831": {
                    "category": "Standard",
                    "campaignStateId": "5dc40291e680339a6aecc831",
                    "actions": [
                        {
                            "icon": "icon-tts",
                            "name": "Play Collect Google TTS",
                            "description": "Play Collect using Text-To-Speech",
                            "properties": {
                                "description": "Save (1), Listen (2), Re-record (3), Cancel (*)",
                                "voiceName": "en-US-Wavenet-J",
                                "voiceGender": "male",
                                "text": '<prosody pitch="-2st">To save your message, press 1. To hear your message, press 2. To re-record your message, press 3. To cancel your message, press star.</prosody>',
                                "numberDigits": 1,
                                "terminationKey": "#",
                                "timeoutInSeconds": "7",
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
                            "name": "Play Recording",
                            "description": "",
                            "properties": {
                                "description": "workitem.digits == '2'",
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
                                "loop": 1,
                                "recordingFilename": "workitem.data.acdvm.filename",
                            },
                            "type": "playrecording",
                            "_selected": False,
                            "id": "refId1740101739507",
                            "icon": "icon-playrecording",
                        },
                        {
                            "name": "Back to Top",
                            "description": "Transition to another state",
                            "properties": {
                                "description": "workitem.digits == '2'",
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
                                "stateName": "Options Menu",
                            },
                            "type": "transitionbyname",
                            "_selected": False,
                            "transitionId": "refId1740101739453",
                            "id": "refId1740101739508",
                            "icon": "icon-transition",
                        },
                        {
                            "name": "Save Variable",
                            "description": "",
                            "properties": {
                                "description": "messageRecorded = 0, workitem.digits == '3' or '*'",
                                "condition": {
                                    "conditionType": "OR",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.digits",
                                            "operator": "==",
                                            "rightExpression": "'3'",
                                        },
                                        {
                                            "leftExpression": "workitem.digits",
                                            "operator": "==",
                                            "rightExpression": "'*'",
                                        },
                                    ],
                                },
                                "rightExpression": "0",
                                "variableName": "messageRecorded",
                                "asObject": True,
                            },
                            "type": "savevariable",
                            "_selected": False,
                            "id": "refId1740101739509",
                            "icon": "icon-save",
                        },
                        {
                            "name": "Record VM",
                            "description": "Transition to another state",
                            "properties": {
                                "description": "workitem.digits == '3'",
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.digits",
                                            "operator": "==",
                                            "rightExpression": "'3'",
                                        }
                                    ],
                                },
                                "stateName": "Record VM",
                            },
                            "type": "transitionbyname",
                            "_selected": False,
                            "transitionId": "refId1740101739373",
                            "id": "refId1740101739510",
                            "icon": "icon-transition",
                        },
                        {
                            "name": "Create ACD VM",
                            "description": "Transition to another state",
                            "properties": {
                                "description": "workitem.digits == '1'",
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
                                "stateId": "5dc40521e22562777dcb2007",
                                "name": "Transition",
                                "points": {
                                    "h": True,
                                    "r": [],
                                    "ct": 0,
                                    "__gohashid": 20591,
                                },
                            },
                            "type": "transition",
                            "_selected": False,
                            "transitionId": "refId1573126598797",
                            "id": "refId1740101739511",
                            "icon": "icon-transition",
                        },
                        {
                            "name": "Return To Workflow",
                            "description": "",
                            "properties": {
                                "description": "workitem.digits == '*'",
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.digits",
                                            "operator": "==",
                                            "rightExpression": "'*'",
                                        }
                                    ],
                                },
                            },
                            "type": "functionreturn",
                            "_selected": False,
                            "id": "refId1740101739512",
                            "icon": "icon-functionreturn",
                        },
                        {
                            "name": "Back to Top",
                            "description": "Transition to another state",
                            "properties": {
                                "description": "",
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "stateName": "Options Menu",
                            },
                            "type": "transitionbyname",
                            "_selected": True,
                            "transitionId": "refId1740101739423",
                            "id": "refId1740101739513",
                            "icon": "icon-transition",
                        },
                    ],
                    "name": "Options Menu",
                    "description": "Newly Created State",
                    "objectType": "campaignstate",
                    "_id": "5dc40291e680339a6aecc831",
                    "key": "5dc40291e680339a6aecc831",
                    "location": "-334.13535998891757 470.32989886237533",
                    "loc": "165.03145361646278 67.5546875",
                    "__gohashid": 8936,
                    "transitions": [
                        {"name": "Back to Top", "id": "refId1740101739453"},
                        {"name": "Record VM", "id": "refId1740101739373"},
                        {"name": "Create ACD VM", "id": "refId1573126598797"},
                        {"name": "Back to Top", "id": "refId1740101739423"},
                    ],
                },
                "5dc40521e22562777dcb2007": {
                    "category": "Standard",
                    "campaignStateId": "5dc40521e22562777dcb2007",
                    "actions": [
                        {
                            "icon": "icon-tts",
                            "name": "Synthesize Text via Google TTS",
                            "description": "Convert Text into Audio using Google's Text-To-Speech",
                            "properties": {
                                "description": "Thank you for calling...",
                                "voiceName": "en-US-Wavenet-J",
                                "text": '<prosody pitch="-2st">Thank you for calling, and have a great Day!</prosody>',
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                            },
                            "type": "googletts",
                            "_selected": False,
                        },
                        {
                            "name": "Save Variable",
                            "description": "",
                            "properties": {
                                "description": "messageRecorded = 0",
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "rightExpression": "0",
                                "variableName": "messageRecorded",
                                "asObject": True,
                            },
                            "type": "savevariable",
                            "_selected": False,
                            "id": "refId1740101740016",
                            "icon": "icon-save",
                        },
                        {
                            "name": "ACD Voicemail From Expression",
                            "description": "Create ACD Voicemail",
                            "properties": {
                                "description": "workitem.data.queueId",
                                "priority": 3,
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "queueIdsExpression": "workitem.data.queueId",
                                "transcription": True,
                            },
                            "type": "acdvmfromexpression",
                            "_selected": False,
                            "id": "refId1740101740017",
                            "icon": "icon-directconnect",
                        },
                        {
                            "name": "End State",
                            "description": "Transition to another state",
                            "properties": {
                                "description": "Transition to another state",
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "stateId": "5dc401ec494df97002ea2b57",
                                "name": "Transition",
                                "points": {
                                    "h": True,
                                    "r": [],
                                    "ct": 0,
                                    "__gohashid": 28713,
                                },
                            },
                            "type": "transition",
                            "_selected": True,
                            "transitionId": "refId1573126598835",
                            "id": "refId1740101740018",
                            "icon": "icon-transition",
                        },
                    ],
                    "name": "Create ACD VM",
                    "description": "Newly Created State",
                    "objectType": "campaignstate",
                    "_id": "5dc40521e22562777dcb2007",
                    "key": "5dc40521e22562777dcb2007",
                    "location": "-31.9566348868193 679.5074891788356",
                    "loc": "213.03145361646278 459.0546875",
                    "__gohashid": 62107,
                    "transitions": [{"name": "End State", "id": "refId1573126598835"}],
                },
            },
            "name": function_name,
        }
    )
    headers = {
        "Authorization": ncc_token,
        "Content-Type": "application/json",
    }
    try:
        conn.request("POST", "/data/api/types/function/", payload, headers)
        res = conn.getresponse()
        if res.status == 201:
            data = res.read().decode("utf-8")
            function = json.loads(data)
    except:
        pass
    conn.close()
    return function


def create_acd_callback_function(
    ncc_location: str, ncc_token: str, function_name: str
) -> dict:
    """
    This function creates an NCC function.
    """
    function = {}
    conn = http.client.HTTPSConnection(ncc_location)
    payload = json.dumps(
        {
            "localizations": {
                "name": {
                    "en": {
                        "language": "en",
                        "value": function_name,
                    }
                }
            },
            "states": {
                "5c73b01813488773a0fd8999": {
                    "category": "Standard",
                    "campaignStateId": "5c73b01813488773a0fd8999",
                    "actions": [
                        {
                            "name": "terminate",
                            "type": "terminate",
                            "properties": {
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                }
                            },
                        }
                    ],
                    "objectType": "campaignstate",
                    "key": "5c73b01813488773a0fd8999",
                    "_id": "5c73b01813488773a0fd8999",
                    "description": "End State",
                    "name": "End State",
                    "location": "186.51006895312503 587.3275995566405",
                    "__gohashid": 2480,
                    "transitions": [],
                },
                "start-state": {
                    "category": "Begin",
                    "campaignStateId": "start-state",
                    "actions": [
                        {
                            "name": "Save Variable",
                            "properties": {
                                "variableName": "callbackNumber",
                                "rightExpression": "workitem.from.slice(-10)",
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [],
                                },
                                "description": "callbackNumber",
                                "asObject": True,
                            },
                            "type": "savevariable",
                            "_selected": False,
                            "_icon": "icon-savevariable",
                            "id": "refId1740106540449",
                            "icon": "icon-save",
                        },
                        {
                            "name": "Confirm Number",
                            "properties": {
                                "stateId": "5c73b0b8071b1abb22a4a96d",
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [],
                                },
                                "name": "Transition",
                                "description": "Transition to another state",
                                "points": {
                                    "h": True,
                                    "r": [
                                        {
                                            "b": 348.79713078124996,
                                            "k": 332.8502000500488,
                                            "h": True,
                                        },
                                        {
                                            "b": 358.79713078124996,
                                            "k": 332.8502000500488,
                                            "h": True,
                                        },
                                        {"b": 356, "k": 332.8502000500488, "h": True},
                                        {"b": 356, "k": 332.8502000500488, "h": True},
                                        {
                                            "b": 597.0250689531251,
                                            "k": 332.8502000500488,
                                            "h": True,
                                        },
                                        {
                                            "b": 597.0250689531251,
                                            "k": 418.86155312668416,
                                            "h": True,
                                        },
                                        {
                                            "b": 597.0250689531251,
                                            "k": 428.86155312668416,
                                            "h": True,
                                        },
                                    ],
                                    "ct": 7,
                                    "__gohashid": 30883,
                                },
                            },
                            "type": "transition",
                            "transitionId": "5c73b5e87176db9eb5140a8d",
                            "description": "Transition to confirm number",
                            "_selected": True,
                            "_icon": "icon-transition",
                            "id": "refId1740106540450",
                            "icon": "icon-transition",
                        },
                    ],
                    "transitions": [
                        {"name": "Confirm Number", "id": "5c73b5e87176db9eb5140a8d"}
                    ],
                    "objectType": "campaignstate",
                    "key": "start-state",
                    "_id": "start-state",
                    "description": "Begin State",
                    "name": "Begin State",
                    "location": "265.79713078124996 315.96619354980464",
                    "__gohashid": 2481,
                },
                "5c73b0b8071b1abb22a4a96d": {
                    "category": "Standard",
                    "campaignStateId": "5c73b0b8071b1abb22a4a96d",
                    "actions": [
                        {
                            "name": "Play Collect Google TTS",
                            "description": "Play Collect using Text-To-Speech",
                            "properties": {
                                "voiceName": "en-US-Wavenet-J",
                                "voiceGender": "male",
                                "text": '<prosody pitch="-2st">The phone number from which you are calling is <emphasis level="strong"><say-as interpret-as="verbatim">${workitem.data.callbackNumber}</say-as></emphasis>. To receive a call back on this number, press 1. To enter a different number, press 2. To return to the queue, press 3.</prosody>',
                                "numberDigits": 1,
                                "terminationKey": "#",
                                "timeoutInSeconds": "3",
                                "dlpOption": False,
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "description": "Play Collect using Text-To-Speech",
                            },
                            "type": "googlettscollect",
                            "_selected": True,
                            "id": "refId1740106541182",
                            "icon": "icon-tts",
                        },
                        {
                            "name": "Return To Workflow",
                            "properties": {
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.digits",
                                            "operator": "==",
                                            "rightExpression": "'3'",
                                        }
                                    ],
                                },
                                "description": "workitem.digits == '3'",
                            },
                            "type": "functionreturn",
                            "_selected": False,
                            "id": "refId1740106541183",
                            "icon": "icon-functionreturn",
                        },
                        {
                            "name": "Enter Number",
                            "description": "Go to Enter Number",
                            "properties": {
                                "stateId": "5c73b30f83d76227e78b95ac",
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
                                "name": "Transition",
                                "description": "workitem.digits == '2'",
                                "points": {
                                    "h": True,
                                    "r": [],
                                    "ct": 0,
                                    "__gohashid": 43879,
                                },
                            },
                            "type": "transition",
                            "transitionId": "5c73b7fe46ac3a6fe943b071",
                            "_selected": False,
                            "id": "refId1740106541184",
                            "icon": "icon-transition",
                        },
                        {
                            "name": "Exit Queue",
                            "properties": {
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
                                "description": "workitem.digits == '1'",
                            },
                            "type": "exitqueue",
                            "description": "Remove workitem from queue",
                            "_selected": False,
                            "id": "refId1740106541185",
                            "icon": "icon-exitqueues",
                        },
                        {
                            "name": "Callback From Expression",
                            "description": "Create Callback",
                            "properties": {
                                "description": "workitem.data.queueId",
                                "address": "workitem.data.callbackNumber",
                                "priority": 3,
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
                                "queueIdsExpression": "workitem.data.queueId",
                            },
                            "type": "acdcallbackfromexpression",
                            "_selected": False,
                            "id": "refId1740106541186",
                            "icon": "icon-callback",
                        },
                        {
                            "name": "Synthesize Text via Google TTS",
                            "description": "Convert Text into Audio using Google's Text-To-Speech",
                            "properties": {
                                "description": "Thank you... (workitem.digits == '1')",
                                "voiceName": "en-US-Wavenet-J",
                                "text": '<prosody pitch="-2st">Thank you for calling, and have a great day!</prosody>',
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
                            },
                            "type": "googletts",
                            "_selected": False,
                            "id": "refId1740106541187",
                            "icon": "icon-tts",
                        },
                        {
                            "name": "End State",
                            "description": "Transition to another state",
                            "properties": {
                                "description": "workitem.digits == '1'",
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
                                "stateName": "End State",
                            },
                            "type": "transitionbyname",
                            "_selected": False,
                            "transitionId": "refId1740106540183",
                            "id": "refId1740106541188",
                            "icon": "icon-transition",
                        },
                        {
                            "name": "Synthesize Text via Google TTS",
                            "description": "Convert Text into Audio using Google's Text-To-Speech",
                            "properties": {
                                "voiceName": "en-US-Wavenet-J",
                                "text": '<prosody pitch="-2st">The number you entered is invalid.</prosody>',
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "description": "The number you entered is invalid.",
                            },
                            "type": "googletts",
                            "_selected": False,
                            "id": "refId1740106541189",
                            "icon": "icon-tts",
                        },
                        {
                            "name": "Back to Top",
                            "description": "Transition to another state",
                            "properties": {
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "stateName": "Confirm Number",
                                "description": "Transition to another state",
                            },
                            "type": "transitionbyname",
                            "_selected": False,
                            "transitionId": "refId1740106540224",
                            "id": "refId1740106541190",
                            "icon": "icon-transition",
                        },
                    ],
                    "name": "Confirm Number",
                    "description": "Newly Created State",
                    "objectType": "campaignstate",
                    "_id": "5c73b0b8071b1abb22a4a96d",
                    "key": "5c73b0b8071b1abb22a4a96d",
                    "location": "550.590755005469 527.3958566683345",
                    "loc": "-371 -120",
                    "__gohashid": 6556,
                    "transitions": [
                        {"name": "Enter Number", "id": "5c73b7fe46ac3a6fe943b071"},
                        {"name": "End State", "id": "refId1740106540183"},
                        {"name": "Back to Top", "id": "refId1740106540224"},
                    ],
                },
                "5c73b30f83d76227e78b95ac": {
                    "category": "Standard",
                    "campaignStateId": "5c73b30f83d76227e78b95ac",
                    "actions": [
                        {
                            "name": "Play Collect Google TTS",
                            "description": "Play Collect using Text-To-Speech",
                            "properties": {
                                "description": "Please enter the 10-digit phone number...",
                                "voiceName": "en-US-Wavenet-J",
                                "voiceGender": "male",
                                "text": '<prosody pitch="-2st">Please enter the 10-digit phone number to which you would like to receive a call back. When you are finished, press the pound key.</prosody>',
                                "numberDigits": 10,
                                "terminationKey": "#",
                                "timeoutInSeconds": "10",
                                "dlpOption": False,
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                            },
                            "type": "googlettscollect",
                            "_selected": False,
                            "id": "refId1740106540675",
                            "icon": "icon-tts",
                        },
                        {
                            "icon": "icon-tts",
                            "name": "Synthesize Text via Google TTS",
                            "description": "Convert Text into Audio using Google's Text-To-Speech",
                            "properties": {
                                "description": "Sorry... (workitem.digits.length != 10)",
                                "voiceName": "en-US-Wavenet-J",
                                "text": '<prosody pitch="-2st">Sorry, but I need you to enter a valid 10-digit phone number, including the area code.</prosody>',
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.digits.length",
                                            "operator": "!=",
                                            "rightExpression": "10",
                                        }
                                    ],
                                },
                            },
                            "type": "googletts",
                            "_selected": False,
                        },
                        {
                            "name": "Back to Top",
                            "description": "Transition to another state",
                            "properties": {
                                "description": "workitem.digits.length != 10",
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.digits.length",
                                            "operator": "!=",
                                            "rightExpression": "10",
                                        }
                                    ],
                                },
                                "stateName": "Enter Number",
                            },
                            "type": "transitionbyname",
                            "_selected": False,
                            "transitionId": "refId1740106540260",
                            "id": "refId1740106540676",
                            "icon": "icon-transition",
                        },
                        {
                            "name": "Save Variable",
                            "description": "Save callback number",
                            "properties": {
                                "variableName": "callbackNumber",
                                "rightExpression": "workitem.digits",
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "description": "callbackNumber",
                                "asObject": True,
                            },
                            "type": "savevariable",
                            "_selected": False,
                            "id": "refId1740106540677",
                            "icon": "icon-save",
                        },
                        {
                            "name": "Confirm Number",
                            "description": "Transition to another state",
                            "properties": {
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "stateName": "Confirm Number",
                                "description": "Transition to another state",
                            },
                            "type": "transitionbyname",
                            "_selected": True,
                            "transitionId": "refId1740106540402",
                            "icon": "icon-transition",
                            "id": "refId1740106540678",
                        },
                    ],
                    "name": "Enter Number",
                    "description": "Newly Created State",
                    "objectType": "campaignstate",
                    "_id": "5c73b30f83d76227e78b95ac",
                    "key": "5c73b30f83d76227e78b95ac",
                    "location": "855.3347402125003 711.8236854064451",
                    "loc": "212 93",
                    "__gohashid": 7864,
                    "transitions": [
                        {"name": "Back to Top", "id": "refId1740106540260"},
                        {"name": "Confirm Number", "id": "refId1740106540402"},
                    ],
                },
            },
            "name": function_name,
        }
    )
    headers = {
        "Authorization": ncc_token,
        "Content-Type": "application/json",
    }
    try:
        conn.request("POST", "/data/api/types/function/", payload, headers)
        res = conn.getresponse()
        if res.status == 201:
            data = res.read().decode("utf-8")
            function = json.loads(data)
    except:
        pass
    conn.close()
    return function


def delete_function(ncc_location: str, ncc_token: str, function_id: str) -> bool:
    """
    This function deletes an NCC function with the specified function ID.
    """
    success = False
    conn = http.client.HTTPSConnection(ncc_location)
    payload = ""
    headers = {"Authorization": ncc_token}
    try:
        conn.request(
            "DELETE", f"/data/api/types/function/{function_id}", payload, headers
        )
        res = conn.getresponse()
        if res.status == 204:
            success = True
    except:
        pass
    conn.close()
    return success
