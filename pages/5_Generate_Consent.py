import os
import base64
import streamlit as st
import json
import markdown
import time
from streamlit_pdf_viewer import pdf_viewer
from openai import OpenAI
from markdown_pdf import MarkdownPdf, Section
from Markdown2docx import Markdown2docx


st.image("static/ipa.png")
st.write("")

# define session state
session_state = st.session_state

# save content to file                      
def save_to_file(filename, content):
    with open(filename,'w') as fw:
        fw.writelines(content)
        fw.close()

    
# create openAI client API
organization = st.secrets["ORGANIZATION"]
project = st.secrets["PROJECT"]
api_key = st.secrets["API_KEY"]

client = OpenAI(
    organization = organization,
    project = project,
    api_key = api_key)


system_message = "You are a draft document generator AI assistant that takes in json text and images \
    and generates a research study consent template draft document using the format provided. \
    The draft should be formatted for downloading into a word document. \
    The draft should be logical and exclude sections that are not required based on \
    the data provided.\
    For example if there is no GPS or Photography used in the study, \
    the sections for GPS and photography should be removed from the output. \
    If the study doesn't have mutliple study procedures, the draft should not \
    have the multiple study procedures table."
        
user_message = "Use the data and image templates provided to generate a research study consent draft. \
    The values and text of the draft output should come from the given text data and image templates and \
    follow the format in the images provided. \
    Instructional or optional text for example those in brackets that do not apply, \
    should be removed from the final draft.\
    Formatting should match the provided templates."
        
# encode images to base64
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')


base64_image0 = encode_image("templates/page0.png")
base64_image1 = encode_image("templates/page1.png")
base64_image2 = encode_image("templates/page2.png")
base64_image3 = encode_image("templates/page3.png")
base64_image4 = encode_image("templates/page4.png")
base64_image5 = encode_image("templates/page5.png")
base64_image6 = encode_image("templates/page6.png")
base64_image7 = encode_image("templates/page7.png")
base64_image8 = encode_image("templates/page8.png")
base64_image9 = encode_image("templates/page9.png")


# to preview pdf
@st.experimental_dialog("Consent Template Draft", width="large")
def displayPDF(pdf_file, docx_file):
    
    # Opening file from file path
    with open(docx_file, "rb") as f:
        pdf_doc = f.read()

    with st.container(height=700):
        pdf_viewer_content = pdf_viewer(pdf_file,rendering="unwrap",width=700,height=700)
        
        col1, col2,col3,col4 = st.columns(4)
        with col3:
            st.download_button(":green[Download]", data=pdf_doc,
                               file_name="consent_draft.docx", mime="text/plain")


def generate_consent_draft(client,system_message, user_message,submitted_study_data):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role":'system',
             "content":[
                 {"type":"text","text":system_message} 
                 ]
             },
            {
                "role":"user",
                "content": [
                    {"type":"text","text":user_message},
                    {"type":"text","text":str(submitted_study_data)},
                    {"type":"image_url","image_url":{"url":f"data:image/jpeg;base64,{base64_image0}"}},
                    {"type":"image_url","image_url":{"url":f"data:image/jpeg;base64,{base64_image1}"}},
                    {"type":"image_url","image_url":{"url":f"data:image/jpeg;base64,{base64_image2}"}},
                    {"type":"image_url","image_url":{"url":f"data:image/jpeg;base64,{base64_image3}"}},
                    {"type":"image_url","image_url":{"url":f"data:image/jpeg;base64,{base64_image4}"}},
                    {"type":"image_url","image_url":{"url":f"data:image/jpeg;base64,{base64_image5}"}},
                    {"type":"image_url","image_url":{"url":f"data:image/jpeg;base64,{base64_image6}"}},
                    {"type":"image_url","image_url":{"url":f"data:image/jpeg;base64,{base64_image7}"}},
                    {"type":"image_url","image_url":{"url":f"data:image/jpeg;base64,{base64_image8}"}},
                    {"type":"image_url","image_url":{"url":f"data:image/jpeg;base64,{base64_image9}"}},
                    ]
                }
            ],
        max_tokens=2500
        )
    consent_draft_content = response.choices[0].message.content
    return consent_draft_content

