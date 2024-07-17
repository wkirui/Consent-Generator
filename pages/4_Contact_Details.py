import streamlit as st
import json

st.image("static/ipa.png")
session_state = st.session_state

# load  existing details
def load_project_info(filename):
    try:
        with open(filename) as fr:
            existing_project_details = json.load(fr)
    except  Exception as e:
        st.write(e)
    return existing_project_details

# save to file
def save_to_file(file_name,project_data):
    try:
        with open(file_name,"w") as fr:
            fr.write(json.dumps(project_data))
            fr.close()
    except Exception as e:
        pass
    
def contact_information_page(session_state):
    st.title("Contact Information")
    st.write("")
    yes_no_choices = ["No","Yes",""]
    contact_details = {}
    
    contact_details_fields = ["research_associate", "other_or_local_irb_exists",
                              "other_or_local_irb_contacts"]
    for field in contact_details_fields:
        if field not in session_state:
            session_state[field] = ""   
        
    research_associate = st.text_area("Enter the name of the Research Associate/other responsible project personne, \
        their title e.g. Research Associciate and their local phone number",
        value=session_state["research_associate"])
    st.session_state["research_associate"] = research_associate
    
    other_or_local_irb_exists = st.selectbox("Do you have contact information of another/local IRB?",
                                           yes_no_choices,
                                           index=yes_no_choices.index(session_state["other_or_local_irb_exists"]))
    st.session_state["other_or_local_irb_exists"] = other_or_local_irb_exists
    if other_or_local_irb_exists == "Yes":
        other_or_local_irb_contacts = st.text_area("Enter the name of the other/local IRB and their Email/Phone number",
                                                   value = session_state["other_or_local_irb_contacts"])
        st.session_state["other_or_local_irb_contacts"] = other_or_local_irb_contacts
                                    
     # serialize session state values
    session_vals = [x for x in session_state.values()]
    session_keys = [x for x in session_state.keys()]
    research_study_values = dict(zip(session_keys,session_vals))

    return research_study_values   



# submit contact information
filename = "data/input/submitted_project_details.txt"
# existing_project_details = load_project_info(filename)
contact_details = contact_information_page(session_state)
col1, col2,col3,col4 = st.columns(4)
with col1:
    if st.button(":red[Back]"):
        save_to_file(filename,contact_details)
        st.switch_page("pages/3_Risks_And_Benefits.py")
with col4:
    if st.button(":green[Next]"):
        save_to_file(filename,contact_details)
        st.switch_page("pages/5_Generate_Consent.py")
