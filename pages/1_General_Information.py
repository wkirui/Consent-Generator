import streamlit as st
import json
import os

st.image("static/ipa.png")

session_state = st.session_state

# check if we have saved file  
def check_file_exists(filename,session_state):
    file_exists = os.path.isfile(filename)
    if file_exists == False:
        with open(filename,'w') as fw:
            fw.write(json.dumps(session_state))
            fw.close()

def load_project_info(filename):
    try:
        with open(filename) as fr:
            existing_project_details = json.load(fr)
    except  Exception as e:
        pass
    return existing_project_details


# save submission to file
def save_to_file(filename,project_data):
    try:
        with open(filename,"w") as fr:
            fr.write(json.dumps(project_data))
            fr.close()
    except Exception as e:
        pass
def project_details_page(session_state):
    st.title("General Study Information")
    st.write("")

    project_details = {}
    yes_no_choices = ["No","Yes",""]
    consent_mode = ["Enumerator","Self-Administered",""]
    study_participants = ['An Adult','A child','A parent and a child','']
    survey_type_choices = ["Survey", "Interview","Other procedure",""]

    study_details_fields = ["research_title", "principal_investigators", "ipa_research_study",
                            "ipa_project_id_number", "data_collection_firm", "data_collection_firm_function",
                            "how_consent_is_administered", "study_participant","funding_organization",
                            "study_purpose", "eligibility_criteria","study_examples", "research_hypothesis",
                            "research_impact", "participation_duration", "survey_type","participants_are_employees",
                            "participants_employer", "research_team_can_terminate_participation",
                            "reasons_for_participation_termination",
                            ]
    for field in study_details_fields:
        if field not in st.session_state:
            st.session_state[field] = ""
            
    research_title = st.text_area(label="Title of the Research Study",value=session_state["research_title"])
    session_state["research_title"] = research_title
    principal_investigators = st.text_input("Name(s) of the Principal Ivestigator(s)",
                                            value=session_state["principal_investigators"])
    session_state["principal_investigators"] = principal_investigators
        
    ipa_research_study = st.selectbox("Is this an IPA research study?",yes_no_choices,
                                      index=yes_no_choices.index(session_state['ipa_research_study']))
    session_state["ipa_research_study"] = ipa_research_study
    if ipa_research_study == "Yes":
        ipa_project_id_number = st.text_input("Enter the 5-Digit IPA Project ID number",
                                       value=session_state["ipa_project_id_number"])
        session_state["ipa_project_id_number"] = ipa_project_id_number
        
    elif ipa_research_study == "No":
        data_collection_firm = st.text_input("Enter the name of the data collection firm",
                                            value=session_state['data_collection_firm'])
        session_state["data_collection_firm"] = data_collection_firm
        data_collection_firm_function = st.text_area("What does the data collection firm do?",
                                            value=session_state['data_collection_firm_function'])
        session_state["data_collection_firm_function"] = data_collection_firm_function
           
    how_consent_is_administered = st.selectbox("Who will administer the consent?",
                                               consent_mode,
                                               index=consent_mode.index(session_state['how_consent_is_administered']))
    session_state["how_consent_is_administered"] = how_consent_is_administered
    study_participant = st.selectbox("Who are the participants in the study for which you're seeking consent?",
                                     study_participants,
                                     index=study_participants.index(session_state['study_participant']))
    session_state["study_participant"] = study_participant
        
    funding_organization = st.text_input("Name of the funding agency/organisation or other institution commissioning the research",
                                         value=session_state["funding_organization"])
    session_state["funding_organization"] = funding_organization
    
    study_purpose = st.text_area("Summary of the overall purpose of the study in lay language",
                                 value=session_state["study_purpose"])
    session_state["study_purpose"] = study_purpose
    eligibility_criteria = st.text_input("Eligibility/screening/inclusion criteria",
                                         value=session_state["eligibility_criteria"])
    session_state["eligibility_criteria"] = eligibility_criteria
    study_examples = st.text_area("Study specific examples",
                                  value=session_state["study_examples"])
    session_state["study_examples"] = study_examples
    research_hypothesis = st.text_area("Specific research aim/hypothesis",value=session_state["research_hypothesis"])
    session_state["research_hypothesis"] = research_hypothesis
    research_impact = st.text_area("How will the research impact public good",value=session_state["research_impact"])
    session_state["research_impact"] = research_impact
    participation_duration = st.text_input("What is the total time expected in participation in minutes/hours? e.g 1.5 hours",
                                           value=session_state["participation_duration"])
    session_state["participation_duration"] = participation_duration
    survey_type = st.selectbox("Is this a survey, interview or other procedure?",
                                survey_type_choices,
                                index=survey_type_choices.index(session_state['survey_type']))
    session_state["survey_type"] = survey_type
    
    participants_are_employees = st.selectbox("Are the participants employees at a firm, teachers at a school, etc.?",
                                              yes_no_choices,
                                              index= yes_no_choices.index(session_state["participants_are_employees"]))
    session_state["participants_are_employees"] = participants_are_employees
    
    if participants_are_employees == "Yes":
        participants_employer = st.text_input("Enter the name of the employer",
                                              value=session_state["participants_employer"])
        session_state["participants_employer"] = participants_employer
        
    research_team_can_terminate_participation = st.selectbox("Are there any circumstances where the research \
        team would terminate a subject's participation?", yes_no_choices,
        index = yes_no_choices.index(session_state["research_team_can_terminate_participation"]))
    session_state["research_team_can_terminate_participation"] = research_team_can_terminate_participation
    
    if research_team_can_terminate_participation == "Yes":
        reasons_for_participation_termination = st.text_area("Describe the circumstances where a PI would terminate a subject's \
            participation in the research",
            value= session_state["reasons_for_participation_termination"])
        session_state["reasons_for_participation_termination"] = reasons_for_participation_termination
        
    # serialize session state values
    session_vals = [x for x in session_state.values()]
    session_keys = [x for x in session_state.keys()]
    research_study_values = dict(zip(session_keys,session_vals))


    return research_study_values   


# project details file
filename = "data/input/submitted_project_details.txt"
project_details = project_details_page(session_state)
st.write(project_details)
save_to_file(filename,project_details)

col1, col2,col3,col4 = st.columns(4)
with col1:
    if st.button(":red[Back]"):
        save_to_file(filename,project_details)
        st.switch_page("Home.py")
with col4:
    if st.button(":green[Next]"):
        save_to_file(filename,project_details)
        st.switch_page("pages/2_Research_Procedures.py")



