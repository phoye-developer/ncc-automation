import logging
import datetime
from authentication_info import *
from config import *
from authentication_info import *
from ncc_workflow import *
from ncc_function import *
from ncc_campaign import *
from ncc_survey import *
from ncc_rest_call import *
from ncc_classification import *
from ncc_scorecard import *
from ncc_report import *


def tear_down_campaign(ncc_location: str, ncc_token: str, username: str):
    """
    This function deletes entities (e.g., surveys) specific to the specified Nextiva Contact Center (NCC) campaign.
    """

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    cancelled = False

    print()
    print('Enter "cancel" at any prompt to cancel.')

    # Enter campaign name
    campaign_name = ""
    while campaign_name == "":
        print()
        campaign_name = input("Campaign prefix: ")
        if campaign_name.lower() == "cancel":
            print()
            print("Operation cancelled.")
            cancelled = True
        elif campaign_name == "":
            print()
            print("Invalid campaign name.")

    if cancelled == False:

        print()
        start_time = datetime.datetime.now()

        logging.info("Starting...")

        # Delete campaigns
        campaigns_to_delete = []
        campaigns = get_campaigns(ncc_location, ncc_token)
        if len(campaigns) > 0:
            for campaign in campaigns:
                if str(campaign["name"]).startswith(campaign_name):
                    campaigns_to_delete.append(campaign)
        else:
            logging.warning(f"No campaigns found.")
        if len(campaigns_to_delete) > 0:
            for campaign_to_delete in campaigns_to_delete:
                success = delete_campaign(
                    ncc_location, ncc_token, campaign_to_delete["_id"]
                )
                if success:
                    logging.info(f'Campaign "{campaign_to_delete["name"]}" deleted.')
                else:
                    logging.error(
                        f'Campaign "{campaign_to_delete["name"]}" not deleted.'
                    )
        else:
            logging.warning(
                f'No campaigns with name "{campaign_name}" found for deletion.'
            )

        # Delete workflows
        workflows_to_delete = []
        workflows = get_workflows(ncc_location, ncc_token)
        if len(workflows) > 0:
            for workflow in workflows:
                if str(workflow["name"]).startswith(campaign_name):
                    workflows_to_delete.append(workflow)
        else:
            logging.warning(f"No workflows found.")
        if len(workflows_to_delete) > 0:
            for workflow_to_delete in workflows_to_delete:
                success = delete_workflow(
                    ncc_location, ncc_token, workflow_to_delete["_id"]
                )
                if success:
                    logging.info(f'Workflow "{workflow_to_delete["name"]}" deleted.')
                else:
                    logging.error(
                        f'Workflow "{workflow_to_delete["name"]}" not deleted.'
                    )
        else:
            logging.warning(
                f'No workflows with campaign name "{campaign_name}" found for deletion.'
            )

        # Delete surveys
        surveys = search_campaign_surveys(ncc_location, ncc_token, campaign_name)
        if len(surveys) > 0:
            for survey in surveys:
                success = delete_survey(ncc_location, ncc_token, survey["_id"])
                if success:
                    logging.info(f'Survey "{survey["name"]}" deleted.')
                else:
                    logging.error(f'Survey "{survey["name"]}" not deleted.')
        else:
            logging.warning(
                f'No surveys with campaign name "{campaign_name}" found for deletion.'
            )

        # Delete REST API objects
        rest_calls = search_campaign_rest_calls(ncc_location, ncc_token, campaign_name)
        if len(rest_calls) > 0:
            for rest_call in rest_calls:
                success = delete_rest_call(ncc_location, ncc_token, rest_call["_id"])
                if success:
                    logging.info(f'REST API Object "{rest_call["name"]}" deleted.')
                else:
                    logging.warning(
                        f'REST API object "{rest_call["name"]}" not deleted.'
                    )
        else:
            logging.warning(
                f'No REST API objects with campaign name "{campaign_name}" found for deletion.'
            )

        # Delete reports
        reports_to_delete = []
        reports = get_reports(ncc_location, ncc_token)
        if len(reports) > 0:
            for report in reports:
                if str(report["name"]).startswith(campaign_name):
                    reports_to_delete.append(report)
        else:
            logging.warning(f"No reports found.")
        if len(reports_to_delete) > 0:
            for report_to_delete in reports_to_delete:
                success = delete_report(
                    ncc_location, ncc_token, report_to_delete["_id"]
                )
                if success:
                    logging.info(f'Report "{report_to_delete["name"]}" deleted.')
                else:
                    logging.error(f'Report "{report_to_delete["name"]}" not deleted.')
        else:
            logging.warning(
                f'No reports with campaign name "{campaign_name}" found for deletion.'
            )

        duration = datetime.datetime.now() - start_time
        logging.info(f"Duration: {str(duration)}")