def create_consent_draft(example_project_details,submitted_study_data):
    with st.spinner("Working on your draft..."):

        # api call to generate draft
        num_values_submitted = len([x for x in submitted_study_data.values()])
        original_filename = "data/output/original_api_output.txt"
        if num_values_submitted > 20:    
            template_draft_content = generate_consent_draft(client,
                                                        system_message,
                                                        user_message,
                                                        submitted_study_data)
            # save api output
            save_to_file(original_filename,template_draft_content)
            
        else:
            st.write(":red[You did not provide enough details, the following is a sample draft!]")
            with open(original_filename,'r') as f:
                template_draft_content = f.read()
        
        st.write("Based on the information provided, I have generated \
            the following consent template draft for your project. \
                Review this output and make as much changes as you need. Once everything looks good, \
                    use the :green[Preview & Download] button to preview the document and download it.\
                        You can :red[Regenerate] the draft if you're not happy with the draft.")
        st.write("")
         

        
        # save original content to pdf
        html_response = markdown.markdown(template_draft_content,output_format="html")
        
        # st.text_area("html value", value=html_response,height=1000)
            
        pdf_doc1 = MarkdownPdf()
        pdf_doc1.add_section(Section(html_response,toc=False))
        pdf_doc1.save("data/output/Consent Template Draft_Original.pdf")
        
        # preview_consent_draft(template_draft_content)
            
        with st.container(height=480):
            updated_template_draft_content = template_draft_content.replace("```","").replace("markdown","")
            updated_draft_content = st.text_area(label="output preview",
                                                 value=updated_template_draft_content,
                                                 height=380,label_visibility="hidden")
            
            # save draft content to file
            updated_output_filename = "data/output/updated_api_output.txt"
            updated_output_md = "data/output/updated_api_output_md.md"
            save_to_file(updated_output_filename,updated_draft_content) 
            save_to_file(updated_output_md,updated_draft_content)
            
            # convert to word document and html
            template_doc = Markdown2docx('data/output/updated_api_output_md')
            template_doc.eat_soup()
            template_doc.write_html()
            template_doc.save()
            html_filename = "data/output/updated_api_output_md.html"
            with open(html_filename,'r') as f:
                html_doc = f.read()
                html_doc = markdown.markdown(html_doc)

        
        
            # save file to pdf
            # html_response = markdown.markdown(updated_draft_content)
            template_css = """
                        body {
                            fontfamily: open-sans;
                            fontsize: 8;
                            }
                            """
            
            pdf_doc = MarkdownPdf()
            pdf_doc.add_section(Section(html_doc,toc=False),
                                user_css=template_css)
            pdf_doc.save("data/output/Consent_Template_Draft_Final.pdf")

# load submitted data
# serialize session state values
session_vals = [x for x in session_state.values()]
session_keys = [x for x in session_state.keys()]
session_fields_dict = dict(zip(session_keys,session_vals))

submitted_study_data = {}
for k, v in submitted_study_data.items():
    if v:
        session_fields_dict[k] = v
        

# load saved data
with open("data/input/submitted_project_details.txt") as f:
    example_project_details = json.load(f)

create_consent_draft(example_project_details, submitted_study_data)

col1, col2,col3,col4 = st.columns(4)
with col1:
    if st.button(":red[Back]"):
        st.switch_page("pages/4_Contact_Details.py")

with col2:
    if st.button(":orange[Regenerate Draft]"):
        st.rerun()
        
with col4:
    preview_button =  st.button(":green[Preview & Download]")
    if preview_button:
        # preview pdf
        pdf_output_file = "data/output/Consent_Template_Draft_Final.pdf"
        docx_output_file = "data/output/updated_api_output_md.docx"
        displayPDF(pdf_output_file, docx_output_file)