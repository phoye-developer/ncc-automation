import http.client
import urllib.parse
import json


def get_survey_themes(ncc_location: str, ncc_token: str) -> list:
    """
    This function searches for a list of survey themes in Nextiva Contact Center (NCC)
    """
    survey_themes = []
    conn = http.client.HTTPSConnection(ncc_location)
    payload = ""
    headers = {"Authorization": ncc_token}
    conn.request("GET", "/data/api/types/surveytheme?q=Test%20", payload, headers)
    res = conn.getresponse()
    if res.status == 200:
        data = res.read().decode("utf-8")
        json_data = json.loads(data)
        total = json_data["total"]
        if total > 0:
            results = json_data["objects"]
            for result in results:
                survey_theme_name = result["name"]
                if survey_theme_name[0:5] == "Test ":
                    survey_themes.append(result)
    return survey_themes


def search_survey_themes(
    ncc_location: str, ncc_token: str, survey_theme_name: str
) -> dict:
    """
    This function searches for an existing survey theme with the same name as the intended new survey theme.
    """
    survey_theme = {}
    conn = http.client.HTTPSConnection(ncc_location)
    payload = ""
    headers = {"Authorization": ncc_token}
    url_encoded_name = urllib.parse.quote(survey_theme_name)
    conn.request(
        "GET",
        f"/data/api/types/surveytheme?q={url_encoded_name}",
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
                if result["name"] == survey_theme_name:
                    survey_theme = result
                    break
    conn.close()
    return survey_theme


def create_survey_theme(
    ncc_location: str, ncc_token: str, survey_theme_name: str
) -> dict:
    """
    This function creates a new survey theme in Nextiva Contact Center (NCC).
    """
    survey_theme = {}
    conn = http.client.HTTPSConnection(ncc_location)
    payload = json.dumps(
        {
            "localizations": {
                "name": {"en": {"language": "en", "value": survey_theme_name}},
            },
            "type": "system",
            "theme": {
                "booleanFalseColor": "rgb(208, 2, 27)",
                "booleanHandleColor": "rgb(255, 255, 255)",
                "booleanTrueColor": "rgb(107, 155, 52)",
                "buttonBackground": "#005fec",
                "buttonBackgroundHover": "rgb(255, 255, 255)",
                "buttonBorder": "rgba(0, 0, 0, 0)",
                "buttonBorderHover": "rgba(0, 0, 0, 0)",
                "buttonColor": "rgba(255, 255, 255)",
                "buttonColorHover": "#005fec",
                "calendarActiveBackground": "#005fec",
                "calendarActivetColor": "rgb(255, 255, 255)",
                "calendarHighlightBackground": "rgb(240, 240, 240)",
                "calendarHighlightColor": "#005fec",
                "chatMessageInputBackground": "rgba(0, 0, 0, 0)",
                "chatMessageInputColor": "rgb(54, 69, 79)",
                "clientMessageBackground": "rgb(240, 240, 240)",
                "disabledColor": "rgb(211,211,211)",
                "dropdownBackground": "rgb(240, 240, 240)",
                "dropdownTextColor": "rgb(54, 69, 79)",
                "footerBackground": "rgba(255, 255, 255)",
                "footerIconColor": "rgb(54, 69, 79)",
                "headerBackground": "rgb(54, 69, 79)",
                "headerIconColor": "rgba(255, 255, 255)",
                "inputBackground": "rgb(240, 240, 240)",
                "inputBorderColor": "rgb(200, 200, 200)",
                "inputColor": "rgb(54, 69, 79)",
                "inputFocusBackground": "rgb(255, 255, 255)",
                "inputFocusBorderColor": "#005fec",
                "inputFocusColor": "rgb(54, 69, 79)",
                "labelColor": "#005fec",
                "listHoverColor": "rgb(240, 240, 240)",
                "messagesBackgroundColor": "rgba(0, 0, 0, 0)",
                "panelBackground": "rgba(0, 0, 0, 0)",
                "panelDescriptionColor": "#005fec",
                "panelTitleColor": "rgb(54, 69, 79)",
                "selectedColor": "#005fec",
                "surveyButtonBackground": "#005fec",
            },
        }
    )
    headers = {
        "Authorization": ncc_token,
        "Content-Type": "application/json",
    }
    conn.request("POST", "/data/api/types/surveytheme", payload, headers)
    res = conn.getresponse()
    if res.status == 201:
        data = res.read().decode("utf-8")
        survey_theme = json.loads(data)
    return survey_theme


def delete_survey_theme(
    ncc_location: str, ncc_token: str, survey_theme_id: str
) -> bool:
    """
    This function deletes a survey theme with the specified survey theme ID.
    """
    success = False
    conn = http.client.HTTPSConnection(ncc_location)
    payload = ""
    headers = {"Authorization": ncc_token}
    conn.request(
        "DELETE", f"/data/api/types/surveytheme/{survey_theme_id}", payload, headers
    )
    res = conn.getresponse()
    if res.status == 204:
        success = True
    return success
