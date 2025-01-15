import http.client
import urllib.parse
import json


def get_surveys(ncc_location: str, ncc_token: str) -> str:
    """
    This function fetches a list of surveys present on the Nextiva Contact Center tenant.
    """
    test_survey_ids = []
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
                    test_survey_ids.append(result["surveyId"])
    return test_survey_ids


def search_surveys(ncc_location: str, ncc_token: str, survey_name: str) -> str:
    """
    This function searches for an existing survey with the same name as the intended new survey.
    """
    survey_id = ""
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
                    survey_id = result["surveyId"]
                    break
    conn.close()
    return survey_id


def create_survey(
    ncc_location: str, ncc_token: str, survey_name: str, survey_body: dict
) -> str:
    """
    This function creates a survey with a specified name.
    """
    survey_id = ""
    conn = http.client.HTTPSConnection(ncc_location)
    payload = json.dumps(survey_body)
    headers = {
        "Authorization": ncc_token,
        "Content-Type": "application/json",
    }
    conn.request("POST", "/data/api/types/survey/", payload, headers)
    res = conn.getresponse()
    if res.status == 201:
        data = res.read().decode("utf-8")
        json_data = json.loads(data)
        survey_id = json_data["surveyId"]
    conn.close()
    return survey_id


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
