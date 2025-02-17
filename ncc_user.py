import http.client
import urllib.parse
import json


def get_users(ncc_location: str, ncc_token: str, user_profile_id: str) -> list:
    """
    This function fetches a list of users present on the Nextiva Contact Center (NCC) tenant.
    """
    users = []
    conn = http.client.HTTPSConnection(ncc_location)
    payload = ""
    headers = {"Authorization": ncc_token}
    try:
        conn.request("GET", "/data/api/types/user", payload, headers)
        res = conn.getresponse()
        if res.status == 200:
            data = res.read().decode("utf-8")
            json_data = json.loads(data)
            total = json_data["total"]
            if total > 0:
                results = json_data["objects"]
                for result in results:
                    if result["userProfileId"] == user_profile_id:
                        users.append(result)
    except:
        pass
    conn.close()
    return users


def search_users(
    ncc_location: str, ncc_token: str, first_name: str, last_name: str
) -> dict:
    """
    This function searches for an existing user with the same username as the intended new user.
    """
    user = {}
    conn = http.client.HTTPSConnection(ncc_location)
    payload = ""
    headers = {"Authorization": ncc_token}
    url_encoded_name = urllib.parse.quote(first_name)
    try:
        conn.request(
            "GET",
            f"/data/api/types/user?q={url_encoded_name}",
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
                    if (
                        result["firstName"] == first_name
                        and result["lastName"] == last_name
                    ):
                        user = result
                        break
    except:
        pass
    conn.close()
    return user


def create_user(
    ncc_location: str,
    ncc_token: str,
    first_name: str,
    last_name: str,
    email: str,
    user_profile_id: str,
):
    """
    This function creates a new user in Nextiva Contact Center (NCC).
    """
    user = {}
    conn = http.client.HTTPSConnection(ncc_location)
    payload = json.dumps(
        {
            "recordingAnalysisPercentage": 100,
            "outboundExtensionCallDurationNotification": False,
            "pbxUser": False,
            "hideInDirectory": False,
            "hideInCompanyDirectory": False,
            "password": "",
            "socialDurationNotification": False,
            "outboundCallDurationNotification": False,
            "inboundCallHoldNotification": False,
            "chatWelcome": "",
            "dialpadMode": "inline",
            "inboundSMSDurationNotification": False,
            "userProfileId": user_profile_id,
            "lastName": last_name,
            "acdAutoLogin": False,
            "inboundEmailDurationNotification": False,
            "enabled": True,
            "predictiveSMSDurationNotification": False,
            "outboundSMSDurationNotification": False,
            "scrubOnDial": False,
            "outboundCallHoldNotification": False,
            "credentialsNonExpired": False,
            "disableDisposition": "off",
            "allowClientTracing": False,
            "disableEmailNotification": False,
            "enableHoldWebNotification": False,
            "ringPhoneOnOffer": False,
            "alwaysDurationWebNotification": False,
            "inboundExtensionCallDurationNotification": False,
            "confirmDisposition": "off",
            "contentType": "image/jpeg",
            "predictiveCallDurationNotification": False,
            "verifyConsentOnSMS": False,
            "chatDurationNotification": False,
            "callFailedNotification": False,
            "allowAcdChanges": False,
            "firstName": first_name,
            "telephony": {
                "useSipEndpoint": False,
                "workOffHook": False,
                "type": "WEBRTC",
            },
            "name": f"{first_name} {last_name}",
            "acdAutoAccept": False,
            "outboundEmailDurationNotification": False,
            "disableStartRecording": False,
            "voicemailDropFilename": "",
            "timezone": "America/Phoenix",
            "verifyConsentOnDial": False,
            "pseudonym": "",
            "disableStopRecording": False,
            "oAuthProfileAssignmentFromExternalRole": False,
            "useSideBarHeader": "userProfile",
            "showWebrtcNotification": False,
            "dispositionNotification": False,
            "progressiveCallDurationNotification": False,
            "allowServerTracing": False,
            "alwaysHoldWebNotification": False,
            "inboundCallDurationNotification": False,
            "enableRealtimeTranscription": "on",
            "dialConfirmation": False,
            "enableDurationWebNotification": False,
            "ringOnLogout": False,
            "username": email,
        }
    )
    headers = {
        "Authorization": ncc_token,
        "Content-Type": "application/json",
    }
    try:
        conn.request("POST", "/data/api/types/user", payload, headers)
        res = conn.getresponse()
        if res.status == 201:
            data = res.read().decode("utf-8")
            user = json.loads(data)
    except:
        pass
    conn.close()
    return user


def delete_user(ncc_location: str, ncc_token: str, user_id: str) -> bool:
    """
    This function deletes a user with the specified user ID.
    """
    success = False
    conn = http.client.HTTPSConnection(ncc_location)
    payload = ""
    headers = {"Authorization": ncc_token}
    try:
        conn.request("DELETE", f"/data/api/types/user/{user_id}", payload, headers)
        res = conn.getresponse()
        if res.status == 204:
            success = True
    except:
        pass
    conn.close()
    return success
