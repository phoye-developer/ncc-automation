import http.client
import urllib.parse
import json


def get_reports(ncc_location: str, ncc_token: str) -> list:
    """
    This function searches for an existing report with the same name as the intended new report.
    """
    reports = []
    conn = http.client.HTTPSConnection(ncc_location)
    payload = ""
    headers = {"Authorization": ncc_token}
    try:
        conn.request(
            "GET",
            f"/data/api/types/report",
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
                    reports.append(result)
    except:
        pass
    conn.close()
    return reports


def search_reports(ncc_location: str, ncc_token: str, report_name: str) -> dict:
    """
    This function searches for an existing report with the same name as the intended new report.
    """
    report = {}
    conn = http.client.HTTPSConnection(ncc_location)
    payload = ""
    headers = {"Authorization": ncc_token}
    url_encoded_name = urllib.parse.quote(report_name)
    try:
        conn.request(
            "GET",
            f"/data/api/types/report?q={url_encoded_name}",
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
                    if result["name"] == report_name:
                        report = result
                        break
    except:
        pass
    conn.close()
    return report


def create_report(ncc_location: str, ncc_token: str, report_body: dict) -> dict:
    """
    This function creates a report with a specified name.
    """
    report = {}
    conn = http.client.HTTPSConnection(ncc_location)
    payload = json.dumps(report_body)
    headers = {
        "Authorization": ncc_token,
        "Content-Type": "application/json",
    }
    try:
        conn.request("POST", "/data/api/types/report/", payload, headers)
        res = conn.getresponse()
        if res.status == 201:
            data = res.read().decode("utf-8")
            report = json.loads(data)
    except:
        pass
    conn.close()
    return report


def create_csat_report(
    ncc_location: str,
    ncc_token: str,
    report_name: str,
    report_range: str,
    csat_survey: dict,
    csat_campaign: dict,
) -> dict:
    """
    This function creates a report with a specified name.
    """
    report = {}
    conn = http.client.HTTPSConnection(ncc_location)
    payload = json.dumps(
        {
            "scheduleCsvSeparator": "",
            "timezone": "America/Phoenix",
            "range": {
                "type": report_range,
            },
            "totalQuery": "\n\n\n",
            "type": "GenericQuery",
            "scheduleExcludeHeaders": False,
            "scheduleApplyQuotesToAll": False,
            "reportuser": {"total": 0, "count": 0},
            "genericQuery": 'WITH\r\n  surveyResults AS (\r\n  SELECT\r\n    FORMAT_TIMESTAMP("%x %X", TIMESTAMP_MILLIS(createdAt), \'${timezone}\') AS start_time,\r\n    REPLACE(JSON_QUERY(object, "$.surveyResult.'
            + csat_survey["_id"]
            + '.relatedWorkitemId.value"), "\\"", "") AS related_workitem_id,\r\n    REPLACE(JSON_QUERY(object, "$.surveyResult.'
            + csat_survey["_id"]
            + '.resolved.value"), "\\"", "") AS resolved,\r\n    REPLACE(JSON_QUERY(object, "$.surveyResult.'
            + csat_survey["_id"]
            + '.satisfied.value"), "\\"", "") AS satisfied,\r\n    REPLACE(JSON_QUERY(object, "$.surveyResult.'
            + csat_survey["_id"]
            + '.friendly.value"), "\\"", "") AS friendly,\r\n    REPLACE(JSON_QUERY(object, "$.surveyResult.'
            + csat_survey["_id"]
            + '.wouldRecommend.value"), "\\"", "") AS would_recommend\r\n  FROM\r\n    `REPORTS_WORKITEMS`\r\n  WHERE\r\n    ${partitionTime}\r\n    AND campaigns = "'
            + csat_campaign["_id"]
            + '"\r\n    AND type = "Survey"\r\n    AND REPLACE(JSON_QUERY(object, "$.surveyResult.'
            + csat_survey["_id"]
            + '.relatedWorkitemId.value"), "\\"", "") IS NOT NULL\r\n    AND REPLACE(JSON_QUERY(object, "$.surveyResult.'
            + csat_survey["_id"]
            + '.relatedWorkitemId.value"), "\\"", "") != "undefined"\r\n    AND REPLACE(JSON_QUERY(object, "$.surveyResult.'
            + csat_survey["_id"]
            + '.relatedWorkitemId.value"), "\\"", "") != "workitem.data.relatedWorkitemId"\r\n    AND REPLACE(JSON_QUERY(object, "$.surveyResult.'
            + csat_survey["_id"]
            + '.satisfied.value"), "\\"", "") != "0"\r\n    AND REPLACE(JSON_QUERY(object, "$.surveyResult.'
            + csat_survey["_id"]
            + '.resolved.value"), "\\"", "") != ""\r\n    AND REPLACE(JSON_QUERY(object, "$.surveyResult.'
            + csat_survey["_id"]
            + '.friendly.value"), "\\"", "") != ""\r\n    AND REPLACE(JSON_QUERY(object, "$.surveyResult.'
            + csat_survey["_id"]
            + '.wouldRecommend.value"), "\\"", "") != ""),\r\n  workitems AS (\r\n  SELECT\r\n    id AS workitemId,\r\n    campaignName AS campaign_name,\r\n    channelType AS channel_type,\r\n    dispositionName AS disposition_name\r\n  FROM\r\n    `DATA_WORKITEMS`\r\n  WHERE\r\n    ${partitionTime}\r\n    AND createdAt between ${startTime} AND ${endTime}),\r\n  user_workitems AS (\r\n  SELECT\r\n    workitemId AS workitem_id,\r\n    userId AS user_id\r\n  FROM\r\n    `DATA_WORKITEMS_USERS`\r\n  WHERE\r\n    ${partitionTime}\r\n    AND createdAt between ${startTime} AND ${endTime}),\r\n  user_data AS (\r\n  SELECT\r\n    userId AS user_id,\r\n    firstName AS first_name,\r\n    lastName AS last_name\r\n  FROM\r\n    `user`\r\n  WHERE\r\n    userId in ${users})\r\nSELECT\r\n  surveyResults.start_time AS survey_start_time,\r\n  surveyResults.related_workitem_id AS workitem_id,\r\n  surveyResults.resolved,\r\n  surveyResults.satisfied,\r\n  surveyResults.friendly,\r\n  surveyResults.would_recommend,\r\n  workitems.campaign_name,\r\n  workitems.channel_type,\r\n  workitems.disposition_name,\r\n  user_data.first_name AS agent_first_name,\r\n  user_data.last_name AS agent_last_name\r\nFROM\r\n  surveyResults\r\nJOIN\r\n  workitems\r\nON\r\n  surveyResults.related_workitem_id = workitems.workitemId\r\nJOIN\r\n  user_workitems\r\nON\r\n  workitems.workitemId = user_workitems.workitem_id\r\nJOIN\r\n  user_data\r\nON\r\n  user_workitems.user_id = user_data.user_id\r\nLIMIT\r\n  1000',
            "localizations": {"name": {"en": {"language": "en", "value": report_name}}},
            "scheduleAvoidSendingIfNoData": False,
            "filters": {
                "supervisedUsers": True,
                "supervisedQueues": False,
                "supervisedCampaigns": False,
                "withCompleted": False,
                "withCallbacks": False,
                "withNew": False,
                "withMaxAttempts": False,
                "withFailed": False,
                "lastAgentOnly": False,
                "selectUsers": [],
            },
            "scheduleRawData": False,
            "name": report_name,
        }
    )
    headers = {
        "Authorization": ncc_token,
        "Content-Type": "application/json",
    }
    try:
        conn.request("POST", "/data/api/types/report/", payload, headers)
        res = conn.getresponse()
        if res.status == 201:
            data = res.read().decode("utf-8")
            report = json.loads(data)
    except:
        pass
    conn.close()
    return report


def delete_report(ncc_location: str, ncc_token: str, report_id: str) -> bool:
    """
    This function deletes a report with the specified report ID.
    """
    success = False
    conn = http.client.HTTPSConnection(ncc_location)
    payload = ""
    headers = {"Authorization": ncc_token}
    try:
        conn.request("DELETE", f"/data/api/types/report/{report_id}", payload, headers)
        res = conn.getresponse()
        if res.status == 204:
            success = True
    except:
        pass
    conn.close()
    return success
