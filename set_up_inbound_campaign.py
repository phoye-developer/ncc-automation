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
from ncc_survey_theme import *
from ncc_survey import *
from ncc_classification import *
from ncc_scorecard import *
from ncc_scorecard_classification import *
from ncc_campaign_scorecard import *
from ncc_template import *
from ncc_campaign_template import *
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

    start_time = datetime.datetime.now()

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
        print()
        choice = input("Command: ")
        print()
        if choice == "1":
            dispositions = general_dispositions
            queues = general_queues
            classifications = general_classifications
            templates = general_templates
            topics = general_topics
            reports = general_reports
        elif choice == "2":
            dispositions = general_dispositions + hc_dispositions
            queues = general_queues + hc_queues
            classifications = general_classifications + hc_classifications
            templates = general_templates + hc_templates
            topics = general_topics + hc_topics
            reports = general_reports + hc_reports
        elif choice == "3":
            dispositions = general_dispositions + finserv_dispositions
            queues = general_queues + finserv_queues
            classifications = general_classifications + finserv_classifications
            templates = general_templates + finserv_templates
            topics = general_topics + finserv_topics
            reports = general_reports + finserv_reports
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
            workflow_type = iva_workflow
        elif choice == "2":
            workflow_type = non_iva_workflow
        elif choice == "3":
            workflow_type = direct_line_workflow
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
        print("Please select whether to assign all agents to all queues.")
        print("---------------------------------------------------------")
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

    logging.info("Starting...")
    # Create dispositions
    dispositions_to_assign = []
    for disposition in dispositions:
        result = search_dispositions(ncc_location, ncc_token, disposition["name"])
        if result == {}:
            result = create_disposition(ncc_location, ncc_token, disposition)
            if result != {}:
                logging.info(f'"{result["name"]}" disposition created.')
                dispositions_to_assign.append(result)
                tenant_id = result["tenantId"]
            else:
                logging.warning(f'"{disposition["name"]}" disposition not created.')
        else:
            logging.info(f'"{result["name"]}" disposition already exists.')
            dispositions_to_assign.append(result)
            tenant_id = result["tenantId"]

    # Assign user profiles to dispositions
    for user_profile in user_profiles:
        result = search_user_profiles(ncc_location, ncc_token, user_profile)
        if result != {}:
            logging.info(f'"{user_profile}" user profile found.')
            for disposition in dispositions_to_assign:
                success = search_user_profile_dispositions(
                    ncc_location, ncc_token, disposition["_id"], result["_id"]
                )
                if success:
                    logging.info(
                        f'"{disposition["name"]}" disposition already assigned.'
                    )
                else:
                    user_profile_disposition = create_user_profile_disposition(
                        ncc_location, ncc_token, result["_id"], disposition["_id"]
                    )
                    if user_profile_disposition != {}:
                        logging.info(f'"{disposition["name"]}" disposition assigned.')
                    else:
                        logging.warning(
                            f'"{disposition["name"]}" disposition not assigned.'
                        )
        else:
            logging.warning(f'"{user_profile}" user profile not found.')

    # Create queues
    queues_to_assign = {}
    for queue in queues:
        result = search_queues(ncc_location, ncc_token, queue["name"])
        if result == {}:
            result = create_queue(ncc_location, ncc_token, queue)
            if result != {}:
                logging.info(f'"{result["name"]}" queue created.')
                queues_to_assign[result["name"]] = result["_id"]
            else:
                logging.warning("Queue not created.")
        else:
            logging.info(f'"{queue["name"]}" queue already exists.')
            queues_to_assign[result["name"]] = result["_id"]

    # Assign agents to queues
    if assign_agents and (len(queues_to_assign) > 0):
        agent_user_profile = search_user_profiles(ncc_location, ncc_token, "Agent")
        if agent_user_profile != {}:
            agents = get_users(ncc_location, ncc_token, agent_user_profile["_id"])
            if len(agents) > 0:
                for agent in agents:
                    for key, value in queues_to_assign.items():
                        success = search_user_queues(ncc_location, ncc_token, agent["_id"], value)
                        if success:
                            logging.info(f'"{agent["name"]}" agent already assigned to "{key}" queue.')
                        else:
                            success = create_user_queue(ncc_location, ncc_token, agent["_id"], value)
                            if success:
                                logging.info(f'"{agent["name"]}" agent assigned to "{key}" queue.')
                            else:
                                logging.warning(f'"{agent["name"]}" agent not assigned to "{key}" queue.')
            else:
                logging.warning("No agents found to assign to queues.")
        else:
            logging.warning('"Agent" user profile not found.')

    # Create survey theme
    survey_theme = search_survey_themes(
        ncc_location, ncc_token, f"Test {business_name}"
    )
    if survey_theme == {}:
        survey_theme = create_survey_theme(
            ncc_location, ncc_token, f"Test {business_name}"
        )
        if survey_theme != {}:
            logging.info(f'"Test {business_name}" survey theme created.')
        else:
            logging.warning(f'"Test {business_name}" survey theme not created.')
    else:
        logging.info(f'"Test {business_name}" survey theme already exists.')

    # Create user survey
    user_survey = search_surveys(ncc_location, ncc_token, f"{campaign_name} - User")
    if user_survey == {}:
        user_survey = create_survey(
            ncc_location,
            ncc_token,
            f"{campaign_name} - User",
            main_user_survey_body,
            survey_theme,
        )
        if user_survey != {}:
            logging.info(f'"{campaign_name} - User" survey created.')
        else:
            logging.warning(f'"{campaign_name} - User" survey not created.')
    else:
        logging.info(f'"{campaign_name} - User" survey already exists.')

    # Create chat survey
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
            logging.info(f'"{campaign_name} - Chat" survey created.')
        else:
            logging.warning(f'"{campaign_name} - Chat" survey not created.')
    else:
        logging.info(f'"{campaign_name} - Chat" survey already exists.')

    # Create QM survey
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
            logging.info(f'"{campaign_name} - QM" survey created.')
        else:
            logging.warning(f'"{campaign_name} - QM" survey not created.')
    else:
        logging.info(f'"{campaign_name} - QM" survey already exists')

    # Create topic
    for topic in topics:
        result = search_topics(ncc_location, ncc_token, topic)
        if result == {}:
            result = create_topic(ncc_location, ncc_token, topic)
            if result != {}:
                logging.info(f'"{topic}" topic created.')
            else:
                logging.warning(f'"{topic}" topic not created.')
        else:
            logging.info(f'"{topic}" topic already exists.')

    # Create TEXT_TO_SPEECH service
    tts_service = search_services(ncc_location, ncc_token, "TEXT_TO_SPEECH")
    if tts_service != {}:
        logging.info('"TEXT_TO_SPEECH" type service already exists.')
    else:
        tts_service = create_tts_service(
            ncc_location, ncc_token, "Test Google - Text To Speech"
        )
        if tts_service != {}:
            logging.info('"TEXT_TO_SPEECH" type service created.')
        else:
            logging.warning('"TEXT_TO_SPEECH" type service not created.')

    # Create GENERATIVE_AI service
    gen_ai_service = search_services(ncc_location, ncc_token, "GENERATIVE_AI")
    if gen_ai_service != {}:
        logging.info('"GENERATIVE_AI" type service already exists.')
    else:
        gen_ai_service = create_gen_ai_service(
            ncc_location,
            ncc_token,
            "Test Google - Generative AI",
            f"thrio-prod-{tenant_id}",
        )
        if gen_ai_service != {}:
            logging.info('"GENERATIVE_AI" type service created.')
        else:
            logging.warning('"GENERATIVE_AI" type service not created.')

    # Search for REALTIME_ANALYSIS service
    real_time_transcription_service = search_services(
        ncc_location, ncc_token, "REALTIME_ANALYSIS"
    )
    if real_time_transcription_service != {}:
        logging.info('"REALTIME_ANALYSIS" type service already exists.')
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
                logging.info('"Test Key" Deepgram API key created.')
            else:
                logging.warning('"Test Key" Deepgram API key not created.')
        else:
            logging.info('"Test Key" Deepgram API key already exists.')

    # Create REALTIME_ANALYSIS service
    if real_time_transcription_service == {} and deepgram_api_key != "":
        real_time_transcription_service = create_real_time_transcription_service(
            ncc_location,
            ncc_token,
            "Test Deepgram Real-Time Transcription",
            deepgram_api_key,
        )
        if real_time_transcription_service != {}:
            logging.info('"Test Deepgram Real-Time Transcription" service created.')
        else:
            logging.warning(
                '"Test Deepgram Real-Time Transcription" service not created.'
            )

    # Create classifications
    classifications_to_assign = []
    for classification in classifications:
        result = search_classifications(ncc_location, ncc_token, classification["name"])
        if result == {}:
            result = create_classification(ncc_location, ncc_token, classification)
            if result != {}:
                logging.info(f'"{classification["name"]}" classification created.')
                classifications_to_assign.append(result)
            else:
                logging.warning(
                    f'"{classification["name"]}" classification not created.'
                )
        else:
            logging.info(f'"{classification["name"]}" classification already exists.')
            classifications_to_assign.append(result)

    # Create scorecard
    scorecard = search_scorecards(ncc_location, ncc_token, campaign_name)
    if scorecard == {}:
        scorecard = create_scorecard(ncc_location, ncc_token, campaign_name)
        if scorecard != {}:
            logging.info(f'"{campaign_name}" scorecard created.')
        else:
            logging.warning(f'"{campaign_name}" scorecard not created.')
    else:
        logging.info(f'"{campaign_name}" scorecard already exists.')

    # Assign classifications to scorecard
    if scorecard != {}:
        for classification in classifications_to_assign:
            success = search_scorecard_classifications(
                ncc_location, ncc_token, classification["_id"], scorecard["_id"]
            )
            if success:
                logging.info(
                    f'"{classification["name"]}" classification already assigned to scorecard.'
                )
            else:
                scorecard_classification = create_scorecard_classification(
                    ncc_location, ncc_token, scorecard["_id"], classification["_id"]
                )
                if scorecard_classification != {}:
                    logging.info(
                        f'"{classification["name"]}" classification assigned to scorecard.'
                    )
                else:
                    logging.warning(
                        f'"{classification["name"]}" classification not assigned to scorecard.'
                    )

    # Create templates
    templates_to_assign = []
    for template in templates:
        result = search_templates(ncc_location, ncc_token, template["name"])
        if result == {}:
            result = create_template(ncc_location, ncc_token, template)
            if result != {}:
                logging.info(f'"{template["name"]}" template created.')
                templates_to_assign.append(result)
            else:
                logging.warning(f'"{template["name"]}" template not created.')
        else:
            logging.info(f'"{template["name"]}" template already exists.')
            templates_to_assign.append(result)

    # Create ACD Voicemail function
    acd_voicemail_function = search_functions(
        ncc_location, ncc_token, "Test ACD Voicemail"
    )
    if acd_voicemail_function == {}:
        acd_voicemail_function = create_function(
            ncc_location, ncc_token, acd_voicemail_function_body
        )
        if acd_voicemail_function != {}:
            logging.info(f'"Test ACD Voicemail" function created.')
        else:
            logging.warning(f'"Test ACD Voicemail" function not created.')
    else:
        logging.info(f'"Test ACD Voicemail" function already exists.')

    # Create ACD Callback function
    acd_callback_function = search_functions(
        ncc_location, ncc_token, "Test ACD Callback"
    )
    if acd_callback_function == {}:
        acd_callback_function = create_function(
            ncc_location, ncc_token, acd_callback_function_body
        )
        if acd_callback_function != {}:
            logging.info(f'"Test ACD Callback" function created.')
        else:
            logging.warning(f'"Test ACD Callback" function not created.')
    else:
        logging.info(f'"Test ACD Callback" function already exists.')

    # Create workflow
    workflow = search_workflows(ncc_location, ncc_token, campaign_name)
    if workflow == {}:
        workflow = create_workflow(
            ncc_location,
            ncc_token,
            workflow_type,
            campaign_name,
            business_name,
            queues_to_assign,
            acd_voicemail_function,
            acd_callback_function,
        )
        if workflow != {}:
            logging.info(f'"{campaign_name}" workflow created.')
        else:
            logging.warning(f'"{campaign_name}" workflow not created.')
    else:
        logging.info(f'"{campaign_name}" workflow already exists.')

    # Create campaign
    campaign = search_campaigns_by_name(ncc_location, ncc_token, campaign_name)
    if campaign == {}:
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
            logging.info(f'"{campaign_name}" campaign created.')
        else:
            logging.warning(f'"{campaign_name}" campaign not created.')
    else:
        logging.info(f'"{campaign_name}" campaign already exists.')

    # Assign campaign address to campaign
    if campaign != {} and campaign_address != "":
        success = assign_address_to_campaign(
            ncc_location, ncc_token, campaign_address, campaign["_id"]
        )
        if success:
            logging.info(f'"{campaign_address}" assigned to campaign.')
        else:
            logging.warning(f'"{campaign_address}" not assigned to campaign.')

    # Update chat survey campaign ID
    if campaign != {} and chat_survey != {}:
        success = update_chat_survey_campaign_id(
            ncc_location, ncc_token, chat_survey["_id"], campaign["_id"]
        )
        if success:
            logging.info(f'"{chat_survey["name"]}" survey updated with new campaign.')
        else:
            logging.warning(
                f'"{chat_survey["name"]}" survey not updated with new campaign.'
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
                        f'"{disposition["name"]}" disposition assigned to campaign.'
                    )
                else:
                    logging.warning(
                        f'"{disposition["name"]}" disposition not assigned to campaign.'
                    )
            else:
                logging.info(
                    f'"{disposition["name"]}" disposition already assigned to campaign.'
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
                logging.info(f'"{scorecard["name"]}" scorecard assigned to campaign.')
            else:
                logging.warning(
                    f'"{scorecard["name"]}" scorecard not assigned to campaign.'
                )
        else:
            logging.info(
                f'"{scorecard["name"]}" scorecard already assigned to campaign.'
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
                    logging.info(f'"{template["name"]}" template assigned to campaign.')
                else:
                    logging.warning(
                        f'"{template["name"]}" template not assigned to campaign.'
                    )
            else:
                logging.info(
                    f'"{template["name"]}" template already assigned to campaign.'
                )

    # Create reports
    for report in reports:
        result = search_reports(ncc_location, ncc_token, report["name"])
        if result == {}:
            result = create_report(ncc_location, ncc_token, report)
            if result != {}:
                logging.info(f'"{report["name"]}" report created')
            else:
                logging.warning(f'"{report["name"]}" report not created.')
        else:
            logging.info(f'"{report["name"]}" report already exists.')

    duration = datetime.datetime.now() - start_time
    logging.info(f"Duration: {str(duration)}")
