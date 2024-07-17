import streamlit as st

st.image("static/ipa_20_cover.png")
         
def main():
    st.title("Consent Template Generator")
    st.write("Welcome to IPA's Consent Template Generator")
    st.write("Please click on the :red[**Next**] button below to proceed to fill in your research study information")
    
    if st.button(":red[Next]"):
        st.switch_page("pages/1_General_Information.py")
    
if __name__ == "__main__":
    main()