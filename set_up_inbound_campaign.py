import datetime
import logging
from config import *
from authentication_info import *
from datadog import *
from ncc_pstn_number import *
from ncc_disposition import *
from ncc_user_profile import *
from ncc_user_profile_disposition import *
from ncc_queue import *
from ncc_user import *
from ncc_user_queue import *
from ncc_supervisor_queue import *
from ncc_survey_theme import *
from ncc_survey import *
from ncc_classification import *
from ncc_scorecard import *
from ncc_scorecard_classification import *
from ncc_campaign_scorecard import *
from ncc_template import *
from ncc_campaign_template import *
from ncc_supervisor_campaign import *
from ncc_function import *
from ncc_script import *
from ncc_prompt import *
from ncc_workflow import *
from ncc_service import *
from ncc_campaign import *
from ncc_campaign_disposition import *
from ncc_topic import *
from ncc_report import *


def set_up_inbound_campaign(ncc_location: str, ncc_token: str, username: str):
    """
    This function performs the basic setup of a new Nextiva Contact Center (NCC) campaign.
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
                "Inbound Campaign Setup Cancelled",
                f'User "{username}" cancelled inbound campaign setup.',
                ["inboundcampaignsetup"],
            )
            print()
            print("Operation cancelled.")
            cancelled = True
        elif campaign_name == "":
            print()
            print("Invalid campaign name.")

    if cancelled == False:

        # Enter business name
        business_name = ""
        while business_name == "":
            print()
            business_name = input("Business name: ")
            if business_name.lower() == "cancel":
                post_datadog_event(
                    dd_api_key,
                    dd_application_key,
                    username,
                    "warning",
                    "normal",
                    "Inbound Campaign Setup Cancelled",
                    f'User "{username}" cancelled "{campaign_name}" inbound campaign setup.',
                    ["inboundcampaignsetup"],
                )
                print()
                print("Operation cancelled.")
                cancelled = True
            elif business_name == "":
                print()
                print("Invalid business name.")

    if cancelled == False:

        # Select vertical
        print()
        choice = ""
        while choice == "":
            print("Please select a vertical.")
            print("-------------------------")
            print("1. General")
            print("2. Healthcare")
            print("3. FinServ")
            print("4. Insurance")
            print("5. Retail")
            print("6. PubSec")
            print()
            choice = input("Command: ")
            print()
            if choice.lower() == "cancel":
                post_datadog_event(
                    dd_api_key,
                    dd_application_key,
                    username,
                    "warning",
                    "normal",
                    "Inbound Campaign Setup Cancelled",
                    f'User "{username}" cancelled "{campaign_name}" inbound campaign setup.',
                    ["inboundcampaignsetup"],
                )
                print("Operation cancelled.")
                cancelled = True
            else:
                if choice == "1":
                    vertical = "general"
                    dispositions = general_dispositions
                    queues = general_queues
                    categories = general_categories
                    options = general_options
                    classifications = general_classifications.copy()
                    templates = general_templates
                    topics = general_topics
                    reports = general_reports
                elif choice == "2":
                    vertical = "hc"
                    dispositions = general_dispositions + hc_dispositions
                    queues = general_queues + hc_queues
                    categories = general_categories + hc_categories
                    options = hc_options
                    classifications = (
                        general_classifications.copy() + hc_classifications.copy()
                    )
                    templates = general_templates + hc_templates
                    topics = general_topics + hc_topics
                    reports = general_reports + hc_reports
                elif choice == "3":
                    vertical = "finserv"
                    dispositions = general_dispositions + finserv_dispositions
                    queues = general_queues + finserv_queues
                    categories = general_categories + finserv_categories
                    options = finserv_options
                    classifications = (
                        general_classifications.copy() + finserv_classifications.copy()
                    )
                    templates = general_templates + finserv_templates
                    topics = general_topics + finserv_topics
                    reports = general_reports + finserv_reports
                elif choice == "4":
                    vertical = "insurance"
                    dispositions = general_dispositions + insurance_dispositions
                    queues = general_queues + insurance_queues
                    categories = general_categories + insurance_categories
                    options = insurance_options
                    classifications = (
                        general_classifications.copy()
                        + insurance_classifications.copy()
                    )
                    templates = general_templates + insurance_templates
                    topics = general_topics + insurance_topics
                    reports = general_reports + insurance_reports
                elif choice == "5":
                    vertical = "retail"
                    dispositions = general_dispositions + retail_dispositions
                    queues = general_queues + retail_queues
                    categories = general_categories + retail_categories
                    options = retail_options
                    classifications = (
                        general_classifications.copy() + retail_classifications.copy()
                    )
                    templates = general_templates + retail_templates
                    topics = general_topics + retail_topics
                    reports = general_reports + retail_reports
                elif choice == "6":
                    vertical = "pubsec"
                    dispositions = general_dispositions + pubsec_dispositions
                    queues = general_queues + pubsec_queues
                    categories = general_categories + pubsec_categories
                    options = pubsec_options
                    classifications = (
                        general_classifications.copy() + pubsec_classifications.copy()
                    )
                    templates = general_templates + pubsec_templates
                    topics = general_topics + pubsec_topics
                    reports = general_reports + pubsec_reports
                else:
                    choice = ""
                    print("Invalid choice.")
                    print()

    if cancelled == False:

        # Select workflow_type
        workflow_type = ""
        choice = ""
        while choice == "":
            print("Please select a workflow type.")
            print("------------------------------")
            print("1. IVA")
            print("2. Non-IVA, DTMF")
            print("3. Direct Line")
            print()
            choice = input("Command: ")
            print()
            if choice.lower() == "cancel":
                post_datadog_event(
                    dd_api_key,
                    dd_application_key,
                    username,
                    "warning",
                    "normal",
                    "Inbound Campaign Setup Cancelled",
                    f'User "{username}" cancelled "{campaign_name}" inbound campaign setup.',
                    ["inboundcampaignsetup"],
                )
                print("Operation cancelled.")
                cancelled = True
            else:
                if choice == "1":
                    workflow_type = "iva"
                elif choice == "2":
                    workflow_type = "non_iva_dtmf"
                elif choice == "3":
                    workflow_type = "direct_line"
                else:
                    choice = ""
                    print("Invalid choice.")
                    print()

    if cancelled == False:

        # Select PSTN number
        campaign_address = ""
        campaign_addresses_available = []
        print("Searching for available PSTN numbers...")
        print()
        pstn_numbers = get_pstn_numbers(ncc_location, ncc_token)
        if len(pstn_numbers) > 0:
            for index, pstn_number in enumerate(pstn_numbers):
                success = search_campaigns_by_address(
                    ncc_location, ncc_token, pstn_number["name"]
                )
                if success:
                    pass
                else:
                    campaign_addresses_available.append(pstn_number)
        if len(campaign_addresses_available) > 0:
            while campaign_address == "":
                print("Please select a PSTN number:")
                print("----------------------------")
                for index, campaign_address_available in enumerate(
                    campaign_addresses_available
                ):
                    print(f"{index + 1}. {campaign_address_available["name"]}")
                print(f"{len(campaign_addresses_available) + 1}. None")
                print()
                choice = input("Command: ")
                if choice.lower() == "cancel":
                    post_datadog_event(
                        dd_api_key,
                        dd_application_key,
                        username,
                        "warning",
                        "normal",
                        "Inbound Campaign Setup Cancelled",
                        f'User "{username}" cancelled "{campaign_name}" inbound campaign setup.',
                        ["inboundcampaignsetup"],
                    )
                    print()
                    print("Operation cancelled.")
                    cancelled = True
                    campaign_address = "None"
                elif choice == str(len(campaign_addresses_available) + 1):
                    print()
                    campaign_address = "None"
                else:
                    choice = int(choice) - 1
                    try:
                        campaign_address = campaign_addresses_available[choice]["name"]
                        print()
                    except:
                        print()
                        print("Invalid choice.")
                        print()
        else:
            print("No phone numbers available.")
            print()

    if cancelled == False:

        # Select campaign caller ID
        campaign_caller_id = ""
        if len(pstn_numbers) > 0:
            while campaign_caller_id == "":
                print("Please select a caller ID number for this campaign:")
                print("---------------------------------------------------")
                for index, pstn_number in enumerate(pstn_numbers):
                    print(f"{index + 1}. {pstn_number["name"]}")
                print()
                choice = input("Command: ")
                if choice.lower() == "cancel":
                    post_datadog_event(
                        dd_api_key,
                        dd_application_key,
                        username,
                        "warning",
                        "normal",
                        "Inbound Campaign Setup Cancelled",
                        f'User "{username}" cancelled "{campaign_name}" inbound campaign setup.',
                        ["inboundcampaignsetup"],
                    )
                    print()
                    print("Operation cancelled.")
                    cancelled = True
                    campaign_caller_id = "None"
                else:
                    choice = int(choice) - 1
                    try:
                        campaign_caller_id = pstn_numbers[choice]["name"]
                        print()
                    except:
                        print()
                        print("Invalid choice.")
                        print()

    if cancelled == False:

        # Select whether to assign agents to queues
        choice = ""
        while choice == "":
            print("Assign all agents to queues?")
            print("----------------------------")
            print("1. Yes")
            print("2. No")
            print()
            choice = input("Command: ")
            print()
            if choice.lower() == "cancel":
                post_datadog_event(
                    dd_api_key,
                    dd_application_key,
                    username,
                    "warning",
                    "normal",
                    "Inbound Campaign Setup Cancelled",
                    f'User "{username}" cancelled "{campaign_name}" inbound campaign setup.',
                    ["inboundcampaignsetup"],
                )
                print("Operation cancelled.")
                cancelled = True
            else:
                if choice == "1":
                    assign_agents = True
                elif choice == "2":
                    assign_agents = False
                else:
                    choice = ""
                    print("Invalid choice.")
                    print()

    if cancelled == False:

        # Select whether to assign supervisors to queues
        choice = ""
        while choice == "":
            print("Assign all supervisors to queues?")
            print("---------------------------------")
            print("1. Yes")
            print("2. No")
            print()
            choice = input("Command: ")
            print()
            if choice.lower() == "cancel":
                post_datadog_event(
                    dd_api_key,
                    dd_application_key,
                    username,
                    "warning",
                    "normal",
                    "Inbound Campaign Setup Cancelled",
                    f'User "{username}" cancelled "{campaign_name}" inbound campaign setup.',
                    ["inboundcampaignsetup"],
                )
                print("Operation cancelled.")
                cancelled = True
            else:
                if choice == "1":
                    assign_supervisors_to_queues = True
                elif choice == "2":
                    assign_supervisors_to_queues = False
                else:
                    choice = ""
                    print("Invalid choice.")
                    print()

    if cancelled == False:

        # Select whether to assign supervisors to the campaign
        choice = ""
        while choice == "":
            print("Assign all supervisors to campaign?")
            print("-----------------------------------")
            print("1. Yes")
            print("2. No")
            print()
            choice = input("Command: ")
            print()
            if choice.lower() == "cancel":
                post_datadog_event(
                    dd_api_key,
                    dd_application_key,
                    username,
                    "warning",
                    "normal",
                    "Inbound Campaign Setup Cancelled",
                    f'User "{username}" cancelled "{campaign_name}" inbound campaign setup.',
                    ["inboundcampaignsetup"],
                )
                print("Operation cancelled.")
                cancelled = True
            else:
                if choice == "1":
                    assign_supervisors_to_campaign = True
                elif choice == "2":
                    assign_supervisors_to_campaign = False
                else:
                    choice = ""
                    print("Invalid choice.")
                    print()

    if cancelled == False:

        # Select whether to assign agent to topics
        choice = ""
        while choice == "":
            print("Assign all agents to topics?")
            print("----------------------------")
            print("1. Yes")
            print("2. No")
            print()
            choice = input("Command: ")
            print()
            if choice.lower() == "cancel":
                post_datadog_event(
                    dd_api_key,
                    dd_application_key,
                    username,
                    "warning",
                    "normal",
                    "Inbound Campaign Setup Cancelled",
                    f'User "{username}" cancelled "{campaign_name}" inbound campaign setup.',
                    ["inboundcampaignsetup"],
                )
                print("Operation cancelled.")
                cancelled = True
            else:
                if choice == "1":
                    assign_agents_to_topics = True
                elif choice == "2":
                    assign_agents_to_topics = False
                else:
                    choice = ""
                    print("Invalid choice.")
                    print()

    if cancelled == False:

        # Select whether to assign supervisor to topics
        choice = ""
        while choice == "":
            print("Assign all supervisors to topics?")
            print("---------------------------------")
            print("1. Yes")
            print("2. No")
            print()
            choice = input("Command: ")
            print()
            if choice.lower() == "cancel":
                post_datadog_event(
                    dd_api_key,
                    dd_application_key,
                    username,
                    "warning",
                    "normal",
                    "Inbound Campaign Setup Cancelled",
                    f'User "{username}" cancelled "{campaign_name}" inbound campaign setup.',
                    ["inboundcampaignsetup"],
                )
                print("Operation cancelled.")
                cancelled = True
            else:
                if choice == "1":
                    assign_supervisors_to_topics = True
                elif choice == "2":
                    assign_supervisors_to_topics = False
                else:
                    choice = ""
                    print("Invalid choice.")
                    print()

    if cancelled == False:

        start_time = datetime.datetime.now()

        logging.info("Starting...")
        # Create dispositions
        dispositions_to_assign = []
        tenant_id = ""
        for disposition in dispositions:
            result = search_dispositions(
                ncc_location,
                ncc_token,
                disposition["name"],
            )
            if result == {}:
                result = create_disposition(
                    ncc_location,
                    ncc_token,
                    disposition,
                )
                if result != {}:
                    logging.info(f'Disposition "{result["name"]}" created.')
                    dispositions_to_assign.append(result)
                    tenant_id = result["tenantId"]
                else:
                    post_datadog_event(
                        dd_api_key,
                        dd_application_key,
                        username,
                        "error",
                        "normal",
                        "Disposition Creation Failed",
                        f'Disposition "{disposition["name"]}" not created.',
                        ["inboundcampaignsetup"],
                    )
                    logging.error(f'Disposition "{disposition["name"]}" not created.')
            else:
                logging.info(f'Disposition "{result["name"]}" already exists.')
                dispositions_to_assign.append(result)
                tenant_id = result["tenantId"]

        # Assign user profiles to dispositions
        for user_profile in user_profiles:
            result = search_user_profiles(
                ncc_location,
                ncc_token,
                user_profile,
            )
            if result != {}:
                logging.info(f'User profile "{user_profile}" found.')
                for disposition in dispositions_to_assign:
                    success = search_user_profile_dispositions(
                        ncc_location,
                        ncc_token,
                        disposition["_id"],
                        result["_id"],
                    )
                    if success:
                        logging.info(
                            f'Disposition "{disposition["name"]}" already assigned.'
                        )
                    else:
                        user_profile_disposition = create_user_profile_disposition(
                            ncc_location,
                            ncc_token,
                            result["_id"],
                            disposition["_id"],
                        )
                        if user_profile_disposition != {}:
                            logging.info(
                                f'Disposition "{disposition["name"]}" assigned.'
                            )
                        else:
                            post_datadog_event(
                                dd_api_key,
                                dd_application_key,
                                username,
                                "error",
                                "normal",
                                "Disposition Assignment to User Profile Failed",
                                f'Disposition "{disposition["name"]}" not assigned.',
                                ["inboundcampaignsetup"],
                            )
                            logging.error(
                                f'Disposition "{disposition["name"]}" not assigned.'
                            )
            else:
                post_datadog_event(
                    dd_api_key,
                    dd_application_key,
                    username,
                    "warning",
                    "normal",
                    "User Profile Not Found",
                    f'User profile "{user_profile}" not found.',
                    ["inboundcampaignsetup"],
                )
                logging.warning(f'User profile "{user_profile}" not found.')

        # Create queues
        queues_to_assign = {}
        for queue in queues:
            result = search_queues(
                ncc_location,
                ncc_token,
                queue["name"],
            )
            if result == {}:
                result = create_queue(
                    ncc_location,
                    ncc_token,
                    queue,
                )
                if result != {}:
                    logging.info(f'Queue "{result["name"]}" created.')
                    queues_to_assign[result["name"]] = result["_id"]
                else:
                    post_datadog_event(
                        dd_api_key,
                        dd_application_key,
                        username,
                        "error",
                        "normal",
                        "Queue Creation Failed",
                        f'Queue "{queue["name"]}" not created.',
                        ["inboundcampaignsetup"],
                    )
                    logging.error(f'Queue "{queue["name"]}" not created.')
            else:
                logging.info(f'Queue "{queue["name"]}" already exists.')
                queues_to_assign[result["name"]] = result["_id"]

        # Assign agents to queues
        if assign_agents and (len(queues_to_assign) > 0):
            agent_user_profile = search_user_profiles(
                ncc_location,
                ncc_token,
                "Agent",
            )
            if agent_user_profile != {}:
                agents = get_users(
                    ncc_location,
                    ncc_token,
                    agent_user_profile["_id"],
                )
                if len(agents) > 0:
                    for agent in agents:
                        for (
                            key,
                            value,
                        ) in queues_to_assign.items():
                            success = search_user_queues(
                                ncc_location,
                                ncc_token,
                                agent["_id"],
                                value,
                            )
                            if success:
                                logging.info(
                                    f'Agent "{agent["firstName"]} {agent["lastName"]}" already assigned to "{key}" queue.'
                                )
                            else:
                                success = create_user_queue(
                                    ncc_location,
                                    ncc_token,
                                    agent["_id"],
                                    value,
                                )
                                if success:
                                    logging.info(
                                        f'Agent "{agent["firstName"]} {agent["lastName"]}" assigned to "{key}" queue.'
                                    )
                                else:
                                    post_datadog_event(
                                        dd_api_key,
                                        dd_application_key,
                                        username,
                                        "error",
                                        "normal",
                                        "Agent Assignment to Queue Failed",
                                        f'Agent "{agent["firstName"]} {agent["lastName"]}" not assigned to "{key}" queue.',
                                        ["inboundcampaignsetup"],
                                    )
                                    logging.error(
                                        f'Agent "{agent["firstName"]} {agent["lastName"]}" not assigned to "{key}" queue.'
                                    )
                else:
                    post_datadog_event(
                        dd_api_key,
                        dd_application_key,
                        username,
                        "warning",
                        "normal",
                        "No Agents Found",
                        "No agents found to assign to queues.",
                        ["inboundcampaignsetup"],
                    )
                    logging.warning("No agents found to assign to queues.")
            else:
                post_datadog_event(
                    dd_api_key,
                    dd_application_key,
                    username,
                    "warning",
                    "normal",
                    "User Profile Not Found",
                    'User profile "Agent" not found for queue assignment.',
                    ["inboundcampaignsetup"],
                )
                logging.warning('User profile "Agent" not found for queue assignment.')

        # Assign supervisors to queues
        if assign_supervisors_to_queues and len(queues_to_assign) > 0:
            supervisor_user_profile = search_user_profiles(
                ncc_location,
                ncc_token,
                "Supervisor",
            )
            if supervisor_user_profile != {}:
                supervisors = get_users(
                    ncc_location,
                    ncc_token,
                    supervisor_user_profile["_id"],
                )
                if len(supervisors) > 0:
                    for supervisor in supervisors:
                        for (
                            key,
                            value,
                        ) in queues_to_assign.items():
                            success = search_supervisor_queues(
                                ncc_location,
                                ncc_token,
                                supervisor["_id"],
                                value,
                            )
                            if success:
                                logging.info(
                                    f'Supervisor "{supervisor["name"]}" already assigned to "{key}" queue.'
                                )
                            else:
                                success = create_supervisor_queue(
                                    ncc_location,
                                    ncc_token,
                                    supervisor["_id"],
                                    value,
                                )
                                if success:
                                    logging.info(
                                        f'Supervisor "{supervisor["name"]}" assigned to "{key}" queue.'
                                    )
                                else:
                                    post_datadog_event(
                                        dd_api_key,
                                        dd_application_key,
                                        username,
                                        "error",
                                        "normal",
                                        "Supervisor Assignment to Queue Failed",
                                        f'Supervisor "{supervisor["name"]}" not assigned to "{key}" queue.',
                                        ["inboundcampaignsetup"],
                                    )
                                    logging.error(
                                        f'Supervisor "{supervisor["name"]}" not assigned to "{key}" queue.'
                                    )
                else:
                    post_datadog_event(
                        dd_api_key,
                        dd_application_key,
                        username,
                        "warning",
                        "normal",
                        "No Supervisors Found",
                        "No supervisors found to assign to queues.",
                        ["inboundcampaignsetup"],
                    )
                    logging.warning("No supervisors found to assign to queues.")
            else:
                post_datadog_event(
                    dd_api_key,
                    dd_application_key,
                    username,
                    "warning",
                    "normal",
                    "User Profile Not Found",
                    'User profile "Supervisor" not found for queue assignment.',
                    ["inboundcampaignsetup"],
                )
                logging.warning(
                    'User profile "Supervisor" not found for queue assignment.'
                )

        # Create survey theme
        survey_theme = search_survey_themes(
            ncc_location,
            ncc_token,
            f"{business_name}",
        )
        if survey_theme == {}:
            survey_theme = create_survey_theme(
                ncc_location,
                ncc_token,
                f"{business_name}",
            )
            if survey_theme != {}:
                logging.info(f'Survey theme "{business_name}" created.')
            else:
                post_datadog_event(
                    dd_api_key,
                    dd_application_key,
                    username,
                    "error",
                    "normal",
                    "Survey Theme Creation Failed",
                    f'Survey theme "{business_name}" not created.',
                    ["inboundcampaignsetup"],
                )
                logging.error(f'Survey theme "{business_name}" not created.')
        else:
            logging.info(f'Survey theme "{business_name}" already exists.')

        # Create user survey
        if survey_theme != {}:
            user_survey = search_surveys(
                ncc_location,
                ncc_token,
                f"{campaign_name} - User",
            )
            if user_survey == {}:
                user_survey = create_user_survey(
                    ncc_location,
                    ncc_token,
                    f"{campaign_name} - User",
                    categories,
                    survey_theme,
                )
                if user_survey != {}:
                    logging.info(f'Survey "{campaign_name} - User" created.')
                else:
                    post_datadog_event(
                        dd_api_key,
                        dd_application_key,
                        username,
                        "error",
                        "normal",
                        "Survey Creation Failed",
                        f'Survey "{campaign_name} - User" not created.',
                        ["inboundcampaignsetup"],
                    )
                    logging.error(f'Survey "{campaign_name} - User" not created.')
            else:
                logging.info(f'Survey "{campaign_name} - User" already exists.')
        else:
            post_datadog_event(
                dd_api_key,
                dd_application_key,
                username,
                "warning",
                "normal",
                "Survey Creation Failed",
                "Insufficient data to create user survey.",
                ["inboundcampaignsetup"],
            )
            logging.warning("Insufficient data to create user survey.")

        # Create chat survey
        chat_survey = search_surveys(
            ncc_location,
            ncc_token,
            f"{campaign_name} - Chat",
        )
        if chat_survey == {}:
            if survey_theme != {}:
                chat_queues = []
                for (
                    key,
                    value,
                ) in queues_to_assign.items():
                    chat_queues.append(value)
                chat_survey = create_chat_survey(
                    ncc_location,
                    ncc_token,
                    f"{campaign_name} - Chat",
                    options,
                    survey_theme,
                    chat_queues,
                )
                if chat_survey != {}:
                    logging.info(f'Survey "{campaign_name} - Chat" created.')
                else:
                    post_datadog_event(
                        dd_api_key,
                        dd_application_key,
                        username,
                        "error",
                        "normal",
                        "Survey Creation Failed",
                        f'Survey "{campaign_name} - Chat" not created.',
                        ["inboundcampaignsetup"],
                    )
                    logging.error(f'Survey "{campaign_name} - Chat" not created.')
            else:
                post_datadog_event(
                    dd_api_key,
                    dd_application_key,
                    username,
                    "warning",
                    "normal",
                    "Survey Creation Failed",
                    "Insufficient data to create chat survey.",
                    ["inboundcampaignsetup"],
                )
                logging.warning("Insufficient data to create chat survey.")
        else:
            logging.info(f'Survey "{campaign_name} - Chat" already exists.')

        # Create QM survey
        if survey_theme != {}:
            qm_survey = search_surveys(
                ncc_location,
                ncc_token,
                f"{campaign_name} - QM",
            )
            if qm_survey == {}:
                qm_survey = create_survey(
                    ncc_location,
                    ncc_token,
                    f"{campaign_name} - QM",
                    main_qm_survey_body,
                    survey_theme,
                )
                if qm_survey != {}:
                    logging.info(f'Survey "{campaign_name} - QM" created.')
                else:
                    post_datadog_event(
                        dd_api_key,
                        dd_application_key,
                        username,
                        "error",
                        "normal",
                        "Survey Creation Failed",
                        f'Survey "{campaign_name} - QM" not created.',
                        ["inboundcampaignsetup"],
                    )
                    logging.error(f'Survey "{campaign_name} - QM" not created.')
            else:
                logging.info(f'Survey "{campaign_name} - QM" already exists')
        else:
            post_datadog_event(
                dd_api_key,
                dd_application_key,
                username,
                "warning",
                "normal",
                "Survey Creation Failed",
                "Insufficient data to create QM survey.",
                ["inboundcampaignsetup"],
            )
            logging.warning("Insufficient data to create QM survey.")

        # Create topics
        topics_to_assign = []
        for topic in topics:
            result = search_topics(
                ncc_location,
                ncc_token,
                topic,
            )
            if result == {}:
                result = create_topic(
                    ncc_location,
                    ncc_token,
                    topic,
                )
                if result != {}:
                    logging.info(f'Topic "{topic}" created.')
                    topics_to_assign.append(result)
                else:
                    post_datadog_event(
                        dd_api_key,
                        dd_application_key,
                        username,
                        "error",
                        "normal",
                        "Topic Creation Failed",
                        f'Topic "{topic}" not created.',
                        ["inboundcampaignsetup"],
                    )
                    logging.error(f'Topic "{topic}" not created.')
            else:
                logging.info(f'Topic "{topic}" already exists.')
                topics_to_assign.append(result)

        # Assign agents to topics
        if assign_agents_to_topics and (len(topics_to_assign) > 0):
            agent_user_profile = search_user_profiles(
                ncc_location,
                ncc_token,
                "Agent",
            )
            if agent_user_profile != {}:
                agents = get_users(
                    ncc_location,
                    ncc_token,
                    agent_user_profile["_id"],
                )
                if len(agents) > 0:
                    for agent in agents:
                        for topic in topics_to_assign:
                            if "users" in topic:
                                users = topic["users"]
                            else:
                                users = []
                            if agent["_id"] in users:
                                logging.info(
                                    f'Agent "{agent["firstName"]} {agent["lastName"]}" already assigned to topic "{topic["name"]}".'
                                )
                            else:
                                users.append(agent["_id"])
                                success = update_topic_users(
                                    ncc_location,
                                    ncc_token,
                                    topic["_id"],
                                    users,
                                )
                                if success:
                                    logging.info(
                                        f'Agent "{agent["firstName"]} {agent["lastName"]}" assigned to topic "{topic["name"]}".'
                                    )
                                else:
                                    post_datadog_event(
                                        dd_api_key,
                                        dd_application_key,
                                        username,
                                        "error",
                                        "normal",
                                        "Agent Assignment to Topic Failed",
                                        f'Agent "{agent["firstName"]} {agent["lastName"]}" not assigned to topic "{topic["name"]}".',
                                        ["inboundcampaignsetup"],
                                    )
                                    logging.error(
                                        f'Agent "{agent["firstName"]} {agent["lastName"]}" not assigned to topic "{topic["name"]}".'
                                    )
                else:
                    post_datadog_event(
                        dd_api_key,
                        dd_application_key,
                        username,
                        "warning",
                        "normal",
                        "No Agents Found",
                        "No agents found to assign to topics.",
                        ["inboundcampaignsetup"],
                    )
                    logging.warning("No agents found to assign to topics.")
            else:
                post_datadog_event(
                    dd_api_key,
                    dd_application_key,
                    username,
                    "warning",
                    "normal",
                    "User Profile Not Found",
                    'User profile "Agent" not found for topic assignment.',
                    ["inboundcampaignsetup"],
                )
                logging.warning('User profile "Agent" not found for topic assignment.')

        # Assign supervisors to topics
        if assign_supervisors_to_topics and (len(topics_to_assign) > 0):
            supervisor_user_profile = search_user_profiles(
                ncc_location,
                ncc_token,
                "Supervisor",
            )
            if supervisor_user_profile != {}:
                supervisors = get_users(
                    ncc_location,
                    ncc_token,
                    supervisor_user_profile["_id"],
                )
                if len(supervisors) > 0:
                    for supervisor in supervisors:
                        for topic in topics_to_assign:
                            if "users" in topic:
                                users = topic["users"]
                            else:
                                users = []
                            if supervisor["_id"] in users:
                                logging.info(
                                    f'Supervisor "{supervisor["firstName"]} {supervisor["lastName"]}" already assigned to topic "{topic["name"]}".'
                                )
                            else:
                                users.append(supervisor["_id"])
                                success = update_topic_users(
                                    ncc_location,
                                    ncc_token,
                                    topic["_id"],
                                    users,
                                )
                                if success:
                                    logging.info(
                                        f'Supervisor "{supervisor["firstName"]} {supervisor["lastName"]}" assigned to topic "{topic["name"]}".'
                                    )
                                else:
                                    post_datadog_event(
                                        dd_api_key,
                                        dd_application_key,
                                        username,
                                        "error",
                                        "normal",
                                        "Supervisor Assignment to Topic Failed",
                                        f'Supervisor "{supervisor["firstName"]} {supervisor["lastName"]}" not assigned to topic "{topic["name"]}".',
                                        ["inboundcampaignsetup"],
                                    )
                                    logging.error(
                                        f'Supervisor "{supervisor["firstName"]} {supervisor["lastName"]}" not assigned to topic "{topic["name"]}".'
                                    )
                else:
                    post_datadog_event(
                        dd_api_key,
                        dd_application_key,
                        username,
                        "warning",
                        "normal",
                        "No Supervisors Found",
                        "No supervisors found to assign to topics.",
                        ["inboundcampaignsetup"],
                    )
                    logging.warning("No supervisors found to assign to topics.")
            else:
                post_datadog_event(
                    dd_api_key,
                    dd_application_key,
                    username,
                    "warning",
                    "normal",
                    "User Profile Not Found",
                    'User profile "Supervisor" not found for topic assignment.',
                    ["inboundcampaignsetup"],
                )
                logging.warning('User profile "Supervisor" not found.')

        # Create MEDIA service
        media_service = search_services(
            ncc_location,
            ncc_token,
            "MEDIA",
        )
        if media_service != {}:
            logging.info('Service type "MEDIA" already exists.')
            if media_service["enabled"] == False:
                success = update_enable_service(
                    ncc_location, ncc_token, media_service["_id"]
                )
                if success:
                    logging.info(f'Service "{media_service["name"]}" enabled.')
                else:
                    post_datadog_event(
                        dd_api_key,
                        dd_application_key,
                        username,
                        "error",
                        "normal",
                        "Service Update Failed",
                        f'Service "{media_service["name"]}" not enabled.',
                        ["inboundcampaignsetup"],
                    )
                    logging.error(f'Service "{media_service["name"]}" not enabled.')
        else:
            media_service = create_media_service(
                ncc_location,
                ncc_token,
                "Freeswitch - Media Server",
            )
            if media_service != {}:
                logging.info('Service type "MEDIA" created.')
            else:
                post_datadog_event(
                    dd_api_key,
                    dd_application_key,
                    username,
                    "error",
                    "normal",
                    "Service Creation Failed",
                    'Service type "MEDIA" not created.',
                    ["inboundcampaignsetup"],
                )
                logging.error('Service type "MEDIA" not created.')

        # Create TEXT_TO_SPEECH service
        tts_service = search_services(
            ncc_location,
            ncc_token,
            "TEXT_TO_SPEECH",
        )
        if tts_service != {}:
            logging.info('Service type "TEXT_TO_SPEECH" already exists.')
            if tts_service["enabled"] == False:
                success = update_enable_service(
                    ncc_location, ncc_token, tts_service["_id"]
                )
                if success:
                    logging.info(f'Service "{tts_service["name"]}" enabled.')
                else:
                    post_datadog_event(
                        dd_api_key,
                        dd_application_key,
                        username,
                        "error",
                        "normal",
                        "Service Update Failed",
                        f'Service "{tts_service["name"]}" not enabled.',
                        ["inboundcampaignsetup"],
                    )
                    logging.error(f'Service "{tts_service["name"]}" not enabled.')
        else:
            tts_service = create_tts_service(
                ncc_location,
                ncc_token,
                "Google - Text To Speech",
            )
            if tts_service != {}:
                logging.info('Service type "TEXT_TO_SPEECH" created.')
            else:
                post_datadog_event(
                    dd_api_key,
                    dd_application_key,
                    username,
                    "error",
                    "normal",
                    "Service Creation Failed",
                    'Service type "TEXT_TO_SPEECH" not created.',
                    ["inboundcampaignsetup"],
                )
                logging.error('Service type "TEXT_TO_SPEECH" not created.')

        # Create GENERATIVE_AI service
        gen_ai_service = search_services(
            ncc_location,
            ncc_token,
            "GENERATIVE_AI",
        )
        if gen_ai_service != {}:
            logging.info('Service type "GENERATIVE_AI" already exists.')
            if gen_ai_service["enabled"] == False:
                success = update_enable_service(
                    ncc_location, ncc_token, gen_ai_service["_id"]
                )
                if success:
                    logging.info(f'Service "{gen_ai_service["name"]}" enabled.')
                else:
                    post_datadog_event(
                        dd_api_key,
                        dd_application_key,
                        username,
                        "error",
                        "normal",
                        "Service Update Failed",
                        f'Service "{gen_ai_service["name"]}" not enabled.',
                        ["inboundcampaignsetup"],
                    )
                    logging.error(f'Service "{gen_ai_service["name"]}" not enabled.')
        else:
            if tenant_id != "":
                gen_ai_service = create_html_gen_ai_service(
                    ncc_location,
                    ncc_token,
                    "Google - Generative AI",
                    f"thrio-prod-{tenant_id}",
                )
                if gen_ai_service != {}:
                    logging.info('Service type "GENERATIVE_AI" created.')
                else:
                    post_datadog_event(
                        dd_api_key,
                        dd_application_key,
                        username,
                        "error",
                        "normal",
                        "Service Creation Failed",
                        'Service type "GENERATIVE_AI" not created.',
                        ["inboundcampaignsetup"],
                    )
                    logging.error('Service type "GENERATIVE_AI" not created.')
            else:
                post_datadog_event(
                    dd_api_key,
                    dd_application_key,
                    username,
                    "warning",
                    "normal",
                    "Service Creation Failed",
                    'Insufficient data to create service type "GENERATIVE_AI"',
                    ["inboundcampaignsetup"],
                )
                logging.warning(
                    'Insufficient data to create service type "GENERATIVE_AI"'
                )

        # Create TRANSCRIPTION service
        transcription_service = search_services(
            ncc_location,
            ncc_token,
            "TRANSCRIPTION",
        )
        if transcription_service != {}:
            logging.info('Service type "TRANSCRIPTION" already exists.')
            if transcription_service["enabled"] == False:
                success = update_enable_service(
                    ncc_location, ncc_token, transcription_service["_id"]
                )
                if success:
                    logging.info(f'Service "{transcription_service["name"]}" enabled.')
                else:
                    post_datadog_event(
                        dd_api_key,
                        dd_application_key,
                        username,
                        "error",
                        "normal",
                        "Service Update Failed",
                        f'Service "{transcription_service["name"]}" not enabled.',
                        ["inboundcampaignsetup"],
                    )
                    logging.error(
                        f'Service "{transcription_service["name"]}" not enabled.'
                    )
        else:
            if deepgram_api_key != "":
                transcription_service = create_transcription_service(
                    ncc_location,
                    ncc_token,
                    "Deepgram Transcription",
                    deepgram_api_key,
                )
                if transcription_service != {}:
                    logging.info('Service "Deepgram Transcription" created.')
                else:
                    post_datadog_event(
                        dd_api_key,
                        dd_application_key,
                        username,
                        "error",
                        "normal",
                        "Service Creation Failed",
                        'Service "Deepgram Transcription" not created.',
                        ["inboundcampaignsetup"],
                    )
                    logging.error('Service "Deepgram Transcription" not created.')
            else:
                post_datadog_event(
                    dd_api_key,
                    dd_application_key,
                    username,
                    "warning",
                    "normal",
                    "Service Creation Failed",
                    'Insufficient data to create service type "TRANSCRIPTION"',
                    ["inboundcampaignsetup"],
                )
                logging.warning(
                    'Insufficient data to create service type "TRANSCRIPTION".'
                )

        # Create REALTIME_ANALYSIS service
        real_time_transcription_service = search_services(
            ncc_location,
            ncc_token,
            "REALTIME_ANALYSIS",
        )
        if real_time_transcription_service != {}:
            logging.info('Service type "REALTIME_ANALYSIS" already exists.')
            if real_time_transcription_service["enabled"] == False:
                success = update_enable_service(
                    ncc_location, ncc_token, real_time_transcription_service["_id"]
                )
                if success:
                    logging.info(
                        f'Service "{real_time_transcription_service["name"]}" enabled.'
                    )
                else:
                    post_datadog_event(
                        dd_api_key,
                        dd_application_key,
                        username,
                        "error",
                        "normal",
                        "Service Update Failed",
                        f'Service "{real_time_transcription_service["name"]}" not enabled.',
                        ["inboundcampaignsetup"],
                    )
                    logging.error(
                        f'Service "{real_time_transcription_service["name"]}" not enabled.'
                    )
        else:
            if deepgram_api_key != "":
                real_time_transcription_service = (
                    create_real_time_transcription_service(
                        ncc_location,
                        ncc_token,
                        "Deepgram Real-Time Transcription",
                        deepgram_api_key,
                    )
                )
                if real_time_transcription_service != {}:
                    logging.info('Service "Deepgram Real-Time Transcription" created.')
                else:
                    post_datadog_event(
                        dd_api_key,
                        dd_application_key,
                        username,
                        "error",
                        "normal",
                        "Service Creation Failed",
                        'Service "Deepgram Real-Time Transcription" not created.',
                        ["inboundcampaignsetup"],
                    )
                    logging.error(
                        'Service "Deepgram Real-Time Transcription" not created.'
                    )
            else:
                post_datadog_event(
                    dd_api_key,
                    dd_application_key,
                    username,
                    "warning",
                    "normal",
                    "Service Creation Failed",
                    'Insufficient data to create service type "TRANSCRIPTION".',
                    ["inboundcampaignsetup"],
                )
                logging.warning(
                    'Insufficient data to create service type "TRANSCRIPTION".'
                )

        # Create classifications
        classifications_to_assign = []
        for classification in classifications:
            result = search_classifications(
                ncc_location,
                ncc_token,
                f"{campaign_name} - {classification["name"]}",
            )
            if result == {}:
                result = create_classification(
                    ncc_location,
                    ncc_token,
                    f"{campaign_name} - {classification["name"]}",
                    classification["data"],
                )
                if result != {}:
                    logging.info(
                        f'Classification "{campaign_name} - {classification["name"]}" created.'
                    )
                    classifications_to_assign.append(result)
                else:
                    post_datadog_event(
                        dd_api_key,
                        dd_application_key,
                        username,
                        "error",
                        "normal",
                        "Classification Creation Failed",
                        f'Classification "{campaign_name} - {classification["name"]}" not created.',
                        ["inboundcampaignsetup"],
                    )
                    logging.error(
                        f'Classification "{campaign_name} - {classification["name"]}" not created.'
                    )
            else:
                logging.info(
                    f'Classification "{campaign_name} - {classification["name"]}" already exists.'
                )
                classifications_to_assign.append(result)

        # Create scorecard
        scorecard = search_scorecards(
            ncc_location,
            ncc_token,
            campaign_name,
        )
        if scorecard == {}:
            scorecard = create_scorecard(
                ncc_location,
                ncc_token,
                campaign_name,
            )
            if scorecard != {}:
                logging.info(f'Scorecard "{campaign_name}" created.')
            else:
                post_datadog_event(
                    dd_api_key,
                    dd_application_key,
                    username,
                    "error",
                    "normal",
                    "Scorecard Creation Failed",
                    f'Scorecard "{campaign_name}" not created.',
                    ["inboundcampaignsetup"],
                )
                logging.error(f'Scorecard "{campaign_name}" not created.')
        else:
            logging.info(f'Scorecard "{campaign_name}" already exists.')

        # Assign classifications to scorecard
        if scorecard != {}:
            for classification in classifications_to_assign:
                success = search_scorecard_classifications(
                    ncc_location,
                    ncc_token,
                    scorecard["_id"],
                    classification["_id"],
                )
                if success:
                    logging.info(
                        f'Classification "{classification["name"]}" already assigned to scorecard.'
                    )
                else:
                    scorecard_classification = create_scorecard_classification(
                        ncc_location,
                        ncc_token,
                        scorecard["_id"],
                        classification["_id"],
                    )
                    if scorecard_classification != {}:
                        logging.info(
                            f'Classification "{classification["name"]}" assigned to scorecard.'
                        )
                    else:
                        post_datadog_event(
                            dd_api_key,
                            dd_application_key,
                            username,
                            "error",
                            "normal",
                            "Classification Assignment to Scorecard Failed",
                            f'Classification "{classification["name"]}" not assigned to scorecard.',
                            ["inboundcampaignsetup"],
                        )
                        logging.error(
                            f'Classification "{classification["name"]}" not assigned to scorecard.'
                        )

        # Create templates
        templates_to_assign = []
        for template in templates:
            result = search_templates(
                ncc_location,
                ncc_token,
                template["name"],
            )
            if result == {}:
                result = create_template(
                    ncc_location,
                    ncc_token,
                    template,
                )
                if result != {}:
                    logging.info(f'Template "{template["name"]}" created.')
                    templates_to_assign.append(result)
                else:
                    post_datadog_event(
                        dd_api_key,
                        dd_application_key,
                        username,
                        "error",
                        "normal",
                        "Template Creation Failed",
                        f'Template "{template["name"]}" not created.',
                        ["inboundcampaignsetup"],
                    )
                    logging.error(f'Template "{template["name"]}" not created.')
            else:
                logging.info(f'Template "{template["name"]}" already exists.')
                templates_to_assign.append(result)

        # Create Search Contacts function
        search_contacts_function = search_functions(
            ncc_location,
            ncc_token,
            f"{campaign_name} - Search Contacts",
        )
        if search_contacts_function == {}:
            search_contacts_function = create_search_contacts_function(
                ncc_location,
                ncc_token,
                f"{campaign_name} - Search Contacts",
            )
            if search_contacts_function != {}:
                logging.info(f'Function "{campaign_name} - Search Contacts" created.')
            else:
                post_datadog_event(
                    dd_api_key,
                    dd_application_key,
                    username,
                    "error",
                    "normal",
                    "Function Creation Failed",
                    f'Function "{campaign_name} - Search Contacts" not created.',
                    ["inboundcampaignsetup"],
                )
                logging.error(
                    f'Function "{campaign_name} - Search Contacts" not created.'
                )
        else:
            logging.info(
                f'Function "{campaign_name} - Search Contacts" already exists.'
            )

        # Create Two Way Chat function
        two_way_chat_function = search_functions(
            ncc_location,
            ncc_token,
            f"{campaign_name} - Two Way Chat",
        )
        if two_way_chat_function == {}:
            two_way_chat_function = create_two_way_chat_function(
                ncc_location,
                ncc_token,
                f"{campaign_name} - Two Way Chat",
            )
            if two_way_chat_function != {}:
                logging.info(f'Function "{campaign_name} - Two Way Chat" created.')
            else:
                post_datadog_event(
                    dd_api_key,
                    dd_application_key,
                    username,
                    "error",
                    "normal",
                    "Function Creation Failed",
                    f'Function "{campaign_name} - Two Way Chat" not created.',
                    ["inboundcampaignsetup"],
                )
                logging.error(f'Function "{campaign_name} - Two Way Chat" not created.')
        else:
            logging.info(f'Function "{campaign_name} - Two Way Chat" already exists.')

        # Create Two Way SMS function
        two_way_sms_function = search_functions(
            ncc_location,
            ncc_token,
            f"{campaign_name} - Two Way SMS",
        )
        if two_way_sms_function == {}:
            two_way_sms_function = create_two_way_sms_function(
                ncc_location,
                ncc_token,
                f"{campaign_name} - Two Way SMS",
            )
            if two_way_sms_function != {}:
                logging.info(f'Function "{campaign_name} - Two Way SMS" created.')
            else:
                post_datadog_event(
                    dd_api_key,
                    dd_application_key,
                    username,
                    "error",
                    "normal",
                    "Function Creation Failed",
                    f'Function "{campaign_name} - Two Way SMS" not created.',
                    ["inboundcampaignsetup"],
                )
                logging.error(f'Function "{campaign_name} - Two Way SMS" not created.')
        else:
            logging.info(f'Function "{campaign_name} - Two Way SMS" already exists.')

        # Search for "music accoustic1" prompt
        prompt = search_prompts(ncc_location, ncc_token, "music accoustic1")
        if prompt != {}:
            logging.info(f'Prompt "music accoustic1" found.')
        else:
            post_datadog_event(
                dd_api_key,
                dd_application_key,
                username,
                "warning",
                "normal",
                "Prompt Not Found",
                'Prompt "music accoustic1" not found.',
                ["inboundcampaignsetup"],
            )
            logging.warning(f'Prompt "music accoustic1" not found.')

        # Create ACD Voicemail function
        acd_voicemail_function = search_functions(
            ncc_location,
            ncc_token,
            f"{campaign_name} - ACD Voicemail",
        )
        if acd_voicemail_function == {}:
            acd_voicemail_function = search_functions(
                ncc_location,
                ncc_token,
                "ACD Voicemail",
            )
            if acd_voicemail_function == {}:
                acd_voicemail_function = create_acd_voicemail_function(
                    ncc_location,
                    ncc_token,
                    "ACD Voicemail",
                )
                if acd_voicemail_function != {}:
                    logging.info('Function "ACD Voicemail" created.')
                else:
                    post_datadog_event(
                        dd_api_key,
                        dd_application_key,
                        username,
                        "error",
                        "normal",
                        "Function Creation Failed",
                        'Function "ACD Voicemail" not created.',
                        ["inboundcampaignsetup"],
                    )
                    logging.error('Function "ACD Voicemail" not created.')
            else:
                logging.info('Function "ACD Voicemail" already exists.')
        else:
            logging.info(f'Function "{campaign_name} - ACD Voicemail" already exists.')

        # Create ACD Callback function
        acd_callback_function = search_functions(
            ncc_location,
            ncc_token,
            f"{campaign_name} - ACD Callback",
        )
        if acd_callback_function == {}:
            acd_callback_function = create_acd_callback_function(
                ncc_location,
                ncc_token,
                f"{campaign_name} - ACD Callback",
            )
            if acd_callback_function != {}:
                logging.info(f'Function "{campaign_name} - ACD Callback" created.')
            else:
                post_datadog_event(
                    dd_api_key,
                    dd_application_key,
                    username,
                    "error",
                    "normal",
                    "Function Creation Failed",
                    f'Function "{campaign_name} - ACD Callback" not created.',
                    ["inboundcampaignsetup"],
                )
                logging.error(f'Function "{campaign_name} - ACD Callback" not created.')
        else:
            logging.info(f'Function "{campaign_name} - ACD Callback" already exists.')

        # Create Check hasAllParameters script
        check_has_all_parameters_script = search_scripts(
            ncc_location, ncc_token, "Check hasAllParameters"
        )
        if check_has_all_parameters_script == {}:
            check_has_all_parameters_script = create_check_has_all_parameters_script(
                ncc_location, ncc_token, "Check hasAllParameters"
            )
            if check_has_all_parameters_script != {}:
                logging.info('Script "Check hasAllParameters" created.')
            else:
                post_datadog_event(
                    dd_api_key,
                    dd_application_key,
                    username,
                    "error",
                    "normal",
                    "Script Creation Failed",
                    'Script "Check hasAllParameters" not created.',
                    ["inboundcampaignsetup"],
                )
                logging.error('Script "Check hasAllParameters" not created.')
        else:
            logging.info('Script "Check hasAllParameters" already exists.')

        # Create Get functionId script
        get_function_id_script = search_scripts(
            ncc_location, ncc_token, "Get functionId"
        )
        if get_function_id_script == {}:
            get_function_id_script = create_get_function_id_script(
                ncc_location, ncc_token, "Get functionId"
            )
            if get_function_id_script != {}:
                logging.info('Script "Get functionId" created.')
            else:
                post_datadog_event(
                    dd_api_key,
                    dd_application_key,
                    username,
                    "error",
                    "normal",
                    "Script Creation Failed",
                    'Script "Get functionId" not created.',
                    ["inboundcampaignsetup"],
                )
                logging.error('Script "Get functionId" not created.')
        else:
            logging.info('Script "Get functionId" already exists.')

        # Create Get queueId script
        get_queue_id_script = search_scripts(ncc_location, ncc_token, "Get queueId")
        if get_queue_id_script == {}:
            get_queue_id_script = create_get_queue_id_script(
                ncc_location,
                ncc_token,
                "Get queueId",
                queues_to_assign["Customer Service"],
            )
            if get_queue_id_script != {}:
                logging.info('Script "Get queueId" created.')
            else:
                post_datadog_event(
                    dd_api_key,
                    dd_application_key,
                    username,
                    "error",
                    "normal",
                    "Script Creation Failed",
                    'Script "Get queueId" not created.',
                    ["inboundcampaignsetup"],
                )
                logging.error('Script "Get queueId" not created.')
        else:
            logging.info('Script "Get queueId" already exists.')

        # Create "main" workflow
        workflow = search_workflows(
            ncc_location,
            ncc_token,
            campaign_name,
        )
        if workflow == {}:
            if (
                acd_voicemail_function != {}
                and acd_callback_function != {}
                and search_contacts_function != {}
                and two_way_chat_function != {}
                and two_way_sms_function != {}
                and prompt != {}
                and chat_survey != {}
                and user_survey != {}
                and get_function_id_script != {}
                and get_queue_id_script != {}
                and check_has_all_parameters_script != {}
            ):
                if workflow_type == "iva":
                    workflow = create_iva_workflow(
                        ncc_location,
                        ncc_token,
                        campaign_name,
                        business_name,
                        queues_to_assign,
                        search_contacts_function,
                        two_way_chat_function,
                        two_way_sms_function,
                        prompt,
                        acd_voicemail_function,
                        acd_callback_function,
                        get_function_id_script,
                        get_queue_id_script,
                        check_has_all_parameters_script,
                    )
                elif workflow_type == "non_iva_dtmf":
                    workflow = create_non_iva_dtmf_workflow(
                        ncc_location,
                        ncc_token,
                        campaign_name,
                        business_name,
                        queues_to_assign,
                        search_contacts_function,
                        two_way_chat_function,
                        two_way_sms_function,
                        prompt,
                        acd_voicemail_function,
                        acd_callback_function,
                        chat_survey,
                        user_survey,
                        vertical,
                    )
                else:
                    workflow = create_direct_line_workflow(
                        ncc_location,
                        ncc_token,
                        campaign_name,
                        business_name,
                        queues_to_assign,
                        search_contacts_function,
                        two_way_chat_function,
                        two_way_sms_function,
                        prompt,
                        acd_voicemail_function,
                        acd_callback_function,
                        user_survey,
                    )
                if workflow != {}:
                    logging.info(f'Workflow "{campaign_name}" created.')
                else:
                    post_datadog_event(
                        dd_api_key,
                        dd_application_key,
                        username,
                        "error",
                        "normal",
                        "Workflow Creation Failed",
                        f'Workflow "{campaign_name}" not created.',
                        ["inboundcampaignsetup"],
                    )
                    logging.error(f'Workflow "{campaign_name}" not created.')
            else:
                post_datadog_event(
                    dd_api_key,
                    dd_application_key,
                    username,
                    "warning",
                    "normal",
                    "Workflow Creation Failed",
                    "Insufficient data to create workflow.",
                    ["inboundcampaignsetup"],
                )
                logging.warning("Insufficient data to create workflow.")
        else:
            logging.info(f'Workflow "{campaign_name}" already exists.')

        # Create campaign
        campaign = search_campaigns_by_name(
            ncc_location,
            ncc_token,
            campaign_name,
        )
        if campaign == {}:
            if (
                "_id" in user_survey
                and "_id" in chat_survey
                and "_id" in qm_survey
                and "_id" in workflow
                and "_id" in real_time_transcription_service
                and "_id" in gen_ai_service
            ):
                campaign = create_campaign(
                    ncc_location,
                    ncc_token,
                    campaign_name,
                    user_survey["_id"],
                    chat_survey["_id"],
                    qm_survey["_id"],
                    campaign_caller_id,
                    workflow["_id"],
                    real_time_transcription_service["_id"],
                    gen_ai_service["_id"],
                )
                if campaign != {}:
                    post_datadog_event(
                        dd_api_key,
                        dd_application_key,
                        username,
                        "success",
                        "normal",
                        "Campaign Creation Successful",
                        f'Campaign "{campaign_name}" created.',
                        ["inboundcampaignsetup"],
                    )
                    logging.info(f'Campaign "{campaign_name}" created.')
                else:
                    post_datadog_event(
                        dd_api_key,
                        dd_application_key,
                        username,
                        "error",
                        "normal",
                        "Campaign Creation Failed",
                        f'Campaign "{campaign_name}" not created.',
                        ["inboundcampaignsetup"],
                    )
                    logging.error(f'Campaign "{campaign_name}" not created.')
            else:
                post_datadog_event(
                    dd_api_key,
                    dd_application_key,
                    username,
                    "warning",
                    "normal",
                    "Campaign Creation Failed",
                    "Insufficient data to create campaign.",
                    ["inboundcampaignsetup"],
                )
                logging.warning("Insufficient data to create campaign.")
        else:
            logging.info(f'Campaign "{campaign_name}" already exists.')

        # Assign campaign address to campaign
        if campaign != {} and campaign_address != "" and campaign_address != "None":
            success = assign_address_to_campaign(
                ncc_location,
                ncc_token,
                campaign_address,
                campaign["_id"],
            )
            if success:
                logging.info(
                    f'PSTN number "{campaign_address}" assigned to campaign "{campaign_name}".'
                )
            else:
                post_datadog_event(
                    dd_api_key,
                    dd_application_key,
                    username,
                    "error",
                    "normal",
                    "Campaign Address Assignment Failed",
                    f'PSTN number "{campaign_address}" not assigned to campaign "{campaign_name}".',
                    ["inboundcampaignsetup"],
                )
                logging.error(
                    f'PSTN number "{campaign_address}" not assigned to campaign "{campaign_name}".'
                )

        # Update chat survey campaign ID
        if campaign != {} and chat_survey != {}:
            success = update_chat_survey_campaign_id(
                ncc_location,
                ncc_token,
                chat_survey["_id"],
                campaign["_id"],
            )
            if success:
                logging.info(
                    f'Survey "{chat_survey["name"]}" updated with new campaign.'
                )
            else:
                post_datadog_event(
                    dd_api_key,
                    dd_application_key,
                    username,
                    "error",
                    "normal",
                    "Survey Update Failed",
                    f'Survey "{chat_survey["name"]}" not updated with new campaign.',
                    ["inboundcampaignsetup"],
                )
                logging.error(
                    f'Survey "{chat_survey["name"]}" not updated with new campaign.'
                )

        # Assign dispositions to campaign
        if campaign != {}:
            for disposition in dispositions_to_assign:
                success = search_campaign_dispositions(
                    ncc_location,
                    ncc_token,
                    campaign["_id"],
                    disposition["_id"],
                )
                if not success:
                    success = create_campaign_disposition(
                        ncc_location,
                        ncc_token,
                        campaign["_id"],
                        disposition["_id"],
                    )
                    if success:
                        logging.info(
                            f'Disposition "{disposition["name"]}" assigned to campaign.'
                        )
                    else:
                        post_datadog_event(
                            dd_api_key,
                            dd_application_key,
                            username,
                            "error",
                            "normal",
                            "Disposition Assignment to Campaign Failed",
                            f'Disposition "{disposition["name"]}" not assigned to campaign.',
                            ["inboundcampaignsetup"],
                        )
                        logging.error(
                            f'Disposition "{disposition["name"]}" not assigned to campaign.'
                        )
                else:
                    logging.info(
                        f'Disposition "{disposition["name"]}" already assigned to campaign.'
                    )

        # Assign scorecard to campaign
        if campaign != {} and scorecard != {}:
            success = search_campaign_scorecards(
                ncc_location,
                ncc_token,
                campaign["_id"],
                scorecard["_id"],
            )
            if not success:
                success = create_campaign_scorecard(
                    ncc_location,
                    ncc_token,
                    campaign["_id"],
                    scorecard["_id"],
                )
                if success:
                    logging.info(
                        f'Scorecard "{scorecard["name"]}" assigned to campaign.'
                    )
                else:
                    post_datadog_event(
                        dd_api_key,
                        dd_application_key,
                        username,
                        "error",
                        "normal",
                        "Scorecard Assignment to Campaign Failed",
                        f'Scorecard "{scorecard["name"]}" not assigned to campaign.',
                        ["inboundcampaignsetup"],
                    )
                    logging.error(
                        f'Scorecard "{scorecard["name"]}" not assigned to campaign.'
                    )
            else:
                logging.info(
                    f'Scorecard "{scorecard["name"]}" already assigned to campaign.'
                )

        # Assign templates to campaign
        if campaign != {}:
            for template in templates_to_assign:
                success = search_campaign_templates(
                    ncc_location,
                    ncc_token,
                    campaign["_id"],
                    template["_id"],
                )
                if not success:
                    success = create_campaign_template(
                        ncc_location,
                        ncc_token,
                        campaign["_id"],
                        template["_id"],
                    )
                    if success:
                        logging.info(
                            f'Template "{template["name"]}" assigned to campaign.'
                        )
                    else:
                        post_datadog_event(
                            dd_api_key,
                            dd_application_key,
                            username,
                            "error",
                            "normal",
                            "Template Assignment to Campaign Failed",
                            f'Template "{template["name"]}" not assigned to campaign.',
                            ["inboundcampaignsetup"],
                        )
                        logging.error(
                            f'Template "{template["name"]}" not assigned to campaign.'
                        )
                else:
                    logging.info(
                        f'Template "{template["name"]}" already assigned to campaign.'
                    )

        # Assign supervisors to campaign
        if campaign != {} and assign_supervisors_to_campaign:
            supervisor_user_profile = search_user_profiles(
                ncc_location,
                ncc_token,
                "Supervisor",
            )
            if supervisor_user_profile != {}:
                supervisors = get_users(
                    ncc_location,
                    ncc_token,
                    supervisor_user_profile["_id"],
                )
                if len(supervisors) > 0:
                    for supervisor in supervisors:
                        success = search_supervisor_campaigns(
                            ncc_location,
                            ncc_token,
                            supervisor["_id"],
                            campaign["_id"],
                        )
                        if success:
                            logging.info(
                                f'Supervisor "{supervisor["firstName"]} {supervisor["lastName"]}" already assigned to "{campaign["name"]}" campaign.'
                            )
                        else:
                            success = create_supervisor_campaign(
                                ncc_location,
                                ncc_token,
                                supervisor["_id"],
                                campaign["_id"],
                            )
                            if success:
                                logging.info(
                                    f'Supervisor "{supervisor["firstName"]} {supervisor["lastName"]}" assigned to "{campaign["name"]}" campaign.'
                                )
                            else:
                                post_datadog_event(
                                    dd_api_key,
                                    dd_application_key,
                                    username,
                                    "error",
                                    "normal",
                                    "Supervisor Assignment to Campaign Failed",
                                    f'Supervisor "{supervisor["firstName"]} {supervisor["lastName"]}" not assigned to "{campaign["name"]}" campaign.',
                                    ["inboundcampaignsetup"],
                                )
                                logging.error(
                                    f'Supervisor "{supervisor["firstName"]} {supervisor["lastName"]}" not assigned to "{campaign["name"]}" campaign.'
                                )
                else:
                    post_datadog_event(
                        dd_api_key,
                        dd_application_key,
                        username,
                        "warning",
                        "normal",
                        "No Supervisors Found",
                        "No supervisors found to assign to campaign",
                        ["inboundcampaignsetup"],
                    )
                    logging.warning("No supervisors found to assign to campaign.")
            else:
                post_datadog_event(
                    dd_api_key,
                    dd_application_key,
                    username,
                    "warning",
                    "normal",
                    "User Profile Not Found",
                    'User profile "Supervisor" not found.',
                    ["inboundcampaignsetup"],
                )
                logging.warning('User profile "Supervisor" not found.')

        # Create reports
        for report in reports:
            result = search_reports(
                ncc_location,
                ncc_token,
                report["name"],
            )
            if result == {}:
                result = create_report(
                    ncc_location,
                    ncc_token,
                    report,
                )
                if result != {}:
                    logging.info(f'Report "{report["name"]}" created')
                else:
                    post_datadog_event(
                        dd_api_key,
                        dd_application_key,
                        username,
                        "error",
                        "normal",
                        "Report Creation Failed",
                        f'Report "{report["name"]}" not created.',
                        ["inboundcampaignsetup"],
                    )
                    logging.error(f'Report "{report["name"]}" not created.')
            else:
                logging.info(f'Report "{report["name"]}" already exists.')

        duration = datetime.datetime.now() - start_time
        logging.info(f"Duration: {str(duration)}")
