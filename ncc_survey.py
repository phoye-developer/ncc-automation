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


def get_surveys(ncc_location: str, ncc_token: str) -> list:
    """
    This function fetches a list of surveys present on the Nextiva Contact Center (NCC) tenant.
    """
    surveys = []
    conn = http.client.HTTPSConnection(ncc_location)
    payload = ""
    headers = {"Authorization": ncc_token}
    try:
        conn.request("GET", "/data/api/types/survey?q=Test%20", payload, headers)
        res = conn.getresponse()
        if res.status == 200:
            data = res.read().decode("utf-8")
            json_data = json.loads(data)
            total = json_data["total"]
            if total > 0:
                results = json_data["objects"]
                for result in results:
                    survey_name = result["name"]
                    if survey_name[0:5] == "Test ":
                        surveys.append(result)
    except:
        pass
    conn.close()
    return surveys


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
                                                    "mandatory": True,
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
                                                    "mandatory": True,
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
                                                    "mandatory": True,
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
