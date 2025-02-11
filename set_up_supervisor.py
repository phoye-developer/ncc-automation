import datetime
import logging
from ncc_user_profile import *
from ncc_user import *
from ncc_queue import *
from ncc_user_queue import *
from ncc_supervisor_user import *
from ncc_supervisor_queue import *
from ncc_campaign import *
from ncc_supervisor_campaign import *


def set_up_supervisor(ncc_location: str, ncc_token: str):
    """
    This function creates a supervisor in Nextiva Contact Center (NCC), assigns them to queues, and assigns agents for them to supervise.
    """

    start_time = datetime.datetime.now()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Enter first name
    first_name = ""
    while first_name == "":
        print()
        first_name = input("First name: ")
        if first_name == "":
            print()
            print("Invalid first name.")
        else:
            first_name = f"Test {first_name}"

    # Enter last name
    last_name = ""
    while last_name == "":
        print()
        last_name = input("Last name: ")
        if last_name == "":
            print()
            print("Invalid last name.")

    # Enter email
    email = ""
    while email == "":
        print()
        email = input("Email: ")
        if email == "":
            print()
            print("Invalid email.")
        else:
            print()

    # Select whether to assign supervisors to queues
    choice = ""
    while choice == "":
        print("Assign supervisor to all queues?")
        print("--------------------------------")
        print("1. Yes")
        print("2. No")
        print()
        choice = input("Command: ")
        print()
        if choice == "1":
            assign_to_queues = True
        elif choice == "2":
            assign_to_queues = False
        else:
            choice = ""
            print("Invalid choice.")
            print()

    # Select whether to assign all agents to the supervisor
    choice = ""
    while choice == "":
        print("Assign all agents to supervisor?")
        print("--------------------------------")
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

    # Select whether to assign all campaigns to the supervisor
    choice = ""
    while choice == "":
        print("Assign supervisor to all campaigns?")
        print("-----------------------------------")
        print("1. Yes")
        print("2. No")
        print()
        choice = input("Command: ")
        print()
        if choice == "1":
            assign_to_campaigns = True
        elif choice == "2":
            assign_to_campaigns = False
        else:
            choice = ""
            print("Invalid choice.")
            print()

    logging.info("Starting...")
    # Create supervisor
    supervisor = search_users(ncc_location, ncc_token, first_name, last_name)
    if supervisor == {}:
        supervisor_user_profile = search_user_profiles(
            ncc_location, ncc_token, "Supervisor"
        )
        if supervisor_user_profile != {}:
            supervisor = create_user(
                ncc_location,
                ncc_token,
                first_name,
                last_name,
                email,
                supervisor_user_profile["_id"],
            )
            if supervisor != {}:
                logging.info(f'"{first_name} {last_name}" supervisor user created.')
            else:
                logging.warning(
                    f'"{first_name} {last_name}" supervisor user not created.'
                )
        else:
            logging.warning('"Supervisor" user profile not found.')
    else:
        logging.info(f'"{first_name} {last_name}" supervisor user already exists.')

    # Assign supervisor to queues
    if supervisor != {} and assign_to_queues:
        queues = get_queues(ncc_location, ncc_token)
        if len(queues) > 0:
            for queue in queues:
                success = search_supervisor_queues(
                    ncc_location, ncc_token, supervisor["_id"], queue["_id"]
                )
                if success:
                    logging.info(
                        f'"{supervisor["name"]}" supervisor already assigned to "{queue["name"]}" queue.'
                    )
                else:
                    success = create_supervisor_queue(
                        ncc_location, ncc_token, supervisor["_id"], queue["_id"]
                    )
                    if success:
                        logging.info(
                            f'"{supervisor["name"]}" supervisor assigned to "{queue["name"]}" queue.'
                        )
                    else:
                        logging.warning(
                            f'"{supervisor["name"]}" supervisor not assigned to "{queue["name"]}" queue.'
                        )
        else:
            logging.warning("No queues found for assignment.")

    # Assign agents to supervisor
    if supervisor != {} and assign_agents:
        agent_user_profile = search_user_profiles(ncc_location, ncc_token, "Agent")
        if agent_user_profile != {}:
            agents = get_users(ncc_location, ncc_token, agent_user_profile["_id"])
            if len(agents) > 0:
                for agent in agents:
                    success = search_supervisor_users(
                        ncc_location, ncc_token, supervisor["_id"], agent["_id"]
                    )
                    if success:
                        logging.info(
                            f'"{agent["firstName"]} {agent["lastName"]}" already assigned to "{first_name} {last_name}".'
                        )
                    else:
                        success = create_supervisor_user(
                            ncc_location, ncc_token, supervisor["_id"], agent["_id"]
                        )
                        if success:
                            logging.info(
                                f'"{agent["firstName"]} {agent["lastName"]}" assigned to "{first_name} {last_name}".'
                            )
                        else:
                            logging.warning(
                                f'"{agent["firstName"]} {agent["lastName"]}" not assigned to "{first_name} {last_name}".'
                            )
            else:
                logging.warning("No agents found for assignment.")
        else:
            logging.warning('"Agent" user profile not found.')

    # Assign supervisor to campaigns
    if supervisor != {} and assign_to_campaigns:
        campaigns = get_campaigns(ncc_location, ncc_token)
        if len(campaigns) > 0:
            for campaign in campaigns:
                success = search_supervisor_campaigns(
                    ncc_location, ncc_token, supervisor["_id"], campaign["_id"]
                )
                if success:
                    logging.info(
                        f'"{first_name} {last_name}" already assigned to "{campaign["name"]}" campaign.'
                    )
                else:
                    success = create_supervisor_campaign(
                        ncc_location, ncc_token, supervisor["_id"], campaign["_id"]
                    )
                    if success:
                        logging.info(
                            f'"{first_name} {last_name}" assigned to "{campaign["name"]}" campaign.'
                        )
                    else:
                        logging.warning(
                            f'"{first_name} {last_name}" not assigned to "{campaign["name"]}" campaign'
                        )
        else:
            logging.warning("No campaigns found for assignment.")

    duration = datetime.datetime.now() - start_time
    logging.info(f"Duration: {str(duration)}")
