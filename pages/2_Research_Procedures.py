import streamlit as st
import json
import pandas as pd
from io import StringIO
st.image("static/ipa.png")

session_state = st.session_state

# save submission to file
def save_to_file(file_name,project_data):
    try:
        with open(file_name, 'w') as fr:
            fr.write(json.dumps(project_data))
            fr.close()
    except Exception as e:
        pass
    
def load_project_info(filename):
    try:
        with open(filename) as fr:
            session_state = json.load(fr)
    except  Exception as e:
        st.write(e)
    return session_state

def study_procedures_page(session_state):
    st.title("Study Procedures")
    st.write("")

    study_procedures_list = {}
    
    yes_no_choices = ["No","Yes",""] # define choices for indexing
    study_procedures_choices = ["Single Study Procedure",
                                "Multiple Study Procedures (for example, a survey AND a focus group)",""]
    audio_or_video = ["audio","video",""]
    all_or_parts_choices = ["All","Parts",""]

    
    study_procedures_fields = ["data_collection_procedure","research_topics_covered", "has_randomization_or_intervention",
                               "share_randomization_design","randomization_design", "study_procedures","other_study_procedures",
                               "other_study_procedures_topics","followup_data_collection","number_of_returns_known",
                               "num_future_data_collections","future_data_collection_timeframe","audio_or_video_used",
                               "study_participation","photograph_participants","gps_collected","gps_purpose",
                               "gps_photos_recordings_required","anthropometric_measurements", "anthropometric_measure",
                               "biospecimen_and_biometric_data","biospecimen_and_biometric_mandatory","biospecimen_collected",
                               "biospecimen_collection_method","participants_given_health_information", "biospecimen_mandatory",
                               "physical_samples_collected", "biometric_physical_discomfort","what_will_be_photographed",
                               "photography_purpose","share_photos_publicly", "audio_or_video_recorded", "all_or_parts_recorded",
                               "audio_or_video_purpose","photo_subjects_anonymity"
                               ]
    
    for field in study_procedures_fields:
        if field not in session_state:
            session_state[field] = ""
    
    data_collection_procedure = st.text_area("Describe the data collection procedure e.g., complete a survey, participate in a focus group",
                                             value=session_state['data_collection_procedure'])
    session_state["data_collection_procedure"] = data_collection_procedure
    research_topics_covered = st.text_area("Describe topics to be covered e.g., household information, \
        education, savings behaviors, any sensitive topics, etc.",
        value=session_state["research_topics_covered"])
    session_state["research_topics_covered"] = research_topics_covered
    
    has_randomization_or_intervention = st.selectbox("Does this study involve randomization, intervention etc.?", yes_no_choices,
                                index = yes_no_choices.index(session_state['has_randomization_or_intervention']))
    session_state["has_randomization_or_intervention"] = has_randomization_or_intervention
    if has_randomization_or_intervention == "Yes":
        share_randomization_design = st.selectbox("Do you want to explicitly share your randomization design?",
                                                  yes_no_choices,
                                                  index=yes_no_choices.index(session_state["share_randomization_design"]))
        session_state["share_randomization_design"] = share_randomization_design
        if share_randomization_design == "Yes":
            randomization_design = st.text_area("Describe possible intervention(s) e.g., be invited to participate in a training, receive SMS messages about xyz",
                                                value=session_state["randomization_design"])
            session_state["randomization_design"] = randomization_design
            study_procedures_list = study_procedures_list | {"randomization_design": randomization_design} 
    
    
    study_procedures = st.selectbox("Does this study involve single or multiple study procedures?",
                                    study_procedures_choices,
                                    index= study_procedures_choices.index(
                                        session_state["study_procedures"]))
    session_state ["study_procedures"] = study_procedures
   
    if study_procedures == "Multiple Study Procedures (for example, a survey AND a focus group)":
        other_study_procedures = st.text_area("Describe other data collection procedures, including duration.",
                                              value=session_state["other_study_procedures"])
        session_state["other_study_procedures"] = other_study_procedures
        
        other_study_procedures_topics  = st.text_area("Describe the topics to be covered",
                                                         value=session_state["other_study_procedures_topics"])
        session_state["other_study_procedures_topics"] = other_study_procedures_topics
        study_procedures_list = study_procedures_list | {"other_study_procedures" : other_study_procedures,
                                                         "other_study_procedures_topics": other_study_procedures_topics}
         

    study_participation = st.selectbox("Does the study require participation by the same sub-group of participants in more than one study procedure? \
                                        (ex. survey and a focus group and an in-depth interview as part of the study)",
                                        yes_no_choices,
                                        index=yes_no_choices.index(session_state['study_participation']))
    session_state["study_participation"] = study_participation
   
    followup_data_collection = st.selectbox("Will this study involve follow-up data collection?",
                                            yes_no_choices,
                                            index=yes_no_choices.index(session_state['followup_data_collection']))
    session_state["followup_data_collection"] = followup_data_collection
    
    if followup_data_collection == "Yes":
        number_of_returns_known = st.selectbox("Do you know how many times you expect to return?",
                                              yes_no_choices,
                                              index=yes_no_choices.index(session_state['number_of_returns_known']))
        session_state["number_of_returns_known"] = number_of_returns_known
        
        if number_of_returns_known == "Yes":
            num_future_data_collections = st.text_input("Enter the number of times",
                                                        value=session_state["num_future_data_collections"])
            session_state["num_future_data_collections"] = num_future_data_collections
            future_data_collection_timeframe = st.text_input("What is the total timeframe for the follow-up data collections?",
                                                             value=session_state["future_data_collection_timeframe"])
            session_state["future_data_collection_timeframe"] = future_data_collection_timeframe
            

    audio_or_video_used = st.selectbox("Is audio/video recordings going to be used?",yes_no_choices,
                                       index=yes_no_choices.index(session_state['audio_or_video_used']))
    session_state["audio_or_video_used"] = audio_or_video_used

    if audio_or_video_used == "Yes":
        audio_or_video_recorded = st.selectbox("What will be recorded?",audio_or_video,
                                                index=audio_or_video.index(session_state["audio_or_video_recorded"]))
        session_state["audio_or_video_recorded"] = audio_or_video_recorded
        all_or_parts_recorded = st.selectbox("Will you record parts or all of the survey, interviews, etc?",
                                              all_or_parts_choices,
                                              index = all_or_parts_choices.index(session_state["all_or_parts_recorded"]))
        session_state["all_or_parts_recorded"] = all_or_parts_recorded
        audio_or_video_purpose = st.text_area("Specify purpose of the audio or the video recorded e.g., to help us validate the quality of the data collected, for further analysis, etc.",
                                              value=session_state["audio_or_video_purpose"])
        session_state["audio_or_video_purpose"] = audio_or_video_purpose

    photograph_participants = st.selectbox("Will you photograph the participants?",yes_no_choices,
                                    index=yes_no_choices.index(session_state['photograph_participants']))
    session_state["photograph_participants"] = photograph_participants
    if photograph_participants == "Yes":
        what_will_be_photographed = st.text_area("Specify what will be photographed. Be as specific as possible",
                                                 value=session_state["what_will_be_photographed"])
        session_state["what_will_be_photographed"] = what_will_be_photographed
        photography_purpose = st.text_area("Specify purpose of the photographs e.g., to allow us to analyze xyz",
                                             value=session_state["photography_purpose"])
        session_state["photography_purpose"] = photography_purpose
        share_photos_publicly = st.selectbox("Do you plan to share photos? e.g. publicly in presentations, publications, etc.",
                                             yes_no_choices,
                                             index=yes_no_choices.index(session_state["share_photos_publicly"]))
        session_state["share_photos_publicly"] = share_photos_publicly
        if share_photos_publicly == "Yes":
            photo_subjects_anonymity = st.text_area("Explain any steps you will take to preserve anonymity for \
                photo subjects if photos will be used publicly, e.g., photographing from behind.",
                value=session_state["photo_subjects_anonymity"])
            session_state["photo_subjects_anonymity"] = photo_subjects_anonymity
                

        
    gps_collected = st.selectbox("Is GPS location data going to be collected?",yes_no_choices,
                                 index=yes_no_choices.index(session_state['gps_collected']))
    session_state["gps_collected"] = gps_collected
    if gps_collected == "Yes":
        gps_purpose = st.text_area("What is the purpose of the GPS collected?",
                                   value=session_state["gps_purpose"])
        session_state["gps_purpose"] = gps_purpose
    
    gps_photos_recordings_required = st.selectbox("Are audio recording/video recording/GPS data collection/photography mandatory?", 
                                                      yes_no_choices,
                                                      index=yes_no_choices.index(session_state["gps_photos_recordings_required"]))
    session_state["gps_photos_recordings_required"] = gps_photos_recordings_required
    
    anthropometric_measurements = st.selectbox("Does this data collection involve anthropometric measurements such as height, weight, etc.?",
                                               yes_no_choices,
                                               index = yes_no_choices.index(session_state["anthropometric_measurements"]))
    session_state["anthropometric_measurements"] = anthropometric_measurements
    if anthropometric_measurements == "Yes":
        anthropometric_measure = st.text_input("What is the anthropometric measurement to be collected?",
                                               value=session_state["anthropometric_measurements"])
        session_state["anthropometric_measure"] = anthropometric_measure
    biospecimen_and_biometric_data = st.selectbox("Does this data collection involve biospecimen and other biometric data collection?",
                                                  yes_no_choices,
                                                  index=yes_no_choices.index(session_state["biospecimen_and_biometric_data"]))
    session_state["biospecimen_and_biometric_data"] = biospecimen_and_biometric_data
    
    if biospecimen_and_biometric_data == "Yes":
        biospecimen_collected = st.text_area("What will be collected/measured? e.g. heart rate/blood pressure/stress levels/etc.",
                                             value=session_state["biospecimen_collected"])
        session_state["biospecimen_collected"] = biospecimen_collected
        biospecimen_collection_method = st.text_area("Explain how the biospecimen or biometric data will be colllected \
            e.g., put a cuff on your arm to take your blood pressure, prick your finger to collect a single drop of blood, etc.",
            value=session_state["biospecimen_collection_method"])
        session_state["biospecimen_collection_method"] = biospecimen_collection_method
        participants_given_health_information = st.text_area("Explain if participants will be informed of any relevant health information, e.g., high blood pressure.",
                                                       value=session_state["participants_given_health_information"])
        session_state["participants_given_health_information"] = participants_given_health_information
        biospecimen_mandatory = st.selectbox("Is biospecimen/biometric data collection mandatory?",
                                                        yes_no_choices,
                                                        index=yes_no_choices.index(session_state["biospecimen_mandatory"]))
        session_state["biospecimen_mandatory"] = biospecimen_mandatory
        physical_samples_collected = st.selectbox("Will you be collecting physical samples for biospecimen/bio data?",
                                                  yes_no_choices,
                                                  index=yes_no_choices.index(session_state["physical_samples_collected"]))
        session_state["physical_samples_collected"] = physical_samples_collected
        biometric_physical_discomfort = st.text_area("List any physical discomforts that might result from biometric data collection",
                                                     value=session_state["biometric_physical_discomfort"])
        session_state["biometric_physical_discomfort"] = biometric_physical_discomfort
        
    biospecimen_and_biometric_mandatory = st.selectbox("Is the collection/measurement of biospecimen/biometric data mandatory?",
                                                       yes_no_choices,
                                                       index = yes_no_choices.index(session_state["biospecimen_and_biometric_mandatory"]))
    session_state["biospecimen_and_biometric_mandatory"] = biospecimen_and_biometric_mandatory
          
    # serialize session state values
    session_vals = [x for x in session_state.values()]
    session_keys = [x for x in session_state.keys()]
    research_study_values = dict(zip(session_keys,session_vals))

    return research_study_values   

# submit study procedures
filename = "data/input/submitted_project_details.txt"
# session_state = load_project_info(filename)
study_procedures_list = study_procedures_page(session_state)
save_to_file(filename, study_procedures_list)
col1, col2,col3,col4 = st.columns(4)
with col1:
    if st.button(":red[Back]"):
        save_to_file(filename,study_procedures_list)
        st.switch_page("pages/1_General_Information.py")
with col4:
    if st.button(":green[Next]"):
        save_to_file(filename,study_procedures_list)
        st.switch_page("pages/3_Risks_And_Benefits.py")
    