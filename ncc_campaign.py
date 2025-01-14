import http.client
import urllib.parse
import json


def search_campaigns(ncc_location: str, ncc_token: str, campaign_name: str) -> str:
    """
    This function searches for an existing campaign with the specified name.
    """
    campaign_id = ""
    conn = http.client.HTTPSConnection(ncc_location)
    payload = ""
    headers = {"Authorization": ncc_token}
    url_encoded_campaign_name = urllib.parse.quote(campaign_name)
    conn.request(
        "GET",
        f"/data/api/types/campaign?q={url_encoded_campaign_name}",
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
                    campaign_id = result["campaignId"]
                    break
    conn.close()
    return campaign_id


def create_campaign(
    ncc_location: str,
    ncc_token: str,
    campaign_name: str,
    workflow_id: str,
    real_time_transcription_service_id: str,
) -> str:
    """
    This function creates a campaign with the specified name.
    """
    campaign_id = ""
    conn = http.client.HTTPSConnection(ncc_location)
    payload = json.dumps(
        {
            "realtimeAnalysisServiceId": [real_time_transcription_service_id],
            "smsFromAddress": "",
            "recordingAnalysisPercentage": 100,
            "userRecordings": False,
            "recordingAnalysisMinDuration": "0",
            "recordingAnalysisLanguages": "",
            "recordingAnalysisServiceId": "62f5f778a4a0a35b078738f7",
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
                "name": {"en": {"language": "en", "value": campaign_name}},
                "description": {"en": {"language": "en", "value": "Voice, Chat, SMS"}},
            },
            "useForExtension": True,
            "spoofANICompanyDirectory": False,
            "complianceRecordingsFileNameFormat": "",
            "outboundANI": False,
            "userRecordingsFileNameFormat": "",
            "addresses": [],
            "surveyId": "66c540b6c1e79a57d4c4b947",
            "useForEmail": False,
            "defaultExtension": True,
            "recordingEventsTranscription": True,
            "ftpFilenameFormat": "",
            "recordingAnalysisMaxDuration": "86400",
            "useForPredictive": False,
            "name": campaign_name,
            "useForOutbound": True,
            "callerId": "+16232590432",
            "priorityCallbacks": False,
            "recordingPercentage": 100,
            "description": "Voice, Chat, SMS",
            "holdMusicUrl": "http://twimlets.com/holdmusic?Bucket=music-acoustic&",
            "emailFromAddress": "",
            "disableImageOnMMS": False,
            "preSurveyId": "675b506895da237375b51a01",
            "enableRealtimeTranscription": True,
            "applyRecordingConsent": False,
            "agentCallbacksAsPriority": False,
            "useForFax": False,
            "disableRecordingOnTwoParty": False,
            "workflowId": workflow_id,
        }
    )
    headers = {
        "Authorization": ncc_token,
        "Content-Type": "application/json",
    }
    conn.request("POST", "/data/api/types/campaign/", payload, headers)
    res = conn.getresponse()
    if res.status == 201:
        data = res.read().decode("utf-8")
        json_data = json.loads(data)
        campaign_id = json_data["campaignId"]
    return campaign_id


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
