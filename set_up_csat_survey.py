import logging
import datetime
from authentication_info import *
from datadog import *
from ncc_survey import *
from ncc_workflow import *
from ncc_campaign import *
from ncc_report import *


def set_up_csat_survey(
    ncc_location: str,
    ncc_token: str,
    username: str,
    campaign_name: str,
    business_name: str,
):
    """
    This function creates a survey, workflow, campaign, and report in Nextiva Contact Center (NCC) facilitate a CSAT survey.
    """

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    start_time = datetime.datetime.now()

    logging.info("Starting...")
    # Find survey theme
    surveys = search_campaign_surveys(ncc_location, ncc_token, campaign_name)
    if len(surveys) > 0:
        for survey in surveys:
            if "surveythemeId" in survey:
                survey_theme_id = survey["surveythemeId"]
            if "tenantId" in survey:
                tenant_id = survey["tenantId"]
    else:
        post_datadog_event(
            dd_api_key,
            dd_application_key,
            username,
            "warning",
            "normal",
            "Survey Lookup Failed",
            f"Survey theme or tenant ID not found.",
            ["featuresetup"],
        )
        logging.warning("Survey theme or tenant ID not found.")

    # Create CSAT survey
    csat_survey = search_surveys(
        ncc_location,
        ncc_token,
        f"{campaign_name} - CSAT",
    )
    if csat_survey == {}:
        if survey_theme_id != "":
            csat_survey = create_csat_survey(
                ncc_location,
                ncc_token,
                f"{campaign_name} - CSAT",
                survey_theme_id,
                business_name,
            )
            if csat_survey != {}:
                post_datadog_event(
                    dd_api_key,
                    dd_application_key,
                    username,
                    "success",
                    "normal",
                    "Survey Creation Successful",
                    f'Survey "{campaign_name} - CSAT" created.',
                    ["featuresetup"],
                )
                logging.info(f'Survey "{campaign_name} - CSAT" created.')
            else:
                post_datadog_event(
                    dd_api_key,
                    dd_application_key,
                    username,
                    "error",
                    "normal",
                    "Survey Creation Failed",
                    f'Survey "{campaign_name} - CSAT" not created.',
                    ["featuresetup"],
                )
                logging.error(f'Survey "{campaign_name} - CSAT" not created.')
        else:
            post_datadog_event(
                dd_api_key,
                dd_application_key,
                username,
                "warning",
                "normal",
                "Survey Creation Failed",
                f"Insufficient data to create survey.",
                ["featuresetup"],
            )
            logging.warning("Insufficient data to create survey.")
    else:
        logging.info(f'Survey "{campaign_name} - CSAT" already exists')

    #  Create CSAT workflow
    csat_workflow = search_workflows(
        ncc_location,
        ncc_token,
        f"{campaign_name} - CSAT",
    )
    if csat_workflow == {}:
        if csat_survey != {}:
            csat_workflow = create_csat_workflow(
                ncc_location, ncc_token, f"{campaign_name} - CSAT"
            )
            if csat_workflow != {}:
                logging.info(f'Workflow "{campaign_name} - CSAT" created.')
            else:
                post_datadog_event(
                    dd_api_key,
                    dd_application_key,
                    username,
                    "error",
                    "normal",
                    "Workflow Creation Failed",
                    f'Workflow "{campaign_name} - CSAT" not created.',
                    ["featuresetup"],
                )
                logging.error(f'Workflow "{campaign_name} - CSAT" not created.')
        else:
            post_datadog_event(
                dd_api_key,
                dd_application_key,
                username,
                "warning",
                "normal",
                "Workflow Creation Failed",
                "Insufficient data to create workflow.",
                ["featuresetup"],
            )
            logging.warning("Insufficient data to create workflow.")
    else:
        logging.info(f'Workflow "{campaign_name} - CSAT" already exists.')

    # Create CSAT campaign
    csat_campaign = search_campaigns_by_name(
        ncc_location,
        ncc_token,
        f"{campaign_name} - CSAT",
    )
    if csat_campaign == {}:
        if "_id" in csat_survey and "_id" in csat_workflow:
            csat_campaign = create_csat_campaign(
                ncc_location,
                ncc_token,
                f"{campaign_name} - CSAT",
                csat_workflow,
                csat_survey,
            )
            if csat_campaign != {}:
                logging.info(f'Campaign "{campaign_name} - CSAT" created.')
            else:
                post_datadog_event(
                    dd_api_key,
                    dd_application_key,
                    username,
                    "error",
                    "normal",
                    "Campaign Creation Failed",
                    f'Campaign "{campaign_name} - CSAT" not created.',
                    ["featuresetup"],
                )
                logging.error(f'Campaign "{campaign_name} - CSAT" not created.')
        else:
            post_datadog_event(
                dd_api_key,
                dd_application_key,
                username,
                "warning",
                "normal",
                "Campaign Creation Failed",
                "Insufficient data to create campaign.",
                ["featuresetup"],
            )
            logging.warning("Insufficient data to create campaign.")
    else:
        logging.info(f'Campaign "{campaign_name} - CSAT" already exists.')

    # Find "main" campaign
    campaign = search_campaigns_by_name(ncc_location, ncc_token, campaign_name)
    if campaign == {}:
        post_datadog_event(
            dd_api_key,
            dd_application_key,
            username,
            "warning",
            "normal",
            "Campaign Search Failed",
            f'Campaign "{campaign_name}" not found.',
            ["featuresetup"],
        )
        logging.warning(f'Campaign "{campaign_name}" not found.')

    # Update "main" workflow
    workflow = search_workflows(ncc_location, ncc_token, campaign_name)
    if workflow != {}:
        if "_id" in csat_campaign and "callerId" in campaign and tenant_id != "":
            states = workflow["states"]
            for key, value in enumerate(states):
                if workflow["states"][value]["name"] == "End State":
                    actions = workflow["states"][value]["actions"]
                    found = False
                    for action in actions:
                        if action["name"] == "Send Survey Link via SMS":
                            found = True
                            break
                    if found == False:
                        actions.insert(
                            -1,
                            {
                                "name": "Send Survey Link via SMS",
                                "description": "Thank you for... (InboundCall or InboundSMS)",
                                "properties": {
                                    "description": "Thank you for... (InboundCall or InboundSMS)",
                                    "message": "Thank you for contacting us. To take a brief survey, go to https://login.thrio.io/survey/?tenant="
                                    + tenant_id
                                    + "&campaignId="
                                    + csat_campaign["_id"]
                                    + "&context=%7B%22relatedWorkitemId%22%3A%22${workitem.workitemId}%22%7D. We look forward to hearing from you!",
                                    "toAddress": "workitem.from",
                                    "fromAddress": "workitem.to",
                                    "createNewWorkitem": False,
                                    "condition": {
                                        "conditionType": "OR",
                                        "customCondition": "",
                                        "expressions": [
                                            {
                                                "leftExpression": "workitem.type",
                                                "operator": "==",
                                                "rightExpression": "'InboundCall'",
                                            },
                                            {
                                                "leftExpression": "workitem.type",
                                                "operator": "==",
                                                "rightExpression": "'InboundSMS'",
                                            },
                                        ],
                                    },
                                },
                                "type": "smsmessageconsumer",
                                "_selected": False,
                                "id": "refId1740784151527",
                                "icon": "icon-ai-message",
                            },
                        )
                        actions.insert(
                            -1,
                            {
                                "name": "Send Survey Link via SMS",
                                "description": "Thank you for... (Chat)",
                                "properties": {
                                    "description": "Thank you for... (Chat)",
                                    "message": "Thank you for contacting us. To take a brief survey, go to https://login.thrio.io/survey/?tenant="
                                    + tenant_id
                                    + "&campaignId="
                                    + csat_campaign["_id"]
                                    + "&context=%7B%22relatedWorkitemId%22%3A%22${workitem.workitemId}%22%7D. We look forward to hearing from you!",
                                    "toAddress": "workitem.data.context.consumerData.phone",
                                    "fromAddress": f"'{campaign["callerId"]}'",
                                    "createNewWorkitem": False,
                                    "condition": {
                                        "conditionType": "AND",
                                        "customCondition": "",
                                        "expressions": [
                                            {
                                                "leftExpression": "workitem.type",
                                                "operator": "==",
                                                "rightExpression": "'Chat'",
                                            }
                                        ],
                                    },
                                },
                                "type": "smsmessageconsumer",
                                "_selected": True,
                                "id": "refId1741450628018",
                                "icon": "icon-ai-message",
                            },
                        )
                        success = update_workflow(
                            ncc_location, ncc_token, workflow["_id"], workflow
                        )
                        if success:
                            logging.info(f'Workflow "{campaign_name}" updated.')
                        else:
                            post_datadog_event(
                                dd_api_key,
                                dd_application_key,
                                username,
                                "error",
                                "normal",
                                "Workflow Update Failed",
                                f'Workflow "{campaign_name}" not updated due to unspecified error.',
                                ["featuresetup"],
                            )
                            logging.error(
                                f'Workflow "{campaign_name}" not updated due to unspecified error.'
                            )
                    else:
                        logging.info(f'Workflow "{campaign_name}" already updated.')
        else:
            post_datadog_event(
                dd_api_key,
                dd_application_key,
                username,
                "warning",
                "normal",
                "Workflow Update Failed",
                f"Insufficient data to update workflow.",
                ["featuresetup"],
            )
            logging.warning(f"Insufficient data to update workflow.")
    else:
        post_datadog_event(
            dd_api_key,
            dd_application_key,
            username,
            "warning",
            "normal",
            "Workflow Update Failed",
            f'Workflow "{campaign_name}" not found for updating.',
            ["featuresetup"],
        )
        logging.warning(f'Workflow "{campaign_name}" not found for updating.')

    # Create CSAT report
    csat_report = search_reports(
        ncc_location,
        ncc_token,
        f"{campaign_name} - CSAT",
    )
    if csat_report == {}:
        if csat_survey != {} and csat_campaign != {}:
            csat_report = create_csat_report(
                ncc_location,
                ncc_token,
                f"{campaign_name} - CSAT",
                "today",
                csat_survey,
                csat_campaign,
            )
            if csat_report != {}:
                logging.info(f'Report "{campaign_name} - CSAT" created')
            else:
                post_datadog_event(
                    dd_api_key,
                    dd_application_key,
                    username,
                    "error",
                    "normal",
                    "Report Creation Failed",
                    f'Report "{campaign_name} - CSAT" not created.',
                    ["featuresetup"],
                )
                logging.error(f'Report "{campaign_name} - CSAT" not created.')
        else:
            post_datadog_event(
                dd_api_key,
                dd_application_key,
                username,
                "warning",
                "normal",
                "Report Creation Failed",
                "Insufficient data to create report.",
                ["featuresetup"],
            )
            logging.warning("Insufficient data to create report.")
    else:
        logging.info(f'Report "{campaign_name} - CSAT" already exists.')

    duration = datetime.datetime.now() - start_time
    logging.info(f"Duration: {str(duration)}")
