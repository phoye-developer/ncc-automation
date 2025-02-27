import logging
import datetime
from datadog import *
from authentication_info import *
from config import *
from authentication_info import *
from ncc_workflow import *
from ncc_function import *
from ncc_campaign import *
from ncc_survey import *
from ncc_classification import *
from ncc_scorecard import *


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
        campaign_name = input("Campaign name: ")
        if campaign_name.lower() == "cancel":
            post_datadog_event(
                dd_api_key,
                dd_application_key,
                username,
                "warning",
                "normal",
                "Campaign Teardown Cancelled",
                f'User "{username}" cancelled campaign teardown.',
                ["campaignteardown"],
            )
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
        # Delete campaign
        campaign = search_campaigns_by_name(ncc_location, ncc_token, campaign_name)
        if campaign != {}:
            success = delete_campaign(ncc_location, ncc_token, campaign["_id"])
            if success:
                post_datadog_event(
                    dd_api_key,
                    dd_application_key,
                    username,
                    "success",
                    "normal",
                    "Campaign Teardown Successful",
                    f'Campaign "{campaign_name}" deleted.',
                    ["campaignteardown"],
                )
                logging.info(f'Campaign "{campaign_name}" deleted.')
            else:
                post_datadog_event(
                    dd_api_key,
                    dd_application_key,
                    username,
                    "error",
                    "normal",
                    "Campaign Teardown Failed",
                    f'Campaign "{campaign_name}" not deleted.',
                    ["campaignteardown"],
                )
                logging.error(f'Campaign "{campaign_name}" not deleted.')
        else:
            post_datadog_event(
                dd_api_key,
                dd_application_key,
                username,
                "warning",
                "normal",
                "Campaign Teardown Failed",
                f'Campaign "{campaign_name}" not found for deletion.',
                ["campaignteardown"],
            )
            logging.warning(f'Campaign "{campaign_name}" not found for deletion.')

        # Delete workflow
        workflow = search_workflows(ncc_location, ncc_token, campaign_name)
        if workflow != {}:
            success = delete_workflow(ncc_location, ncc_token, workflow["_id"])
            if success:
                logging.info(f'Workflow "{campaign_name}" deleted.')
            else:
                post_datadog_event(
                    dd_api_key,
                    dd_application_key,
                    username,
                    "error",
                    "normal",
                    "Workflow Teardown Failed",
                    f'Workflow "{campaign_name}" not deleted.',
                    ["campaignteardown"],
                )
                logging.error(f'Workflow "{campaign_name}" not deleted.')
        else:
            post_datadog_event(
                dd_api_key,
                dd_application_key,
                username,
                "warning",
                "normal",
                "Workflow Teardown Failed",
                f'Workflow "{campaign_name}" not found for deletion.',
                ["campaignteardown"],
            )
            logging.warning(f'Workflow "{campaign_name}" not found.')

        # Delete functions
        functions = search_campaign_functions(ncc_location, ncc_token, campaign_name)
        if len(functions) > 0:
            for function in functions:
                success = delete_function(ncc_location, ncc_token, function["_id"])
                if success:
                    logging.info(f'Function "{function["name"]}" deleted.')
                else:
                    post_datadog_event(
                        dd_api_key,
                        dd_application_key,
                        username,
                        "error",
                        "normal",
                        "Function Teardown Failed",
                        f'Function "{function["name"]}" not deleted.',
                        ["campaignteardown"],
                    )
                    logging.error(f'Function "{function["name"]}" not deleted.')
        else:
            post_datadog_event(
                dd_api_key,
                dd_application_key,
                username,
                "warning",
                "normal",
                "Function Teardown Failed",
                f'No functions with campaign name "{campaign_name}" found for deletion.',
                ["campaignteardown"],
            )
            logging.warning(
                f'No functions with campaign name "{campaign_name}" found for deletion.'
            )

        # Delete surveys
        surveys = search_campaign_surveys(ncc_location, ncc_token, campaign_name)
        if len(surveys) > 0:
            for survey in surveys:
                success = delete_survey(ncc_location, ncc_token, survey["_id"])
                if success:
                    logging.info(f'Survey "{survey["name"]}" deleted.')
                else:
                    post_datadog_event(
                        dd_api_key,
                        dd_application_key,
                        username,
                        "error",
                        "normal",
                        "Survey Teardown Failed",
                        f'Survey "{survey["name"]}" not deleted.',
                        ["campaignteardown"],
                    )
                    logging.error(f'Survey "{survey["name"]}" not deleted.')
        else:
            post_datadog_event(
                dd_api_key,
                dd_application_key,
                username,
                "warning",
                "normal",
                "Survey Teardown Failed",
                f'No surveys with campaign name "{campaign_name}" found for deletion.',
                ["campaignteardown"],
            )
            logging.warning(
                f'No surveys with campaign name "{campaign_name}" found for deletion.'
            )

        # Delete classifications
        classifications = search_campaign_classifications(
            ncc_location, ncc_token, campaign_name
        )
        if len(classifications) > 0:
            for classification in classifications:
                success = delete_classification(
                    ncc_location, ncc_token, classification["_id"]
                )
                if success:
                    logging.info(f'Classification "{classification["name"]}" deleted.')
                else:
                    post_datadog_event(
                        dd_api_key,
                        dd_application_key,
                        username,
                        "error",
                        "normal",
                        "Classification Teardown Failed",
                        f'Classification "{classification["name"]}" not deleted.',
                        ["campaignteardown"],
                    )
                    logging.error(
                        f'Classification "{classification["name"]}" not deleted.'
                    )
        else:
            post_datadog_event(
                dd_api_key,
                dd_application_key,
                username,
                "warning",
                "normal",
                "Classification Teardown Failed",
                f'No classifications with campaign name "{campaign_name}" found for deletion.',
                ["campaignteardown"],
            )
            logging.warning(
                f'No classifications with campaign name "{campaign_name}" found for deletion.'
            )

        # Delete scorecards
        scorecards = search_campaign_scorecards(ncc_location, ncc_token, campaign_name)
        if len(scorecards) > 0:
            for scorecard in scorecards:
                success = delete_scorecard(ncc_location, ncc_token, scorecard["_id"])
                if success:
                    logging.info(f'Scorecard "{scorecard["name"]}" deleted.')
                else:
                    post_datadog_event(
                        dd_api_key,
                        dd_application_key,
                        username,
                        "error",
                        "normal",
                        "Scorecard Teardown Failed",
                        f'Scorecard "{scorecard["name"]}" not deleted.',
                        ["campaignteardown"],
                    )
                    logging.error(f'Scorecard "{scorecard["name"]}" not deleted.')
        else:
            post_datadog_event(
                dd_api_key,
                dd_application_key,
                username,
                "warning",
                "normal",
                "Scorecard Teardown Failed",
                f'No scorecard with campaign name "{campaign_name}" found for deletion.',
                ["campaignteardown"],
            )
            logging.warning(
                f'No scorecard with campaign name "{campaign_name}" found for deletion.'
            )

        duration = datetime.datetime.now() - start_time
        logging.info(f"Duration: {str(duration)}")
