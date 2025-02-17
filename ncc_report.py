import http.client
import urllib.parse
import json


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
