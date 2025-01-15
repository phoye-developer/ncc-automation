# Deepgram
deepgram_project_id = "90b9d6eb-c8c6-46a9-a0d7-c35f585403c4"

# NCC entities
general_dispositions = [
    "Test Billing",
    "Test Customer Service",
    "Test Callback",
    "Test Block Number",
]
hc_dispositions = [
    "Test Refill Prescription",
    "Test Schedule Appointment",
    "Test Reschedule Appointment",
    "Test Cancel Appointment",
]
finserv_dispositions = [
    "Test Credit Card Application",
    "Test Loan Application",
    "Test Open Account",
    "Test Close Account",
]

user_profiles = ["Agent", "Supervisor", "Administrator"]

general_queues = [
    "Test Billing",
    "Test Customer Service",
    "Test Sales",
    "Test Technical Support",
]
hc_queues = [
    "Test Prescription Refills",
    "Test Appointments",
]
finserv_queues = [
    "Test Credit Card Applications",
    "Test Loan Applications",
    "Test Accounts",
]

hubspot_survey_body = {
    "hideSurveyBoxShadown": False,
    "type": "full",
    "showFooter": False,
    "surveythemeId": "5f6784bc8fbed55422effb9b",
    "showTabs": True,
    "showBottomNavigatorPage": False,
    "height": 1130,
    "debug": False,
    "localizations": {
        "name": {
            "en": {
                "language": "en",
                "value": "Test HubSpot"
            }
        }
    },
    "showHeader": False,
    "allowTabinationMandatoryFields": False,
    "entryPanelId": "6568d29611501e41ad52c81d",
    "layout": {
        "elements": [
            {
                "icon": "icon-ui-panel",
                "name": "Panel",
                "description": "Basic component to display content in a survey",
                "type": "panel",
                "component": "panel",
                "elements": [
                    {
                        "icon": "icon-ui-panel",
                        "name": "Panel",
                        "description": "Basic component to display content in a survey",
                        "type": "panel",
                        "component": "panel",
                        "elements": [
                            {
                                "icon": "icon-ui-text",
                                "name": "Text",
                                "description": "Displays direct text to the customer",
                                "type": "label",
                                "component": "label",
                                "elements": [],
                                "properties": {
                                    "label": "<strong>HubSpot Information</strong>",
                                    "fontSize": 18,
                                    "margin": "8px",
                                    "alignment": "center"
                                },
                                "_id": "6568d2c4a60469f242e09c33",
                                "selected": False,
                                "show": True
                            },
                            {
                                "icon": "icon-ui-text",
                                "name": "Text",
                                "description": "Displays direct text to the customer",
                                "type": "label",
                                "component": "label",
                                "elements": [],
                                "properties": {
                                    "label": "Thank you for calling ${workitem.data.companyName}. My name is _. How can I help you today?",
                                    "fontSize": 16,
                                    "width": "95%",
                                    "alignment": "center",
                                    "condition": "${workitem.type} == 'InboundCall'"
                                },
                                "_id": "65ea549972b85bedb9e21bc4",
                                "selected": False,
                                "show": True
                            }
                        ],
                        "properties": {
                            "label": "",
                            "labelAlignment": "left",
                            "labelFontSize": "24",
                            "descriptionAlignment": "left",
                            "descriptionFontSize": "24",
                            "alignment": "justify",
                            "canCollapse": False,
                            "state": False,
                            "scroll": False,
                            "showScrollbar": False,
                            "vertical": "fit",
                            "direction": "column",
                            "panelShadow": False,
                            "showOverlay": False,
                            "showHeader": False,
                            "allowPanelInDashboard": False
                        },
                        "_id": "6568d301fafdb453c286c263",
                        "selected": False,
                        "show": True
                    },
                    {
                        "icon": "icon-ui-panel",
                        "name": "Panel",
                        "description": "Basic component to display content in a survey",
                        "type": "panel",
                        "component": "panel",
                        "elements": [
                            {
                                "icon": "icon-ui-input",
                                "name": "Input",
                                "description": "A box for the customer to enter information",
                                "type": "input",
                                "component": "input",
                                "elements": [],
                                "properties": {
                                    "label": "First Name",
                                    "labelInReport": "firstName",
                                    "fontSize": "14",
                                    "width": "100%",
                                    "margin": "8px",
                                    "fieldname": "firstName",
                                    "defaultValue": "${workitem.data.hubSpotFirstName}",
                                    "mandatory": False,
                                    "readOnly": True,
                                    "validateOnInput": False,
                                    "sensitiveData": False,
                                    "saveToLocalStorage": False
                                },
                                "_id": "6568d3ade17f756c6978be2d",
                                "selected": False,
                                "show": True
                            },
                            {
                                "icon": "icon-ui-input",
                                "name": "Input",
                                "description": "A box for the customer to enter information",
                                "type": "input",
                                "component": "input",
                                "elements": [],
                                "properties": {
                                    "label": "Last Name",
                                    "labelInReport": "lastName",
                                    "fontSize": "14",
                                    "width": "100%",
                                    "margin": "8px",
                                    "fieldname": "lastName",
                                    "defaultValue": "${workitem.data.hubSpotLastName}",
                                    "mandatory": False,
                                    "readOnly": True,
                                    "validateOnInput": False,
                                    "sensitiveData": False,
                                    "saveToLocalStorage": False
                                },
                                "_id": "6570ab7dc4edc2a9af3097a4",
                                "selected": False,
                                "show": True
                            },
                            {
                                "icon": "icon-ui-input",
                                "name": "Input",
                                "description": "A box for the customer to enter information",
                                "type": "input",
                                "component": "input",
                                "elements": [],
                                "properties": {
                                    "label": "Phone",
                                    "labelInReport": "phone",
                                    "fontSize": "14",
                                    "width": "100%",
                                    "margin": "8px",
                                    "fieldname": "phone",
                                    "defaultValue": "${workitem.data.phone}",
                                    "mandatory": False,
                                    "readOnly": True,
                                    "validateOnInput": False,
                                    "sensitiveData": False,
                                    "saveToLocalStorage": False
                                },
                                "_id": "6568d4005c8b218f2803ecee",
                                "selected": False,
                                "show": True
                            }
                        ],
                        "properties": {
                            "label": "",
                            "labelAlignment": "left",
                            "labelFontSize": "24",
                            "descriptionAlignment": "left",
                            "descriptionFontSize": "24",
                            "alignment": "justify",
                            "canCollapse": False,
                            "state": False,
                            "scroll": False,
                            "showScrollbar": False,
                            "vertical": "fit",
                            "direction": "column",
                            "margin": "8px",
                            "panelShadow": False,
                            "showOverlay": False,
                            "showHeader": False,
                            "allowPanelInDashboard": False
                        },
                        "_id": "6568d32e7590d268980778f1",
                        "selected": False,
                        "show": True
                    },
                    {
                        "icon": "icon-auto-accept-interaction",
                        "name": "Action",
                        "description": "Calls APIs and Thrio dispositions",
                        "type": "action",
                        "component": "action",
                        "elements": [],
                        "properties": {
                            "label": "View Contact",
                            "fontSize": 24,
                            "buttonWidth": "95%",
                            "buttonPadding": "10px",
                            "buttonMargin": "10px",
                            "type": "newTab",
                            "url": "https://app.hubspot.com/contacts/8294123/record/0-1/${workitem.data.hubSpotId}",
                            "onEvent": "onButtonClick",
                            "useProxy": False,
                            "windowName": "Contact",
                            "properties": [],
                            "headers": [],
                            "successVariables": [],
                            "onSuccess": "none",
                            "errorVariables": [],
                            "onError": "none",
                            "hideApplication": False
                        },
                        "_id": "65e8f8326d1b7d9ff73fee3d",
                        "selected": False,
                        "show": True
                    }
                ],
                "properties": {
                    "label": "",
                    "labelAlignment": "left",
                    "labelFontSize": "24",
                    "descriptionAlignment": "left",
                    "descriptionFontSize": "24",
                    "tabLabel": "Main",
                    "alignment": "justify",
                    "canCollapse": False,
                    "state": False,
                    "scroll": False,
                    "showScrollbar": False,
                    "vertical": "full",
                    "direction": "column",
                    "margin": "8px",
                    "panelShadow": False,
                    "showOverlay": False,
                    "showHeader": False,
                    "allowPanelInDashboard": False,
                    "main": True
                },
                "_id": "6568d29611501e41ad52c81d",
                "panelId": "refId1701367439506",
                "selected": False,
                "show": True
            },
            {
                "icon": "icon-ui-panel",
                "name": "Panel",
                "description": "Basic component to display content in a survey",
                "type": "panel",
                "component": "panel",
                "elements": [
                    {
                        "icon": "icon-next-survey",
                        "name": "Move To Survey",
                        "description": "Moves to a different survey",
                        "type": "survey",
                        "component": "survey",
                        "elements": [],
                        "properties": {
                            "label": "SPAA - Payment",
                            "fontSize": 20,
                            "buttonPadding": "8px",
                            "buttonMargin": "8px",
                            "variables": [],
                            "dataVariables": [
                                {
                                    "label": "lastName",
                                    "value": "${surveyInformation.lastName.value}"
                                },
                                {
                                    "label": "email",
                                    "value": "${surveyInformation.email.value}"
                                },
                                {
                                    "label": "phone",
                                    "value": "${surveyInformation.phone.value}"
                                },
                                {
                                    "label": "firstName",
                                    "value": "${surveyInformation.firstName.value}"
                                }
                            ],
                            "surveyId": "65b16a40dcd0f136cfd8c2f6",
                            "expansions": {
                                "surveyId": {
                                    "name": "SPAA - Payment V4"
                                }
                            },
                            "_working": False
                        },
                        "_id": "65c27c53e132a976ad1e2a47",
                        "selected": False,
                        "show": True
                    }
                ],
                "properties": {
                    "label": "SPAA",
                    "labelAlignment": "left",
                    "labelFontSize": "24",
                    "descriptionAlignment": "left",
                    "descriptionFontSize": "24",
                    "tabLabel": "SPAA",
                    "alignment": "justify",
                    "canCollapse": False,
                    "state": False,
                    "scroll": False,
                    "showScrollbar": False,
                    "vertical": "full",
                    "direction": "column",
                    "panelShadow": False,
                    "showOverlay": False,
                    "showHeader": False,
                    "allowPanelInDashboard": False,
                    "main": True
                },
                "_id": "65c27c3abddd7278c9f3adea",
                "panelId": "refId1707244416013",
                "selected": False,
                "show": True
            }
        ],
        "footer": {
            "icon": "icon-ui-footer",
            "name": "Footer",
            "description": "Displays navigation buttons at the bottom of a survey",
            "type": "footer",
            "component": "footer",
            "elements": [],
            "properties": {
                "type": "iconButton",
                "icon": "icon-next",
                "size": "24"
            },
            "_id": "6568d292a5df5f52dc30e84b"
        },
        "header": {
            "icon": "icon-ui-header",
            "name": "Header",
            "description": "Displays navigation buttons at the top of a survey",
            "type": "header",
            "component": "header",
            "elements": [],
            "properties": {
                "showPrevious": False,
                "showOptions": False,
                "icon": "icon-next",
                "showClose": False,
                "size": "24",
                "titleFontSize": "24"
            },
            "_id": "6568d292a4e94559fe3b3a61"
        },
        "overlay": {
            "icon": "icon-ui-panels",
            "name": "Overlay Panel",
            "description": "This panel will always be visible and allow the user to minimise or maxime it.",
            "type": "overlay",
            "component": "overlay",
            "elements": [],
            "properties": {
                "label": "Overlay Panel",
                "labelAlignment": "left",
                "labelFontSize": "24",
                "descriptionAlignment": "left",
                "descriptionFontSize": "24",
                "alignment": "justify",
                "canCollapse": False,
                "state": False,
                "scroll": False,
                "vertical": "full",
                "direction": "column",
                "height": 80
            },
            "_id": "6568d292414caef39be57858"
        }
    },
    "name": "Test HubSpot",
    "width": 700,
    "showTopNavigatorPage": False,
    "usePanelShadow": False,
    "font": "Rubik:400,400i,700;Rubik, sans-serif"
}
zendesk_survey_body = {
    "overlayTitle": "",
    "hideSurveyBoxShadown": False,
    "type": "full",
    "showFooter": False,
    "surveythemeId": "5c6ac608c32fd448ed08038b",
    "showTabs": True,
    "showBottomNavigatorPage": False,
    "height": 700,
    "debug": False,
    "localizations": {
        "name": {
            "en": {
                "language": "en",
                "value": "Test Zendesk"
            }
        }
    },
    "showHeader": False,
    "allowTabinationMandatoryFields": True,
    "entryPanelId": "6643d7aaac0c7120501d5236",
    "layout": {
        "elements": [
            {
                "icon": "icon-survey",
                "name": "Panel",
                "description": "Basic component to display content in a survey",
                "type": "panel",
                "component": "panel",
                "elements": [
                    {
                        "icon": "icon-ui-input",
                        "name": "Input",
                        "description": "A box for the customer to enter information",
                        "type": "input",
                        "component": "input",
                        "elements": [],
                        "properties": {
                            "label": "Name:",
                            "labelInReport": "name",
                            "fontSize": 24,
                            "assistance": "The contact's first and last name, if known.",
                            "width": "",
                            "margin": "10px",
                            "fieldname": "name",
                            "defaultValue": "${workitem.data?.name || \"Not found or unconfirmed\"}",
                            "mandatory": False,
                            "readOnly": False,
                            "validateOnInput": False,
                            "sensitiveData": False,
                            "saveToLocalStorage": False
                        },
                        "_id": "6643da58be3b4842c2254275",
                        "selected": False,
                        "show": True
                    },
                    {
                        "icon": "icon-auto-watchloop",
                        "name": "Action",
                        "description": "Calls APIs and Thrio dispositions",
                        "type": "action",
                        "component": "action",
                        "elements": [],
                        "properties": {
                            "label": "Show Contact",
                            "fontSize": 24,
                            "buttonWidth": "100%",
                            "buttonPadding": "10px",
                            "buttonMargin": "10px",
                            "condition": "workitem.data.contactId != null",
                            "type": "newTab",
                            "url": "https://d3v-phoye.zendesk.com/agent/users/${workitem.data.contactId}/requested_tickets",
                            "onEvent": "onButtonClick",
                            "useProxy": False,
                            "windowName": "Zendesk",
                            "properties": [],
                            "headers": [],
                            "successVariables": [],
                            "errorVariables": [],
                            "hideApplication": False
                        },
                        "_id": "6643df7ba9cf906971e9c961",
                        "selected": False,
                        "show": True
                    }
                ],
                "properties": {
                    "label": "",
                    "labelAlignment": "left",
                    "labelFontSize": "24",
                    "descriptionAlignment": "left",
                    "descriptionFontSize": "24",
                    "tabLabel": "Main",
                    "alignment": "justify",
                    "canCollapse": False,
                    "state": False,
                    "scroll": False,
                    "showScrollbar": False,
                    "vertical": "full",
                    "direction": "column",
                    "panelShadow": False,
                    "showOverlay": False,
                    "showHeader": False,
                    "titleHeader": "",
                    "allowPanelInDashboard": False,
                    "main": True
                },
                "_id": "6643d7aaac0c7120501d5236",
                "panelId": "refId1715697954366",
                "selected": False,
                "show": True
            }
        ],
        "footer": {
            "icon": "icon-ui-footer",
            "name": "Footer",
            "description": "Displays navigation buttons at the bottom of a survey",
            "type": "footer",
            "component": "footer",
            "elements": [],
            "properties": {
                "type": "iconButton",
                "icon": "icon-next",
                "size": "24"
            },
            "_id": "6643d79f79f8b689d794d559"
        },
        "header": {
            "icon": "icon-ui-header",
            "name": "Header",
            "description": "Displays navigation buttons at the top of a survey",
            "type": "header",
            "component": "header",
            "elements": [],
            "properties": {
                "showPrevious": False,
                "showOptions": False,
                "icon": "icon-next",
                "showClose": False,
                "size": "24",
                "titleFontSize": "24"
            },
            "_id": "6643d79f8f20684d04e5249e"
        },
        "overlay": {
            "icon": "icon-ui-panels",
            "name": "Overlay Panel",
            "description": "This panel will always be visible and allow the user to minimise or maxime it.",
            "type": "overlay",
            "component": "overlay",
            "elements": [],
            "properties": {
                "label": "Overlay Panel",
                "labelAlignment": "left",
                "labelFontSize": "24",
                "descriptionAlignment": "left",
                "descriptionFontSize": "24",
                "alignment": "justify",
                "canCollapse": False,
                "state": False,
                "scroll": False,
                "vertical": "full",
                "direction": "column",
                "height": 80
            },
            "_id": "6643d79fed1327b08ac410de"
        }
    },
    "name": "Test Zendesk",
    "width": 380,
    "showTopNavigatorPage": False,
    "usePanelShadow": False,
    "font": "Roboto:400,400i,700;Roboto, sans-serif"
}

