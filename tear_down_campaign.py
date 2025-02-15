import logging
import datetime
from config import *
from authentication_info import *
from ncc_workflow import *
from ncc_function import *
from ncc_campaign import *
from ncc_survey import *
from ncc_classification import *
from ncc_scorecard import *


def tear_down_campaign(ncc_location: str, ncc_token: str) -> str:
    """
    This function deletes entities (e.g., surveys) specific to the specified Nextiva Contact Center (NCC) campaign.
    """
    print()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Enter campaign name
    campaign_name = ""
    while campaign_name == "":
        print()
        campaign_name = input("Campaign name: ")
        if campaign_name == "":
            print()
            print("Invalid campaign name.")
        else:
            campaign_name = f"Test {campaign_name}"

    start_time = datetime.datetime.now()

    logging.info("Starting...")
    # Delete campaign
    campaign = search_campaigns_by_name(ncc_location, ncc_token, campaign_name)
    if campaign != {}:
        success = delete_campaign(ncc_location, ncc_token, campaign["_id"])
        if success:
            logging.info(f'Campaign "{campaign_name}" deleted.')
        else:
            logging.warning(f'Campaign "{campaign_name}" not deleted.')
    else:
        logging.warning(f'Campaign "{campaign_name}" not found.')

    # Delete workflow
    workflow = search_workflows(ncc_location, ncc_token, campaign_name)
    if workflow != {}:
        success = delete_workflow(ncc_location, ncc_token, workflow["_id"])
        if success:
            logging.info(f'Workflow "{campaign_name}" deleted.')
        else:
            logging.warning(f'Workflow "{campaign_name}" not deleted.')
    else:
        logging.warning(f'Workflow "{campaign_name}" not found.')

    # Delete functions
    functions = search_campaign_functions(ncc_location, ncc_token, campaign_name)
    if len(functions) > 0:
        for function in functions:
            success = delete_function(ncc_location, ncc_token, function["_id"])
            if success:
                logging.info(f'Function "{function["name"]}" deleted.')
            else:
                logging.warning(f'Function "{function["name"]}" not deleted.')
    else:
        logging.warning(f"No functions found with campaign name.")

    # Delete surveys
    surveys = search_campaign_surveys(ncc_location, ncc_token, campaign_name)
    if len(surveys) > 0:
        for survey in surveys:
            success = delete_survey(ncc_location, ncc_token, survey["_id"])
            if success:
                logging.info(f'Survey "{survey["name"]}" deleted.')
            else:
                logging.warning(f'Survey "{survey["name"]}" not deleted.')
    else:
        logging.warning(f"No surveys found with campaign name.")

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
                logging.warning(
                    f'Classification "{classification["name"]}" not deleted.'
                )
    else:
        logging.warning(f"No classifications found with campaign name.")

    # Delete scorecards
    scorecards = search_campaign_scorecards(ncc_location, ncc_token, campaign_name)
    if len(scorecards) > 0:
        for scorecard in scorecards:
            success = delete_scorecard(ncc_location, ncc_token, scorecard["_id"])
            if success:
                logging.info(f'Scorecard "{scorecard["name"]}" deleted.')
            else:
                logging.warning(f'Scorecard "{scorecard["name"]}" not deleted.')
    else:
        logging.warning(f"No scorecards found with campaign name.")

    duration = datetime.datetime.now() - start_time
    logging.info(f"Duration: {str(duration)}")
