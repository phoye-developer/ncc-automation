import http.client
import urllib.parse
import json


def get_survey(ncc_location: str, ncc_token: str, survey_id: str) -> list:
    """
    This function fetches the details of a survey present on the Nextiva Contact Center (NCC) tenant.
    """
    survey = {}
    conn = http.client.HTTPSConnection(ncc_location)
    payload = ""
    headers = {"Authorization": ncc_token}
    try:
        conn.request("GET", f"/data/api/types/survey/{survey_id}", payload, headers)
        res = conn.getresponse()
        if res.status == 200:
            data = res.read().decode("utf-8")
            survey = json.loads(data)
    except:
        pass
    conn.close()
    return survey


def search_surveys(ncc_location: str, ncc_token: str, survey_name: str) -> dict:
    """
    This function searches for an existing survey with the same name as the intended new survey.
    """
    survey = {}
    conn = http.client.HTTPSConnection(ncc_location)
    payload = ""
    headers = {"Authorization": ncc_token}
    url_encoded_name = urllib.parse.quote(survey_name)
    try:
        conn.request(
            "GET",
            f"/data/api/types/survey?q={url_encoded_name}",
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
                    if result["name"] == survey_name:
                        survey = result
                        break
    except:
        pass
    conn.close()
    return survey


def search_campaign_surveys(
    ncc_location: str, ncc_token: str, campaign_name: str
) -> dict:
    """
    This function searches for existing surveys in Nextiva Contact Center (NCC) whose name begins with the specified campaign name.
    """
    surveys = []
    conn = http.client.HTTPSConnection(ncc_location)
    payload = ""
    headers = {"Authorization": ncc_token}
    url_encoded_name = urllib.parse.quote(campaign_name)
    try:
        conn.request(
            "GET",
            f"/data/api/types/survey?q={url_encoded_name}",
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
                        surveys.append(result)
    except:
        pass
    conn.close()
    return surveys


def create_survey(
    ncc_location: str,
    ncc_token: str,
    survey_name: str,
    survey_body: dict,
    survey_theme: dict,
) -> dict:
    """
    This function creates a survey with a specified name.
    """
    survey = {}
    conn = http.client.HTTPSConnection(ncc_location)
    survey_body["localizations"]["name"]["en"]["value"] = survey_name
    survey_body["surveythemeId"] = survey_theme["_id"]
    survey_body["expansions"]["surveythemeId"]["localizations"]["name"]["en"][
        "value"
    ] = survey_theme["name"]
    payload = json.dumps(survey_body)
    headers = {
        "Authorization": ncc_token,
        "Content-Type": "application/json",
    }
    try:
        conn.request("POST", "/data/api/types/survey/", payload, headers)
        res = conn.getresponse()
        if res.status == 201:
            data = res.read().decode("utf-8")
            survey = json.loads(data)
    except:
        pass
    conn.close()
    return survey


def create_user_survey(
    ncc_location: str,
    ncc_token: str,
    survey_name: str,
    survey_categories: list,
    survey_theme: dict,
) -> dict:
    """
    This function creates a survey with a specified name.
    """
    survey = {}
    conn = http.client.HTTPSConnection(ncc_location)
    payload = json.dumps(
        {
            "hideSurveyBoxShadown": False,
            "type": "full",
            "showFooter": False,
            "surveythemeId": survey_theme["_id"],
            "showTabs": True,
            "expansions": {
                "surveythemeId": {
                    "localizations": {
                        "name": {
                            "en": {"language": "en", "value": survey_theme["name"]}
                        }
                    }
                }
            },
            "showBottomNavigatorPage": False,
            "height": 700,
            "debug": False,
            "localizations": {"name": {"en": {"language": "en", "value": survey_name}}},
            "showHeader": False,
            "allowTabinationMandatoryFields": True,
            "entryPanelId": "66c540d6a14be123ae577468",
            "layout": {
                "elements": [
                    {
                        "icon": "icon-survey",
                        "name": "Panel",
                        "description": "Basic component to display content in a survey",
                        "type": "panel",
                        "component": "panel",
                        "elements": [
                            {
                                "icon": "icon-ui-text",
                                "name": "Text",
                                "description": "Displays direct text to the customer",
                                "type": "label",
                                "component": "label",
                                "elements": [],
                                "properties": {
                                    "label": "Contact Info",
                                    "fontSize": 20,
                                    "width": "100%",
                                    "margin": "10px 10px 0px 10px",
                                    "alignment": "left",
                                },
                                "_id": "66c6d1673427fd785dfc98ae",
                                "selected": False,
                                "show": True,
                            },
                            {
                                "icon": "icon-survey",
                                "name": "Panel",
                                "description": "Basic component to display content in a survey",
                                "type": "panel",
                                "component": "panel",
                                "elements": [
                                    {
                                        "icon": "icon-survey",
                                        "name": "Panel",
                                        "description": "Basic component to display content in a survey",
                                        "type": "panel",
                                        "component": "panel",
                                        "elements": [
                                            {
                                                "icon": "icon-ui-input",
                                                "name": "Input",
                                                "description": "A box for the customer to enter information",
                                                "type": "input",
                                                "component": "input",
                                                "elements": [],
                                                "properties": {
                                                    "label": "First Name",
                                                    "labelInReport": "firstName",
                                                    "fontSize": 16,
                                                    "width": "100%",
                                                    "fieldname": "firstName",
                                                    "defaultValue": '${workitem.contact?.firstName || ""}',
                                                    "mandatory": False,
                                                    "readOnly": False,
                                                    "validateOnInput": False,
                                                    "sensitiveData": False,
                                                    "saveToLocalStorage": False,
                                                },
                                                "_id": "66c6c8057e27eb6683f02546",
                                                "selected": False,
                                                "show": True,
                                            }
                                        ],
                                        "properties": {
                                            "label": "",
                                            "labelAlignment": "center",
                                            "labelFontSize": "24",
                                            "descriptionAlignment": "left",
                                            "descriptionFontSize": "24",
                                            "tabLabel": "First Name",
                                            "alignment": "center",
                                            "canCollapse": False,
                                            "state": False,
                                            "scroll": False,
                                            "showScrollbar": False,
                                            "vertical": "full",
                                            "direction": "column",
                                            "width": "100%",
                                            "margin": "10px 4px 4px 10px",
                                            "panelShadow": False,
                                            "showOverlay": False,
                                            "showHeader": False,
                                            "allowPanelInDashboard": False,
                                        },
                                        "_id": "66c6c7d76222b158d78bc27d",
                                        "selected": False,
                                        "show": True,
                                    },
                                    {
                                        "icon": "icon-survey",
                                        "name": "Panel",
                                        "description": "Basic component to display content in a survey",
                                        "type": "panel",
                                        "component": "panel",
                                        "elements": [
                                            {
                                                "icon": "icon-ui-input",
                                                "name": "Input",
                                                "description": "A box for the customer to enter information",
                                                "type": "input",
                                                "component": "input",
                                                "elements": [],
                                                "properties": {
                                                    "label": "Last Name",
                                                    "labelInReport": "lastName",
                                                    "fontSize": 16,
                                                    "width": "100%",
                                                    "fieldname": "lastName",
                                                    "defaultValue": '${workitem.contact?.lastName || ""}',
                                                    "mandatory": False,
                                                    "readOnly": False,
                                                    "validateOnInput": False,
                                                    "sensitiveData": False,
                                                    "saveToLocalStorage": False,
                                                },
                                                "_id": "66c6c84621c6ba30400e9d8c",
                                                "selected": False,
                                                "show": True,
                                            }
                                        ],
                                        "properties": {
                                            "label": "",
                                            "labelAlignment": "center",
                                            "labelFontSize": "24",
                                            "descriptionAlignment": "left",
                                            "descriptionFontSize": "24",
                                            "tabLabel": "Last Name",
                                            "alignment": "center",
                                            "canCollapse": False,
                                            "state": False,
                                            "scroll": False,
                                            "showScrollbar": False,
                                            "vertical": "full",
                                            "direction": "column",
                                            "width": "100%",
                                            "margin": "10px 10px 4px 4px",
                                            "panelShadow": False,
                                            "showOverlay": False,
                                            "showHeader": False,
                                            "allowPanelInDashboard": False,
                                        },
                                        "_id": "66c6c7f5e514d687d7234f30",
                                        "selected": False,
                                        "show": True,
                                    },
                                ],
                                "properties": {
                                    "label": "",
                                    "labelAlignment": "left",
                                    "labelFontSize": 20,
                                    "descriptionAlignment": "left",
                                    "descriptionFontSize": "24",
                                    "tabLabel": "Name",
                                    "alignment": "left",
                                    "canCollapse": False,
                                    "state": False,
                                    "scroll": False,
                                    "showScrollbar": False,
                                    "vertical": "fit",
                                    "direction": "row",
                                    "width": "100%",
                                    "panelShadow": False,
                                    "showOverlay": False,
                                    "showHeader": False,
                                    "allowPanelInDashboard": False,
                                },
                                "_id": "66c6c7b873f2a34fd26a73bf",
                                "selected": False,
                                "show": True,
                            },
                            {
                                "icon": "icon-ui-text",
                                "name": "Text",
                                "description": "Displays direct text to the customer",
                                "type": "label",
                                "component": "label",
                                "elements": [],
                                "properties": {
                                    "label": "Workitem Info",
                                    "fontSize": 20,
                                    "width": "100%",
                                    "margin": "20px 10px 0px 10px",
                                    "alignment": "left",
                                },
                                "_id": "66c6e5a8ab42181be0f9e5de",
                                "selected": False,
                                "show": True,
                            },
                            {
                                "icon": "icon-survey",
                                "name": "Panel",
                                "description": "Basic component to display content in a survey",
                                "type": "panel",
                                "component": "panel",
                                "elements": [
                                    {
                                        "icon": "icon-survey",
                                        "name": "Panel",
                                        "description": "Basic component to display content in a survey",
                                        "type": "panel",
                                        "component": "panel",
                                        "elements": [
                                            {
                                                "icon": "icon-ui-select",
                                                "name": "Select",
                                                "description": "A drop-down to select one value from a list of values",
                                                "type": "select",
                                                "component": "select",
                                                "elements": [],
                                                "properties": {
                                                    "label": "Category",
                                                    "labelInReport": "category",
                                                    "fontSize": 16,
                                                    "width": "",
                                                    "fieldname": "category",
                                                    "options": survey_categories,
                                                    "mandatory": True,
                                                    "sortOnField": "label",
                                                },
                                                "_id": "67b2499a5c4c9b37da9891b0",
                                                "selected": False,
                                                "show": True,
                                            }
                                        ],
                                        "properties": {
                                            "label": "",
                                            "labelAlignment": "center",
                                            "labelFontSize": "24",
                                            "descriptionAlignment": "left",
                                            "descriptionFontSize": "24",
                                            "tabLabel": "Category",
                                            "alignment": "left",
                                            "canCollapse": False,
                                            "state": False,
                                            "scroll": False,
                                            "showScrollbar": False,
                                            "vertical": "fit",
                                            "direction": "column",
                                            "width": "100%",
                                            "margin": "10px 4px 4px 10px",
                                            "panelShadow": False,
                                            "showOverlay": False,
                                            "showHeader": False,
                                            "allowPanelInDashboard": False,
                                        },
                                        "_id": "66c6e6b5bd5e6e4c67f0a8b3",
                                        "selected": False,
                                        "show": True,
                                    },
                                    {
                                        "icon": "icon-survey",
                                        "name": "Panel",
                                        "description": "Basic component to display content in a survey",
                                        "type": "panel",
                                        "component": "panel",
                                        "elements": [
                                            {
                                                "icon": "icon-ui-textarea",
                                                "name": "Textarea",
                                                "description": "Takes large amounts of text from the customer",
                                                "type": "textarea",
                                                "component": "textarea",
                                                "elements": [],
                                                "properties": {
                                                    "label": "Agent Notes",
                                                    "labelInReport": "agentNotes",
                                                    "fontSize": 16,
                                                    "width": "100%",
                                                    "fieldname": "agentNotes",
                                                    "mandatory": False,
                                                    "validateOnInput": False,
                                                    "sensitiveData": False,
                                                },
                                                "_id": "67b24a9ad1229dc175af08ea",
                                                "selected": False,
                                                "show": True,
                                            }
                                        ],
                                        "properties": {
                                            "label": "",
                                            "labelAlignment": "left",
                                            "labelFontSize": "24",
                                            "descriptionAlignment": "left",
                                            "descriptionFontSize": "24",
                                            "tabLabel": "Agent Notes",
                                            "alignment": "center",
                                            "canCollapse": False,
                                            "state": False,
                                            "scroll": False,
                                            "showScrollbar": False,
                                            "vertical": "fit",
                                            "direction": "column",
                                            "width": "100%",
                                            "margin": "10px 4px 4px 10px",
                                            "panelShadow": False,
                                            "showOverlay": False,
                                            "showHeader": False,
                                            "allowPanelInDashboard": False,
                                        },
                                        "_id": "67b24a41dcc526e3960c1c46",
                                        "selected": False,
                                        "show": True,
                                    },
                                ],
                                "properties": {
                                    "label": "",
                                    "labelAlignment": "center",
                                    "labelFontSize": "24",
                                    "descriptionAlignment": "left",
                                    "descriptionFontSize": "24",
                                    "tabLabel": "Workitem Info",
                                    "alignment": "center",
                                    "canCollapse": False,
                                    "state": False,
                                    "scroll": False,
                                    "showScrollbar": False,
                                    "vertical": "fit",
                                    "direction": "column",
                                    "width": "100%",
                                    "panelShadow": False,
                                    "showOverlay": False,
                                    "showHeader": False,
                                    "allowPanelInDashboard": False,
                                },
                                "_id": "66c6e66937d5e87ab51ca611",
                                "selected": False,
                                "show": True,
                            },
                        ],
                        "properties": {
                            "label": "",
                            "labelAlignment": "center",
                            "labelFontSize": "24",
                            "descriptionAlignment": "left",
                            "descriptionFontSize": "24",
                            "tabLabel": "Main",
                            "alignment": "left",
                            "canCollapse": False,
                            "state": False,
                            "scroll": False,
                            "showScrollbar": False,
                            "vertical": "full",
                            "direction": "column",
                            "width": "",
                            "panelShadow": False,
                            "showOverlay": False,
                            "showHeader": False,
                            "allowPanelInDashboard": False,
                            "main": True,
                        },
                        "_id": "66c540d6a14be123ae577468",
                        "panelId": "refId1724193616114",
                        "selected": False,
                        "show": True,
                    }
                ],
                "footer": {
                    "icon": "icon-ui-footer",
                    "name": "Footer",
                    "description": "Displays navigation buttons at the bottom of a survey",
                    "type": "footer",
                    "component": "footer",
                    "elements": [],
                    "properties": {
                        "type": "iconButton",
                        "icon": "icon-next",
                        "size": "24",
                    },
                    "_id": "66c540d375b7e61ab8322d44",
                },
                "header": {
                    "icon": "icon-ui-header",
                    "name": "Header",
                    "description": "Displays navigation buttons at the top of a survey",
                    "type": "header",
                    "component": "header",
                    "elements": [],
                    "properties": {
                        "showPrevious": False,
                        "showOptions": False,
                        "icon": "icon-next",
                        "showClose": False,
                        "size": "24",
                        "titleFontSize": "24",
                    },
                    "_id": "66c540d37bf6ce297c2edf6a",
                },
                "overlay": {
                    "icon": "icon-ui-panels",
                    "name": "Overlay Panel",
                    "description": "This panel will always be visible and allow the user to minimise or maxime it.",
                    "type": "overlay",
                    "component": "overlay",
                    "elements": [],
                    "properties": {
                        "label": "Overlay Panel",
                        "labelAlignment": "left",
                        "labelFontSize": "24",
                        "descriptionAlignment": "left",
                        "descriptionFontSize": "24",
                        "alignment": "justify",
                        "canCollapse": False,
                        "state": False,
                        "scroll": False,
                        "vertical": "full",
                        "direction": "column",
                        "height": 80,
                    },
                    "_id": "66c540d37805cb06b8f68dd1",
                },
            },
            "width": 700,
            "name": survey_name,
            "showTopNavigatorPage": False,
            "usePanelShadow": True,
            "font": "Rubik:400,400i,700;Rubik, sans-serif",
        }
    )
    headers = {
        "Authorization": ncc_token,
        "Content-Type": "application/json",
    }
    try:
        conn.request("POST", "/data/api/types/survey/", payload, headers)
        res = conn.getresponse()
        if res.status == 201:
            data = res.read().decode("utf-8")
            survey = json.loads(data)
    except:
        pass
    conn.close()
    return survey


def create_chat_survey(
    ncc_location: str,
    ncc_token: str,
    survey_name: str,
    survey_options: list,
    survey_theme: dict,
) -> dict:
    """
    This function creates a survey with a specified name.
    """
    survey = {}
    conn = http.client.HTTPSConnection(ncc_location)
    payload = json.dumps(
        {
            "hideSurveyBoxShadown": False,
            "type": "full",
            "showFooter": False,
            "surveythemeId": survey_theme["_id"],
            "showTabs": False,
            "expansions": {
                "surveythemeId": {
                    "localizations": {
                        "name": {
                            "en": {"language": "en", "value": survey_theme["name"]}
                        },
                    }
                }
            },
            "showBottomNavigatorPage": False,
            "height": 640,
            "debug": True,
            "localizations": {
                "name": {"en": {"language": "en", "value": survey_name}},
            },
            "showHeader": False,
            "allowTabinationMandatoryFields": True,
            "entryPanelId": "6568aac066adc3c1634e7448",
            "layout": {
                "elements": [
                    {
                        "icon": "icon-ui-panel",
                        "name": "Panel",
                        "description": "Basic component to display content in a survey",
                        "type": "panel",
                        "component": "panel",
                        "elements": [
                            {
                                "icon": "icon-ui-panel",
                                "name": "Panel",
                                "description": "Basic component to display content in a survey",
                                "type": "panel",
                                "component": "panel",
                                "elements": [
                                    {
                                        "icon": "icon-ui-text",
                                        "name": "Text",
                                        "description": "Displays direct text to the customer",
                                        "type": "label",
                                        "component": "label",
                                        "elements": [],
                                        "properties": {
                                            "label": "<strong>We Look Forward To Chatting With You!</strong>",
                                            "fontSize": 16,
                                            "margin": "8px",
                                            "alignment": "center",
                                        },
                                        "_id": "6568ab15f9e81c3a70a77c14",
                                        "selected": False,
                                        "show": True,
                                    },
                                    {
                                        "icon": "icon-ui-text",
                                        "name": "Text",
                                        "description": "Displays direct text to the customer",
                                        "type": "label",
                                        "component": "label",
                                        "elements": [],
                                        "properties": {
                                            "label": "Please answer a few questions to help us route you to the the best resource",
                                            "fontSize": "14",
                                            "margin": "8px",
                                            "alignment": "center",
                                        },
                                        "_id": "6568ab324acefc5baa1ea15f",
                                        "selected": False,
                                        "show": True,
                                    },
                                    {
                                        "icon": "icon-ui-radio",
                                        "name": "Radio button",
                                        "description": "Displays mutually exclusive values, and only one can be selected",
                                        "type": "radio",
                                        "component": "radio",
                                        "elements": [],
                                        "properties": {
                                            "label": "I am interested in...",
                                            "labelInReport": "interest",
                                            "fontSize": "14",
                                            "orientation": "vertical",
                                            "width": "100",
                                            "margin": "8px",
                                            "fieldname": "interest",
                                            "options": survey_options,
                                            "wrapOptions": False,
                                            "mandatory": False,
                                        },
                                        "_id": "6568ab7338b8d570e3a8b808",
                                        "selected": False,
                                        "show": True,
                                    },
                                    {
                                        "icon": "icon-ui-move-to-panel",
                                        "name": "Move To Panel",
                                        "description": "Moves to a specific panel in a survey",
                                        "type": "move",
                                        "component": "move",
                                        "elements": [],
                                        "properties": {
                                            "label": "Next >>",
                                            "fontSize": "14",
                                            "buttonWidth": "100%",
                                            "buttonPadding": "8px",
                                            "buttonMargin": "8px",
                                            "variables": [],
                                            "panelId": "6568acb8a8990b9bcbd36c35",
                                            "hideApplication": False,
                                            "sendMessageToWorkflow": False,
                                            "properties": [],
                                        },
                                        "_id": "6568b6fbe7fdf34e67688a78",
                                        "selected": False,
                                        "show": True,
                                    },
                                ],
                                "properties": {
                                    "label": "",
                                    "labelAlignment": "left",
                                    "labelFontSize": "24",
                                    "descriptionAlignment": "left",
                                    "descriptionFontSize": "24",
                                    "alignment": "justify",
                                    "canCollapse": False,
                                    "state": False,
                                    "scroll": False,
                                    "showScrollbar": False,
                                    "vertical": "full",
                                    "direction": "column",
                                    "margin": "8px",
                                    "panelShadow": False,
                                    "showOverlay": False,
                                    "showHeader": False,
                                    "allowPanelInDashboard": False,
                                },
                                "_id": "6568aaf681cf2e78afbcf27e",
                                "selected": False,
                                "show": True,
                            }
                        ],
                        "properties": {
                            "label": "",
                            "labelAlignment": "left",
                            "labelFontSize": "24",
                            "descriptionAlignment": "left",
                            "descriptionFontSize": "24",
                            "tabLabel": "Main",
                            "alignment": "justify",
                            "canCollapse": False,
                            "state": False,
                            "scroll": False,
                            "showScrollbar": False,
                            "vertical": "full",
                            "direction": "column",
                            "width": "",
                            "height": "",
                            "margin": "8px",
                            "panelBackgroundColor": "#ffffff",
                            "panelShadow": True,
                            "panelBorderRadius": "10px",
                            "showOverlay": False,
                            "showHeader": False,
                            "allowPanelInDashboard": False,
                            "main": True,
                        },
                        "_id": "6568aac066adc3c1634e7448",
                        "panelId": "refId1701357311323",
                        "selected": False,
                        "show": True,
                    },
                    {
                        "icon": "icon-ui-panel",
                        "name": "Panel",
                        "description": "Basic component to display content in a survey",
                        "type": "panel",
                        "component": "panel",
                        "elements": [
                            {
                                "icon": "icon-ui-panel",
                                "name": "Panel",
                                "description": "Basic component to display content in a survey",
                                "type": "panel",
                                "component": "panel",
                                "elements": [
                                    {
                                        "icon": "icon-ui-panel",
                                        "name": "Panel",
                                        "description": "Basic component to display content in a survey",
                                        "type": "panel",
                                        "component": "panel",
                                        "elements": [
                                            {
                                                "icon": "icon-ui-text",
                                                "name": "Text",
                                                "description": "Displays direct text to the customer",
                                                "type": "label",
                                                "component": "label",
                                                "elements": [],
                                                "properties": {
                                                    "label": "<strong>In case we get disconnected, please let us know how to contact you . . .</strong>",
                                                    "fontSize": 16,
                                                    "alignment": "center",
                                                },
                                                "_id": "6568b967795e9376558f5577",
                                                "selected": False,
                                                "show": True,
                                            },
                                            {
                                                "icon": "icon-ui-input",
                                                "name": "Input",
                                                "description": "A box for the customer to enter information",
                                                "type": "input",
                                                "component": "input",
                                                "elements": [],
                                                "properties": {
                                                    "label": "First Name",
                                                    "labelInReport": "firstName",
                                                    "fontSize": "14",
                                                    "width": "100%",
                                                    "margin": "8px",
                                                    "fieldname": "firstName",
                                                    "defaultValue": "",
                                                    "mandatory": False,
                                                    "readOnly": False,
                                                    "validateOnInput": False,
                                                    "sensitiveData": False,
                                                    "saveToLocalStorage": False,
                                                },
                                                "_id": "6568b9f56274299551339279",
                                                "selected": False,
                                                "show": True,
                                            },
                                            {
                                                "icon": "icon-ui-input",
                                                "name": "Input",
                                                "description": "A box for the customer to enter information",
                                                "type": "input",
                                                "component": "input",
                                                "elements": [],
                                                "properties": {
                                                    "label": "Last Name",
                                                    "labelInReport": "lastName",
                                                    "fontSize": "14",
                                                    "width": "100%",
                                                    "margin": "8px",
                                                    "fieldname": "lastName",
                                                    "defaultValue": "",
                                                    "mandatory": False,
                                                    "readOnly": False,
                                                    "validateOnInput": False,
                                                    "sensitiveData": False,
                                                    "saveToLocalStorage": False,
                                                },
                                                "_id": "6568baac91bac25f7de05fe3",
                                                "selected": False,
                                                "show": True,
                                            },
                                            {
                                                "icon": "icon-ui-input",
                                                "name": "Input",
                                                "description": "A box for the customer to enter information",
                                                "type": "input",
                                                "component": "input",
                                                "elements": [],
                                                "properties": {
                                                    "label": "Email",
                                                    "labelInReport": "email",
                                                    "fontSize": "14",
                                                    "width": "100%",
                                                    "margin": "8px",
                                                    "fieldname": "email",
                                                    "defaultValue": "",
                                                    "mandatory": False,
                                                    "readOnly": False,
                                                    "validateOnInput": False,
                                                    "sensitiveData": False,
                                                    "saveToLocalStorage": False,
                                                },
                                                "_id": "6568bad2c3efd4ffce67d209",
                                                "selected": False,
                                                "show": True,
                                            },
                                            {
                                                "icon": "icon-ui-input",
                                                "name": "Input",
                                                "description": "A box for the customer to enter information",
                                                "type": "input",
                                                "component": "input",
                                                "elements": [],
                                                "properties": {
                                                    "label": "Phone",
                                                    "labelInReport": "phone",
                                                    "fontSize": "14",
                                                    "width": "100%",
                                                    "margin": "8px",
                                                    "fieldname": "phone",
                                                    "defaultValue": "",
                                                    "mandatory": False,
                                                    "readOnly": False,
                                                    "validateOnInput": False,
                                                    "sensitiveData": False,
                                                    "saveToLocalStorage": False,
                                                },
                                                "_id": "6568bc2b12be343b5e2e86bd",
                                                "selected": False,
                                                "show": True,
                                            },
                                            {
                                                "icon": "icon-ui-panel",
                                                "name": "Panel",
                                                "description": "Basic component to display content in a survey",
                                                "type": "panel",
                                                "component": "panel",
                                                "elements": [
                                                    {
                                                        "icon": "icon-ui-move-to-panel",
                                                        "name": "Move To Panel",
                                                        "description": "Moves to a specific panel in a survey",
                                                        "type": "move",
                                                        "component": "move",
                                                        "elements": [],
                                                        "properties": {
                                                            "label": "<< Back",
                                                            "fontSize": "14",
                                                            "buttonWidth": "100px",
                                                            "buttonPadding": "8px",
                                                            "buttonMargin": "8px",
                                                            "variables": [],
                                                            "panelId": "6568aac066adc3c1634e7448",
                                                            "hideApplication": False,
                                                            "sendMessageToWorkflow": False,
                                                            "properties": [],
                                                        },
                                                        "_id": "6568bcd9bcb697fbacf9a2ce",
                                                        "selected": False,
                                                        "show": True,
                                                    }
                                                ],
                                                "properties": {
                                                    "label": "",
                                                    "labelAlignment": "left",
                                                    "labelFontSize": "24",
                                                    "descriptionAlignment": "left",
                                                    "descriptionFontSize": "24",
                                                    "alignment": "center",
                                                    "canCollapse": False,
                                                    "state": False,
                                                    "scroll": False,
                                                    "showScrollbar": False,
                                                    "vertical": "fit",
                                                    "direction": "row",
                                                    "margin": "8px",
                                                    "panelShadow": False,
                                                    "showOverlay": False,
                                                    "showHeader": False,
                                                    "allowPanelInDashboard": False,
                                                },
                                                "_id": "6568bcd062acab90f772f6c8",
                                                "selected": False,
                                                "show": True,
                                            },
                                            {
                                                "icon": "icon-ui-panel",
                                                "name": "Panel",
                                                "description": "Basic component to display content in a survey",
                                                "type": "panel",
                                                "component": "panel",
                                                "elements": [
                                                    {
                                                        "icon": "icon-avatar-chat",
                                                        "name": "Chat",
                                                        "description": "Creates a new chat workitem with a customer",
                                                        "type": "chat",
                                                        "component": "chat",
                                                        "elements": [],
                                                        "properties": {
                                                            "label": "Chat Now !",
                                                            "fontSize": "14",
                                                            "buttonWidth": "120px",
                                                            "buttonPadding": "8px",
                                                            "buttonMargin": "8px",
                                                            "campaignId": "66c520866287b156174162b7",
                                                            "name": "firstName",
                                                            "email": "email",
                                                            "messages": [],
                                                            "attachedData": [
                                                                {
                                                                    "label": "firstName",
                                                                    "value": "${surveyInformation.firstName.value}",
                                                                },
                                                                {
                                                                    "label": "lastName",
                                                                    "value": "${surveyInformation.lastName.value}",
                                                                },
                                                                {
                                                                    "label": "email",
                                                                    "value": "${surveyInformation.email.value}",
                                                                },
                                                                {
                                                                    "label": "phone",
                                                                    "value": "${surveyInformation.phone.value}",
                                                                },
                                                                {
                                                                    "label": "contactType",
                                                                    "value": "${surveyInformation.contactType.value}",
                                                                },
                                                                {
                                                                    "label": "interest",
                                                                    "value": "${surveyInformation.interest.value}",
                                                                },
                                                            ],
                                                            "successVariables": [],
                                                            "onSuccess": "panel",
                                                            "successPanelId": "6568c3cea79bbc3acda46610",
                                                            "errorVariables": [],
                                                            "onError": "panel",
                                                            "errorPanelId": "6568aac066adc3c1634e7448",
                                                        },
                                                        "_id": "6568bd4129e47abf48831836",
                                                        "selected": False,
                                                        "show": True,
                                                    },
                                                    {
                                                        "icon": "icon-ui-text",
                                                        "name": "Text",
                                                        "description": "Displays direct text to the customer",
                                                        "type": "label",
                                                        "component": "label",
                                                        "elements": [],
                                                        "properties": {
                                                            "label": "<strong>OR</strong>",
                                                            "fontSize": 16,
                                                            "margin": "8px",
                                                            "alignment": "center",
                                                        },
                                                        "_id": "6568bdac16402e21c84d5a4d",
                                                        "selected": False,
                                                        "show": True,
                                                    },
                                                    {
                                                        "icon": "icon-callback",
                                                        "name": "Web Callback",
                                                        "description": "Creates an outbound call to a specific number at a specific time",
                                                        "type": "webcallback",
                                                        "component": "webcallback",
                                                        "elements": [],
                                                        "properties": {
                                                            "label": "Just Call Me !",
                                                            "fontSize": "14",
                                                            "buttonWidth": "120px",
                                                            "buttonPadding": "8px",
                                                            "buttonMargin": "8px",
                                                            "campaignId": "66c520866287b156174162b7",
                                                            "phone": "phone",
                                                            "attachedData": [
                                                                {
                                                                    "label": "firstName",
                                                                    "value": "${surveyInformation.firstName.value}",
                                                                },
                                                                {
                                                                    "label": "lastName",
                                                                    "value": "${surveyInformation.lastName.value}",
                                                                },
                                                                {
                                                                    "label": "email",
                                                                    "value": "${surveyInformation.email.value}",
                                                                },
                                                                {
                                                                    "label": "phone",
                                                                    "value": "${surveyInformation.phone.value}",
                                                                },
                                                                {
                                                                    "label": "contactType",
                                                                    "value": "${surveyInformation.contactType.value}",
                                                                },
                                                                {
                                                                    "label": "queueId",
                                                                    "value": "'66c529376287b156174162c6'",
                                                                },
                                                            ],
                                                            "successVariables": [],
                                                            "onSuccess": "panel",
                                                            "success": "An agent will call you momentarily.",
                                                            "successPanelId": "656a352d987c4fbc26b622f2",
                                                            "errorVariables": [],
                                                            "onError": "panel",
                                                            "errorPanelId": "6568aac066adc3c1634e7448",
                                                        },
                                                        "_id": "6568bdf7cedb0075e4b376d9",
                                                        "selected": False,
                                                        "show": True,
                                                    },
                                                ],
                                                "properties": {
                                                    "label": "",
                                                    "labelAlignment": "left",
                                                    "labelFontSize": "24",
                                                    "descriptionAlignment": "left",
                                                    "descriptionFontSize": "24",
                                                    "alignment": "center",
                                                    "canCollapse": False,
                                                    "state": False,
                                                    "scroll": False,
                                                    "showScrollbar": False,
                                                    "vertical": "fit",
                                                    "direction": "row",
                                                    "panelShadow": False,
                                                    "showOverlay": False,
                                                    "showHeader": False,
                                                    "allowPanelInDashboard": False,
                                                },
                                                "_id": "6568bd21d1ecac48b58ca805",
                                                "selected": False,
                                                "show": True,
                                            },
                                        ],
                                        "properties": {
                                            "label": "",
                                            "labelAlignment": "left",
                                            "labelFontSize": "24",
                                            "descriptionAlignment": "left",
                                            "descriptionFontSize": "24",
                                            "alignment": "justify",
                                            "canCollapse": False,
                                            "state": False,
                                            "scroll": False,
                                            "showScrollbar": False,
                                            "vertical": "full",
                                            "direction": "column",
                                            "margin": "8px",
                                            "panelShadow": False,
                                            "showOverlay": False,
                                            "showHeader": False,
                                            "allowPanelInDashboard": False,
                                        },
                                        "_id": "65736dee929ae8f69411053b",
                                        "selected": False,
                                        "show": True,
                                    }
                                ],
                                "properties": {
                                    "label": "",
                                    "labelAlignment": "left",
                                    "labelFontSize": "24",
                                    "descriptionAlignment": "left",
                                    "descriptionFontSize": "24",
                                    "alignment": "justify",
                                    "canCollapse": False,
                                    "state": False,
                                    "scroll": False,
                                    "showScrollbar": False,
                                    "vertical": "full",
                                    "direction": "column",
                                    "panelShadow": False,
                                    "showOverlay": False,
                                    "showHeader": False,
                                    "allowPanelInDashboard": False,
                                },
                                "_id": "6568b8ee6c7eea345f18c3a6",
                                "selected": False,
                                "show": True,
                            }
                        ],
                        "properties": {
                            "label": "",
                            "labelAlignment": "left",
                            "labelFontSize": "24",
                            "descriptionAlignment": "left",
                            "descriptionFontSize": "24",
                            "tabLabel": "Chat or Call Now",
                            "alignment": "justify",
                            "canCollapse": False,
                            "state": False,
                            "scroll": False,
                            "showScrollbar": False,
                            "vertical": "full",
                            "direction": "column",
                            "width": "",
                            "height": "",
                            "margin": "8px",
                            "panelBackgroundColor": "#ffffff",
                            "panelShadow": True,
                            "panelBorderRadius": "10px",
                            "showOverlay": False,
                            "showHeader": False,
                            "allowPanelInDashboard": False,
                            "main": True,
                        },
                        "_id": "6568acb8a8990b9bcbd36c35",
                        "panelId": "refId1701357311619",
                        "selected": False,
                        "show": True,
                    },
                    {
                        "icon": "icon-ui-panel",
                        "name": "Panel",
                        "description": "Basic component to display content in a survey",
                        "type": "panel",
                        "component": "panel",
                        "elements": [
                            {
                                "icon": "icon-ui-header",
                                "name": "Header",
                                "description": "Displays navigation buttons at the top of a survey",
                                "type": "header",
                                "component": "header",
                                "elements": [],
                                "properties": {
                                    "margin": "",
                                    "showPrevious": False,
                                    "showOptions": False,
                                    "icon": "icon-next",
                                    "showClose": True,
                                    "closePanelId": "656a2d794b998c22b17591ae",
                                    "size": "24",
                                    "titleFontSize": "24",
                                },
                                "_id": "657b3ed5358649ca9f796b61",
                                "selected": False,
                                "show": True,
                            },
                            {
                                "icon": "icon-ll-avatar-authorities-unlock",
                                "name": "Waiting for Agent",
                                "description": "Presents a message while waiting for an agent to become available",
                                "type": "waiting",
                                "component": "waiting",
                                "elements": [],
                                "properties": {
                                    "label": "",
                                    "labelAlignment": "left",
                                    "labelFontSize": "24",
                                    "descriptionAlignment": "left",
                                    "descriptionFontSize": "24",
                                    "waitingMsgFontSize": 24,
                                    "waitingIcon": "icon-clock",
                                    "waitingIconFontSize": 116,
                                    "vertical": "full",
                                    "alignment": "center",
                                    "verticalAlignment": "top",
                                    "direction": "column",
                                    "margin": "8px",
                                    "onAgentAvailable": "panel",
                                    "onAgentAvailablePanelId": "657a16abdcfd5d8dd6bcd6dd",
                                    "timer": 30,
                                    "onTerminate": "panel",
                                    "terminatePanelId": "656a2d794b998c22b17591ae",
                                    "useReverseProxy": False,
                                },
                                "_id": "6568c76ed96c51849bba7af4",
                                "selected": False,
                                "show": True,
                            },
                        ],
                        "properties": {
                            "label": "",
                            "labelAlignment": "left",
                            "labelFontSize": "24",
                            "descriptionAlignment": "left",
                            "descriptionFontSize": "24",
                            "tabLabel": "Waiting for Chat",
                            "alignment": "justify",
                            "canCollapse": False,
                            "state": False,
                            "scroll": False,
                            "showScrollbar": False,
                            "vertical": "full",
                            "direction": "column",
                            "width": "",
                            "height": "",
                            "margin": "8px",
                            "panelBackgroundColor": "#ffffff",
                            "panelShadow": True,
                            "panelBorderRadius": "10px",
                            "showOverlay": False,
                            "showHeader": False,
                            "allowPanelInDashboard": False,
                            "main": True,
                        },
                        "_id": "6568c3cea79bbc3acda46610",
                        "panelId": "refId1701357314946",
                        "selected": False,
                        "show": True,
                    },
                    {
                        "icon": "icon-ui-panel",
                        "name": "Panel",
                        "description": "Basic component to display content in a survey",
                        "type": "panel",
                        "component": "panel",
                        "elements": [
                            {
                                "icon": "icon-ui-header",
                                "name": "Header",
                                "description": "Displays navigation buttons at the top of a survey",
                                "type": "header",
                                "component": "header",
                                "elements": [],
                                "properties": {
                                    "margin": "",
                                    "showPrevious": False,
                                    "showOptions": False,
                                    "icon": "icon-next",
                                    "showClose": True,
                                    "closePanelId": "656a2d794b998c22b17591ae",
                                    "size": "24",
                                    "titleFontSize": "24",
                                },
                                "_id": "657b3eb2bea14e6ae6d4979c",
                                "selected": False,
                                "show": True,
                            },
                            {
                                "icon": "icon-ui-panel",
                                "name": "Panel",
                                "description": "Basic component to display content in a survey",
                                "type": "panel",
                                "component": "panel",
                                "elements": [
                                    {
                                        "icon": "icon-chat-1to2",
                                        "name": "Chat Panel",
                                        "description": "A Thrio resource to send messages to and from a customer’s device",
                                        "type": "conversation",
                                        "component": "conversation",
                                        "elements": [],
                                        "properties": {
                                            "vertical": "full",
                                            "margin": "8px",
                                            "allowAttachments": True,
                                            "allowVoiceMessage": True,
                                            "allowEmoji": True,
                                            "onTerminate": "panel",
                                            "terminatePanelId": "656a2d794b998c22b17591ae",
                                        },
                                        "_id": "657a16ab113fd58e152c58ef",
                                        "selected": False,
                                        "show": True,
                                    }
                                ],
                                "properties": {
                                    "label": "",
                                    "labelAlignment": "left",
                                    "labelFontSize": "24",
                                    "descriptionAlignment": "left",
                                    "descriptionFontSize": "24",
                                    "tabLabel": "Chatting",
                                    "alignment": "justify",
                                    "canCollapse": False,
                                    "state": False,
                                    "scroll": False,
                                    "showScrollbar": False,
                                    "vertical": "full",
                                    "direction": "column",
                                    "width": "",
                                    "height": "",
                                    "margin": "",
                                    "panelShadow": False,
                                    "showOverlay": False,
                                    "showHeader": False,
                                    "allowPanelInDashboard": False,
                                    "main": True,
                                },
                                "_id": "657a16aba18f8e8f80065a5c",
                                "panelId": "refId1702499779267",
                                "selected": False,
                                "show": True,
                            },
                        ],
                        "properties": {
                            "label": "",
                            "labelAlignment": "left",
                            "labelFontSize": "24",
                            "descriptionAlignment": "left",
                            "descriptionFontSize": "24",
                            "tabLabel": "Chatting",
                            "alignment": "justify",
                            "canCollapse": False,
                            "state": False,
                            "scroll": False,
                            "showScrollbar": False,
                            "vertical": "full",
                            "direction": "column",
                            "width": "",
                            "height": "",
                            "margin": "8px",
                            "panelBackgroundColor": "#ffffff",
                            "panelShadow": True,
                            "panelBorderRadius": "10px",
                            "showOverlay": False,
                            "showHeader": False,
                            "allowPanelInDashboard": False,
                            "main": True,
                        },
                        "_id": "657a16abdcfd5d8dd6bcd6dd",
                        "panelId": "refId1702499779265",
                        "selected": False,
                        "show": True,
                    },
                    {
                        "icon": "icon-ui-panel",
                        "name": "Panel",
                        "description": "Basic component to display content in a survey",
                        "type": "panel",
                        "component": "panel",
                        "elements": [
                            {
                                "icon": "icon-ui-panel",
                                "name": "Panel",
                                "description": "Basic component to display content in a survey",
                                "type": "panel",
                                "component": "panel",
                                "elements": [
                                    {
                                        "icon": "icon-ui-text",
                                        "name": "Text",
                                        "description": "Displays direct text to the customer",
                                        "type": "label",
                                        "component": "label",
                                        "elements": [],
                                        "properties": {
                                            "label": "<strong>Thank you for chatting with us!</strong>",
                                            "fontSize": 16,
                                            "margin": "12px",
                                            "alignment": "center",
                                        },
                                        "_id": "656a33163cfeee888196f585",
                                        "selected": False,
                                        "show": True,
                                    }
                                ],
                                "properties": {
                                    "label": "",
                                    "labelAlignment": "left",
                                    "labelFontSize": 16,
                                    "descriptionAlignment": "left",
                                    "descriptionFontSize": "24",
                                    "tabLabel": "",
                                    "alignment": "justify",
                                    "canCollapse": False,
                                    "state": False,
                                    "scroll": False,
                                    "showScrollbar": False,
                                    "vertical": "fit",
                                    "direction": "column",
                                    "margin": "8px",
                                    "panelShadow": False,
                                    "showOverlay": False,
                                    "showHeader": False,
                                    "allowPanelInDashboard": False,
                                },
                                "_id": "656a3309ed6114ca301f35ce",
                                "selected": False,
                                "show": True,
                            },
                            {
                                "icon": "icon-ui-move-to-panel",
                                "name": "Move To Panel",
                                "description": "Moves to a specific panel in a survey",
                                "type": "move",
                                "component": "move",
                                "elements": [],
                                "properties": {
                                    "label": "<< Go Back to Main",
                                    "fontSize": "14",
                                    "buttonWidth": "300px",
                                    "buttonPadding": "8px",
                                    "buttonMargin": "8px",
                                    "variables": [],
                                    "panelId": "6568aac066adc3c1634e7448",
                                    "hideApplication": False,
                                    "sendMessageToWorkflow": False,
                                    "properties": [],
                                },
                                "_id": "657b3fbe045e7f8fc721c96c",
                                "selected": False,
                                "show": True,
                            },
                        ],
                        "properties": {
                            "label": "",
                            "labelAlignment": "left",
                            "labelFontSize": "24",
                            "descriptionAlignment": "left",
                            "descriptionFontSize": "24",
                            "tabLabel": "Chat Completed",
                            "alignment": "justify",
                            "canCollapse": False,
                            "state": False,
                            "scroll": False,
                            "showScrollbar": False,
                            "vertical": "full",
                            "direction": "column",
                            "width": "",
                            "height": "",
                            "margin": "8px",
                            "panelBackgroundColor": "#ffffff",
                            "panelShadow": True,
                            "panelBorderRadius": "10px",
                            "showOverlay": False,
                            "showHeader": False,
                            "allowPanelInDashboard": False,
                            "main": True,
                        },
                        "_id": "656a2d794b998c22b17591ae",
                        "panelId": "refId1701455752204",
                        "selected": False,
                        "show": True,
                    },
                    {
                        "icon": "icon-ui-panel",
                        "name": "Panel",
                        "description": "Basic component to display content in a survey",
                        "type": "panel",
                        "component": "panel",
                        "elements": [
                            {
                                "icon": "icon-ui-panel",
                                "name": "Panel",
                                "description": "Basic component to display content in a survey",
                                "type": "panel",
                                "component": "panel",
                                "elements": [
                                    {
                                        "icon": "icon-ui-text",
                                        "name": "Text",
                                        "description": "Displays direct text to the customer",
                                        "type": "label",
                                        "component": "label",
                                        "elements": [],
                                        "properties": {
                                            "label": "<strong>Thank you!  An agent will call you shortly.</strong>",
                                            "fontSize": 16,
                                            "margin": "8px",
                                            "alignment": "center",
                                        },
                                        "_id": "656a352dd9aa375ace00222e",
                                        "selected": False,
                                        "show": True,
                                    }
                                ],
                                "properties": {
                                    "label": "",
                                    "labelAlignment": "left",
                                    "labelFontSize": 16,
                                    "descriptionAlignment": "left",
                                    "descriptionFontSize": "24",
                                    "tabLabel": "",
                                    "alignment": "justify",
                                    "canCollapse": False,
                                    "state": False,
                                    "scroll": False,
                                    "showScrollbar": False,
                                    "vertical": "fit",
                                    "direction": "column",
                                    "margin": "8px",
                                    "panelShadow": False,
                                    "showOverlay": False,
                                    "showHeader": False,
                                    "allowPanelInDashboard": False,
                                    "main": True,
                                },
                                "_id": "656a352d57709ac888eaef62",
                                "selected": False,
                                "show": True,
                                "panelId": "refId1701455753221",
                            },
                            {
                                "icon": "icon-ui-move-to-panel",
                                "name": "Move To Panel",
                                "description": "Moves to a specific panel in a survey",
                                "type": "move",
                                "component": "move",
                                "elements": [],
                                "properties": {
                                    "label": "<< Go Back to Main",
                                    "fontSize": "14",
                                    "buttonWidth": "300px",
                                    "buttonPadding": "8px",
                                    "buttonMargin": "8px",
                                    "variables": [],
                                    "panelId": "6568aac066adc3c1634e7448",
                                    "hideApplication": False,
                                    "sendMessageToWorkflow": False,
                                    "properties": [],
                                },
                                "_id": "657b40fb28a29d0b799ab328",
                                "selected": False,
                                "show": True,
                            },
                        ],
                        "properties": {
                            "label": "",
                            "labelAlignment": "left",
                            "labelFontSize": "24",
                            "descriptionAlignment": "left",
                            "descriptionFontSize": "24",
                            "tabLabel": "Callback In Progress",
                            "alignment": "justify",
                            "canCollapse": False,
                            "state": False,
                            "scroll": False,
                            "showScrollbar": False,
                            "vertical": "full",
                            "direction": "column",
                            "width": "",
                            "height": "",
                            "margin": "8px",
                            "panelBackgroundColor": "#ffffff",
                            "panelShadow": True,
                            "panelBorderRadius": "10px",
                            "showOverlay": False,
                            "showHeader": False,
                            "allowPanelInDashboard": False,
                            "main": True,
                        },
                        "_id": "656a352d987c4fbc26b622f2",
                        "panelId": "refId1701455753219",
                        "selected": False,
                        "show": True,
                    },
                ],
                "footer": {
                    "icon": "icon-ui-footer",
                    "name": "Footer",
                    "description": "Displays navigation buttons at the bottom of a survey",
                    "type": "footer",
                    "component": "footer",
                    "elements": [],
                    "properties": {
                        "type": "iconButton",
                        "icon": "icon-next",
                        "size": "24",
                    },
                    "_id": "6568aa7226c9c87360287a56",
                },
                "header": {
                    "icon": "icon-ui-header",
                    "name": "Header",
                    "description": "Displays navigation buttons at the top of a survey",
                    "type": "header",
                    "component": "header",
                    "elements": [],
                    "properties": {
                        "showPrevious": False,
                        "showOptions": False,
                        "icon": "icon-next",
                        "showClose": False,
                        "size": "24",
                        "titleFontSize": "24",
                    },
                    "_id": "6568aa7210f8073561993f07",
                    "show": True,
                },
                "overlay": {
                    "icon": "icon-ui-panels",
                    "name": "Overlay Panel",
                    "description": "This panel will always be visible and allow the user to minimise or maxime it.",
                    "type": "overlay",
                    "component": "overlay",
                    "elements": [],
                    "properties": {
                        "label": "Overlay Panel",
                        "labelAlignment": "left",
                        "labelFontSize": "24",
                        "descriptionAlignment": "left",
                        "descriptionFontSize": "24",
                        "alignment": "justify",
                        "canCollapse": False,
                        "state": False,
                        "scroll": False,
                        "vertical": "full",
                        "direction": "column",
                        "height": 80,
                    },
                    "_id": "6568aa724b5a2b5452a0d373",
                    "show": True,
                },
            },
            "width": 380,
            "files": {
                "pet_png": {"name": "pet.png", "contentType": "image/png"},
                "pet__1__png": {"name": "pet__1_.png", "contentType": "image/png"},
                "pet__2__png": {"name": "pet__2_.png", "contentType": "image/png"},
                "pets_png": {"name": "pets.png", "contentType": "image/png"},
                "paws_png": {"name": "paws.png", "contentType": "image/png"},
                "pet__3__png": {"name": "pet__3_.png", "contentType": "image/png"},
                "chat_png": {"name": "chat.png", "contentType": "image/png"},
                "png-transparent-chat-bubble-illustration-speech-balloon-computer-icons-online-chat-chat-miscellaneous-text-monochrome-thumbnail_png": {
                    "name": "png-transparent-chat-bubble-illustration-speech-balloon-computer-icons-online-chat-chat-miscellaneous-text-monochrome-thumbnail.png",
                    "contentType": "image/png",
                },
                "chat-now-icon-png-115537221333kmknwuqm6_png": {
                    "name": "chat-now-icon-png-115537221333kmknwuqm6.png",
                    "contentType": "image/png",
                },
                "1380370_png": {"name": "1380370.png", "contentType": "image/png"},
                "2194522-200_png": {
                    "name": "2194522-200.png",
                    "contentType": "image/png",
                },
                "chat-icon-design-in-blue-circle-png_webp": {
                    "name": "chat-icon-design-in-blue-circle-png.webp",
                    "contentType": "image/webp",
                },
                "chat-circle-blue-512_webp": {
                    "name": "chat-circle-blue-512.webp",
                    "contentType": "image/webp",
                },
                "87-512_webp": {"name": "87-512.webp", "contentType": "image/webp"},
                "Top-10-Communication-Skills-Every-Manager-Needs-to-Have_webp": {
                    "name": "Top-10-Communication-Skills-Every-Manager-Needs-to-Have.webp",
                    "contentType": "image/webp",
                },
                "9bf0d084963d20b664b5ff32a9c8e271_png": {
                    "name": "9bf0d084963d20b664b5ff32a9c8e271.png",
                    "contentType": "image/png",
                },
            },
            "showTopNavigatorPage": False,
            "usePanelShadow": False,
            "font": "Rubik:400,400i,700;Rubik, sans-serif",
            "name": survey_name,
        }
    )
    headers = {
        "Authorization": ncc_token,
        "Content-Type": "application/json",
    }
    try:
        conn.request("POST", "/data/api/types/survey/", payload, headers)
        res = conn.getresponse()
        if res.status == 201:
            data = res.read().decode("utf-8")
            survey = json.loads(data)
    except:
        pass
    conn.close()
    return survey


def update_chat_survey_campaign_id(
    ncc_location: str, ncc_token: str, survey_id: str, campaign_id: str
) -> bool:
    """
    This function updates the campaign ID associated with two buttons on the chat survey.
    """
    success = False
    survey = get_survey(ncc_location, ncc_token, survey_id)
    if survey != {}:
        conn = http.client.HTTPSConnection(ncc_location)
        survey["layout"]["elements"][1]["elements"][0]["elements"][0]["elements"][6][
            "elements"
        ][0]["properties"]["campaignId"] = campaign_id
        survey["layout"]["elements"][1]["elements"][0]["elements"][0]["elements"][6][
            "elements"
        ][2]["properties"]["campaignId"] = campaign_id
        payload = json.dumps(survey)
        headers = {
            "Authorization": ncc_token,
            "Content-Type": "application/json",
        }
        try:
            conn.request(
                "PATCH",
                f"/data/api/types/survey/{survey_id}",
                payload,
                headers,
            )
            res = conn.getresponse()
            if res.status == 200:
                success = True
        except:
            pass
        conn.close()
    return success


def delete_survey(ncc_location: str, ncc_token: str, survey_id: str) -> bool:
    """
    This function deletes a survey with the specified survey ID.
    """
    success = False
    conn = http.client.HTTPSConnection(ncc_location)
    payload = ""
    headers = {"Authorization": ncc_token}
    try:
        conn.request("DELETE", f"/data/api/types/survey/{survey_id}", payload, headers)
        res = conn.getresponse()
        if res.status == 204:
            success = True
    except:
        pass
    conn.close()
    return success
