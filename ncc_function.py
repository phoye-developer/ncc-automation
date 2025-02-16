import http.client
import urllib.parse
import json
from config import *


def get_functions(ncc_location: str, ncc_token: str) -> list:
    """
    This function fetches a list of NCC functions present on the Nextiva Contact Center tenant.
    """
    functions = []
    conn = http.client.HTTPSConnection(ncc_location)
    payload = ""
    headers = {"Authorization": ncc_token}
    try:
        conn.request("GET", "/data/api/types/function?q=Test%20", payload, headers)
        res = conn.getresponse()
        if res.status == 200:
            data = res.read().decode("utf-8")
            json_data = json.loads(data)
            total = json_data["total"]
            if total > 0:
                results = json_data["objects"]
                for result in results:
                    function_name = result["name"]
                    if function_name[0:5] == "Test ":
                        functions.append(result)
    except:
        pass
    conn.close()
    return functions


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
                                "description": "InboundCall or InboundSMS",
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
                    "location": "-616.3333740234373 -655",
                    "transitions": [],
                    "__gohashid": 66405,
                },
                "start-state": {
                    "category": "Begin",
                    "campaignStateId": "start-state",
                    "actions": [
                        {
                            "name": "To Wait for Message",
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
                            "id": "refId1702415443173",
                            "icon": "icon-transition",
                        }
                    ],
                    "transitions": [
                        {
                            "name": "To Wait for Message",
                            "id": "refId1630518553842",
                            "__gohashid": 13172,
                        }
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
                    "name": "Handle User Messages",
                    "description": "Newly Created State",
                    "actions": [
                        {
                            "name": "Forward to consumer",
                            "description": "Forward chat message to consumer",
                            "properties": {
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "description": "Forward chat message to consumer",
                            },
                            "type": "chatforwardconsumer",
                            "_selected": True,
                            "id": "refId1678901939403",
                            "icon": "icon-chat-forward-consumer",
                        },
                        {
                            "name": "Transition - Wait Messages",
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
                            "_selected": False,
                            "transitionId": "refId1630518553991",
                            "id": "refId1678901939404",
                            "icon": "icon-transition",
                        },
                    ],
                    "_id": "612ff3bd59517fb2d65d306b",
                    "key": "612ff3bd59517fb2d65d306b",
                    "location": "50.68510709065231 -258.93826994112607",
                    "transitions": [
                        {
                            "name": "Transition - Wait Messages",
                            "id": "refId1630518553991",
                            "__gohashid": 13218,
                        }
                    ],
                    "__gohashid": 66409,
                },
                "612ff3c80832633212b10106": {
                    "category": "Standard",
                    "objectType": "campaignstate",
                    "campaignStateId": "612ff3c80832633212b10106",
                    "name": "Handle Customer Messages",
                    "description": "Newly Created State",
                    "actions": [
                        {
                            "name": "Forward to agent",
                            "description": "Forward chat message to agent",
                            "properties": {
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "description": "Forward chat message to agent",
                            },
                            "type": "chatforwardagent",
                            "_selected": False,
                            "id": "refId1655733056662",
                            "icon": "icon-chat-forward-agent",
                        },
                        {
                            "name": "Transition - Wait Messages",
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
                            "transitionId": "refId1630518554009",
                            "id": "refId1655733056663",
                            "icon": "icon-transition",
                        },
                    ],
                    "_id": "612ff3c80832633212b10106",
                    "key": "612ff3c80832633212b10106",
                    "location": "-227.9815188859102 -108.53824069969977",
                    "transitions": [
                        {
                            "name": "Transition - Wait Messages",
                            "id": "refId1630518554009",
                            "__gohashid": 13264,
                        }
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
                            "icon": "icon-timer",
                            "name": "Wait Chat Message",
                            "description": "",
                            "properties": {
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                }
                            },
                            "type": "waitforchatmessage",
                            "_selected": True,
                        },
                        {
                            "name": "Transition - User Messages",
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
                            "id": "refId1678901939383",
                            "transitionId": "refId1655733056505",
                            "icon": "icon-transition",
                        },
                        {
                            "name": "Transition - Customer Messages",
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
                            "_selected": False,
                            "transitionId": "refId1655733056506",
                            "id": "refId1678901939384",
                            "icon": "icon-transition",
                        },
                    ],
                    "_id": "62b08f28e945230cb5347c5b",
                    "key": "62b08f28e945230cb5347c5b",
                    "location": "-426.9883614959492 -364.3766170225258",
                    "transitions": [
                        {
                            "name": "Transition - User Messages",
                            "id": "refId1655733056505",
                            "__gohashid": 13310,
                        },
                        {
                            "name": "Transition - Customer Messages",
                            "id": "refId1655733056506",
                            "__gohashid": 13315,
                        },
                    ],
                    "__gohashid": 2780,
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
                "name": {"en": {"language": "en", "value": function_name}}
            },
            "name": function_name,
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
                    "location": "18.313131530711985 675.3981425236382",
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
                            "id": "refId1723573943893",
                            "icon": "icon-clock",
                        },
                        {
                            "name": "Save Variable",
                            "description": "",
                            "properties": {
                                "description": "queueId - workitem.queues",
                                "rightExpression": "workitem.queues",
                                "variableName": "queueId",
                                "asObject": False,
                                "dlpOption": False,
                                "wfmOption": False,
                                "dashboard": False,
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "'queueId' in workitem.data",
                                            "operator": "==",
                                            "rightExpression": "false",
                                        },
                                        {
                                            "leftExpression": "'queues'  in workitem",
                                            "operator": "==",
                                            "rightExpression": "true",
                                        },
                                    ],
                                },
                            },
                            "type": "savevariable",
                            "_selected": True,
                            "id": "refId1723573943894",
                            "icon": "icon-save",
                        },
                        {
                            "name": "Exit Queue",
                            "description": "Remove workitem from queue",
                            "properties": {
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "description": "Remove workitem from queue",
                            },
                            "type": "exitqueue",
                            "_selected": False,
                            "id": "refId1723573943895",
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
                                "description": "Set messageRecorded = 0",
                                "asObject": True,
                            },
                            "type": "savevariable",
                            "_selected": False,
                            "id": "refId1723573943896",
                            "icon": "icon-save",
                        },
                        {
                            "name": "Transition - Record VM",
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
                                    "__gohashid": 8249,
                                    "_isFrozen": True,
                                    "s": [
                                        {
                                            "x": -785.9999999999999,
                                            "y": 121.43979496706925,
                                            "_isFrozen": True,
                                        },
                                        {
                                            "x": -775.9999999999999,
                                            "y": 121.43979496706925,
                                            "_isFrozen": True,
                                        },
                                        {
                                            "x": -652.4756306329477,
                                            "y": 121.43979496706925,
                                            "_isFrozen": True,
                                        },
                                        {
                                            "x": -652.4756306329477,
                                            "y": 135.10859965070503,
                                            "_isFrozen": True,
                                        },
                                        {
                                            "x": -652.4756306329477,
                                            "y": 148.77740433434082,
                                            "_isFrozen": True,
                                        },
                                        {
                                            "x": -652.4756306329477,
                                            "y": 158.77740433434082,
                                            "_isFrozen": True,
                                        },
                                    ],
                                    "Ja": 6,
                                },
                            },
                            "transitionId": "5dc4023452d09c4fc8369c19",
                            "_selected": False,
                            "id": "refId1723573943897",
                            "icon": "icon-transition",
                        },
                    ],
                    "transitions": [
                        {
                            "name": "Transition - Record VM",
                            "id": "5dc4023452d09c4fc8369c19",
                        }
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
                            "name": "Play Prompt",
                            "description": "",
                            "properties": {
                                "description": "Please leave your voicemail after the tone",
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "loop": 1,
                                "promptId": "599d70ddee2f2566c4321477",
                                "_working": False,
                                "expansions": {"promptId": {"name": "8630"}},
                            },
                            "type": "playprompt",
                            "_selected": False,
                            "id": "refId1655475277111",
                            "icon": "icon-playprompt",
                        },
                        {
                            "name": "Recording",
                            "description": "",
                            "properties": {
                                "description": "Start Recording with Beep",
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
                            "id": "refId1655475277112",
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
                                "description": "set messageRecorded = 1",
                                "asObject": True,
                            },
                            "type": "savevariable",
                            "_selected": True,
                            "id": "refId1655475277172",
                            "icon": "icon-savevariable",
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
                            "id": "refId1655475277143",
                            "icon": "icon-starttimer",
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
                                "description": "Set retries = 1",
                                "asObject": True,
                            },
                            "type": "savevariable",
                            "_selected": False,
                            "id": "refId1655475277115",
                            "icon": "icon-savevariable",
                        },
                        {
                            "name": "Transition - Options Menu",
                            "description": "Transition to another state",
                            "properties": {
                                "description": "goto options",
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "stateId": "5dc40291e680339a6aecc831",
                                "name": "Transition",
                            },
                            "type": "transition",
                            "_selected": False,
                            "transitionId": "refId1573126598874",
                            "id": "refId1655475277116",
                            "icon": "icon-transition",
                        },
                    ],
                    "name": "Record VM",
                    "description": "Newly Created State",
                    "objectType": "campaignstate",
                    "_id": "5dc401fe07b302d7a780e761",
                    "key": "5dc401fe07b302d7a780e761",
                    "location": "-652.4756306329476 223.16141083458496",
                    "loc": "200.03145361646278 -52.4453125",
                    "__gohashid": 4074,
                    "transitions": [
                        {
                            "name": "Transition - Options Menu",
                            "id": "refId1573126598874",
                        }
                    ],
                },
                "5dc40291e680339a6aecc831": {
                    "category": "Standard",
                    "campaignStateId": "5dc40291e680339a6aecc831",
                    "actions": [
                        {
                            "name": "Play & Collect Digits",
                            "description": "",
                            "properties": {
                                "description": "To save your message, press 1, to hear your message, press 2, to re-record your message, press 3, to cancel your message, press star.",
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "loop": 1,
                                "numberDigits": 1,
                                "promptId": "599d7152ee2f2566c4321478",
                                "terminationKey": "#",
                                "timeoutInSeconds": "7",
                                "_working": False,
                                "expansions": {"promptId": {"name": "8631"}},
                            },
                            "type": "playdigits",
                            "_selected": False,
                            "id": "refId1655475276883",
                            "icon": "icon-playdigits",
                        },
                        {
                            "name": "Play Recording",
                            "description": "",
                            "properties": {
                                "description": "DIGITS - TWO - Hear Message",
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
                            "id": "refId1655475276884",
                            "icon": "icon-playrecording",
                        },
                        {
                            "name": "Transition - Options Menu",
                            "description": "Transition to another state",
                            "properties": {
                                "description": "SELECT 2 - goto options",
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
                                "stateId": "5dc40291e680339a6aecc831",
                                "name": "Transition",
                            },
                            "type": "transition",
                            "_selected": True,
                            "transitionId": "refId1573126598778",
                            "id": "refId1655475276885",
                            "icon": "icon-transition",
                        },
                        {
                            "name": "Save Variable",
                            "description": "",
                            "properties": {
                                "description": "Set messageRecorded = 0",
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
                            "id": "refId1655475276886",
                            "icon": "icon-savevariable",
                        },
                        {
                            "name": "Transition - Record VM",
                            "description": "Transition to another state",
                            "properties": {
                                "description": "SELECT 3 - goto record",
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
                                "stateId": "5dc401fe07b302d7a780e761",
                                "name": "Transition",
                            },
                            "type": "transition",
                            "_selected": False,
                            "transitionId": "refId1573126598787",
                            "id": "refId1655475276887",
                            "icon": "icon-transition",
                        },
                        {
                            "name": "Transition - Create VM",
                            "description": "Transition to another state",
                            "properties": {
                                "description": "SELECT 1 - create ACD VM",
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
                            },
                            "type": "transition",
                            "_selected": False,
                            "transitionId": "refId1573126598797",
                            "id": "refId1655475276888",
                            "icon": "icon-transition",
                        },
                        {
                            "name": "Return To Workflow",
                            "description": "",
                            "properties": {
                                "description": "SELECT * - return to workflow",
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
                            "id": "refId1655475276889",
                            "icon": "icon-functionreturn",
                        },
                        {
                            "name": "Transition - Options Menu",
                            "description": "Transition to another state",
                            "properties": {
                                "description": "If Invalid Option Loop",
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "stateId": "5dc40291e680339a6aecc831",
                            },
                            "type": "transition",
                            "_selected": False,
                            "transitionId": "refId1585421559053",
                            "icon": "icon-transition",
                            "id": "refId1655475276890",
                        },
                    ],
                    "name": "Options Menu",
                    "description": "Newly Created State",
                    "objectType": "campaignstate",
                    "_id": "5dc40291e680339a6aecc831",
                    "key": "5dc40291e680339a6aecc831",
                    "location": "-433.1248747227851 409.75422566702383",
                    "loc": "165.03145361646278 67.5546875",
                    "__gohashid": 8936,
                    "transitions": [
                        {
                            "name": "Transition - Options Menu",
                            "id": "refId1573126598778",
                        },
                        {"name": "Transition - Record VM", "id": "refId1573126598787"},
                        {"name": "Transition - Create VM", "id": "refId1573126598797"},
                        {
                            "name": "Transition - Options Menu",
                            "id": "refId1585421559053",
                        },
                    ],
                },
                "5dc40521e22562777dcb2007": {
                    "category": "Standard",
                    "campaignStateId": "5dc40521e22562777dcb2007",
                    "actions": [
                        {
                            "name": "Play Prompt",
                            "description": "",
                            "properties": {
                                "description": "thanks for calling",
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "loop": 1,
                                "promptId": "59567ffda798c90678770d66",
                                "_working": False,
                                "expansions": {"promptId": {"name": "4091"}},
                            },
                            "type": "playprompt",
                            "_selected": False,
                            "id": "refId1727322591514",
                            "icon": "icon-playprompt",
                        },
                        {
                            "name": "Save Variable",
                            "description": "",
                            "properties": {
                                "description": "Set messageRecorded = 0",
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
                            "id": "refId1727322591515",
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
                            "_selected": True,
                            "icon": "icon-directconnect",
                            "id": "refId1727322591516",
                        },
                        {
                            "name": "Transition - End State",
                            "description": "Transition to another state",
                            "properties": {
                                "description": "Terminate",
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "stateId": "5dc401ec494df97002ea2b57",
                                "name": "Transition",
                            },
                            "type": "transition",
                            "_selected": False,
                            "transitionId": "refId1573126598835",
                            "id": "refId1727322591517",
                            "icon": "icon-transition",
                        },
                    ],
                    "name": "Create ACD VM",
                    "description": "Newly Created State",
                    "objectType": "campaignstate",
                    "_id": "5dc40521e22562777dcb2007",
                    "key": "5dc40521e22562777dcb2007",
                    "location": "-201.86401092256142 579.0405190011794",
                    "loc": "213.03145361646278 459.0546875",
                    "__gohashid": 62107,
                    "transitions": [
                        {"name": "Transition - End State", "id": "refId1573126598835"}
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
                "name": {"en": {"language": "en", "value": function_name}}
            },
            "name": function_name,
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
                    "location": "519 663.6666564941406",
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
                                "description": "Store Customer's phone number",
                                "asObject": True,
                            },
                            "type": "savevariable",
                            "_selected": False,
                            "_icon": "icon-savevariable",
                            "id": "refId1723573943857",
                            "icon": "icon-save",
                        },
                        {
                            "name": "Save Variable",
                            "properties": {
                                "variableName": "queueId",
                                "rightExpression": "workitem.queues",
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "'queueId' in workitem.data",
                                            "operator": "==",
                                            "rightExpression": "false",
                                        },
                                        {
                                            "leftExpression": "'queues' in workitem",
                                            "operator": "==",
                                            "rightExpression": "true",
                                        },
                                    ],
                                },
                                "description": "queueId - workitem.queues",
                                "asObject": False,
                            },
                            "type": "savevariable",
                            "_selected": True,
                            "_icon": "icon-savevariable",
                            "id": "refId1723573943858",
                            "icon": "icon-save",
                        },
                        {
                            "name": "Transition - Confirm Number",
                            "properties": {
                                "stateId": "5c73b0b8071b1abb22a4a96d",
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [],
                                },
                                "name": "Transition",
                                "description": "Transition to another state",
                                "points": {
                                    "__gohashid": 5725,
                                    "_isFrozen": True,
                                    "s": [
                                        {
                                            "x": 389,
                                            "y": 339.55067825317377,
                                            "_isFrozen": True,
                                        },
                                        {
                                            "x": 399,
                                            "y": 339.55067825317377,
                                            "_isFrozen": True,
                                        },
                                        {
                                            "x": 396,
                                            "y": 339.55067825317377,
                                            "_isFrozen": True,
                                        },
                                        {
                                            "x": 396,
                                            "y": 339.55067825317377,
                                            "_isFrozen": True,
                                        },
                                        {
                                            "x": 526,
                                            "y": 339.55067825317377,
                                            "_isFrozen": True,
                                        },
                                        {
                                            "x": 526,
                                            "y": 360.80209443918415,
                                            "_isFrozen": True,
                                        },
                                        {
                                            "x": 526,
                                            "y": 370.80209443918415,
                                            "_isFrozen": True,
                                        },
                                    ],
                                    "Ja": 7,
                                },
                            },
                            "type": "transition",
                            "transitionId": "5c73b5e87176db9eb5140a8d",
                            "description": "Transition to confirm number",
                            "_selected": False,
                            "_icon": "icon-transition",
                            "id": "refId1723573943859",
                            "icon": "icon-transition",
                        },
                    ],
                    "transitions": [
                        {
                            "name": "Transition - Confirm Number",
                            "id": "5c73b5e87176db9eb5140a8d",
                            "__gohashid": 11800,
                        }
                    ],
                    "objectType": "campaignstate",
                    "key": "start-state",
                    "_id": "start-state",
                    "description": "Begin State",
                    "name": "Begin State",
                    "location": "306 322.66667175292963",
                    "__gohashid": 2481,
                },
                "5c73b0b8071b1abb22a4a96d": {
                    "category": "Standard",
                    "campaignStateId": "5c73b0b8071b1abb22a4a96d",
                    "actions": [
                        {
                            "name": "Play Prompt",
                            "description": "Here's the number I have to call you",
                            "properties": {
                                "promptId": "59567ffda798c90678770d90",
                                "loop": 1,
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "_working": False,
                                "expansions": {"promptId": {"name": "5039"}},
                                "description": "The number I have for you is:",
                            },
                            "type": "playprompt",
                            "_selected": False,
                            "id": "refId1723573611949",
                            "icon": "icon-playprompt",
                        },
                        {
                            "name": "PLAY NUMBER",
                            "description": "Play callback number ",
                            "properties": {
                                "number": "workitem.data.callbackNumber",
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "description": "Play Number, one digit at a time.",
                            },
                            "type": "playnumber",
                            "_selected": False,
                            "id": "refId1723573611950",
                            "icon": "icon-play-number",
                        },
                        {
                            "name": "Play & Collect Digits",
                            "description": "If correct, press one. If not, press 2.",
                            "properties": {
                                "promptId": "59567ffda798c90678770d91",
                                "loop": 1,
                                "numberDigits": 1,
                                "terminationKey": "#",
                                "timeoutInSeconds": "5",
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "_working": False,
                                "expansions": {"promptId": {"name": "5040"}},
                                "description": "Press 1 to accept or 2 to re-enter",
                            },
                            "type": "playdigits",
                            "_selected": False,
                            "id": "refId1723573611951",
                            "icon": "icon-playdigits",
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
                                }
                            },
                            "type": "functionreturn",
                            "_selected": False,
                            "id": "refId1723573611952",
                            "icon": "icon-functionreturn",
                        },
                        {
                            "name": "Transition - Enter Number",
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
                                "description": "Transition to another state",
                                "points": {
                                    "__gohashid": 4866,
                                    "_isFrozen": True,
                                    "s": [
                                        {
                                            "x": 609,
                                            "y": 471.70213868967244,
                                            "_isFrozen": True,
                                        },
                                        {
                                            "x": 619,
                                            "y": 471.70213868967244,
                                            "_isFrozen": True,
                                        },
                                        {
                                            "x": 620,
                                            "y": 471.70213868967244,
                                            "_isFrozen": True,
                                        },
                                        {
                                            "x": 620,
                                            "y": 471.70213868967244,
                                            "_isFrozen": True,
                                        },
                                        {
                                            "x": 751.0000000000002,
                                            "y": 471.70213868967244,
                                            "_isFrozen": True,
                                        },
                                        {
                                            "x": 751.0000000000002,
                                            "y": 589.5048637390134,
                                            "_isFrozen": True,
                                        },
                                        {
                                            "x": 751.0000000000002,
                                            "y": 599.5048637390134,
                                            "_isFrozen": True,
                                        },
                                    ],
                                    "Ja": 7,
                                },
                            },
                            "type": "transition",
                            "transitionId": "5c73b7fe46ac3a6fe943b071",
                            "_selected": False,
                            "id": "refId1723573611953",
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
                                "description": "Remove workitem from queue",
                            },
                            "type": "exitqueue",
                            "description": "Remove workitem from queue",
                            "_selected": False,
                            "id": "refId1723573611955",
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
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "queueIdsExpression": "workitem.data.queueId",
                            },
                            "type": "acdcallbackfromexpression",
                            "_selected": False,
                            "id": "refId1723573611956",
                            "icon": "icon-callback",
                        },
                        {
                            "name": "Play Prompt",
                            "description": "Thank you goodbye",
                            "properties": {
                                "promptId": "59567ffda798c90678770d66",
                                "loop": 1,
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
                                "_working": False,
                                "expansions": {"promptId": {"name": "4091"}},
                            },
                            "type": "playprompt",
                            "_selected": False,
                            "id": "refId1723573611957",
                            "icon": "icon-playprompt",
                        },
                        {
                            "name": "Transition - End State",
                            "properties": {
                                "stateId": "5c73b01813488773a0fd8999",
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
                                "name": "Transition",
                                "description": "If pressed 1",
                                "points": {
                                    "__gohashid": 4867,
                                    "_isFrozen": True,
                                    "s": [
                                        {
                                            "x": 609,
                                            "y": 515.7021386896724,
                                            "_isFrozen": True,
                                        },
                                        {
                                            "x": 619,
                                            "y": 515.7021386896724,
                                            "_isFrozen": True,
                                        },
                                        {
                                            "x": 619,
                                            "y": 515.7021386896724,
                                            "_isFrozen": True,
                                        },
                                        {
                                            "x": 619,
                                            "y": 630.8506408691406,
                                            "_isFrozen": True,
                                        },
                                        {
                                            "x": 519,
                                            "y": 630.8506408691406,
                                            "_isFrozen": True,
                                        },
                                        {
                                            "x": 519,
                                            "y": 640.8506408691406,
                                            "_isFrozen": True,
                                        },
                                    ],
                                    "Ja": 6,
                                },
                            },
                            "type": "transition",
                            "transitionId": "5c7874ea7c4290d731f50ccd",
                            "description": "Transition to another state",
                            "_selected": False,
                            "id": "refId1723573611958",
                            "icon": "icon-transition",
                        },
                        {
                            "name": "Play Prompt",
                            "description": "The number you entered is invalid",
                            "properties": {
                                "promptId": "59567ffda798c90678770e77",
                                "loop": 1,
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "_working": False,
                                "expansions": {"promptId": {"name": "8604"}},
                            },
                            "type": "playprompt",
                            "_selected": False,
                            "id": "refId1723573611959",
                            "icon": "icon-playprompt",
                        },
                        {
                            "name": "Transition - Confirm Number",
                            "description": "Start over",
                            "properties": {
                                "stateId": "5c73b0b8071b1abb22a4a96d",
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "name": "Transition",
                                "description": "Transition to another state",
                                "points": {
                                    "__gohashid": 4868,
                                    "_isFrozen": True,
                                    "s": [
                                        {
                                            "x": 609,
                                            "y": 559.7021386896724,
                                            "_isFrozen": True,
                                        },
                                        {
                                            "x": 619,
                                            "y": 559.7021386896724,
                                            "_isFrozen": True,
                                        },
                                        {
                                            "x": 642.261423749154,
                                            "y": 559.7021386896724,
                                            "_isFrozen": True,
                                        },
                                        {
                                            "x": 642.261423749154,
                                            "y": 360.80209443918415,
                                            "_isFrozen": True,
                                        },
                                        {
                                            "x": 526,
                                            "y": 360.80209443918415,
                                            "_isFrozen": True,
                                        },
                                        {
                                            "x": 526,
                                            "y": 370.80209443918415,
                                            "_isFrozen": True,
                                        },
                                    ],
                                    "Ja": 6,
                                },
                            },
                            "type": "transition",
                            "transitionId": "5c827d0ee8796c5c7deebaa1",
                            "_selected": False,
                            "id": "refId1723573611960",
                            "icon": "icon-transition",
                        },
                    ],
                    "name": "Confirm Number State",
                    "description": "Newly Created State",
                    "objectType": "campaignstate",
                    "_id": "5c73b0b8071b1abb22a4a96d",
                    "key": "5c73b0b8071b1abb22a4a96d",
                    "location": "526 489.0021165644283",
                    "loc": "-371 -120",
                    "__gohashid": 6556,
                    "transitions": [
                        {
                            "name": "Transition - Enter Number",
                            "id": "5c73b7fe46ac3a6fe943b071",
                            "__gohashid": 11846,
                        },
                        {
                            "name": "Transition - End State",
                            "id": "5c7874ea7c4290d731f50ccd",
                            "__gohashid": 11851,
                        },
                        {
                            "name": "Transition - Confirm Number",
                            "id": "5c827d0ee8796c5c7deebaa1",
                            "__gohashid": 11856,
                        },
                    ],
                },
                "5c73b30f83d76227e78b95ac": {
                    "category": "Standard",
                    "campaignStateId": "5c73b30f83d76227e78b95ac",
                    "actions": [
                        {
                            "name": "Play & Collect Digits",
                            "description": "Type your phone number including area code followed by the pound key",
                            "properties": {
                                "promptId": "59567ffda798c90678770e9d",
                                "loop": 1,
                                "numberDigits": 12,
                                "terminationKey": "#",
                                "timeoutInSeconds": "10",
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "_working": False,
                                "expansions": {"promptId": {"name": "9012"}},
                                "description": "Enter the phone number for the callback",
                            },
                            "type": "playdigits",
                            "_selected": False,
                            "id": "refId1655829864328",
                            "icon": "icon-playdigits",
                        },
                        {
                            "name": "Transition - Enter Number",
                            "properties": {
                                "stateId": "5c73b30f83d76227e78b95ac",
                                "condition": {
                                    "conditionType": "AND",
                                    "expressions": [
                                        {
                                            "leftExpression": "workitem.digits.length",
                                            "operator": "<",
                                            "rightExpression": "10",
                                        }
                                    ],
                                },
                                "name": "Transition",
                                "description": "Transition to another state",
                            },
                            "type": "transition",
                            "transitionId": "5c73b4a27505c3cbc32fd523",
                            "description": "Transition to another state",
                            "_selected": False,
                            "id": "refId1655829864329",
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
                                "description": "Store Callback Number",
                                "asObject": True,
                            },
                            "type": "savevariable",
                            "_selected": True,
                            "id": "refId1655829864330",
                            "icon": "icon-savevariable",
                        },
                        {
                            "name": "Transition - Confirm Number",
                            "description": "Confitrm Number",
                            "properties": {
                                "stateId": "5c73b0b8071b1abb22a4a96d",
                                "condition": {
                                    "conditionType": "NONE",
                                    "expressions": [{"operator": "=="}],
                                },
                                "name": "Transition",
                                "description": "Transition to another state",
                            },
                            "type": "transition",
                            "transitionId": "5c73b4a2ed4d2329191dd2ad",
                            "_selected": False,
                            "id": "refId1655829864331",
                            "icon": "icon-transition",
                        },
                    ],
                    "name": "Enter Number State",
                    "description": "Newly Created State",
                    "objectType": "campaignstate",
                    "_id": "5c73b30f83d76227e78b95ac",
                    "key": "5c73b30f83d76227e78b95ac",
                    "location": "751.0000000000002 685.8888702392576",
                    "loc": "212 93",
                    "__gohashid": 7864,
                    "transitions": [
                        {
                            "name": "Transition - Enter Number",
                            "id": "5c73b4a27505c3cbc32fd523",
                            "__gohashid": 11902,
                        },
                        {
                            "name": "Transition - Confirm Number",
                            "id": "5c73b4a2ed4d2329191dd2ad",
                            "__gohashid": 11907,
                        },
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
