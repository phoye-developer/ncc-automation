import logging
import datetime
from authentication_info import *
from datadog import *
from ncc_workflow import *
from ncc_campaign import *


def set_up_csat_survey(
    ncc_location: str,
    ncc_token: str,
    username: str,
    campaign_name: str,
):
    """
    This function re-configures a workflow in Nextiva Contact Center (NCC) to send an SMS text with a link to a CSAT survey.
    """

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    start_time = datetime.datetime.now()

    logging.info("Starting...")
    # Find "CSAT" campaign
    csat_campaign = search_campaigns_by_name(
        ncc_location,
        ncc_token,
        f"{campaign_name} - CSAT",
    )
    if csat_campaign == {}:
        post_datadog_event(
            dd_api_key,
            dd_application_key,
            username,
            "warning",
            "normal",
            "CSAT Survey Setup Failed",
            f'Campaign "{campaign_name} - CSAT" not found.',
            ["featuresetup"],
        )
        logging.warning(f'Campaign "{campaign_name} - CSAT" not found.')
    else:
        tenant_id = csat_campaign["tenantId"]
        logging.info(f'Campaign "{campaign_name} - CSAT" found.')

    # Find "Main" campaign
    campaign = search_campaigns_by_name(
        ncc_location,
        ncc_token,
        campaign_name,
    )
    if campaign == {}:
        post_datadog_event(
            dd_api_key,
            dd_application_key,
            username,
            "warning",
            "normal",
            "CSAT Survey Setup Failed",
            f'Campaign "{campaign_name}" not found.',
            ["featuresetup"],
        )
        logging.warning(f'Campaign "{campaign_name}" not found.')
    else:
        logging.info(f'Campaign "{campaign_name}" found.')

    # Update "main" workflow
    workflow = search_workflows(ncc_location, ncc_token, campaign_name)
    if workflow != {}:
        if csat_campaign != {} and campaign != {}:
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

    duration = datetime.datetime.now() - start_time
    logging.info(f"Duration: {str(duration)}")
