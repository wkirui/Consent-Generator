import streamlit as st
import json

st.image("static/ipa.png")

session_state = st.session_state

# load existing information
def load_project_info(filename):
    try:
        with open(filename) as fr:
            session_state = json.load(fr)
    except  Exception as e:
        st.write(e)
    return session_state



# save submission to file
def save_to_file(file_name,project_data):
    try:
        with open(file_name, 'w') as fr:
            fr.write(json.dumps(project_data))
            fr.close()
    except Exception as e:
        pass

def risks_benefits_page(session_state):
    st.title("Potential Risks And Anticipated Benefits")
    st.write("")

    risks_and_benefits = {}
    yes_no_choices = ["No","Yes",""]
    
    risks_benefits_fields = ["participants_compensated","participants_compensation","other_procedures_compensation",
                             "study_has_direct_benefits", "study_direct_benefits", "other_procedures_compensation",
                             "indirect_community_benefit", "sensitive_questions", "greater_than_minimal_risk",
                             "mandated_reporter_requirements", "access_to_participant_information",
                             "focus_group_discussions","has_co_data_protection_language", "co_data_protection_language",
                             "share_deidentified_data_only", "share_identifiable_information"
                             ]
    
    for field in risks_benefits_fields:
        if field not in session_state:
            session_state[field] = ""
    
    participants_compensated = st.selectbox("Will participants be paid or given anything to take part in this study?",
                                            yes_no_choices,
                                            index=yes_no_choices.index(session_state["participants_compensated"]))
    session_state["participants_compensated"] = participants_compensated
    if participants_compensated == "Yes":
        participants_compensation = st.text_area("Describe compensation, including amount & method of delivery, e.g., mobile money",
                                                value= session_state["participants_compensation"])
        session_state["participants_compensation"] = participants_compensation
        other_procedures_compensation = st.selectbox("Will the participants be compensated for any other procedures?",
                                                     yes_no_choices,
                                                     index=yes_no_choices.index(session_state["other_procedures_compensation"]))
        session_state["other_procedures_compensation"] = other_procedures_compensation
          
    study_has_direct_benefits = st.selectbox("Are there any benefits for participating in this study?",yes_no_choices,
                                  index=yes_no_choices.index(session_state["study_has_direct_benefits"]))
    session_state["study_has_direct_benefits"] = study_has_direct_benefits
    if study_has_direct_benefits == "Yes":
        study_direct_benefits = st.text_area("State how participants might benefit e.g., \
            if participants may receive information via SMS on farming best practices",
            value=session_state["study_direct_benefits"])
        session_state["study_direct_benefits"] = study_direct_benefits        
    elif study_has_direct_benefits == "No":
        indirect_community_benefit = st.text_area("Note a community that may benefit from the research in the long run e.g., at-risk youth in xyz city",
                                                  value=session_state["indirect_community_benefit"])
        session_state["indirect_community_benefit"] = indirect_community_benefit    
   
    sensitive_questions = st.selectbox("Does the study contain sensitive questions?",yes_no_choices,
                                       index=yes_no_choices.index(session_state["sensitive_questions"]))
    session_state["sensitive_questions"] = sensitive_questions
    
    greater_than_minimal_risk = st.selectbox("Is this a greater than minimal risk research study?", yes_no_choices,
                                       index=yes_no_choices.index(session_state["greater_than_minimal_risk"]))
    session_state["greater_than_minimal_risk"] = greater_than_minimal_risk
    mandated_reporter_requirements = st.selectbox("Are there any mandated reporter requirements and this research study may result in information that you are mandated to report?",
                                                  yes_no_choices,
                                                  yes_no_choices.index(session_state["mandated_reporter_requirements"]))
    session_state["mandated_reporter_requirements"] = mandated_reporter_requirements
    
    access_to_participant_information = st.text_area("Besides the research team, individuals from which organization will have access to participant's information? - IPA/other non-IPA organization",
                                                     value=session_state["access_to_participant_information"])
    session_state["access_to_participant_information"] = access_to_participant_information
    focus_group_discussions = st.selectbox("Does this study involve Focus Group Discussion?",yes_no_choices,
                                       index=yes_no_choices.index(session_state["focus_group_discussions"]))
    session_state["focus_group_discussions"] = focus_group_discussions
    has_co_data_protection_language = st.selectbox("Does the study have a country-specific data protection language?",
                                               yes_no_choices, yes_no_choices.index(session_state["has_co_data_protection_language"]))
    session_state["has_co_data_protection_language"] = has_co_data_protection_language
    if has_co_data_protection_language == "Yes":
        co_data_protection_language = st.text_area("Enter the country-specific data protection language:",
                                                   value=session_state["co_data_protection_language"])
        session_state["co_data_protection_language"] = co_data_protection_language
    share_deidentified_data_only = st.selectbox("Do you plan to share de-identified data only?",
                                                yes_no_choices, 
                                                index = yes_no_choices.index(session_state["share_deidentified_data_only"])) 
    session_state["share_deidentified_data_only"] = share_deidentified_data_only
    share_identifiable_information = st.selectbox("Do you plan to share identifiable research information for other future research studies?",
                                                  yes_no_choices, 
                                                  index=yes_no_choices.index(session_state["share_identifiable_information"]))
    session_state["share_identifiable_information"] = share_identifiable_information
     
    # serialize session state values
    session_vals = [x for x in session_state.values()]
    session_keys = [x for x in session_state.keys()]
    research_study_values = dict(zip(session_keys,session_vals))

    return research_study_values   


# save anticipated risks and benefits details
filename = "data/input/submitted_project_details.txt"
# session_state = load_project_info(filename)

risks_and_benefits = risks_benefits_page(session_state)
save_to_file(filename,risks_and_benefits)

col1, col2,col3,col4 = st.columns(4)
with col1:
    if st.button(":red[Back]"):
        save_to_file(filename,risks_and_benefits)
        st.switch_page("pages/2_Research_Procedures.py")
with col4:
    if st.button(":green[Next]"):
        save_to_file(filename,risks_and_benefits)
        st.switch_page("pages/4_Contact_Details.py")
