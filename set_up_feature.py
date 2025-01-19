from ncc_workflow import *
from ncc_function import *


def set_up_feature(ncc_location: str, ncc_token: str):
    """
    This function presents a menu to set up a new feature on an existing campaign.
    """

    # Select feature
    print()
    print("Please select a feature.")
    choice = ""
    while choice == "":
        print()
        print("1. Post-call phone survey")
        print("2. Post-workitem SMS text with survey link")
        print()
        choice = input("Command: ")
        print()
        if choice == "1":
            set_up_post_call_phone_survey(ncc_location, ncc_token, "Test Workflow")
        elif choice == "2":
            set_up_post_workitem_sms_text_with_survey_link(
                ncc_location, ncc_token, "Test Workflow"
            )
        else:
            choice = ""
            print("Invalid choice. Please try again.")


def set_up_post_call_phone_survey(
    ncc_location: str, ncc_token: str, workflow_name: str
):
    """
    This function creates a function relevant to post-call phone surveys and modifies a workflow to use that function.
    """
    print('Searching for "Test Workflow"...', end="")
    workflow = search_workflows(ncc_location, ncc_token, workflow_name)
    if workflow != {}:
        workflow_id = workflow["_id"]
        print("found.")
        print('Searching for "Test Post-Call Phone Survey" function...', end="")
        function = search_functions(
            ncc_location, ncc_token, "Test Post-Call Phone Survey"
        )
        if function == {}:
            print("not found.")
            print('Creating "Test Post-Call Phone Survey" function...', end="")
            function = create_function(
                ncc_location, ncc_token, post_call_phone_survey_function_body
            )
            if function != {}:
                function_id = function["_id"]
                print("success!")
                print('Adding "Extend Call" component...', end="")
                success = add_extend_call_component(
                    ncc_location, ncc_token, workflow_id, function_id
                )
                if success:
                    print("success!")
                else:
                    print("failed.")
            else:
                print("failed.")
        else:
            print("found.")
    else:
        print("not found.")


def set_up_post_workitem_sms_text_with_survey_link(
    ncc_location: str, ncc_token: str, workflow_name: str
):
    print('Searching for "Test Workflow"...', end="")
    workflow = search_workflows(ncc_location, ncc_token, workflow_name)
    if workflow != {}:
        workflow_id = workflow["_id"]
        print("found.")
        print('Adding "SMS Message Consumer" component...', end="")
        success = add_sms_message_consumer_survey_link(
            ncc_location, ncc_token, workflow_id
        )
        if success:
            print("success!")
        else:
            print("failed.")
    else:
        print("not found.")
