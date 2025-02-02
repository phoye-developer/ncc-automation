import http.client
import urllib.parse
import json


def get_reports(ncc_location: str, ncc_token: str) -> list:
    """
    This function fetches a list of reports present on the Nextiva Contact Center tenant.
    """
    reports = []
    conn = http.client.HTTPSConnection(ncc_location)
    payload = ""
    headers = {"Authorization": ncc_token}
    conn.request("GET", "/data/api/types/report?q=Test%20", payload, headers)
    res = conn.getresponse()
    if res.status == 200:
        data = res.read().decode("utf-8")
        json_data = json.loads(data)
        total = json_data["total"]
        if total > 0:
            results = json_data["objects"]
            for result in results:
                report_name = result["name"]
                if report_name[0:5] == "Test ":
                    reports.append(result)
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
    conn.request("POST", "/data/api/types/report/", payload, headers)
    res = conn.getresponse()
    if res.status == 201:
        data = res.read().decode("utf-8")
        report = json.loads(data)
    conn.close()
    return report


def assign_rest_call_to_dispositon(
    ncc_location: str, ncc_token: str, rest_call_id: str, report_id: str
) -> bool:
    success = False
    conn = http.client.HTTPSConnection(ncc_location)
    payload = json.dumps({"restcallId": rest_call_id})
    headers = {"Authorization": ncc_token, "Content-Type": "application/json"}
    conn.request("PATCH", f"/data/api/types/report/{report_id}", payload, headers)
    res = conn.getresponse()
    if res.status == 200:
        success = True
    conn.close()
    return success


def delete_report(ncc_location: str, ncc_token: str, report_id: str) -> bool:
    """
    This function deletes a report with the specified report ID.
    """
    success = False
    conn = http.client.HTTPSConnection(ncc_location)
    payload = ""
    headers = {"Authorization": ncc_token}
    conn.request("DELETE", f"/data/api/types/report/{report_id}", payload, headers)
    res = conn.getresponse()
    if res.status == 204:
        success = True
    return success