# Google Dialogflow
google_dialogflow_parent = "projects/rosy-proposal-446621-a5/agent"

general_intents = [
    {
        "intent": "Test_Get_Hours",
        "training_phrases": [
            {"type": "EXAMPLE", "parts": [{"text": "What are your hours?"}]},
            {"type": "EXAMPLE", "parts": [{"text": "Are you open right now?"}]},
            {"type": "EXAMPLE", "parts": [{"text": "Could you tell me your hours of operation?"}]},
            {"type": "EXAMPLE", "parts": [{"text": "What time does the contact center open and close?"}]},
            {"type": "EXAMPLE", "parts": [{"text": "When are you available to take calls?"}]},
            {"type": "EXAMPLE", "parts": [{"text": "I'd like to know your business hours, please."}]},
            {"type": "EXAMPLE", "parts": [{"text": "Can you let me know what your opening hours are?"}]},
            {"type": "EXAMPLE", "parts": [{"text": "What are your customer service hours?"}]},
            {"type": "EXAMPLE", "parts": [{"text": "Could you provide the hours you're open for assistance?"}]},
            {"type": "EXAMPLE", "parts": [{"text": "I'd like to find out your operating hours."}]},
            {"type": "EXAMPLE", "parts": [{"text": "When is your contact center open for queries?"}]},
            {"type": "EXAMPLE", "parts": [{"text": "Can you tell me what time you're open today?"}]},
            {"type": "EXAMPLE", "parts": [{"text": "Are you open tomorrow before 8?"}]},
            {"type": "EXAMPLE", "parts": [{"text": "Are you open after 5 today?"}]},
            {"type": "EXAMPLE", "parts": [{"text": "Are you open on the weekends?"}]},
        ],
        "action": "FAQ",
        "messages": [
            {
                "text": {
                    "text": [
                        "Normal operating hours are Monday through Friday, 8 AM to 6 PM Eastern Standard Time. We are closed most weekends and holidays. What else can I help you with today?"
                    ]
                }
            }
        ],
        "webhook_state": "WEBHOOK_STATE_ENABLED",
        "end_interaction": False,
    },
    {
        "intent": "Test_Get_Location",
        "training_phrases": [
            {"type": "EXAMPLE", "parts": [{"text": "Can you tell me where the office is located?"}]},
            {"type": "EXAMPLE", "parts": [{"text": "Where is your office situated?"}]},
            {"type": "EXAMPLE", "parts": [{"text": "I'd like to know the address of your office."}]},
            {"type": "EXAMPLE", "parts": [{"text": "Could you provide me with directions to the office?"}]},
            {"type": "EXAMPLE", "parts": [{"text": "What is your office location?"}]},
            {"type": "EXAMPLE", "parts": [{"text": "Is there an office nearby? If so, where?"}]},
            {"type": "EXAMPLE", "parts": [{"text": "Where can I find your office?"}]},
            {"type": "EXAMPLE", "parts": [{"text": "Could you give me the location details for your office?"}]},
            {"type": "EXAMPLE", "parts": [{"text": "I'm trying to visit the office; where is it located?"}]},
            {"type": "EXAMPLE", "parts": [{"text": "Can you give me the office address, please?"}]},
            {"type": "EXAMPLE", "parts": [{"text": "Where are you located?"}]},
            {"type": "EXAMPLE", "parts": [{"text": "Are you near the stadium?"}]},
            {"type": "EXAMPLE", "parts": [{"text": "Is your office located near the freeway?"}]},
            {"type": "EXAMPLE", "parts": [{"text": "What are your major cross streets?"}]},
        ],
        "action": "FAQ",
        "messages": [
            {
                "text": {
                    "text": [
                        "Our national office is located at 9451 East Via de Ventura in Scottsdale, Arizona, 85256. What else can I help you with today?"
                    ]
                }
            }
        ],
        "webhook_state": "WEBHOOK_STATE_ENABLED",
        "end_interaction": False,
    },
    {
        "intent": "Test_Billing_Questions",
        "training_phrases": [
            {"type": "EXAMPLE", "parts": [{"text": "I have a question about a charge on my bill."}]},
            {"type": "EXAMPLE", "parts": [{"text": "Can you help me understand my invoice?"}]},
            {"type": "EXAMPLE", "parts": [{"text": "I'm not sure why this amount is on my bill."}]},
            {"type": "EXAMPLE", "parts": [{"text": "Can you explain this line item on my invoice?"}]},
            {"type": "EXAMPLE", "parts": [{"text": "There appears to be an error on my statement."}]},
            {"type": "EXAMPLE", "parts": [{"text": "I need clarification on a charge I'm seeing."}]},
            {"type": "EXAMPLE", "parts": [{"text": "Could you go over this bill with me?"}]},
            {"type": "EXAMPLE", "parts": [{"text": "This bill seems higher than expected; could you explain why?"}]},
            {"type": "EXAMPLE", "parts": [{"text": "I'm unsure of this charge; can we review it together?"}]},
            {"type": "EXAMPLE", "parts": [{"text": "I think there's a mistake on my invoice, can you check?"}]},
            {"type": "EXAMPLE", "parts": [{"text": "Can you provide more details about the fees listed?"}]},
            {"type": "EXAMPLE", "parts": [{"text": "What's this unfamiliar charge on my bill?"}]},
            {"type": "EXAMPLE", "parts": [{"text": "I need to verify the information on my statement."}]},
            {"type": "EXAMPLE", "parts": [{"text": "Can you help me break down the charges on my invoice?"}]},
            {"type": "EXAMPLE", "parts": [{"text": "I'd like to dispute a charge I see here."}]},
            {"type": "EXAMPLE", "parts": [{"text": "I want to dispute my bill."}]},
            {"type": "EXAMPLE", "parts": [{"text": "You guys sent me a bill, and it isn't right."}]},
        ],
        "action": "ConnectAgent",
        "messages": [
            {
                "text": {
                    "text": [
                        "Please wait while I transfer you to an agent who can assist you with your account."
                    ]
                }
            }
        ],
        "webhook_state": "WEBHOOK_STATE_ENABLED",
        "end_interaction": True,
    },
    {
        "intent": "Test_Get_Account_Balance",
        "training_phrases": [
            {"type": "EXAMPLE", "parts": [{"text": "Could you please tell me my current account balance?"}]},
            {"type": "EXAMPLE", "parts": [{"text": "I would like to check my account balance, please."}]},
            {"type": "EXAMPLE", "parts": [{"text": "Can you provide me with my account balance?"}]},
            {"type": "EXAMPLE", "parts": [{"text": "What is the balance on my account right now?"}]},
            {"type": "EXAMPLE", "parts": [{"text": "Could you let me know how much I have in my account?"}]},
            {"type": "EXAMPLE", "parts": [{"text": "I'm calling to find out my account balance."}]},
            {"type": "EXAMPLE", "parts": [{"text": "I need to verify my account balance."}]},
            {"type": "EXAMPLE", "parts": [{"text": "Can you tell me the amount in my account?"}]},
            {"type": "EXAMPLE", "parts": [{"text": "I’d like to inquire about the balance of my account."}]},
            {"type": "EXAMPLE", "parts": [{"text": "Could you check and tell me my account balance?"}]},
            {"type": "EXAMPLE", "parts": [{"text": "How much do I owe?"}]},
            {"type": "EXAMPLE", "parts": [{"text": "How much do I need to pay to bring my account current?"}]},
            {"type": "EXAMPLE", "parts": [{"text": "What's the past due amount?"}]},
        ],
        "action": "ConnectAgent",
        "messages": [
            {
                "text": {
                    "text": [
                        "Please wait while I transfer you to an agent who can assist you with your account."
                    ]
                }
            }
        ],
        "webhook_state": "WEBHOOK_STATE_ENABLED",
        "end_interaction": True,
    },
    {
        "intent": "Test_Speak_To_Agent",
        "training_phrases": [
            {"type": "EXAMPLE", "parts": [{"text": "I would like to speak to a live agent, please."}]},
            {"type": "EXAMPLE", "parts": [{"text": "Can I talk to a human representative?"}]},
            {"type": "EXAMPLE", "parts": [{"text": "Could you connect me to a customer service agent?"}]},
            {"type": "EXAMPLE", "parts": [{"text": "Please transfer me to a live person."}]},
            {"type": "EXAMPLE", "parts": [{"text": "I need to speak with someone directly."}]},
            {"type": "EXAMPLE", "parts": [{"text": "Is there a representative I can talk to?"}]},
            {"type": "EXAMPLE", "parts": [{"text": "I'd like to discuss this with an actual agent."}]},
            {"type": "EXAMPLE", "parts": [{"text": "Can you put me through to a human, please?"}]},
            {"type": "EXAMPLE", "parts": [{"text": "I prefer to speak to a live customer service representative."}]},
            {"type": "EXAMPLE", "parts": [{"text": "Could you help me get in touch with a real person?"}]},
            {"type": "EXAMPLE", "parts": [{"text": "operator"}]},
            {"type": "EXAMPLE", "parts": [{"text": "agent"}]},
            {"type": "EXAMPLE", "parts": [{"text": "live person"}]},
            {"type": "EXAMPLE", "parts": [{"text": "live human being"}]},
        ],
        "action": "ConnectAgent",
        "messages": [
            {
                "text": {
                    "text": [
                        "Please wait while I transfer you to an agent who can assist you."
                    ]
                }
            }
        ],
        "webhook_state": "WEBHOOK_STATE_ENABLED",
        "end_interaction": True,
    },
]
hc_intents = [
    {
        "intent": "Test_Refill_Prescription",
        "training_phrases": [
            {"type": "EXAMPLE", "parts": [{"text": "I would like to refill my prescription, please."}]},
            {"type": "EXAMPLE", "parts": [{"text": "Could you help me with a prescription refill?"}]},
            {"type": "EXAMPLE", "parts": [{"text": "I'm calling to see if I can get my medication refilled."}]},
            {"type": "EXAMPLE", "parts": [{"text": "I need to request a refill for my prescription."}]},
            {"type": "EXAMPLE", "parts": [{"text": "Can you refill my medication for me?"}]},
            {"type": "EXAMPLE", "parts": [{"text": "I'd like to order a refill of my prescription."}]},
            {"type": "EXAMPLE", "parts": [{"text": "Could you check if I'm eligible for a refill on my medication?"}]},
            {"type": "EXAMPLE", "parts": [{"text": "I would like to arrange a refill for my prescription."}]},
            {"type": "EXAMPLE", "parts": [{"text": "Please refill my prescription at your earliest convenience."}]},
            {"type": "EXAMPLE", "parts": [{"text": "I'd like to ask about getting my prescription refilled."}]},
        ],
        "action": "ConnectAgent",
        "messages": [
            {
                "text": {
                    "text": [
                        "Please wait while I transfer you to an agent who can assist you with a prescription refill."
                    ]
                }
            }
        ],
        "webhook_state": "WEBHOOK_STATE_ENABLED",
        "end_interaction": True,
    },
    {
        "intent": "Test_Schedule_Appointment",
        "training_phrases": [
            {"type": "EXAMPLE", "parts": [{"text": "I would like to schedule an appointment, please."}]},
            {"type": "EXAMPLE", "parts": [{"text": "Can I book a time to see the doctor?"}]},
            {"type": "EXAMPLE", "parts": [{"text": "I'd like to make an appointment for a check-up."}]},
            {"type": "EXAMPLE", "parts": [{"text": "Could you help me arrange a visit with the physician?"}]},
            {"type": "EXAMPLE", "parts": [{"text": "When is the next available slot for an appointment?"}]},
            {"type": "EXAMPLE", "parts": [{"text": "I need to set up a consultation with my provider."}]},
            {"type": "EXAMPLE", "parts": [{"text": "Could I schedule a visit to the clinic?"}]},
            {"type": "EXAMPLE", "parts": [{"text": "I’m calling to arrange an appointment, please."}]},
            {"type": "EXAMPLE", "parts": [{"text": "Is it possible to book an appointment sometime this week?"}]},
            {"type": "EXAMPLE", "parts": [{"text": "I need to see the doctor; could you help me find a time?"}]},
        ],
        "action": "ConnectAgent",
        "messages": [
            {
                "text": {
                    "text": [
                        "Please wait while I transfer you to an agent who can assist you with scheduling an appointment."
                    ]
                }
            }
        ],
        "webhook_state": "WEBHOOK_STATE_ENABLED",
        "end_interaction": True,
    },
    {
        "intent": "Test_Reschedule_Appointment",
        "training_phrases": [
            {"type": "EXAMPLE", "parts": [{"text": "I need to reschedule my appointment."}]},
            {"type": "EXAMPLE", "parts": [{"text": "Is it possible to change the date of my appointment?"}]},
            {"type": "EXAMPLE", "parts": [{"text": "I'd like to move my appointment to another day."}]},
            {"type": "EXAMPLE", "parts": [{"text": "Can we arrange a different time for my appointment?"}]},
            {"type": "EXAMPLE", "parts": [{"text": "Could I please reschedule my appointment?"}]},
            {"type": "EXAMPLE", "parts": [{"text": "I need to postpone my appointment."}]},
            {"type": "EXAMPLE", "parts": [{"text": "May I reschedule my appointment to a later date?"}]},
            {"type": "EXAMPLE", "parts": [{"text": "Would it be possible to shift my appointment to a new time?"}]},
            {"type": "EXAMPLE", "parts": [{"text": "I'm unable to attend my scheduled appointment and need to reschedule."}]},
            {"type": "EXAMPLE", "parts": [{"text": "I have a conflict with my upcoming appointment time; can we reschedule?"}]},
        ],
        "action": "ConnectAgent",
        "messages": [
            {
                "text": {
                    "text": [
                        "Please wait while I transfer you to an agent who can assist you with rescheduling your appointment."
                    ]
                }
            }
        ],
        "webhook_state": "WEBHOOK_STATE_ENABLED",
        "end_interaction": True,
    },
    {
        "intent": "Test_Cancel_Appointment",
        "training_phrases": [
            {"type": "EXAMPLE", "parts": [{"text": "I need to cancel my appointment."}]},
            {"type": "EXAMPLE", "parts": [{"text": "I'd like to cancel my scheduled visit."}]},
            {"type": "EXAMPLE", "parts": [{"text": "Can I please cancel my appointment?"}]},
            {"type": "EXAMPLE", "parts": [{"text": "I'm unable to attend my appointment and need to cancel."}]},
            {"type": "EXAMPLE", "parts": [{"text": "I'd like to cancel my booking"}]},
            {"type": "EXAMPLE", "parts": [{"text": "Can you help me cancel my upcoming appointment?"}]},
            {"type": "EXAMPLE", "parts": [{"text": "I'm calling to cancel my appointment."}]},
            {"type": "EXAMPLE", "parts": [{"text": "I won't be able to make it and need to cancel my appointment."}]},
            {"type": "EXAMPLE", "parts": [{"text": "Please cancel my appointment."}]},
            {"type": "EXAMPLE", "parts": [{"text": "I need to cancel my visit with the doctor."}]},
            {"type": "EXAMPLE", "parts": [{"text": "Due to unforeseen circumstances, I must cancel my appointment."}]},
            {"type": "EXAMPLE", "parts": [{"text": "I'm unable to keep my appointment and would like to cancel."}]},
            {"type": "EXAMPLE", "parts": [{"text": "Could you please cancel my appointment and confirm?"}]},
            {"type": "EXAMPLE", "parts": [{"text": "I'm sorry, but I have to cancel my scheduled appointment."}]},
            {"type": "EXAMPLE", "parts": [{"text": "I would like to cancel my consultation."}]},
        ],
        "action": "ConnectAgent",
        "messages": [
            {
                "text": {
                    "text": [
                        "Please wait while I transfer you to an agent who can assist you with cancelling your appointment."
                    ]
                }
            }
        ],
        "webhook_state": "WEBHOOK_STATE_ENABLED",
        "end_interaction": True,
    },
]
finserv_intents = [
    {
        "intent": "Test_Get_Credit_Card",
        "training_phrases": [
            {"type": "EXAMPLE", "parts": [{"text": "I would like to apply for a credit card."}]},
            {"type": "EXAMPLE", "parts": [{"text": "Can you guide me through the process of applying for a credit card?"}]},
            {"type": "EXAMPLE", "parts": [{"text": "I'm interested in opening a new credit card account."}]},
            {"type": "EXAMPLE", "parts": [{"text": "Could you please send me the application form for a credit card?"}]},
            {"type": "EXAMPLE", "parts": [{"text": "I am considering applying for a credit card with your institution."}]},
            {"type": "EXAMPLE", "parts": [{"text": "What are the requirements for applying for a credit card?"}]},
            {"type": "EXAMPLE", "parts": [{"text": "Could you provide me with information on your credit card options?"}]},
            {"type": "EXAMPLE", "parts": [{"text": "I am looking to get a credit card and would like to know how to proceed."}]},
            {"type": "EXAMPLE", "parts": [{"text": "Is there an online application available for a credit card?"}]},
            {"type": "EXAMPLE", "parts": [{"text": "Can you assist me with initiating an application for a credit card?"}]},
        ],
        "action": "ConnectAgent",
        "messages": [
            {
                "text": {
                    "text": [
                        "Please wait while I transfer you to an agent who can assist you with a credit card application."
                    ]
                }
            }
        ],
        "webhook_state": "WEBHOOK_STATE_ENABLED",
        "end_interaction": True,
    },
    {
        "intent": "Test_Get_Loan",
        "training_phrases": [
            {"type": "EXAMPLE", "parts": [{"text": "I would like to inquire about applying for a loan."}]},
            {"type": "EXAMPLE", "parts": [{"text": "Could you provide information on how to start a loan application?"}]},
            {"type": "EXAMPLE", "parts": [{"text": "I'm interested in applying for a loan with the credit union."}]},
            {"type": "EXAMPLE", "parts": [{"text": "Can you guide me through the process of getting a loan?"}]},
            {"type": "EXAMPLE", "parts": [{"text": "I'd like to discuss the steps involved in applying for a loan."}]},
            {"type": "EXAMPLE", "parts": [{"text": "Could you help me understand the loan application requirements?"}]},
            {"type": "EXAMPLE", "parts": [{"text": "I am considering taking out a loan, can you assist me with the application?"}]},
            {"type": "EXAMPLE", "parts": [{"text": "What are the options available for loan applications?"}]},
            {"type": "EXAMPLE", "parts": [{"text": "How do I begin the application process for a loan?"}]},
            {"type": "EXAMPLE", "parts": [{"text": "I need to apply for a loan; what are the first steps?"}]},
        ],
        "action": "ConnectAgent",
        "messages": [
            {
                "text": {
                    "text": [
                        "Please wait while I transfer you to an agent who can assist you with a loan application."
                    ]
                }
            }
        ],
        "webhook_state": "WEBHOOK_STATE_ENABLED",
        "end_interaction": True,
    },
    {
        "intent": "Test_Open_Account",
        "training_phrases": [
            {"type": "EXAMPLE", "parts": [{"text": "I'd like to open a new checking account, please."}]},
            {"type": "EXAMPLE", "parts": [{"text": "Can you help me set up a savings account?"}]},
            {"type": "EXAMPLE", "parts": [{"text": "I'm interested in opening a new checking account."}]},
            {"type": "EXAMPLE", "parts": [{"text": "Could you guide me on how to open a savings account here?"}]},
            {"type": "EXAMPLE", "parts": [{"text": "I'd like to discuss opening a checking account."}]},
            {"type": "EXAMPLE", "parts": [{"text": "What are the steps to open a new savings account with your credit union?"}]},
            {"type": "EXAMPLE", "parts": [{"text": "I need assistance with opening a checking account."}]},
            {"type": "EXAMPLE", "parts": [{"text": "Could you provide information on your savings account options?"}]},
            {"type": "EXAMPLE", "parts": [{"text": "I'm looking to start a new checking account, can you help?"}]},
            {"type": "EXAMPLE", "parts": [{"text": "I'd like to open a savings account, what do I need to do?"}]},
        ],
        "action": "ConnectAgent",
        "messages": [
            {
                "text": {
                    "text": [
                        "Please wait while I transfer you to an agent who can assist you with opening a new account."
                    ]
                }
            }
        ],
        "webhook_state": "WEBHOOK_STATE_ENABLED",
        "end_interaction": True,
    },
    {
        "intent": "Test_Close_Account",
        "training_phrases": [
            {"type": "EXAMPLE", "parts": [{"text": "I would like to close my checking account, please."}]},
            {"type": "EXAMPLE", "parts": [{"text": "I would like to close my savings account, please."}]},
            {"type": "EXAMPLE", "parts": [{"text": "Can you assist me with closing my account?"}]},
            {"type": "EXAMPLE", "parts": [{"text": "I need to close my bank account; what are the steps to do so?"}]},
            {"type": "EXAMPLE", "parts": [{"text": "Could you provide information on how to close my checking account?"}]},
            {"type": "EXAMPLE", "parts": [{"text": "Could you provide information on how to close my savings account?"}]},
            {"type": "EXAMPLE", "parts": [{"text": "I am considering closing my account and would like to start the process."}]},
            {"type": "EXAMPLE", "parts": [{"text": "Please initiate the closure of my checking account."}]},
            {"type": "EXAMPLE", "parts": [{"text": "Please initiate the closure of my savings account."}]},
            {"type": "EXAMPLE", "parts": [{"text": "I'm contacting you to terminate my account."}]},
            {"type": "EXAMPLE", "parts": [{"text": "I’d like to cancel my account."}]},
            {"type": "EXAMPLE", "parts": [{"text": "I am planning to close my account and would appreciate your help with this."}]},
            {"type": "EXAMPLE", "parts": [{"text": "Could you guide me through the account closure process?"}]},
        ],
        "action": "ConnectAgent",
        "messages": [
            {
                "text": {
                    "text": [
                        "Please wait while I transfer you to an agent who can assist you with closing your account."
                    ]
                }
            }
        ],
        "webhook_state": "WEBHOOK_STATE_ENABLED",
        "end_interaction": True,
    },
]
