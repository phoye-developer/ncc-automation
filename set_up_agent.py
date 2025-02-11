import datetime
import logging
from ncc_user_profile import *
from ncc_user import *
from ncc_queue import *
from ncc_user_queue import *


def set_up_agent(ncc_location: str, ncc_token: str):
    """
    This function creates an agent in Nextiva Contact Center (NCC) and assigns them to queues.
    """
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

    # Select whether to assign agents to queues
    choice = ""
    while choice == "":
        print("Please select whether to assign agent to all queues.")
        print("----------------------------------------------------")
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

    start_time = datetime.datetime.now()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    logging.info("Starting...")
    # Create agent
    agent = search_users(ncc_location, ncc_token, first_name, last_name)
    if agent == {}:
        agent_user_profile = search_user_profiles(ncc_location, ncc_token, "Agent")
        if agent_user_profile != {}:
            agent = create_user(
                ncc_location,
                ncc_token,
                first_name,
                last_name,
                email,
                agent_user_profile["_id"],
            )
            if agent != {}:
                logging.info(f'"{first_name} {last_name}" user created.')
            else:
                logging.warning(f'"{first_name} {last_name}" user not created.')
        else:
            logging.warning('"Agent" user profile not found.')
    else:
        logging.info(f'"{first_name} {last_name}" user already exists.')

    # Assign agent to queues
    if agent != {} and assign_agents:
        queues = get_queues(ncc_location, ncc_token)
        if len(queues) > 0:
            for queue in queues:
                success = search_user_queues(
                    ncc_location, ncc_token, agent["_id"], queue["_id"]
                )
                if success:
                    logging.info(
                        f'"{agent["name"]}" agent already assigned to "{queue["name"]}" queue.'
                    )
                else:
                    success = create_user_queue(
                        ncc_location, ncc_token, agent["_id"], queue["_id"]
                    )
                    if success:
                        logging.info(
                            f'"{agent["name"]}" agent assigned to "{queue["name"]}" queue.'
                        )
                    else:
                        logging.warning(
                            f'"{agent["name"]}" agent not assigned to "{queue["name"]}" queue.'
                        )
        else:
            logging.warning("No queues found for assignment.")

    duration = datetime.datetime.now() - start_time
    logging.info(f"Duration: {str(duration)}")
