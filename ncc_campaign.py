import http.client
import urllib.parse
import json


def search_campaigns_by_name(
    ncc_location: str, ncc_token: str, campaign_name: str
) -> dict:
    """
    This function searches for an existing campaign with the specified name.
    """
    campaign = {}
    conn = http.client.HTTPSConnection(ncc_location)
    payload = ""
    headers = {"Authorization": ncc_token}
    url_encoded_name = urllib.parse.quote(campaign_name)
    try:
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
    except:
        pass
    conn.close()
    return campaign


def search_campaigns_by_address(
    ncc_location: str, ncc_token: str, campaign_address: str
) -> bool:
    """
    This function searches for an existing campaign with the specified address.
    """
    success = False
    conn = http.client.HTTPSConnection(ncc_location)
    payload = ""
    headers = {"Authorization": ncc_token}
    try:
        conn.request(
            "GET",
            f"/data/api/types/campaign?q={campaign_address}",
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
                    if "addresses" in result:
                        addresses = result["addresses"]
                        for address in addresses:
                            if address == campaign_address:
                                success = True
                                break
    except:
        pass
    conn.close()
    return success


def create_campaign(
    ncc_location: str,
    ncc_token: str,
    campaign_name: str,
    user_survey_id: str,
    chat_survey_id: str,
    qm_survey_id: str,
    campaign_caller_id: str,
    workflow_id: str,
    real_time_transcription_service_id: str,
    gen_ai_service_id: str,
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
            "defaultOutbound": False,
            "useForSMS": True,
            "complianceRecordings": False,
            "loadLeadOnlyForThridPartySkill": False,
            "amdUnknownAsVoicemail": False,
            "useForProgressive": False,
            "generativeAIServiceId": gen_ai_service_id,
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
            "surveyId": user_survey_id,
            "useForEmail": False,
            "defaultExtension": False,
            "recordingEventsTranscription": True,
            "ftpFilenameFormat": "",
            "recordingAnalysisMaxDuration": "86400",
            "useForPredictive": False,
            "useForOutbound": True,
            "callerId": campaign_caller_id,
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
            "name": campaign_name,
        },
    )
    headers = {
        "Authorization": ncc_token,
        "Content-Type": "application/json",
    }
    try:
        conn.request("POST", "/data/api/types/campaign/", payload, headers)
        res = conn.getresponse()
        if res.status == 201:
            data = res.read().decode("utf-8")
            campaign = json.loads(data)
    except:
        pass
    conn.close()
    return campaign


def assign_address_to_campaign(
    ncc_location: str, ncc_token: str, campaign_address: str, campaign_id: str
) -> bool:
    success = False
    conn = http.client.HTTPSConnection(ncc_location)
    payload = json.dumps({"addresses": [campaign_address]})
    headers = {
        "Authorization": ncc_token,
        "Content-Type": "application/json",
    }
    try:
        conn.request(
            "PATCH", f"/data/api/types/campaign/{campaign_id}", payload, headers
        )
        res = conn.getresponse()
        if res.status == 200:
            success = True
    except:
        pass
    conn.close()
    return success


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
    try:
        conn.request(
            "PATCH", f"/data/api/types/campaign/{campaign_id}", payload, headers
        )
        res = conn.getresponse()
        if res.status == 200:
            success = True
    except:
        pass
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
    try:
        conn.request(
            "DELETE", f"/data/api/types/campaign/{campaign_id}", payload, headers
        )
        res = conn.getresponse()
        if res.status == 204:
            success = True
    except:
        pass
    conn.close()
    return success
