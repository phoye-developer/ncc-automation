import datetime
import logging
from config import *
from authentication_info import *
from deepgram import *
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
from ncc_workflow import *
from ncc_service import *
from ncc_campaign import *
from ncc_campaign_disposition import *
from ncc_topic import *
from ncc_report import *


def set_up_inbound_campaign(ncc_location: str, ncc_token: str):
    """
    This function performs the basic setup of a new Nextiva Contact Center (NCC) campaign.
    """

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

    # Enter business name
    business_name = ""
    while business_name == "":
        print()
        business_name = input("Business name: ")
        if business_name == "":
            print()
            print("Invalid business name.")

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
        print()
        choice = input("Command: ")
        print()
        if choice == "1":
            vertical = "general"
            dispositions = general_dispositions
            queues = general_queues
            categories = general_categories
            classifications = general_classifications.copy()
            templates = general_templates
            topics = general_topics
            reports = general_reports
        elif choice == "2":
            vertical = "hc"
            dispositions = general_dispositions + hc_dispositions
            queues = general_queues + hc_queues
            categories = general_categories + hc_categories
            classifications = general_classifications.copy() + hc_classifications.copy()
            templates = general_templates + hc_templates
            topics = general_topics + hc_topics
            reports = general_reports + hc_reports
        elif choice == "3":
            vertical = "finserv"
            dispositions = general_dispositions + finserv_dispositions
            queues = general_queues + finserv_queues
            categories = general_categories + finserv_categories
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
            classifications = (
                general_classifications.copy() + insurance_classifications.copy()
            )
            templates = general_templates + insurance_templates
            topics = general_topics + insurance_topics
            reports = general_reports + insurance_reports
        else:
            choice = ""
            print("Invalid choice.")
            print()

    # Select workflow_type
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

    # Select PSTN number
    campaign_address = ""
    print("Searching for available PSTN numbers...")
    print()
    pstn_numbers = get_pstn_numbers(ncc_location, ncc_token)
    if len(pstn_numbers) > 0:
        campaign_addresses_available = []
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
            print()
            choice = input("Command: ")
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
            choice = int(choice) - 1
            try:
                campaign_caller_id = pstn_numbers[choice]["name"]
                print()
            except:
                print()
                print("Invalid choice.")
                print()

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
        if choice == "1":
            assign_agents = True
        elif choice == "2":
            assign_agents = False
        else:
            choice = ""
            print("Invalid choice.")
            print()

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
        if choice == "1":
            assign_supervisors_to_queues = True
        elif choice == "2":
            assign_supervisors_to_queues = False
        else:
            choice = ""
            print("Invalid choice.")
            print()

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
        if choice == "1":
            assign_supervisors_to_campaign = True
        elif choice == "2":
            assign_supervisors_to_campaign = False
        else:
            choice = ""
            print("Invalid choice.")
            print()

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
        if choice == "1":
            assign_agents_to_topics = True
        elif choice == "2":
            assign_agents_to_topics = False
        else:
            choice = ""
            print("Invalid choice.")
            print()

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
        if choice == "1":
            assign_supervisors_to_topics = True
        elif choice == "2":
            assign_supervisors_to_topics = False
        else:
            choice = ""
            print("Invalid choice.")
            print()

    start_time = datetime.datetime.now()

    logging.info("Starting...")
    # Create dispositions
    dispositions_to_assign = []
    for disposition in dispositions:
        result = search_dispositions(ncc_location, ncc_token, disposition["name"])
        if result == {}:
            result = create_disposition(ncc_location, ncc_token, disposition)
            if result != {}:
                logging.info(f'Disposition "{result["name"]}" created.')
                dispositions_to_assign.append(result)
                tenant_id = result["tenantId"]
            else:
                logging.warning(f'Disposition "{disposition["name"]}" not created.')
        else:
            logging.info(f'Disposition "{result["name"]}" already exists.')
            dispositions_to_assign.append(result)
            tenant_id = result["tenantId"]

    # Assign user profiles to dispositions
    for user_profile in user_profiles:
        result = search_user_profiles(ncc_location, ncc_token, user_profile)
        if result != {}:
            logging.info(f'User profile "{user_profile}" found.')
            for disposition in dispositions_to_assign:
                success = search_user_profile_dispositions(
                    ncc_location, ncc_token, disposition["_id"], result["_id"]
                )
                if success:
                    logging.info(
                        f'Disposition "{disposition["name"]}" already assigned.'
                    )
                else:
                    user_profile_disposition = create_user_profile_disposition(
                        ncc_location, ncc_token, result["_id"], disposition["_id"]
                    )
                    if user_profile_disposition != {}:
                        logging.info(f'Disposition "{disposition["name"]}" assigned.')
                    else:
                        logging.warning(
                            f'Disposition "{disposition["name"]}" not assigned.'
                        )
        else:
            logging.warning(f'User profile "{user_profile}" not found.')

    # Create queues
    queues_to_assign = {}
    for queue in queues:
        result = search_queues(ncc_location, ncc_token, queue["name"])
        if result == {}:
            result = create_queue(ncc_location, ncc_token, queue)
            if result != {}:
                logging.info(f'Queue "{result["name"]}" created.')
                queues_to_assign[result["name"]] = result["_id"]
            else:
                logging.warning(f'Queue "{queue["name"]}" not created.')
        else:
            logging.info(f'Queue "{queue["name"]}" already exists.')
            queues_to_assign[result["name"]] = result["_id"]

    # Assign agents to queues
    if assign_agents and (len(queues_to_assign) > 0):
        agent_user_profile = search_user_profiles(ncc_location, ncc_token, "Agent")
        if agent_user_profile != {}:
            agents = get_users(ncc_location, ncc_token, agent_user_profile["_id"])
            if len(agents) > 0:
                for agent in agents:
                    for key, value in queues_to_assign.items():
                        success = search_user_queues(
                            ncc_location, ncc_token, agent["_id"], value
                        )
                        if success:
                            logging.info(
                                f'Agent "{agent["name"]}" already assigned to "{key}" queue.'
                            )
                        else:
                            success = create_user_queue(
                                ncc_location, ncc_token, agent["_id"], value
                            )
                            if success:
                                logging.info(
                                    f'Agent "{agent["name"]}" assigned to "{key}" queue.'
                                )
                            else:
                                logging.warning(
                                    f'Agent "{agent["name"]}" not assigned to "{key}" queue.'
                                )
            else:
                logging.warning("No agents found to assign to queues.")
        else:
            logging.warning('User profile "Agent" not found.')

    # Assign supervisors to queues
    if assign_supervisors_to_queues and len(queues_to_assign) > 0:
        supervisor_user_profile = search_user_profiles(
            ncc_location, ncc_token, "Supervisor"
        )
        if supervisor_user_profile != {}:
            supervisors = get_users(
                ncc_location, ncc_token, supervisor_user_profile["_id"]
            )
            if len(supervisors) > 0:
                for supervisor in supervisors:
                    for key, value in queues_to_assign.items():
                        success = search_supervisor_queues(
                            ncc_location, ncc_token, supervisor["_id"], value
                        )
                        if success:
                            logging.info(
                                f'Supervisor "{supervisor["name"]}" already assigned to "{key}" queue.'
                            )
                        else:
                            success = create_supervisor_queue(
                                ncc_location, ncc_token, supervisor["_id"], value
                            )
                            if success:
                                logging.info(
                                    f'Supervisor "{supervisor["name"]}" assigned to "{key}" queue.'
                                )
                            else:
                                logging.warning(
                                    f'Supervisor "{supervisor["name"]}" not assigned to "{key}" queue.'
                                )
            else:
                logging.warning("No supervisors found to assign to queues.")
        else:
            logging.warning('User profile "Supervisor" not found.')

    # Create survey theme
    survey_theme = search_survey_themes(
        ncc_location, ncc_token, f"Test {business_name}"
    )
    if survey_theme == {}:
        survey_theme = create_survey_theme(
            ncc_location, ncc_token, f"Test {business_name}"
        )
        if survey_theme != {}:
            logging.info(f'Survey theme "Test {business_name}" created.')
        else:
            logging.warning(f'Survey theme "Test {business_name}" not created.')
    else:
        logging.info(f'Survey theme "Test {business_name}" already exists.')

    # Create user survey
    if survey_theme != {}:
        user_survey = search_surveys(ncc_location, ncc_token, f"{campaign_name} - User")
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
                logging.warning(f'Survey "{campaign_name} - User" not created.')
        else:
            logging.info(f'Survey "{campaign_name} - User" already exists.')
    else:
        logging.warning("Insufficient data to create user survey.")

    # Create chat survey
    if survey_theme != {}:
        chat_survey = search_surveys(ncc_location, ncc_token, f"{campaign_name} - Chat")
        if chat_survey == {}:
            chat_survey = create_survey(
                ncc_location,
                ncc_token,
                f"{campaign_name} - Chat",
                main_chat_survey_body,
                survey_theme,
            )
            if chat_survey != {}:
                logging.info(f'Survey "{campaign_name} - Chat" created.')
            else:
                logging.warning(f'Survey "{campaign_name} - Chat" not created.')
        else:
            logging.info(f'Survey "{campaign_name} - Chat" already exists.')
    else:
        logging.warning("Insufficient data to create chat survey.")

    # Create QM survey
    if survey_theme != {}:
        qm_survey = search_surveys(ncc_location, ncc_token, f"{campaign_name} - QM")
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
                logging.warning(f'Survey "{campaign_name} - QM" not created.')
        else:
            logging.info(f'Survey "{campaign_name} - QM" already exists')
    else:
        logging.warning("Insufficient data to create QM survey.")

    # Create topics
    topics_to_assign = []
    for topic in topics:
        result = search_topics(ncc_location, ncc_token, topic)
        if result == {}:
            result = create_topic(ncc_location, ncc_token, topic)
            if result != {}:
                logging.info(f'Topic "{topic}" created.')
                topics_to_assign.append(result)
            else:
                logging.warning(f'Topic "{topic}" not created.')
        else:
            logging.info(f'Topic "{topic}" already exists.')
            topics_to_assign.append(result)

    # Assign agents to topics
    if assign_agents_to_topics and (len(topics_to_assign) > 0):
        agent_user_profile = search_user_profiles(ncc_location, ncc_token, "Agent")
        if agent_user_profile != {}:
            agents = get_users(ncc_location, ncc_token, agent_user_profile["_id"])
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
                                ncc_location, ncc_token, topic["_id"], users
                            )
                            if success:
                                logging.info(
                                    f'Agent "{agent["firstName"]} {agent["lastName"]}" assigned to topic "{topic["name"]}".'
                                )
                            else:
                                logging.warning(
                                    f'Agent "{agent["firstName"]} {agent["lastName"]}" not assigned to topic "{topic["name"]}".'
                                )
            else:
                logging.warning("No agents found to assign to topics.")
        else:
            logging.warning('User profile "Agent" not found.')

    # Assign supervisors to topics
    if assign_supervisors_to_topics and (len(topics_to_assign) > 0):
        supervisor_user_profile = search_user_profiles(
            ncc_location, ncc_token, "Supervisor"
        )
        if supervisor_user_profile != {}:
            supervisors = get_users(
                ncc_location, ncc_token, supervisor_user_profile["_id"]
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
                                ncc_location, ncc_token, topic["_id"], users
                            )
                            if success:
                                logging.info(
                                    f'Supervisor "{supervisor["firstName"]} {supervisor["lastName"]}" assigned to topic "{topic["name"]}".'
                                )
                            else:
                                logging.warning(
                                    f'Supervisor "{supervisor["firstName"]} {supervisor["lastName"]}" not assigned to topic "{topic["name"]}".'
                                )
            else:
                logging.warning("No supervisors found to assign to topics.")
        else:
            logging.warning('User profile "Supervisor" not found.')

    # Create TEXT_TO_SPEECH service
    tts_service = search_services(ncc_location, ncc_token, "TEXT_TO_SPEECH")
    if tts_service != {}:
        logging.info('Service type "TEXT_TO_SPEECH" already exists.')
    else:
        tts_service = create_tts_service(
            ncc_location, ncc_token, "Test Google - Text To Speech"
        )
        if tts_service != {}:
            logging.info('Service type "TEXT_TO_SPEECH" created.')
        else:
            logging.warning('Service type "TEXT_TO_SPEECH" not created.')

    # Create GENERATIVE_AI service
    gen_ai_service = search_services(ncc_location, ncc_token, "GENERATIVE_AI")
    if gen_ai_service != {}:
        logging.info('Service type "GENERATIVE_AI" already exists.')
    else:
        gen_ai_service = create_gen_ai_service(
            ncc_location,
            ncc_token,
            "Test Google - Generative AI",
            f"thrio-prod-{tenant_id}",
        )
        if gen_ai_service != {}:
            logging.info('Service type "GENERATIVE_AI" created.')
        else:
            logging.warning('Service type "GENERATIVE_AI" not created.')

    # Search for REALTIME_ANALYSIS service
    real_time_transcription_service = search_services(
        ncc_location, ncc_token, "REALTIME_ANALYSIS"
    )
    if real_time_transcription_service != {}:
        logging.info('Service type "REALTIME_ANALYSIS" already exists.')
    else:
        # Create Deepgram API key
        deepgram_api_key_id = search_deepgram_api_keys(
            deepgram_project_id, deepgram_main_api_key, "Test Key"
        )
        if deepgram_api_key_id == "":
            deepgram_api_key = create_deepgram_api_key(
                deepgram_project_id, deepgram_main_api_key
            )
            if deepgram_api_key != "":
                logging.info('Deepgram API key "Test Key" created.')
            else:
                logging.warning('Deepgram API key "Test Key" not created.')
        else:
            logging.info('Deepgram API key "Test Key" already exists.')

    # Create REALTIME_ANALYSIS service
    if real_time_transcription_service == {} and deepgram_api_key != "":
        real_time_transcription_service = create_real_time_transcription_service(
            ncc_location,
            ncc_token,
            "Test Deepgram Real-Time Transcription",
            deepgram_api_key,
        )
        if real_time_transcription_service != {}:
            logging.info('Service "Test Deepgram Real-Time Transcription" created.')
        else:
            logging.warning(
                'Service "Test Deepgram Real-Time Transcription" not created.'
            )

    # Create classifications
    classifications_to_assign = []
    for classification in classifications:
        result = search_classifications(
            ncc_location, ncc_token, f"{campaign_name} - {classification["name"]}"
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
                logging.warning(
                    f'Classification "{campaign_name} - {classification["name"]}" not created.'
                )
        else:
            logging.info(
                f'Classification "{campaign_name} - {classification["name"]}" already exists.'
            )
            classifications_to_assign.append(result)

    # Create scorecard
    scorecard = search_scorecards(ncc_location, ncc_token, campaign_name)
    if scorecard == {}:
        scorecard = create_scorecard(ncc_location, ncc_token, campaign_name)
        if scorecard != {}:
            logging.info(f'Scorecard "{campaign_name}" created.')
        else:
            logging.warning(f'Scorecard "{campaign_name}" not created.')
    else:
        logging.info(f'Scorecard "{campaign_name}" already exists.')

    # Assign classifications to scorecard
    if scorecard != {}:
        for classification in classifications_to_assign:
            success = search_scorecard_classifications(
                ncc_location, ncc_token, scorecard["_id"], classification["_id"]
            )
            if success:
                logging.info(
                    f'Classification "{classification["name"]}" already assigned to scorecard.'
                )
            else:
                scorecard_classification = create_scorecard_classification(
                    ncc_location, ncc_token, scorecard["_id"], classification["_id"]
                )
                if scorecard_classification != {}:
                    logging.info(
                        f'Classification "{classification["name"]}" assigned to scorecard.'
                    )
                else:
                    logging.warning(
                        f'Classification "{classification["name"]}" not assigned to scorecard.'
                    )

    # Create templates
    templates_to_assign = []
    for template in templates:
        result = search_templates(ncc_location, ncc_token, template["name"])
        if result == {}:
            result = create_template(ncc_location, ncc_token, template)
            if result != {}:
                logging.info(f'Template "{template["name"]}" created.')
                templates_to_assign.append(result)
            else:
                logging.warning(f'Template "{template["name"]}" not created.')
        else:
            logging.info(f'Template "{template["name"]}" already exists.')
            templates_to_assign.append(result)

    # Create Search Contacts function
    search_contacts_function = search_functions(
        ncc_location, ncc_token, f"{campaign_name} - Search Contacts"
    )
    if search_contacts_function == {}:
        search_contacts_function = create_search_contacts_function(
            ncc_location, ncc_token, f"{campaign_name} - Search Contacts"
        )
        if search_contacts_function != {}:
            logging.info(f'Function "{campaign_name} - Search Contacts" created.')
        else:
            logging.warning(
                f'Function "{campaign_name} - Search Contacts" not created.'
            )
    else:
        logging.info(f'Function "{campaign_name} - Search Contacts" already exists.')

    # Create Two Way Chat function
    two_way_chat_function = search_functions(
        ncc_location, ncc_token, f"{campaign_name} - Two Way Chat"
    )
    if two_way_chat_function == {}:
        two_way_chat_function = create_two_way_chat_function(
            ncc_location, ncc_token, f"{campaign_name} - Two Way Chat"
        )
        if two_way_chat_function != {}:
            logging.info(f'Function "{campaign_name} - Two Way Chat" created.')
        else:
            logging.warning(f'Function "{campaign_name} - Two Way Chat" not created.')
    else:
        logging.info(f'Function "{campaign_name} - Two Way Chat" already exists.')

    # Create Two Way SMS function
    two_way_sms_function = search_functions(
        ncc_location, ncc_token, f"{campaign_name} - Two Way SMS"
    )
    if two_way_sms_function == {}:
        two_way_sms_function = create_two_way_sms_function(
            ncc_location, ncc_token, f"{campaign_name} - Two Way SMS"
        )
        if two_way_sms_function != {}:
            logging.info(f'Function "{campaign_name} - Two Way SMS" created.')
        else:
            logging.warning(f'Function "{campaign_name} - Two Way SMS" not created.')
    else:
        logging.info(f'Function "{campaign_name} - Two Way SMS" already exists.')

    # Create ACD Voicemail function
    acd_voicemail_function = search_functions(
        ncc_location, ncc_token, f"{campaign_name} - ACD Voicemail"
    )
    if acd_voicemail_function == {}:
        acd_voicemail_function = create_acd_voicemail_function(
            ncc_location, ncc_token, f"{campaign_name} - ACD Voicemail"
        )
        if acd_voicemail_function != {}:
            logging.info(f'Function "{campaign_name} - ACD Voicemail" created.')
        else:
            logging.warning(f'Function "{campaign_name} - ACD Voicemail" not created.')
    else:
        logging.info(f'Function "{campaign_name} - ACD Voicemail" already exists.')

    # Create ACD Callback function
    acd_callback_function = search_functions(
        ncc_location, ncc_token, f"{campaign_name} - ACD Callback"
    )
    if acd_callback_function == {}:
        acd_callback_function = create_acd_callback_function(
            ncc_location, ncc_token, f"{campaign_name} - ACD Callback"
        )
        if acd_callback_function != {}:
            logging.info(f'Function "{campaign_name} - ACD Callback" created.')
        else:
            logging.warning(f'Function "{campaign_name} - ACD Callback" not created.')
    else:
        logging.info(f'Function "{campaign_name} - ACD Callback" already exists.')

    # Create workflow
    workflow = search_workflows(ncc_location, ncc_token, campaign_name)
    if workflow == {}:
        if (
            acd_voicemail_function != {}
            and acd_callback_function != {}
            and search_contacts_function != {}
            and two_way_chat_function != {}
            and two_way_sms_function != {}
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
                    acd_voicemail_function,
                    acd_callback_function,
                )
            elif workflow_type == "non_iva_dtmf":
                if vertical == "general":
                    workflow = create_general_non_iva_dtmf_workflow(
                        ncc_location,
                        ncc_token,
                        campaign_name,
                        business_name,
                        queues_to_assign,
                        search_contacts_function,
                        two_way_chat_function,
                        two_way_sms_function,
                        acd_voicemail_function,
                        acd_callback_function,
                    )
                elif vertical == "hc":
                    workflow = create_hc_non_iva_dtmf_workflow(
                        ncc_location,
                        ncc_token,
                        campaign_name,
                        business_name,
                        queues_to_assign,
                        search_contacts_function,
                        two_way_chat_function,
                        two_way_sms_function,
                        acd_voicemail_function,
                        acd_callback_function,
                    )
                elif vertical == "finserv":
                    workflow = create_finserv_non_iva_dtmf_workflow(
                        ncc_location,
                        ncc_token,
                        campaign_name,
                        business_name,
                        queues_to_assign,
                        search_contacts_function,
                        two_way_chat_function,
                        two_way_sms_function,
                        acd_voicemail_function,
                        acd_callback_function,
                    )
                elif vertical == "insurance":
                    workflow = create_insurance_non_iva_dtmf_workflow(
                        ncc_location,
                        ncc_token,
                        campaign_name,
                        business_name,
                        queues_to_assign,
                        search_contacts_function,
                        two_way_chat_function,
                        two_way_sms_function,
                        acd_voicemail_function,
                        acd_callback_function,
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
                    acd_voicemail_function,
                    acd_callback_function,
                )
            if workflow != {}:
                logging.info(f'Workflow "{campaign_name}" created.')
            else:
                logging.warning(f'Workflow "{campaign_name}" not created.')
        else:
            logging.warning("Insufficient data to create workflow.")
    else:
        logging.info(f'Workflow "{campaign_name}" already exists.')

    # Create campaign
    campaign = search_campaigns_by_name(ncc_location, ncc_token, campaign_name)
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
                logging.info(f'Campaign "{campaign_name}" created.')
            else:
                logging.warning(f'Campaign "{campaign_name}" not created.')
        else:
            logging.warning("Insufficient data to create campaign.")
    else:
        logging.info(f'Campaign "{campaign_name}" already exists.')

    # Assign campaign address to campaign
    if campaign != {} and campaign_address != "":
        success = assign_address_to_campaign(
            ncc_location, ncc_token, campaign_address, campaign["_id"]
        )
        if success:
            logging.info(f'PSTN number "{campaign_address}" assigned to campaign.')
        else:
            logging.warning(
                f'PSTN number "{campaign_address}" not assigned to campaign.'
            )

    # Update chat survey campaign ID
    if campaign != {} and chat_survey != {}:
        success = update_chat_survey_campaign_id(
            ncc_location, ncc_token, chat_survey["_id"], campaign["_id"]
        )
        if success:
            logging.info(f'Survey "{chat_survey["name"]}" updated with new campaign.')
        else:
            logging.warning(
                f'Survey "{chat_survey["name"]}" not updated with new campaign.'
            )

    # Assign dispositions to campaign
    if campaign != {}:
        for disposition in dispositions_to_assign:
            success = search_campaign_dispositions(
                ncc_location, ncc_token, campaign["_id"], disposition["_id"]
            )
            if not success:
                success = create_campaign_disposition(
                    ncc_location, ncc_token, campaign["_id"], disposition["_id"]
                )
                if success:
                    logging.info(
                        f'Disposition "{disposition["name"]}" assigned to campaign.'
                    )
                else:
                    logging.warning(
                        f'Disposition "{disposition["name"]}" not assigned to campaign.'
                    )
            else:
                logging.info(
                    f'Disposition "{disposition["name"]}" already assigned to campaign.'
                )

    # Assign scorecard to campaign
    if campaign != {} and scorecard != {}:
        success = search_campaign_scorecards(
            ncc_location, ncc_token, campaign["_id"], scorecard["_id"]
        )
        if not success:
            success = create_campaign_scorecard(
                ncc_location, ncc_token, campaign["_id"], scorecard["_id"]
            )
            if success:
                logging.info(f'Scorecard "{scorecard["name"]}" assigned to campaign.')
            else:
                logging.warning(
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
                ncc_location, ncc_token, campaign["_id"], template["_id"]
            )
            if not success:
                success = create_campaign_template(
                    ncc_location, ncc_token, campaign["_id"], template["_id"]
                )
                if success:
                    logging.info(f'Template "{template["name"]}" assigned to campaign.')
                else:
                    logging.warning(
                        f'Template "{template["name"]}" not assigned to campaign.'
                    )
            else:
                logging.info(
                    f'Template "{template["name"]}" already assigned to campaign.'
                )

    # Assign supervisors to campaign
    if campaign != {} and assign_supervisors_to_campaign:
        supervisor_user_profile = search_user_profiles(
            ncc_location, ncc_token, "Supervisor"
        )
        if supervisor_user_profile != {}:
            supervisors = get_users(
                ncc_location, ncc_token, supervisor_user_profile["_id"]
            )
            if len(supervisors) > 0:
                for supervisor in supervisors:
                    success = search_supervisor_campaigns(
                        ncc_location, ncc_token, supervisor["_id"], campaign["_id"]
                    )
                    if success:
                        logging.info(
                            f'Supervisor "{supervisor["firstName"]} {supervisor["lastName"]}" already assigned to "{campaign["name"]}" campaign.'
                        )
                    else:
                        success = create_supervisor_campaign(
                            ncc_location, ncc_token, supervisor["_id"], campaign["_id"]
                        )
                        if success:
                            logging.info(
                                f'Supervisor "{supervisor["firstName"]} {supervisor["lastName"]}" assigned to "{campaign["name"]}" campaign.'
                            )
                        else:
                            logging.warning(
                                f'Supervisor "{supervisor["firstName"]} {supervisor["lastName"]}" not assigned to "{campaign["name"]}" campaign.'
                            )
            else:
                logging.warning("No supervisors found to assign to campaign.")
        else:
            logging.warning('User profile "Supervisor" not found.')

    # Create reports
    for report in reports:
        result = search_reports(ncc_location, ncc_token, report["name"])
        if result == {}:
            result = create_report(ncc_location, ncc_token, report)
            if result != {}:
                logging.info(f'Report "{report["name"]}" created')
            else:
                logging.warning(f'Report "{report["name"]}" not created.')
        else:
            logging.info(f'Report "{report["name"]}" already exists.')

    duration = datetime.datetime.now() - start_time
    logging.info(f"Duration: {str(duration)}")
