import http.client
import urllib.parse
import json


def get_campaigns(ncc_location: str, ncc_token: str) -> list:
    """
    This function fetches a list of campaigns present on the Nextiva Contact Center tenant.
    """
    campaigns = []
    conn = http.client.HTTPSConnection(ncc_location)
    payload = ""
    headers = {"Authorization": ncc_token}
    conn.request("GET", "/data/api/types/campaign?q=Test%20", payload, headers)
    res = conn.getresponse()
    if res.status == 200:
        data = res.read().decode("utf-8")
        json_data = json.loads(data)
        total = json_data["total"]
        if total > 0:
            results = json_data["objects"]
            for result in results:
                campaign_name = result["name"]
                if campaign_name[0:5] == "Test ":
                    campaigns.append(result)
    return campaigns


def search_campaigns(ncc_location: str, ncc_token: str, campaign_name: str) -> dict:
    """
    This function searches for an existing campaign with the specified name.
    """
    campaign = {}
    conn = http.client.HTTPSConnection(ncc_location)
    payload = ""
    headers = {"Authorization": ncc_token}
    url_encoded_name = urllib.parse.quote(campaign_name)
    conn.request(
        "GET",
        f"/data/api/types/campaign?q={url_encoded_name}",
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
                if result["name"] == campaign_name:
                    campaign = result
                    break
    conn.close()
    return campaign


def create_campaign(
    ncc_location: str,
    ncc_token: str,
    campaign_name: str,
    user_survey_id: str,
    chat_survey_id: str,
    qm_survey_id: str,
    workflow_id: str,
    real_time_transcription_service_id: str,
) -> dict:
    """
    This function creates a campaign with the specified name.
    """
    campaign = {}
    conn = http.client.HTTPSConnection(ncc_location)
    payload = json.dumps(
        {
            "realtimeAnalysisServiceId": [real_time_transcription_service_id],
            "smsFromAddress": "",
            "recordingAnalysisPercentage": 100,
            "userRecordings": False,
            "recordingAnalysisMinDuration": "0",
            "recordingAnalysisLanguages": "",
            "recordingAnalysisServiceId": real_time_transcription_service_id,
            "qualityMonitoringSurveyId": qm_survey_id,
            "defaultOutbound": True,
            "useForSMS": True,
            "complianceRecordings": False,
            "loadLeadOnlyForThridPartySkill": False,
            "amdUnknownAsVoicemail": False,
            "useForProgressive": False,
            "generativeAIServiceId": "641c589f9535e44e4b8b0c67",
            "filterOnLeads": "",
            "recordingAnalysisEndTime": 1439,
            "localizations": {
                "name": {"en": {"language": "en", "value": campaign_name}}
            },
            "useForExtension": True,
            "spoofANICompanyDirectory": False,
            "complianceRecordingsFileNameFormat": "",
            "outboundANI": False,
            "userRecordingsFileNameFormat": "",
            "addresses": [],
            "surveyId": user_survey_id,
            "useForEmail": False,
            "defaultExtension": True,
            "recordingEventsTranscription": True,
            "ftpFilenameFormat": "",
            "recordingAnalysisMaxDuration": "86400",
            "useForPredictive": False,
            "useForOutbound": True,
            "callerId": "",
            "priorityCallbacks": False,
            "recordingPercentage": 100,
            "description": "Voice, Chat, SMS",
            "holdMusicUrl": "http://twimlets.com/holdmusic?Bucket=music-acoustic&",
            "emailFromAddress": "",
            "disableImageOnMMS": False,
            "preSurveyId": chat_survey_id,
            "enableRealtimeTranscription": True,
            "applyRecordingConsent": False,
            "agentCallbacksAsPriority": False,
            "useForFax": False,
            "disableRecordingOnTwoParty": False,
            "workflowId": workflow_id,
            "expansions": {
                "realtimeAnalysisServiceId": {
                    "localizations": {
                        "name": {"en": "Test Deepgram Real-Time Transcription"}
                    }
                }
            },
        },
    )
    headers = {
        "Authorization": ncc_token,
        "Content-Type": "application/json",
    }
    conn.request("POST", "/data/api/types/campaign/", payload, headers)
    res = conn.getresponse()
    if res.status == 201:
        data = res.read().decode("utf-8")
        campaign = json.loads(data)
    return campaign


def assign_survey_to_campaign(
    ncc_location: str, ncc_token: str, survey_id: str, campaign_id: str
) -> bool:
    success = False
    conn = http.client.HTTPSConnection(ncc_location)
    payload = json.dumps({"surveyId": survey_id})
    headers = {
        "Authorization": ncc_token,
        "Content-Type": "application/json",
    }
    conn.request("PATCH", f"/data/api/types/campaign/{campaign_id}", payload, headers)
    res = conn.getresponse()
    if res.status == 200:
        success = True
    conn.close()
    return success


def delete_campaign(ncc_location: str, ncc_token: str, campaign_id: str) -> bool:
    """
    This function deletes a campaign with the specified campaign ID.
    """
    success = False
    conn = http.client.HTTPSConnection(ncc_location)
    payload = ""
    headers = {"Authorization": ncc_token}
    conn.request("DELETE", f"/data/api/types/campaign/{campaign_id}", payload, headers)
    res = conn.getresponse()
    if res.status == 204:
        success = True
    return success
