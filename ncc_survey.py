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
    conn.request("GET", f"/data/api/types/survey/{survey_id}", payload, headers)
    res = conn.getresponse()
    if res.status == 200:
        data = res.read().decode("utf-8")
        survey = json.loads(data)
    return survey


def get_surveys(ncc_location: str, ncc_token: str) -> list:
    """
    This function fetches a list of surveys present on the Nextiva Contact Center tenant.
    """
    surveys = []
    conn = http.client.HTTPSConnection(ncc_location)
    payload = ""
    headers = {"Authorization": ncc_token}
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
    conn.close()
    return survey


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
    conn.request("POST", "/data/api/types/survey/", payload, headers)
    res = conn.getresponse()
    if res.status == 201:
        data = res.read().decode("utf-8")
        survey = json.loads(data)
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
        conn.request(
            "PATCH",
            f"/data/api/types/survey/{survey_id}",
            payload,
            headers,
        )
        res = conn.getresponse()
        if res.status == 200:
            success = True
    return success


def delete_survey(ncc_location: str, ncc_token: str, survey_id: str) -> bool:
    """
    This function deletes a survey with the specified survey ID.
    """
    success = False
    conn = http.client.HTTPSConnection(ncc_location)
    payload = ""
    headers = {"Authorization": ncc_token}
    conn.request("DELETE", f"/data/api/types/survey/{survey_id}", payload, headers)
    res = conn.getresponse()
    if res.status == 204:
        success = True
    return success
