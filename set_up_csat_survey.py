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
    csat_survey_name: str,
    campaign_name: str,
    campaign_caller_id: str,
):
    """
    This function performs the setup of a survey, report, and other entities related to a CSAT survey in Nextiva Contact Center (NCC).
    """

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    start_time = datetime.datetime.now()

    logging.info("Starting...")
    # Get survey theme
    survey_theme_id = ""
    surveys = search_campaign_surveys(ncc_location, ncc_token, campaign_name)
    if len(surveys) > 0:
        survey_theme_id = surveys[0]["surveythemeId"]
        tenant_id = surveys[0]["tenantId"]
    else:
        post_datadog_event(
            dd_api_key,
            dd_application_key,
            username,
            "warning",
            "normal",
            "Survey Creation Failed",
            f'No surveys found using "{campaign_name}" to identify survey theme.',
            ["featuresetup"],
        )
        logging.warning(
            f'No surveys found using "{campaign_name}" to identify survey theme.'
        )

    # Create CSAT survey
    csat_survey = search_surveys(
        ncc_location,
        ncc_token,
        csat_survey_name,
    )
    if csat_survey == {}:
        if survey_theme_id != "":
            csat_survey = create_csat_survey(
                ncc_location, ncc_token, csat_survey_name, survey_theme_id
            )
            if csat_survey != {}:
                post_datadog_event(
                    dd_api_key,
                    dd_application_key,
                    username,
                    "success",
                    "normal",
                    "Survey Creation Successful",
                    f'Survey "{csat_survey_name}" created.',
                    ["featuresetup"],
                )
                logging.info(f'Survey "{csat_survey_name}" created.')
            else:
                post_datadog_event(
                    dd_api_key,
                    dd_application_key,
                    username,
                    "error",
                    "normal",
                    "Survey Creation Failed",
                    f'Survey "{csat_survey_name}" not created.',
                    ["featuresetup"],
                )
                logging.error(f'Survey "{csat_survey_name}" not created.')
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
        logging.info(f'Survey "{csat_survey_name}" already exists')

    # Create CSAT workflow
    workflow = search_workflows(
        ncc_location,
        ncc_token,
        csat_survey_name,
    )
    if workflow == {}:
        if csat_survey != {}:
            workflow = create_csat_workflow(ncc_location, ncc_token, csat_survey_name)
            if workflow != {}:
                logging.info(f'Workflow "{csat_survey_name}" created.')
            else:
                post_datadog_event(
                    dd_api_key,
                    dd_application_key,
                    username,
                    "error",
                    "normal",
                    "Workflow Creation Failed",
                    f'Workflow "{csat_survey_name}" not created.',
                    ["featuresetup"],
                )
                logging.error(f'Workflow "{csat_survey_name}" not created.')
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
        logging.info(f'Workflow "{csat_survey_name}" already exists.')

    # Create CSAT campaign
    campaign = search_campaigns_by_name(
        ncc_location,
        ncc_token,
        csat_survey_name,
    )
    if campaign == {}:
        if "_id" in csat_survey and "_id" in workflow:
            campaign = create_csat_campaign(
                ncc_location, ncc_token, csat_survey_name, workflow, csat_survey
            )
            if campaign != {}:
                logging.info(f'Campaign "{csat_survey_name}" created.')
            else:
                post_datadog_event(
                    dd_api_key,
                    dd_application_key,
                    username,
                    "error",
                    "normal",
                    "Campaign Creation Failed",
                    f'Campaign "{csat_survey_name}" not created.',
                    ["featuresetup"],
                )
                logging.error(f'Campaign "{csat_survey_name}" not created.')
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
        logging.info(f'Campaign "{csat_survey_name}" already exists.')

    # Create CSAT report
    report = search_reports(
        ncc_location,
        ncc_token,
        csat_survey_name,
    )
    if report == {}:
        if csat_survey != {} and campaign != {}:
            report = create_csat_report(
                ncc_location,
                ncc_token,
                csat_survey_name,
                "today",
                csat_survey,
                campaign,
            )
            if report != {}:
                logging.info(f'Report "{csat_survey_name}" created')
            else:
                post_datadog_event(
                    dd_api_key,
                    dd_application_key,
                    username,
                    "error",
                    "normal",
                    "Report Creation Failed",
                    f'Report "{csat_survey_name}" not created.',
                    ["featuresetup"],
                )
                logging.error(f'Report "{csat_survey_name}" not created.')
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
        logging.info(f'Report "{csat_survey_name}" already exists.')

    # Update "main" workflow
    workflow = search_workflows(ncc_location, ncc_token, campaign_name)
    if workflow != {}:
        if campaign != {}:
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
                                    + campaign["_id"]
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
                                    + campaign["_id"]
                                    + "&context=%7B%22relatedWorkitemId%22%3A%22${workitem.workitemId}%22%7D. We look forward to hearing from you!",
                                    "toAddress": "workitem.data.context.consumerData.phone",
                                    "fromAddress": f"'{campaign_caller_id}'",
                                    "createNewWorkitem": False,
                                    "condition": {
                                        "conditionType": "AND",
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
                                "id": "refId1740784151528",
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

    duration = datetime.datetime.now() - start_time
    logging.info(f"Duration: {str(duration)}")
